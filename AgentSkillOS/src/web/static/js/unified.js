/**
 * Unified App Alpine.js Application
 * Manages the unified skill search + orchestration UI
 */

function unifiedApp() {
    return {
        // Connection state
        connected: false,
        ws: null,

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

        // File upload state
        uploadedFiles: [],      // [{name, path, size}]
        dragOver: false,
        uploading: false,
        uploadMessage: '',      // Upload result message
        uploadError: false,     // Whether it's an error

        // Copy message state
        copyMessage: '',        // Copy result message
        copyError: false,       // Whether it's an error

        // Log state
        logs: [],
        maxLogs: 2000,
        autoScroll: true,

        // Search state
        searchStats: { llmCalls: 0, nodesExplored: 0 },
        searchEvents: [],
        searchResult: { skills: [] },
        selectedSkills: [],
        searchComplete: false,  // Flag to indicate search has completed (waiting for user confirmation)
        treeData: null,
        treeRendered: false,
        pendingTreeEvents: [],

        // Pruning state
        isPruning: false,
        pruneSkillCount: 0,
        prunedSkillCount: 0,

        // Orchestrator state
        orchestrator: null,
        workDir: '',  // Working directory relative path (e.g., runs/20260124-dag-xxx)
        showPlanSelection: false,
        showTreeBrowser: false,
        treeBrowserSearch: '',
        treeBrowserCollapsed: new Set(),  // Track collapsed node IDs
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
        pendingPlanIndex: null,  // Pre-selected plan index

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
        viewingFile: null,          // {name, path, content, error, is_binary}
        viewingFileLoading: false,
        fileLoadTimeout: null,      // Timeout handle for file loading

        // Directory tree collapse state
        collapsedDirs: {},          // {path: true/false}

        // Method: logs from main agent only
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

        // Method: active node IDs (running or recently completed with logs)
        activeNodeIds() {
            if (!this.orchestrator || !this.orchestrator.nodes) return [];
            const withLogs = [...new Set(this.logs.filter(l => l.node_id).map(l => l.node_id))];
            return withLogs.filter(id => {
                const node = this.orchestrator.nodes.find(n => n.id === id);
                return node && (node.status === 'pending' || node.status === 'running' || node.status === 'completed' || node.status === 'failed');
            });
        },

        init() {
            // Expose instance for onclick handlers in rendered HTML
            window.unifiedAppInstance = this;

            this.connect();

            // Start elapsed time update timer
            setInterval(() => {
                if (this.startTime) {
                    const elapsed = Math.floor((Date.now() - this.startTime) / 1000);
                    this.elapsed = formatElapsed(elapsed);
                }
            }, 1000);

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

            // Watch for tree browser modal open (only in full mode)
            this.$watch('showTreeBrowser', (value) => {
                if (value && this.mode === 'full') {
                    this.$nextTick(() => this.renderTreeBrowser());
                }
            });

            // Watch for tree browser search changes
            this.$watch('treeBrowserSearch', (newValue, oldValue) => {
                // Clear collapse state when search changes (show all matching results expanded)
                if (newValue !== oldValue) {
                    this.treeBrowserCollapsed = new Set();
                }
                if (this.showTreeBrowser) {
                    this.$nextTick(() => this.renderTreeBrowser());
                }
            });

            // Watch selectedSkills changes to sync D3 tree browser visual state
            this.$watch('selectedSkills', (newValue) => {
                if (this.mode === 'full') {
                    this.$nextTick(() => {
                        d3.selectAll('.tree-node--skill').each(function(d) {
                            if (d && d.data) {
                                d3.select(this).classed('tree-node--selected', newValue.includes(d.data.id));
                            }
                        });
                    });
                }
            });

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
            switch (msg.type) {
                case 'init':
                    this.restoreState(msg.data);
                    break;
                case 'phase':
                    // Unified workflow phase (string) vs orchestrator phase (number)
                    if (typeof msg.data === 'number') {
                        if (!this.orchestrator) this.orchestrator = {};
                        this.orchestrator.current_phase = msg.data;
                    } else if (typeof msg.data === 'string') {
                        this.phase = msg.data;
                    } else if (msg.data && typeof msg.data.phase !== 'undefined') {
                        this.phase = msg.data.phase;
                    }
                    break;
                case 'work_dir':
                    this.workDir = msg.data.path || '';
                    break;
                case 'log':
                    this.appendLog(msg.data);
                    if (this.autoScroll && !msg.data.node_id) {
                        this.$nextTick(() => this.scrollLogsToBottom());
                    }
                    break;
                case 'log_batch':
                    if (Array.isArray(msg.data)) {
                        msg.data.forEach(logEntry => this.appendLog(logEntry));
                        if (this.autoScroll) {
                            this.$nextTick(() => this.scrollLogsToBottom());
                        }
                    }
                    break;
                case 'tree_data':
                    this.treeData = msg.data.tree;
                    this.treeRendered = false;
                    this.$nextTick(() => {
                        this.renderSearchTree();
                        this.treeRendered = true;
                        // Replay any pending events
                        this.pendingTreeEvents.forEach(e => this.updateTreeNode(e));
                        this.pendingTreeEvents = [];
                    });
                    break;
                case 'search_event':
                    this.searchEvents.push(msg.data);
                    this.updateSearchStats(msg.data);
                    // Queue event if tree not rendered yet
                    if (!this.treeRendered) {
                        this.pendingTreeEvents.push(msg.data);
                    } else {
                        this.updateTreeNode(msg.data);
                    }
                    break;
                case 'search_complete':
                    this.searchResult = { skills: msg.data.skills, llm_calls: msg.data.llm_calls };
                    this.selectedSkills = msg.data.selected_ids || [];
                    this.searchComplete = true;  // Mark search as complete, waiting for user confirmation
                    break;
                case 'skills_updated':
                    this.selectedSkills = msg.data.selected_ids;
                    break;
                case 'nodes':
                    if (!this.orchestrator) this.orchestrator = {};
                    this.orchestrator.nodes = msg.data.nodes;
                    this.waitingForNodes = false;
                    this.computeUniqueSkills();
                    break;
                case 'status':
                    this.updateNodeStatus(msg.data.node_id, msg.data.status, msg.data.time);
                    break;
                case 'plans':
                    if (!this.orchestrator) this.orchestrator = {};
                    this.orchestrator.plans = msg.data.plans;
                    this.showPlanSelection = true;
                    break;
                case 'error':
                    this.appendLog({ message: msg.data.message, level: 'error', timestamp: new Date().toLocaleTimeString() });
                    break;
                case 'skill_group_changed':
                    this.skillGroups = msg.data.groups || [];
                    break;
                case 'custom_config_changed':
                    this.customConfig = {
                        skills_dir: msg.data.skills_dir || '',
                        tree_path: msg.data.tree_path || ''
                    };
                    break;
                case 'skill_detail':
                    this.skillDetailLoading = false;
                    this.skillDirectoryTree = msg.data.directory_tree;
                    this.skillDetailName = msg.data.name || this.selectedSkillDetail?.name || '';
                    this.skillDetailDescription = msg.data.description || '';
                    this.renderedSkillMarkdown = marked.parse(msg.data.content || '');
                    // Reset file viewing state when loading new skill detail
                    this.viewingFile = null;
                    this.viewingFileLoading = false;
                    this.collapsedDirs = {};  // Reset collapse state for new skill
                    break;
                case 'file_content':
                    // Clear timeout
                    if (this.fileLoadTimeout) {
                        clearTimeout(this.fileLoadTimeout);
                        this.fileLoadTimeout = null;
                    }
                    this.viewingFileLoading = false;
                    if (this.viewingFile) {
                        if (msg.data.error) {
                            this.viewingFile.content = null;
                            this.viewingFile.error = msg.data.error;
                            this.viewingFile.is_binary = msg.data.is_binary || false;
                        } else {
                            this.viewingFile.content = msg.data.content;
                            this.viewingFile.error = null;
                            this.viewingFile.is_binary = false;
                        }
                    }
                    break;
                case 'ping':
                    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
                        this.ws.send(JSON.stringify({ type: 'pong' }));
                    }
                    break;
            }
        },

        restoreState(data) {
            this.phase = data.phase || 'idle';
            this.task = data.task || '';
            this.elapsed = data.elapsed || '0:00';

            // Restore mode state (for execute mode)
            this.mode = data.mode || 'full';
            this.runMode = data.run_mode || null;
            this.presetSkills = data.preset_skills || [];
            // Restore execution mode for unified flow
            this.executionMode = data.execution_mode || 'dag';
            // Restore working directory
            this.workDir = data.work_dir || '';

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

        // Check if we're in execute mode (no search UI)
        isExecuteMode() {
            return this.mode === 'execute';
        },

        startSearch() {
            if (!this.taskInput.trim()) return;
            this.task = this.taskInput;
            this.startTime = Date.now();
            this.searchStats = { llmCalls: 0, nodesExplored: 0 };
            this.searchEvents = [];
            this.treeRendered = false;
            this.pendingTreeEvents = [];
            this.searchComplete = false;  // Reset search complete flag
            // Reset pruning state
            this.isPruning = false;
            this.pruneSkillCount = 0;
            this.prunedSkillCount = 0;
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

        toggleSkill(skillId, skillData = null) {
            const idx = this.selectedSkills.indexOf(skillId);
            if (idx === -1) {
                this.selectedSkills = [...this.selectedSkills, skillId];
                // Reassign entire searchResult object to ensure Alpine detects the change
                if (skillData && !this.searchResult.skills.find(s => s.id === skillId)) {
                    this.searchResult = {
                        ...this.searchResult,
                        skills: [...this.searchResult.skills, skillData]
                    };
                }
            } else {
                this.selectedSkills = this.selectedSkills.filter((_, i) => i !== idx);
            }
            this.ws.send(JSON.stringify({ type: 'update_skills', skill_ids: this.selectedSkills }));
        },

        confirmSkills() {
            // Only show waiting state for DAG mode (Auto mode shows log only)
            if (this.executionMode === 'dag') {
                this.waitingForNodes = true;
            }
            this.ws.send(JSON.stringify({
                type: 'confirm_skills',
                execution_mode: this.executionMode
            }));
        },

        selectSkillGroup(groupId) {
            if (this.phase !== 'idle') {
                // Don't change skill group during active workflow
                return;
            }
            this.ws.send(JSON.stringify({ type: 'set_skill_group', group_id: groupId }));
        },

        setCustomConfig() {
            this.ws.send(JSON.stringify({
                type: 'set_custom_config',
                skills_dir: this.customConfig.skills_dir,
                tree_path: this.customConfig.tree_path
            }));
        },

        selectPlan(index) {
            this.waitingForNodes = true;
            this.ws.send(JSON.stringify({ type: 'select_plan', index: index }));
            this.showPlanSelection = false;
            this.pendingPlanIndex = null;
        },

        // Pre-select plan (called when clicking card)
        preSelectPlan(index) {
            this.pendingPlanIndex = index;
        },

        // Confirm plan selection (called when clicking confirm button)
        confirmPlanSelection() {
            if (this.pendingPlanIndex !== null) {
                this.selectPlan(this.pendingPlanIndex);
            }
        },

        // Cancel pre-selection
        cancelPlanSelection() {
            this.pendingPlanIndex = null;
        },

        resetSearch() {
            this.phase = 'idle';
            this.taskInput = this.task;
        },

        // Copy install commands to clipboard
        copyInstallCommands() {
            const selectedSkillData = this.searchResult.skills.filter(s => this.selectedSkills.includes(s.id));
            if (selectedSkillData.length === 0) {
                this.copyMessage = 'No skills selected';
                this.copyError = true;
                setTimeout(() => { this.copyMessage = ''; }, 3000);
                return;
            }

            // Generate cp commands, one per skill directory
            const commands = selectedSkillData.map(skill => {
                // skill_path is the path to SKILL.md, get its parent directory
                const skillDir = skill.skill_path.replace(/\/SKILL\.md$/, '');
                const skillName = skill.id;
                return `cp -r "${skillDir}" "./.claude/skills/${skillName}"`;
            });

            const fullCommand = `mkdir -p ./.claude/skills\n${commands.join('\n')}`;

            navigator.clipboard.writeText(fullCommand).then(() => {
                this.copyMessage = `Copied ${commands.length} install command(s)!`;
                this.copyError = false;
                setTimeout(() => { this.copyMessage = ''; }, 3000);
            }).catch(err => {
                console.error('Failed to copy:', err);
                this.copyMessage = 'Failed to copy to clipboard';
                this.copyError = true;
                setTimeout(() => { this.copyMessage = ''; }, 3000);
            });
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

            // Reset all frontend state to initial values
            this.phase = 'idle';
            this.task = '';
            this.taskInput = '';
            this.taskNameInput = '';
            this.elapsed = '0:00';
            this.startTime = null;
            this.logs = [];
            this.searchStats = { llmCalls: 0, nodesExplored: 0 };
            this.searchEvents = [];
            this.searchResult = { skills: [] };
            this.selectedSkills = [];
            this.searchComplete = false;
            this.treeData = null;
            this.treeRendered = false;
            this.pendingTreeEvents = [];
            this.orchestrator = null;
            this.workDir = '';
            this.showPlanSelection = false;
            this.pendingPlanIndex = null;
            this.showTreeBrowser = false;
            this.treeBrowserSearch = '';
            this.treeBrowserCollapsed = new Set();
            this.selectedNodeId = null;
            this.dagZoom = 1.0;
            this.panX = 0;
            this.panY = 0;
            this.waitingForNodes = false;
            this.uniqueSkills = [];
            this.isPruning = false;
            this.pruneSkillCount = 0;
            this.prunedSkillCount = 0;
            this.uploadedFiles = [];
            this.uploadMessage = '';
            this.uploadError = false;
            this.copyMessage = '';
            this.copyError = false;
            this.completionModalDismissed = false;
            this.showEndTaskConfirm = false;
            this.executionMode = 'dag';
            this.previewPlan = null;
            this.previewZoom = 1.0;
            this.previewPanX = 0;
            this.previewPanY = 0;
        },

        // File upload handlers
        async handleFileSelect(event) {
            await this.uploadFiles(event.target.files);
            event.target.value = '';  // Reset input for re-selection
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
                // Clear message after 3 seconds
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

        // Demo tasks handlers
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
                    // Fill the task input with the prompt
                    this.taskInput = data.prompt || '';
                    // Add the files to uploadedFiles
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
        },

        closeModals() {
            this.showPlanSelection = false;
            this.pendingPlanIndex = null;
            this.showTreeBrowser = false;
            this.treeBrowserSearch = '';
            this.treeBrowserCollapsed = new Set();  // Reset collapse state
            this.selectedNodeId = null;
            this.selectedSkillDetail = null;
        },

        openSkillDetail(skill) {
            this.selectedSkillDetail = skill;
            this.skillDetailLoading = true;
            this.skillDirectoryTree = null;
            this.renderedSkillMarkdown = '';
            this.ws.send(JSON.stringify({
                type: 'get_skill_detail',
                skill_id: skill.id,
                skill_path: skill.skill_path
            }));
        },

        closeSkillDetail() {
            this.selectedSkillDetail = null;
            this.skillDirectoryTree = null;
            this.renderedSkillMarkdown = '';
            this.skillDetailName = '';
            this.skillDetailDescription = '';
            this.viewingFile = null;
            this.viewingFileLoading = false;
        },

        viewFile(relativePath) {
            const fileName = relativePath.split('/').pop();
            this.viewingFile = { name: fileName, path: relativePath, content: '', error: null, is_binary: false };
            this.viewingFileLoading = true;

            // Clear previous timeout
            if (this.fileLoadTimeout) {
                clearTimeout(this.fileLoadTimeout);
            }

            // Set 10 second timeout
            this.fileLoadTimeout = setTimeout(() => {
                if (this.viewingFileLoading) {
                    this.viewingFileLoading = false;
                    if (this.viewingFile) {
                        this.viewingFile.content = null;
                        this.viewingFile.error = 'Request timed out';
                    }
                }
            }, 10000);

            this.ws.send(JSON.stringify({
                type: 'get_file_content',
                skill_path: this.selectedSkillDetail.skill_path,
                relative_path: relativePath
            }));
        },

        backToSkillMd() {
            this.viewingFile = null;
            this.viewingFileLoading = false;
        },

        renderDirectoryTree(tree, depth = 0, parentRelPath = '', parentFullPath = '') {
            if (!tree) return '';
            // fullPath includes root name (for collapse state uniqueness)
            const fullPath = parentFullPath ? `${parentFullPath}/${tree.name}` : tree.name;
            // relativePath excludes root name (for backend file requests)
            // At depth 0, relativePath is empty; at depth 1+, we build from parent
            const relativePath = depth === 0 ? '' : (parentRelPath ? `${parentRelPath}/${tree.name}` : tree.name);

            const isFile = tree.type === 'file';
            const isDir = tree.type === 'directory';
            const hasChildren = tree.children && tree.children.length > 0;
            // Default: collapse directories beyond depth 0
            const isCollapsed = this.collapsedDirs[fullPath] ?? (depth > 0);

            const icon = isDir ? (isCollapsed && hasChildren ? '📁' : '📂') : '📄';
            const cursorClass = isFile ? 'cursor-pointer hover:bg-surface-tertiary rounded' :
                                (isDir && hasChildren ? 'cursor-pointer hover:bg-surface-tertiary rounded' : '');

            // Use relativePath for viewFile (backend expects path relative to skill dir)
            // Use fullPath for toggleDir (needs unique key including root)
            const clickHandler = isFile ?
                `onclick="window.unifiedAppInstance.viewFile('${relativePath.replace(/'/g, "\\'")}')"` :
                (isDir && hasChildren ?
                    `onclick="window.unifiedAppInstance.toggleDir('${fullPath.replace(/'/g, "\\'")}')"` : '');

            let html = `<div class="flex items-center gap-1 py-0.5 px-1 ${cursorClass}" style="padding-left: ${depth * 12}px;" ${clickHandler}>
                <span class="text-sm">${icon}</span>
                <span class="text-sm text-gray-700 dark:text-gray-300 ${isFile ? 'hover:text-purple-500 dark:hover:text-purple-400' : ''}">${tree.name}</span>
            </div>`;

            if (hasChildren && !isCollapsed) {
                tree.children.forEach(child => {
                    html += this.renderDirectoryTree(child, depth + 1, relativePath, fullPath);
                });
            }
            return html;
        },

        toggleDir(path) {
            // Toggle collapse state; default is collapsed for depth > 0
            const currentState = this.collapsedDirs[path] ?? true;
            this.collapsedDirs[path] = !currentState;
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

        updateNodeStatus(nodeId, status, time) {
            if (this.orchestrator && this.orchestrator.nodes) {
                const node = this.orchestrator.nodes.find(n => n.id === nodeId);
                if (node) {
                    node.status = status;
                    if (time) node.time = time;
                }
            }
        },

        // Update unique skills from nodes
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

        scrollLogsToBottom() {
            const container = this.$refs.logContainer;
            if (container) container.scrollTop = container.scrollHeight;
        },

        // Get logs for a specific node
        getNodeLogs(nodeId) {
            return this.logs.filter(l => l.node_id === nodeId);
        },

        // Get latest log message for a node (single line)
        getLatestLog(nodeId) {
            const logs = this.getNodeLogs(nodeId);
            if (logs.length === 0) return 'Starting...';
            const latest = logs[logs.length - 1];
            return latest.message.substring(0, 100);
        },

        // Get node status
        getNodeStatus(nodeId) {
            if (!this.orchestrator || !this.orchestrator.nodes) return 'pending';
            const node = this.orchestrator.nodes.find(n => n.id === nodeId);
            return node?.status || 'pending';
        },

        // Render DAG SVG for orchestration phase
        renderDag() {
            if (!this.orchestrator || !this.orchestrator.nodes || this.orchestrator.nodes.length === 0) {
                return '';
            }
            const dagData = computeDagLayout(this.orchestrator.nodes);
            return renderDagSvg(dagData);
        },

        // DAG pan/zoom handlers
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
        },

        // Plan preview methods
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
        },

        renderSearchTree() {
            if (!this.treeData) return;
            const container = document.getElementById('search-tree');
            if (!container) return;

            // Clear container
            container.innerHTML = '';

            // Calculate dimensions based on tree size
            const root = d3.hierarchy(this.treeData);
            const leafCount = root.leaves().length;
            const depth = root.height;

            // Use vertical layout (top-to-bottom) with consistent node spacing
            const nodeVerticalSpacing = 30;
            const nodeHorizontalSpacing = 180;

            // Calculate SVG dimensions based on tree structure
            const width = Math.max((depth + 1) * nodeHorizontalSpacing + 100, container.clientWidth || 800);
            const height = Math.max(leafCount * nodeVerticalSpacing + 60, container.clientHeight || 480);

            // Use nodeSize for consistent spacing
            const treeLayout = d3.tree()
                .nodeSize([nodeVerticalSpacing, nodeHorizontalSpacing])
                .separation((a, b) => a.parent === b.parent ? 1 : 1.5);

            treeLayout(root);

            // Calculate bounds for proper positioning
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

            // Position g to center the tree vertically
            const g = svg.append('g')
                .attr('transform', `translate(80, ${-minY + 40})`);

            // Diagonal link generator using curves
            const diagonal = d3.linkHorizontal()
                .x(d => d.y)
                .y(d => d.x);

            // Links with curved paths (styles controlled by CSS .tree-link)
            g.selectAll('.tree-link')
                .data(root.links())
                .enter()
                .append('path')
                .attr('class', 'tree-link')
                .attr('d', diagonal);

            // Nodes
            const nodes = g.selectAll('.tree-node')
                .data(root.descendants())
                .enter()
                .append('g')
                .attr('class', d => `tree-node tree-node--${d.data.type || 'category'}`)
                .attr('id', d => `node-${d.data.id}`)
                .attr('transform', d => `translate(${d.y}, ${d.x})`);

            // Node circles with different sizes for different types
            nodes.append('circle')
                .attr('r', d => d.data.type === 'skill' ? 5 : (d.depth === 0 ? 10 : 7))
                .style('cursor', 'pointer');

            // Node labels (fill color controlled by CSS .tree-node text)
            nodes.append('text')
                .attr('dy', '0.31em')
                .attr('x', d => d.children || d._children ? -12 : 12)
                .attr('text-anchor', d => d.children || d._children ? 'end' : 'start')
                .text(d => d.data.name)
                .style('font-size', '11px')
                .style('pointer-events', 'none');

            // Add tooltips for skills
            nodes.filter(d => d.data.description)
                .append('title')
                .text(d => d.data.description);
        },

        // Initialize tree browser collapse state (collapse nodes at depth >= 3 by default)
        initTreeBrowserCollapse(node, depth = 0) {
            // If depth >= 3 and node has children and is not a skill, collapse it
            if (depth >= 3 && node.children && node.children.length > 0 && node.type !== 'skill') {
                this.treeBrowserCollapsed.add(node.id);
            }
            // Recursively process children
            if (node.children) {
                node.children.forEach(child => this.initTreeBrowserCollapse(child, depth + 1));
            }
        },

        // Toggle collapse state for a node
        toggleTreeBrowserCollapse(nodeId) {
            if (this.treeBrowserCollapsed.has(nodeId)) {
                this.treeBrowserCollapsed.delete(nodeId);
            } else {
                this.treeBrowserCollapsed.add(nodeId);
            }
            this.$nextTick(() => this.renderTreeBrowser());
        },

        // Apply collapse state to tree (remove children of collapsed nodes)
        applyTreeBrowserCollapse(node) {
            // If node is collapsed, remove its children and mark it
            if (this.treeBrowserCollapsed.has(node.id)) {
                return { ...node, children: undefined, _collapsed: true };
            }
            // Recursively process children
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
                return node; // No search query, return full tree
            }

            const q = query.toLowerCase().trim();

            // Check if current node matches
            const nodeMatches = (node.name && node.name.toLowerCase().includes(q)) ||
                                (node.description && node.description.toLowerCase().includes(q)) ||
                                (node.id && node.id.toLowerCase().includes(q));

            // If it's a skill node, directly determine match
            if (node.type === 'skill') {
                return nodeMatches ? { ...node } : null;
            }

            // If it's a category node, recursively filter children
            const filteredChildren = [];
            if (node.children) {
                for (const child of node.children) {
                    const filtered = this.filterTreeForSearch(child, query);
                    if (filtered) filteredChildren.push(filtered);
                }
            }

            // Keep this node if it matches or has matching children
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

            // Save scroll position before clearing (DOM rebuild resets scrollTop)
            const scrollTop = container.scrollTop;

            // Clear container
            container.innerHTML = '';

            // Filter tree data based on search query
            const filteredTree = this.filterTreeForSearch(this.treeData, this.treeBrowserSearch);
            if (!filteredTree) {
                container.innerHTML = '<div class="text-gray-500 dark:text-gray-400 p-8 text-center">No skills match your search</div>';
                return;
            }

            // Initialize collapse state on first render (only when not searching)
            if (this.treeBrowserCollapsed.size === 0 && !this.treeBrowserSearch) {
                this.initTreeBrowserCollapse(filteredTree);
            }

            // Apply collapse state to tree (only when not searching)
            const collapsedTree = this.treeBrowserSearch ? filteredTree : this.applyTreeBrowserCollapse(filteredTree);

            // Calculate dimensions based on filtered tree size
            const root = d3.hierarchy(collapsedTree);
            const leafCount = root.leaves().length;
            const depth = root.height;

            // Use vertical layout with consistent node spacing
            const nodeVerticalSpacing = 28;
            const nodeHorizontalSpacing = 200;

            // Use nodeSize for consistent spacing
            const treeLayout = d3.tree()
                .nodeSize([nodeVerticalSpacing, nodeHorizontalSpacing])
                .separation((a, b) => a.parent === b.parent ? 1 : 1.5);

            treeLayout(root);

            // Calculate bounds for proper positioning
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

            // Position g to center the tree vertically
            const g = svg.append('g')
                .attr('transform', `translate(100, ${-minY + 40})`);

            // Diagonal link generator using curves
            const diagonal = d3.linkHorizontal()
                .x(d => d.y)
                .y(d => d.x);

            // Links with curved paths (styles controlled by CSS .tree-link)
            g.selectAll('.tree-link')
                .data(root.links())
                .enter()
                .append('path')
                .attr('class', 'tree-link')
                .attr('d', diagonal);

            // Nodes
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
                    // Category nodes with children (or collapsed) are clickable
                    if (d.children || d.data._collapsed) return 'pointer';
                    return 'default';
                })
                .on('click', (event, d) => {
                    event.preventDefault();
                    if (d.data.type === 'skill') {
                        const skillData = { id: d.data.id, name: d.data.name, description: d.data.description || '', skill_path: d.data.skill_path || '' };
                        self.toggleSkill(d.data.id, skillData);
                        // D3 class update is handled by $watch on selectedSkills
                    } else if (d.children || d.data._collapsed) {
                        // Category node - toggle collapse (only when not searching)
                        if (!self.treeBrowserSearch) {
                            self.toggleTreeBrowserCollapse(d.data.id);
                        }
                    }
                });

            // Node circles with different sizes for different types
            nodes.append('circle')
                .attr('r', d => d.data.type === 'skill' ? 6 : (d.depth === 0 ? 10 : 8))
                .style('cursor', d => {
                    if (d.data.type === 'skill') return 'pointer';
                    if (d.children || d.data._collapsed) return 'pointer';
                    return 'default';
                });

            // Node labels (fill color controlled by CSS .tree-node text)
            nodes.append('text')
                .attr('dy', '0.31em')
                .attr('x', d => d.children || d._children ? -14 : 14)
                .attr('text-anchor', d => d.children || d._children ? 'end' : 'start')
                .text(d => d.data.name)
                .style('font-size', '12px')
                .style('pointer-events', 'none');

            // Add expand/collapse indicators (+/-) for category nodes with children
            nodes.filter(d => d.data.type !== 'skill' && (d.children || d.data._collapsed))
                .append('text')
                .attr('class', 'collapse-indicator')
                .attr('x', -20)
                .attr('dy', '0.35em')
                .attr('text-anchor', 'middle')
                .text(d => d.data._collapsed ? '+' : '−')
                .style('font-size', '14px')
                .style('font-weight', 'bold')
                .style('cursor', 'pointer')
                .style('fill', 'currentColor');

            // Add tooltips for all nodes with descriptions
            nodes.filter(d => d.data.description)
                .append('title')
                .text(d => d.data.description);

            // Restore scroll position after DOM rebuild
            container.scrollTop = scrollTop;
        },

        updateTreeNode(event) {
            const eventType = event.type;
            const data = event.data;

            if (eventType === 'node_enter') {
                // Clear previous exploring state, highlight current node
                d3.selectAll('.tree-node').classed('tree-node--exploring', false);
                d3.select(`#node-${data.node_id}`).classed('tree-node--exploring', true);
            }

            if (eventType === 'children_selected') {
                // Clear parent node exploring state
                d3.select(`#node-${data.parent_id}`).classed('tree-node--exploring', false);
                // Mark selected children
                data.selected.forEach(id => {
                    d3.select(`#node-${id}`).classed('tree-node--selected', true);
                });
                // Mark rejected children and their descendants
                data.rejected.forEach(id => {
                    // Mark rejected node as rejected (gray)
                    d3.select(`#node-${id}`).classed('tree-node--rejected', true);

                    // Mark all descendants of rejected node as pruned (red)
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
                // Skill selection results
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
                // Pruning started - show pruning state indicator
                this.isPruning = true;
                this.pruneSkillCount = data.skill_count || 0;
            }

            if (eventType === 'prune_complete') {
                // Pruning completed
                this.isPruning = false;
                this.prunedSkillCount = data.skill_count || 0;

                // Mark pruned skills in red
                if (data.pruned_ids) {
                    data.pruned_ids.forEach(id => {
                        d3.select(`#node-${id}`)
                            .classed('tree-node--pruned', true)
                            .classed('tree-node--skill-selected', false)
                            .classed('tree-node--selected', false);
                    });
                }

                // Mark remaining selected skills
                if (data.selected_ids) {
                    data.selected_ids.forEach(id => {
                        d3.select(`#node-${id}`)
                            .classed('tree-node--final', true)
                            .classed('tree-node--skill-selected', false);
                    });
                }
            }

            if (eventType === 'search_complete') {
                // Search completed - mark final selected skills
                d3.selectAll('.tree-node').classed('tree-node--exploring', false);
                const finalSkillIds = (data.skills || []).map(s => s.id);
                const finalSet = new Set(finalSkillIds);  // Use Set for O(1) lookup

                // Use requestAnimationFrame to avoid blocking the main thread
                requestAnimationFrame(() => {
                    // For all skill nodes: mark final selected as final, others as rejected
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

// Make available globally
window.unifiedApp = unifiedApp;
