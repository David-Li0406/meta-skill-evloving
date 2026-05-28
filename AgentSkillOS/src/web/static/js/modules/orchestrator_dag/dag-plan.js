/**
 * DAG Plan module slice.
 * Provides plan selection, preview, and plan modal interaction methods.
 */
function dagPlanSlice() {
    return {
        selectPlan(index) {
            this.waitingForNodes = true;
            this.ws.send(JSON.stringify({ type: 'select_plan', index: index }));
            this.showPlanSelection = false;
            this.pendingPlanIndex = null;
        },

        preSelectPlan(index) {
            this.pendingPlanIndex = index;
        },

        confirmPlanSelection() {
            if (this.pendingPlanIndex !== null) {
                this.selectPlan(this.pendingPlanIndex);
            }
        },

        cancelPlanSelection() {
            this.pendingPlanIndex = null;
        },

        openPlanPreview(plan) {
            this.previewPlan = plan;
            this.previewZoom = 1.0;
            this.previewPanX = 0;
            this.previewPanY = 0;
        },

        closePlanPreview() {
            this.previewPlan = null;
        },

        renderLargePlanPreview() {
            if (!this.previewPlan) return '';
            const nodes = this.previewPlan.nodes || [];
            if (nodes.length === 0) return '<div class="text-gray-500 text-sm p-4">No nodes in this plan</div>';
            const dagData = computeDagLayout(nodes);
            return renderDagSvg(dagData, { showStatus: false });
        },

        handlePreviewWheel(e) {
            if (e.ctrlKey || e.metaKey) {
                e.preventDefault();
                const delta = e.deltaY > 0 ? -0.1 : 0.1;
                this.previewZoom = Math.min(3, Math.max(0.3, this.previewZoom + delta));
            }
        },

        startPreviewDrag(e) {
            this.isPreviewDragging = true;
            this.previewDragStartX = e.clientX - this.previewPanX;
            this.previewDragStartY = e.clientY - this.previewPanY;
        },

        dragPreview(e) {
            if (!this.isPreviewDragging) return;
            this.previewPanX = e.clientX - this.previewDragStartX;
            this.previewPanY = e.clientY - this.previewDragStartY;
        },

        endPreviewDrag() {
            this.isPreviewDragging = false;
        },

        resetPreviewView() {
            this.previewZoom = 1.0;
            this.previewPanX = 0;
            this.previewPanY = 0;
        }
    };
}

window.dagPlanSlice = dagPlanSlice;
