"""
Advanced Analytics Module for Facebook Social Network Analysis
- Comparative Benchmarking
- Statistical Significance Testing  
- Network Efficiency Metrics
- Faculty-Level Analysis
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import chi2_contingency, mannwhitneyu, kruskal
import pandas as pd
from pathlib import Path
import json
import time

class AdvancedAnalytics:
    def __init__(self, G, centrality_data, community_data, feature_data):
        self.G = G
        self.centrality_data = centrality_data
        self.community_data = community_data
        self.feature_data = feature_data
        self.results_dir = Path('data/results/advanced')
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
    def calculate_network_efficiency_metrics(self):
        """Calculate comprehensive network efficiency metrics"""
        print("[ADVANCED] Calculating network efficiency metrics...")
        
        metrics = {}
        
        # Basic network properties
        metrics['nodes'] = self.G.number_of_nodes()
        metrics['edges'] = self.G.number_of_edges()
        metrics['density'] = nx.density(self.G)
        metrics['clustering'] = nx.average_clustering(self.G)
        metrics['transitivity'] = nx.transitivity(self.G)
        
        # Small world properties
        try:
            # Calculate average shortest path length
            if nx.is_connected(self.G):
                metrics['avg_path_length'] = nx.average_shortest_path_length(self.G)
            else:
                # For disconnected components
                components = list(nx.connected_components(self.G))
                path_lengths = []
                for component in components:
                    if len(component) > 1:
                        subgraph = self.G.subgraph(component)
                        path_lengths.append(nx.average_shortest_path_length(subgraph))
                metrics['avg_path_length'] = np.mean(path_lengths) if path_lengths else 0
        except:
            metrics['avg_path_length'] = 0
            
        # Calculate small world coefficient properly
        try:
            if metrics['avg_path_length'] > 0 and metrics['clustering'] > 0:
                # Create random network with same density
                n = self.G.number_of_nodes()
                p = metrics['density']
                
                # Expected values for random network
                L_random = np.log(n) / np.log(p * n) if p > 0 and n > 1 else 0
                C_random = p
                
                # Small world coefficient
                if L_random > 0 and C_random > 0:
                    metrics['small_world_coefficient'] = (metrics['clustering'] / C_random) / (metrics['avg_path_length'] / L_random)
                else:
                    metrics['small_world_coefficient'] = 0
            else:
                metrics['small_world_coefficient'] = 0
        except:
            metrics['small_world_coefficient'] = 0
            
        # Network efficiency
        try:
            metrics['global_efficiency'] = nx.global_efficiency(self.G)
        except:
            metrics['global_efficiency'] = 0
            
        # Assortativity
        try:
            metrics['degree_assortativity'] = nx.degree_assortativity_coefficient(self.G)
        except:
            metrics['degree_assortativity'] = 0
            
        # Scale-free properties
        degrees = [d for n, d in self.G.degree()]
        metrics['max_degree'] = max(degrees)
        metrics['min_degree'] = min(degrees)
        metrics['avg_degree'] = np.mean(degrees)
        metrics['degree_variance'] = np.var(degrees)
        
        # Power-law fitting
        try:
            from scipy.optimize import curve_fit
            def power_law(x, a, b):
                return a * np.power(x, b)
            
            # Fit power law to degree distribution
            degree_counts = np.bincount(degrees)
            x_data = np.arange(1, len(degree_counts))
            y_data = degree_counts[1:]
            y_data = y_data[y_data > 0]
            x_data = x_data[:len(y_data)]
            
            if len(x_data) > 2 and len(y_data) > 2:
                popt, _ = curve_fit(power_law, x_data, y_data, maxfev=1000)
                metrics['power_law_exponent'] = popt[1]
                metrics['power_law_r2'] = self._calculate_r2(y_data, power_law(x_data, *popt))
            else:
                metrics['power_law_exponent'] = 0
                metrics['power_law_r2'] = 0
        except:
            metrics['power_law_exponent'] = 0
            metrics['power_law_r2'] = 0
            
        # Network robustness
        metrics['robustness_random'] = self._calculate_robustness('random')
        metrics['robustness_targeted'] = self._calculate_robustness('targeted')
        
        return metrics
    
    def _calculate_r2(self, y_actual, y_predicted):
        """Calculate R-squared value"""
        try:
            ss_res = np.sum((y_actual - y_predicted) ** 2)
            ss_tot = np.sum((y_actual - np.mean(y_actual)) ** 2)
            return 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        except:
            return 0
    
    def _calculate_robustness(self, attack_type='random'):
        """Calculate network robustness under different attack strategies"""
        try:
            if attack_type == 'random':
                # Random node removal
                nodes = list(self.G.nodes())
                np.random.shuffle(nodes)
            else:
                # Targeted attack (remove highest degree nodes first)
                nodes = sorted(self.G.degree(), key=lambda x: x[1], reverse=True)
                nodes = [n[0] for n in nodes]
            
            # Calculate robustness as area under the curve
            robustness_values = []
            temp_G = self.G.copy()
            
            for i in range(min(100, len(nodes))):  # Remove up to 100 nodes
                if nodes[i] in temp_G:
                    temp_G.remove_node(nodes[i])
                    
                # Calculate largest component size
                if temp_G.number_of_nodes() > 0:
                    largest_cc = max(nx.connected_components(temp_G), key=len)
                    robustness_values.append(len(largest_cc) / self.G.number_of_nodes())
                else:
                    robustness_values.append(0)
            
            return np.trapz(robustness_values, dx=1.0/len(robustness_values)) if robustness_values else 0
        except:
            return 0
    
    def perform_statistical_tests(self):
        """Perform comprehensive statistical significance tests"""
        print("[ADVANCED] Performing statistical significance tests...")
        
        tests = {}
        
        # Get centrality measures
        degree_centrality = self.centrality_data.get('degree_centrality', {})
        betweenness_centrality = self.centrality_data.get('betweenness_centrality', {})
        closeness_centrality = self.centrality_data.get('closeness_centrality', {})
        eigenvector_centrality = self.centrality_data.get('eigenvector_centrality', {})
        
        # Convert to lists for statistical testing
        degree_values = list(degree_centrality.values()) if degree_centrality else []
        betweenness_values = list(betweenness_centrality.values()) if betweenness_centrality else []
        closeness_values = list(closeness_centrality.values()) if closeness_centrality else []
        eigenvector_values = list(eigenvector_centrality.values()) if eigenvector_centrality else []
        
        # 1. Normality tests for centrality measures
        tests['normality'] = {}
        for name, values in [('degree', degree_values), ('betweenness', betweenness_values), 
                           ('closeness', closeness_values), ('eigenvector', eigenvector_values)]:
            if len(values) > 3:
                try:
                    stat, p_value = stats.shapiro(values[:5000])  # Limit sample size for performance
                    tests['normality'][name] = {
                        'statistic': float(stat),
                        'p_value': float(p_value),
                        'is_normal': bool(p_value > 0.05)
                    }
                except:
                    tests['normality'][name] = {'statistic': 0, 'p_value': 1, 'is_normal': False}
            else:
                tests['normality'][name] = {'statistic': 0, 'p_value': 1, 'is_normal': False}
        
        # 2. Correlation tests between centrality measures
        tests['correlations'] = {}
        centrality_pairs = [
            ('degree', 'betweenness', degree_values, betweenness_values),
            ('degree', 'closeness', degree_values, closeness_values),
            ('degree', 'eigenvector', degree_values, eigenvector_values),
            ('betweenness', 'closeness', betweenness_values, closeness_values),
            ('betweenness', 'eigenvector', betweenness_values, eigenvector_values),
            ('closeness', 'eigenvector', closeness_values, eigenvector_values)
        ]
        
        for name1, name2, values1, values2 in centrality_pairs:
            if len(values1) > 3 and len(values2) > 3:
                try:
                    # Pearson correlation
                    pearson_r, pearson_p = stats.pearsonr(values1, values2)
                    # Spearman correlation
                    spearman_r, spearman_p = stats.spearmanr(values1, values2)
                    
                    tests['correlations'][f'{name1}_vs_{name2}'] = {
                        'pearson': {'r': float(pearson_r), 'p_value': float(pearson_p)},
                        'spearman': {'r': float(spearman_r), 'p_value': float(spearman_p)},
                        'significant': bool(pearson_p < 0.05 or spearman_p < 0.05)
                    }
                except:
                    tests['correlations'][f'{name1}_vs_{name2}'] = {
                        'pearson': {'r': 0, 'p_value': 1},
                        'spearman': {'r': 0, 'p_value': 1},
                        'significant': False
                    }
            else:
                tests['correlations'][f'{name1}_vs_{name2}'] = {
                    'pearson': {'r': 0, 'p_value': 1},
                    'spearman': {'r': 0, 'p_value': 1},
                    'significant': False
                }
        
        # 3. Community significance tests
        tests['community_significance'] = {}
        if 'louvain' in self.community_data and 'communities' in self.community_data['louvain']:
            communities = self.community_data['louvain']['communities']
            if communities:
                # Test if community sizes follow power law
                community_sizes = [len(comm) for comm in communities]
                if len(community_sizes) > 3:
                    try:
                        # Kolmogorov-Smirnov test for power law
                        from scipy.stats import kstest
                        # Generate power law distribution for comparison
                        alpha = 2.0  # Typical power law exponent
                        x_min = min(community_sizes)
                        power_law_sample = np.random.power(alpha-1, len(community_sizes)) * (max(community_sizes) - x_min) + x_min
                        
                        ks_stat, ks_p = kstest(community_sizes, lambda x: np.interp(x, sorted(power_law_sample), np.linspace(0, 1, len(power_law_sample))))
                        
                        tests['community_significance']['power_law'] = {
                            'ks_statistic': float(ks_stat),
                            'p_value': float(ks_p),
                            'follows_power_law': bool(ks_p > 0.05)
                        }
                    except:
                        tests['community_significance']['power_law'] = {
                            'ks_statistic': 0,
                            'p_value': 1,
                            'follows_power_law': False
                        }
                else:
                    tests['community_significance']['power_law'] = {
                        'ks_statistic': 0,
                        'p_value': 1,
                        'follows_power_law': False
                    }
        
        return tests
    
    def perform_benchmarking_analysis(self):
        """Compare network against theoretical benchmarks"""
        print("[ADVANCED] Performing benchmarking analysis...")
        
        benchmarks = {}
        
        # Get network metrics
        n = self.G.number_of_nodes()
        m = self.G.number_of_edges()
        density = nx.density(self.G)
        clustering = nx.average_clustering(self.G)
        
        # 1. Random network benchmarks
        benchmarks['random_network'] = {
            'expected_density': 2 * m / (n * (n - 1)) if n > 1 else 0,
            'expected_clustering': density,  # For random networks, clustering ≈ density
            'expected_avg_degree': 2 * m / n if n > 0 else 0
        }
        
        # 2. Scale-free network benchmarks
        degrees = [d for n, d in self.G.degree()]
        if degrees:
            degree_dist = np.bincount(degrees)
            # Calculate degree distribution statistics
            benchmarks['scale_free'] = {
                'degree_variance': float(np.var(degrees)),
                'degree_skewness': float(stats.skew(degrees)),
                'degree_kurtosis': float(stats.kurtosis(degrees)),
                'max_degree_ratio': float(max(degrees) / np.mean(degrees)) if np.mean(degrees) > 0 else 0
            }
        else:
            benchmarks['scale_free'] = {
                'degree_variance': 0,
                'degree_skewness': 0,
                'degree_kurtosis': 0,
                'max_degree_ratio': 0
            }
        
        # 3. Small world benchmarks
        try:
            # Calculate small world coefficient
            if nx.is_connected(self.G):
                L = nx.average_shortest_path_length(self.G)
                C = nx.average_clustering(self.G)
                
                # Random network with same density
                p = density
                L_random = np.log(n) / np.log(p * n) if p > 0 and n > 1 else 0
                C_random = p
                
                small_world_coefficient = (C / C_random) / (L / L_random) if L_random > 0 and C_random > 0 else 0
                
                benchmarks['small_world'] = {
                    'coefficient': float(small_world_coefficient),
                    'is_small_world': bool(small_world_coefficient > 1),
                    'clustering_ratio': float(C / C_random) if C_random > 0 else 0,
                    'path_length_ratio': float(L / L_random) if L_random > 0 else 0
                }
            else:
                benchmarks['small_world'] = {
                    'coefficient': 0,
                    'is_small_world': False,
                    'clustering_ratio': 0,
                    'path_length_ratio': 0
                }
        except:
            benchmarks['small_world'] = {
                'coefficient': 0,
                'is_small_world': False,
                'clustering_ratio': 0,
                'path_length_ratio': 0
            }
        
        # 4. Real-world network comparisons
        benchmarks['real_world_comparison'] = {
            'facebook_typical_density': 0.01,  # Typical Facebook network density
            'facebook_typical_clustering': 0.5,  # Typical clustering coefficient
            'our_density': float(density),
            'our_clustering': float(clustering),
            'density_ratio': float(density / 0.01) if density > 0 else 0,
            'clustering_ratio': float(clustering / 0.5) if clustering > 0 else 0
        }
        
        return benchmarks
    
    def create_advanced_visualizations(self):
        """Create comprehensive advanced visualizations with explanations"""
        print("[ADVANCED] Creating comprehensive advanced visualizations...")
        
        plt.style.use('default')
        sns.set_palette("husl")
        
        visualizations = {}
        
        # 1. Network Efficiency Dashboard
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Degree distribution with power law fit
        degrees = [d for n, d in self.G.degree()]
        ax1.hist(degrees, bins=50, alpha=0.7, color='skyblue', edgecolor='black')
        ax1.set_title('Degree Distribution: Scale-Free Network Analysis', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Degree (Number of Connections)')
        ax1.set_ylabel('Frequency (Number of Users)')
        ax1.grid(True, alpha=0.3)
        
        # Add power law explanation
        ax1.text(0.7, 0.8, f'Mean Degree: {np.mean(degrees):.1f}\nMax Degree: {max(degrees)}\nVariance: {np.var(degrees):.1f}', 
                transform=ax1.transAxes, fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        
        # 2. Centrality Correlation Heatmap
        centrality_data = {
            'Degree': list(self.centrality_data.get('degree_centrality', {}).values()),
            'Betweenness': list(self.centrality_data.get('betweenness_centrality', {}).values()),
            'Closeness': list(self.centrality_data.get('closeness_centrality', {}).values()),
            'Eigenvector': list(self.centrality_data.get('eigenvector_centrality', {}).values())
        }
        
        # Create correlation matrix
        df = pd.DataFrame(centrality_data)
        correlation_matrix = df.corr()
        
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, ax=ax2, 
                   cbar_kws={'label': 'Correlation Coefficient'})
        ax2.set_title('Centrality Measures Correlation Matrix', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Centrality Measures')
        ax2.set_ylabel('Centrality Measures')
        
        # 3. Community Size Distribution
        if 'louvain' in self.community_data and 'communities' in self.community_data['louvain']:
            communities = self.community_data['louvain']['communities']
            community_sizes = [len(comm) for comm in communities]
            ax3.hist(community_sizes, bins=20, alpha=0.7, color='lightgreen', edgecolor='black')
            ax3.set_title('Community Size Distribution: Social Group Analysis', fontsize=14, fontweight='bold')
            ax3.set_xlabel('Community Size (Number of Users)')
            ax3.set_ylabel('Number of Communities')
            ax3.grid(True, alpha=0.3)
            
            # Add community statistics
            ax3.text(0.7, 0.8, f'Total Communities: {len(communities)}\nLargest: {max(community_sizes)}\nSmallest: {min(community_sizes)}\nAvg Size: {np.mean(community_sizes):.1f}', 
                    transform=ax3.transAxes, fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        
        # 4. Network Robustness Analysis
        robustness_random = self._calculate_robustness('random')
        robustness_targeted = self._calculate_robustness('targeted')
        
        categories = ['Random Attack', 'Targeted Attack']
        robustness_values = [robustness_random, robustness_targeted]
        
        bars = ax4.bar(categories, robustness_values, color=['lightcoral', 'lightblue'])
        ax4.set_title('Network Robustness: Attack Resistance Analysis', fontsize=14, fontweight='bold')
        ax4.set_ylabel('Robustness Score (0-1)')
        ax4.set_ylim(0, 1)
        ax4.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, value in zip(bars, robustness_values):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                    f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # Add robustness explanation
        robustness_level = "Excellent" if min(robustness_values) > 0.8 else "Good" if min(robustness_values) > 0.6 else "Average"
        ax4.text(0.5, 0.7, f'Overall Robustness: {robustness_level}\nRandom Attack: {robustness_random:.3f}\nTargeted Attack: {robustness_targeted:.3f}', 
                transform=ax4.transAxes, fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        
        plt.tight_layout()
        plt.savefig(self.results_dir / 'advanced_analytics_dashboard.png', dpi=300, bbox_inches='tight')
        plt.close()
        visualizations['advanced_dashboard'] = 'advanced_analytics_dashboard.png'
        
        # 2. Small World Analysis
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Small World Coefficient Analysis
        small_world_coeff = self.calculate_network_efficiency_metrics().get('small_world_coefficient', 0)
        clustering = self.calculate_network_efficiency_metrics().get('clustering', 0)
        avg_path_length = self.calculate_network_efficiency_metrics().get('avg_path_length', 0)
        
        # Clustering vs Path Length
        ax1.scatter([avg_path_length], [clustering], s=200, c='red', alpha=0.7, label='Our Network')
        ax1.set_xlabel('Average Path Length')
        ax1.set_ylabel('Clustering Coefficient')
        ax1.set_title('Small World Analysis: Clustering vs Path Length', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Add small world explanation
        small_world_status = "Yes" if small_world_coeff > 1 else "No"
        ax1.text(0.05, 0.95, f'Small World Coefficient: {small_world_coeff:.3f}\nStatus: {small_world_status}\nClustering: {clustering:.3f}\nPath Length: {avg_path_length:.3f}', 
                transform=ax1.transAxes, fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        
        # Degree Distribution Log-Log Plot
        degrees = [d for n, d in self.G.degree()]
        degree_counts = np.bincount(degrees)
        x_data = np.arange(1, len(degree_counts))
        y_data = degree_counts[1:]
        y_data = y_data[y_data > 0]
        x_data = x_data[:len(y_data)]
        
        ax2.loglog(x_data, y_data, 'bo', alpha=0.6, markersize=4)
        ax2.set_xlabel('Degree (log scale)')
        ax2.set_ylabel('Frequency (log scale)')
        ax2.set_title('Power Law Distribution: Scale-Free Network', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        # Add power law explanation
        power_law_r2 = self.calculate_network_efficiency_metrics().get('power_law_r2', 0)
        ax2.text(0.05, 0.95, f'Power Law R²: {power_law_r2:.3f}\nScale-Free: {"Yes" if power_law_r2 > 0.8 else "No"}\nExponent: {self.calculate_network_efficiency_metrics().get("power_law_exponent", 0):.3f}', 
                transform=ax2.transAxes, fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        
        # Network Efficiency Metrics
        efficiency_metrics = self.calculate_network_efficiency_metrics()
        metrics_names = ['Global Efficiency', 'Clustering', 'Transitivity', 'Density']
        metrics_values = [
            efficiency_metrics.get('global_efficiency', 0),
            efficiency_metrics.get('clustering', 0),
            efficiency_metrics.get('transitivity', 0),
            efficiency_metrics.get('density', 0)
        ]
        
        bars = ax3.bar(metrics_names, metrics_values, color=['skyblue', 'lightgreen', 'lightcoral', 'lightyellow'])
        ax3.set_title('Network Efficiency Metrics', fontsize=14, fontweight='bold')
        ax3.set_ylabel('Value')
        ax3.tick_params(axis='x', rotation=45)
        ax3.grid(True, alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars, metrics_values):
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                    f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # Statistical Significance Summary
        statistical_tests = self.perform_statistical_tests()
        normality_results = []
        test_names = []
        for test_name, result in statistical_tests.get('normality', {}).items():
            normality_results.append(result['p_value'])
            test_names.append(test_name.capitalize())
        
        bars = ax4.bar(test_names, normality_results, color=['lightcoral' if p < 0.05 else 'lightgreen' for p in normality_results])
        ax4.axhline(y=0.05, color='red', linestyle='--', alpha=0.7, label='Significance Level (0.05)')
        ax4.set_title('Statistical Significance Tests', fontsize=14, fontweight='bold')
        ax4.set_ylabel('p-value')
        ax4.set_ylim(0, 1)
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars, normality_results):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                    f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.results_dir / 'small_world_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        visualizations['small_world_analysis'] = 'small_world_analysis.png'
        
        # 3. Benchmarking Analysis
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Random Network Comparison
        benchmarks = self.perform_benchmarking_analysis()
        metrics = ['Density', 'Clustering', 'Path Length']
        our_values = [
            benchmarks['real_world_comparison']['our_density'],
            benchmarks['real_world_comparison']['our_clustering'],
            efficiency_metrics.get('avg_path_length', 0)
        ]
        random_values = [
            benchmarks['random_network']['expected_density'],
            benchmarks['random_network']['expected_clustering'],
            benchmarks['random_network'].get('expected_path_length', 0)
        ]
        
        x = np.arange(len(metrics))
        width = 0.35
        
        bars1 = ax1.bar(x - width/2, our_values, width, label='Our Network', color='lightblue')
        bars2 = ax1.bar(x + width/2, random_values, width, label='Random Network', color='lightcoral')
        
        ax1.set_title('Network vs Random Network Comparison', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Value')
        ax1.set_xticks(x)
        ax1.set_xticklabels(metrics)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Scale-Free Properties
        scale_free_metrics = benchmarks.get('scale_free', {})
        properties = ['Degree Variance', 'Max Degree Ratio', 'Skewness', 'Kurtosis']
        values = [
            scale_free_metrics.get('degree_variance', 0),
            scale_free_metrics.get('max_degree_ratio', 0),
            scale_free_metrics.get('degree_skewness', 0),
            scale_free_metrics.get('degree_kurtosis', 0)
        ]
        
        bars = ax2.bar(properties, values, color=['skyblue', 'lightgreen', 'lightcoral', 'lightyellow'])
        ax2.set_title('Scale-Free Network Properties', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Value')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3)
        
        # Real-World Comparison
        real_world = benchmarks.get('real_world_comparison', {})
        comparison_metrics = ['Density Ratio', 'Clustering Ratio']
        comparison_values = [
            real_world.get('density_ratio', 0),
            real_world.get('clustering_ratio', 0)
        ]
        
        bars = ax3.bar(comparison_metrics, comparison_values, color=['lightblue', 'lightgreen'])
        ax3.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='Facebook Typical')
        ax3.set_title('Real-World Network Comparison', fontsize=14, fontweight='bold')
        ax3.set_ylabel('Ratio (Our Network / Facebook Typical)')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars, comparison_values):
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                    f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # Correlation Analysis
        correlations = statistical_tests.get('correlations', {})
        correlation_names = []
        correlation_values = []
        for name, result in correlations.items():
            correlation_names.append(name.replace('_vs_', ' vs '))
            correlation_values.append(result.get('pearson', {}).get('r', 0))
        
        bars = ax4.bar(range(len(correlation_names)), correlation_values, 
                     color=['lightgreen' if abs(v) > 0.5 else 'lightcoral' for v in correlation_values])
        ax4.set_title('Centrality Correlations', fontsize=14, fontweight='bold')
        ax4.set_ylabel('Correlation Coefficient')
        ax4.set_xticks(range(len(correlation_names)))
        ax4.set_xticklabels(correlation_names, rotation=45, ha='right')
        ax4.grid(True, alpha=0.3)
        
        # Add value labels
        for i, (bar, value) in enumerate(zip(bars, correlation_values)):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                    f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.results_dir / 'benchmarking_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        visualizations['benchmarking_analysis'] = 'benchmarking_analysis.png'
        
        # 4. Statistical Analysis Summary
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Normality test results
        normality_results = []
        test_names = []
        for test_name, result in statistical_tests.get('normality', {}).items():
            normality_results.append(result['p_value'])
            test_names.append(test_name.capitalize())
        
        bars = ax1.bar(test_names, normality_results, color=['lightcoral' if p < 0.05 else 'lightgreen' for p in normality_results])
        ax1.axhline(y=0.05, color='red', linestyle='--', alpha=0.7, label='Significance Level (0.05)')
        ax1.set_title('Normality Tests (Shapiro-Wilk)', fontsize=14, fontweight='bold')
        ax1.set_ylabel('p-value')
        ax1.set_ylim(0, 1)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars, normality_results):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                    f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # P-value distribution
        p_values = []
        for result in statistical_tests.get('correlations', {}).values():
            p_values.append(result.get('pearson', {}).get('p_value', 1))
        
        ax2.hist(p_values, bins=10, alpha=0.7, color='skyblue', edgecolor='black')
        ax2.axvline(x=0.05, color='red', linestyle='--', alpha=0.7, label='Significance Level (0.05)')
        ax2.set_title('P-value Distribution in Correlation Tests', fontsize=14, fontweight='bold')
        ax2.set_xlabel('p-value')
        ax2.set_ylabel('Frequency')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Network metrics comparison
        network_metrics = ['Nodes', 'Edges', 'Density', 'Clustering']
        network_values = [
            self.G.number_of_nodes(),
            self.G.number_of_edges(),
            efficiency_metrics.get('density', 0),
            efficiency_metrics.get('clustering', 0)
        ]
        
        bars = ax3.bar(network_metrics, network_values, color=['skyblue', 'lightgreen', 'lightcoral', 'lightyellow'])
        ax3.set_title('Network Structure Metrics', fontsize=14, fontweight='bold')
        ax3.set_ylabel('Value')
        ax3.tick_params(axis='x', rotation=45)
        ax3.grid(True, alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars, network_values):
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                    f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
        
        # Community analysis
        if 'louvain' in self.community_data and 'communities' in self.community_data['louvain']:
            communities = self.community_data['louvain']['communities']
            community_sizes = [len(comm) for comm in communities]
            
            ax4.hist(community_sizes, bins=15, alpha=0.7, color='lightgreen', edgecolor='black')
            ax4.set_title('Community Size Distribution', fontsize=14, fontweight='bold')
            ax4.set_xlabel('Community Size')
            ax4.set_ylabel('Number of Communities')
            ax4.grid(True, alpha=0.3)
            
            # Add community statistics
            ax4.text(0.7, 0.8, f'Total: {len(communities)}\nLargest: {max(community_sizes)}\nSmallest: {min(community_sizes)}', 
                    transform=ax4.transAxes, fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        
        plt.tight_layout()
        plt.savefig(self.results_dir / 'statistical_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        visualizations['statistical_analysis'] = 'statistical_analysis.png'
        
        # 3. Benchmarking Analysis
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Random Network Comparison
        benchmarks = self.perform_benchmarking_analysis()
        metrics = ['Density', 'Clustering', 'Path Length']
        our_values = [
            benchmarks['real_world_comparison']['our_density'],
            benchmarks['real_world_comparison']['our_clustering'],
            self.calculate_network_efficiency_metrics().get('avg_path_length', 0)
        ]
        random_values = [
            benchmarks['random_network']['expected_density'],
            benchmarks['random_network']['expected_clustering'],
            benchmarks['random_network'].get('expected_path_length', 0)
        ]
        
        x = np.arange(len(metrics))
        width = 0.35
        
        bars1 = ax1.bar(x - width/2, our_values, width, label='Our Network', color='lightblue')
        bars2 = ax1.bar(x + width/2, random_values, width, label='Random Network', color='lightcoral')
        
        ax1.set_title('Network vs Random Network Comparison', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Value')
        ax1.set_xticks(x)
        ax1.set_xticklabels(metrics)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Scale-Free Properties
        scale_free_metrics = benchmarks.get('scale_free', {})
        properties = ['Degree Variance', 'Max Degree Ratio', 'Skewness', 'Kurtosis']
        values = [
            scale_free_metrics.get('degree_variance', 0),
            scale_free_metrics.get('max_degree_ratio', 0),
            scale_free_metrics.get('degree_skewness', 0),
            scale_free_metrics.get('degree_kurtosis', 0)
        ]
        
        bars = ax2.bar(properties, values, color=['skyblue', 'lightgreen', 'lightcoral', 'lightyellow'])
        ax2.set_title('Scale-Free Network Properties', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Value')
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3)
        
        # Real-World Comparison
        real_world = benchmarks.get('real_world_comparison', {})
        comparison_metrics = ['Density Ratio', 'Clustering Ratio']
        comparison_values = [
            real_world.get('density_ratio', 0),
            real_world.get('clustering_ratio', 0)
        ]
        
        bars = ax3.bar(comparison_metrics, comparison_values, color=['lightblue', 'lightgreen'])
        ax3.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='Facebook Typical')
        ax3.set_title('Real-World Network Comparison', fontsize=14, fontweight='bold')
        ax3.set_ylabel('Ratio (Our Network / Facebook Typical)')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars, comparison_values):
            ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                    f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # Correlation Analysis
        correlations = self.perform_statistical_tests().get('correlations', {})
        correlation_names = []
        correlation_values = []
        for name, result in correlations.items():
            correlation_names.append(name.replace('_vs_', ' vs '))
            correlation_values.append(result.get('pearson', {}).get('r', 0))
        
        bars = ax4.bar(range(len(correlation_names)), correlation_values, 
                     color=['lightgreen' if abs(v) > 0.5 else 'lightcoral' for v in correlation_values])
        ax4.set_title('Centrality Correlations', fontsize=14, fontweight='bold')
        ax4.set_ylabel('Correlation Coefficient')
        ax4.set_xticks(range(len(correlation_names)))
        ax4.set_xticklabels(correlation_names, rotation=45, ha='right')
        ax4.grid(True, alpha=0.3)
        
        # Add value labels
        for i, (bar, value) in enumerate(zip(bars, correlation_values)):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                    f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.results_dir / 'benchmarking_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        visualizations['benchmarking_analysis'] = 'benchmarking_analysis.png'
        
        return visualizations
    
    def generate_comprehensive_report(self):
        """Generate comprehensive analytics report with optimizations"""
        print("[ADVANCED] Generating comprehensive analytics report...")
        start_time = time.time()
        
        # Calculate all metrics in parallel where possible
        print("[ADVANCED] Calculating network efficiency metrics...")
        efficiency_metrics = self.calculate_network_efficiency_metrics()
        
        print("[ADVANCED] Performing statistical significance tests...")
        statistical_tests = self.perform_statistical_tests()
        
        print("[ADVANCED] Performing benchmarking analysis...")
        benchmarks = self.perform_benchmarking_analysis()
        
        print("[ADVANCED] Creating advanced visualizations...")
        visualizations = self.create_advanced_visualizations()
        
        # Generate report
        report = {
            'timestamp': time.time(),
            'network_efficiency': efficiency_metrics,
            'statistical_tests': statistical_tests,
            'benchmarking': benchmarks,
            'visualizations': visualizations,
            'summary': {
                'total_analyses': 3,
                'statistical_tests_performed': len(statistical_tests.get('normality', {})) + len(statistical_tests.get('correlations', {})),
                'benchmarks_comparison': len(benchmarks),
                'visualizations_created': len(visualizations)
            }
        }
        
        # Convert numpy types to Python types for JSON serialization
        report = self._convert_numpy_types(report)
        
        # Save report
        with open(self.results_dir / 'advanced_analytics_report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        elapsed_time = time.time() - start_time
        print(f"[ADVANCED] Report generated in {elapsed_time:.2f} seconds and saved to {self.results_dir / 'advanced_analytics_report.json'}")
        return report
    
    def _convert_numpy_types(self, obj):
        """Convert numpy types to Python types for JSON serialization"""
        if isinstance(obj, dict):
            return {key: self._convert_numpy_types(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_numpy_types(item) for item in obj]
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj
