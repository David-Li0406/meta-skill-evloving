#!/usr/bin/env node
/**
 * Task Manager - Centralized task management for Dashboard
 *
 * Features:
 * - PID tracking for running tasks
 * - Task cancellation via SIGTERM
 * - Task deletion from state files
 * - Batch retry for failed tasks
 * - Task launching from GUI
 *
 * Usage:
 *   import { TaskManager } from './task-manager.js';
 *   const manager = new TaskManager();
 *   await manager.cancelTask('module-analyzer', 'task-id');
 */

import { promises as fs } from 'fs';
import path from 'path'
import { fileURLToPath } from 'url';
import { spawn } from 'child_process';
import { readJsonSafe, writeJsonSafe } from './shared.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/**
 * PID file for tracking running processes
 * Format: { "module-analyzer": { "task-id": pid, ... }, ... }
 */
const PID_FILE = path.join(__dirname, '.task-pids.json');

/**
 * Available task types that can be launched from GUI
 */
export const TASK_TYPES = {
  'module-analyzer': {
    script: 'module-analyzer.js',
    description: '文档更新 + 代码审计',
    args: {
      '--stale': '仅过期模块 (默认)',
      '--missing': '仅缺失文档/审计',
      '--all': '过期 + 缺失',
      '--force': '强制刷新全部大目录',
      '--no-kanban': '不创建 Kanban 任务',
      '--no-doc': '跳过文档更新',
      '--no-audit': '跳过审计',
      '--dry-run': '只预览，不执行',
      '--concurrency': '并发数 (默认 6)',
      '--resume': '从中断处继续',
      '--retry-failed': '仅重试失败任务'
    }
  },
  'update-bg': {
    script: 'update-bg.js',
    description: '后台 CLAUDE.md 更新',
    args: {
      '--concurrency': '并发数 (默认 6)'
    }
  },
  'check-stale': {
    script: 'check-stale.js',
    description: '检测过期模块',
    args: {
      '--json': 'JSON 输出',
      '--stale-only': '只显示过期'
    }
  },
  'test-status': {
    script: 'test-status.js',
    description: '测试覆盖率分析',
    args: {
      '--untested': '只显示未测试',
      '--stale': '只显示过期测试'
    }
  },
  'test-analyzer': {
    script: 'test-analyzer.js',
    description: '测试质量检测',
    args: {
      '--summary': '只显示摘要',
      '--fix': '显示修复建议'
    }
  },
  'scan': {
    script: 'scan.js',
    description: '扫描项目结构',
    args: {}
  },
  'generate': {
    script: 'generate.js',
    description: '生成 CLAUDE.md',
    args: {
      '--auto': '自动生成所有层级',
      '--layer': '指定层级 (1/2/3)'
    }
  },
  'test-generator': {
    script: 'test-generator.js',
    description: '批量生成测试文件',
    args: {
      '--untested': '仅未测试文件 (默认)',
      '--stale': '仅过期测试',
      '--all': '未测试 + 过期',
      '--dry-run': '只预览，不执行',
      '--concurrency': '并发数 (默认 3)',
      '--resume': '从中断处继续',
      '--retry-failed': '仅重试失败任务'
    }
  },
  'test-fix': {
    script: 'test-fix.js',
    description: '测试错误自动修复',
    args: {
      '--dry-run': '只预览，不执行',
      '--concurrency': '并发数 (默认 6)',
      '--offset': '从第 N 个错误开始',
      '--limit': '处理 N 个错误 (默认 40)',
      '--resume': '从中断处继续',
      '--retry-failed': '仅重试失败任务'
    }
  },
  'audit-fix': {
    script: 'audit-fix.js',
    description: '审计问题自动修复',
    args: {
      '--dry-run': '只预览，不执行',
      '--severity': '只修复指定级别 (LOW/MEDIUM/HIGH)',
      '--module': '只修复指定模块',
      '--concurrency': '并发数 (默认 3)'
    }
  },
  'test-result': {
    script: 'test-result.js',
    description: '测试结果提取',
    args: {
      '--save': '保存结果到缓存',
      '--summary': '单行摘要输出',
      '--errors': '仅显示错误详情'
    }
  }
};

