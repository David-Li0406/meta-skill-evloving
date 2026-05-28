#!/usr/bin/env node
/**
 * Batch LLM Runner - Generic framework for parallel LLM tasks
 *
 * Features:
 * - Concurrent execution with configurable limit
 * - Detailed per-task state tracking (pending/running/completed/failed)
 * - Checkpoint/resume for crash recovery
 * - Single task retry support
 * - Real-time progress updates for dashboard
 *
 * Usage:
 *   import { BatchRunner } from './batch-llm-runner.js';
 *
 *   const runner = new BatchRunner({
 *     name: 'code-audit',
 *     concurrency: 8,
 *     timeout: 120000
 *   });
 *
 *   await runner.run({
 *     scan: async (cwd) => [...items],
 *     buildPrompt: (item) => '...',
 *     handleResult: async (item, result) => { ... }
 *   });
 *
 * CLI:
 *   node batch-llm-runner.js --status <name>      # Show task status
 *   node batch-llm-runner.js --retry <name> <id>  # Retry single task
 */

import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { spawn } from 'child_process';
import {
  readJsonSafe,
  writeJsonSafe,
  unlinkSafe,
  createLogger,
  DEFAULT_CONCURRENCY,
  DEFAULT_TIMEOUT
} from './shared.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/**
 * @typedef {'pending' | 'running' | 'completed' | 'failed' | 'timeout' | 'cancelled'} TaskStatus
 */

/**
 * @typedef {object} TaskState
 * @property {string} id - Task identifier
 * @property {TaskStatus} status - Current status
 * @property {string} [module] - Module path or scope
 * @property {Date} [startedAt] - When task started
 * @property {Date} [completedAt] - When task completed
 * @property {number} [duration] - Duration in ms
 * @property {string} [error] - Error message if failed
 * @property {string} [sessionId] - LLM session ID for resume
 * @property {object} [result] - Task result
 * @property {number} [retryCount] - Number of retries
 */

/**
 * Run codeagent-wrapper with spawn, capture session_id and validate output
 * Uses stdin to pass prompt to avoid argument length issues
 * @param {string} prompt
 * @param {string} cwd
 * @param {number} timeout
 * @returns {Promise<{success: boolean, output: string, sessionId: string|null, error: string|null, isRateLimited: boolean}>}
 */
export async function runCodeagent(prompt, cwd, timeout = 120000, options = {}) {
  return new Promise((resolve) => {
    // Use "-" to read from stdin, configurable backend via env
    const backend = process.env.CODEAGENT_BACKEND || 'codex';

    const args = ['--backend', backend, '-'];

    const child = spawn('codeagent-wrapper', args, {
      cwd,
      stdio: ['pipe', 'pipe', 'pipe'],
      env: {
        ...process.env,
        CODEX_TIMEOUT: String(timeout)  // Pass timeout to codeagent-wrapper
      }
    });

    let stdout = '';
    let stderr = '';
    let sessionId = null;
    let resolved = false;

    const timer = setTimeout(() => {
      if (!resolved) {
        resolved = true;
        child.kill('SIGTERM');
        resolve({
          success: false,
          output: stdout,
          sessionId,
          error: 'timeout',
          isRateLimited: false
        });
      }
    }, timeout);

    child.stdout.on('data', (data) => { stdout += data.toString(); });
    child.stderr.on('data', (data) => {
      const chunk = data.toString();
      stderr += chunk;
      const match = chunk.match(/SESSION_ID:\s*([a-f0-9-]+)/i);
      if (match) sessionId = match[1];
    });

    child.on('close', (code) => {
      if (resolved) return;
      resolved = true;
      clearTimeout(timer);

      const trimmedOutput = stdout.trim();
      const isSuccess = code === 0 && trimmedOutput;
      const isRateLimited = !isSuccess && isRateLimitError(code, stderr);

      if (isSuccess) {
        resolve({
          success: true,
          output: trimmedOutput,
          sessionId,
          error: null,
          isRateLimited: false
        });
        return;
      }

      resolve({
        success: false,
        output: trimmedOutput,
        sessionId,
        error: code === 0 ? 'empty output' : `exit code ${code}`,
        isRateLimited
      });
    });

    child.on('error', (err) => {
      if (resolved) return;
      resolved = true;
      clearTimeout(timer);
      resolve({
        success: false,
        output: '',
        sessionId,
        error: err.message,
        isRateLimited: false
      });
    });

    // Write prompt to stdin and close
    child.stdin.write(prompt);
    child.stdin.end();
  });
}

