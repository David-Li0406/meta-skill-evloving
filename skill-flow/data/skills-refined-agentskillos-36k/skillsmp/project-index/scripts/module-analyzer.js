#!/usr/bin/env node
/**
 * Module Analyzer - Combined doc update + audit in one pass
 *
 * One scan, one LLM call per module, multiple outputs:
 * - CLAUDE.md (module description)
 * - AUDIT.md (security/quality audit)
 * - Kanban tasks (for issues found)
 *
 * Usage:
 *   node module-analyzer.js [options] [path]
 *
 * Modes (mutually exclusive):
 *   --stale        Process stale modules only (default)
 *   --missing      Only missing docs/audits
 *   --all          Stale + missing
 *   --force        Force refresh all large modules
 *   --reindex      Alias for --force
 *
 * Feature toggles:
 *   --no-doc       Skip CLAUDE.md update
 *   --no-audit     Skip AUDIT.md update
 *   --no-kanban    Skip Kanban task creation
 *
 * Execution:
 *   --dry-run      Preview only (no LLM calls)
 *   --concurrency=N  Override concurrency (default 6)
 *   --resume       Resume crashed task
 *   --daemon       Run in background
 *   --status       Show last result
 *   --help         Show help
 */

import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { BatchRunner } from './batch-llm-runner.js';
import { execSync } from 'child_process';
import { findDirsNeedingIndex, findLargeDirs } from './generate.js';
import { fileExists, loadConfig, parseArgs, readFileSafe, shouldProcess } from './shared.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const KANBAN_API = process.env.KANBAN_URL || 'http://127.0.0.1:3007/api/v1';
const CODE_EXTENSIONS = new Set([
  '.js', '.ts', '.jsx', '.tsx', '.mjs', '.cjs',
  '.py', '.go', '.rs', '.java', '.kt', '.rb', '.php',
  '.c', '.cpp', '.h', '.hpp', '.cs', '.swift', '.vue', '.svelte'
]);

/**
 * Detect current project from Kanban
 * @returns {Promise<{id: string, name: string, path: string}|null>}
 */
async function detectProject() {
  const cwd = process.cwd();
  try {
    const res = await fetch(`${KANBAN_API}/projects`);
    if (!res.ok) return null;
    const data = await res.json();

    for (const project of data.items || []) {
      if (project.path === cwd || cwd.startsWith(project.path + '/')) {
        return project;
      }
    }
  } catch { }
  return null;
}

/**
 * Create Kanban task (single issue)
 * @param {string} projectId
 * @param {object} task - {title, description, priority, tags}
 * @returns {Promise<string|null>} task ID
 */
async function createKanbanTask(projectId, task) {
  try {
    const res = await fetch(`${KANBAN_API}/projects/${projectId}/tasks/create`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: task.title,
        description: task.description || '',
        status: 'todo',
        priority: task.priority ?? 2,
        tags: task.tags || [],
        dueDate: null,
        worktreeId: null
      })
    });

    if (res.ok) {
      const data = await res.json();
      return data.item?.id || null;
    }
  } catch { }
  return null;
}

/**
 * Create Kanban tasks for audit issues
 * Groups all issues from a module into individual tasks with [AUDIT] prefix
 *
 * @param {string} projectId
 * @param {string} modulePath
 * @param {object} audit - { severity, issues, summary }
 * @returns {Promise<{taskIds: string[]}>}
 */
async function createAuditTasks(projectId, modulePath, audit) {
  const { severity, issues, summary } = audit;
  if (!issues || issues.length === 0) return { taskIds: [] };

  const priorityMap = { critical: 0, high: 1, medium: 2, low: 3 };
  const basePriority = priorityMap[severity] ?? 2;
  const taskIds = [];

  for (const issue of issues) {
    const task = {
      title: `[AUDIT/${severity?.toUpperCase()}] ${modulePath}: ${issue.type}`,
      description: `## 问题描述
${issue.description}

## 位置
- **模块**: ${modulePath}
- **文件**: ${issue.file || 'N/A'}
- **行号**: ${issue.line || 'N/A'}

## 代码上下文
\`\`\`
${issue.context || 'N/A'}
\`\`\`

## 修复建议
${issue.suggestion || '待分析'}

## 审计摘要
${summary || 'N/A'}

---
*由 module-analyzer 自动创建*`,
      priority: priorityMap[issue.severity] ?? basePriority,
      tags: ['audit', severity, issue.type].filter(Boolean)
    };

    const taskId = await createKanbanTask(projectId, task);
    if (taskId) taskIds.push(taskId);
  }

  return { taskIds };
}

