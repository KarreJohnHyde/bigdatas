/**
 * Advanced Analytics Dashboard JavaScript
 * Handles statistical analysis, benchmarking, and network efficiency metrics
 */

class AdvancedAnalytics {
    constructor() {
        this.socket = null;
        this.analysisData = null;
        this.charts = {};
        this.init();
    }

    init() {
        console.log('[ADVANCED] Initializing Advanced Analytics Dashboard...');
        this.setupSocketConnection();
        this.loadAdvancedAnalytics();
        this.setupEventListeners();
    }

    setupSocketConnection() {
        this.socket = io();
        
        this.socket.on('connect', () => {
            console.log('[ADVANCED] Connected to server');
        });

        this.socket.on('disconnect', () => {
            console.log('[ADVANCED] Disconnected from server');
        });

        this.socket.on('analysis_progress', (data) => {
            this.updateProgress(data);
        });

        this.socket.on('analysis_complete', (data) => {
            console.log('[ADVANCED] Analysis complete, loading advanced analytics...');
            this.loadAdvancedAnalytics();
        });
    }

    async loadAdvancedAnalytics() {
        try {
            console.log('[ADVANCED] Loading advanced analytics data...');
            this.updateLoadingText('Loading advanced analytics data...');
            this.updateProgress(10);

            // Check if main analysis is complete
            const analysisStatus = await fetch('/api/analysis-status');
            const statusData = await analysisStatus.json();
            
            if (statusData.status !== 'complete') {
                console.log('[ADVANCED] Main analysis not complete, waiting...');
                this.updateLoadingText('Waiting for main analysis to complete...');
                setTimeout(() => this.loadAdvancedAnalytics(), 2000);
                return;
            }

            this.updateProgress(30);
            this.updateLoadingText('Checking for cached data...');

            // Load advanced analytics with progress indication
            const startTime = Date.now();
            const response = await fetch('/api/advanced-analytics');
            const loadTime = Date.now() - startTime;
            
            this.updateProgress(70);
            
            if (loadTime < 2000) {
                this.updateLoadingText('Loading cached data (fast)...');
            } else {
                this.updateLoadingText('Generating fresh analysis (this may take a moment)...');
            }
            
            const data = await response.json();

            if (data.error) {
                throw new Error(data.error);
            }

            this.updateProgress(90);
            this.updateLoadingText('Rendering visualizations...');

            this.analysisData = data;
            this.displayAdvancedAnalytics();
            
            this.updateProgress(100);
            this.hideLoadingScreen();

        } catch (error) {
            console.error('[ADVANCED] Error loading advanced analytics:', error);
            this.showError('Failed to load advanced analytics: ' + error.message);
        }
    }

    displayAdvancedAnalytics() {
        console.log('[ADVANCED] Displaying advanced analytics data...');
        
        this.displayNetworkEfficiencyMetrics();
        this.displayStatisticalTests();
        this.displayBenchmarkingAnalysis();
        this.displayAdvancedVisualizations();
        this.displayAnalysisSummary();
    }

    displayNetworkEfficiencyMetrics() {
        const metrics = this.analysisData.network_efficiency;
        
        // Update metric cards
        this.updateMetricCard('global-efficiency', metrics.global_efficiency, 3);
        this.updateMetricCard('small-world-coeff', metrics.small_world_coefficient || 0, 3);
        this.updateMetricCard('robustness-random', metrics.robustness_random, 3);
        this.updateMetricCard('power-law-r2', metrics.power_law_r2, 3);
    }

    displayStatisticalTests() {
        const tests = this.analysisData.statistical_tests;
        
        // Display normality tests
        const normalityContainer = document.getElementById('normality-tests');
        normalityContainer.innerHTML = '';
        
        Object.entries(tests.normality || {}).forEach(([testName, result]) => {
            const testElement = this.createTestResultElement(
                testName,
                result.p_value,
                result.is_normal ? 'Normal' : 'Not Normal',
                result.is_normal
            );
            normalityContainer.appendChild(testElement);
        });

        // Display correlation tests
        const correlationContainer = document.getElementById('correlation-tests');
        correlationContainer.innerHTML = '';
        
        Object.entries(tests.correlations || {}).forEach(([testName, result]) => {
            const isSignificant = result.significant;
            const pearson = result.pearson || {};
            const correlationElement = this.createCorrelationElement(
                testName,
                pearson.r || 0,
                pearson.p_value || 0,
                isSignificant
            );
            correlationContainer.appendChild(correlationElement);
        });
    }