function isRateLimitError(code, stderr) {
  // 429 = rate limit
  if (code === 429) return true;
  if (!stderr) return false;
  // Check for rate limit patterns
  if (/\b429\b/.test(stderr) || /rate limit|too many requests/i.test(stderr)) {
    return true;
  }
  // Treat 400 with "No available" as transient (CRS proxy account switching)
  if (/\b400\b/.test(stderr) && /no available|account/i.test(stderr)) {
    return true;
  }
  return false;
}

/**
 * Run codeagent-wrapper with retry on rate limit or transient errors
 * @param {string} prompt
 * @param {string} cwd
 * @param {number} timeout
 * @param {number} [maxRetries=3]
 * @param {number} [retryDelay=5000]
 * @returns {Promise<{success: boolean, output: string, sessionId: string|null, error: string|null, isRateLimited: boolean}>}
 */
export async function runWithRetry(prompt, cwd, timeout, maxRetries = 3, retryDelay = 5000) {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    const result = await runCodeagent(prompt, cwd, timeout);

    // Retry on rate limit or exit code errors (transient failures)
    const shouldRetry = result.isRateLimited ||
      (result.error && result.error.startsWith('exit code'));

    if (!shouldRetry || attempt === maxRetries) {
      return result;
    }

    const delay = retryDelay * Math.pow(2, attempt);
    await new Promise(resolve => setTimeout(resolve, delay));
  }
}

/**
 * Concurrency pool for parallel execution with status tracking
 */
async function runWithConcurrency(tasks, concurrency, handler, onStatusChange) {
  const results = [];
  const executing = new Map(); // promise -> taskId

  for (const task of tasks) {
    const promise = (async () => {
      onStatusChange?.(task.id, 'running');
      const result = await handler(task);
      executing.delete(promise);
      return result;
    })();

    executing.set(promise, task.id);
    results.push(promise);

    if (executing.size >= concurrency) {
      await Promise.race(executing.keys());
    }
  }

  return Promise.all(results);
}

/**
 * @typedef {Object} BatchRunnerOptions
 * @property {string} name - Task name for file naming
 * @property {number} [concurrency=8] - Max concurrent tasks
 * @property {number} [timeout=120000] - Timeout per LLM call in ms
 * @property {number} [maxRetries=3] - Max retries for rate-limited calls
 * @property {number} [retryDelay=5000] - Base delay in ms for exponential backoff
 * @property {string} [stateDir] - Directory for state files (default: __dirname)
 * @property {boolean} [silent=false] - Suppress console output
 */

/**
 * @typedef {Object} TaskHandlers
 * @property {(cwd: string) => Promise<Array<{id: string, [key: string]: any}>>} scan - Returns items to process
 * @property {(item: object) => string | Promise<string>} buildPrompt - Build LLM prompt for item
 * @property {(item: object, result: {success: boolean, output: string, sessionId: string|null, error: string|null, isRateLimited: boolean}) => Promise<{status: string, [key: string]: any}>} handleResult - Process LLM result
 */