/**
 * Get stale modules from check-stale.js
 * @param {string} cwd - Working directory
 * @returns {Promise<Array>}
 */
async function getStaleModules(cwd) {
  try {
    const checkScript = path.join(__dirname, 'check-stale.js');
    const result = execSync(`node "${checkScript}" --json`, {
      encoding: 'utf-8',
      cwd,
      timeout: 60000
    });
    return JSON.parse(result).filter(r => r.status === 'stale');
  } catch {
    return [];
  }
}

/**
 * Get ALL modules (for full reindex)
 * @param {string} cwd - Working directory
 * @returns {Promise<Array>}
 */
async function getAllModules(cwd) {
  try {
    const checkScript = path.join(__dirname, 'check-stale.js');
    const result = execSync(`node "${checkScript}" --json`, {
      encoding: 'utf-8',
      cwd,
      timeout: 60000
    });
    return JSON.parse(result);
  } catch {
    return [];
  }
}

function normalizeModulePath(modulePath) {
  if (!modulePath || modulePath === '.') return '.';
  return modulePath.replace(/\\/g, '/').replace(/\/+$/, '');
}

function normalizePathInput(input) {
  if (!input) return null;
  const normalized = path.normalize(input).replace(/\\/g, '/');
  const trimmed = normalized.replace(/^\.\/+/, '').replace(/\/+$/, '');
  return trimmed || '.';
}

async function resolvePathFilter(input, cwd) {
  if (!input) return null;
  const absolutePath = path.isAbsolute(input) ? input : path.resolve(cwd, input);
  const relativePath = path.relative(cwd, absolutePath);

  if (relativePath.startsWith('..') || path.isAbsolute(relativePath)) {
    throw new Error(`Path is outside project root: ${input}`);
  }

  try {
    const stat = await fs.stat(absolutePath);
    if (!stat.isDirectory()) {
      throw new Error(`Path is not a directory: ${input}`);
    }
  } catch {
    throw new Error(`Path not found: ${input}`);
  }

  return normalizePathInput(relativePath);
}

function matchesPathFilter(modulePath, filterPath) {
  if (!filterPath) return true;
  const moduleNormalized = normalizePathInput(modulePath) || '.';
  const filterNormalized = normalizePathInput(filterPath) || '.';
  if (filterNormalized === '.' || filterNormalized === '') return true;
  return moduleNormalized === filterNormalized ||
    moduleNormalized.startsWith(`${filterNormalized}/`);
}

function mergeModules(...lists) {
  const merged = new Map();

  for (const list of lists) {
    for (const item of list) {
      const key = normalizeModulePath(item.path);
      const existing = merged.get(key);
      if (!existing) {
        merged.set(key, { ...item, path: key });
        continue;
      }

      const existingChanged = existing.changedFiles || [];
      const incomingChanged = item.changedFiles || [];
      merged.set(key, {
        ...existing,
        ...item,
        path: key,
        changedFiles: existingChanged.length > 0 ? existingChanged : incomingChanged
      });
    }
  }

  return Array.from(merged.values());
}

function getDepth(p) {
  return p.split(/[\\/]+/).filter(Boolean).length;
}

function sortModules(modules) {
  return modules.sort((a, b) => {
    const depthA = getDepth(a.path);
    const depthB = getDepth(b.path);
    if (depthA !== depthB) return depthB - depthA;
    return a.path.localeCompare(b.path);
  });
}

function filterModules(modules, config, pathFilter) {
  return modules.filter(m =>
    shouldProcess(m.path, config) && matchesPathFilter(m.path, pathFilter)
  );
}

async function findMissingDocs(cwd, scanPath) {
  try {
    const { needsCreate } = await findDirsNeedingIndex(cwd, scanPath);
    return needsCreate.map(dir => ({
      path: normalizeModulePath(dir.path),
      changedFiles: [],
      status: 'missing_doc'
    }));
  } catch {
    return [];
  }
}

