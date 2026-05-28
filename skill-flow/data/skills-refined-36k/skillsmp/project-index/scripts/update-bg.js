#!/usr/bin/env node
/**
 * Background CLAUDE.md updater with LLM review
 *
 * For each stale module:
 * 1. Read current CLAUDE.md
 * 2. Read changed code files
 * 3. Ask LLM: does the change affect the doc?
 * 4. If no → touch; If yes → generate updated doc
 *
 * Usage:
 *   node update-bg.js [--all | path1 path2 ...]
 *   node update-bg.js --status
 *   node update-bg.js --log
 */

import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { spawn, execSync } from 'child_process';

/**
 * Run codeagent-wrapper with spawn, capture session_id and validate output
 * @param {string} prompt
 * @param {string} cwd
 * @param {number} timeout
 * @returns {Promise<{success: boolean, output: string, sessionId: string|null, error: string|null}>}
 */
async function runCodeagent(prompt, cwd, timeout = 120000) {
  return new Promise((resolve) => {
    const child = spawn('codeagent-wrapper', ['--backend', 'codex', prompt], {
      cwd,
      stdio: ['pipe', 'pipe', 'pipe']
    });

    let stdout = '';
    let stderr = '';
    let sessionId = null;
    let resolved = false;

    const timer = setTimeout(() => {
      if (!resolved) {
        resolved = true;
        child.kill('SIGTERM');
        resolve({ success: false, output: stdout, sessionId, error: 'timeout' });
      }
    }, timeout);

    child.stdout.on('data', (data) => { stdout += data.toString(); });
    child.stderr.on('data', (data) => {
      const chunk = data.toString();
      stderr += chunk;
      // Extract session ID from stderr
      const match = chunk.match(/SESSION_ID:\s*([a-f0-9-]+)/i);
      if (match) sessionId = match[1];
    });

    child.on('close', (code) => {
      if (resolved) return;
      resolved = true;
      clearTimeout(timer);

      if (code === 0 && stdout.trim()) {
        resolve({ success: true, output: stdout.trim(), sessionId, error: null });
      } else {
        resolve({
          success: false,
          output: stdout.trim(),
          sessionId,
          error: code === 0 ? 'empty output' : `exit code ${code}`
        });
      }
    });

    child.on('error', (err) => {
      if (resolved) return;
      resolved = true;
      clearTimeout(timer);
      resolve({ success: false, output: '', sessionId, error: err.message });
    });
  });
}

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const LOG_FILE = path.join(__dirname, '.update-bg.log');
const PID_FILE = path.join(__dirname, '.update-bg.pid');
const RESULT_FILE = path.join(__dirname, '.update-result.json');
const PROGRESS_FILE = path.join(__dirname, '.update-progress.json');
const DEFAULT_CONCURRENCY = 8;

/**
 * Progress tracking for crash recovery
 */
async function loadProgress() {
  try {
    const content = await fs.readFile(PROGRESS_FILE, 'utf-8');
    return JSON.parse(content);
  } catch {
    return {
      status: 'idle',
      startedAt: null,
      items: [],        // All items to process
      completed: [],    // Completed item paths
      results: []       // Results for each completed item
    };
  }
}

async function saveProgress(progress) {
  await fs.writeFile(PROGRESS_FILE, JSON.stringify(progress, null, 2));
}

async function clearProgress() {
  try {
    await fs.unlink(PROGRESS_FILE);
  } catch {}
}

async function log(msg) {
  const timestamp = new Date().toISOString().slice(11, 19);
  const line = `[${timestamp}] ${msg}\n`;
  await fs.appendFile(LOG_FILE, line);
  console.log(line.trim()); // Also print when running as daemon
}

async function isRunning() {
  try {
    const pid = await fs.readFile(PID_FILE, 'utf-8');
    process.kill(parseInt(pid.trim()), 0);
    return true;
  } catch {
    return false;
  }
}

async function showStatus() {
  if (await isRunning()) {
    const pid = await fs.readFile(PID_FILE, 'utf-8');
    console.log(`Running (PID: ${pid.trim()})`);
  } else {
    console.log('Not running');
  }

  try {
    const logContent = await fs.readFile(LOG_FILE, 'utf-8');
    const lines = logContent.trim().split('\n').slice(-10);
    console.log('\nRecent log:');
    lines.forEach(l => console.log(`  ${l}`));
  } catch {
    console.log('\nNo log file found.');
  }
}