export class BatchRunner {
  /**
   * @param {BatchRunnerOptions} options
   */
  constructor(options) {
    this.name = options.name;
    this.concurrency = options.concurrency || DEFAULT_CONCURRENCY;
    this.timeout = options.timeout || DEFAULT_TIMEOUT;
    this.maxRetries = options.maxRetries ?? 3;
    this.retryDelay = options.retryDelay ?? 5000;

    // Use .project-index subfolder for state files
    const baseDir = options.stateDir || __dirname;
    this.stateDir = path.join(baseDir, '.project-index');
    this.silent = options.silent || false;

    this.logFile = path.join(this.stateDir, `.${this.name}.log`);
    this.progressFile = path.join(this.stateDir, `.${this.name}-progress.json`);
    this.resultFile = path.join(this.stateDir, `.${this.name}-result.json`);
    this.tasksFile = path.join(this.stateDir, `.${this.name}-tasks.json`);

    this.logger = createLogger(this.logFile, this.silent);

    /** @type {Map<string, TaskState>} */
    this.taskStates = new Map();
  }

  /**
   * Ensure state directory exists
   */
  async ensureStateDir() {
    await fs.mkdir(this.stateDir, { recursive: true });
  }

  async log(msg) {
    await this.logger.log(msg);
  }

  /**
   * Load task states from file
   */
  async loadTaskStates() {
    const data = await readJsonSafe(this.tasksFile, { tasks: [] });
    this.taskStates = new Map(data.tasks.map(t => [t.id, t]));
    return this.taskStates;
  }

  /**
   * Save task states to file (for dashboard to read)
   */
  async saveTaskStates() {
    const tasks = Array.from(this.taskStates.values());
    const summary = {
      total: tasks.length,
      pending: tasks.filter(t => t.status === 'pending').length,
      running: tasks.filter(t => t.status === 'running').length,
      completed: tasks.filter(t => t.status === 'completed').length,
      failed: tasks.filter(t => t.status === 'failed').length,
      timeout: tasks.filter(t => t.status === 'timeout').length
    };

    await writeJsonSafe(this.tasksFile, {
      name: this.name,
      updatedAt: new Date().toISOString(),
      summary,
      tasks
    });
  }

  /**
   * Update a single task's state
   * @param {string} id
   * @param {Partial<TaskState>} updates
   */
  async updateTaskState(id, updates) {
    const existing = this.taskStates.get(id) || { id, status: 'pending' };
    this.taskStates.set(id, { ...existing, ...updates });
    await this.saveTaskStates();
  }

  async loadProgress() {
    return await readJsonSafe(this.progressFile, {
      status: 'idle',
      items: [],
      completed: [],
      results: []
    });
  }

  async saveProgress(progress) {
    await writeJsonSafe(this.progressFile, progress);
  }

  async clearProgress() {
    await unlinkSafe(this.progressFile);
  }

  /**
   * Get current task status summary
   */
  async getStatus() {
    const data = await readJsonSafe(this.tasksFile, null);
    if (!data) {
      return { status: 'never_run', name: this.name };
    }
    return data;
  }

  /**
   * Retry a specific failed task
   * @param {string} taskId
   * @param {TaskHandlers} handlers
   * @param {string} cwd
   */
  async retryTask(taskId, handlers, cwd) {
    await this.loadTaskStates();
    const task = this.taskStates.get(taskId);

    if (!task) {
      throw new Error(`Task not found: ${taskId}`);
    }

    if (task.status !== 'failed' && task.status !== 'timeout') {
      throw new Error(`Task ${taskId} is not failed (status: ${task.status})`);
    }

    await this.log(`Retrying task: ${taskId}`);
    await this.updateTaskState(taskId, {
      status: 'running',
      startedAt: new Date().toISOString(),
      error: null,
      retryCount: (task.retryCount || 0) + 1
    });

    try {
      // Reconstruct item from saved state
      const item = { id: taskId, ...task.context };
      const prompt = await handlers.buildPrompt(item);
      const llmResult = await runWithRetry(
        prompt,
        cwd,
        this.timeout,
        this.maxRetries,
        this.retryDelay
      );
      const result = await handlers.handleResult(item, llmResult);

      const completedAt = new Date().toISOString();
      await this.updateTaskState(taskId, {
        status: result.status.includes('error') ? 'failed' : 'completed',
        completedAt,
        duration: new Date(completedAt) - new Date(task.startedAt),
        sessionId: llmResult.sessionId,
        result,
        error: result.status.includes('error') ? result.reason : null
      });

      await this.log(`  → Retry ${result.status}: ${taskId}`);
      return result;
    } catch (e) {
      await this.updateTaskState(taskId, {
        status: 'failed',
        completedAt: new Date().toISOString(),
        error: e.message
      });
      throw e;
    }
  }