export class TaskManager {
  constructor(stateDir = __dirname) {
    this.stateDir = stateDir;
    /** @type {Map<string, Map<string, number>>} name -> (taskId -> pid) */
    this.runningPids = new Map();
  }

  /**
   * Get tasks file path for a task name
   */
  getTasksFile(name) {
    return path.join(this.stateDir, `.${name}-tasks.json`);
  }

  /**
   * Load PID mappings from file
   */
  async loadPids() {
    const data = await readJsonSafe(PID_FILE, {});
    for (const [name, pids] of Object.entries(data)) {
      this.runningPids.set(name, new Map(Object.entries(pids)));
    }
  }

  /**
   * Save PID mappings to file
   */
  async savePids() {
    const data = {};
    for (const [name, pids] of this.runningPids) {
      data[name] = Object.fromEntries(pids);
    }
    await writeJsonSafe(PID_FILE, data);
  }

  /**
   * Register a running task's PID
   */
  async registerPid(name, taskId, pid) {
    if (!this.runningPids.has(name)) {
      this.runningPids.set(name, new Map());
    }
    this.runningPids.get(name).set(taskId, pid);
    await this.savePids();
  }

  /**
   * Unregister a task's PID
   */
  async unregisterPid(name, taskId) {
    if (this.runningPids.has(name)) {
      this.runningPids.get(name).delete(taskId);
      await this.savePids();
    }
  }

  /**
   * Get task status data
   */
  async getTaskStatus(name) {
    const tasksFile = this.getTasksFile(name);
    return await readJsonSafe(tasksFile, null);
  }

  /**
   * Update task state in file
   */
  async updateTaskState(name, taskId, updates) {
    const tasksFile = this.getTasksFile(name);
    const data = await readJsonSafe(tasksFile, { tasks: [] });

    const taskIndex = data.tasks.findIndex(t => t.id === taskId);
    if (taskIndex === -1) {
      return { success: false, error: 'Task not found' };
    }

    data.tasks[taskIndex] = { ...data.tasks[taskIndex], ...updates };

    // Recalculate summary
    data.summary = {
      total: data.tasks.length,
      pending: data.tasks.filter(t => t.status === 'pending').length,
      running: data.tasks.filter(t => t.status === 'running').length,
      completed: data.tasks.filter(t => t.status === 'completed').length,
      failed: data.tasks.filter(t => t.status === 'failed').length,
      timeout: data.tasks.filter(t => t.status === 'timeout').length,
      cancelled: data.tasks.filter(t => t.status === 'cancelled').length
    };
    data.updatedAt = new Date().toISOString();

    await writeJsonSafe(tasksFile, data);
    return { success: true };
  }

  /**
   * Delete a task from state
   */
  async deleteTask(name, taskId) {
    const tasksFile = this.getTasksFile(name);
    const data = await readJsonSafe(tasksFile, { tasks: [] });

    const taskIndex = data.tasks.findIndex(t => t.id === taskId);
    if (taskIndex === -1) {
      return { success: false, error: 'Task not found' };
    }

    const task = data.tasks[taskIndex];
    if (task.status === 'running') {
      return { success: false, error: 'Cannot delete running task, cancel first' };
    }

    data.tasks.splice(taskIndex, 1);

    // Recalculate summary
    data.summary = {
      total: data.tasks.length,
      pending: data.tasks.filter(t => t.status === 'pending').length,
      running: data.tasks.filter(t => t.status === 'running').length,
      completed: data.tasks.filter(t => t.status === 'completed').length,
      failed: data.tasks.filter(t => t.status === 'failed').length,
      timeout: data.tasks.filter(t => t.status === 'timeout').length,
      cancelled: data.tasks.filter(t => t.status === 'cancelled').length
    };
    data.updatedAt = new Date().toISOString();

    await writeJsonSafe(tasksFile, data);
    return { success: true };
  }

