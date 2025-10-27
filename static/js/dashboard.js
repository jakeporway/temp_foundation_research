/**
 * Foundation Dashboard Interactive JavaScript
 * Handles filtering, searching, and dynamic content updates
 */

class FoundationDashboard {
    constructor() {
        this.foundations = [];
        this.filteredFoundations = [];
        this.activeFilters = {};
        this.searchTerm = '';
        this.isFilterPanelOpen = false;
        
        // Bind methods
        this.handleSearch = this.debounce(this.handleSearch.bind(this), 300);
        this.handleFilterChange = this.handleFilterChange.bind(this);
        this.renderFoundations = this.renderFoundations.bind(this);
        this.updateStats = this.updateStats.bind(this);
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.loadInitialData();
    }
    
    setupEventListeners() {
        // Search functionality
        const searchInput = document.getElementById('searchInput');
        const clearSearch = document.getElementById('clearSearch');
        
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.searchTerm = e.target.value;
                this.handleSearch();
                this.toggleClearButton();
            });
        }
        
        if (clearSearch) {
            clearSearch.addEventListener('click', () => {
                searchInput.value = '';
                this.searchTerm = '';
                this.handleSearch();
                this.toggleClearButton();
            });
        }
        
        // Filter toggle
        const filterToggle = document.getElementById('filterToggle');
        if (filterToggle) {
            filterToggle.addEventListener('click', () => {
                this.toggleFilterPanel();
            });
        }
        
        // Clear all filters
        const clearAllFilters = document.getElementById('clearAllFilters');
        if (clearAllFilters) {
            clearAllFilters.addEventListener('click', () => {
                this.clearAllFilters();
            });
        }
        
        // Filter checkboxes
        const filterPanel = document.getElementById('filterPanel');
        if (filterPanel) {
            filterPanel.addEventListener('change', (e) => {
                if (e.target.type === 'checkbox') {
                    this.handleFilterChange(e.target);
                }
            });
        }
        
        // Foundation card clicks
        document.addEventListener('click', (e) => {
            const card = e.target.closest('.foundation-card');
            if (card) {
                const foundationName = card.dataset.foundationName;
                if (foundationName) {
                    this.openFoundationDetail(foundationName);
                }
            }
        });
    }
    
    toggleClearButton() {
        const clearBtn = document.getElementById('clearSearch');
        if (clearBtn) {
            clearBtn.style.display = this.searchTerm ? 'block' : 'none';
        }
    }
    
    toggleFilterPanel() {
        const filterPanel = document.getElementById('filterPanel');
        const filterToggle = document.getElementById('filterToggle');
        
        this.isFilterPanelOpen = !this.isFilterPanelOpen;
        
        if (filterPanel) {
            filterPanel.classList.toggle('active', this.isFilterPanelOpen);
        }
        
        if (filterToggle) {
            filterToggle.textContent = this.isFilterPanelOpen ? 
                '⚙ Hide Filters' : '⚙ Filters';
        }
    }
    
    async loadInitialData() {
        try {
            const response = await fetch(window.foundationDashboard.apiEndpoints.foundations);
            const data = await response.json();
            
            this.foundations = data.foundations;
            this.filteredFoundations = [...this.foundations];
            
            this.renderFoundations();
            this.updateStats();
        } catch (error) {
            console.error('Error loading foundation data:', error);
            this.showError('Failed to load foundation data');
        }
    }
    
    async handleSearch() {
        await this.applyFilters();
    }
    
    handleFilterChange(checkbox) {
        const fieldName = checkbox.name;
        const value = checkbox.value;
        const isChecked = checkbox.checked;
        
        if (!this.activeFilters[fieldName]) {
            this.activeFilters[fieldName] = [];
        }
        
        if (isChecked) {
            if (!this.activeFilters[fieldName].includes(value)) {
                this.activeFilters[fieldName].push(value);
            }
        } else {
            this.activeFilters[fieldName] = this.activeFilters[fieldName].filter(v => v !== value);
            if (this.activeFilters[fieldName].length === 0) {
                delete this.activeFilters[fieldName];
            }
        }
        
        this.applyFilters();
        this.updateActiveFilterDisplay();
    }
    
    async applyFilters() {
        try {
            // Build query parameters
            const params = new URLSearchParams();
            
            if (this.searchTerm) {
                params.append('search', this.searchTerm);
            }
            
            // Add taxonomy filters
            for (const [fieldName, values] of Object.entries(this.activeFilters)) {
                values.forEach(value => {
                    params.append(fieldName, value);
                });
            }
            
            // Fetch filtered data
            const response = await fetch(`${window.foundationDashboard.apiEndpoints.foundations}?${params}`);
            const data = await response.json();
            
            this.filteredFoundations = data.foundations;
            
            this.renderFoundations();
            this.updateStats(data.stats);
            
        } catch (error) {
            console.error('Error applying filters:', error);
            this.showError('Failed to apply filters');
        }
    }
    
    renderFoundations() {
        const grid = document.getElementById('foundationsGrid');
        if (!grid) return;
        
        if (this.filteredFoundations.length === 0) {
            grid.innerHTML = `
                <div class="no-results">
                    <h3>No foundations found</h3>
                    <p>Try adjusting your search terms or filters</p>
                </div>
            `;
            return;
        }
        
        grid.innerHTML = this.filteredFoundations.map(foundation => this.createFoundationCard(foundation)).join('');
    }
    
    createFoundationCard(foundation) {
        const readinessLevel = this.getReadinessLevel(foundation.ai_readiness_score);
        const normalizedName = this.normalizeFoundationName(foundation.name);
        
        return `
            <div class="foundation-card" data-foundation-name="${normalizedName}">
                <div class="foundation-card-header">
                    <div class="foundation-name">${this.escapeHtml(foundation.name)}</div>
                    <div class="ai-score score-${foundation.ai_readiness_score}">
                        ${foundation.ai_readiness_score}/10
                    </div>
                </div>
                
                <div class="foundation-meta">
                    <div class="meta-item">
                        <div class="meta-label">Type</div>
                        <div class="meta-value">${this.escapeHtml(foundation.foundation_type || 'Unknown')}</div>
                    </div>
                    <div class="meta-item">
                        <div class="meta-label">Location</div>
                        <div class="meta-value">${this.escapeHtml(this.truncate(foundation.location || 'Unknown', 30))}</div>
                    </div>
                    <div class="meta-item">
                        <div class="meta-label">AI Integration</div>
                        <div class="meta-value">${this.escapeHtml(foundation.ai_funding_integration || 'Unknown')}</div>
                    </div>
                    <div class="meta-item">
                        <div class="meta-label">Focus</div>
                        <div class="meta-value">${this.escapeHtml(foundation.innovation_focus || 'Unknown')}</div>
                    </div>
                </div>
                
                ${foundation.readiness_level ? `
                    <div class="foundation-summary">
                        <strong>AI Strategy:</strong> ${this.escapeHtml(this.truncate(foundation.readiness_level, 150))}
                    </div>
                ` : ''}
            </div>
        `;
    }
    
    getReadinessLevel(score) {
        if (score >= 8) return 'High';
        if (score >= 6) return 'Medium-High';
        if (score >= 4) return 'Medium';
        return 'Low';
    }
    
    normalizeFoundationName(name) {
        if (!name) return '';
        // Match the Python normalization logic:
        // 1. Remove all non-word, non-space characters
        // 2. Replace spaces with underscores
        // 3. Remove leading/trailing whitespace
        let normalized = name.toLowerCase().replace(/[^\w\s]/g, '');
        normalized = normalized.replace(/\s+/g, '_').trim();
        return normalized;
    }
    
    updateStats(stats = null) {
        // Update current count
        const currentCount = document.getElementById('currentCount');
        const totalCount = document.getElementById('totalCount');
        
        if (currentCount) {
            currentCount.textContent = this.filteredFoundations.length;
        }
        
        if (totalCount) {
            totalCount.textContent = window.foundationDashboard.totalFoundations;
        }
        
        if (stats) {
            // Update average readiness
            const avgReadiness = document.getElementById('avgReadiness');
            if (avgReadiness && stats.ai_readiness) {
                avgReadiness.textContent = stats.ai_readiness.average || '-';
            }
            
            // Update high readiness count
            const highReadinessCount = document.getElementById('highReadinessCount');
            if (highReadinessCount && stats.ai_readiness) {
                highReadinessCount.textContent = stats.ai_readiness.high_count || '-';
            }
        }
    }
    
    updateActiveFilterDisplay() {
        const activeFilters = document.getElementById('activeFilters');
        const filterCount = document.getElementById('activeFilterCount');
        
        const totalFilters = Object.values(this.activeFilters).reduce((sum, arr) => sum + arr.length, 0);
        const hasSearch = this.searchTerm.length > 0;
        const totalActiveFilters = totalFilters + (hasSearch ? 1 : 0);
        
        // Update filter count badge
        if (filterCount) {
            if (totalActiveFilters > 0) {
                filterCount.textContent = totalActiveFilters;
                filterCount.classList.add('active');
            } else {
                filterCount.classList.remove('active');
            }
        }
        
        // Update active filters display
        if (activeFilters) {
            const filterTags = [];
            
            // Add search tag
            if (hasSearch) {
                filterTags.push(`
                    <div class="filter-tag">
                        Search: "${this.escapeHtml(this.searchTerm)}"
                        <span class="remove" onclick="dashboard.clearSearch()">×</span>
                    </div>
                `);
            }
            
            // Add taxonomy filter tags
            for (const [fieldName, values] of Object.entries(this.activeFilters)) {
                const displayName = this.getFilterDisplayName(fieldName);
                values.forEach(value => {
                    filterTags.push(`
                        <div class="filter-tag">
                            ${displayName}: ${this.escapeHtml(value)}
                            <span class="remove" onclick="dashboard.removeFilter('${fieldName}', '${this.escapeHtml(value)}')">×</span>
                        </div>
                    `);
                });
            }
            
            activeFilters.innerHTML = filterTags.join('');
        }
    }
    
    getFilterDisplayName(fieldName) {
        const taxonomy = window.foundationDashboard.taxonomyData;
        return taxonomy[fieldName]?.display_name || fieldName;
    }
    
    clearSearch() {
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.value = '';
        }
        this.searchTerm = '';
        this.handleSearch();
        this.toggleClearButton();
        this.updateActiveFilterDisplay();
    }
    
    removeFilter(fieldName, value) {
        const checkbox = document.querySelector(`input[name="${fieldName}"][value="${value}"]`);
        if (checkbox) {
            checkbox.checked = false;
            this.handleFilterChange(checkbox);
        }
    }
    
    clearAllFilters() {
        // Clear search
        this.clearSearch();
        
        // Clear all checkboxes
        const checkboxes = document.querySelectorAll('#filterPanel input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            checkbox.checked = false;
        });
        
        // Clear active filters
        this.activeFilters = {};
        
        // Refresh data
        this.applyFilters();
        this.updateActiveFilterDisplay();
    }
    
    openFoundationDetail(foundationName) {
        // Navigate to detail page
        const detailUrl = window.foundationDashboard.apiEndpoints.foundationDetail.replace('PLACEHOLDER', encodeURIComponent(foundationName));
        const pageUrl = detailUrl.replace('/api/foundation/', '/foundation/');
        window.location.href = pageUrl;
    }
    
    // Utility methods
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return String(text || '').replace(/[&<>"']/g, (m) => map[m]);
    }
    
    truncate(text, maxLength) {
        if (!text || text.length <= maxLength) return text;
        return text.substr(0, maxLength) + '...';
    }
    
    showError(message) {
        const grid = document.getElementById('foundationsGrid');
        if (grid) {
            grid.innerHTML = `
                <div class="error-message">
                    <h3>Error</h3>
                    <p>${this.escapeHtml(message)}</p>
                    <button onclick="location.reload()" class="btn-primary">Reload Page</button>
                </div>
            `;
        }
    }
}

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    if (window.foundationDashboard) {
        window.dashboard = new FoundationDashboard();
    }
});