async function showLog() {
  try {
    const logContent = await fs.readFile(LOG_FILE, 'utf-8');
    console.log(logContent);
  } catch {
    console.log('No log file found.');
  }
}

/**
 * Get stale items from check-stale.js
 */
async function getStaleItems(cwd) {
  const checkScript = path.join(__dirname, 'check-stale.js');
  const result = execSync(`node "${checkScript}" --json`, {
    encoding: 'utf-8',
    cwd,
    timeout: 60000
  });
  return JSON.parse(result).filter(r => r.status === 'stale');
}

/**
 * Read file content safely
 */
async function readFileSafe(filePath, maxLines = 100) {
  try {
    const content = await fs.readFile(filePath, 'utf-8');
    const lines = content.split('\n');
    if (lines.length > maxLines) {
      return lines.slice(0, maxLines).join('\n') + `\n... (${lines.length - maxLines} more lines)`;
    }
    return content;
  } catch {
    return null;
  }
}

/**
 * Use codeagent-wrapper to generate updated CLAUDE.md content
 * @returns {Promise<{content: string|null, sessionId: string|null, error: string|null}>}
 */
async function generateWithLLM(claudeMdPath, changedFiles, cwd, modulePath) {
  const claudeContent = await readFileSafe(claudeMdPath);
  if (!claudeContent) return { content: null, sessionId: null, error: 'Cannot read CLAUDE.md' };

  // Read changed files
  const filesToCheck = changedFiles.slice(0, 5);
  let changedContent = '';

  for (const f of filesToCheck) {
    const fullPath = path.join(cwd, f.path);
    const content = await readFileSafe(fullPath, 80);
    if (content) {
      changedContent += `\n--- ${f.path} ---\n${content}\n`;
    }
  }

  const prompt = `你是一个代码文档维护助手。请根据代码变更更新 CLAUDE.md 文档。

模块路径: ${modulePath}

当前 CLAUDE.md 内容:
\`\`\`markdown
${claudeContent.slice(0, 3000)}
\`\`\`

变更的代码文件:
${changedContent.slice(0, 4000)}

请生成更新后的 CLAUDE.md 内容。保持原有结构和风格，只更新与代码变更相关的部分。
直接输出 markdown 内容，不要包含 \`\`\`markdown 标记。`;

  const result = await runCodeagent(prompt, cwd, 180000);

  if (result.success && result.output.length > 50) {
    return { content: result.output, sessionId: result.sessionId, error: null };
  }
  return { content: null, sessionId: result.sessionId, error: result.error || 'empty or too short' };
}

/**
 * Concurrency pool for parallel execution
 */
async function runWithConcurrency(tasks, concurrency, handler) {
  const results = [];
  const executing = new Set();

  for (const task of tasks) {
    const promise = handler(task).then(result => {
      executing.delete(promise);
      return result;
    });
    executing.add(promise);
    results.push(promise);

    if (executing.size >= concurrency) {
      await Promise.race(executing);
    }
  }

  return Promise.all(results);
}
/**
 * Check if CLAUDE.md needs update using LLM
 * @returns {Promise<{needsUpdate: boolean, reason: string, sessionId: string|null, error: string|null}>}
 */
async function checkWithLLM(claudeMdPath, changedFiles, cwd) {
  const claudeContent = await readFileSafe(claudeMdPath);
  if (!claudeContent) return { needsUpdate: false, reason: 'Cannot read CLAUDE.md', sessionId: null, error: null };

  // Read changed files (limit to first 3)
  const filesToCheck = changedFiles.slice(0, 3);
  let changedContent = '';

  for (const f of filesToCheck) {
    const fullPath = path.join(cwd, f.path);
    const content = await readFileSafe(fullPath, 50);
    if (content) {
      changedContent += `\n--- ${f.path} ---\n${content}\n`;
    }
  }

  if (!changedContent) {
    return { needsUpdate: false, reason: 'Cannot read changed files', sessionId: null, error: null };
  }

  // Build prompt for LLM
  const prompt = `你是一个代码文档审查助手。请判断以下代码变更是否需要更新 CLAUDE.md 文档。

当前 CLAUDE.md 内容:
\`\`\`markdown
${claudeContent.slice(0, 2000)}
\`\`\`

变更的代码文件:
${changedContent.slice(0, 3000)}

请判断：这些代码变更是否影响 CLAUDE.md 中描述的模块职责、接口、架构或重要功能？

回答格式 (JSON):
{"needsUpdate": true/false, "reason": "简要说明", "suggestedChanges": "如需更新，建议修改哪些部分"}`;

  const result = await runCodeagent(prompt, cwd, 120000);

  if (!result.success) {
    // LLM failed - don't touch, mark as error for retry
    return { needsUpdate: false, reason: `LLM failed: ${result.error}`, sessionId: result.sessionId, error: result.error };
  }

  // Parse JSON from response
  const jsonMatch = result.output.match(/\{[\s\S]*"needsUpdate"[\s\S]*\}/);
  if (jsonMatch) {
    try {
      const parsed = JSON.parse(jsonMatch[0]);
      return { ...parsed, sessionId: result.sessionId, error: null };
    } catch {
      return { needsUpdate: false, reason: 'JSON parse failed', sessionId: result.sessionId, error: 'invalid json' };
    }
  }
  return { needsUpdate: false, reason: 'LLM response unclear', sessionId: result.sessionId, error: null };
}

