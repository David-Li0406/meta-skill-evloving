    // Dashboard JS - All data from real APIs

    let serverOnline = false;
    const STATUS_LABELS = {
      running: '运行中',
      completed: '成功',
      success: '成功',
      failed: '失败',
      error: '失败',
      timeout: '超时',
      cancelled: '已取消',
      pending: '排队中',
      never_run: '排队中',
      unknown: '排队中'
    };
    const FAILURE_LABELS = new Set(['失败', '超时', '已取消']);
    const VALUE_ARG_FORMATS = { '--concurrency': 'equals', '--layer': 'separate' };
    const DEPTH_LAYER_MAP = { shallow: '1', normal: '2', deep: '3' };

    // Toast 通知
    function showToast(message, type = 'info', duration = 3000) {
      const container = document.getElementById('toast-container');
      if (!container) return;

      const colors = {
        success: 'bg-accent-green text-background-dark',
        error: 'bg-accent-red text-white',
        info: 'bg-primary text-background-dark',
        warning: 'bg-accent-yellow text-background-dark'
      };
      const icons = {
        success: 'check_circle',
        error: 'error',
        info: 'info',
        warning: 'warning'
      };

      const toast = document.createElement('div');
      toast.className = `flex items-center gap-3 px-4 py-3 rounded-lg shadow-lg ${colors[type]} transform translate-x-full transition-transform duration-300`;
      toast.innerHTML = `
        <span class="material-symbols-outlined text-lg">${icons[type]}</span>
        <span class="text-sm font-medium">${message}</span>
      `;

      container.appendChild(toast);

      // 动画进入
      requestAnimationFrame(() => {
        toast.classList.remove('translate-x-full');
      });

      // 自动消失
      setTimeout(() => {
        toast.classList.add('translate-x-full');
        setTimeout(() => toast.remove(), 300);
      }, duration);
    }

    const SENSITIVITY_PRESETS = {
      permissive: ['critical'],
      strict: ['critical', 'high', 'medium'],
      paranoid: ['critical', 'high', 'medium', 'low']
    };

    async function checkServer() {
      try {
        const res = await fetch('/api/projects', { method: 'GET' });
        if (res.ok) {
          serverOnline = true;
          return true;
        }
      } catch {}
      return false;
    }

    function showOfflineWarning() {
      const warning = document.createElement('div');
      warning.id = 'offline-warning';
      warning.className = 'fixed inset-0 bg-background-dark/95 z-[100] flex items-center justify-center';
      warning.innerHTML = `
        <div class="bg-surface-dark border border-border-dark rounded-xl p-8 max-w-md text-center">
          <span class="material-symbols-outlined text-6xl text-accent-red mb-4">cloud_off</span>
          <h2 class="text-xl font-bold mb-2">后端服务未启动</h2>
          <p class="text-text-muted mb-6">请先启动仪表盘服务器：</p>
          <code class="block bg-background-dark border border-border-dark rounded-lg p-4 text-sm text-primary font-mono mb-6">
            node scripts/dashboard.js --open
          </code>
          <p class="text-text-muted text-xs">服务启动后会自动打开浏览器</p>
          <button onclick="location.reload()" class="mt-6 px-6 py-2 bg-primary text-background-dark rounded-lg font-bold">
            重新检测
          </button>
        </div>
      `;
      document.body.appendChild(warning);
    }

    async function api(path, method = 'GET', body = null) {
      const opts = { method };
      if (body) {
        opts.headers = { 'Content-Type': 'application/json' };
        opts.body = JSON.stringify(body);
      }
      try {
        // 自动附加 project 参数
        let url = '/api' + path;
        if (currentProject && !path.includes('project=')) {
          url += (path.includes('?') ? '&' : '?') + 'project=' + encodeURIComponent(currentProject);
        }
        const res = await fetch(url, opts);
        return res.json();
      } catch (e) {
        console.error('API error:', path, e);
        return null;
      }
    }

    async function updateCache(payload) {
      if (!payload) return null;
      return await api('/cached-data', 'POST', payload);
    }

    async function initWithCache() {
      const cached = await api('/cached-data');
      if (cached && cached.project) {
        renderFromCache(cached);
      }
      await initProjects(cached?.project);
    }

    function renderFromCache(cached) {
      if (!cached) return;
      if (cached.insights) renderInsights(cached.insights);
      if (cached.operations) {
        if (cached.eta && !cached.operations.eta) {
          cached.operations.eta = cached.eta;
        }
        renderOpsSummary(cached.operations);
      }
      const footer = document.getElementById('footer-sync');
      if (footer) {
        footer.textContent = `缓存: ${cached.cachedAt || '--'}`;
      }
    }

    async function loadTaskSummaries() {
      const data = await api('/tasks');
      return Array.isArray(data) ? data : [];
    }

    async function loadTaskDetails(name) {
      return await api('/task-details/' + name) || { tasks: [] };
    }

    async function loadTaskHistory(name) {
      const data = await api('/history/' + name);
      return data?.history || [];
    }

    async function startTask(taskType, args = []) {
      return await api('/tasks/start', 'POST', { type: taskType, args }) || { success: false };
    }

    async function retryTask(taskName, taskId) {
      return await api(`/tasks/${taskName}/retry/${encodeURIComponent(taskId)}`, 'POST') || { success: false };
    }

    function normalizeConfig(raw) {
      const config = { ...raw };
      if (!Array.isArray(config.include)) config.include = [];
      if (!Array.isArray(config.ignore)) config.ignore = ['**/node_modules', 'dist/', '.git/'];
      config.features = { doc: true, audit: true, kanban: true, testAnalysis: true, ...(config.features || {}) };
      config.notify = { enabled: true, threshold: 3, onSessionStart: true, ...(config.notify || {}) };
      config.testing = { ...(config.testing || {}) };
      config.testing.coverage = { target: 90, minimum: 70, ...(config.testing.coverage || {}) };
      config.security = { ...(config.security || {}) };
      if (!Array.isArray(config.security.severity)) {
        config.security.severity = ['critical', 'high', 'medium', 'low'];
      }
      if (config.security.maxCyclomatic == null) {
        config.security.maxCyclomatic = 12;
      }
      return config;
    }

    function deriveSensitivityLevel(severity) {
      const list = Array.isArray(severity) ? severity : [];
      if (list.includes('low')) return 'paranoid';
      if (list.includes('medium') || list.includes('high')) return 'strict';
      return 'permissive';
    }

    async function loadConfig() {
      const data = await api('/config');
      if (!data || Object.keys(data).length === 0) {
        configLastSaved = '使用默认值';
        return normalizeConfig({});
      }
      configLastSaved = '从文件加载';
      return normalizeConfig(data);
    }

    async function saveConfig(config) {
      const res = await api('/config', 'PUT', config);
      return res && res.success ? { ok: true } : { ok: false };
    }

    async function loadProjects() {
      const data = await api('/projects');
      return data || { projects: [] };
    }

    async function loadAuditStatus() {
      return await api('/audit-status') || {};
    }

    async function loadTestStatus() {
      return await api('/test-status') || {};
    }

    async function loadStaleStatus() {
      return await api('/stale-status') || {};
    }

    async function loadTaskTypes() {
      return await api('/task-types') || { types: [] };
    }

    function toDisplayStatus(status) {
      if (!status) return '排队中';
      const key = String(status).toLowerCase();
      return STATUS_LABELS[key] || STATUS_LABELS[status] || '排队中';
    }

    function formatTime(value) {
      if (!value) return '--';
      const date = new Date(value);
      if (Number.isNaN(date.getTime())) return '--';
      return date.toLocaleTimeString();
    }

    function formatDuration(ms) {
      if (ms == null) return '--';
      if (ms < 1000) return `${ms}ms`;
      const totalSeconds = Math.round(ms / 1000);
      const minutes = Math.floor(totalSeconds / 60);
      const seconds = totalSeconds % 60;
      if (minutes > 0) return `${minutes}m ${String(seconds).padStart(2, '0')}s`;
      return `${seconds}s`;
    }

    function formatEtaDuration(ms) {
      if (!ms || ms <= 0) return '--';
      const totalSeconds = Math.round(ms / 1000);
      const hours = Math.floor(totalSeconds / 3600);
      const minutes = Math.floor((totalSeconds % 3600) / 60);
      const seconds = totalSeconds % 60;
      if (hours > 0) return `${hours}h ${String(minutes).padStart(2, '0')}m`;
      if (minutes > 0) return `${minutes}m ${String(seconds).padStart(2, '0')}s`;
      return `${seconds}s`;
    }

    function formatClockTime(value) {
      if (!value) return '--';
      const date = new Date(value);
      if (Number.isNaN(date.getTime())) return '--';
      return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
    }

    function normalizeStaleCounts(raw) {
      if (!raw) return { fresh: 0, stale: 0 };
      if (Array.isArray(raw)) {
        let fresh = 0;
        let stale = 0;
        raw.forEach((item) => {
          if (item?.status === 'fresh') {
            fresh += 1;
          } else if (item?.status === 'stale' || item?.status === 'missing') {
            stale += 1;
          }
        });
        return { fresh, stale };
      }
      const fresh = Number(raw.fresh || 0);
      let stale = Number(raw.stale || 0);
      if (raw.missing != null) {
        stale += Number(raw.missing || 0);
      }
      return { fresh, stale };
    }

    function buildTaskLogs(task, displayTarget, statusLabel) {
      const logs = [];
      if (task.startedAt) {
        logs.push({
          time: formatTime(task.startedAt),
          level: '信息',
          message: `开始处理 ${displayTarget}`
        });
      }
      if (task.completedAt) {
        logs.push({
          time: formatTime(task.completedAt),
          level: FAILURE_LABELS.has(statusLabel) ? '错误' : '信息',
          message: `完成: ${statusLabel}`
        });
      }
      if (task.error) {
        logs.push({
          time: formatTime(task.completedAt || task.startedAt),
          level: '错误',
          message: task.error
        });
      }
      if (task.result?.status) {
        logs.push({
          time: formatTime(task.completedAt || task.startedAt),
          level: '信息',
          message: `结果: ${task.result.status}`
        });
      }
      if (logs.length === 0) {
        logs.push({ time: '--', level: '信息', message: '暂无运行记录' });
      }
      return logs;
    }

    function buildTaskStack(task) {
      const stack = task.error || task.result?.reason || task.result?.error || '';
      return stack ? String(stack) : '无堆栈数据';
    }

    function buildTaskParams(task, taskName) {
      const params = task.context || {
        id: task.id,
        module: task.module,
        task: taskName,
        retryCount: task.retryCount,
        sessionId: task.sessionId
      };
      try {
        return JSON.stringify(params, null, 2);
      } catch {
        return String(params);
      }
    }

    function normalizeSubtask(task, taskName) {
      const rawId = task.module || task.id || task.path || taskName;
      const displayTarget = rawId || taskName;
      const displayName = String(displayTarget).split('/').filter(Boolean).pop() || displayTarget;
      const statusLabel = toDisplayStatus(task.status);
      const canRetry = task.canRetry === true || (task.canRetry == null && FAILURE_LABELS.has(statusLabel));
      const duration = task.duration != null
        ? formatDuration(task.duration)
        : (task.startedAt && task.completedAt)
          ? formatDuration(new Date(task.completedAt) - new Date(task.startedAt))
          : '--';
      return {
        id: `${taskName}:${task.id || rawId}`,
        taskId: task.id || rawId,
        taskName,
        status: statusLabel,
        canRetry,
        name: displayName,
        note: taskName,
        target: displayTarget,
        duration,
        logs: buildTaskLogs(task, displayTarget, statusLabel),
        metrics: {
          memory: task.retryCount ? `重试 ${task.retryCount} 次` : '--',
          speed: duration,
          node: task.sessionId ? String(task.sessionId).slice(0, 8) : '--'
        },
        raw: task
      };
    }

    function aggregateByStatus(histories) {
      const combined = {};
      histories.forEach((history) => {
        const run = Array.isArray(history) ? history[0] : null;
        if (!run?.byStatus) return;
        Object.entries(run.byStatus).forEach(([status, count]) => {
          combined[status] = (combined[status] || 0) + count;
        });
      });
      return combined;
    }

    function computeSuccessRate(byStatus) {
      const entries = Object.entries(byStatus || {});
      const total = entries.reduce((sum, [, count]) => sum + (count || 0), 0);
      if (total === 0) return 0;
      let failed = 0;
      entries.forEach(([status, count]) => {
        const key = String(status).toLowerCase();
        if (key.includes('error') || key.includes('fail') || key.includes('timeout') || key.includes('cancel')) {
          failed += count || 0;
        }
      });
      const success = Math.max(0, total - failed);
      return Math.round((success / total) * 1000) / 10;
    }

    function latestHistoryTime(histories) {
      let latest = null;
      histories.forEach((history) => {
        const run = Array.isArray(history) ? history[0] : null;
        const time = run?.completedAt || run?.archivedAt;
        if (!time) return;
        const date = new Date(time);
        if (!latest || date > latest) latest = date;
      });
      return latest;
    }

    let currentTasks = [];
    let activeTaskId = null;
    let currentProject = null;
    let projectList = [];
    let selectedTool = null;
    let selectedToolArgs = {};
    let currentConfig = null;
    let configLastSaved = '--';
    let activeOpsTab = 'logs';
    // 筛选和分组状态
    let filterStatus = 'all';
    let filterType = 'all';
    let groupByTask = false;
    // 自动刷新间隔（秒）
    const AUTO_REFRESH_INTERVAL = 30000;  // 30 秒
    let refreshInterval = null;

    async function initProjects(preferredProject = null) {
      const data = await loadProjects();
      projectList = data.projects || [];
      const selector = document.getElementById('project-selector');
      selector.innerHTML = '<option value="">选择项目...</option>' +
        projectList.map(p => `<option value="${p.path}">${p.name}</option>`).join('');

      // 自动选中第一个项目
      if (projectList.length > 0) {
        const preferred = preferredProject && projectList.find(p => p.path === preferredProject);
        const selected = preferred || projectList[0];
        selector.value = selected.path;
        await switchProject(selected.path);
      }
    }

    async function switchProject(projectPath) {
      currentProject = projectPath;
      if (!projectPath) return;
      lastInsightsRefreshAt = Date.now();

      // 并行加载所有数据
      const [projectData, audit, testStatus, staleStatus, config, eta] = await Promise.all([
        api('/project-data/' + encodeURIComponent(projectPath)),
        loadAuditStatus(),
        loadTestStatus(),
        loadStaleStatus(),
        loadConfig(),
        api('/eta')
      ]);

      const modules = projectData?.modules || [];
      const total = modules.length || 0;
      const ready = modules.filter(m => m.status === 'ready').length;
      const auditEnabled = modules.filter(m => m.enableAudit).length;

      // 计算总行数（从模块的 lines 字段累加）
      const totalLines = modules.reduce((sum, m) => sum + (m.lines || 0), 0);
      // 审计统计：使用 audit-status 返回的数据
      const staleStats = audit.stats || {};
      const claudeModules = audit.total || 0;
      const auditedModules = Math.max(0, claudeModules - (staleStats.never || 0));
      const auditedFiles = audit.totalFiles || 0;
      const discoveredFiles = audit.totalDiscoveredFiles || 0;
      const uncoveredFiles = audit.uncoveredFiles || 0;
      const coveragePercent = audit.coveragePercent || 0;

      const severityCounts = audit.severityCounts || {};
      const severityValues = ['critical', 'high', 'medium', 'low'].map(k => severityCounts[k] || 0);
      const maxSeverity = Math.max(...severityValues, 0);

      const docCoverage = audit.docCoveragePercent || 0;  // CLAUDE.md 覆盖率
      const auditCoverage = audit.coveragePercent || 0;   // 审计文件覆盖率
      const readyModules = (staleStats.fresh || 0) + (staleStats.clean || 0);
      const readyCoverage = auditedModules > 0
        ? Math.round((readyModules / auditedModules) * 100)
        : 0;
      const testCoverage = testStatus.coveragePercent || 0;  // 测试文件覆盖率
      const staleData = staleStatus || {};
      const staleClaude = normalizeStaleCounts(staleData.claude);
      const staleAudit = normalizeStaleCounts(staleData.audit);

      const insightsPayload = {
        lastSync: new Date().toLocaleTimeString(),
        audit: {
          total: audit.totalIssues || 0,
          trend: 0,
          modulesScanned: auditedModules,
          filesScanned: auditedFiles,
          discoveredFiles,
          uncoveredFiles,
          coveragePercent,
          history: audit.history || { resolved: 0, previous: 0, new: 0 },
          bars: [
            { label: "CRITICAL", value: maxSeverity ? (severityCounts.critical || 0) / maxSeverity : 0, count: severityCounts.critical || 0 },
            { label: "HIGH", value: maxSeverity ? (severityCounts.high || 0) / maxSeverity : 0, count: severityCounts.high || 0 },
            { label: "MEDIUM", value: maxSeverity ? (severityCounts.medium || 0) / maxSeverity : 0, count: severityCounts.medium || 0 },
            { label: "LOW", value: maxSeverity ? (severityCounts.low || 0) / maxSeverity : 0, count: severityCounts.low || 0 }
          ],
          dirCoverage: audit.dirCoverage || {}
        },
        tests: {
          value: Math.min(100, Math.round(testCoverage)),
          delta: 0,
          total: testStatus.total || 0,
          covered: testStatus.stats?.covered || 0,
          untested: testStatus.stats?.untested || 0
        },
        docs: {
          value: Math.min(100, docCoverage),
          core: Math.min(100, readyCoverage),
          auth: Math.min(100, auditCoverage)
        },
        stale: {
          claude: staleClaude,
          audit: staleAudit
        }
      };
      renderInsights(insightsPayload);

      // refreshOperations 和 renderConfig 可以并行
      const operationsSummary = await refreshOperations({ etaData: eta });
      renderConfig(config);

      await updateCache({
        cachedAt: new Date().toISOString(),
        project: projectPath,
        insights: insightsPayload,
        operations: operationsSummary,
        eta: eta?.eta || null
      });
    }

    function setActiveTab(tabKey) {
      console.log("setActiveTab:", tabKey);
      const tabButtons = document.querySelectorAll("[data-tab-button]");
      const tabPanels = document.querySelectorAll("[data-tab-panel]");
      console.log("Found panels:", tabPanels.length);
      tabButtons.forEach((button) => {
        const isActive = button.dataset.tabButton === tabKey;
        button.classList.toggle("is-active", isActive);
        button.setAttribute("aria-selected", isActive ? "true" : "false");
      });
      tabPanels.forEach((panel) => {
        const isActive = panel.dataset.tabPanel === tabKey;
        console.log("Panel:", panel.dataset.tabPanel, "isActive:", isActive);
        if (isActive) {
          panel.classList.remove("panel-hidden");
        } else {
          panel.classList.add("panel-hidden");
        }
      });
      const sidebarMap = { launchpad: "grid", operations: "analytics", insights: "analytics" };
      setActiveSidebar(sidebarMap[tabKey]);
    }

    function setActiveSidebar(sidebarKey) {
      const sidebarButtons = document.querySelectorAll("[data-sidebar-button]");
      sidebarButtons.forEach((button) => {
        const isActive = button.dataset.sidebarButton === sidebarKey;
        button.classList.toggle("is-active", isActive);
      });
    }

    function showRefreshing(show) {
      const el = document.getElementById('footer-sync');
      if (!el) return;
      if (show) {
        el.innerHTML = '<span class="animate-pulse">刷新中...</span>';
      }
    }

    async function refreshOperations(options = {}) {
      const hasEta = Object.prototype.hasOwnProperty.call(options, 'etaData');
      const etaData = options.etaData;
      showRefreshing(true);
      try {
        const taskSummaries = await loadTaskSummaries();
        const etaPromise = hasEta ? Promise.resolve(etaData) : api('/eta');
        const detailSets = await Promise.all(taskSummaries.map(async (task) => ({
          name: task.name,
          detail: await loadTaskDetails(task.name)
        })));

        const subtasks = [];
        detailSets.forEach(({ name, detail }) => {
          const tasks = Array.isArray(detail?.tasks) ? detail.tasks : [];
          tasks.forEach((task) => subtasks.push(normalizeSubtask(task, name)));
        });

        currentTasks = subtasks;
        renderOpsTable(currentTasks);
        const defaultTask = currentTasks.find((task) => FAILURE_LABELS.has(task.status)) || currentTasks[0] || null;
        renderOpsDetail(defaultTask);

        const histories = await Promise.all(taskSummaries.map((task) => loadTaskHistory(task.name)));
        const resolvedEta = await etaPromise;
        const successRate = computeSuccessRate(aggregateByStatus(histories));
        const running = currentTasks.filter(task => task.status === '运行中').length;
        const failed = currentTasks.filter(task => FAILURE_LABELS.has(task.status)).length;
        const lastSync = latestHistoryTime(histories);

        const summary = {
          running,
          runningDelta: 0,
          failed,
          failedDelta: 0,
          failedNote: failed > 0 ? `${failed} 个子任务失败` : '无失败',
          successRate,
          successDelta: 0,
          lastSync: new Date().toLocaleTimeString(),  // 使用当前时间
          lastSyncId: currentProject ? currentProject.split('/').pop() : '--',
          eta: resolvedEta?.eta
        };
        console.log("renderOpsSummary:", summary);
        renderOpsSummary(summary);
        return summary;
      } finally {
        showRefreshing(false);
      }
    }

    function startAutoRefresh() {
      if (refreshInterval) return;
      refreshInterval = setInterval(async () => {
        // 只在当前可见 tab 刷新
        const hash = location.hash.replace('#', '') || 'launchpad';
        if (hash === 'operations') {
          await refreshOperations();
        } else if (hash === 'insights' && currentProject) {
          await switchProject(currentProject);
        }
        // launchpad 不自动刷新
      }, AUTO_REFRESH_INTERVAL);
    }

    function stopAutoRefresh() {
      if (refreshInterval) {
        clearInterval(refreshInterval);
        refreshInterval = null;
      }
    }

    async function renderLaunchpad() {
      const taskTypes = await loadTaskTypes();
      return renderLaunchpadWithTypes(taskTypes);
    }

    async function renderLaunchpadWithTypes(taskTypes) {
      console.log('[renderLaunchpad] taskTypes:', taskTypes);
      const types = taskTypes?.types || [];
      console.log('[renderLaunchpad] types 数量:', types.length);

      // 隐藏加载提示
      const loadingHint = document.getElementById("launchpad-loading");
      if (loadingHint) loadingHint.remove();

      // 图标映射
      const iconMap = {
        'module-analyzer': 'hub',
        'update-bg': 'sync',
        'check-stale': 'schedule',
        'test-status': 'bug_report',
        'test-analyzer': 'analytics',
        'test-generator': 'science',
        'scan': 'search',
        'generate': 'description'
      };

      const presetContainer = document.getElementById("launchpad-presets");
      // 预设按钮：常用任务
      const presets = [
        { id: 'module-analyzer', name: '完整索引', hint: '--all', primary: true },
        { id: 'check-stale', name: '检测过期', hint: '--stale-only', primary: false },
        { id: 'test-status', name: '测试分析', hint: '--untested', primary: false },
        { id: 'test-generator', name: '生成测试', hint: '--untested', primary: false }
      ];
      presetContainer.innerHTML = presets.map((preset) => {
        const baseClasses = preset.primary
          ? "bg-primary text-background-dark shadow-lg shadow-primary/10"
          : "bg-surface-dark text-white border border-border-dark hover:bg-border-dark";
        return `
          <button class="px-5 py-3 ${baseClasses} rounded-lg font-bold text-sm flex items-center gap-2 transition-transform active:scale-95" data-preset="${preset.id}" data-args="${preset.hint}">
            ${preset.name}
            <span class="text-[10px] text-text-muted font-mono tracking-tight">${preset.hint}</span>
          </button>
        `;
      }).join("");

      const cardContainer = document.getElementById("launchpad-cards");
      cardContainer.innerHTML = types.map((tool, i) => {
        const icon = iconMap[tool.name] || 'terminal';
        const argsHint = Object.keys(tool.args || {}).slice(0, 2).join(' ');
        return `
          <div class="group relative p-6 bg-surface-dark/40 border border-border-dark card-glow rounded-xl transition-all cursor-pointer" data-tool-id="${tool.name}">
            <div class="flex items-start justify-between mb-4">
              <div class="size-12 rounded-lg bg-border-dark flex items-center justify-center text-primary border border-border-dark group-hover:scale-110 transition-transform">
                <span class="material-symbols-outlined text-2xl">${icon}</span>
              </div>
              <span class="text-[10px] font-mono bg-background-dark text-text-muted px-2 py-1 rounded">${tool.script}</span>
            </div>
            <h4 class="text-lg font-bold mb-2">${tool.name}</h4>
            <p class="text-sm text-text-muted leading-relaxed">${tool.description}</p>
            ${argsHint ? `<p class="text-xs text-text-muted mt-2 font-mono">${argsHint}</p>` : ''}
          </div>
        `;
      }).join("") + `
        <div class="group relative p-6 border-2 border-dashed border-border-dark rounded-xl hover:border-primary/50 transition-all cursor-pointer flex flex-col items-center justify-center text-center">
          <div class="size-12 rounded-full bg-background-dark flex items-center justify-center text-text-muted group-hover:text-primary transition-colors">
            <span class="material-symbols-outlined text-2xl">add</span>
          </div>
          <h4 class="text-sm font-bold mt-4 text-text-muted">自定义脚本</h4>
        </div>
      `;

      const argsContainer = document.getElementById("launchpad-args");
      const concurrencySection = document.getElementById("launchpad-concurrency-section");
      const depthSection = document.getElementById("launchpad-depth-section");
      const cards = Array.from(cardContainer.querySelectorAll('[data-tool-id]'));

      function renderLaunchpadArgs(tool, presetArg) {
        if (!tool) {
          selectedToolArgs = {};
          argsContainer.innerHTML = '<p class="text-xs text-text-muted">请选择任务以查看可选参数</p>';
          concurrencySection.classList.add('hidden');
          depthSection.classList.add('hidden');
          return;
        }

        const args = tool.args || {};
        selectedToolArgs = {};
        if (presetArg) selectedToolArgs[presetArg] = true;

        const supportsConcurrency = Object.prototype.hasOwnProperty.call(args, '--concurrency');
        concurrencySection.classList.toggle('hidden', !supportsConcurrency);
        if (supportsConcurrency) {
          const concurrencyInput = document.getElementById("launchpad-concurrency-input");
          selectedToolArgs['--concurrency'] = concurrencyInput.value;
          document.getElementById("launchpad-concurrency").textContent = String(concurrencyInput.value).padStart(2, "0");
        }

        const supportsLayer = Object.prototype.hasOwnProperty.call(args, '--layer');
        depthSection.classList.toggle('hidden', !supportsLayer);
        if (supportsLayer) {
          const activeDepth = depthSection.querySelector('[data-depth].bg-primary') || depthSection.querySelector('[data-depth="normal"]');
          selectedToolArgs['--layer'] = activeDepth?.dataset.layer || '2';
          const depthLabel = document.getElementById("launchpad-depth");
          if (depthLabel && activeDepth) depthLabel.textContent = activeDepth.textContent.trim();
        }

        const flagArgs = Object.entries(args).filter(([arg]) => !['--concurrency', '--layer'].includes(arg));
        if (flagArgs.length === 0) {
          argsContainer.innerHTML = '<p class="text-xs text-text-muted">该工具无可选参数</p>';
          return;
        }

        argsContainer.innerHTML = flagArgs.map(([arg, desc]) => {
          const isOn = selectedToolArgs[arg];
          return `
            <div class="flex items-center justify-between" data-arg-row="${arg}">
              <div>
                <p class="text-sm font-bold">${arg}</p>
                <p class="text-xs text-text-muted">${desc}</p>
              </div>
              <div class="toggle ${isOn ? 'is-on' : ''}" data-arg="${arg}"><span></span></div>
            </div>
          `;
        }).join("");

        argsContainer.querySelectorAll('[data-arg]').forEach((toggle) => {
          toggle.addEventListener('click', () => {
            const arg = toggle.dataset.arg;
            const isOn = toggle.classList.toggle('is-on');
            if (isOn) {
              selectedToolArgs[arg] = true;
            } else {
              delete selectedToolArgs[arg];
            }
          });
        });
      }

      function selectTool(tool, options = {}) {
        if (!tool) return;
        selectedTool = tool;

        cards.forEach(card => {
          card.classList.remove('border-primary', 'border-2', 'shadow-2xl', 'shadow-primary/5');
          card.classList.add('border-border-dark');
        });
        const activeCard = cards.find(card => card.dataset.toolId === tool.name);
        if (activeCard) {
          activeCard.classList.remove('border-border-dark');
          activeCard.classList.add('border-primary', 'border-2', 'shadow-2xl', 'shadow-primary/5');
        }

        const configTitle = document.getElementById('launchpad-config-title');
        if (configTitle) configTitle.textContent = tool.name;

        presetContainer.querySelectorAll('[data-preset]').forEach(b => {
          b.classList.remove('ring-2', 'ring-primary');
        });
        if (options.presetButton) {
          options.presetButton.classList.add('ring-2', 'ring-primary');
        }

        renderLaunchpadArgs(tool, options.presetArg);
      }

      cards.forEach(card => {
        card.addEventListener('click', () => {
          const toolId = card.dataset.toolId;
          const tool = types.find(t => t.name === toolId);
          selectTool(tool);
        });
      });

      presetContainer.querySelectorAll('[data-preset]').forEach(btn => {
        btn.addEventListener('click', () => {
          const preset = btn.dataset.preset;
          const tool = types.find(t => t.name === preset);
          selectTool(tool || { name: preset, args: {} }, { presetArg: btn.dataset.args, presetButton: btn });
        });
      });

      if (types.length > 0) {
        selectTool(types[0]);
      } else {
        renderLaunchpadArgs(null);
      }
    }

    function renderOpsSummary(summary) {
      document.getElementById("ops-running-count").textContent = summary.running;
      document.getElementById("ops-running-delta").textContent = summary.runningDelta;
      document.getElementById("ops-failed-count").textContent = summary.failed;
      document.getElementById("ops-failed-delta").textContent = summary.failedDelta;
      document.getElementById("ops-failed-note").textContent = summary.failedNote;
      document.getElementById("ops-success-rate").textContent = `${summary.successRate}%`;
      document.getElementById("ops-success-delta").textContent = `${summary.successDelta}%`;
      document.getElementById("ops-last-sync").textContent = summary.lastSync;
      document.getElementById("ops-last-sync-id").textContent = `编号: ${summary.lastSyncId}`;
      document.getElementById("footer-sync").textContent = `最后同步: ${summary.lastSync}`;

      const etaEl = document.getElementById("ops-eta");
      const etaNoteEl = document.getElementById("ops-eta-note");
      if (etaEl && etaNoteEl) {
        const eta = summary.eta || {};
        const remainingTasks = Number(eta.pending || 0) + Number(eta.running || 0);
        if (eta.estimatedRemaining && eta.estimatedRemaining > 0) {
          etaEl.textContent = `预计剩余: ${formatEtaDuration(eta.estimatedRemaining)}`;
          etaNoteEl.textContent = eta.estimatedCompletion
            ? `预计完成: ${formatClockTime(eta.estimatedCompletion)}`
            : '基于历史耗时';
        } else if (remainingTasks === 0) {
          etaEl.textContent = '预计剩余: 0s';
          etaNoteEl.textContent = '暂无待处理任务';
        } else {
          etaEl.textContent = '预计剩余: --';
          etaNoteEl.textContent = '基于历史耗时';
        }
      }
    }

    function statusClass(status) {
      if (status === "运行中") return "status-running";
      if (FAILURE_LABELS.has(status)) return "status-failed";
      if (status === "成功") return "status-success";
      return "status-queued";
    }

    // 筛选任务
    function filterTasks(tasks) {
      return tasks.filter(task => {
        // 状态筛选
        if (filterStatus !== 'all') {
          const statusMap = {
            'running': '运行中',
            'failed': task => FAILURE_LABELS.has(task.status),
            'completed': '成功'
          };
          const matcher = statusMap[filterStatus];
          if (typeof matcher === 'function') {
            if (!matcher(task)) return false;
          } else if (task.status !== matcher) {
            return false;
          }
        }
        // 类型筛选
        if (filterType !== 'all' && task.taskName !== filterType) {
          return false;
        }
        return true;
      });
    }

    // 按任务类型分组
    function groupTasks(tasks) {
      const groups = new Map();
      for (const task of tasks) {
        const key = task.taskName || 'unknown';
        if (!groups.has(key)) {
          groups.set(key, []);
        }
        groups.get(key).push(task);
      }
      return groups;
    }

    // 渲染分组表格
    function renderGroupedTable(tasks) {
      const tbody = document.getElementById("ops-table-body");
      const filtered = filterTasks(tasks);

      if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td class="px-6 py-8 text-center text-xs text-text-muted" colspan="5">无匹配任务</td></tr>`;
        return;
      }

      const groups = groupTasks(filtered);
      let html = '';

      for (const [taskName, groupTasks] of groups) {
        const runningCount = groupTasks.filter(t => t.status === '运行中').length;
        const failedCount = groupTasks.filter(t => FAILURE_LABELS.has(t.status)).length;
        const successCount = groupTasks.filter(t => t.status === '成功').length;

        // 分组标题行
        html += `
          <tr class="bg-surface-dark/80 cursor-pointer hover:bg-surface-dark" data-group="${taskName}" onclick="toggleGroup('${taskName}')">
            <td class="px-6 py-3" colspan="5">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <span class="material-symbols-outlined text-sm text-text-muted group-arrow" data-group-arrow="${taskName}">chevron_right</span>
                  <span class="font-bold">${taskName}</span>
                  <span class="text-xs text-text-muted">${groupTasks.length} 个任务</span>
                </div>
                <div class="flex items-center gap-4 text-xs">
                  ${runningCount > 0 ? `<span class="text-primary">${runningCount} 运行中</span>` : ''}
                  ${failedCount > 0 ? `<span class="text-accent-red">${failedCount} 失败</span>` : ''}
                  ${successCount > 0 ? `<span class="text-accent-green">${successCount} 成功</span>` : ''}
                </div>
              </div>
            </td>
          </tr>
        `;

        // 子任务行 (默认折叠)
        for (const task of groupTasks) {
          const activeClass = task.id === activeTaskId ? "bg-primary/5" : "";
          const canRetry = task.canRetry;
          html += `
            <tr class="hover:bg-surface-dark/60 cursor-pointer transition-colors ${activeClass} group-row hidden" data-task-id="${task.id}" data-parent-group="${taskName}">
              <td class="px-6 py-3 pl-12"><span class="status-tag ${statusClass(task.status)}">${task.status.toUpperCase()}</span></td>
              <td class="px-6 py-3">
                <div class="flex flex-col">
                  <span class="text-sm font-bold">${task.name}</span>
                </div>
              </td>
              <td class="px-6 py-3"><code class="text-xs bg-background-dark px-1.5 py-0.5 rounded text-text-muted">${task.target}</code></td>
              <td class="px-6 py-3 text-xs font-mono text-text-muted">${task.duration}</td>
              <td class="px-6 py-3 text-right">
                <div class="flex justify-end gap-2">
                  ${canRetry ? `<button class="p-1.5 bg-accent-red/10 text-accent-red rounded hover:bg-accent-red hover:text-white transition-all" data-action="retry" data-task-id="${task.id}"><span class="material-symbols-outlined text-sm">replay</span></button>` : `<button class="p-1.5 hover:bg-border-dark rounded text-text-muted" data-action="view" data-task-id="${task.id}"><span class="material-symbols-outlined text-sm">visibility</span></button>`}
                </div>
              </td>
            </tr>
          `;
        }
      }

      tbody.innerHTML = html;
    }

    // 切换分组展开/折叠
    window.toggleGroup = function(groupName) {
      const rows = document.querySelectorAll(`[data-parent-group="${groupName}"]`);
      const arrow = document.querySelector(`[data-group-arrow="${groupName}"]`);
      const isExpanded = !rows[0]?.classList.contains('hidden');

      rows.forEach(row => {
        row.classList.toggle('hidden', isExpanded);
      });

      if (arrow) {
        arrow.textContent = isExpanded ? 'chevron_right' : 'expand_more';
      }
    };

    function renderOpsTable(tasks) {
      // 如果开启分组模式，使用分组渲染
      if (groupByTask) {
        renderGroupedTable(tasks);
        return;
      }

      const filtered = filterTasks(tasks);
      const tbody = document.getElementById("ops-table-body");

      if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td class="px-6 py-8 text-center text-xs text-text-muted" colspan="5">无匹配任务</td></tr>`;
        return;
      }

      tbody.innerHTML = filtered.map((task) => {
        const activeClass = task.id === activeTaskId ? "bg-primary/5" : "";
        const canRetry = task.canRetry;
        return `
          <tr class="hover:bg-surface-dark/60 cursor-pointer transition-colors ${activeClass}" data-task-id="${task.id}">
            <td class="px-6 py-4"><span class="status-tag ${statusClass(task.status)}">${task.status.toUpperCase()}</span></td>
            <td class="px-6 py-4">
              <div class="flex flex-col">
                <span class="text-sm font-bold">${task.name}</span>
                <span class="text-[10px] text-text-muted">${task.note}</span>
              </div>
            </td>
            <td class="px-6 py-4"><code class="text-xs bg-background-dark px-1.5 py-0.5 rounded text-text-muted">${task.target}</code></td>
            <td class="px-6 py-4 text-xs font-mono text-text-muted">${task.duration}</td>
            <td class="px-6 py-4 text-right">
              <div class="flex justify-end gap-2">
                ${canRetry ? "<button class=\"p-1.5 bg-accent-red/10 text-accent-red rounded hover:bg-accent-red hover:text-white transition-all\" data-action=\"retry\" data-task-id=\"" + task.id + "\"><span class=\"material-symbols-outlined text-sm\">replay</span></button>" : "<button class=\"p-1.5 hover:bg-border-dark rounded text-text-muted\" data-action=\"view\" data-task-id=\"" + task.id + "\"><span class=\"material-symbols-outlined text-sm\">visibility</span></button>"}
                <button class="p-1.5 hover:bg-border-dark rounded text-text-muted" data-action="delete" data-task-id="${task.id}"><span class="material-symbols-outlined text-sm">delete</span></button>
              </div>
            </td>
          </tr>
        `;
      }).join("");
    }

    function renderOpsDetail(task) {
      const titleEl = document.getElementById("ops-detail-title");
      const pathEl = document.getElementById("ops-detail-path");
      const statusTag = document.getElementById("ops-detail-status");
      const logsContainer = document.getElementById("ops-detail-logs");
      const stackContainer = document.getElementById("ops-detail-stack");
      const paramsContainer = document.getElementById("ops-detail-params");
      const retryButton = document.getElementById("ops-detail-retry");

      if (!task) {
        activeTaskId = null;
        titleEl.textContent = '--';
        pathEl.innerHTML = `<span class="material-symbols-outlined text-xs">folder</span>--`;
        statusTag.textContent = '排队中';
        statusTag.className = 'status-tag status-queued';
        logsContainer.textContent = '暂无任务详情';
        stackContainer.textContent = '无堆栈数据';
        paramsContainer.textContent = '无参数数据';
        if (retryButton) retryButton.disabled = true;
        return;
      }

      activeTaskId = task.id;
      titleEl.textContent = task.name;
      pathEl.innerHTML = `<span class="material-symbols-outlined text-xs">folder</span>${task.taskName} · ${task.target}`;
      statusTag.textContent = task.status.toUpperCase();
      statusTag.className = `status-tag ${statusClass(task.status)}`;

      logsContainer.innerHTML = task.logs.map((log) => {
        const levelColor = log.level === "错误" || log.level === "致命" ? "text-accent-red" : log.level === "调试" ? "text-text-muted" : "text-primary";
        const detailBlock = log.detail ? `<div class=\"mt-2 text-text-muted\">${log.detail.join("<br>")}</div>` : "";
        const highlightClass = log.level === "错误" || log.level === "致命" ? "bg-accent-red/10 border-l-2 border-accent-red p-2" : "";
        return `
          <div class="flex gap-4 mb-1 ${highlightClass}">
            <span class="text-text-muted">[${log.time}]</span>
            <span class="${levelColor}">${log.level.toUpperCase()}:</span>
            <div class="text-white/80">
              <div>${log.message}</div>
              ${detailBlock}
            </div>
          </div>
        `;
      }).join("") + "<div class=\"mt-4 animate-pulse\"><span class=\"text-primary\">_</span></div>";

      stackContainer.textContent = buildTaskStack(task.raw);
      paramsContainer.textContent = buildTaskParams(task.raw, task.taskName);

      if (retryButton) {
        retryButton.dataset.taskId = task.id;
        retryButton.disabled = !task.canRetry;
        retryButton.classList.toggle('opacity-50', retryButton.disabled);
        retryButton.classList.toggle('cursor-not-allowed', retryButton.disabled);
      }

      const metrics = document.getElementById("ops-detail-metrics");
      metrics.innerHTML = `
        <div class="flex gap-4">
          <span class="flex items-center gap-1"><span class="material-symbols-outlined text-[10px]">memory</span> ${task.metrics.memory}</span>
          <span class="flex items-center gap-1"><span class="material-symbols-outlined text-[10px]">speed</span> ${task.metrics.speed}</span>
        </div>
        <span>工作节点: ${task.metrics.node}</span>
      `;

      setOpsDetailTab(activeOpsTab);
      renderOpsTable(currentTasks);
    }

    function renderInsights(insights) {
      document.getElementById("insights-last-sync").textContent = `最后同步: ${insights.lastSync}`;
      document.getElementById("insights-audit-total").textContent = insights.audit.total;

      const trendEl = document.getElementById("insights-audit-trend");
      if (trendEl) {
        trendEl.innerHTML = `<span class="material-symbols-outlined text-sm">trending_up</span>${insights.audit.trend}%`;
      }

      const history = insights.audit.history || { resolved: 0, previous: 0, new: 0, totalResolved: 0 };
      const totalResolved = Number(history.totalResolved || 0);
      const total = insights.audit.total + totalResolved;
      const pct = total > 0 ? Math.round((totalResolved / total) * 100) : 0;

      // 更新已修复数字
      const resolvedEl = document.getElementById("insights-audit-resolved");
      if (resolvedEl) {
        resolvedEl.textContent = totalResolved;
      }

      // 中间的进度条
      const historyEl = document.getElementById("insights-audit-history");
      if (historyEl) {
        historyEl.innerHTML = `
          <div class="flex flex-col gap-2">
            <div class="relative h-3 bg-border-dark rounded-full overflow-hidden">
              <div class="absolute left-0 top-0 h-full bg-accent-green rounded-full transition-all" style="width: ${pct}%;"></div>
            </div>
            <div class="flex justify-between text-[10px] text-text-muted">
              <span>0%</span>
              <span class="text-white font-bold">${pct}%</span>
              <span>100%</span>
            </div>
          </div>
        `;
      }

      // 审计统计信息
      const auditedModules = insights.audit.modulesScanned || 0;
      const files = insights.audit.filesScanned || 0;
      const discovered = insights.audit.discoveredFiles || 0;
      const coverage = insights.audit.coveragePercent || 0;
      document.getElementById("insights-audit-stats").textContent =
        `${auditedModules} 个模块 · ${files}/${discovered} 文件 · ${coverage}% 覆盖`;

      const bars = document.getElementById("insights-audit-bars");
      bars.innerHTML = insights.audit.bars.map((bar) => {
        const heightPct = Math.max(5, Math.round(bar.value * 100)); // 最小 5% 高度
        return `
          <div class="flex flex-col items-center gap-2 h-full">
            <div class="flex-1 w-full flex flex-col justify-end">
              <div class="bg-primary/70 w-full rounded-t-sm" style="height: ${heightPct}%" title="${bar.count || 0}"></div>
            </div>
            <p class="text-text-muted text-[10px] font-bold uppercase tracking-wider">${bar.label}</p>
            <span class="text-white text-sm font-bold">${bar.count || 0}</span>
          </div>
        `;
      }).join("");

      // 目录覆盖率热力图
      const dirCoverageEl = document.getElementById("insights-dir-coverage");
      if (dirCoverageEl && insights.audit.dirCoverage) {
        const dirs = Object.entries(insights.audit.dirCoverage);
        dirCoverageEl.innerHTML = dirs.map(([dir, data]) => {
          const pct = data.coveragePercent || 0;
          // 颜色映射：0-30% 红，30-70% 黄，70-100% 绿
          let colorClass = 'bg-accent-red';
          if (pct >= 70) colorClass = 'bg-accent-green';
          else if (pct >= 30) colorClass = 'bg-accent-yellow';
          const shortDir = dir.replace(/^js\//, '');
          return `
            <div class="flex flex-col items-center gap-1 px-2 py-1 rounded ${colorClass}/20 border border-${colorClass.replace('bg-', '')}/30" title="${dir}: ${data.audited}/${data.discovered} 文件">
              <span class="text-[10px] text-text-muted">${shortDir}</span>
              <span class="text-xs font-bold ${colorClass.replace('bg-', 'text-')}">${pct}%</span>
            </div>
          `;
        }).join("") || '<span class="text-text-muted text-[10px]">无数据</span>';
      }

      document.getElementById("insights-test-rate").textContent = `${insights.tests.value}%`;
      document.getElementById("insights-test-stats").textContent = `${insights.tests.covered}/${insights.tests.total} 模块有测试`;
      document.getElementById("insights-doc-coverage").textContent = `${insights.docs.value}%`;
      document.getElementById("insights-doc-core").textContent = insights.docs.core !== null ? `${insights.docs.core}%` : '--';
      document.getElementById("insights-doc-auth").textContent = `${insights.docs.auth}%`;
      document.getElementById("insights-doc-core-bar").style.width = `${insights.docs.core || 0}%`;
      document.getElementById("insights-doc-auth-bar").style.width = `${insights.docs.auth}%`;
      document.getElementById("insights-stale-claude-fresh").textContent = insights.stale.claude.fresh;
      document.getElementById("insights-stale-claude-stale").textContent = insights.stale.claude.stale;
      document.getElementById("insights-stale-audit-fresh").textContent = insights.stale.audit.fresh;
      document.getElementById("insights-stale-audit-stale").textContent = insights.stale.audit.stale;
      const totalFresh = insights.stale.claude.fresh + insights.stale.audit.fresh;
      const totalStale = insights.stale.claude.stale + insights.stale.audit.stale;
      const staleTotal = totalFresh + totalStale;
      const staleRatio = staleTotal > 0 ? (totalFresh / staleTotal) * 100 : 0;
      document.getElementById("insights-stale-bar").style.width = `${staleRatio}%`;
    }

    function renderIncludeChips() {
      const container = document.getElementById("config-include-chips");
      if (!container || !currentConfig) return;
      container.innerHTML = currentConfig.include.map((path, i) => {
        return `<span class="bg-primary/20 text-primary text-[10px] font-bold px-2 py-1 rounded-md flex items-center gap-1.5">${path}<span class="material-symbols-outlined text-[12px] cursor-pointer hover:text-white" data-remove-include="${i}">close</span></span>`;
      }).join("") || '<span class="text-text-muted text-[10px]">无</span>';
      container.querySelectorAll('[data-remove-include]').forEach(btn => {
        btn.addEventListener('click', () => {
          const idx = parseInt(btn.dataset.removeInclude, 10);
          currentConfig.include.splice(idx, 1);
          renderIncludeChips();
          syncConfigEditor();
        });
      });
    }

    function renderIgnoreChips() {
      const container = document.getElementById("config-ignore-chips");
      if (!container || !currentConfig) return;
      container.innerHTML = currentConfig.ignore.map((path, i) => {
        return `<span class="bg-accent-red/20 text-accent-red text-[10px] font-bold px-2 py-1 rounded-md flex items-center gap-1.5">${path}<span class="material-symbols-outlined text-[12px] cursor-pointer hover:text-white" data-remove-ignore="${i}">close</span></span>`;
      }).join("") || '<span class="text-text-muted text-[10px]">无</span>';
      container.querySelectorAll('[data-remove-ignore]').forEach(btn => {
        btn.addEventListener('click', () => {
          const idx = parseInt(btn.dataset.removeIgnore, 10);
          currentConfig.ignore.splice(idx, 1);
          renderIgnoreChips();
          syncConfigEditor();
        });
      });
    }

    function renderFeatureToggles() {
      const container = document.getElementById("config-features");
      if (!container || !currentConfig) return;
      container.querySelectorAll('[data-feature]').forEach(toggle => {
        const feature = toggle.dataset.feature;
        const isOn = currentConfig.features?.[feature] !== false;
        toggle.classList.toggle('is-on', isOn);
      });
    }

    function renderConfig(config) {
      currentConfig = normalizeConfig(config);
      renderIncludeChips();
      renderIgnoreChips();
      renderFeatureToggles();

      const sensitivityLevel = deriveSensitivityLevel(currentConfig.security?.severity);
      const sensitivityButtons = document.querySelectorAll("#config-sensitivity button");
      sensitivityButtons.forEach((button) => {
        const isActive = button.dataset.sensitivity === sensitivityLevel;
        button.classList.toggle("bg-primary", isActive);
        button.classList.toggle("text-background-dark", isActive);
        button.classList.toggle("text-text-muted", !isActive);
      });

      const autoFixToggle = document.getElementById("config-auto-fix");
      autoFixToggle.classList.toggle("is-on", currentConfig.features?.doc !== false);

      document.getElementById("config-min-coverage").value = currentConfig.testing?.coverage?.minimum ?? 0;
      document.getElementById("config-max-cyclomatic").value = currentConfig.security?.maxCyclomatic ?? 0;

      const editor = document.getElementById("config-editor");
      editor.value = JSON.stringify(currentConfig, null, 2);
      document.getElementById("config-last-saved").textContent = `上次保存: ${configLastSaved}`;
      updateConfigValidation(editor.value);
    }

    function updateConfigValidation(text) {
      const validation = document.getElementById("config-validation");
      if (!validation) return;
      try {
        JSON.parse(text);
        validation.textContent = "JSON 格式正确";
        validation.classList.remove("text-accent-red");
        validation.classList.add("text-accent-green");
      } catch {
        validation.textContent = "JSON 格式错误";
        validation.classList.remove("text-accent-green");
        validation.classList.add("text-accent-red");
      }
    }

    function markConfigDirty() {
      const status = document.getElementById("config-status");
      if (status) status.textContent = "未保存";
    }

    function syncConfigEditor() {
      const editor = document.getElementById("config-editor");
      if (!editor || !currentConfig) return;
      editor.value = JSON.stringify(currentConfig, null, 2);
      updateConfigValidation(editor.value);
      markConfigDirty();
    }

    function setOpsDetailTab(tabKey) {
      activeOpsTab = tabKey;
      document.querySelectorAll('[data-ops-tab]').forEach((button) => {
        const isActive = button.dataset.opsTab === tabKey;
        button.classList.toggle('text-primary', isActive);
        button.classList.toggle('border-b-2', isActive);
        button.classList.toggle('border-primary', isActive);
        button.classList.toggle('text-text-muted', !isActive);
        button.setAttribute('aria-selected', isActive ? 'true' : 'false');
      });
      document.querySelectorAll('[data-ops-panel]').forEach((panel) => {
        const isActive = panel.dataset.opsPanel === tabKey;
        panel.classList.toggle('panel-hidden', !isActive);
      });
    }

    function buildSelectedArgs() {
      const args = [];
      Object.entries(selectedToolArgs).forEach(([arg, value]) => {
        if (value === true) {
          args.push(arg);
        } else if (value !== undefined && value !== null && value !== '') {
          const format = VALUE_ARG_FORMATS[arg];
          if (format === 'equals') {
            args.push(`${arg}=${value}`);
          } else if (format === 'separate') {
            args.push(arg, String(value));
          } else {
            args.push(arg, String(value));
          }
        }
      });
      return args;
    }

    document.addEventListener("DOMContentLoaded", async () => {
      // 1. 并行：检测服务 + 获取缓存（不阻塞）
      const [online, cached] = await Promise.all([
        checkServer(),
        api('/cached-data').catch(() => null)
      ]);

      // 2. 立即渲染缓存（秒开）
      if (cached && cached.project) {
        renderFromCache(cached);
        currentProject = cached.project;
      }

      // 3. 服务不在线则显示警告
      if (!online) {
        showOfflineWarning();
        return;
      }

      // 4. 并行加载：项目列表 + 任务类型
      const [, taskTypes] = await Promise.all([
        initProjects(cached?.project),
        loadTaskTypes()
      ]);

      // 渲染任务启动器（使用预加载的 taskTypes）
      await renderLaunchpadWithTypes(taskTypes);

      if (!currentProject) {
        await refreshOperations();
        renderConfig(await loadConfig());
      }

      // 项目选择器事件
      document.getElementById('project-selector').addEventListener('change', (e) => {
        switchProject(e.target.value);
      });

      document.querySelectorAll("[data-tab-button]").forEach((button) => {
        button.addEventListener("click", (e) => {
          e.preventDefault();
          const tabKey = button.dataset.tabButton;
          console.log("Tab clicked:", tabKey);
          location.hash = tabKey;
          setActiveTab(tabKey);
        });
      });

      document.querySelectorAll("[data-sidebar-button]").forEach((button) => {
        button.addEventListener("click", () => {
          setActiveSidebar(button.dataset.sidebarButton);
        });
      });

      document.getElementById("ops-table-body").addEventListener("click", async (event) => {
        const actionButton = event.target.closest("[data-action]");
        if (actionButton) {
          const action = actionButton.dataset.action;
          const taskId = actionButton.dataset.taskId;
          const task = currentTasks.find((item) => item.id === taskId);
          if (!task) return;
          if (action === "retry") {
            await retryTask(task.taskName, task.taskId);
            await refreshOperations();
            return;
          }
          if (action === "view") {
            renderOpsDetail(task);
            return;
          }
        }
        const row = event.target.closest("[data-task-id]");
        if (row) {
          const task = currentTasks.find((item) => item.id === row.dataset.taskId);
          renderOpsDetail(task);
        }
      });

      const detailRetryButton = document.getElementById("ops-detail-retry");
      if (detailRetryButton) {
        detailRetryButton.addEventListener("click", async () => {
          const task = currentTasks.find((item) => item.id === activeTaskId);
          if (!task || !FAILURE_LABELS.has(task.status)) return;
          await retryTask(task.taskName, task.taskId);
          await refreshOperations();
        });
      }

      document.getElementById("ops-run-all").addEventListener("click", async () => {
        await startTask("all");
      });

      // 筛选下拉菜单
      const filterBtn = document.getElementById("ops-filter-btn");
      const filterMenu = document.getElementById("ops-filter-menu");
      const filterLabel = document.getElementById("ops-filter-label");

      filterBtn?.addEventListener("click", (e) => {
        e.stopPropagation();
        filterMenu.classList.toggle("hidden");
      });

      // 点击外部关闭菜单
      document.addEventListener("click", () => {
        filterMenu?.classList.add("hidden");
      });

      // 状态筛选
      document.querySelectorAll("[data-filter-status]").forEach(btn => {
        btn.addEventListener("click", () => {
          filterStatus = btn.dataset.filterStatus;
          const labels = { all: '全部', running: '运行中', failed: '失败', completed: '成功' };
          filterLabel.textContent = labels[filterStatus] || '全部';
          filterMenu.classList.add("hidden");
          renderOpsTable(currentTasks);
        });
      });

      // 类型筛选
      document.querySelectorAll("[data-filter-type]").forEach(btn => {
        btn.addEventListener("click", () => {
          filterType = btn.dataset.filterType;
          filterMenu.classList.add("hidden");
          renderOpsTable(currentTasks);
        });
      });

      // 分组切换
      document.getElementById("ops-group-toggle")?.addEventListener("click", () => {
        groupByTask = !groupByTask;
        const btn = document.getElementById("ops-group-toggle");
        btn.classList.toggle("bg-primary", groupByTask);
        btn.classList.toggle("text-background-dark", groupByTask);
        renderOpsTable(currentTasks);
      });

      document.getElementById("ops-refresh")?.addEventListener("click", async () => {
        console.log("ops-refresh clicked");
        const btn = document.getElementById("ops-refresh");
        const icon = btn.querySelector("span");
        icon.style.animation = "spin 1s linear infinite";
        try {
          await refreshOperations();
          console.log("refreshOperations done");
        } catch (e) {
          console.error("refreshOperations error:", e);
        }
        icon.style.animation = "";
      });

      document.getElementById("insights-refresh")?.addEventListener("click", async () => {
        console.log("insights-refresh clicked");
        const btn = document.getElementById("insights-refresh");
        btn.querySelector("span").classList.add("animate-spin");
        if (currentProject) await switchProject(currentProject);
        btn.querySelector("span").classList.remove("animate-spin");
      });

      document.getElementById("launchpad-refresh")?.addEventListener("click", async () => {
        console.log("launchpad-refresh clicked");
        const btn = document.getElementById("launchpad-refresh");
        btn.querySelector("span").classList.add("animate-spin");
        await renderLaunchpad();
        btn.querySelector("span").classList.remove("animate-spin");
      });

      document.getElementById("launchpad-start").addEventListener("click", async () => {
        if (!selectedTool) {
          showToast('请先选择一个任务', 'warning');
          return;
        }
        const btn = document.getElementById("launchpad-start");
        btn.disabled = true;
        btn.innerHTML = '<span class="material-symbols-outlined animate-spin">sync</span> 启动中...';
        const args = buildSelectedArgs();
        console.log('[launchpad] 启动任务:', selectedTool.name, args);
        const result = await startTask(selectedTool.name, args);
        console.log('[launchpad] 启动结果:', result);
        btn.disabled = false;
        btn.innerHTML = '<span class="material-symbols-outlined">play_arrow</span> 开始任务';
        if (result && (result.success || result.pid)) {
          showToast(`任务 ${selectedTool.name} 已启动 (PID: ${result.pid})`, 'success');
          location.hash = 'operations';
          setActiveTab('operations');
          await refreshOperations();
        } else {
          showToast('任务启动失败: ' + (result?.message || result?.error || '未知错误'), 'error');
        }
      });

      document.getElementById("launchpad-concurrency-input").addEventListener("input", (event) => {
        const value = event.target.value;
        document.getElementById("launchpad-concurrency").textContent = String(value).padStart(2, "0");
        if (selectedTool?.args && Object.prototype.hasOwnProperty.call(selectedTool.args, '--concurrency')) {
          selectedToolArgs['--concurrency'] = value;
        }
      });

      document.querySelectorAll("[data-depth]").forEach((button) => {
        button.addEventListener("click", () => {
          document.querySelectorAll("[data-depth]").forEach((b) => {
            b.classList.remove("bg-primary", "text-background-dark", "rounded");
            b.classList.add("text-text-muted");
          });
          button.classList.add("bg-primary", "text-background-dark", "rounded");
          button.classList.remove("text-text-muted");
          document.getElementById("launchpad-depth").textContent = button.textContent.trim();
          if (selectedTool?.args && Object.prototype.hasOwnProperty.call(selectedTool.args, '--layer')) {
            selectedToolArgs['--layer'] = button.dataset.layer || DEPTH_LAYER_MAP[button.dataset.depth];
          }
        });
      });

      document.querySelectorAll("[data-ops-tab]").forEach((button) => {
        button.addEventListener("click", () => {
          setOpsDetailTab(button.dataset.opsTab);
        });
      });

      document.querySelectorAll("#config-sensitivity button").forEach((button) => {
        button.addEventListener("click", () => {
          if (!currentConfig) return;
          const level = button.dataset.sensitivity;
          currentConfig.security.severity = [...(SENSITIVITY_PRESETS[level] || SENSITIVITY_PRESETS.permissive)];
          document.querySelectorAll("#config-sensitivity button").forEach((b) => {
            const isActive = b.dataset.sensitivity === level;
            b.classList.toggle("bg-primary", isActive);
            b.classList.toggle("text-background-dark", isActive);
            b.classList.toggle("text-text-muted", !isActive);
          });
          syncConfigEditor();
        });
      });

      const autoFixToggle = document.getElementById("config-auto-fix");
      autoFixToggle.addEventListener("click", () => {
        if (!currentConfig) return;
        const isOn = autoFixToggle.classList.toggle("is-on");
        currentConfig.features.doc = isOn;
        syncConfigEditor();
      });

      const minCoverageInput = document.getElementById("config-min-coverage");
      minCoverageInput.addEventListener("change", (event) => {
        if (!currentConfig) return;
        const value = Number(event.target.value);
        if (!Number.isNaN(value)) {
          currentConfig.testing.coverage.minimum = value;
          syncConfigEditor();
        }
      });

      const maxCyclomaticInput = document.getElementById("config-max-cyclomatic");
      maxCyclomaticInput.addEventListener("change", (event) => {
        if (!currentConfig) return;
        const value = Number(event.target.value);
        if (!Number.isNaN(value)) {
          currentConfig.security.maxCyclomatic = value;
          syncConfigEditor();
        }
      });

      const configEditor = document.getElementById("config-editor");
      configEditor.addEventListener("input", () => {
        updateConfigValidation(configEditor.value);
        markConfigDirty();
      });

      // 包含路径添加
      document.getElementById("config-include-add").addEventListener("click", () => {
        if (!currentConfig) return;
        const input = document.getElementById("config-include-input");
        const path = input.value.trim();
        if (path && !currentConfig.include.includes(path)) {
          currentConfig.include.push(path);
          renderIncludeChips();
          syncConfigEditor();
          input.value = "";
        }
      });
      document.getElementById("config-include-input").addEventListener("keypress", (e) => {
        if (e.key === "Enter") document.getElementById("config-include-add").click();
      });

      // 忽略模式添加
      document.getElementById("config-ignore-add").addEventListener("click", () => {
        if (!currentConfig) return;
        const input = document.getElementById("config-ignore-input");
        const path = input.value.trim();
        if (path && !currentConfig.ignore.includes(path)) {
          currentConfig.ignore.push(path);
          renderIgnoreChips();
          syncConfigEditor();
          input.value = "";
        }
      });
      document.getElementById("config-ignore-input").addEventListener("keypress", (e) => {
        if (e.key === "Enter") document.getElementById("config-ignore-add").click();
      });

      // 功能开关
      document.querySelectorAll("#config-features [data-feature]").forEach(toggle => {
        toggle.addEventListener("click", () => {
          if (!currentConfig) return;
          const feature = toggle.dataset.feature;
          const isOn = toggle.classList.toggle("is-on");
          currentConfig.features[feature] = isOn;
          syncConfigEditor();
        });
      });

      document.getElementById("config-save").addEventListener("click", async () => {
        const editor = document.getElementById("config-editor");
        let parsed = null;
        try {
          parsed = JSON.parse(editor.value);
          document.getElementById("config-status").textContent = "保存中...";
          const result = await saveConfig(parsed);
          if (result.ok) {
            currentConfig = normalizeConfig(parsed);
            configLastSaved = new Date().toLocaleTimeString();
            renderConfig(currentConfig);
            document.getElementById("config-status").textContent = "已保存";
          } else {
            document.getElementById("config-status").textContent = "保存失败";
          }
        } catch (error) {
          document.getElementById("config-status").textContent = "JSON 无效";
          updateConfigValidation(editor.value);
        }
      });

      document.getElementById("config-discard").addEventListener("click", async () => {
        renderConfig(await loadConfig());
        document.getElementById("config-status").textContent = "已还原";
      });

      document.getElementById("header-new-task").addEventListener("click", async () => {
        await startTask("new-task");
        location.hash = 'launchpad';
        setActiveTab("launchpad");
      });

      // Hash 路由支持
      const hash = location.hash.replace('#', '');
      const validTabs = ['launchpad', 'operations', 'insights'];
      setActiveTab(validTabs.includes(hash) ? hash : 'launchpad');

      window.addEventListener('hashchange', () => {
        const h = location.hash.replace('#', '');
        if (validTabs.includes(h)) setActiveTab(h);
      });

      // 页面可见时刷新，隐藏时停止
      document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
          stopAutoRefresh();
        } else {
          startAutoRefresh();
        }
      });

      startAutoRefresh();
    });
