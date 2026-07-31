// Facebook Social Network Analysis Dashboard
class DashboardApp {
    constructor() {
        this.pollInterval = null;
        this.charts = {};
        this.init();
    }

    init() {
        console.log('Dashboard initialized');
        this.startStatusPolling();
    }

    startStatusPolling() {
        // Poll status every 1 second
        this.pollInterval = setInterval(() => {
            this.checkStatus();
        }, 1000);
        
        // Initial check
        this.checkStatus();
    }

    async checkStatus() {
        try {
            const response = await fetch('/api/status');
            const status = await response.json();
            
            this.updateLoadingScreen(status);
            
            if (status.complete) {
                // Stop polling
                clearInterval(this.pollInterval);
                
                // Load results
                await this.loadResults();
                
                // Hide loading, show dashboard
                setTimeout(() => {
                    document.getElementById('loading-screen').classList.add('hidden');
                    document.getElementById('dashboard').classList.remove('hidden');
                }, 1000);
            }
        } catch (error) {
            console.error('Error checking status:', error);
        }
    }

    updateLoadingScreen(status) {
        // Update progress bar
        const progressFill = document.getElementById('progress-fill');
        const progressText = document.getElementById('progress-text');
        progressFill.style.width = status.progress + '%';
        progressText.textContent = status.progress + '%';
        
        // Update current step
        const stepText = document.getElementById('step-text');
        stepText.textContent = status.current_step;
        
        // Update step indicators
        if (status.progress >= 10) this.updateStep('step-1', status.progress >= 25 ? 'complete' : 'active');
        if (status.progress >= 30) this.updateStep('step-2', status.progress >= 50 ? 'complete' : 'active');
        if (status.progress >= 55) this.updateStep('step-3', status.progress >= 75 ? 'complete' : 'active');
        if (status.progress >= 80) this.updateStep('step-4', status.progress >= 90 ? 'complete' : 'active');
        if (status.progress >= 95) this.updateStep('step-5', status.progress >= 100 ? 'complete' : 'active');
    }

    updateStep(stepId, state) {
        const step = document.getElementById(stepId);
        step.classList.remove('active', 'complete');
        if (state) {
            step.classList.add(state);
        }
    }

    async loadResults() {
        try {
            const response = await fetch('/api/results');
            const data = await response.json();
            
            console.log('Results loaded:', data);
            
            // Update network stats
            this.updateNetworkStats(data.network);
            
            // Update top users
            this.updateTopUsers(data.centrality.top_users);
            
            // Update communities
            this.updateCommunities(data.communities);
            
            // Create charts
            this.createCharts(data);
            
            // Update insights
            this.updateInsights(data);
            
        } catch (error) {
            console.error('Error loading results:', error);
        }
    }

    updateNetworkStats(network) {
        document.getElementById('total-nodes').textContent = network.nodes.toLocaleString();
        document.getElementById('total-edges').textContent = network.edges.toLocaleString();
        document.getElementById('density').textContent = network.density.toFixed(4);
        document.getElementById('avg-degree').textContent = network.avg_degree.toFixed(1);
    }

    updateTopUsers(users) {
        const container = document.getElementById('top-users');
        container.innerHTML = '';
        
        const gradients = [
            'linear-gradient(135deg, #f59e0b, #d97706)', // Gold
            'linear-gradient(135deg, #3b82f6, #2563eb)', // Blue
            'linear-gradient(135deg, #8b5cf6, #7c3aed)'  // Purple
        ];
        
        const icons = ['fa-crown', 'fa-medal', 'fa-award'];
        const roles = ['Most Influential', 'Highly Connected', 'Key Connector'];
        
        users.slice(0, 3).forEach((user, index) => {
            const card = document.createElement('div');
            card.className = 'user-card floating';
            card.style.background = gradients[index];
            card.style.animationDelay = `${index * 0.1}s`;
            
            card.innerHTML = `
                <div class="user-header">
                    <div class="user-rank">#${index + 1}</div>
                    <div class="user-badge">
                        <i class="fas ${icons[index]}"></i>
                    </div>
                </div>
                <div class="user-name">User ${user.user_id}</div>
                <div class="user-role">${roles[index]}</div>
                <div class="user-metrics">
                    <div class="metric">
                        <span>Degree:</span>
                        <span><strong>${user.degree.toFixed(4)}</strong></span>
                    </div>
                    <div class="metric">
                        <span>Betweenness:</span>
                        <span><strong>${user.betweenness.toFixed(4)}</strong></span>
                    </div>
                    <div class="metric">
                        <span>Closeness:</span>
                        <span><strong>${user.closeness.toFixed(4)}</strong></span>
                    </div>
                </div>
            `;
            
            container.appendChild(card);
        });
    }

