/**
 * App Shell - slim main entry for the Alpine.js application.
 *
 * Merges module slices (loaded before this file) with core methods.
 * Module slices are loaded conditionally based on UI_CONTRIBUTION["scripts"].
 * Execute slices self-register via slice-registry.js — no manual detection needed.
 *
 * Load order: initial-state.js → ws-handlers.js → phase-hooks.js → slice-registry.js → module slices → app-shell.js
 */

// Method names that need delegation to the active execute slice
const _executeMethodNames = [
    'activeNodeIds', 'updateNodeStatus', 'computeUniqueSkills',
    'getNodeLogs', 'getLatestLog', 'getNodeStatus',
    'renderDag', 'handleWheel', 'startDrag', 'drag', 'endDrag', 'resetDagView',
];

function unifiedApp() {
    return {
        // ── State ──
        ...getInitialState(),

        // ── Module slices (defensive merge: missing modules won't break core) ──
        ...(typeof treeSearchSlice === 'function' ? treeSearchSlice() : {}),
        ...(typeof skillReviewSlice === 'function' ? skillReviewSlice() : {}),
        ...(typeof dagPlanSlice === 'function' ? dagPlanSlice() : {}),
        ...(typeof recipeSlice === 'function' ? recipeSlice() : {}),

        // ── Execute slice delegation (dispatches to the active engine's slice) ──
        ..._executeMethodNames.reduce((acc, name) => {
            acc[name] = function(...args) {
                const slice = _executeSliceRegistry[this.executionMode] || _executeSliceRegistry['dag'];
                if (slice && typeof slice[name] === 'function') {
                    return slice[name].apply(this, args);
                }
            };
            return acc;
        }, {}),

        // ── Core methods ──

        mainLogs() {
            return this.logs.filter(l => !l.node_id);
        },

        trimLogs() {
            if (this.logs.length > this.maxLogs) {
                this.logs.splice(0, this.logs.length - this.maxLogs);
            }
        },

        appendLog(entry) {
            this.logs.push(entry);
            this.trimLogs();
        },

        scrollLogsToBottom() {
            const container = this.$refs.logContainer;
            if (container) container.scrollTop = container.scrollHeight;
        },

        init() {
            // Expose instance for onclick handlers in rendered HTML
            window.unifiedAppInstance = this;

            this.connect();

            // Fallback: if WebSocket init doesn't arrive within 3s, show UI anyway
            this._initTimeout = setTimeout(() => {
                if (!this.initialized) this.initialized = true;
            }, 3000);

            // Start elapsed time update timer
            setInterval(() => {
                if (this.startTime) {
                    const elapsed = Math.floor((Date.now() - this.startTime) / 1000);
                    this.elapsed = formatElapsed(elapsed);
                }
            }, 1000);

            // Core watcher: phase lifecycle hooks
            this.$watch('phase', (newPhase, oldPhase) => {
                firePhaseTransition(this, oldPhase, newPhase);
            });

            // Module watcher setup (defensive: missing modules won't break)
            if (typeof setupTreeSearchWatchers === 'function') setupTreeSearchWatchers(this);
            if (typeof setupSkillReviewWatchers === 'function') setupSkillReviewWatchers(this);

            // Watch for mode changes to conditionally fetch demos
            this.$watch('mode', (newMode) => {
                if (newMode === 'full' && this.demoTasks.length === 0) {
                    this.fetchDemos();
                }
            });

            // Fetch demos on initial load if in full mode
            if (this.mode === 'full') {
                this.fetchDemos();
            }

            // Fetch recipes on initial load
            if (typeof this.fetchRecipes === 'function') {
                this.$nextTick(() => {
                    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
                        this.fetchRecipes();
                    } else {
                        // Wait for connection
                        const checkConnection = setInterval(() => {
                            if (this.ws && this.ws.readyState === WebSocket.OPEN) {
                                this.fetchRecipes();
                                clearInterval(checkConnection);
                            }
                        }, 100);
                        // Give up after 5 seconds
                        setTimeout(() => clearInterval(checkConnection), 5000);
                    }
                });
            }

            // Resync state after tab is backgrounded and restored
            document.addEventListener('visibilitychange', () => {
                if (document.visibilityState !== 'visible') return;
                if (!this.connected) {
                    this.connect();
                    return;
                }
                if (this.ws && this.ws.readyState === WebSocket.OPEN) {
                    this.ws.send(JSON.stringify({ type: 'sync' }));
                }
            });
        },

        connect() {
            if (this.ws && (this.ws.readyState === WebSocket.OPEN || this.ws.readyState === WebSocket.CONNECTING)) {
                return;
            }
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            this.ws = new WebSocket(`${protocol}//${window.location.host}/ws`);

            this.ws.onopen = () => {
                this.connected = true;
            };

            this.ws.onclose = () => {
                this.connected = false;
                setTimeout(() => this.connect(), 2000);
            };

            this.ws.onmessage = (event) => {
                const msg = JSON.parse(event.data);
                this.handleMessage(msg);
            };
        },

        handleMessage(msg) {
            // Dispatch through handler registry
            dispatchMessage(this, msg);
        },

        restoreState(data) {
            const restoredPhase = data.phase || 'idle';
            if (restoredPhase === 'complete' || restoredPhase === 'error') {
                this.completionModalDismissed = true;
                this.completionTriggeredLive = false;
            }
            this.phase = restoredPhase;
            this.task = data.task || '';
            this.elapsed = data.elapsed || '0:00';

            // Restore mode state (for execute mode)
            this.mode = data.mode || 'full';
            this.runMode = data.run_mode || null;
            this.presetSkills = data.preset_skills || [];
            // Restore execution mode for unified flow
            this.executionMode = data.execution_mode || 'dag';
            // Restore available engines for skill review UI
            this.availableEngines = data.available_engines || [];
            // Restore working directory
            this.workDir = data.work_dir || '';
            // Restore UI hints
            if (data.ui_hints) this.uiHints = data.ui_hints;

            if (data.elapsed && data.task) {
                const totalSeconds = parseElapsed(data.elapsed);
                if (!Number.isNaN(totalSeconds)) {
                    this.startTime = Date.now() - totalSeconds * 1000;
                }
            }
            const unifiedLogs = data.logs || [];
            const orchestratorLogs = data.orchestrator?.logs || [];
            this.logs = unifiedLogs.concat(orchestratorLogs);
            this.trimLogs();
            this.treeData = data.tree_data;
            this.searchEvents = data.search_events || [];
            if (data.search_result) {
                this.searchResult = data.search_result;
                this.selectedSkills = data.selected_skill_ids || [];
            }
            // Restore dormant suggestions from layered search
            this.dormantSuggestions = data.dormant_suggestions || [];
            // Restore recipe recommendations
            this.recommendedRecipes = data.recommended_recipes || [];
            // Restore completion status and error message
            this.completionResultStatus = data.completion_status || null;
            this.errorMessage = data.error_message || null;
            // Restore uploaded files from backend paths
            if (data.files && data.files.length > 0) {
                this.uploadedFiles = data.files.map(p => ({
                    name: p.split('/').pop(),
                    path: p,
                    size: 0
                }));
            }
            // Restore searchComplete state from backend
            this.searchComplete = data.search_complete || false;
            // Restore waitingForNodes state based on phase and execution mode
            // Free-Style mode doesn't use node visualization
            if ((data.phase === 'planning' || data.phase === 'executing') && data.execution_mode !== 'free-style') {
                this.waitingForNodes = true;
            }
            if (data.orchestrator) {
                this.orchestrator = data.orchestrator;
                // If we have nodes data, turn off waitingForNodes
                if (data.orchestrator.nodes && data.orchestrator.nodes.length > 0) {
                    this.waitingForNodes = false;
                    this.computeUniqueSkills();  // Recompute skill list from restored nodes
                }
                // Restore plan selection modal state
                if (data.orchestrator.waiting_for_selection && data.orchestrator.plans?.length > 0) {
                    this.showPlanSelection = true;
                }
            }
            // Restore skill groups
            if (data.skill_groups) {
                this.skillGroups = data.skill_groups;
                // Restore custom config from skill groups
                const customGroup = data.skill_groups.find(g => g.is_configurable);
                if (customGroup) {
                    this.customConfig = {
                        skills_dir: customGroup.custom_skills_dir || '',
                        tree_path: customGroup.custom_tree_path || ''
                    };
                }
            }
            // Mark app as initialized (gate opens, spinner hides)
            this.initialized = true;

            // Render tree and replay events after restore (only in full mode)
            if (this.treeData && this.mode === 'full') {
                this.$nextTick(() => {
                    this.renderSearchTree();
                    this.treeRendered = true;
                    // Apply all historical search events to tree visualization
                    this.searchEvents.forEach(e => this.updateTreeNode(e));
                });
            }
        },

        getPhaseLabel() {
            // In execute mode, show run mode info
            if (this.mode === 'execute') {
                const modeLabels = {
                    'baseline': 'Baseline',
                    'free-style': 'Free-Style',
                    'dag': 'DAG'
                };
                const runModeLabel = modeLabels[this.runMode] || this.runMode || '';
                const phaseLabels = {
                    'idle': runModeLabel ? `${runModeLabel} Mode - Starting` : 'Starting',
                    'planning': runModeLabel ? `${runModeLabel} Mode - Planning` : 'Planning',
                    'executing': runModeLabel ? `${runModeLabel} Mode - Executing` : 'Executing',
                    'complete': runModeLabel ? `${runModeLabel} Mode - Complete` : 'Complete',
                    'error': 'Error'
                };
                return phaseLabels[this.phase] || this.phase;
            }
            // Full mode labels
            const labels = {
                'idle': 'Ready',
                'searching': 'Searching Skill Tree',
                'reviewing': 'Review Skills',
                'planning': 'Planning',
                'executing': 'Executing',
                'complete': 'Complete',
                'error': 'Error'
            };
            return labels[this.phase] || this.phase;
        },

        isExecuteMode() {
            return this.mode === 'execute';
        },

        endTaskEarly() {
            this.showEndTaskConfirm = true;
        },

        confirmEndTask() {
            this.showEndTaskConfirm = false;
            this.resetToStart();
        },

        cancelEndTask() {
            this.showEndTaskConfirm = false;
        },

        resetToStart() {
            // Send reset message to backend
            this.ws.send(JSON.stringify({ type: 'reset' }));
            // Reset all frontend state using centralized function
            resetAppState(this);
        },

        closeModals() {
            this.showPlanSelection = false;
            this.pendingPlanIndex = null;
            this.showTreeBrowser = false;
            this.treeBrowserSearch = '';
            this.treeBrowserCollapsed = new Set();
            this.selectedNodeId = null;
            this.selectedSkillDetail = null;
            this.showSaveRecipeModal = false;
            this.savingRecipe = false;
        },

        // ── File Upload (idle phase core) ──

        async handleFileSelect(event) {
            await this.uploadFiles(event.target.files);
            event.target.value = '';
        },

        async handleDrop(event) {
            this.dragOver = false;
            await this.uploadFiles(event.dataTransfer.files);
        },

        async uploadFiles(files) {
            if (!files || files.length === 0) return;
            this.uploading = true;
            this.uploadMessage = '';
            this.uploadError = false;

            const formData = new FormData();
            for (const file of files) {
                formData.append('files', file);
            }

            try {
                const response = await fetch('/api/upload', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error(`Upload failed: ${response.status}`);
                }

                const result = await response.json();
                this.uploadedFiles.push(...result.files);
                this.uploadMessage = `Successfully uploaded ${result.files.length} file(s)`;
                this.uploadError = false;
            } catch (error) {
                console.error('Upload failed:', error);
                this.uploadMessage = `Upload failed: ${error.message}`;
                this.uploadError = true;
            } finally {
                this.uploading = false;
                setTimeout(() => { this.uploadMessage = ''; }, 3000);
            }
        },

        async removeFile(index) {
            const file = this.uploadedFiles[index];
            try {
                await fetch(`/api/upload/${encodeURIComponent(file.name)}`, { method: 'DELETE' });
            } catch (error) {
                console.error('Delete failed:', error);
            }
            this.uploadedFiles.splice(index, 1);
        },

        formatFileSize(bytes) {
            if (bytes < 1024) return bytes + ' B';
            if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
            return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
        },

        // ── Dormant Skills ──

        addDormantSkill(skill) {
            // Add to searchResult.skills if not already there
            if (!this.searchResult.skills.find(s => s.id === skill.id)) {
                this.searchResult.skills.push(skill);
            }
            // Select it if not already selected
            if (!this.selectedSkills.includes(skill.id)) {
                this.selectedSkills.push(skill.id);
            }
            // Notify backend
            if (this.ws && this.ws.readyState === WebSocket.OPEN) {
                this.ws.send(JSON.stringify({ type: 'update_skills', skill_ids: this.selectedSkills }));
            }
        },

        // ── Demos ──

        async fetchDemos() {
            try {
                const response = await fetch('/api/demos');
                if (response.ok) {
                    const data = await response.json();
                    this.demoTasks = data.demos || [];
                }
            } catch (error) {
                console.error('Failed to fetch demos:', error);
            }
        },

        async loadDemo(demoId) {
            if (this.loadingDemoId) return;
            this.loadingDemoId = demoId;

            try {
                const response = await fetch(`/api/demos/${demoId}/load`, { method: 'POST' });
                if (response.ok) {
                    const data = await response.json();
                    this.taskInput = data.prompt || '';
                    this.uploadedFiles = data.files || [];
                    this.uploadMessage = `Demo loaded: ${data.files?.length || 0} file(s) ready`;
                    this.uploadError = false;
                    setTimeout(() => { this.uploadMessage = ''; }, 3000);
                } else {
                    this.uploadMessage = 'Failed to load demo';
                    this.uploadError = true;
                    setTimeout(() => { this.uploadMessage = ''; }, 3000);
                }
            } catch (error) {
                console.error('Failed to load demo:', error);
                this.uploadMessage = `Failed to load demo: ${error.message}`;
                this.uploadError = true;
                setTimeout(() => { this.uploadMessage = ''; }, 3000);
            } finally {
                this.loadingDemoId = null;
            }
        }
    };
}

// Make available globally
window.unifiedApp = unifiedApp;
