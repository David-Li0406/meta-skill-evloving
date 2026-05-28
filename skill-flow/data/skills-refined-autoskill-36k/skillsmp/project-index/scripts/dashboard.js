#!/usr/bin/env node
/**
 * Project Index Dashboard v2.0 - 项目索引仪表盘
 * 
 * 特性:
 *   - 浅色现代化 UI (Tailwind CSS)
 *   - 多页面导航
 *   - 完整配置编辑器
 *   - 全中文界面
 */

import { createServer } from 'http';
import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { exec } from 'child_process';
import { promisify } from 'util';
import { TaskManager, TASK_TYPES } from './task-manager.js';
import { DEFAULT_CONCURRENCY, loadConfig, readJsonSafe } from './shared.js';

const execAsync = promisify(exec);
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_PORT = 3008;
const stateDir = path.join(__dirname, '..', '.project-index');
const CACHE_FILE = path.join(stateDir, '.dashboard-cache.json');
const apiCache = new Map();
const CACHE_TTL = 30000;

const taskManager = new TaskManager(__dirname);

// 读取缓存
async function readCache() {
  try {
    return JSON.parse(await fs.readFile(CACHE_FILE, 'utf-8'));
  } catch {
    return null;
  }
}

// 写入缓存
async function writeCache(data) {
  await fs.mkdir(stateDir, { recursive: true });
  await fs.writeFile(CACHE_FILE, JSON.stringify(data, null, 2));
}

async function parseBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      try { resolve(body ? JSON.parse(body) : {}); }
      catch (e) { reject(new Error('Invalid JSON')); }
    });
    req.on('error', reject);
  });
}

async function runScript(script, args = [], projectPath = null) {
  const scriptPath = path.join(__dirname, script);
  const cwd = projectPath || process.cwd();
  try {
    const { stdout } = await execAsync(`node "${scriptPath}" ${args.join(' ')} --json`, {
      cwd, timeout: 60000
    });
    return JSON.parse(stdout);
  } catch (err) {
    return { error: err.message };
  }
}

/**
 * Get registered projects from registry
 */
async function getRegisteredProjects() {
  const registryPath = path.join(__dirname, 'projects.json');
  try {
    const content = await fs.readFile(registryPath, 'utf-8');
    const registry = JSON.parse(content);
    return registry.projects || [];
  } catch {
    return [];
  }
}

/**
 * Get project data from a specific project directory
 */
async function getProjectData(projectPath) {
  const stateDir = path.join(projectPath, '.project-index');
  const progressFile = path.join(stateDir, '.module-analyzer-progress.json');
  const historyFile = path.join(stateDir, '.module-analyzer-history.json');

  try {
    const content = await fs.readFile(progressFile, 'utf-8');
    const data = JSON.parse(content);
    const items = data.items || [];

    // Load history to get last failed modules
    let failedModules = new Map();
    try {
      const historyContent = await fs.readFile(historyFile, 'utf-8');
      const history = JSON.parse(historyContent);
      // Get failures from most recent run
      if (history.length > 0) {
        const lastRun = history[history.length - 1];
        if (lastRun.failedList) {
          lastRun.failedList.forEach(f => {
            failedModules.set(f.id, { status: f.status, reason: f.reason });
          });
        }
      }
    } catch { }

    // Build module list with detailed status
    const modules = items.map(item => {
      const id = item.id || item.modulePath;
      const failed = failedModules.get(id);
      return {
        id,
        path: item.fullPath || item.modulePath,
        enableAudit: item.enableAudit || false,
        enableDoc: item.enableDoc || false,
        status: failed ? failed.status : (item.enableAudit ? 'ready' : 'disabled'),
        error: failed ? failed.reason : null,
        language: item.conventions?.language || null
      };
    });

    // Calculate stats
    const stats = {
      total: modules.length,
      auditEnabled: modules.filter(m => m.enableAudit).length,
      failed: failedModules.size,
      ready: modules.filter(m => m.status === 'ready').length
    };

    return {
      modules,
      stats,
      status: data.status || 'unknown',
      startedAt: data.startedAt
    };
  } catch {
    return { modules: [], stats: { total: 0, auditEnabled: 0, failed: 0, ready: 0 }, status: 'no_data' };
  }
}

async function getTaskStatus(projectPath) {
  const stateDir = path.join(projectPath || __dirname, '.project-index');
  const tasks = [];

  // 遍历所有在 TASK_TYPES 中定义的任务类型
  for (const name of Object.keys(TASK_TYPES)) {
    const resultFile = path.join(stateDir, `.${name}-result.json`);
    const historyFile = path.join(stateDir, `.${name}-history.json`);

    let result = null;
    let history = [];

    try {
      const content = await fs.readFile(resultFile, 'utf-8');
      result = JSON.parse(content);
    } catch { }

    try {
      const historyContent = await fs.readFile(historyFile, 'utf-8');
      history = JSON.parse(historyContent).slice(-5);
    } catch { }

    if (result) {
      tasks.push({
        name,
        status: result.status || 'unknown',
        processed: result.processed,
        lastRun: result.completedAt || result.endTime,
        byStatus: result.byStatus,
        history
      });
    } else if (history.length > 0) {
      const lastRun = history[history.length - 1];
      tasks.push({
        name,
        status: lastRun.status || 'completed',
        processed: lastRun.processed,
        lastRun: lastRun.completedAt || lastRun.archivedAt,
        byStatus: lastRun.byStatus,
        history
      });
    } else {
      tasks.push({ name, status: 'never_run' });
    }
  }

  return tasks;
}

async function getDetailedTaskStatus(name, projectPath) {
  const stateDir = path.join(projectPath || __dirname, '.project-index');
  const tasksFile = path.join(stateDir, `.${name}-tasks.json`);
  try {
    const content = await fs.readFile(tasksFile, 'utf-8');
    return JSON.parse(content);
  } catch {
    return null;
  }
}

async function cachedFetch(key, fetcher) {
  const now = Date.now();
  const cached = apiCache.get(key);

  if (cached?.data && now - cached.time < CACHE_TTL) {
    return cached.data;
  }

  if (cached?.data) {
    if (!cached.promise) {
      const promise = fetcher()
        .catch(err => ({ error: err.message }))
        .then(data => {
          apiCache.set(key, { data, time: Date.now() });
          return data;
        });
      apiCache.set(key, { ...cached, promise });
    }
    return cached.data;
  }

  if (cached?.promise) {
    return cached.promise;
  }

  const promise = fetcher().catch(err => ({ error: err.message }));
  apiCache.set(key, { promise });
  const data = await promise;
  apiCache.set(key, { data, time: Date.now() });
  return data;
}

