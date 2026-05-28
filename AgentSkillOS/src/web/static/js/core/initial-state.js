/**
 * Unified initial state definition.
 * Single source of truth for all Alpine.js app state.
 */

function getInitialState() {
    return {
        // Connection state
        connected: false,
        ws: null,
        initialized: false,

        // Phase state
        phase: 'idle',
        task: '',
        taskInput: '',
        taskNameInput: '',
        elapsed: '0:00',
        startTime: null,

        // Mode state: "full" for complete workflow, "execute" for direct execution
        mode: 'full',
        runMode: null,  // "baseline" | "free-style" | "dag"
        presetSkills: [],

        // Execution mode for unified flow: "dag" or "free-style"
        executionMode: 'dag',

        // Available engines for skill review UI (populated from backend init)
        availableEngines: [],

        // UI hints from backend for conditional panel rendering
        uiHints: {
            search_visual: 'tree',
            has_planning: true,
            execution_visual: 'graph',
            has_search: true,
            has_skill_review: true,
        },

        // File upload state
        uploadedFiles: [],
        dragOver: false,
        uploading: false,
        uploadMessage: '',
        uploadError: false,

        // Copy message state
        copyMessage: '',
        copyError: false,

        // Log state
        logs: [],
        maxLogs: 2000,
        autoScroll: true,

        // Search state
        searchStats: { llmCalls: 0, nodesExplored: 0 },
        searchEvents: [],
        searchResult: { skills: [] },
        selectedSkills: [],
        searchComplete: false,
        treeData: null,
        treeRendered: false,
        pendingTreeEvents: [],

        // Pruning state
        isPruning: false,
        pruneSkillCount: 0,
        prunedSkillCount: 0,

        // Dormant suggestions from layered search
        dormantSuggestions: [],

        // Vector search state
        vectorSearchState: {
            embeddingQuery: false,
            queryEmbedded: false,
            topK: 10,
            totalSkills: 0,
        },

        // Orchestrator state
        orchestrator: null,
        workDir: '',
        showPlanSelection: false,
        showTreeBrowser: false,
        treeBrowserSearch: '',
        treeBrowserCollapsed: new Set(),
        selectedNodeId: null,
        dagZoom: 1.0,
        panX: 0,
        panY: 0,
        isDragging: false,
        dragStartX: 0,
        dragStartY: 0,
        waitingForNodes: false,
        uniqueSkills: [],
        completionModalDismissed: false,
        completionTriggeredLive: false,
        completionResultStatus: null,
        errorMessage: null,
        showEndTaskConfirm: false,

        // Skill group state
        skillGroups: [],

        // Plan preview state
        previewPlan: null,
        previewZoom: 1.0,
        previewPanX: 0,
        previewPanY: 0,
        isPreviewDragging: false,
        previewDragStartX: 0,
        previewDragStartY: 0,

        // Plan selection state
        pendingPlanIndex: null,

        // Custom skill group config
        customConfig: { skills_dir: '', tree_path: '' },

        // Demo tasks state
        demoTasks: [],
        loadingDemoId: null,

        // Skill detail modal state
        selectedSkillDetail: null,
        skillDetailLoading: false,
        skillDirectoryTree: null,
        renderedSkillMarkdown: '',
        skillDetailName: '',
        skillDetailDescription: '',

        // File viewing state
        viewingFile: null,
        viewingFileLoading: false,
        fileLoadTimeout: null,

        // Directory tree collapse state
        collapsedDirs: {},

        // Recipe state
        recipes: [],
        recommendedRecipes: [],
        recipeSearching: false,
        showSaveRecipeModal: false,
        saveRecipeName: '',
        savingRecipe: false,
        selectedRecipeDetail: null,
    };
}

/**
 * Reset app state to initial values (preserving ws connection).
 * Call this from resetToStart().
 */
function resetAppState(app) {
    const fresh = getInitialState();
    // Reset all state properties except ws, connected, demoTasks, and recipes
    for (const key of Object.keys(fresh)) {
        if (key === 'ws' || key === 'connected' || key === 'initialized' || key === 'demoTasks' || key === 'recipes') continue;
        app[key] = fresh[key];
    }
}

// Export
if (typeof window !== 'undefined') {
    window.getInitialState = getInitialState;
    window.resetAppState = resetAppState;
}
