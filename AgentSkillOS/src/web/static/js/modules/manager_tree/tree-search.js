/**
 * Tree Search module slice.
 * Provides search tree visualization, tree browser, and search interaction methods.
 */
function treeSearchSlice() {
    return {
        startSearch() {
            if (!this.taskInput.trim()) return;
            this.task = this.taskInput;
            this.startTime = Date.now();
            this.searchStats = { llmCalls: 0, nodesExplored: 0 };
            this.searchEvents = [];
            this.treeRendered = false;
            this.pendingTreeEvents = [];
            this.searchComplete = false;
            // Reset pruning state
            this.isPruning = false;
            this.pruneSkillCount = 0;
            this.prunedSkillCount = 0;
            // Reset recipe recommendations
            this.recommendedRecipes = [];
            // Use uploaded file paths
            const files = this.uploadedFiles.map(f => f.path);
            this.ws.send(JSON.stringify({
                type: 'start_search',
                task: this.task,
                task_name: this.taskNameInput.trim(),
                files: files
            }));
            // Trigger recipe recommendation in parallel with skill search
            if (typeof this.triggerRecipeRecommendation === 'function') {
                this.triggerRecipeRecommendation();
            }
        },

        confirmSearchResults() {
            this.searchComplete = false;
            this.ws.send(JSON.stringify({ type: 'confirm_search' }));
        },

        resetSearch() {
            this.phase = 'idle';
            this.taskInput = this.task;
        },

        updateSearchStats(event) {
            if (event.type === 'node_enter') {
                this.searchStats.nodesExplored++;
            }
            if (event.type === 'children_selected' && !event.data.auto_expand) {
                this.searchStats.llmCalls++;
            }
            if (event.type === 'skills_selected') {
                this.searchStats.llmCalls++;
            }
        },

        formatSearchEvent(event) {
            const type = event.type;
            const data = event.data;
            switch (type) {
                case 'node_enter':
                    return `Exploring: ${data.node_name}`;
                case 'children_selected':
                    return `Selected: ${data.selected.join(', ')}`;
                case 'skills_selected':
                    return `Skills: ${data.selected.join(', ')}`;
                default:
                    return type;
            }
        },

        renderSearchTree() {
            if (!this.treeData) return;
            const container = document.getElementById('search-tree');
            if (!container) return;

            container.innerHTML = '';

            const root = d3.hierarchy(this.treeData);
            const leafCount = root.leaves().length;
            const depth = root.height;

            const nodeVerticalSpacing = 30;
            const nodeHorizontalSpacing = 180;

            const width = Math.max((depth + 1) * nodeHorizontalSpacing + 100, container.clientWidth || 800);
            const height = Math.max(leafCount * nodeVerticalSpacing + 60, container.clientHeight || 480);

            const treeLayout = d3.tree()
                .nodeSize([nodeVerticalSpacing, nodeHorizontalSpacing])
                .separation((a, b) => a.parent === b.parent ? 1 : 1.5);

            treeLayout(root);

            let minY = Infinity, maxY = -Infinity;
            root.descendants().forEach(d => {
                minY = Math.min(minY, d.x);
                maxY = Math.max(maxY, d.x);
            });

            const treeHeight = maxY - minY + 80;
            const svgHeight = Math.max(treeHeight, height);

            const svg = d3.select(container)
                .append('svg')
                .attr('width', width)
                .attr('height', svgHeight);

            const g = svg.append('g')
                .attr('transform', `translate(80, ${-minY + 40})`);

            const diagonal = d3.linkHorizontal()
                .x(d => d.y)
                .y(d => d.x);

            g.selectAll('.tree-link')
                .data(root.links())
                .enter()
                .append('path')
                .attr('class', 'tree-link')
                .attr('d', diagonal);

            const nodes = g.selectAll('.tree-node')
                .data(root.descendants())
                .enter()
                .append('g')
                .attr('class', d => `tree-node tree-node--${d.data.type || 'category'}`)
                .attr('id', d => `node-${d.data.id}`)
                .attr('transform', d => `translate(${d.y}, ${d.x})`);

            nodes.append('circle')
                .attr('r', d => d.data.type === 'skill' ? 5 : (d.depth === 0 ? 10 : 7))
                .style('cursor', 'pointer');

            nodes.append('text')
                .attr('dy', '0.31em')
                .attr('x', d => d.children || d._children ? -12 : 12)
                .attr('text-anchor', d => d.children || d._children ? 'end' : 'start')
                .text(d => d.data.name)
                .style('font-size', '11px')
                .style('pointer-events', 'none');

            nodes.filter(d => d.data.description)
                .append('title')
                .text(d => d.data.description);
        },

        initTreeBrowserCollapse(node, depth = 0) {
            if (depth >= 3 && node.children && node.children.length > 0 && node.type !== 'skill') {
                this.treeBrowserCollapsed.add(node.id);
            }
            if (node.children) {
                node.children.forEach(child => this.initTreeBrowserCollapse(child, depth + 1));
            }
        },

        toggleTreeBrowserCollapse(nodeId) {
            if (this.treeBrowserCollapsed.has(nodeId)) {
                this.treeBrowserCollapsed.delete(nodeId);
            } else {
                this.treeBrowserCollapsed.add(nodeId);
            }
            this.$nextTick(() => this.renderTreeBrowser());
        },

        applyTreeBrowserCollapse(node) {
            if (this.treeBrowserCollapsed.has(node.id)) {
                return { ...node, children: undefined, _collapsed: true };
            }
            if (node.children) {
                return {
                    ...node,
                    children: node.children.map(child => this.applyTreeBrowserCollapse(child))
                };
            }
            return node;
        },

        filterTreeForSearch(node, query) {
            if (!query || query.trim() === '') {
                return node;
            }

            const q = query.toLowerCase().trim();

            const nodeMatches = (node.name && node.name.toLowerCase().includes(q)) ||
                                (node.description && node.description.toLowerCase().includes(q)) ||
                                (node.id && node.id.toLowerCase().includes(q));

            if (node.type === 'skill') {
                return nodeMatches ? { ...node } : null;
            }

            const filteredChildren = [];
            if (node.children) {
                for (const child of node.children) {
                    const filtered = this.filterTreeForSearch(child, query);
                    if (filtered) filteredChildren.push(filtered);
                }
            }

            if (nodeMatches || filteredChildren.length > 0) {
                return {
                    ...node,
                    children: filteredChildren.length > 0 ? filteredChildren : undefined
                };
            }

            return null;
        },

        renderTreeBrowser() {
            if (!this.treeData) return;
            const container = document.getElementById('tree-browser');
            if (!container) return;

            const scrollTop = container.scrollTop;
            container.innerHTML = '';

            const filteredTree = this.filterTreeForSearch(this.treeData, this.treeBrowserSearch);
            if (!filteredTree) {
                container.innerHTML = '<div class="text-gray-500 dark:text-gray-400 p-8 text-center">No skills match your search</div>';
                return;
            }

            if (this.treeBrowserCollapsed.size === 0 && !this.treeBrowserSearch) {
                this.initTreeBrowserCollapse(filteredTree);
            }

            const collapsedTree = this.treeBrowserSearch ? filteredTree : this.applyTreeBrowserCollapse(filteredTree);

            const root = d3.hierarchy(collapsedTree);
            const leafCount = root.leaves().length;
            const depth = root.height;

            const nodeVerticalSpacing = 28;
            const nodeHorizontalSpacing = 200;

            const treeLayout = d3.tree()
                .nodeSize([nodeVerticalSpacing, nodeHorizontalSpacing])
                .separation((a, b) => a.parent === b.parent ? 1 : 1.5);

            treeLayout(root);

            let minY = Infinity, maxY = -Infinity, maxX = 0;
            root.descendants().forEach(d => {
                minY = Math.min(minY, d.x);
                maxY = Math.max(maxY, d.x);
                maxX = Math.max(maxX, d.y);
            });

            const treeHeight = maxY - minY + 80;
            const treeWidth = maxX + 250;
            const width = Math.max(container.clientWidth || 900, treeWidth);
            const height = Math.max(treeHeight, 500);

            const svg = d3.select(container)
                .append('svg')
                .attr('width', width)
                .attr('height', height);

            const g = svg.append('g')
                .attr('transform', `translate(100, ${-minY + 40})`);

            const diagonal = d3.linkHorizontal()
                .x(d => d.y)
                .y(d => d.x);

            g.selectAll('.tree-link')
                .data(root.links())
                .enter()
                .append('path')
                .attr('class', 'tree-link')
                .attr('d', diagonal);

            const self = this;
            const nodes = g.selectAll('.tree-node')
                .data(root.descendants())
                .enter()
                .append('g')
                .attr('class', d => {
                    let cls = `tree-node tree-node--${d.data.type || 'category'}`;
                    if (d.data.type === 'skill' && self.selectedSkills.includes(d.data.id)) {
                        cls += ' tree-node--selected';
                    }
                    return cls;
                })
                .attr('id', d => `node-${d.data.id}`)
                .attr('transform', d => `translate(${d.y}, ${d.x})`)
                .style('cursor', d => {
                    if (d.data.type === 'skill') return 'pointer';
                    if (d.children || d.data._collapsed) return 'pointer';
                    return 'default';
                })
                .on('click', (event, d) => {
                    event.preventDefault();
                    if (d.data.type === 'skill') {
                        const skillData = { id: d.data.id, name: d.data.name, description: d.data.description || '', skill_path: d.data.skill_path || '' };
                        self.toggleSkill(d.data.id, skillData);
                    } else if (d.children || d.data._collapsed) {
                        if (!self.treeBrowserSearch) {
                            self.toggleTreeBrowserCollapse(d.data.id);
                        }
                    }
                });

            nodes.append('circle')
                .attr('r', d => d.data.type === 'skill' ? 6 : (d.depth === 0 ? 10 : 8))
                .style('cursor', d => {
                    if (d.data.type === 'skill') return 'pointer';
                    if (d.children || d.data._collapsed) return 'pointer';
                    return 'default';
                });

            nodes.append('text')
                .attr('dy', '0.31em')
                .attr('x', d => d.children || d._children ? -14 : 14)
                .attr('text-anchor', d => d.children || d._children ? 'end' : 'start')
                .text(d => d.data.name)
                .style('font-size', '12px')
                .style('pointer-events', 'none');

            nodes.filter(d => d.data.type !== 'skill' && (d.children || d.data._collapsed))
                .append('text')
                .attr('class', 'collapse-indicator')
                .attr('x', -20)
                .attr('dy', '0.35em')
                .attr('text-anchor', 'middle')
                .text(d => d.data._collapsed ? '+' : '\u2212')
                .style('font-size', '14px')
                .style('font-weight', 'bold')
                .style('cursor', 'pointer')
                .style('fill', 'currentColor');

            nodes.filter(d => d.data.description)
                .append('title')
                .text(d => d.data.description);

            container.scrollTop = scrollTop;
        },

        updateTreeNode(event) {
            const eventType = event.type;
            const data = event.data;

            if (eventType === 'node_enter') {
                d3.selectAll('.tree-node').classed('tree-node--exploring', false);
                d3.select(`#node-${data.node_id}`).classed('tree-node--exploring', true);
            }

            if (eventType === 'children_selected') {
                d3.select(`#node-${data.parent_id}`).classed('tree-node--exploring', false);
                data.selected.forEach(id => {
                    d3.select(`#node-${id}`).classed('tree-node--selected', true);
                });
                data.rejected.forEach(id => {
                    d3.select(`#node-${id}`).classed('tree-node--rejected', true);

                    const rejectedNode = d3.select(`#node-${id}`).datum();
                    if (rejectedNode && rejectedNode.descendants) {
                        rejectedNode.descendants().slice(1).forEach(descendant => {
                            d3.select(`#node-${descendant.data.id}`)
                                .classed('tree-node--exploring', false)
                                .classed('tree-node--pruned', true)
                                .classed('tree-node--skill', false)
                                .classed('tree-node--category', false);
                        });
                    }
                });
            }

            if (eventType === 'skills_selected') {
                data.selected.forEach(id => {
                    d3.select(`#node-${id}`)
                        .classed('tree-node--skill-selected', true)
                        .classed('tree-node--exploring', false);
                });
                data.rejected.forEach(id => {
                    d3.select(`#node-${id}`)
                        .classed('tree-node--skill-rejected', true);
                });
            }

            if (eventType === 'prune_start') {
                this.isPruning = true;
                this.pruneSkillCount = data.skill_count || 0;
            }

            if (eventType === 'prune_complete') {
                this.isPruning = false;
                this.prunedSkillCount = data.skill_count || 0;

                if (data.pruned_ids) {
                    data.pruned_ids.forEach(id => {
                        d3.select(`#node-${id}`)
                            .classed('tree-node--pruned', true)
                            .classed('tree-node--skill-selected', false)
                            .classed('tree-node--selected', false);
                    });
                }

                if (data.selected_ids) {
                    data.selected_ids.forEach(id => {
                        d3.select(`#node-${id}`)
                            .classed('tree-node--final', true)
                            .classed('tree-node--skill-selected', false);
                    });
                }
            }

            if (eventType === 'search_complete') {
                d3.selectAll('.tree-node').classed('tree-node--exploring', false);
                const finalSkillIds = (data.skills || []).map(s => s.id);
                const finalSet = new Set(finalSkillIds);

                requestAnimationFrame(() => {
                    d3.selectAll('.tree-node').each(function(d) {
                        if (d && d.data && d.data.type === 'skill') {
                            const node = d3.select(this);
                            if (finalSet.has(d.data.id)) {
                                node.classed('tree-node--final', true)
                                    .classed('tree-node--skill-selected', false)
                                    .classed('tree-node--skill-rejected', false)
                                    .classed('tree-node--selected', false);
                            } else {
                                node.classed('tree-node--skill-rejected', true)
                                    .classed('tree-node--skill-selected', false)
                                    .classed('tree-node--selected', false);
                            }
                        }
                    });
                });
            }
        }
    };
}

/**
 * Register tree-search-specific Alpine.js watchers.
 * Called from app-shell init() with the app instance.
 */
function setupTreeSearchWatchers(app) {
    // Re-render tree browser when modal opens
    app.$watch('showTreeBrowser', (value) => {
        if (value && app.mode === 'full') {
            app.$nextTick(() => app.renderTreeBrowser());
        }
    });

    // Clear collapse state and re-render on search change
    app.$watch('treeBrowserSearch', (newValue, oldValue) => {
        if (newValue !== oldValue) {
            app.treeBrowserCollapsed = new Set();
        }
        if (app.showTreeBrowser) {
            app.$nextTick(() => app.renderTreeBrowser());
        }
    });
}

window.treeSearchSlice = treeSearchSlice;
window.setupTreeSearchWatchers = setupTreeSearchWatchers;