    displayBenchmarkingAnalysis() {
        const benchmarks = this.analysisData.benchmarking;
        
        // Random network comparison
        this.displayBenchmarkComparison('random-network-comparison', {
            'Density': {
                our: benchmarks.vs_random_network?.density_ratio || 0,
                benchmark: 1.0
            },
            'Clustering': {
                our: benchmarks.vs_random_network?.clustering_ratio || 0,
                benchmark: 1.0
            }
        });

        // Scale-free analysis
        this.displayBenchmarkComparison('scale-free-analysis', {
            'Degree Variance': {
                our: benchmarks.scale_free_properties?.degree_variance || 0,
                benchmark: 'High variance indicates scale-free'
            },
            'Max Degree Ratio': {
                our: benchmarks.scale_free_properties?.max_degree_ratio || 0,
                benchmark: '>10 indicates scale-free'
            }
        });

        // Real-world comparison
        this.displayBenchmarkComparison('real-world-comparison', {
            'Density Ratio': {
                our: benchmarks.vs_random_network?.density_ratio || 0,
                benchmark: 1.0
            },
            'Clustering Ratio': {
                our: benchmarks.vs_random_network?.clustering_ratio || 0,
                benchmark: 1.0
            }
        });
    }

    displayAdvancedVisualizations() {
        const visualizations = this.analysisData.visualizations;
        
        // Advanced Analytics Dashboard
        if (visualizations.advanced_dashboard) {
            const img = document.getElementById('advanced-dashboard-img');
            const btn = document.getElementById('view-advanced-dashboard');
            img.src = `/data/results/advanced/${visualizations.advanced_dashboard}`;
            img.alt = 'Advanced Analytics Dashboard';
            img.style.display = 'block';
            if (btn) btn.style.display = 'flex';
        }

        // Small World Analysis
        if (visualizations.small_world) {
            const img = document.getElementById('small-world-analysis-img');
            const btn = document.getElementById('view-small-world');
            img.src = `/data/results/advanced/${visualizations.small_world}`;
            img.alt = 'Small World Analysis';
            img.style.display = 'block';
            if (btn) btn.style.display = 'flex';
        }

        // Benchmarking Analysis
        if (visualizations.benchmarking) {
            const img = document.getElementById('benchmarking-analysis-img');
            const btn = document.getElementById('view-benchmarking');
            img.src = `/data/results/advanced/${visualizations.benchmarking}`;
            img.alt = 'Benchmarking Analysis';
            img.style.display = 'block';
            if (btn) btn.style.display = 'flex';
        }

        // Statistical Analysis
        if (visualizations.statistical) {
            const img = document.getElementById('statistical-analysis-img');
            const btn = document.getElementById('view-statistical');
            img.src = `/data/results/advanced/${visualizations.statistical}`;
            img.alt = 'Statistical Analysis';
            img.style.display = 'block';
            if (btn) btn.style.display = 'flex';
        }
    }

    displayAnalysisSummary() {
        const summary = this.analysisData.summary;
        const container = document.getElementById('analysis-summary');
        
        container.innerHTML = `
            <div class="bg-slate-700 rounded-lg p-4">
                <h3 class="text-lg font-semibold text-white mb-3">Analysis Overview</h3>
                <div class="space-y-2">
                    <div class="flex justify-between">
                        <span class="text-gray-400">Total Analyses:</span>
                        <span class="text-white font-bold">${summary.total_analyses}</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-400">Statistical Tests:</span>
                        <span class="text-white font-bold">${summary.statistical_tests_performed}</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-400">Benchmarks:</span>
                        <span class="text-white font-bold">${summary.benchmarks_comparison}</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-400">Visualizations:</span>
                        <span class="text-white font-bold">${summary.visualizations_created}</span>
                    </div>
                </div>
            </div>
            
            <div class="bg-slate-700 rounded-lg p-4">
                <h3 class="text-lg font-semibold text-white mb-3">Network Characteristics</h3>
                <div class="space-y-2">
                    <div class="flex justify-between">
                        <span class="text-gray-400">Small World:</span>
                        <span class="text-white font-bold">${this.analysisData.benchmarking?.small_world?.is_small_world ? 'Yes' : 'No'}</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-400">Scale-Free:</span>
                        <span class="text-white font-bold">${this.analysisData.network_efficiency?.power_law_r2 > 0.8 ? 'Yes' : 'No'}</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-400">Robustness:</span>
                        <span class="text-white font-bold">${this.getRobustnessLevel(this.analysisData.network_efficiency?.robustness_random)}</span>
                    </div>
                </div>
            </div>
            
            <div class="bg-slate-700 rounded-lg p-4">
                <h3 class="text-lg font-semibold text-white mb-3">Statistical Significance</h3>
                <div class="space-y-2">
                    <div class="flex justify-between">
                        <span class="text-gray-400">Normal Distributions:</span>
                        <span class="text-white font-bold">${this.countNormalDistributions()}</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-400">Significant Correlations:</span>
                        <span class="text-white font-bold">${this.countSignificantCorrelations()}</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-gray-400">Power Law Fit:</span>
                        <span class="text-white font-bold">${this.analysisData.network_efficiency?.power_law_r2 > 0.8 ? 'Good' : 'Poor'}</span>
                    </div>
                </div>
            </div>
        `;
    }