/**
 * Touch a CLAUDE.md file (update mtime only)
 */
async function touchFile(filePath) {
  const now = new Date();
  await fs.utimes(filePath, now, now);
}

/**
 * Process a single stale item
 * @returns {Promise<{status: string, path: string, sessionId?: string, reason?: string}>}
 */
async function processItem(item, cwd) {
  const claudeMdPath = path.join(cwd, item.path, 'CLAUDE.md');
  await log(`Checking: ${item.path}`);

  const checkResult = await checkWithLLM(claudeMdPath, item.changedFiles || [], cwd);

  // If LLM check failed, don't touch - keep stale for retry
  if (checkResult.error) {
    await log(`  → LLM check failed: ${checkResult.error} (session: ${checkResult.sessionId || 'none'})`);
    return { status: 'llm_error', path: item.path, sessionId: checkResult.sessionId, reason: checkResult.error };
  }

  if (checkResult.needsUpdate) {
    await log(`  → Needs update: ${checkResult.reason}`);

    // Generate new content
    const genResult = await generateWithLLM(claudeMdPath, item.changedFiles || [], cwd, item.path);

    if (genResult.content) {
      await fs.writeFile(claudeMdPath, genResult.content);
      await log(`  → Updated: ${item.path}/CLAUDE.md`);
      return { status: 'updated', path: item.path, sessionId: genResult.sessionId };
    } else {
      await log(`  → Generation failed: ${genResult.error} (session: ${genResult.sessionId || 'none'})`);
      return { status: 'gen_error', path: item.path, sessionId: genResult.sessionId, reason: genResult.error };
    }
  } else {
    await log(`  → No update needed: ${checkResult.reason}`);
    await touchFile(claudeMdPath);
    await log(`  → Touched: ${item.path}/CLAUDE.md`);
    return { status: 'touched', path: item.path };
  }
}

/**
 * Main daemon logic with checkpoint recovery
 */