    updateCommunities(communities) {
        const container = document.getElementById('communities');
        container.innerHTML = '';
        
        const methods = [
            { key: 'louvain', name: 'Louvain', gradient: 'linear-gradient(135deg, #3b82f6, #2563eb)', quality: 'Excellent' },
            { key: 'label_propagation', name: 'Label Propagation', gradient: 'linear-gradient(135deg, #10b981, #059669)', quality: 'Good' },
            { key: 'greedy_modularity', name: 'Greedy Modularity', gradient: 'linear-gradient(135deg, #8b5cf6, #7c3aed)', quality: 'Very Good' }
        ];
        
        methods.forEach((method, index) => {
            const data = communities[method.key];
            const card = document.createElement('div');
            card.className = 'community-card floating';
            card.style.background = method.gradient;
            card.style.animationDelay = `${index * 0.1}s`;
            
            card.innerHTML = `
                <div class="community-header">
                    <div class="community-name">${method.name}</div>
                    <div class="user-badge">
                        <i class="fas fa-layer-group"></i>
                    </div>
                </div>
                <div class="community-count">${data.count}</div>
                <div class="community-label">Communities Found</div>
                <div class="user-metrics">
                    <div class="metric">
                        <span>Modularity:</span>
                        <span><strong>${data.modularity.toFixed(4)}</strong></span>
                    </div>
                    <div class="metric">
                        <span>Quality:</span>
                        <span><strong>${method.quality}</strong></span>
                    </div>
                </div>
            `;
            
            container.appendChild(card);
        });
    }

    createCharts(data) {
        // Centrality Chart
        const centralityCtx = document.getElementById('centralityChart').getContext('2d');
        const topUser = data.centrality.top_users[0];
        
        this.charts.centrality = new Chart(centralityCtx, {
            type: 'bar',
            data: {
                labels: ['Degree', 'Betweenness', 'Closeness', 'Eigenvector'],
                datasets: [{
                    label: 'Top User Centrality Values',
                    data: [
                        topUser.degree,
                        topUser.betweenness,
                        topUser.closeness,
                        topUser.eigenvector
                    ],
                    backgroundColor: [
                        'rgba(59, 130, 246, 0.8)',
                        'rgba(16, 185, 129, 0.8)',
                        'rgba(245, 158, 11, 0.8)',
                        'rgba(139, 92, 246, 0.8)'
                    ],
                    borderColor: [
                        'rgba(59, 130, 246, 1)',
                        'rgba(16, 185, 129, 1)',
                        'rgba(245, 158, 11, 1)',
                        'rgba(139, 92, 246, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: 'white' }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { color: 'white' },
                        grid: { color: 'rgba(255, 255, 255, 0.1)' }
                    },
                    x: {
                        ticks: { color: 'white' },
                        grid: { color: 'rgba(255, 255, 255, 0.1)' }
                    }
                }
            }
        });
        
        // Community Chart
        const communityCtx = document.getElementById('communityChart').getContext('2d');
        
        this.charts.community = new Chart(communityCtx, {
            type: 'doughnut',
            data: {
                labels: ['Louvain', 'Label Propagation', 'Greedy Modularity'],
                datasets: [{
                    data: [
                        data.communities.louvain.count,
                        data.communities.label_propagation.count,
                        data.communities.greedy_modularity.count
                    ],
                    backgroundColor: [
                        'rgba(59, 130, 246, 0.8)',
                        'rgba(16, 185, 129, 0.8)',
                        'rgba(139, 92, 246, 0.8)'
                    ],
                    borderColor: [
                        'rgba(59, 130, 246, 1)',
                        'rgba(16, 185, 129, 1)',
                        'rgba(139, 92, 246, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: 'white',
                            padding: 20
                        }
                    }
                }
            }
        });
    }

    updateInsights(data) {
        const container = document.getElementById('insights');
        container.innerHTML = '';
        
        const insights = [
            {
                title: 'Network Structure',
                items: [
                    `<strong>Connected Network:</strong> All ${data.network.nodes.toLocaleString()} users are connected`,
                    `<strong>Density:</strong> ${data.network.density.toFixed(4)} (sparse but well-connected)`,
                    `<strong>Average Degree:</strong> ${data.network.avg_degree.toFixed(1)} connections per user`,
                    `<strong>Total Connections:</strong> ${data.network.edges.toLocaleString()} edges in the network`
                ],
                gradient: 'linear-gradient(135deg, #3b82f6, #2563eb)'
            },
            {
                title: 'Influence Analysis',
                items: [
                    `<strong>Top Influencer:</strong> User ${data.centrality.top_users[0].user_id} (${(data.centrality.top_users[0].degree * 100).toFixed(1)}% degree centrality)`,
                    `<strong>Key Connectors:</strong> Users ${data.centrality.top_users.slice(1, 4).map(u => u.user_id).join(', ')}`,
                    `<strong>Network Hubs:</strong> ${data.communities.louvain.count} major community centers (Louvain)`,
                    `<strong>Information Flow:</strong> Fast through high betweenness centrality nodes`
                ],
                gradient: 'linear-gradient(135deg, #ec4899, #be185d)'
            }
        ];
        
        insights.forEach((insight, index) => {
            const card = document.createElement('div');
            card.className = 'insight-card floating';
            card.style.background = insight.gradient;
            card.style.animationDelay = `${index * 0.1}s`;
            
            card.innerHTML = `
                <div class="insight-title">${insight.title}</div>
                <ul class="insight-list">
                    ${insight.items.map(item => `<li>• ${item}</li>`).join('')}
                </ul>
            `;
            
            container.appendChild(card);
        });
    }
}

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', () => {
    new DashboardApp();
});

