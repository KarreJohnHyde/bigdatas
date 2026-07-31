"""
Community Detection Module for Facebook Social Network
Identifies natural friend groups and communities using multiple algorithms
"""

import networkx as nx
import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple, Set
import time
from collections import defaultdict

logger = logging.getLogger(__name__)

class CommunityDetector:
    """Detects communities in social networks using multiple algorithms"""
    
    def __init__(self, G: nx.Graph):
        """Initialize with a NetworkX graph"""
        self.G = G
        self.results = {}
        
    def detect_louvain_communities(self) -> Dict[int, int]:
        """Detect communities using Louvain method (fast and effective)"""
        logger.info("Detecting communities using Louvain method...")
        start_time = time.time()
        
        try:
            # Use community detection from networkx
            communities = nx.community.louvain_communities(self.G, seed=42)
            
            # Create node-to-community mapping
            community_labels = {}
            for i, community in enumerate(communities):
                for node in community:
                    community_labels[node] = i
            
            execution_time = time.time() - start_time
            logger.info(f"Louvain communities detected in {execution_time:.3f} seconds")
            logger.info(f"Found {len(communities)} communities")
            
            # Calculate modularity
            modularity = nx.community.modularity(self.G, communities)
            
            # Analyze community structure
            community_sizes = [len(comm) for comm in communities]
            analysis = {
                'num_communities': len(communities),
                'community_sizes': community_sizes,
                'largest_community': max(community_sizes),
                'smallest_community': min(community_sizes),
                'avg_community_size': np.mean(community_sizes),
                'community_size_distribution': {}
            }
            
            # Analyze size distribution
            size_counts = defaultdict(int)
            for size in community_sizes:
                size_counts[size] += 1
            analysis['community_size_distribution'] = dict(size_counts)
            
            self.results['louvain'] = {
                'communities': communities,
                'labels': community_labels,
                'num_communities': len(communities),
                'insights': {
                    'modularity': modularity,
                    'analysis': analysis
                }
            }
            
            return community_labels
            
        except Exception as e:
            logger.error(f"Louvain method failed: {e}")
            return {}
    
    def detect_label_propagation_communities(self) -> Dict[int, int]:
        """Detect communities using label propagation algorithm"""
        logger.info("Detecting communities using label propagation...")
        start_time = time.time()
        
        try:
            communities = nx.community.label_propagation_communities(self.G)
            
            # Create node-to-community mapping
            community_labels = {}
            for i, community in enumerate(communities):
                for node in community:
                    community_labels[node] = i
            
            execution_time = time.time() - start_time
            logger.info(f"Label propagation communities detected in {execution_time:.3f} seconds")
            logger.info(f"Found {len(communities)} communities")
            
            # Calculate modularity
            modularity = nx.community.modularity(self.G, communities)
            
            # Analyze community structure
            community_sizes = [len(comm) for comm in communities]
            analysis = {
                'num_communities': len(communities),
                'community_sizes': community_sizes,
                'largest_community': max(community_sizes),
                'smallest_community': min(community_sizes),
                'avg_community_size': np.mean(community_sizes),
                'community_size_distribution': {}
            }
            
            # Analyze size distribution
            size_counts = defaultdict(int)
            for size in community_sizes:
                size_counts[size] += 1
            analysis['community_size_distribution'] = dict(size_counts)
            
            self.results['label_propagation'] = {
                'communities': communities,
                'labels': community_labels,
                'num_communities': len(communities),
                'insights': {
                    'modularity': modularity,
                    'analysis': analysis
                }
            }
            
            return community_labels
            
        except Exception as e:
            logger.error(f"Label propagation failed: {e}")
            return {}
    
    def detect_greedy_modularity_communities(self) -> Dict[int, int]:
        """Detect communities using greedy modularity optimization"""
        logger.info("Detecting communities using greedy modularity...")
        start_time = time.time()
        
        try:
            communities = nx.community.greedy_modularity_communities(self.G)
            
            # Create node-to-community mapping
            community_labels = {}
            for i, community in enumerate(communities):
                for node in community:
                    community_labels[node] = i
            
            execution_time = time.time() - start_time
            logger.info(f"Greedy modularity communities detected in {execution_time:.3f} seconds")
            logger.info(f"Found {len(communities)} communities")
            
            # Calculate modularity
            modularity = nx.community.modularity(self.G, communities)
            
            # Analyze community structure
            community_sizes = [len(comm) for comm in communities]
            analysis = {
                'num_communities': len(communities),
                'community_sizes': community_sizes,
                'largest_community': max(community_sizes),
                'smallest_community': min(community_sizes),
                'avg_community_size': np.mean(community_sizes),
                'community_size_distribution': {}
            }
            
            # Analyze size distribution
            size_counts = defaultdict(int)
            for size in community_sizes:
                size_counts[size] += 1
            analysis['community_size_distribution'] = dict(size_counts)
            
            self.results['greedy_modularity'] = {
                'communities': communities,
                'labels': community_labels,
                'num_communities': len(communities),
                'insights': {
                    'modularity': modularity,
                    'analysis': analysis
                }
            }
            
            return community_labels
            
        except Exception as e:
            logger.error(f"Greedy modularity failed: {e}")
            return {}
    
    def detect_all_communities(self) -> Dict[str, Dict]:
        """Detect communities using all available methods"""
        logger.info("Detecting communities using all methods...")
        
        # Detect communities with different methods
        self.detect_louvain_communities()
        self.detect_label_propagation_communities()
        self.detect_greedy_modularity_communities()
        
        logger.info("All community detection methods completed")
        return self.results
    
    def analyze_community_structure(self, method: str = 'louvain') -> Dict:
        """Analyze the structure of detected communities"""
        if method not in self.results:
            raise ValueError(f"Method '{method}' not available. Run detect_all_communities() first.")
        
        communities_data = self.results[method]
        communities = communities_data['communities']
        
        analysis = {
            'num_communities': len(communities),
            'community_sizes': [len(comm) for comm in communities],
            'largest_community': max(len(comm) for comm in communities),
            'smallest_community': min(len(comm) for comm in communities),
            'avg_community_size': np.mean([len(comm) for comm in communities]),
            'community_size_distribution': {}
        }
        
        # Analyze size distribution
        size_counts = defaultdict(int)
        for size in analysis['community_sizes']:
            size_counts[size] += 1
        
        analysis['community_size_distribution'] = dict(size_counts)
        
        return analysis
    
    def get_community_members(self, method: str = 'louvain', community_id: int = 0) -> Set[int]:
        """Get members of a specific community"""
        if method not in self.results:
            raise ValueError(f"Method '{method}' not available")
        
        communities = self.results[method]['communities']
        if community_id >= len(communities):
            raise ValueError(f"Community ID {community_id} not found")
        
        return communities[community_id]
    
    def calculate_community_modularity(self, method: str = 'louvain') -> float:
        """Calculate modularity of detected communities"""
        if method not in self.results:
            raise ValueError(f"Method '{method}' not available")
        
        communities = self.results[method]['communities']
        modularity = nx.community.modularity(self.G, communities)
        
        logger.info(f"Modularity for {method}: {modularity:.4f}")
        return modularity
    
    def get_community_summary(self) -> pd.DataFrame:
        """Create a summary of all detected communities"""
        if not self.results:
            raise ValueError("No communities detected yet")
        
        summary_data = []
        
        for method, data in self.results.items():
            communities = data['communities']
            
            for i, community in enumerate(communities):
                summary_data.append({
                    'method': method,
                    'community_id': i,
                    'size': len(community),
                    'members': list(community)
                })
        
        df = pd.DataFrame(summary_data)
        return df
    
    def export_communities(self, filename: str = "community_detection.csv"):
        """Export community detection results"""
        if not self.results:
            raise ValueError("No communities detected yet")
        
        df = self.get_community_summary()
        df.to_csv(filename, index=False)
        logger.info(f"Community results exported to {filename}")
        
        return filename
    
    def get_community_insights(self) -> Dict[str, any]:
        """Get comprehensive insights about detected communities"""
        insights = {}
        
        for method in self.results.keys():
            analysis = self.analyze_community_structure(method)
            modularity = self.calculate_community_modularity(method)
            
            insights[method] = {
                'analysis': analysis,
                'modularity': modularity,
                'top_communities': sorted(
                    [(i, len(comm)) for i, comm in enumerate(self.results[method]['communities'])],
                    key=lambda x: x[1], reverse=True
                )[:5]
            }
        
        return insights

def main():
    """Test the community detector"""
    from data_loader import FacebookDataLoader
    
    # Load data
    loader = FacebookDataLoader()
    G = loader.load_facebook_network()
    
    # Create detector
    detector = CommunityDetector(G)
    
    # Detect all communities
    results = detector.detect_all_communities()
    
    # Get insights
    insights = detector.get_community_insights()
    
    # Export results
    detector.export_communities("data/results/community_detection.csv")
    
    print("\n🎉 Community Detection Completed Successfully!")
    print("📊 Results exported to data/results/community_detection.csv")
    
    # Print summary
    for method, data in insights.items():
        print(f"\n📈 {method.upper()} Method:")
        print(f"   Communities: {data['analysis']['num_communities']}")
        print(f"   Modularity: {data['modularity']:.4f}")
        print(f"   Average size: {data['analysis']['avg_community_size']:.1f}")

if __name__ == "__main__":
    main() 