/**
 * WebSocket message handler registry.
 * Modules register their handlers; dispatchMessage routes messages.
 */

const _wsHandlers = {};

/**
 * Register a handler for a WebSocket message type.
 * @param {string} type - Message type (e.g. 'nodes', 'search_event')
 * @param {function(app, data)} fn - Handler function receiving (app, msg.data)
 */
function registerHandler(type, fn) {
    if (!_wsHandlers[type]) {
        _wsHandlers[type] = [];
    }
    _wsHandlers[type].push(fn);
}

/**
 * Dispatch a WebSocket message to registered handlers.
 * Falls back to core handlers for unregistered types.
 * @param {object} app - Alpine.js app instance
 * @param {object} msg - Parsed WebSocket message { type, data }
 * @returns {boolean} Whether a handler was found
 */
function dispatchMessage(app, msg) {
    const handlers = _wsHandlers[msg.type];
    if (handlers && handlers.length > 0) {
        for (const fn of handlers) {
            fn(app, msg.data);
        }
        return true;
    }
    return false;
}

// ── Core handlers (always registered) ──────────────────────────

registerHandler('init', function(app, data) {
    app.restoreState(data);
    if (data.ui_hints) app.uiHints = data.ui_hints;
    // Clear the initialization fallback timeout since we got server state
    if (app._initTimeout) {
        clearTimeout(app._initTimeout);
        app._initTimeout = null;
    }
});

registerHandler('ui_hints', function(app, data) {
    app.uiHints = data;
});

registerHandler('phase', function(app, data) {
    if (typeof data === 'number') {
        if (!app.orchestrator) app.orchestrator = {};
        app.orchestrator.current_phase = data;
    } else if (typeof data === 'string') {
        app.phase = data;
    } else if (data && typeof data.phase !== 'undefined') {
        app.phase = data.phase;
    }
});

registerHandler('work_dir', function(app, data) {
    app.workDir = data.path || '';
});

registerHandler('log', function(app, data) {
    app.appendLog(data);
    if (app.autoScroll && !data.node_id) {
        app.$nextTick(() => app.scrollLogsToBottom());
    }
});

registerHandler('log_batch', function(app, data) {
    if (Array.isArray(data)) {
        data.forEach(logEntry => app.appendLog(logEntry));
        if (app.autoScroll) {
            app.$nextTick(() => app.scrollLogsToBottom());
        }
    }
});

registerHandler('error', function(app, data) {
    app.errorMessage = data.message || null;
    app.appendLog({ message: data.message, level: 'error', timestamp: new Date().toLocaleTimeString() });
});

registerHandler('skill_group_changed', function(app, data) {
    app.skillGroups = data.groups || [];
});

registerHandler('custom_config_changed', function(app, data) {
    app.customConfig = {
        skills_dir: data.skills_dir || '',
        tree_path: data.tree_path || ''
    };
});

registerHandler('result', function(app, data) {
    app.completionResultStatus = data.status || null;
});

registerHandler('ping', function(app, _data) {
    if (app.ws && app.ws.readyState === WebSocket.OPEN) {
        app.ws.send(JSON.stringify({ type: 'pong' }));
    }
});

// ── Manager: tree search handlers ──────────────────────────────

registerHandler('tree_data', function(app, data) {
    app.treeData = data.tree;
    app.treeRendered = false;
    app.$nextTick(() => {
        app.renderSearchTree();
        app.treeRendered = true;
        app.pendingTreeEvents.forEach(e => app.updateTreeNode(e));
        app.pendingTreeEvents = [];
    });
});

registerHandler('search_event', function(app, data) {
    app.searchEvents.push(data);
    app.updateSearchStats(data);
    if (!app.treeRendered) {
        app.pendingTreeEvents.push(data);
    } else {
        app.updateTreeNode(data);
    }
});

registerHandler('search_complete', function(app, data) {
    app.searchResult = { skills: data.skills, llm_calls: data.llm_calls };
    app.selectedSkills = data.selected_ids || [];
    app.searchComplete = true;
    app.dormantSuggestions = data.dormant_suggestions || [];
});

registerHandler('skills_updated', function(app, data) {
    app.selectedSkills = data.selected_ids;
});

// ── Orchestrator: DAG handlers ─────────────────────────────────

registerHandler('nodes', function(app, data) {
    if (!app.orchestrator) app.orchestrator = {};
    app.orchestrator.nodes = data.nodes;
    app.waitingForNodes = false;
    app.computeUniqueSkills();
});

registerHandler('status', function(app, data) {
    app.updateNodeStatus(data.node_id, data.status, data.time);
});

registerHandler('plans', function(app, data) {
    if (!app.orchestrator) app.orchestrator = {};
    app.orchestrator.plans = data.plans;
    app.showPlanSelection = true;
});

// ── Skill detail handlers ──────────────────────────────────────

registerHandler('skill_detail', function(app, data) {
    app.skillDetailLoading = false;
    app.skillDirectoryTree = data.directory_tree;
    app.skillDetailName = data.name || app.selectedSkillDetail?.name || '';
    app.skillDetailDescription = data.description || '';
    app.renderedSkillMarkdown = marked.parse(data.content || '');
    app.viewingFile = null;
    app.viewingFileLoading = false;
    app.collapsedDirs = {};
});

registerHandler('file_content', function(app, data) {
    if (app.fileLoadTimeout) {
        clearTimeout(app.fileLoadTimeout);
        app.fileLoadTimeout = null;
    }
    app.viewingFileLoading = false;
    if (app.viewingFile) {
        if (data.error) {
            app.viewingFile.content = null;
            app.viewingFile.error = data.error;
            app.viewingFile.is_binary = data.is_binary || false;
        } else {
            app.viewingFile.content = data.content;
            app.viewingFile.error = null;
            app.viewingFile.is_binary = false;
        }
    }
});

// ── Recipe handlers ────────────────────────────────────────────

registerHandler('recipe_recommendations', function(app, data) {
    app.recommendedRecipes = data.recipes || [];
    app.recipeSearching = false;
});

registerHandler('recipe_saved', function(app, data) {
    app.recipes.push(data.recipe);
    app.showSaveRecipeModal = false;
    app.savingRecipe = false;
    app.saveRecipeName = '';
});

registerHandler('recipes_list', function(app, data) {
    app.recipes = data.recipes || [];
});

registerHandler('recipe_execution_started', function(app, data) {
    app.recommendedRecipes = [];
});

registerHandler('recipe_deleted', function(app, data) {
    if (data.success) {
        app.recipes = app.recipes.filter(r => r.id !== data.recipe_id);
    }
});

// Export
if (typeof window !== 'undefined') {
    window.registerHandler = registerHandler;
    window.dispatchMessage = dispatchMessage;
}
