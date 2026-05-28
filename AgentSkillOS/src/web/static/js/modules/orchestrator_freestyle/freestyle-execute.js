/**
 * Freestyle Execute module slice.
 * Provides node status tracking and log access methods for freestyle orchestration.
 * No DAG visualization (no renderDag, zoom/pan controls).
 */
function freestyleExecuteSlice() {
    return {
        activeNodeIds() {
            if (!this.orchestrator || !this.orchestrator.nodes) return [];
            const withLogs = [...new Set(this.logs.filter(l => l.node_id).map(l => l.node_id))];
            return withLogs.filter(id => {
                const node = this.orchestrator.nodes.find(n => n.id === id);
                return node && (node.status === 'pending' || node.status === 'running' || node.status === 'completed' || node.status === 'failed');
            });
        },

        updateNodeStatus(nodeId, status, time) {
            if (this.orchestrator && this.orchestrator.nodes) {
                const node = this.orchestrator.nodes.find(n => n.id === nodeId);
                if (node) {
                    node.status = status;
                    if (time) node.time = time;
                }
            }
        },

        computeUniqueSkills() {
            if (!this.orchestrator || !this.orchestrator.nodes) {
                this.uniqueSkills = [];
                return;
            }
            const skillSet = new Map();
            this.orchestrator.nodes.forEach((n) => {
                if (n.name && !skillSet.has(n.name)) {
                    skillSet.set(n.name, getSkillColor(skillSet.size));
                }
            });
            this.uniqueSkills = Array.from(skillSet.entries()).map(([name, color]) => ({ name, color }));
        },

        getNodeLogs(nodeId) {
            return this.logs.filter(l => l.node_id === nodeId);
        },

        getLatestLog(nodeId) {
            const logs = this.getNodeLogs(nodeId);
            if (logs.length === 0) return 'Starting...';
            const latest = logs[logs.length - 1];
            return latest.message.substring(0, 100);
        },

        getNodeStatus(nodeId) {
            if (!this.orchestrator || !this.orchestrator.nodes) return 'pending';
            const node = this.orchestrator.nodes.find(n => n.id === nodeId);
            return node?.status || 'pending';
        },
    };
}

window.freestyleExecuteSlice = freestyleExecuteSlice;
registerExecuteSlice('free-style', freestyleExecuteSlice);