async function findMissingAudits(cwd) {
  const modules = await getAllModules(cwd);
  const checks = await Promise.all(modules.map(async (mod) => ({
    mod,
    missing: !(await fileExists(path.join(cwd, mod.path, 'AUDIT.md')))
  })));

  return checks
    .filter(c => c.missing)
    .map(c => ({
      ...c.mod,
      path: normalizeModulePath(c.mod.path),
      status: 'missing_audit'
    }));
}

async function getModulesByMode({ mode, cwd, scanPath, enableDoc, enableAudit }) {
  if (mode === 'stale') {
    return await getStaleModules(cwd);
  }

  if (mode === 'missing') {
    const missingDocs = enableDoc ? await findMissingDocs(cwd, scanPath) : [];
    const missingAudits = enableAudit ? await findMissingAudits(cwd) : [];
    return mergeModules(missingDocs, missingAudits);
  }

  if (mode === 'all') {
    const stale = await getStaleModules(cwd);
    const missingDocs = enableDoc ? await findMissingDocs(cwd, scanPath) : [];
    const missingAudits = enableAudit ? await findMissingAudits(cwd) : [];
    return mergeModules(stale, missingDocs, missingAudits);
  }

  if (mode === 'force') {
    const largeDirs = await findLargeDirs(cwd, scanPath);
    return largeDirs.map(dir => ({
      path: normalizeModulePath(dir.path),
      changedFiles: [],
      status: 'force'
    }));
  }

  return [];
}

function normalizeArgs(rawArgs) {
  const normalized = [];

  for (let i = 0; i < rawArgs.length; i++) {
    const arg = rawArgs[i];
    if (arg === '--concurrency' && rawArgs[i + 1] && !rawArgs[i + 1].startsWith('-')) {
      normalized.push(`--concurrency=${rawArgs[i + 1]}`);
      i += 1;
      continue;
    }
    normalized.push(arg);
  }

  return normalized;
}

function printHelp() {
  console.log(`Usage:
  node scripts/module-analyzer.js [options] [path]

Modes (mutually exclusive):
  --stale          Only stale modules (default)
  --missing        Only missing docs/audits
  --all            Stale + missing
  --force          Force refresh all large modules
  --reindex        Alias for --force

Feature toggles:
  --no-doc         Skip CLAUDE.md update
  --no-audit       Skip AUDIT.md update
  --no-kanban      Skip Kanban task creation

Execution:
  --dry-run        Preview only (no LLM calls)
  --concurrency=N  Override concurrency (default 6)
  --resume         Resume interrupted task
  --retry-failed   Retry failed tasks only
  --daemon         Run in background
  --status         Show last result
  --help           Show help

Path:
  [path]           Optional subdirectory (e.g. js/agents)
`);
}

async function listCodeFiles(dir, maxFiles) {
  let entries = [];

  try {
    entries = await fs.readdir(dir, { withFileTypes: true });
  } catch {
    return [];
  }

  return entries
    .filter(entry => entry.isFile())
    .map(entry => entry.name)
    .filter(name => CODE_EXTENSIONS.has(path.extname(name).toLowerCase()))
    .filter(name => !name.includes('.test.') && !name.includes('.spec.'))
    .slice(0, maxFiles);
}

/**
 * Read code files from directory
 * @param {string} dir - Module directory
 * @param {Array} files - Files to read
 * @param {number} [maxFiles=5] - Maximum files to read
 * @param {number} [maxLines=60] - Maximum lines per file
 * @returns {Promise<string>}
 */
async function readCodeFiles(dir, files, maxFiles = 5, maxLines = 60) {
  let content = '';
  let toRead = files?.slice(0, maxFiles) || [];

  if (toRead.length === 0) {
    toRead = await listCodeFiles(dir, maxFiles);
  }

  for (const f of toRead) {
    const filePath = typeof f === 'string' ? path.join(dir, f) : path.join(dir, '..', f.path);
    const fileContent = await readFileSafe(filePath, maxLines);
    if (fileContent) {
      const relPath = typeof f === 'string' ? f : f.path;
      content += `\n--- ${relPath} ---\n${fileContent}\n`;
    }
  }

  return content;
}

