/**
 * Skill Review module slice.
 * Provides skill selection, review, detail viewing, and directory tree methods.
 */
function skillReviewSlice() {
    return {
        toggleSkill(skillId, skillData = null) {
            const idx = this.selectedSkills.indexOf(skillId);
            if (idx === -1) {
                this.selectedSkills = [...this.selectedSkills, skillId];
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
            if (this.executionMode === 'dag') {
                this.waitingForNodes = true;
            }
            this.ws.send(JSON.stringify({
                type: 'confirm_skills',
                execution_mode: this.executionMode
            }));
        },

        selectSkillGroup(groupId) {
            if (this.phase !== 'idle') return;
            this.ws.send(JSON.stringify({ type: 'set_skill_group', group_id: groupId }));
        },

        setCustomConfig() {
            this.ws.send(JSON.stringify({
                type: 'set_custom_config',
                skills_dir: this.customConfig.skills_dir,
                tree_path: this.customConfig.tree_path
            }));
        },

        copyInstallCommands() {
            const selectedSkillData = this.searchResult.skills.filter(s => this.selectedSkills.includes(s.id));
            if (selectedSkillData.length === 0) {
                this.copyMessage = 'No skills selected';
                this.copyError = true;
                setTimeout(() => { this.copyMessage = ''; }, 3000);
                return;
            }

            const commands = selectedSkillData.map(skill => {
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

            if (this.fileLoadTimeout) {
                clearTimeout(this.fileLoadTimeout);
            }

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
            const fullPath = parentFullPath ? `${parentFullPath}/${tree.name}` : tree.name;
            const relativePath = depth === 0 ? '' : (parentRelPath ? `${parentRelPath}/${tree.name}` : tree.name);

            const isFile = tree.type === 'file';
            const isDir = tree.type === 'directory';
            const hasChildren = tree.children && tree.children.length > 0;
            const isCollapsed = this.collapsedDirs[fullPath] ?? (depth > 0);

            const icon = isDir ? (isCollapsed && hasChildren ? '\uD83D\uDCC1' : '\uD83D\uDCC2') : '\uD83D\uDCC4';
            const cursorClass = isFile ? 'cursor-pointer hover:bg-surface-tertiary rounded' :
                                (isDir && hasChildren ? 'cursor-pointer hover:bg-surface-tertiary rounded' : '');

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
            const currentState = this.collapsedDirs[path] ?? true;
            this.collapsedDirs[path] = !currentState;
        }
    };
}

/**
 * Register skill-review-specific Alpine.js watchers.
 * Called from app-shell init() with the app instance.
 */
function setupSkillReviewWatchers(app) {
    // Sync D3 tree browser visual state when selectedSkills changes
    app.$watch('selectedSkills', (newValue) => {
        if (app.mode === 'full') {
            app.$nextTick(() => {
                d3.selectAll('.tree-node--skill').each(function(d) {
                    if (d && d.data) {
                        d3.select(this).classed('tree-node--selected', newValue.includes(d.data.id));
                    }
                });
            });
        }
    });
}

window.skillReviewSlice = skillReviewSlice;
window.setupSkillReviewWatchers = setupSkillReviewWatchers;
