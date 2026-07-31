"""
Visualization Module for Facebook Social Network Analysis
Creates interactive network plots, centrality charts, and community visualizations
"""

import networkx as nx
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple, Optional
import os
from pathlib import Path

# Configure matplotlib
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

logger = logging.getLogger(__name__)

class NetworkVisualizer:
    """Creates comprehensive visualizations for social network analysis"""
    
    def __init__(self, G: nx.Graph, output_dir: str = "data/results"):
        """Initialize with a NetworkX graph and output directory"""
        self.G = G
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set color schemes
        self.colors = px.colors.qualitative.Set3
        
    def create_network_overview_plot(self, max_nodes: int = 1000) -> str:
        """Create an overview plot of the network structure"""
        logger.info("Creating network overview plot...")
        
        # Sample nodes if network is too large
        if len(self.G.nodes()) > max_nodes:
            sample_nodes = np.random.choice(list(self.G.nodes()), max_nodes, replace=False)
            G_sample = self.G.subgraph(sample_nodes)
            logger.info(f"Sampled {max_nodes} nodes for visualization")
        else:
            G_sample = self.G
        
        # Calculate layout
        pos = nx.spring_layout(G_sample, k=1, iterations=50, seed=42)
        
        # Create plot
        plt.figure(figsize=(12, 10))
        
        # Draw edges
        nx.draw_networkx_edges(G_sample, pos, alpha=0.3, edge_color='gray', width=0.5)
        
        # Draw nodes with size based on degree
        degrees = dict(G_sample.degree())
        node_sizes = [degrees[node] * 10 for node in G_sample.nodes()]
        
        nx.draw_networkx_nodes(G_sample, pos, 
                              node_size=node_sizes,
                              node_color='lightblue',
                              alpha=0.7)
        
        # Add labels for high-degree nodes
        high_degree_nodes = {node: degree for node, degree in degrees.items() if degree > 50}
        nx.draw_networkx_labels(G_sample, pos, 
                               labels=high_degree_nodes,
                               font_size=8,
                               font_weight='bold')
        
        plt.title(f"Facebook Social Network Overview\n{len(G_sample.nodes())} users, {len(G_sample.edges())} connections", 
                 fontsize=16, fontweight='bold')
        plt.axis('off')
        
        # Save plot
        filename = self.output_dir / "network_overview.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Network overview plot saved to {filename}")
        return str(filename)
    
    def create_centrality_comparison_plot(self, centrality_results: Dict) -> str:
        """Create comparison plots for different centrality measures"""
        logger.info("Creating centrality comparison plots...")
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=['Degree Centrality', 'Betweenness Centrality', 
                          'Closeness Centrality', 'Eigenvector Centrality'],
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        centrality_types = ['degree_centrality', 'betweenness_centrality', 
                           'closeness_centrality', 'eigenvector_centrality']
        
        for i, centrality_type in enumerate(centrality_types):
            if centrality_type in centrality_results:
                values = list(centrality_results[centrality_type].values())
                values.sort(reverse=True)
                
                row = (i // 2) + 1
                col = (i % 2) + 1
                
                fig.add_trace(
                    go.Scatter(x=list(range(len(values))), y=values,
                              mode='lines+markers',
                              name=centrality_type.replace('_', ' ').title(),
                              line=dict(width=2),
                              marker=dict(size=6)),
                    row=row, col=col
                )
        
        fig.update_layout(
            title="Centrality Measures Comparison",
            height=800,
            showlegend=False
        )
        
        # Save plot
        filename = self.output_dir / "centrality_comparison.html"
        fig.write_html(str(filename))
        
        logger.info(f"Centrality comparison plot saved to {filename}")
        return str(filename)
    
    def create_community_visualization(self, community_labels: Dict[int, int], 
                                     method: str = 'louvain') -> str:
        """Create visualization of detected communities"""
        logger.info(f"Creating community visualization for {method} method...")
        
        # Sample nodes if network is too large
        if len(self.G.nodes()) > 1000:
            sample_nodes = np.random.choice(list(self.G.nodes()), 1000, replace=False)
            G_sample = self.G.subgraph(sample_nodes)
            sample_labels = {node: community_labels.get(node, -1) for node in sample_nodes}
            logger.info(f"Sampled 1000 nodes for community visualization")
        else:
            G_sample = self.G
            sample_labels = community_labels
        
        # Calculate layout
        pos = nx.spring_layout(G_sample, k=1, iterations=50, seed=42)
        
        # Create plot
        plt.figure(figsize=(14, 12))
        
        # Get unique communities
        unique_communities = set(sample_labels.values())
        colors = plt.cm.tab20(np.linspace(0, 1, len(unique_communities)))
        
        # Draw communities
        for i, community_id in enumerate(unique_communities):
            if community_id == -1:
                continue
                
            community_nodes = [node for node, comm in sample_labels.items() if comm == community_id]
            
            if community_nodes:
                nx.draw_networkx_nodes(G_sample, pos,
                                      nodelist=community_nodes,
                                      node_color=[colors[i]],
                                      node_size=50,
                                      alpha=0.8,
                                      label=f'Community {community_id}')
        
        # Draw edges
        nx.draw_networkx_edges(G_sample, pos, alpha=0.2, edge_color='gray', width=0.3)
        
        plt.title(f"Community Detection Results - {method.title()} Method\n"
                 f"{len(unique_communities)} communities detected", 
                 fontsize=16, fontweight='bold')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.axis('off')
        
        # Save plot
        filename = self.output_dir / f"community_visualization_{method}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Community visualization saved to {filename}")
        return str(filename)
    
    def create_degree_distribution_plot(self) -> str:
        """Create degree distribution plot"""
        logger.info("Creating degree distribution plot...")
        
        degrees = [d for n, d in self.G.degree()]
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=['Degree Distribution', 'Log-Log Degree Distribution'],
            specs=[[{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Regular degree distribution
        fig.add_trace(
            go.Histogram(x=degrees, nbinsx=50, name='Degree Distribution',
                        marker_color='lightblue'),
            row=1, col=1
        )
        
        # Log-log degree distribution
        degree_counts = pd.Series(degrees).value_counts().sort_index()
        fig.add_trace(
            go.Scatter(x=degree_counts.index, y=degree_counts.values,
                      mode='lines+markers', name='Log-Log Distribution',
                      line=dict(width=2)),
            row=1, col=2
        )
        
        fig.update_xaxes(type="log", title="Degree")
        fig.update_yaxes(type="log", title="Count")
        
        fig.update_layout(
            title="Facebook Network Degree Distribution",
            height=500,
            showlegend=False
        )
        
        # Save plot
        filename = self.output_dir / "degree_distribution.html"
        fig.write_html(str(filename))
        
        logger.info(f"Degree distribution plot saved to {filename}")
        return str(filename)
    
    def create_network_metrics_dashboard(self, centrality_results: Dict, 
                                       community_results: Dict) -> str:
        """Create a comprehensive dashboard of network metrics"""
        logger.info("Creating network metrics dashboard...")
        
        # Calculate basic metrics
        metrics = {
            'Total Nodes': self.G.number_of_nodes(),
            'Total Edges': self.G.number_of_edges(),
            'Density': nx.density(self.G),
            'Average Degree': sum(dict(self.G.degree()).values()) / self.G.number_of_nodes(),
            'Diameter': nx.diameter(self.G) if nx.is_connected(self.G) else 'Disconnected',
            'Clustering Coefficient': nx.average_clustering(self.G)
        }
        
        # Create metrics table
        fig = go.Figure(data=[go.Table(
            header=dict(values=['Metric', 'Value'],
                       fill_color='lightblue',
                       align='left',
                       font=dict(size=14, color='black')),
            cells=dict(values=[list(metrics.keys()), list(metrics.values())],
                      fill_color='white',
                      align='left',
                      font=dict(size=12))
        )])
        
        fig.update_layout(
            title="Facebook Network Metrics Dashboard",
            height=400
        )
        
        # Save dashboard
        filename = self.output_dir / "network_metrics_dashboard.html"
        fig.write_html(str(filename))
        
        logger.info(f"Network metrics dashboard saved to {filename}")
        return str(filename)
    
    def create_interactive_network_plot(self, max_nodes: int = 500) -> str:
        """Create an interactive network plot using Plotly"""
        logger.info("Creating interactive network plot...")
        
        # Sample nodes if network is too large
        if len(self.G.nodes()) > max_nodes:
            sample_nodes = np.random.choice(list(self.G.nodes()), max_nodes, replace=False)
            G_sample = self.G.subgraph(sample_nodes)
            logger.info(f"Sampled {max_nodes} nodes for interactive visualization")
        else:
            G_sample = self.G
        
        # Calculate layout
        pos = nx.spring_layout(G_sample, k=1, iterations=50, seed=42)
        
        # Prepare edge traces
        edge_x = []
        edge_y = []
        for edge in G_sample.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')
        
        # Prepare node traces
        node_x = []
        node_y = []
        node_text = []
        node_size = []
        
        degrees = dict(G_sample.degree())
        for node in G_sample.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(f'User {node}<br>Degree: {degrees[node]}')
            node_size.append(max(5, degrees[node] * 2))
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            text=node_text,
            marker=dict(
                size=node_size,
                color=node_size,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Node Degree")
            ))
        
        # Create layout
        layout = go.Layout(
            title=f'Interactive Facebook Social Network<br>{len(G_sample.nodes())} users, {len(G_sample.edges())} connections',
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )
        
        # Create figure
        fig = go.Figure(data=[edge_trace, node_trace], layout=layout)
        
        # Save plot
        filename = self.output_dir / "interactive_network.html"
        fig.write_html(str(filename))
        
        logger.info(f"Interactive network plot saved to {filename}")
        return str(filename)
    
    def create_all_visualizations(self, centrality_results: Dict = None, 
                                 community_results: Dict = None) -> Dict[str, str]:
        """Create all available visualizations"""
        logger.info("Creating all visualizations...")
        
        visualizations = {}
        
        # Basic network plots
        visualizations['overview'] = self.create_network_overview_plot()
        visualizations['degree_distribution'] = self.create_degree_distribution_plot()
        visualizations['interactive'] = self.create_interactive_network_plot()
        
        # Advanced plots if data available
        if centrality_results:
            visualizations['centrality'] = self.create_centrality_comparison_plot(centrality_results)
            visualizations['metrics_dashboard'] = self.create_network_metrics_dashboard(centrality_results, {})
        
        if community_results:
            for method in community_results.keys():
                if 'labels' in community_results[method]:
                    visualizations[f'community_{method}'] = self.create_community_visualization(
                        community_results[method]['labels'], method)
        
        logger.info(f"Created {len(visualizations)} visualizations")
        return visualizations

def main():
    """Test the visualizer"""
    from data_loader import FacebookDataLoader
    
    # Load data
    loader = FacebookDataLoader()
    G = loader.load_facebook_network()
    
    # Create visualizer
    visualizer = NetworkVisualizer(G)
    
    # Create all visualizations
    visualizations = visualizer.create_all_visualizations()
    
    print("\n🎉 All Visualizations Created Successfully!")
    print("📊 Generated files:")
    for name, path in visualizations.items():
        print(f"   {name}: {path}")

if __name__ == "__main__":
    main() 