async function cachedRunScript(script, args = [], projectPath = null, cacheKey = null) {
  const cwd = projectPath || process.cwd();
  const key = cacheKey || `${script}:${args.join(',')}:${cwd}`;
  return cachedFetch(key, () => runScript(script, args, projectPath));
}

async function runStaleStatus(projectPath) {
  const targetPath = projectPath || '.';
  const scriptPath = path.join(__dirname, 'check-stale.js');
  try {
    const { stdout } = await execAsync(`node "${scriptPath}" --type=all --json "${targetPath}"`, {
      timeout: 60000
    });
    return JSON.parse(stdout);
  } catch (err) {
    return { error: err.message };
  }
}

async function getAvgDurationFromHistory(historyFile) {
  const history = await readJsonSafe(historyFile, []);
  const entries = Array.isArray(history) ? history : (history?.history || []);
  for (let i = entries.length - 1; i >= 0; i -= 1) {
    const entry = entries[i];
    if (!entry || !entry.processed) continue;
    if (Number.isFinite(entry.avgDuration)) {
      return Math.round(entry.avgDuration);
    }
    if (Number.isFinite(entry.duration)) {
      return Math.round(entry.duration / entry.processed);
    }
    if (entry.startedAt && entry.completedAt) {
      const startedAt = new Date(entry.startedAt);
      const completedAt = new Date(entry.completedAt);
      const elapsed = completedAt - startedAt;
      if (Number.isFinite(elapsed) && elapsed > 0) {
        return Math.round(elapsed / entry.processed);
      }
    }
  }
  return 0;
}

async function getEta(projectPath) {
  const basePath = projectPath || process.cwd();
  const stateDir = path.join(basePath, '.project-index');
  const tasksFile = path.join(stateDir, '.module-analyzer-tasks.json');
  const historyFile = path.join(stateDir, '.module-analyzer-history.json');

  const tasksData = await readJsonSafe(tasksFile, null);
  const tasks = Array.isArray(tasksData?.tasks) ? tasksData.tasks : [];
  const summary = tasksData?.summary || {};

  const pending = Number.isFinite(summary.pending)
    ? summary.pending
    : tasks.filter(t => t.status === 'pending').length;
  const running = Number.isFinite(summary.running)
    ? summary.running
    : tasks.filter(t => t.status === 'running').length;

  const completedDurations = tasks.filter(t => t.status === 'completed' && Number.isFinite(t.duration));
  const totalDuration = completedDurations.reduce((sum, t) => sum + t.duration, 0);
  let avgDuration = completedDurations.length > 0
    ? Math.round(totalDuration / completedDurations.length)
    : 0;

  if (!avgDuration) {
    avgDuration = await getAvgDurationFromHistory(historyFile);
  }

  const config = await loadConfig(basePath);
  const concurrency = Math.max(1, Number(config.concurrency) || DEFAULT_CONCURRENCY);
  const remainingTasks = pending + running;
  const estimatedRemaining = avgDuration && remainingTasks > 0
    ? Math.round((remainingTasks * avgDuration) / concurrency)
    : 0;

  return {
    pending,
    running,
    avgDuration,
    concurrency,
    estimatedRemaining,
    estimatedCompletion: estimatedRemaining > 0 ? new Date(Date.now() + estimatedRemaining).toISOString() : null
  };
}

