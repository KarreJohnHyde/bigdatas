"""
Data Loader Module for Facebook Social Network Analysis
Efficiently loads and preprocesses large social network datasets
"""

import pandas as pd
import numpy as np
import networkx as nx
from pathlib import Path
import logging
from typing import Tuple, Dict, Any
import yaml

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FacebookDataLoader:
    """Efficient data loader for Facebook social network datasets"""
    
    def __init__(self, config_path: str = None):
        """Initialize the data loader with configuration"""
        if config_path is None:
            # Try to find config file in multiple locations
            possible_paths = [
                "config/settings.yaml",
                "../config/settings.yaml",
                "../../config/settings.yaml"
            ]
            
            config_path = None
            for path in possible_paths:
                if Path(path).exists():
                    config_path = path
                    break
            
            if config_path is None:
                # Use default config if no file found
                logger.warning("No config file found, using default settings")
                self.config = self.get_default_config()
                return
        
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        """Initialize the data loader with configuration"""
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        
        self.data_config = self.config['data']
        self.performance_config = self.config['performance']
    
    def get_default_config(self):
        """Get default configuration if no config file is found"""
        return {
            'data': {
                'input_file': "data/raw/facebook_combined.txt",
                'ego_folder': "data/raw/facebook/",
                'output_dir': "data/results/",
                'processed_dir': "data/processed/"
            },
            'performance': {
                'max_memory_gb': 8,
                'chunk_size': 10000,
                'parallel_processing': True,
                'num_workers': 4
            }
        }
        
    def load_facebook_network(self) -> nx.Graph:
        """
        Load the main Facebook network from facebook_combined.txt
        Returns: NetworkX graph object
        """
        logger.info("Loading Facebook social network...")
        
        # Try multiple possible paths for the input file
        possible_input_paths = [
            self.data_config['input_file'],
            f"../{self.data_config['input_file']}",
            f"../../{self.data_config['input_file']}"
        ]
        
        input_file = None
        for path in possible_input_paths:
            if Path(path).exists():
                input_file = Path(path)
                break
        
        if not input_file:
            raise FileNotFoundError(f"Facebook data file not found in any of these locations: {possible_input_paths}")
        
        # Load edge data efficiently
        edges_df = pd.read_csv(
            input_file, 
            sep=' ', 
            header=None, 
            names=['source', 'target'],
            dtype={'source': int, 'target': int}
        )
        
        logger.info(f"Loaded {len(edges_df)} edges from {edges_df['source'].nunique()} unique users")
        
        # Create NetworkX graph
        G = nx.from_edgelist(edges_df.values.tolist())
        
        # Add basic node attributes
        G.graph['name'] = 'Facebook Social Network'
        G.graph['source'] = 'Stanford SNAP Dataset'
        
        logger.info(f"Graph created with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
        
        return G
    
    def load_ego_networks(self) -> Dict[int, nx.Graph]:
        """
        Load individual ego networks from the facebook/ folder
        Returns: Dictionary of ego networks
        """
        logger.info("Loading ego networks...")
        
        # Try multiple possible paths for the ego folder
        possible_ego_paths = [
            self.data_config['ego_folder'],
            f"../{self.data_config['ego_folder']}",
            f"../../{self.data_config['ego_folder']}"
        ]
        
        ego_folder = None
        for path in possible_ego_paths:
            if Path(path).exists():
                ego_folder = Path(path)
                break
        
        if not ego_folder:
            logger.warning("Ego networks folder not found, skipping...")
            return {}
        
        ego_networks = {}
        
        # Load each ego network
        for ego_file in ego_folder.glob("*.egonet"):
            ego_id = int(ego_file.stem)
            
            with open(ego_file, 'r') as f:
                lines = f.readlines()
            
            # Parse ego network structure
            ego_network = nx.Graph()
            ego_network.graph['ego_id'] = ego_id
            
            # Add ego node
            ego_network.add_node(ego_id)
            
            # Parse connections
            for line in lines:
                if line.strip():
                    parts = line.strip().split()
                    if len(parts) > 1:
                        ego_network.add_node(int(parts[0]))
                        for neighbor in parts[1:]:
                            ego_network.add_edge(int(parts[0]), int(neighbor))
            
            ego_networks[ego_id] = ego_network
            logger.info(f"Loaded ego network {ego_id} with {ego_network.number_of_nodes()} nodes")
        
        return ego_networks
    
    def load_node_features(self) -> pd.DataFrame:
        """
        Load node features and attributes
        Returns: DataFrame with node features
        """
        logger.info("Loading node features...")
        
        # Try multiple possible paths for the ego folder
        possible_ego_paths = [
            self.data_config['ego_folder'],
            f"../{self.data_config['ego_folder']}",
            f"../../{self.data_config['ego_folder']}"
        ]
        
        ego_folder = None
        for path in possible_ego_paths:
            if Path(path).exists():
                ego_folder = Path(path)
                break
        
        if not ego_folder:
            logger.warning("Ego networks folder not found, skipping node features...")
            return pd.DataFrame()
        
        # Look for feature files
        feature_files = list(ego_folder.glob("*.feat"))
        if not feature_files:
            logger.warning("No feature files found")
            return pd.DataFrame()
        
        # Load first feature file as example
        feature_file = feature_files[0]
        features_df = pd.read_csv(
            feature_file, 
            sep=' ', 
            header=None,
            dtype=int
        )
        
        # Set column names - first column is node_id, rest are features
        num_features = len(features_df.columns) - 1
        feature_names = [f"feature_{i}" for i in range(num_features)]
        features_df.columns = ['node_id'] + feature_names
        
        logger.info(f"Loaded features for {len(features_df)} nodes")
        return features_df
    
    def validate_data(self, G: nx.Graph) -> bool:
        """
        Validate the loaded graph data
        Returns: True if valid, False otherwise
        """
        logger.info("Validating graph data...")
        
        # Check basic properties
        if G.number_of_nodes() == 0:
            logger.error("Graph has no nodes")
            return False
        
        if G.number_of_edges() == 0:
            logger.error("Graph has no edges")
            return False
        
        # Check for isolated nodes
        isolated_nodes = list(nx.isolates(G))
        if isolated_nodes:
            logger.warning(f"Found {len(isolated_nodes)} isolated nodes")
        
        # Check connectivity
        if not nx.is_connected(G):
            components = list(nx.connected_components(G))
            logger.info(f"Graph has {len(components)} connected components")
            largest_component = max(components, key=len)
            logger.info(f"Largest component has {len(largest_component)} nodes")
        
        logger.info("Data validation completed successfully")
        return True
    
    def get_data_summary(self, G: nx.Graph) -> Dict[str, Any]:
        """
        Get comprehensive summary of the loaded data
        Returns: Dictionary with data statistics
        """
        summary = {
            'total_nodes': G.number_of_nodes(),
            'total_edges': G.number_of_edges(),
            'is_connected': nx.is_connected(G),
            'is_directed': G.is_directed(),
            'is_weighted': nx.is_weighted(G),
            'density': nx.density(G),
            'average_degree': sum(dict(G.degree()).values()) / G.number_of_nodes(),
            'max_degree': max(dict(G.degree()).values()),
            'min_degree': min(dict(G.degree()).values())
        }
        
        if not nx.is_connected(G):
            components = list(nx.connected_components(G))
            summary['num_components'] = len(components)
            summary['largest_component_size'] = len(max(components, key=len))
        
        return summary

def main():
    """Test the data loader"""
    loader = FacebookDataLoader()
    
    # Load main network
    G = loader.load_facebook_network()
    
    # Validate data
    if loader.validate_data(G):
        # Get summary
        summary = loader.get_data_summary(G)
        print("\n=== Facebook Network Summary ===")
        for key, value in summary.items():
            print(f"{key}: {value}")
        
        # Load ego networks
        ego_networks = loader.load_ego_networks()
        print(f"\nLoaded {len(ego_networks)} ego networks")
        
        # Load node features
        features = loader.load_node_features()
        if not features.empty:
            print(f"Loaded features for {len(features)} nodes")

if __name__ == "__main__":
    main() 