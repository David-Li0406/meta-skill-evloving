/**
 * TheHUB V1.0 - Live Search
 * Real-time search for riders and clubs
 */

const LiveSearch = {
    debounceTimeout: null,
    minQueryLength: 2,
    debounceMs: 200,

    init() {
        document.querySelectorAll('.live-search').forEach(container => {
            this.initSearch(container);
        });
    },

    initSearch(container) {
        const input = container.querySelector('.live-search-input');
        const results = container.querySelector('.live-search-results');
        const clearBtn = container.querySelector('.search-clear');
        const type = container.dataset.searchType || 'all';
        const onSelect = container.dataset.onSelect;
        const allowAdd = container.dataset.allowAdd === 'true';

        if (!input || !results) return;

        // Input handler
        input.addEventListener('input', () => {
            clearTimeout(this.debounceTimeout);
            const query = input.value.trim();

            // Show/hide clear button
            if (clearBtn) {
                clearBtn.classList.toggle('hidden', query.length === 0);
            }

            if (query.length < this.minQueryLength) {
                this.hideResults(results, input);
                return;
            }

            this.debounceTimeout = setTimeout(() => {
                this.search(query, type, results, input, onSelect, allowAdd);
            }, this.debounceMs);
        });

        // Clear button
        if (clearBtn) {
            clearBtn.addEventListener('click', () => {
                input.value = '';
                clearBtn.classList.add('hidden');
                this.hideResults(results, input);
                input.focus();
            });
        }

        // Click outside to close
        document.addEventListener('click', (e) => {
            if (!container.contains(e.target)) {
                this.hideResults(results, input);
            }
        });

        // Keyboard navigation
        input.addEventListener('keydown', (e) => {
            const items = results.querySelectorAll('.live-search-result');
            const active = results.querySelector('.live-search-result.active');
            let activeIndex = Array.from(items).indexOf(active);

            switch (e.key) {
                case 'ArrowDown':
                    e.preventDefault();
                    activeIndex = Math.min(activeIndex + 1, items.length - 1);
                    this.setActiveItem(items, activeIndex);
                    break;
                case 'ArrowUp':
                    e.preventDefault();
                    activeIndex = Math.max(activeIndex - 1, 0);
                    this.setActiveItem(items, activeIndex);
                    break;
                case 'Enter':
                    e.preventDefault();
                    if (active) {
                        active.click();
                    }
                    break;
                case 'Escape':
                    this.hideResults(results, input);
                    break;
            }
        });
    },

    async search(query, type, container, input, onSelect, allowAdd) {
        try {
            const response = await fetch(`/api/search.php?q=${encodeURIComponent(query)}&type=${type}`);
            const data = await response.json();

            if (data.results.length === 0 && !allowAdd) {
                container.innerHTML = '<div class="live-search-empty">Inga resultat för "' + this.escapeHtml(query) + '"</div>';
            } else {
                let html = data.results.map((item, index) => `
                    <div class="live-search-result${index === 0 ? ' active' : ''}"
                         data-id="${item.id}"
                         data-type="${item.type}"
                         data-name="${this.escapeHtml(item.name)}"
                         role="option"
                         tabindex="-1">
                        <div class="live-search-result-avatar">${item.initials}</div>
                        <div class="live-search-result-info">
                            <span class="live-search-result-name">${this.escapeHtml(item.name)}</span>
                            <span class="live-search-result-meta">${this.escapeHtml(item.meta || '')}</span>
                        </div>
                    </div>
                `).join('');

                if (allowAdd && data.results.length < 5) {
                    html += `
                        <div class="live-search-result live-search-add" data-action="add">
                            <div class="live-search-result-avatar">+</div>
                            <div class="live-search-result-info">
                                <span class="live-search-result-name">Lägg till ny...</span>
                            </div>
                        </div>
                    `;
                }

                container.innerHTML = html;
            }

            this.showResults(container, input);

            // Click handlers
            container.querySelectorAll('.live-search-result').forEach(el => {
                el.addEventListener('click', () => {
                    const { id, type, name, action } = el.dataset;

                    if (action === 'add') {
                        // Handle add new
                        this.handleAddNew(type, container);
                        return;
                    }

                    if (onSelect && typeof window[onSelect] === 'function') {
                        // Custom callback
                        window[onSelect]({ id, type, name });
                    } else {
                        // Default: navigate to detail page
                        const basePath = type === 'club' ? '/database/club/' : '/database/rider/';
                        window.location.href = basePath + id;
                    }

                    this.hideResults(container, input);
                });
            });

        } catch (error) {
            console.error('Search error:', error);
            container.innerHTML = '<div class="live-search-empty">Sökning misslyckades</div>';
            this.showResults(container, input);
        }
    },

    showResults(container, input) {
        container.classList.remove('hidden');
        input.setAttribute('aria-expanded', 'true');
    },

    hideResults(container, input) {
        container.classList.add('hidden');
        input.setAttribute('aria-expanded', 'false');
    },

    setActiveItem(items, index) {
        items.forEach((item, i) => {
            item.classList.toggle('active', i === index);
            if (i === index) {
                item.scrollIntoView({ block: 'nearest' });
            }
        });
    },

    handleAddNew(type, container) {
        // Emit custom event for add new
        container.dispatchEvent(new CustomEvent('search:add', {
            bubbles: true,
            detail: { type }
        }));
    },

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
};

// Initialize on DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => LiveSearch.init());
} else {
    LiveSearch.init();
}

// Export for use in other modules
window.LiveSearch = LiveSearch;