  /**
   * Run batch processing
   * @param {TaskHandlers} handlers
   * @param {object} [options]
   * @param {boolean} [options.resume=false] - Resume from checkpoint
   * @param {string} [options.cwd] - Working directory
   */
  async run(handlers, options = {}) {
    const cwd = options.cwd || process.cwd();

    // Ensure .project-index directory exists
    await this.ensureStateDir();

    await fs.writeFile(this.logFile, '');
    await this.log(`Started: ${this.name}`);
    await this.log(`Concurrency: ${this.concurrency}`);

    let progress = await this.loadProgress();
    const resumeMode = options.resume || progress.status === 'running';
    const retryFailedMode = options.retryFailed === true;
    let itemsToProcess;
    let existingResults = [];

    if (resumeMode && progress.status === 'running') {
      // Resume interrupted run
      await this.log(`Resuming from checkpoint...`);
      await this.loadTaskStates();

      // Get incomplete tasks
      const completedSet = new Set(progress.completed);
      itemsToProcess = progress.items.filter(item => !completedSet.has(item.id));
      existingResults = progress.results || [];
      await this.log(`Remaining: ${itemsToProcess.length}`);
    } else if (retryFailedMode || (options.resume && progress.status !== 'running')) {
      // Retry failed tasks from previous completed run
      await this.log(`Retrying failed tasks...`);
      await this.loadTaskStates();

      // Find failed/timeout tasks
      const failedTasks = Array.from(this.taskStates.values())
        .filter(t => t.status === 'failed' || t.status === 'timeout');

      if (failedTasks.length === 0) {
        await this.log(`No failed tasks to retry`);
        await this.log(`Completed`);
        return [];
      }

      // Reset failed tasks to pending for retry
      itemsToProcess = failedTasks.map(t => t.context || { id: t.id, modulePath: t.module });
      for (const task of failedTasks) {
        await this.updateTaskState(task.id, {
          status: 'pending',
          error: null,
          retryCount: (task.retryCount || 0) + 1
        });
      }
      existingResults = progress.results?.filter(r => !failedTasks.some(t => t.id === r.id)) || [];
      await this.log(`Retrying: ${itemsToProcess.length} failed tasks`);
    } else {
      const allItems = await handlers.scan(cwd);
      await this.log(`Scanned: ${allItems.length} items`);
      itemsToProcess = allItems;

      // Initialize all task states
      this.taskStates.clear();
      for (const item of allItems) {
        this.taskStates.set(item.id, {
          id: item.id,
          status: 'pending',
          module: item.modulePath || item.id,
          context: { ...item } // Save context for potential retry
        });
      }
      await this.saveTaskStates();

      progress = {
        status: 'running',
        startedAt: new Date().toISOString(),
        items: itemsToProcess,
        completed: [],
        results: []
      };
      await this.saveProgress(progress);
    }

    await this.log(`Processing ${itemsToProcess.length} items...`);

    const results = await runWithConcurrency(
      itemsToProcess,
      this.concurrency,
      async (item) => {
        const startedAt = new Date();
        await this.updateTaskState(item.id, {
          status: 'running',
          startedAt: startedAt.toISOString()
        });

        try {
          await this.log(`Processing: ${item.id}`);
          const prompt = await handlers.buildPrompt(item);
          const llmResult = await runWithRetry(
            prompt,
            cwd,
            this.timeout,
            this.maxRetries,
            this.retryDelay
          );
          const result = await handlers.handleResult(item, llmResult);

          const completedAt = new Date();
          const status = llmResult.error === 'timeout' ? 'timeout' :
            result.status.includes('error') ? 'failed' : 'completed';

          await this.updateTaskState(item.id, {
            status,
            completedAt: completedAt.toISOString(),
            duration: completedAt - startedAt,
            sessionId: llmResult.sessionId,
            result,
            error: status !== 'completed' ? (llmResult.error || result.reason) : null
          });

          progress.completed.push(item.id);
          progress.results.push({ id: item.id, ...result });
          await this.saveProgress(progress);

          await this.log(`  → ${result.status}: ${item.id}`);
          return { id: item.id, ...result };
        } catch (e) {
          const completedAt = new Date();
          await this.updateTaskState(item.id, {
            status: 'failed',
            completedAt: completedAt.toISOString(),
            duration: completedAt - startedAt,
            error: e.message
          });

          await this.log(`  → Error: ${item.id} - ${e.message}`);
          const errorResult = { id: item.id, status: 'error', reason: e.message };

          progress.completed.push(item.id);
          progress.results.push(errorResult);
          await this.saveProgress(progress);

          return errorResult;
        }
      },
      (id, status) => {
        // Status change callback - could be used for real-time updates
      }
    );

    const allResults = [...existingResults, ...results];

    // Summarize
    const byStatus = {};
    for (const r of allResults) {
      byStatus[r.status] = (byStatus[r.status] || 0) + 1;
    }

    await this.log(`\nSummary: ${allResults.length} processed`);
    for (const [status, count] of Object.entries(byStatus)) {
      await this.log(`  ${status}: ${count}`);
    }

    const errors = allResults.filter(r => r.status.includes('error'));

    const resultData = {
      name: this.name,
      completedAt: new Date().toISOString(),
      status: errors.length === 0 ? 'success' : 'completed_with_errors',
      processed: allResults.length,
      byStatus,
      failed: errors.length,
      failedList: errors.map(e => ({ id: e.id, reason: e.reason }))
    };

    await fs.writeFile(this.resultFile, JSON.stringify(resultData, null, 2));
    await this.log(`Result: ${this.resultFile}`);

    // Keep task states for retry capability
    await this.clearProgress();
    await this.log('Completed');

    return resultData;
  }
}