  /**
   * Delete all completed tasks
   */
  async deleteCompletedTasks(name) {
    const tasksFile = this.getTasksFile(name);
    const data = await readJsonSafe(tasksFile, { tasks: [] });

    const before = data.tasks.length;
    data.tasks = data.tasks.filter(t => t.status !== 'completed');
    const deleted = before - data.tasks.length;

    // Recalculate summary
    data.summary = {
      total: data.tasks.length,
      pending: data.tasks.filter(t => t.status === 'pending').length,
      running: data.tasks.filter(t => t.status === 'running').length,
      completed: 0,
      failed: data.tasks.filter(t => t.status === 'failed').length,
      timeout: data.tasks.filter(t => t.status === 'timeout').length,
      cancelled: data.tasks.filter(t => t.status === 'cancelled').length
    };
    data.updatedAt = new Date().toISOString();

    await writeJsonSafe(tasksFile, data);
    return { success: true, deleted };
  }

  /**
   * Cancel a running task
   */
  async cancelTask(name, taskId) {
    await this.loadPids();

    // Check if we have a PID for this task
    const pids = this.runningPids.get(name);
    if (pids && pids.has(taskId)) {
      const pid = pids.get(taskId);
      try {
        process.kill(pid, 'SIGTERM');
      } catch (e) {
        // Process may already be dead
      }
      await this.unregisterPid(name, taskId);
    }

    // Update task state
    await this.updateTaskState(name, taskId, {
      status: 'cancelled',
      completedAt: new Date().toISOString(),
      error: 'Cancelled by user'
    });

    return { success: true };
  }

  /**
   * Get list of failed/timeout tasks for retry
   */
  async getFailedTasks(name) {
    const data = await this.getTaskStatus(name);
    if (!data || !data.tasks) return [];

    return data.tasks.filter(t =>
      t.status === 'failed' || t.status === 'timeout' || t.status === 'cancelled'
    );
  }

  /**
   * Launch a task type from GUI
   * Returns the spawned process info
   */
  async launchTask(type, args = [], cwd = process.cwd()) {
    const taskDef = TASK_TYPES[type];
    if (!taskDef) {
      return { success: false, error: `Unknown task type: ${type}` };
    }

    const scriptPath = path.join(__dirname, taskDef.script);

    try {
      await fs.access(scriptPath);
    } catch {
      return { success: false, error: `Script not found: ${taskDef.script}` };
    }

    // Spawn as detached background process
    const child = spawn('node', [scriptPath, ...args], {
      cwd,
      detached: true,
      stdio: 'ignore'
    });
    child.unref();

    return {
      success: true,
      pid: child.pid,
      type,
      args,
      message: `Started ${type} (PID: ${child.pid})`
    };
  }

  /**
   * Get available task types
   */
  getTaskTypes() {
    return Object.entries(TASK_TYPES).map(([name, def]) => ({
      name,
      script: def.script,
      description: def.description,
      args: def.args
    }));
  }
}

// CLI interface
async function main() {
  const args = process.argv.slice(2);
  const manager = new TaskManager();

  if (args[0] === '--list-types') {
    const types = manager.getTaskTypes();
    console.log(JSON.stringify(types, null, 2));
    return;
  }

  if (args[0] === '--cancel' && args[1] && args[2]) {
    const result = await manager.cancelTask(args[1], args[2]);
    console.log(JSON.stringify(result));
    return;
  }

  if (args[0] === '--delete' && args[1] && args[2]) {
    const result = await manager.deleteTask(args[1], args[2]);
    console.log(JSON.stringify(result));
    return;
  }

  if (args[0] === '--delete-completed' && args[1]) {
    const result = await manager.deleteCompletedTasks(args[1]);
    console.log(JSON.stringify(result));
    return;
  }

  if (args[0] === '--launch' && args[1]) {
    const taskArgs = args.slice(2);
    const result = await manager.launchTask(args[1], taskArgs);
    console.log(JSON.stringify(result));
    return;
  }

  console.log(`Task Manager - Dashboard Task Operations

Usage:
  node task-manager.js --list-types              List available task types
  node task-manager.js --cancel <name> <id>      Cancel running task
  node task-manager.js --delete <name> <id>      Delete task record
  node task-manager.js --delete-completed <name> Delete all completed tasks
  node task-manager.js --launch <type> [args]    Launch a task

Examples:
  node task-manager.js --cancel module-analyzer js/agents/core
  node task-manager.js --delete module-analyzer js/agents/core
  node task-manager.js --delete-completed module-analyzer
  node task-manager.js --launch module-analyzer --all
`);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(console.error);
}