function getDashboardHtml() {
  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>项目索引仪表盘</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            primary: '#3b82f6',
            success: '#10b981',
            warning: '#f59e0b',
            danger: '#ef4444',
          }
        }
      }
    }
  </script>
  <style>
    .fade-in { animation: fadeIn 0.3s ease-out; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
    .card-hover { transition: all 0.2s; }
    .card-hover:hover { transform: translateY(-2px); box-shadow: 0 10px 40px -10px rgba(0,0,0,0.1); }
  </style>
</head>
<body class="bg-gray-50 min-h-screen">
  <!-- 导航栏 -->
  <nav class="bg-white border-b border-gray-200 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex items-center gap-4">
          <span class="text-xl font-bold text-gray-900">📊 项目索引仪表盘</span>
          <select id="project-selector" onchange="switchProject(this.value)" 
            class="px-3 py-1.5 text-sm border border-gray-300 rounded-lg bg-white focus:ring-2 focus:ring-blue-500 focus:border-transparent">
            <option value="">选择项目...</option>
          </select>
        </div>
        <div class="flex items-center space-x-1">
          <button onclick="navigate('overview')" class="nav-btn px-4 py-2 rounded-lg text-sm font-medium transition-colors" data-page="overview">
            📈 总览
          </button>
          <button onclick="navigate('tasks')" class="nav-btn px-4 py-2 rounded-lg text-sm font-medium transition-colors" data-page="tasks">
            📋 任务管理
          </button>
          <button onclick="navigate('launch')" class="nav-btn px-4 py-2 rounded-lg text-sm font-medium transition-colors" data-page="launch">
            🚀 启动任务
          </button>
          <button onclick="navigate('config')" class="nav-btn px-4 py-2 rounded-lg text-sm font-medium transition-colors" data-page="config">
            ⚙️ 配置
          </button>
          <button onclick="navigate('insights')" class="nav-btn px-4 py-2 rounded-lg text-sm font-medium transition-colors" data-page="insights">
            🔍 审计洞察
          </button>
        </div>
      </div>
    </div>
  </nav>

  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- 总览页 -->
    <div id="page-overview" class="page fade-in">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div id="card-projects" class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 card-hover">
          <div class="text-sm font-medium text-gray-500 mb-2">项目数量</div>
          <div class="text-3xl font-bold text-gray-900">-</div>
        </div>
        <div id="card-modules" class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 card-hover">
          <div class="text-sm font-medium text-gray-500 mb-2">已索引模块</div>
          <div class="text-3xl font-bold text-primary">-</div>
        </div>
        <div id="card-coverage" class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 card-hover">
          <div class="text-sm font-medium text-gray-500 mb-2">测试结果</div>
          <div class="flex items-baseline gap-2">
            <span id="test-passed" class="text-3xl font-bold text-success">-</span>
            <span id="test-failed" class="text-sm text-red-600">失败: -</span>
          </div>
          <div class="mt-3">
            <div class="relative h-2 bg-gray-200 rounded-full overflow-hidden">
              <div id="test-progress" class="absolute left-0 top-0 h-full rounded-full" style="width: 0%; background-color: #22c55e;"></div>
            </div>
          </div>
        </div>
        <div id="card-issues" class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 card-hover">
          <div class="text-sm font-medium text-gray-500 mb-2">审计问题</div>
          <div class="flex items-baseline gap-2">
            <span id="issues-count" class="text-3xl font-bold text-warning">-</span>
            <span id="issues-resolved" class="text-sm text-green-600">已修复: -</span>
          </div>
          <div class="mt-3">
            <div class="relative h-2 bg-gray-200 rounded-full overflow-hidden">
              <div id="issues-progress" class="absolute left-0 top-0 h-full rounded-full" style="width: 0%; background-color: #22c55e;"></div>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">📁 项目列表</h3>
          <div id="project-list" class="space-y-2">
            <div class="text-gray-400">加载中...</div>
          </div>
        </div>
        <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">⏱️ 后台任务</h3>
          <div id="bg-tasks" class="space-y-3">
            <div class="text-gray-400">加载中...</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 任务管理页 -->
    <div id="page-tasks" class="page hidden fade-in">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- 任务列表 -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-100">
          <div class="p-6 border-b border-gray-100 flex justify-between items-center">
            <h3 class="text-lg font-semibold text-gray-900">任务列表</h3>
            <div class="flex gap-2">
              <button onclick="fetchTaskDetails()" class="px-3 py-1.5 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm font-medium transition-colors">
                🔄 刷新
              </button>
              <button onclick="deleteCompleted()" class="px-3 py-1.5 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm font-medium transition-colors">
                🗑️ 清理
              </button>
            </div>
          </div>
          <div id="task-list" class="p-6 max-h-96 overflow-y-auto">
            <div class="text-gray-400">加载中...</div>
          </div>
        </div>

        <!-- 运行历史 -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-100">
          <div class="p-6 border-b border-gray-100">
            <h3 class="text-lg font-semibold text-gray-900">📜 运行历史</h3>
          </div>
          <div id="history-list" class="p-6 max-h-96 overflow-y-auto">
            <div class="text-gray-400">加载中...</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 启动任务页 -->
    <div id="page-launch" class="page hidden fade-in">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">选择任务类型</h3>
          <div id="task-type-grid" class="grid grid-cols-2 md:grid-cols-3 gap-4">
            <!-- 动态填充 -->
          </div>
        </div>
        <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">参数配置</h3>
          <div id="launch-config" class="space-y-4">
            <p class="text-gray-400 text-sm">请先选择任务类型</p>
          </div>
          <button id="launch-btn" onclick="launchTask()" disabled
            class="mt-6 w-full py-3 bg-primary hover:bg-blue-600 disabled:bg-gray-300 text-white rounded-lg font-medium transition-colors">
            🚀 启动任务
          </button>
        </div>
      </div>
    </div>

    <!-- 配置页 -->
    <div id="page-config" class="page hidden fade-in">
      <div class="bg-white rounded-xl shadow-sm border border-gray-100">
        <div class="p-6 border-b border-gray-100 flex justify-between items-center">
          <div>
            <h3 class="text-lg font-semibold text-gray-900">配置编辑器</h3>
            <p class="text-sm text-gray-500 mt-1">编辑 .stale-config.json 配置文件</p>
          </div>
          <div class="flex gap-2">
            <button onclick="formatConfig()" class="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm font-medium transition-colors">
              📐 格式化
            </button>
            <button onclick="saveConfig()" class="px-4 py-2 bg-primary hover:bg-blue-600 text-white rounded-lg text-sm font-medium transition-colors">
              💾 保存配置
            </button>
          </div>
        </div>
        <div class="p-6">
          <div id="config-editor">
            <textarea id="config-json" 
              class="w-full h-96 font-mono text-sm p-4 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent resize-y"
              placeholder="加载配置中..."></textarea>
            <div id="config-error" class="mt-2 text-sm text-red-600 hidden"></div>
            <div id="config-success" class="mt-2 text-sm text-green-600 hidden"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 审计洞察页 -->
    <div id="page-insights" class="page hidden fade-in">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <div class="text-sm font-medium text-gray-500 mb-2">待处理问题</div>
          <div id="insights-total" class="text-4xl font-bold text-orange-500">-</div>
          <div id="insights-resolved" class="text-sm text-green-600 mt-2">已修复: -</div>
        </div>
        <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <div class="text-sm font-medium text-gray-500 mb-2">问题分布</div>
          <div id="insights-severity" class="flex items-end justify-between h-32 pt-4">
            <!-- 柱状图动态填充 -->
          </div>
        </div>
        <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <div class="text-sm font-medium text-gray-500 mb-2">修复进度</div>
          <div id="insights-progress" class="mt-4">
            <div class="relative h-6 bg-gray-200 rounded-full overflow-hidden">
              <div id="progress-bar" class="absolute left-0 top-0 h-full rounded-full transition-all" style="width: 0%; min-width: 8px; background-color: #22c55e;"></div>
            </div>
            <div id="progress-text" class="text-sm text-gray-600 mt-2 text-center">-</div>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">各级别问题详情</h3>
        <div id="insights-details" class="space-y-3">
          <div class="text-gray-400">加载中...</div>
        </div>
      </div>
    </div>
  </main>

  <script>
    // === 导航 ===
    function navigate(page) {
      document.querySelectorAll('.page').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.nav-btn').forEach(el => {
        el.classList.remove('bg-blue-100', 'text-blue-700');
        el.classList.add('text-gray-600', 'hover:bg-gray-100');
      });
      
      const pageEl = document.getElementById('page-' + page);
      const navBtn = document.querySelector('.nav-btn[data-page="' + page + '"]');
      
      if (pageEl) {
        pageEl.classList.remove('hidden');
        pageEl.classList.add('fade-in');
      }
      if (navBtn) {
        navBtn.classList.add('bg-blue-100', 'text-blue-700');
        navBtn.classList.remove('text-gray-600', 'hover:bg-gray-100');
      }

      // 加载页面数据
      if (page === 'overview') loadOverview();
      if (page === 'tasks') { fetchTaskDetails(); loadHistory(); }
      if (page === 'launch') loadTaskTypes();
      if (page === 'config') loadConfig();
      if (page === 'insights') loadInsights();
    }

    // === API 调用 ===
    async function api(path, method = 'GET', body = null) {
      const opts = { method };
      if (body) {
        opts.headers = { 'Content-Type': 'application/json' };
        opts.body = JSON.stringify(body);
      }
      const res = await fetch('/api' + path, opts);
      return res.json();
    }

    // === 项目管理 ===
    let currentProject = null;
    let projectList = [];

    async function loadProjects() {
      const data = await api('/projects');
      projectList = data.projects || [];
      const selector = document.getElementById('project-selector');
      selector.innerHTML = '<option value="">选择项目...</option>' +
        projectList.map(p => '<option value="' + p.path + '">' + p.name + '</option>').join('');
      
      // 如果只有一个项目，自动选中
      if (projectList.length === 1) {
        selector.value = projectList[0].path;
        switchProject(projectList[0].path);
      } else if (projectList.length === 0) {
        document.getElementById('project-list').innerHTML = 
          '<div class="text-gray-400">暂无注册项目。请先在项目目录运行 module-analyzer。</div>';
      }
    }

    function switchProject(projectPath) {
      currentProject = projectPath;
      if (projectPath) {
        loadOverview();
      }
    }

    // === 总览页 ===
    async function loadOverview() {
      if (!currentProject) {
        document.querySelector('#card-projects .text-3xl').textContent = projectList.length;
        document.querySelector('#card-modules .text-3xl').textContent = '-';
        document.querySelector('#card-coverage .text-3xl').textContent = '-';
        document.getElementById('issues-count').textContent = '-';
        document.getElementById('issues-resolved').textContent = '';
        document.getElementById('issues-progress').style.width = '0%';
        document.getElementById('project-list').innerHTML = 
          projectList.length > 0 ? projectList.map(p => 
            '<div class="px-3 py-2 bg-blue-50 text-blue-700 rounded-lg text-sm font-medium cursor-pointer hover:bg-blue-100" onclick="document.getElementById(\\'project-selector\\').value=\\'' + p.path + '\\';switchProject(\\'' + p.path + '\\')">' + p.name + '</div>'
          ).join('') : '<div class="text-gray-400">暂无项目</div>';
        return;
      }

      const [projectData, test, audit, tasks, testResult] = await Promise.all([
        api('/project-data/' + encodeURIComponent(currentProject)),
        api('/test-status'),
        api('/audit-status'),
        api('/tasks?project=' + encodeURIComponent(currentProject)),
        api('/test-result')
      ]);

      document.querySelector('#card-projects .text-3xl').textContent = projectList.length;
      document.querySelector('#card-modules .text-3xl').textContent = projectData.stats?.total || 0;

      // 测试结果卡片
      const passed = testResult?.passed || 0;
      const failed = testResult?.failed || 0;
      const total = passed + failed;
      const testPct = total > 0 ? Math.round((passed / total) * 100) : 0;
      document.getElementById('test-passed').textContent = passed + '/' + total;
      document.getElementById('test-failed').textContent = '失败: ' + failed;
      document.getElementById('test-progress').style.width = testPct + '%';
      document.getElementById('test-progress').style.backgroundColor = failed > 0 ? '#ef4444' : '#22c55e';

      // 审计问题卡片
      const totalIssues = audit.totalIssues || 0;
      const totalResolved = audit.history?.totalResolved || 0;
      const totalAll = totalIssues + totalResolved;
      const pct = totalAll > 0 ? Math.round((totalResolved / totalAll) * 100) : 0;
      document.getElementById('issues-count').textContent = totalIssues;
      document.getElementById('issues-resolved').textContent = '已修复: ' + totalResolved;
      document.getElementById('issues-progress').style.width = pct + '%';

      // 模块状态列表 - 按状态分组，失败的排在最前面
      const modules = projectData.modules || [];
      const sortedModules = modules.sort((a, b) => {
        const order = { llm_error: 0, timeout: 1, error: 2, ready: 3, disabled: 4 };
        return (order[a.status] ?? 5) - (order[b.status] ?? 5);
      });
      
      const statusMap = {
        llm_error: { text: 'LLM错误', class: 'bg-red-100 text-red-700', icon: '❌' },
        timeout: { text: '超时', class: 'bg-orange-100 text-orange-700', icon: '⏱️' },
        error: { text: '错误', class: 'bg-red-100 text-red-700', icon: '❌' },
        ready: { text: '就绪', class: 'bg-green-100 text-green-700', icon: '✓' },
        disabled: { text: '禁用', class: 'bg-gray-100 text-gray-500', icon: '○' }
      };
      
      const modulesHtml = sortedModules.slice(0, 50).map(m => {
        const st = statusMap[m.status] || { text: m.status, class: 'bg-gray-100', icon: '?' };
        return '<div class="p-3 bg-gray-50 rounded-lg border border-gray-100 mb-2">' +
          '<div class="flex justify-between items-start">' +
            '<div class="flex-1 min-w-0">' +
              '<div class="font-mono text-sm text-gray-900 truncate">' + m.id + '</div>' +
              (m.error ? '<div class="text-xs text-red-600 mt-1">' + m.error + '</div>' : '') +
            '</div>' +
            '<span class="ml-2 px-2 py-0.5 rounded text-xs font-medium whitespace-nowrap ' + st.class + '">' + st.icon + ' ' + st.text + '</span>' +
          '</div>' +
        '</div>';
      }).join('');
      
      const statsHtml = '<div class="mb-4 p-3 bg-blue-50 rounded-lg text-sm">' +
        '<span class="font-medium">统计：</span> ' +
        '共 <strong>' + (projectData.stats?.total || 0) + '</strong> 个模块 · ' +
        '审计启用 <strong>' + (projectData.stats?.auditEnabled || 0) + '</strong> · ' +
        (projectData.stats?.failed > 0 ? '<span class="text-red-600">失败 <strong>' + projectData.stats.failed + '</strong></span>' : '<span class="text-green-600">无失败</span>') +
      '</div>';
      
      document.getElementById('project-list').innerHTML = statsHtml + (modulesHtml || '<div class="text-gray-400">暂无模块</div>');

      // 后台任务
      const tasksHtml = tasks.map(t => {
        const statusClass = t.status === 'running' ? 'bg-blue-100 text-blue-700' : 
                           t.status === 'completed' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600';
        const statusText = { running: '运行中', completed: '已完成', never_run: '未运行', unknown: '未知' }[t.status] || t.status;
        return '<div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">' +
          '<span class="font-medium">' + t.name + '</span>' +
          '<span class="px-2 py-1 rounded text-xs font-medium ' + statusClass + '">' + statusText + '</span>' +
        '</div>';
      }).join('');
      document.getElementById('bg-tasks').innerHTML = tasksHtml;
    }

    // === 任务管理 ===
    const TASK_NAME = 'module-analyzer';

    async function fetchTaskDetails() {
      const data = await api('/task-details/' + TASK_NAME + '?project=' + encodeURIComponent(currentProject || ''));
      const el = document.getElementById('task-list');
      
      if (!data || !data.tasks || data.tasks.length === 0) {
        el.innerHTML = '<div class="text-gray-400 text-center py-8">暂无任务记录</div>';
        return;
      }

      const order = { running: 0, failed: 1, timeout: 2, pending: 3, completed: 4, cancelled: 5 };
      const tasks = data.tasks.sort((a, b) => (order[a.status] ?? 9) - (order[b.status] ?? 9));

      const statusMap = {
        running: { text: '运行中', class: 'bg-blue-100 text-blue-700' },
        completed: { text: '已完成', class: 'bg-green-100 text-green-700' },
        failed: { text: '失败', class: 'bg-red-100 text-red-700' },
        timeout: { text: '超时', class: 'bg-orange-100 text-orange-700' },
        pending: { text: '等待中', class: 'bg-gray-100 text-gray-600' },
        cancelled: { text: '已取消', class: 'bg-gray-100 text-gray-600' }
      };

      const rows = tasks.slice(0, 50).map(t => {
        const st = statusMap[t.status] || { text: t.status, class: 'bg-gray-100' };
        const actions = [];
        if (t.status === 'running') actions.push('<button onclick="cancelTask(\\'' + t.id + '\\')" class="text-red-600 hover:text-red-800">取消</button>');
        if (['failed', 'timeout', 'cancelled'].includes(t.status)) actions.push('<button onclick="retryTask(\\'' + t.id + '\\')" class="text-orange-600 hover:text-orange-800">重试</button>');
        if (t.status !== 'running') actions.push('<button onclick="deleteTask(\\'' + t.id + '\\')" class="text-gray-500 hover:text-gray-700">删除</button>');

        return '<tr class="border-b border-gray-100 hover:bg-gray-50">' +
          '<td class="py-3 px-4"><span class="px-2 py-1 rounded text-xs font-medium ' + st.class + '">' + st.text + '</span></td>' +
          '<td class="py-3 px-4 font-mono text-sm" title="' + t.id + '">' + (t.module || t.id) + '</td>' +
          '<td class="py-3 px-4 text-sm text-gray-500">' + (t.duration ? (t.duration/1000).toFixed(1)+'秒' : '-') + '</td>' +
          '<td class="py-3 px-4 text-sm text-red-600">' + (t.error || '') + '</td>' +
          '<td class="py-3 px-4 text-sm space-x-3">' + actions.join('') + '</td>' +
        '</tr>';
      }).join('');

      el.innerHTML = '<table class="w-full"><thead class="bg-gray-50"><tr>' +
        '<th class="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase">状态</th>' +
        '<th class="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase">模块</th>' +
        '<th class="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase">耗时</th>' +
        '<th class="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase">错误</th>' +
        '<th class="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase">操作</th>' +
        '</tr></thead><tbody>' + rows + '</tbody></table>';
    }

    async function retryTask(id) {
      if (!confirm('确定要重试此任务？')) return;
      alert('请在终端运行:\\nnode batch-llm-runner.js --retry ' + TASK_NAME + ' "' + id + '"');
    }

    async function cancelTask(id) {
      if (!confirm('确定要取消此任务？')) return;
      const res = await api('/tasks/' + TASK_NAME + '/cancel/' + encodeURIComponent(id), 'POST');
      if (res.success) fetchTaskDetails();
    }

    async function deleteTask(id) {
      if (!confirm('确定要删除此记录？')) return;
      const res = await api('/tasks/' + TASK_NAME + '/' + encodeURIComponent(id), 'DELETE');
      if (res.success) fetchTaskDetails();
    }

    async function retryAllFailed() {
      alert('请在终端运行:\\nnode module-analyzer.js --resume');
    }

    async function deleteCompleted() {
      if (!confirm('确定要清理所有已完成的任务记录？')) return;
      const res = await api('/tasks/' + TASK_NAME + '/completed', 'DELETE');
      if (res.success) {
        alert('已清理 ' + (res.deleted || 0) + ' 条记录');
        fetchTaskDetails();
      }
    }

    async function loadHistory() {
      if (!currentProject) {
        document.getElementById('history-list').innerHTML = '<div class="text-gray-400 text-center">请先选择项目</div>';
        return;
      }
      const data = await api('/history/module-analyzer?project=' + encodeURIComponent(currentProject));
      const el = document.getElementById('history-list');
      
      if (!data.history || data.history.length === 0) {
        el.innerHTML = '<div class="text-gray-400 text-center">暂无历史记录</div>';
        return;
      }

      const html = data.history.map((run, idx) => {
        const date = new Date(run.completedAt || run.archivedAt);
        const dateStr = date.toLocaleDateString('zh-CN') + ' ' + date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
        const statusClass = run.status === 'success' && run.failed === 0 ? 'bg-green-100 text-green-700' : 
                           run.failed > 0 ? 'bg-orange-100 text-orange-700' : 'bg-gray-100 text-gray-600';
        const statusText = run.status === 'success' && run.failed === 0 ? '✓ 成功' : 
                          run.failed > 0 ? '⚠ 部分失败' : run.status;
        
        // 统计各状态
        const byStatusHtml = run.byStatus ? Object.entries(run.byStatus).map(([k, v]) => {
          const label = { processed: '成功', llm_error: 'LLM错误', timeout: '超时', error: '错误' }[k] || k;
          const color = k === 'processed' ? 'text-green-600' : 'text-red-600';
          return '<span class="' + color + '">' + label + ':' + v + '</span>';
        }).join(' · ') : '';
        
        // 失败列表详情（前5个）
        let failedHtml = '';
        if (run.failedList && run.failedList.length > 0) {
          const showCount = Math.min(5, run.failedList.length);
          const moreCount = run.failedList.length - showCount;
          failedHtml = '<details class="mt-2"><summary class="cursor-pointer text-xs text-red-600 hover:underline">查看失败详情 (' + run.failedList.length + ')</summary>' +
            '<div class="mt-1 text-xs space-y-1 max-h-32 overflow-y-auto">' +
            run.failedList.slice(0, showCount).map(f => 
              '<div class="p-1.5 bg-red-50 rounded">' +
                '<div class="font-mono text-gray-800">' + f.id + '</div>' +
                '<div class="text-gray-500">' + (f.reason || f.status) + '</div>' +
              '</div>'
            ).join('') +
            (moreCount > 0 ? '<div class="text-gray-400">... 还有 ' + moreCount + ' 个</div>' : '') +
            '</div></details>';
        }
        
        return '<div class="p-3 bg-gray-50 rounded-lg mb-3 border border-gray-100">' +
          '<div class="flex justify-between items-center">' +
            '<span class="font-medium text-gray-900">' + dateStr + '</span>' +
            '<span class="px-2 py-0.5 rounded text-xs font-medium ' + statusClass + '">' + statusText + '</span>' +
          '</div>' +
          '<div class="mt-2 text-sm">' +
            '<span class="text-gray-600">处理: <strong>' + (run.processed || 0) + '</strong> 个模块</span>' +
          '</div>' +
          (byStatusHtml ? '<div class="mt-1 text-xs">' + byStatusHtml + '</div>' : '') +
          failedHtml +
        '</div>';
      }).join('');
      
      el.innerHTML = html;
    }

    // === 启动任务 ===
    let selectedTaskType = null;
    let taskDefinitions = [];

    async function loadTaskTypes() {
      const data = await api('/task-types');
      taskDefinitions = data.types || [];
      
      const grid = document.getElementById('task-type-grid');
      grid.innerHTML = taskDefinitions.map(t => 
        '<div onclick="selectTaskType(\\'' + t.name + '\\')" data-name="' + t.name + '"' +
        ' class="task-type-card p-4 border-2 border-gray-200 rounded-xl cursor-pointer hover:border-primary hover:bg-blue-50 transition-all">' +
        '<div class="font-semibold text-gray-900">' + t.name + '</div>' +
        '<div class="text-sm text-gray-500 mt-1">' + t.description + '</div>' +
        '</div>'
      ).join('');
    }

    function selectTaskType(name) {
      selectedTaskType = name;
      document.querySelectorAll('.task-type-card').forEach(el => {
        el.classList.toggle('border-primary', el.dataset.name === name);
        el.classList.toggle('bg-blue-50', el.dataset.name === name);
        el.classList.toggle('border-gray-200', el.dataset.name !== name);
      });
      document.getElementById('launch-btn').disabled = false;

      const def = taskDefinitions.find(t => t.name === name);
      const container = document.getElementById('launch-config');
      
      if (!def || !def.args || Object.keys(def.args).length === 0) {
        container.innerHTML = '<p class="text-gray-400 text-sm">此任务无需配置参数</p>';
        return;
      }

      container.innerHTML = Object.entries(def.args).map(([arg, desc]) => 
        '<label class="flex items-start gap-3 cursor-pointer p-3 hover:bg-gray-50 rounded-lg">' +
        '<input type="checkbox" class="task-arg mt-1 w-4 h-4 text-primary rounded" value="' + arg + '">' +
        '<div><div class="font-medium text-gray-900">' + arg + '</div>' +
        '<div class="text-sm text-gray-500">' + desc + '</div></div>' +
        '</label>'
      ).join('');
    }

    async function launchTask() {
      const args = Array.from(document.querySelectorAll('.task-arg:checked')).map(cb => cb.value);
      const btn = document.getElementById('launch-btn');
      btn.textContent = '启动中...';
      btn.disabled = true;

      try {
        const res = await api('/tasks/start', 'POST', { type: selectedTaskType, args });
        if (res.success) {
          alert('任务已启动！');
          navigate('tasks');
        } else {
          alert('启动失败: ' + res.error);
        }
      } catch (e) {
        alert('错误: ' + e.message);
      } finally {
        btn.textContent = '🚀 启动任务';
        btn.disabled = false;
      }
    }

    // === 配置编辑器 ===
    async function loadConfig() {
      try {
        const data = await api('/config?project=' + encodeURIComponent(currentProject || ''));
        const textarea = document.getElementById('config-json');
        textarea.value = JSON.stringify(data, null, 2);
        hideConfigMessages();
      } catch (e) {
        document.getElementById('config-json').value = '{}';
      }
    }

    function formatConfig() {
      const textarea = document.getElementById('config-json');
      try {
        const data = JSON.parse(textarea.value);
        textarea.value = JSON.stringify(data, null, 2);
        showConfigSuccess('格式化成功');
      } catch (e) {
        showConfigError('JSON 格式错误: ' + e.message);
      }
    }

    async function saveConfig() {
      const textarea = document.getElementById('config-json');
      try {
        const data = JSON.parse(textarea.value);
        const res = await api('/config?project=' + encodeURIComponent(currentProject || ''), 'PUT', data);
        if (res.success) {
          showConfigSuccess('配置已保存');
        } else {
          showConfigError('保存失败: ' + res.error);
        }
      } catch (e) {
        showConfigError('JSON 格式错误: ' + e.message);
      }
    }

    function hideConfigMessages() {
      document.getElementById('config-error').classList.add('hidden');
      document.getElementById('config-success').classList.add('hidden');
    }

    function showConfigError(msg) {
      hideConfigMessages();
      const el = document.getElementById('config-error');
      el.textContent = msg;
      el.classList.remove('hidden');
    }

    function showConfigSuccess(msg) {
      hideConfigMessages();
      const el = document.getElementById('config-success');
      el.textContent = msg;
      el.classList.remove('hidden');
      setTimeout(hideConfigMessages, 3000);
    }

    // === 审计洞察 ===
    async function loadInsights() {
      if (!currentProject) return;
      const audit = await api('/audit-status');

      // 总问题数和已修复数
      document.getElementById('insights-total').textContent = audit.totalIssues || 0;
      const totalResolved = audit.history?.totalResolved || 0;
      document.getElementById('insights-resolved').textContent = '已修复: ' + totalResolved;

      // 修复进度条
      const total = (audit.totalIssues || 0) + totalResolved;
      const pct = total > 0 ? Math.round((totalResolved / total) * 100) : 0;
      document.getElementById('progress-bar').style.width = pct + '%';
      document.getElementById('progress-text').textContent = totalResolved + ' / ' + total + ' (' + pct + '%)';

      // 问题分布柱状图
      const sc = audit.severityCounts || { critical: 0, high: 0, medium: 0, low: 0 };
      const maxCount = Math.max(sc.critical, sc.high, sc.medium, sc.low, 1);
      const bars = [
        { label: 'Critical', count: sc.critical, color: 'bg-red-500' },
        { label: 'High', count: sc.high, color: 'bg-orange-500' },
        { label: 'Medium', count: sc.medium, color: 'bg-yellow-500' },
        { label: 'Low', count: sc.low, color: 'bg-green-500' }
      ];

      const barHtml = bars.map(b => {
        const h = Math.max(8, Math.round((b.count / maxCount) * 80));
        return '<div class=\"flex flex-col items-center flex-1\">' +
          '<div class=\"' + b.color + ' w-full rounded-t\" style=\"height: ' + h + 'px\"></div>' +
          '<div class=\"text-xs font-medium mt-1\">' + b.count + '</div>' +
          '<div class=\"text-xs text-gray-500\">' + b.label + '</div>' +
        '</div>';
      }).join('');
      document.getElementById('insights-severity').innerHTML = barHtml;

      // 详情列表 - 按模块分组
      const modules = audit.modules || [];
      const byLevel = { critical: [], high: [], medium: [], low: [] };
      for (const m of modules) {
        if (m.issueCount > 0 && byLevel[m.severity]) {
          byLevel[m.severity].push(m);
        }
      }

      const levelInfo = {
        critical: { icon: '🔴', name: 'Critical', cls: 'text-red-600' },
        high: { icon: '🟠', name: 'High', cls: 'text-orange-600' },
        medium: { icon: '🟡', name: 'Medium', cls: 'text-yellow-600' },
        low: { icon: '🟢', name: 'Low', cls: 'text-green-600' }
      };

      let detailsHtml = '';
      for (const level of ['critical', 'high', 'medium', 'low']) {
        const items = byLevel[level];
        if (items.length === 0) continue;
        const info = levelInfo[level];
        detailsHtml += '<div class=\"border-l-4 border-' + level + '-500 pl-4 py-2\">' +
          '<div class=\"font-medium ' + info.cls + '\">' + info.icon + ' ' + info.name + ' (' + items.length + ' 模块)</div>' +
          '<div class=\"text-sm text-gray-600 mt-1\">' +
            items.slice(0, 5).map(m => m.path + ' (' + m.issueCount + ')').join(', ') +
            (items.length > 5 ? ' ...' : '') +
          '</div>' +
        '</div>';
      }
      document.getElementById('insights-details').innerHTML = detailsHtml || '<div class=\"text-green-600\">✅ 无待处理问题</div>';
    }

    // === 初始化 ===
    loadProjects().then(() => navigate('overview'));
    setInterval(() => {
      const activePage = document.querySelector('.page:not(.hidden)')?.id?.replace('page-', '');
      if (activePage === 'overview') loadOverview();
      if (activePage === 'tasks') fetchTaskDetails();
    }, 15000);
  </script>