/**
 * CLI handling
 */
async function main() {
  const args = process.argv.slice(2);

  if (args[0] === '--status' && args[1]) {
    const runner = new BatchRunner({ name: args[1] });
    const status = await runner.getStatus();
    console.log(JSON.stringify(status, null, 2));
    return;
  }

  if (args[0] === '--list-failed' && args[1]) {
    const runner = new BatchRunner({ name: args[1] });
    const status = await runner.getStatus();
    if (status.tasks) {
      const failed = status.tasks.filter(t => t.status === 'failed' || t.status === 'timeout');
      console.log(`Failed/Timeout tasks (${failed.length}):\n`);
      for (const t of failed) {
        console.log(`  ${t.id}`);
        console.log(`    Status: ${t.status}`);
        console.log(`    Error: ${t.error || 'N/A'}`);
        console.log(`    Session: ${t.sessionId || 'N/A'}`);
        console.log('');
      }
    } else {
      console.log('No task data found');
    }
    return;
  }

  console.log(`Batch LLM Runner - Task Status Utility

Usage:
  node batch-llm-runner.js --status <name>       Show task status
  node batch-llm-runner.js --list-failed <name>  List failed tasks

Examples:
  node batch-llm-runner.js --status module-analyzer
  node batch-llm-runner.js --list-failed module-analyzer
`);
}

// Run CLI if invoked directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(console.error);
}
