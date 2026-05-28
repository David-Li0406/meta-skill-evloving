/**
 * Direct Execute module slice.
 * Minimal implementation for direct orchestration (no nodes, no DAG).
 * Provides stub methods so app-shell works without modification.
 */
function directExecuteSlice() {
    return {
        activeNodeIds() {
            return [];
        },

        updateNodeStatus() {},

        computeUniqueSkills() {
            this.uniqueSkills = [];
        },

        getNodeLogs() {
            return [];
        },

        getLatestLog() {
            return '';
        },

        getNodeStatus() {
            return 'pending';
        },
    };
}

window.directExecuteSlice = directExecuteSlice;
registerExecuteSlice('no-skill', directExecuteSlice);
