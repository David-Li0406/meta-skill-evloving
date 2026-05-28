/**
 * DAG Execute module slice.
 * Provides DAG rendering, node status tracking, zoom/pan, and log access methods.
 * Also used by freestyle and direct orchestrators.
 */
function dagExecuteSlice() {
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

        renderDag() {
            if (!this.orchestrator || !this.orchestrator.nodes || this.orchestrator.nodes.length === 0) {
                return '';
            }
            const dagData = computeDagLayout(this.orchestrator.nodes);
            return renderDagSvg(dagData);
        },

        handleWheel(e) {
            if (e.ctrlKey || e.metaKey) {
                e.preventDefault();
                const delta = e.deltaY > 0 ? -0.1 : 0.1;
                this.dagZoom = Math.min(3, Math.max(0.3, this.dagZoom + delta));
            }
        },

        startDrag(e) {
            this.isDragging = true;
            this.dragStartX = e.clientX - this.panX;
            this.dragStartY = e.clientY - this.panY;
        },

        drag(e) {
            if (!this.isDragging) return;
            this.panX = e.clientX - this.dragStartX;
            this.panY = e.clientY - this.dragStartY;
        },

        endDrag() {
            this.isDragging = false;
        },

        resetDagView() {
            this.dagZoom = 1.0;
            this.panX = 0;
            this.panY = 0;
        }
    };
}

window.dagExecuteSlice = dagExecuteSlice;
registerExecuteSlice('dag', dagExecuteSlice);