</body>
</html>`;
}

async function handleRequest(req, res) {
  const url = new URL(req.url, `http://${req.headers.host}`);

  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');

  if (req.method === 'OPTIONS') {
    res.statusCode = 204;
    res.end();
    return;
  }

  try {
    if (url.pathname === '/') {
      res.setHeader('Content-Type', 'text/html; charset=utf-8');
      // 优先使用新的 dashboard.html，fallback 到内嵌版本
      const htmlPath = path.join(__dirname, '../pages/dashboard.html');
      try {
        const html = await fs.readFile(htmlPath, 'utf-8');
        res.end(html);
      } catch {
        res.end(getDashboardHtml());
      }
      return;
    }

    // 静态文件服务
    if (url.pathname === '/dashboard.css') {
      res.setHeader('Content-Type', 'text/css; charset=utf-8');
      const cssPath = path.join(__dirname, '../pages/dashboard.css');
      try {
        res.end(await fs.readFile(cssPath, 'utf-8'));
      } catch {
        res.statusCode = 404;
        res.end('/* Not found */');
      }
      return;
    }

    if (url.pathname === '/dashboard.js') {
      res.setHeader('Content-Type', 'application/javascript; charset=utf-8');
      const jsPath = path.join(__dirname, '../pages/dashboard.js');
      try {
        res.end(await fs.readFile(jsPath, 'utf-8'));
      } catch {
        res.statusCode = 404;
        res.end('// Not found');
      }
      return;
    }

    res.setHeader('Content-Type', 'application/json');

    // Get registered projects from registry
    if (url.pathname === '/api/projects') {
      const projects = await getRegisteredProjects();
      res.end(JSON.stringify({ projects }));
      return;
    }

    // Get data for a specific project
    if (url.pathname.startsWith('/api/project-data/')) {
      const projectPath = decodeURIComponent(url.pathname.replace('/api/project-data/', ''));
      const data = await getProjectData(projectPath);
      const cachedAt = new Date().toISOString();
      const cached = await readCache();
      const sameProject = cached && cached.project === projectPath;
      await writeCache({
        cachedAt,
        project: projectPath,
        insights: sameProject ? cached.insights : null,
        operations: sameProject ? cached.operations : null,
        eta: sameProject ? cached.eta : null
      });
      res.end(JSON.stringify({ ...data, cachedAt }));
      return;
    }

    if (req.method === 'GET' && url.pathname === '/api/cached-data') {
      res.end(JSON.stringify(await readCache() || {}));
      return;
    }

    if (req.method === 'POST' && url.pathname === '/api/cached-data') {
      const body = await parseBody(req);
      const cachedAt = body?.cachedAt || new Date().toISOString();
      await writeCache({ ...body, cachedAt });
      res.end(JSON.stringify({ success: true }));
      return;
    }

    if (url.pathname === '/api/test-status') {
      const projectPath = url.searchParams.get('project');
      res.end(JSON.stringify(await cachedRunScript('test-status.js', ['--json'], projectPath)));
      return;
    }

    if (url.pathname === '/api/audit-status') {
      const projectPath = url.searchParams.get('project');
      res.end(JSON.stringify(await cachedRunScript('audit-status.js', [], projectPath)));
      return;
    }

    if (url.pathname === '/api/test-result') {
      const projectPath = url.searchParams.get('project');
      res.end(JSON.stringify(await cachedRunScript('test-result.js', ['--save'], projectPath)));
      return;
    }

    if (url.pathname === '/api/stale-status') {
      const projectPath = url.searchParams.get('project') || '.';
      const key = `stale-status:${projectPath}`;
      res.end(JSON.stringify(await cachedFetch(key, () => runStaleStatus(projectPath))));
      return;
    }

    if (url.pathname === '/api/tasks') {
      const projectPath = url.searchParams.get('project');
      res.end(JSON.stringify(await getTaskStatus(projectPath)));
      return;
    }

    if (url.pathname === '/api/eta') {
      const projectPath = url.searchParams.get('project');
      res.end(JSON.stringify({ eta: await getEta(projectPath) }));
      return;
    }

    if (url.pathname.startsWith('/api/task-details/')) {
      const name = url.pathname.split('/').pop();
      const projectPath = url.searchParams.get('project');
      res.end(JSON.stringify(await getDetailedTaskStatus(name, projectPath) || { error: 'No data' }));
      return;
    }

    // Get task run history
    if (url.pathname.startsWith('/api/history/')) {
      const name = url.pathname.split('/').pop();
      const projectPath = url.searchParams.get('project');
      const stateDir = path.join(projectPath || __dirname, '.project-index');
      const historyFile = path.join(stateDir, `.${name}-history.json`);
      try {
        const content = await fs.readFile(historyFile, 'utf-8');
        const history = JSON.parse(content);
        // Return last 10 runs, most recent first
        res.end(JSON.stringify({ history: history.slice(-10).reverse() }));
      } catch {
        res.end(JSON.stringify({ history: [] }));
      }
      return;
    }

    if (url.pathname === '/api/task-types') {
      res.end(JSON.stringify({ types: taskManager.getTaskTypes() }));
      return;
    }

    if (req.method === 'POST' && url.pathname === '/api/cache/clear') {
      apiCache.clear();
      res.end(JSON.stringify({ success: true, message: 'Cache cleared' }));
      return;
    }

    if (req.method === 'POST' && url.pathname === '/api/tasks/start') {
      const body = await parseBody(req);
      const projectPath = url.searchParams.get('project') || body.project || process.cwd();
      res.end(JSON.stringify(await taskManager.launchTask(body.type, body.args || [], projectPath)));
      return;
    }

    if (req.method === 'POST' && url.pathname.match(/^\/api\/tasks\/[^/]+\/cancel\/[^/]+$/)) {
      const [, , , name, , id] = url.pathname.split('/');
      res.end(JSON.stringify(await taskManager.cancelTask(name, decodeURIComponent(id))));
      return;
    }

    if (req.method === 'DELETE' && url.pathname.match(/^\/api\/tasks\/[^/]+\/[^/]+$/)) {
      const [, , , name, id] = url.pathname.split('/');
      res.end(JSON.stringify(await taskManager.deleteTask(name, decodeURIComponent(id))));
      return;
    }

    if (req.method === 'DELETE' && url.pathname.match(/^\/api\/tasks\/[^/]+\/completed$/)) {
      const name = url.pathname.split('/')[3];
      res.end(JSON.stringify(await taskManager.deleteCompletedTasks(name)));
      return;
    }

    // Retry failed tasks for a task type
    if (req.method === 'POST' && url.pathname.match(/^\/api\/tasks\/[^/]+\/retry\/[^/]+$/)) {
      const [, , , name, , id] = url.pathname.split('/');
      const projectPath = url.searchParams.get('project') || process.cwd();
      // Use --retry-failed to only retry failed tasks without clearing state
      const result = await taskManager.launchTask(name, ['--retry-failed'], projectPath);
      res.end(JSON.stringify(result));
      return;
    }

    if (req.method === 'GET' && url.pathname === '/api/config') {
      const projectPath = url.searchParams.get('project') || process.cwd();
      const configPath = path.join(projectPath, '.project-index', '.stale-config.json');
      try {
        res.end(await fs.readFile(configPath, 'utf-8'));
      } catch {
        res.end('{}');
      }
      return;
    }

    if (req.method === 'PUT' && url.pathname === '/api/config') {
      const body = await parseBody(req);
      const projectPath = url.searchParams.get('project') || process.cwd();
      const configPath = path.join(projectPath, '.project-index', '.stale-config.json');
      await fs.writeFile(configPath, JSON.stringify(body, null, 2));
      res.end(JSON.stringify({ success: true }));
      return;
    }

    res.statusCode = 404;
    res.end(JSON.stringify({ error: 'Not found' }));
  } catch (err) {
    res.statusCode = 500;
    res.end(JSON.stringify({ error: err.message }));
  }
}

async function main() {
  const args = process.argv.slice(2);
  const portArg = args.find(a => a.startsWith('--port='));
  let port = portArg ? parseInt(portArg.split('=')[1]) : DEFAULT_PORT;
  const shouldOpen = args.includes('--open');

  const server = createServer(handleRequest);

  server.on('error', (e) => {
    if (e.code === 'EADDRINUSE') {
      console.log(`端口 ${port} 被占用，尝试 ${port + 1}...`);
      server.close();
      server.listen(++port);
    } else {
      console.error(e);
      process.exit(1);
    }
  });

  server.on('listening', () => {
    console.log(`\n📊 项目索引仪表盘 v2.0\n   http://localhost:${port}\n`);
    if (shouldOpen) {
      const openCmd = process.platform === 'darwin' ? 'open' :
        process.platform === 'win32' ? 'start' : 'xdg-open';
      exec(`${openCmd} http://localhost:${port}`);
    }
    setTimeout(() => {
      cachedRunScript('audit-status.js', [], process.cwd());
      cachedRunScript('test-status.js', ['--json'], process.cwd());
    }, 1000);
  });

  server.listen(port);
}

main().catch(console.error);
