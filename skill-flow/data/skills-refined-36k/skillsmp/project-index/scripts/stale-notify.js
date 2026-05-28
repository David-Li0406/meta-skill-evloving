#!/usr/bin/env node
/**
 * Stale Notify - Lightweight check for SessionStart hook
 *
 * Logic:
 * - Only notifies when stale count changes by > 3 compared to last check
 * - Prompts AI to invoke skill for details
 *
 * Usage:
 *   node stale-notify.js              # Check and notify if threshold met
 *   node stale-notify.js --enable     # Enable notifications
 *   node stale-notify.js --disable    # Disable notifications
 *   node stale-notify.js --status     # Show current status
 *   node stale-notify.js --reset      # Reset last count to 0
 */

import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';
import {
  readJsonSafe,
  writeJsonSafe,
  unlinkSafe,
  getMtime,
  archiveToHistory,
  CRASH_THRESHOLD_MINUTES
} from './shared.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const STATE_FILE = path.join(__dirname, '.stale-notify-state.json');
const RESULT_FILE = path.join(__dirname, '.update-result.json');
const RESULT_HISTORY = path.join(__dirname, '.update-history.json');
const ANALYZER_RESULT_FILE = path.join(__dirname, '.module-analyzer-result.json');
const ANALYZER_PROGRESS_FILE = path.join(__dirname, '.module-analyzer-progress.json');
const ANALYZER_HISTORY = path.join(__dirname, '.module-analyzer-history.json');
const CHANGE_THRESHOLD = 3;

/**
 * Read notification state
 * @returns {Promise<object>}
 */
async function readState() {
  return await readJsonSafe(STATE_FILE, {
    enabled: true,
    lastCheck: null,
    lastStaleCount: 0
  });
}

/**
 * Write notification state
 * @param {object} state
 * @returns {Promise<void>}
 */
async function writeState(state) {
  await writeJsonSafe(STATE_FILE, state);
}

/**
 * Check if there's a pending result from background task
 * If found, archive it to history and return the result
 * @returns {Promise<object|null>}
 */
async function checkPendingResult() {
  const result = await readJsonSafe(RESULT_FILE, null);
  if (!result) return null;

  await archiveToHistory(RESULT_HISTORY, result);
  await unlinkSafe(RESULT_FILE);
  return result;
}

/**
 * Check if there's a pending result from module-analyzer
 * @returns {Promise<object|null>}
 */
async function checkAnalyzerResult() {
  const result = await readJsonSafe(ANALYZER_RESULT_FILE, null);

  if (result) {
    const mtime = await getMtime(ANALYZER_RESULT_FILE);
    const completedAt = new Date(result.completedAt || mtime);
    const now = new Date();
    const ageHours = (now - completedAt) / (1000 * 60 * 60);

    if (ageHours > 24) {
      await unlinkSafe(ANALYZER_RESULT_FILE);
      return null;
    }

    // Check if already archived
    const history = await readJsonSafe(ANALYZER_HISTORY, []);
    const alreadyArchived = history.some(h => h.completedAt === result.completedAt);
    if (alreadyArchived) {
      await unlinkSafe(ANALYZER_RESULT_FILE);
      return null;
    }

    await archiveToHistory(ANALYZER_HISTORY, result);
    await unlinkSafe(ANALYZER_RESULT_FILE);
    return result;
  }

  // Check for crashed/stale progress
  const progress = await readJsonSafe(ANALYZER_PROGRESS_FILE, null);
  if (!progress || progress.status !== 'running') return null;

  const mtime = await getMtime(ANALYZER_PROGRESS_FILE);
  if (!mtime) return null;

  const staleMinutes = (new Date() - mtime) / (1000 * 60);

  if (staleMinutes > CRASH_THRESHOLD_MINUTES) {
    const completed = progress.completed?.length || 0;
    const total = progress.items?.length || 0;

    return {
      status: 'crashed',
      message: `任务可能已崩溃 (${staleMinutes.toFixed(0)} 分钟无更新)`,
      processed: completed,
      total,
      pending: total - completed,
      canResume: true,
      completedAt: mtime.toISOString()
    };
  }

  return null;
}

