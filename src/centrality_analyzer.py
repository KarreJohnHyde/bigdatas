"""
Centrality Analysis Module for Facebook Social Network
Calculates degree, betweenness, closeness, and eigenvector centrality
"""

import networkx as nx
import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple
import time

logger = logging.getLogger(__name__)

class CentralityAnalyzer:
    """Analyzes centrality measures for social network analysis"""
    
    def __init__(self, G: nx.Graph):
        """Initialize with a NetworkX graph"""
        self.G = G
        self.results = {}
        
    def calculate_degree_centrality(self) -> Dict[int, float]:
        """Calculate degree centrality for all nodes"""
        logger.info("Calculating degree centrality...")
        start_time = time.time()
        
        degree_centrality = nx.degree_centrality(self.G)
        
        execution_time = time.time() - start_time
        logger.info(f"Degree centrality calculated in {execution_time:.3f} seconds")
        
        self.results['degree_centrality'] = degree_centrality
        return degree_centrality
    
    def calculate_betweenness_centrality(self, sample_size: int = None) -> Dict[int, float]:
        """Calculate betweenness centrality (optionally with sampling for large networks)"""
        logger.info("Calculating betweenness centrality...")
        start_time = time.time()
        
        if sample_size and len(self.G.nodes()) > sample_size:
            # Sample nodes for faster computation on large networks
            sample_nodes = np.random.choice(list(self.G.nodes()), sample_size, replace=False)
            betweenness_centrality = nx.betweenness_centrality(self.G, k=sample_size)
            logger.info(f"Used sampling with {sample_size} nodes for faster computation")
        else:
            betweenness_centrality = nx.betweenness_centrality(self.G)
        
        execution_time = time.time() - start_time
        logger.info(f"Betweenness centrality calculated in {execution_time:.3f} seconds")
        
        self.results['betweenness_centrality'] = betweenness_centrality
        return betweenness_centrality
    
    def calculate_closeness_centrality(self) -> Dict[int, float]:
        """Calculate closeness centrality for all nodes"""
        logger.info("Calculating closeness centrality...")
        start_time = time.time()
        
        closeness_centrality = nx.closeness_centrality(self.G)
        
        execution_time = time.time() - start_time
        logger.info(f"Closeness centrality calculated in {execution_time:.3f} seconds")
        
        self.results['closeness_centrality'] = closeness_centrality
        return closeness_centrality
    
    def calculate_eigenvector_centrality(self, max_iter: int = 1000) -> Dict[int, float]:
        """Calculate eigenvector centrality with convergence control"""
        logger.info("Calculating eigenvector centrality...")
        start_time = time.time()
        
        try:
            eigenvector_centrality = nx.eigenvector_centrality(self.G, max_iter=max_iter)
            logger.info("Eigenvector centrality calculated successfully")
        except nx.PowerIterationFailedConvergence:
            logger.warning("Eigenvector centrality failed to converge, using power iteration")
            eigenvector_centrality = nx.power_iteration(self.G, max_iter=max_iter)
        
        execution_time = time.time() - start_time
        logger.info(f"Eigenvector centrality calculated in {execution_time:.3f} seconds")
        
        self.results['eigenvector_centrality'] = eigenvector_centrality
        return eigenvector_centrality
    
    def calculate_all_centralities(self, sample_size: int = None) -> Dict[str, Dict[int, float]]:
        """Calculate all centrality measures"""
        logger.info("Calculating all centrality measures...")
        
        # Calculate all centralities
        self.calculate_degree_centrality()
        self.calculate_betweenness_centrality(sample_size)
        self.calculate_closeness_centrality()
        self.calculate_eigenvector_centrality()
        
        logger.info("All centrality measures calculated successfully")
        return self.results
    
    def get_top_users(self, centrality_type: str, top_n: int = 10) -> List[Tuple[int, float]]:
        """Get top N users by centrality measure"""
        if centrality_type not in self.results:
            raise ValueError(f"Centrality type '{centrality_type}' not calculated yet")
        
        centrality_dict = self.results[centrality_type]
        sorted_users = sorted(centrality_dict.items(), key=lambda x: x[1], reverse=True)
        return sorted_users[:top_n]
    
    def get_centrality_summary(self) -> pd.DataFrame:
        """Create a summary DataFrame of all centrality measures"""
        if not self.results:
            raise ValueError("No centrality measures calculated yet. Run calculate_all_centralities() first.")
        
        # Create DataFrame
        df = pd.DataFrame(self.results)
        df.index.name = 'user_id'
        
        # Add basic statistics
        summary_stats = df.describe()
        
        return df, summary_stats
    
    def identify_influential_users(self, top_n: int = 20) -> Dict[str, List[Tuple[int, float]]]:
        """Identify the most influential users across all centrality measures"""
        if not self.results:
            raise ValueError("No centrality measures calculated yet")
        
        influential_users = {}
        
        for centrality_type in self.results.keys():
            top_users = self.get_top_users(centrality_type, top_n)
            influential_users[centrality_type] = top_users
            
            logger.info(f"\nTop {top_n} users by {centrality_type}:")
            for i, (user_id, score) in enumerate(top_users[:5], 1):
                logger.info(f"  {i}. User {user_id}: {score:.4f}")
        
        return influential_users
    
    def export_results(self, filename: str = "centrality_results.csv"):
        """Export centrality results to CSV"""
        if not self.results:
            raise ValueError("No centrality measures calculated yet")
        
        df, _ = self.get_centrality_summary()
        df.to_csv(filename)
        logger.info(f"Centrality results exported to {filename}")
        
        return filename

def main():
    """Test the centrality analyzer"""
    from data_loader import FacebookDataLoader
    
    # Load data
    loader = FacebookDataLoader()
    G = loader.load_facebook_network()
    
    # Create analyzer
    analyzer = CentralityAnalyzer(G)
    
    # Calculate all centralities
    results = analyzer.calculate_all_centralities()
    
    # Get top influential users
    influential_users = analyzer.identify_influential_users(top_n=10)
    
    # Export results
    analyzer.export_results("data/results/centrality_analysis.csv")
    
    print("\n🎉 Centrality Analysis Completed Successfully!")
    print("📊 Results exported to data/results/centrality_analysis.csv")

if __name__ == "__main__":
    main() 