async function runDaemon(args) {
  const cwd = process.cwd();

  // Parse args
  const concurrencyArg = args.find(a => a.startsWith('--concurrency='));
  const concurrency = concurrencyArg
    ? parseInt(concurrencyArg.split('=')[1]) || DEFAULT_CONCURRENCY
    : DEFAULT_CONCURRENCY;
  const resumeMode = args.includes('--resume');

  // Check for interrupted task
  let progress = await loadProgress();

  if (progress.status === 'running' && !resumeMode) {
    // Previous task was interrupted
    await log(`Found interrupted task from ${progress.startedAt}`);
    await log(`Completed: ${progress.completed.length}/${progress.items.length}`);
    await log(`Use --resume to continue, or start fresh`);

    // Write a "crashed" result so hook can notify
    const crashResult = {
      completedAt: new Date().toISOString(),
      status: 'crashed',
      message: `任务在 ${progress.completed.length}/${progress.items.length} 处中断`,
      processed: progress.completed.length,
      touched: progress.results.filter(r => r.status === 'touched').length,
      updated: progress.results.filter(r => r.status === 'updated').length,
      failed: progress.results.filter(r => r.status === 'failed' || r.status === 'error').length,
      pending: progress.items.length - progress.completed.length,
      canResume: true
    };
    await fs.writeFile(RESULT_FILE, JSON.stringify(crashResult, null, 2));
    return;
  }

  await fs.writeFile(LOG_FILE, '');
  await log(`Started in ${cwd}`);
  await log(`Concurrency: ${concurrency}`);

  try {
    let itemsToProcess;
    let existingResults = [];

    if (resumeMode && progress.status === 'running') {
      // Resume from checkpoint
      await log(`Resuming interrupted task...`);
      const completedSet = new Set(progress.completed);
      itemsToProcess = progress.items.filter(item => !completedSet.has(item.path));
      existingResults = progress.results || [];
      await log(`Resuming ${itemsToProcess.length} remaining items`);
    } else {
      // Fresh start
      const staleItems = await getStaleItems(cwd);
      await log(`Found ${staleItems.length} stale CLAUDE.md files`);

      const processAll = args.includes('--all');
      const pathsToProcess = args.filter(a => !a.startsWith('--'));

      itemsToProcess = staleItems.filter(item => {
        if (processAll) return true;
        if (pathsToProcess.length === 0) return true;
        return pathsToProcess.some(p =>
          item.path === p || item.path.startsWith(p + '/') || item.path.startsWith(p)
        );
      });

      // Initialize progress
      progress = {
        status: 'running',
        startedAt: new Date().toISOString(),
        items: itemsToProcess,
        completed: [],
        results: []
      };
      await saveProgress(progress);
    }

    await log(`Processing ${itemsToProcess.length} items`);

    // Process with concurrency, saving progress after each
    const results = await runWithConcurrency(itemsToProcess, concurrency, async (item) => {
      try {
        const result = await processItem(item, cwd);

        // Checkpoint: save progress immediately
        progress.completed.push(item.path);
        progress.results.push(result);
        await saveProgress(progress);

        return result;
      } catch (e) {
        await log(`  → Error processing ${item.path}: ${e.message}`);
        const errorResult = { status: 'error', path: item.path, reason: e.message };

        progress.completed.push(item.path);
        progress.results.push(errorResult);
        await saveProgress(progress);

        return errorResult;
      }
    });

    // Combine with existing results from resume
    const allResults = [...existingResults, ...results];

    // Summarize with detailed error breakdown
    const touched = allResults.filter(r => r.status === 'touched').length;
    const updated = allResults.filter(r => r.status === 'updated').length;
    const llmErrors = allResults.filter(r => r.status === 'llm_error');
    const genErrors = allResults.filter(r => r.status === 'gen_error');
    const otherErrors = allResults.filter(r => r.status === 'error');
    const allErrors = [...llmErrors, ...genErrors, ...otherErrors];

    await log(`\nSummary: ${allResults.length} processed`);
    await log(`  ✓ Touched: ${touched} | Updated: ${updated}`);
    if (allErrors.length > 0) {
      await log(`  ✗ LLM errors: ${llmErrors.length} | Gen errors: ${genErrors.length} | Other: ${otherErrors.length}`);
    }

    // Write final result
    const resultData = {
      completedAt: new Date().toISOString(),
      status: 'success',
      processed: allResults.length,
      touched,
      updated,
      failed: allErrors.length,
      llmErrors: llmErrors.length,
      genErrors: genErrors.length,
      failedList: allErrors
    };
    await fs.writeFile(RESULT_FILE, JSON.stringify(resultData, null, 2));
    await log(`Result written to ${RESULT_FILE}`);

    // Clear progress file (task completed)
    await clearProgress();

    await log('Completed');
  } catch (e) {
    await log(`Error: ${e.message}`);

    // Mark progress as crashed but keep for resume
    progress.status = 'crashed';
    progress.error = e.message;
    await saveProgress(progress);
  } finally {
    try {
      await fs.unlink(PID_FILE);
    } catch {}
  }
}

async function startBackground(args) {
  if (await isRunning()) {
    console.log('Already running. Use --status to check progress.');
    return;
  }

  const child = spawn(process.execPath, [
    fileURLToPath(import.meta.url),
    '--daemon',
    ...args.filter(a => a !== '--daemon')
  ], {
    cwd: process.cwd(),
    detached: true,
    stdio: 'ignore'
  });

  child.unref();
  await fs.writeFile(PID_FILE, String(child.pid));

  console.log(`Started background update (PID: ${child.pid})`);
  console.log(`Check progress: node ~/.claude/skills/project-index/scripts/update-bg.js --status`);
}

async function main() {
  const args = process.argv.slice(2);

  if (args.includes('--status')) {
    await showStatus();
    return;
  }

  if (args.includes('--log')) {
    await showLog();
    return;
  }

  if (args.includes('--daemon')) {
    await runDaemon(args);
    return;
  }

  await startBackground(args);
}

main().catch(console.error);