async function getStaleData(cwd) {
  try {
    const checkScript = path.join(__dirname, 'check-stale.js');
    const result = execSync(`node "${checkScript}" "${cwd}" --json`, {
      encoding: 'utf-8',
      timeout: 30000,
      cwd
    });
    const data = JSON.parse(result);
    return data.filter(r => r.status === 'stale');
  } catch (e) {
    return [];
  }
}

/**
 * Build a tree structure from stale paths
 * @param {Array} staleItems
 * @returns {object}
 */
function buildTree(staleItems) {
  const tree = {};

  for (const item of staleItems) {
    const parts = item.path.split('/');
    let current = tree;

    for (let i = 0; i < parts.length; i++) {
      const part = parts[i];
      if (!current[part]) {
        current[part] = i === parts.length - 1
          ? { _stale: true, _files: item.changedFiles?.slice(0, 3).map(f => f.path) || [] }
          : {};
      }
      current = current[part];
    }
  }

  return tree;
}

/**
 * Format tree as indented text
 * @param {object} tree
 * @param {string} indent
 * @returns {string}
 */
function formatTree(tree, indent = '') {
  let output = '';
  const entries = Object.entries(tree).filter(([k]) => !k.startsWith('_'));

  for (let i = 0; i < entries.length; i++) {
    const [key, value] = entries[i];
    const isLast = i === entries.length - 1;
    const prefix = isLast ? '└─' : '├─';
    const childIndent = indent + (isLast ? '  ' : '│ ');

    if (value._stale) {
      output += `${indent}${prefix} ${key}/ [STALE]\n`;
      if (value._files?.length > 0) {
        for (const file of value._files) {
          output += `${childIndent}  · ${file}\n`;
        }
      }
    } else {
      output += `${indent}${prefix} ${key}/\n`;
      output += formatTree(value, childIndent);
    }
  }

  return output;
}