async function main() {
  const rawArgs = process.argv.slice(2);
  const cwd = process.cwd();

  if (rawArgs.includes('--help') || rawArgs.includes('-h')) {
    printHelp();
    return;
  }

  const normalizedArgs = normalizeArgs(rawArgs);
  const args = parseArgs(normalizedArgs, {
    dryRun: false,
    resume: false,
    retryFailed: false,
    status: false,
    daemon: false,
    stale: false,
    missing: false,
    all: false,
    force: false,
    reindex: false,
    noDoc: false,
    noAudit: false,
    noKanban: false
  });

  if (args.status) {
    const resultPath = path.join(cwd, '.project-index', '.module-analyzer-result.json');
    try {
      const result = await fs.readFile(resultPath, 'utf-8');
      console.log(result);
    } catch {
      console.log('No result found.');
    }
    return;
  }

  // Daemon mode: fork background process and exit immediately
  if (args.daemon) {
    if (args.dryRun) {
      console.log('Cannot use --daemon with --dry-run.');
      return;
    }

    const { spawn } = await import('child_process');
    const scriptPath = fileURLToPath(import.meta.url);
    const childArgs = normalizedArgs.filter(arg => !arg.startsWith('--daemon'));

    const child = spawn(process.execPath, [scriptPath, ...childArgs], {
      cwd,
      detached: true,
      stdio: 'ignore'
    });
    child.unref();

    const stateDir = path.join(cwd, '.project-index');
    console.log(`module-analyzer started in background (pid: ${child.pid})`);
    console.log(`Check progress: tail -f "${path.join(stateDir, '.module-analyzer.log')}"`);
    console.log(`Check result: node "${scriptPath}" --status`);
    return;
  }

  if (args._ && args._.length > 1) {
    console.error('Too many paths provided. Only one path is supported.');
    process.exit(1);
  }

  let pathFilter = null;
  try {
    pathFilter = await resolvePathFilter(args._?.[0], cwd);
  } catch (e) {
    console.error(e.message);
    process.exit(1);
  }

  // Load config from project root
  const config = await loadConfig(cwd);
  const features = config.features || {};

  // CLI args override config
  const enableDoc = !args.noDoc && (features.doc !== false);
  const enableAudit = !args.noAudit && (features.audit !== false);
  const enableKanban = !args.noKanban && (features.kanban !== false);
  const effectiveKanban = enableKanban && enableAudit;

  if (!enableDoc && !enableAudit) {
    console.log('Nothing to do: doc and audit are both disabled.');
    return;
  }

  const requestedModes = new Set();
  if (args.stale) requestedModes.add('stale');
  if (args.missing) requestedModes.add('missing');
  if (args.all) requestedModes.add('all');
  if (args.force) requestedModes.add('force');
  if (args.reindex) requestedModes.add('force');

  if (requestedModes.size > 1) {
    console.error('Only one mode can be selected: --stale | --missing | --all | --force.');
    process.exit(1);
  }

  const mode = requestedModes.size === 0 ? 'stale' : Array.from(requestedModes)[0];
  const scanPath = pathFilter || '.';

  let concurrency = config.concurrency || 6;
  if (args.concurrency !== undefined) {
    if (!Number.isInteger(args.concurrency) || args.concurrency <= 0) {
      console.error('Invalid --concurrency value. Expected a positive integer.');
      process.exit(1);
    }
    concurrency = args.concurrency;
  }

  const modules = await getModulesByMode({
    mode,
    cwd,
    scanPath,
    enableDoc,
    enableAudit
  });

  const filtered = sortModules(filterModules(modules, config, pathFilter));

  if (args.dryRun) {
    if (args.resume) {
      console.log('Note: --dry-run ignores --resume.');
    }
    const scopeLabel = pathFilter && pathFilter !== '.' ? ` (scope: ${pathFilter})` : '';
    console.log(`Dry run: ${filtered.length} modules${scopeLabel}`);
    for (const mod of filtered) {
      console.log(`- ${mod.path}`);
    }
    return;
  }

  if (filtered.length === 0 && !args.resume) {
    console.log('No modules to process.');
    return;
  }

  console.log(`Features: doc=${enableDoc}, audit=${enableAudit}, kanban=${effectiveKanban}`);
  console.log(`Mode: ${mode.toUpperCase()}`);
  if (pathFilter && pathFilter !== '.') {
    console.log(`Scope: ${pathFilter}`);
  }
  console.log(`Modules: ${filtered.length}`);

  // Detect project for Kanban integration
  let projectId = null;
  if (effectiveKanban) {
    const project = await detectProject();
    if (project) {
      projectId = project.id;
      console.log(`Kanban project: ${project.name} (${project.id})`);
    } else {
      console.log('Kanban: project not found, tasks will not be created');
    }
  }

  // Extract conventions for prompt injection
  const conventions = config.conventions || null;
  if (conventions) {
    console.log(`Conventions: ${conventions.language || 'default'}`);
  }

  // Register project in skills registry
  const registryPath = path.join(__dirname, 'projects.json');
  try {
    let registry = { version: 1, projects: [] };
    try {
      const content = await fs.readFile(registryPath, 'utf-8');
      registry = JSON.parse(content);
    } catch { }

    const existingIdx = registry.projects.findIndex(p => p.path === cwd);
    const projectEntry = {
      path: cwd,
      name: path.basename(cwd),
      lastRun: new Date().toISOString()
    };

    if (existingIdx >= 0) {
      registry.projects[existingIdx] = projectEntry;
    } else {
      registry.projects.push(projectEntry);
    }
    registry.lastUpdated = new Date().toISOString();
    await fs.writeFile(registryPath, JSON.stringify(registry, null, 2));
    console.log(`Project registered: ${projectEntry.name}`);
  } catch (e) {
    console.log('Failed to register project:', e.message);
  }

  const runner = new BatchRunner({
    name: 'module-analyzer',
    concurrency,
    timeout: config.timeout || 180000,
    stateDir: cwd,  // Store state in project directory, not skills directory
    silent: true
  });

  await runner.run({
    scan: async () => filtered.map(m => ({
      id: m.path,
      modulePath: m.path,
      changedFiles: m.changedFiles || [],
      fullPath: path.join(cwd, m.path),
      projectId,
      enableDoc,
      enableAudit,
      enableKanban: effectiveKanban,
      conventions,
      security: config.security || null,
      testing: config.testing || null,
      directoryRules: config.directoryRules || null
    })),

    buildPrompt: async function (item) {
      const claudeMdPath = path.join(item.fullPath, 'CLAUDE.md');
      const claudeContent = await readFileSafe(claudeMdPath, 80) || '(无现有文档)';
      const codeContent = await readCodeFiles(item.fullPath, item.changedFiles, 5, 60);

      // Find matching directory rules (longest prefix match)
      let dirRules = null;
      if (item.directoryRules) {
        const candidates = Object.keys(item.directoryRules)
          .filter(dir => item.modulePath.startsWith(dir))
          .sort((a, b) => b.length - a.length);
        if (candidates.length > 0) {
          dirRules = item.directoryRules[candidates[0]];
        }
      }

      // Build conventions section
      let conventionsSection = '';
      if (item.conventions) {
        const c = item.conventions;
        conventionsSection = `
## 项目约定
- 语言: ${c.language || 'N/A'}
- 运行时: ${c.runtime || 'N/A'}
- 模块系统: ${c.moduleSystem || 'ES Modules'}

### 代码风格
${c.codeStyle?.map(r => `- ${r}`).join('\n') || ''}

### JSDoc 规范
${c.jsDocRules?.map(r => `- ${r}`).join('\n') || ''}

### 错误处理
${c.errorHandling?.map(r => `- ${r}`).join('\n') || ''}
`;
      }

      // Build security section
      let securitySection = '';
      if (item.security) {
        const s = item.security;
        securitySection = `
## 安全审计检查清单

### Critical (必须修复)
${s.critical?.map(r => `- ${r}`).join('\n') || ''}

### High (高优先级)
${s.high?.map(r => `- ${r}`).join('\n') || ''}

### Medium (中优先级)
${s.medium?.map(r => `- ${r}`).join('\n') || ''}

### 浏览器兼容性
${s.browserSpecific?.map(r => `- ${r}`).join('\n') || ''}
`;
      }

      // Build directory-specific section
      let dirSection = '';
      if (dirRules) {
        dirSection = `
## 该目录特别关注 (优先级: ${dirRules.priority || 'medium'})
${dirRules.focus?.map(f => `- ${f}`).join('\n') || ''}

### 测试重点
${dirRules.testFocus?.map(f => `- ${f}`).join('\n') || ''}
`;
      }

      // Build testing section
      let testingSection = '';
      if (item.testing) {
        const t = item.testing;
        testingSection = `
## 测试质量要求
- 目标覆盖率: ${t.coverage?.target || 90}%
- 最低覆盖率: ${t.coverage?.minimum || 70}%

### 反模式检查 (这些是问题)
${t.antiPatterns?.map(r => `- ${r}`).join('\n') || ''}

### 边界条件必测
${t.boundaryConditions?.map(r => `- ${r}`).join('\n') || ''}
`;
      }

      return `你是一个代码分析专家。请同时完成两个任务：

## 任务 1: 更新模块文档
判断代码变更是否需要更新 CLAUDE.md，如需要则生成新内容。

## 任务 2: 安全审计
检查代码中的安全漏洞和质量问题。按照下面的检查清单逐项审查。
${conventionsSection}${securitySection}${dirSection}${testingSection}
---
模块路径: ${item.modulePath}

当前 CLAUDE.md:
\`\`\`markdown
${claudeContent.slice(0, 2000)}
\`\`\`

变更的代码:
${codeContent.slice(0, 4000)}

---
请以 JSON 格式返回：
{
  "doc": {
    "needsUpdate": true/false,
    "reason": "简要说明",
    "content": "如需更新，完整的新 CLAUDE.md 内容（保持原有风格）"
  },
  "audit": {
    "severity": "none|low|medium|high|critical",
    "issues": [{"type": "类型", "severity": "critical|high|medium|low", "description": "描述", "file": "文件", "line": 行号, "context": "相关代码片段", "suggestion": "建议"}],
    "summary": "审计总结"
  }
}`;
    },

    handleResult: async (item, result) => {
      if (!result.success) {
        return { status: 'llm_error', reason: result.error, sessionId: result.sessionId };
      }

      const jsonMatch = result.output.match(/\{[\s\S]*"doc"[\s\S]*"audit"[\s\S]*\}/);
      if (!jsonMatch) {
        return { status: 'parse_error', reason: 'no json found', sessionId: result.sessionId };
      }

      let parsed;
      try {
        parsed = JSON.parse(jsonMatch[0]);
      } catch {
        return { status: 'parse_error', reason: 'invalid json', sessionId: result.sessionId };
      }

      const claudeMdPath = path.join(item.fullPath, 'CLAUDE.md');
      const auditMdPath = path.join(item.fullPath, 'AUDIT.md');
      const now = new Date();
      let docStatus = 'skipped';
      let auditStatus = 'skipped';
      let kanbanResult = { taskIds: [] };

      // Handle doc update (if enabled)
      if (item.enableDoc) {
        if (parsed.doc?.needsUpdate && parsed.doc?.content?.length > 50) {
          await fs.writeFile(claudeMdPath, parsed.doc.content);
          docStatus = 'updated';
        } else {
          // Touch to mark as fresh
          try {
            await fs.utimes(claudeMdPath, now, now);
            docStatus = 'touched';
          } catch { }
        }
      }

      // Handle audit (if enabled)
      if (item.enableAudit && parsed.audit && parsed.audit.severity !== 'none') {
        const issues = parsed.audit.issues || [];
        const auditContent = `# Security Audit - ${item.modulePath}

Generated: ${now.toISOString()}
Severity: **${parsed.audit.severity?.toUpperCase()}**

## Summary
${parsed.audit.summary || 'N/A'}

## Issues (${issues.length})
${issues.length > 0
            ? issues.map((i, idx) => `### ${idx + 1}. ${i.type}
- **File**: ${i.file || 'N/A'}${i.line ? `:${i.line}` : ''}
- **Description**: ${i.description}
- **Suggestion**: ${i.suggestion || 'N/A'}
${i.context ? `\`\`\`\n${i.context}\n\`\`\`` : ''}
`).join('\n')
            : 'No issues found.'}
`;
        await fs.writeFile(auditMdPath, auditContent);
        auditStatus = parsed.audit.severity;

        // Create Kanban tasks if enabled and has issues
        if (item.enableKanban && item.projectId && issues.length > 0) {
          kanbanResult = await createAuditTasks(item.projectId, item.modulePath, parsed.audit);
        }
      }

      return {
        status: 'processed',
        doc: docStatus,
        audit: auditStatus,
        issueCount: parsed.audit?.issues?.length || 0,
        kanban: kanbanResult.taskIds?.length > 0 ? {
          taskCount: kanbanResult.taskIds.length,
          taskIds: kanbanResult.taskIds
        } : null
      };
    }
  }, {
    resume: args.resume,
    retryFailed: args.retryFailed,
    cwd
  });
}

main().catch(console.error);