    // Helper methods
    updateMetricCard(elementId, value, decimals = 2) {
        const element = document.getElementById(elementId);
        if (element) {
            // Fix toFixed error by checking for null/undefined values
            if (value === null || value === undefined || isNaN(value)) {
                element.textContent = 'N/A';
            } else {
                element.textContent = value.toFixed(decimals);
            }
        }
    }

    createTestResultElement(testName, pValue, result, isSignificant) {
        const div = document.createElement('div');
        div.className = `test-result ${isSignificant ? 'significant' : 'not-significant'}`;
        
        const significanceClass = this.getSignificanceClass(pValue);
        
        div.innerHTML = `
            <div class="flex justify-between items-center">
                <span class="text-white font-medium">${testName.charAt(0).toUpperCase() + testName.slice(1)}</span>
                <div class="flex items-center space-x-2">
                    <span class="text-sm ${significanceClass}">${result}</span>
                    <span class="text-xs text-gray-400">(p=${pValue ? pValue.toFixed(3) : 'N/A'})</span>
                </div>
            </div>
        `;
        
        return div;
    }

    createCorrelationElement(testName, correlation, pValue, isSignificant) {
        const div = document.createElement('div');
        div.className = `test-result ${isSignificant ? 'significant' : 'not-significant'}`;
        
        const significanceClass = this.getSignificanceClass(pValue);
        
        div.innerHTML = `
            <div class="flex justify-between items-center">
                <span class="text-white font-medium">${testName.replace('_', ' vs ')}</span>
                <div class="flex items-center space-x-2">
                    <span class="text-sm ${significanceClass}">r=${correlation ? correlation.toFixed(3) : 'N/A'}</span>
                    <span class="text-xs text-gray-400">(p=${pValue ? pValue.toFixed(3) : 'N/A'})</span>
                </div>
            </div>
        `;
        
        return div;
    }

    displayBenchmarkComparison(containerId, comparisons) {
        const container = document.getElementById(containerId);
        container.innerHTML = '';
        
        Object.entries(comparisons).forEach(([metric, data]) => {
            const div = document.createElement('div');
            div.className = 'benchmark-comparison';
            
            const ourValue = typeof data.our === 'number' ? data.our.toFixed(3) : data.our;
            const benchmarkValue = typeof data.benchmark === 'number' ? data.benchmark.toFixed(3) : data.benchmark;
            
            div.innerHTML = `
                <div class="benchmark-label">${metric}</div>
                <div class="benchmark-value">${ourValue}</div>
                <div class="benchmark-ratio">vs ${benchmarkValue}</div>
            `;
            
            container.appendChild(div);
        });
    }

    getSignificanceClass(pValue) {
        if (pValue < 0.001) return 'p-value-excellent';
        if (pValue < 0.01) return 'p-value-good';
        if (pValue < 0.05) return 'p-value-moderate';
        return 'p-value-poor';
    }

    getRobustnessLevel(robustness) {
        if (robustness > 0.8) return 'Excellent';
        if (robustness > 0.6) return 'Good';
        if (robustness > 0.4) return 'Average';
        return 'Poor';
    }

    countNormalDistributions() {
        const normality = this.analysisData.statistical_tests?.normality || {};
        return Object.values(normality).filter(result => result.is_normal).length;
    }

    countSignificantCorrelations() {
        const correlations = this.analysisData.statistical_tests?.correlations || {};
        return Object.values(correlations).filter(result => result.significant).length;
    }

    // Loading and progress methods
    updateLoadingText(text) {
        const loadingText = document.getElementById('loading-text');
        if (loadingText) {
            loadingText.textContent = text;
        }
    }

    updateProgress(progress) {
        const progressBar = document.getElementById('progress-bar');
        const progressText = document.getElementById('progress-text');
        
        if (progressBar) {
            progressBar.style.width = progress + '%';
        }
        
        if (progressText) {
            progressText.textContent = Math.round(progress) + '%';
        }
    }

    hideLoadingScreen() {
        const loadingScreen = document.getElementById('loading-screen');
        const mainContent = document.getElementById('main-content');
        
        if (loadingScreen) {
            loadingScreen.style.display = 'none';
        }
        
        if (mainContent) {
            mainContent.style.display = 'block';
        }
    }

    showError(message) {
        const loadingText = document.getElementById('loading-text');
        if (loadingText) {
            loadingText.textContent = message;
            loadingText.className = 'text-red-400';
        }
    }

    setupEventListeners() {
        // Add any additional event listeners here
        console.log('[ADVANCED] Event listeners setup complete');
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('[ADVANCED] DOM loaded, initializing Advanced Analytics...');
    new AdvancedAnalytics();
});