async function main() {
  const args = process.argv.slice(2);
  const cwd = process.cwd();

  // Handle commands
  if (args.includes('--enable')) {
    const state = await readState();
    state.enabled = true;
    await writeState(state);
    console.log('✓ Stale notifications enabled');
    return;
  }

  if (args.includes('--disable')) {
    const state = await readState();
    state.enabled = false;
    await writeState(state);
    console.log('✓ Stale notifications disabled');
    return;
  }

  if (args.includes('--reset')) {
    const state = await readState();
    state.lastStaleCount = 0;
    state.lastCheck = null;
    await writeState(state);
    console.log('✓ Stale count reset to 0');
    return;
  }

  if (args.includes('--status')) {
    const state = await readState();
    console.log(`Status: ${state.enabled ? 'enabled' : 'disabled'}`);
    console.log(`Last check: ${state.lastCheck || 'never'}`);
    console.log(`Last stale count: ${state.lastStaleCount}`);
    return;
  }

  const state = await readState();

  // If disabled, skip silently
  if (!state.enabled) {
    return;
  }

  // First, check if there's a pending result from background task
  const pendingResult = await checkPendingResult();
  if (pendingResult) {
    if (pendingResult.status === 'crashed') {
      console.log(`\n[project-index] ⚠️ 后台任务中断`);
      console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
      console.log(`${pendingResult.message}`);
      console.log(`已完成: Touch ${pendingResult.touched || 0} | 更新 ${pendingResult.updated || 0}`);
      console.log(`待处理: ${pendingResult.pending || 0}`);
      if (pendingResult.canResume) {
        console.log(`\n可运行 \`update-bg.js --resume\` 继续任务`);
      }
      console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`);
    } else {
      console.log(`\n[project-index] ✓ 后台更新任务完成`);
      console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
      console.log(`完成时间: ${pendingResult.completedAt || 'unknown'}`);
      console.log(`处理: ${pendingResult.processed || 0} | Touch: ${pendingResult.touched || 0} | 更新: ${pendingResult.updated || 0} | 失败: ${pendingResult.failed || 0}`);
      if (pendingResult.failedList && pendingResult.failedList.length > 0) {
        console.log(`\n失败的模块:`);
        pendingResult.failedList.forEach(m => console.log(`  - ${m.path}: ${m.reason || 'unknown'}`));
      }
      console.log(`\n(结果已归档到历史记录)`);
      console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`);
    }
    // Don't return - continue to check current stale status
  }

  // Check module-analyzer result
  const analyzerResult = await checkAnalyzerResult();
  if (analyzerResult) {
    if (analyzerResult.status === 'crashed') {
      console.log(`\n[project-index] ⚠️ 代码分析任务可能已崩溃`);
      console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
      console.log(`${analyzerResult.message}`);
      console.log(`已完成: ${analyzerResult.processed || 0} / ${analyzerResult.total || 0}`);
      console.log(`待处理: ${analyzerResult.pending || 0}`);
      console.log(`\n是否重新执行? 运行: node ~/.claude/skills/project-index/scripts/module-analyzer.js --daemon`);
      console.log(`或续传: node ~/.claude/skills/project-index/scripts/module-analyzer.js --daemon --resume`);
      console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`);
    } else {
      console.log(`\n[project-index] 🔍 代码分析任务完成`);
      console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
      console.log(`完成时间: ${analyzerResult.completedAt || 'unknown'}`);
      console.log(`处理: ${analyzerResult.processed || 0} 个模块`);

      const byStatus = analyzerResult.byStatus || {};
      const statusParts = [];
      if (byStatus.success) statusParts.push(`成功: ${byStatus.success}`);
      if (byStatus.llm_error) statusParts.push(`LLM错误: ${byStatus.llm_error}`);
      if (byStatus.parse_error) statusParts.push(`解析错误: ${byStatus.parse_error}`);
      if (byStatus.error) statusParts.push(`错误: ${byStatus.error}`);
      if (statusParts.length > 0) {
        console.log(`结果: ${statusParts.join(' | ')}`);
      }

      if (analyzerResult.failedList && analyzerResult.failedList.length > 0) {
        console.log(`\n失败的模块:`);
        analyzerResult.failedList.slice(0, 5).forEach(m =>
          console.log(`  - ${m.id || m.path}: ${m.reason || m.status || 'unknown'}`)
        );
        if (analyzerResult.failedList.length > 5) {
          console.log(`  ... 还有 ${analyzerResult.failedList.length - 5} 个`);
        }
        console.log(`\n重试失败模块: node ~/.claude/skills/project-index/scripts/module-analyzer.js --daemon`);
      }
      console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`);
    }
  }

  // Run check
  const staleItems = await getStaleData(cwd);
  const currentCount = staleItems.length;
  const lastCount = state.lastStaleCount || 0;
  const change = currentCount - lastCount;
  const now = new Date().toISOString();

  // Update state
  await writeState({
    enabled: true,
    lastCheck: now,
    lastStaleCount: currentCount
  });

  // Only notify if change > threshold or first detection
  const shouldNotify = change > CHANGE_THRESHOLD || (currentCount > 0 && lastCount === 0);

  if (shouldNotify) {
    console.log(`\n[project-index] CLAUDE.md 过期检测`);
    console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
    console.log(`状态: ${lastCount} → ${currentCount} (${change >= 0 ? '+' : ''}${change})`);
    console.log(`\n需要更新的模块:\n`);

    const tree = buildTree(staleItems);
    console.log(formatTree(tree));

    console.log(`\n建议: 运行 /project-index 查看完整详情或启动后台更新。`);
    console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`);
  }
  // Otherwise, silent - no significant change
}

main().catch(console.error);
