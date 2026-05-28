/**
 * Vector Search module slice.
 * Provides vector similarity search interaction, progress tracking, and event formatting.
 */
function vectorSearchSlice() {
    return {
        startSearch() {
            if (!this.taskInput.trim()) return;
            this.task = this.taskInput;
            this.startTime = Date.now();
            this.searchEvents = [];
            this.searchComplete = false;
            this.vectorSearchState = {
                embeddingQuery: false,
                queryEmbedded: false,
                topK: 10,
                totalSkills: 0,
            };
            // Use uploaded file paths
            const files = this.uploadedFiles.map(f => f.path);
            this.ws.send(JSON.stringify({
                type: 'start_search',
                task: this.task,
                task_name: this.taskNameInput.trim(),
                files: files
            }));
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
            const type = event.type;
            const data = event.data;

            if (type === 'search_start') {
                this.vectorSearchState.topK = data.top_k || 10;
                this.vectorSearchState.totalSkills = data.total_skills || 0;
            }
            if (type === 'embedding_query') {
                this.vectorSearchState.embeddingQuery = true;
            }
            if (type === 'query_embedded') {
                this.vectorSearchState.queryEmbedded = true;
            }
        },

        formatSearchEvent(event) {
            const type = event.type;
            const data = event.data;
            switch (type) {
                case 'search_start':
                    return `Starting search (top-${data.top_k}, ${data.total_skills} skills indexed)`;
                case 'embedding_query':
                    return `Embedding query: "${(data.query || '').substring(0, 50)}..."`;
                case 'query_embedded':
                    return 'Query embedded successfully';
                case 'search_complete':
                    return `Found ${data.result_count} similar skills`;
                case 'build_start':
                    return `Building index: ${data.total_skills} skills`;
                case 'build_progress':
                    return `Embedded ${data.embedded}/${data.total} skills`;
                case 'build_complete':
                    return data.cached ? 'Index loaded from cache' : 'Index built successfully';
                default:
                    return type;
            }
        },

        // No-ops for tree-specific methods that may be called from shared handlers
        renderSearchTree() {},
        updateTreeNode(event) {},
    };
}

/**
 * Register vector-search-specific Alpine.js watchers.
 */
function setupVectorSearchWatchers(app) {
    // No tree-specific watchers needed for vector search
}

window.treeSearchSlice = vectorSearchSlice;
window.setupTreeSearchWatchers = setupVectorSearchWatchers;
