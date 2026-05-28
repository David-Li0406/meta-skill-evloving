#!/usr/bin/env node

import { execSync, spawn, spawnSync } from 'child_process';
import fs from 'fs';
import os from 'os';
import path from 'path';
import { generateSessionName } from './session-name.js';
import {
  loadOrchestratorState,
  markOrchestratorStarted,
  markOrchestratorStopped,
  getOrchestratorSessionId,
  isOrchestratorSession
} from './orchestrator.js';

const TMUX_SESSION_PREFIX = 'coder-';

const colors = {
  green: '\x1b[32m',
  blue: '\x1b[34m',
  yellow: '\x1b[33m',
  red: '\x1b[31m',
  reset: '\x1b[0m'
};

function log(msg, color = 'reset') {
  console.log(`${colors[color]}${msg}${colors.reset}`);
}

function getTimeAgo(timestamp) {
  const seconds = Math.floor((Date.now() - timestamp) / 1000);
  if (seconds < 60) return `${seconds}s ago`;
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}

function getGitRoot() {
  try {
    return execSync('git rev-parse --show-toplevel', { encoding: 'utf8' }).trim();
  } catch {
    return process.cwd();
  }
}

/**
 * Check if zoxide is installed on the system
 */
function isZoxideAvailable() {
  try {
    execSync('which zoxide', { encoding: 'utf8', stdio: 'pipe' });
    return true;
  } catch {
    return false;
  }
}

/**
 * Resolve a path using zoxide if available, otherwise return the path as-is
 * @param {string} pathArg - The path argument (could be partial like "vega")
 * @returns {{ resolved: string, method: 'zoxide' | 'direct' } | null} - Resolved path info or null if resolution failed
 */
function resolvePathWithZoxide(pathArg) {
  // First, check if it's already a valid absolute or relative path
  const directPath = path.isAbsolute(pathArg)
    ? pathArg
    : path.resolve(process.cwd(), pathArg);

  if (fs.existsSync(directPath) && fs.statSync(directPath).isDirectory()) {
    return { resolved: directPath, method: 'direct' };
  }

  // Try zoxide if available
  if (isZoxideAvailable()) {
    try {
      const zoxidePath = execSync(`zoxide query "${pathArg}"`, {
        encoding: 'utf8',
        stdio: ['pipe', 'pipe', 'pipe']
      }).trim();

      if (zoxidePath && fs.existsSync(zoxidePath) && fs.statSync(zoxidePath).isDirectory()) {
        return { resolved: zoxidePath, method: 'zoxide' };
      }
    } catch {
      // zoxide query failed (no match found)
    }
  }

  return null;
}

/**
 * Validate that a path exists and is a directory
 * @param {string} resolvedPath - The path to validate
 * @returns {{ valid: boolean, error?: string }}
 */
function validatePath(resolvedPath) {
  if (!fs.existsSync(resolvedPath)) {
    return { valid: false, error: `Path does not exist: ${resolvedPath}` };
  }

  const stats = fs.statSync(resolvedPath);
  if (!stats.isDirectory()) {
    return { valid: false, error: `Path is not a directory: ${resolvedPath}` };
  }

  return { valid: true };
}

function createWorktree(branchName, baseBranch = 'main') {
  const gitRoot = getGitRoot();
  const worktreePath = path.join(gitRoot, '../worktrees', branchName);
  
  log(`Creating worktree at ${worktreePath}...`, 'blue');
  
  try {
    fs.mkdirSync(path.dirname(worktreePath), { recursive: true });
    execSync(`git worktree add -b ${branchName} ${worktreePath} ${baseBranch}`, { cwd: gitRoot });
    log(`✅ Worktree created: ${worktreePath}`, 'green');
    return worktreePath;
  } catch (e) {
    log(`⚠️  Worktree exists or failed: ${e.message}`, 'yellow');
    return worktreePath;
  }
}

function readFileContent(filePath) {
  try {
    const absPath = path.isAbsolute(filePath) 
      ? filePath 
      : path.join(getGitRoot(), filePath);
    return fs.readFileSync(absPath, 'utf8');
  } catch (e) {
    return null;
  }
}

function generateInitialPrompt(tool, taskDescription, contextFiles = []) {
  let prompt = `TASK: ${taskDescription}\n\n`;

  if (contextFiles.length > 0) {
    prompt += 'CONTEXT FILES:\n';
    contextFiles.forEach(file => {
      const content = readFileContent(file);
      if (content) {
        prompt += `\n--- ${file} ---\n${content}\n`;
      }
    });
    prompt += '\n';
  }

  prompt += '\nYou have full permissions. Complete the task.';
  prompt += '\n\n⚠️  IMPORTANT: When you finish this task, you MUST publish a completion promise.';

  // Different promise instructions based on tool
  if (tool === 'codex' || tool === 'openai-codex') {
    // Codex exec mode: use bash command
    prompt += '\nRun this shell command: coders promise "Brief summary of what you accomplished"';
    prompt += '\n\nThis notifies the orchestrator and dashboard that your work is complete.';
    prompt += '\nIf you get blocked, use: coders promise "Reason for being blocked" --status blocked';
  } else {
    // Claude and other interactive tools: use skill command
    prompt += '\n/coders:promise "Brief summary of what you accomplished"';
    prompt += '\n\nThis notifies the orchestrator and dashboard that your work is complete.';
    prompt += '\nIf you get blocked, use: /coders:promise "Reason for being blocked" --status blocked';
  }

  return prompt;
}

/**
 * Process names to detect for each CLI tool
 */
const CLI_PROCESS_NAMES = {
  'claude': 'claude',
  'claude-code': 'claude',
  'gemini': 'gemini',
  'codex': 'codex',
  'opencode': 'opencode',
  'open-code': 'opencode'
};

/**
 * Wait for the CLI to be ready by detecting the tool process running in the tmux pane
 * @param {string} sessionId - The tmux session ID
 * @param {string} tool - The CLI tool name
 * @param {number} timeoutMs - Timeout in milliseconds (default: 30000)
 * @param {number} pollIntervalMs - Polling interval in milliseconds (default: 500)
 * @returns {Promise<boolean>} - True if CLI is ready, false if timeout
 */
async function waitForCliReady(sessionId, tool, timeoutMs = 30000, pollIntervalMs = 500) {
  const processName = CLI_PROCESS_NAMES[tool] || tool;
  const startTime = Date.now();

  log(`⏳ Waiting for ${tool} process to start...`, 'blue');

  while (Date.now() - startTime < timeoutMs) {
    try {
      // Get the pane PID from tmux
      const panePid = execSync(`tmux display-message -t "${sessionId}" -p '#{pane_pid}'`, {
        encoding: 'utf8',
        timeout: 5000
      }).trim();

      if (panePid) {
        // Check if the tool process is running as a child of the pane
        const children = execSync(`pgrep -P ${panePid} 2>/dev/null || true`, {
          encoding: 'utf8',
          timeout: 5000
        }).trim();

        if (children) {
          // Get process names of children to verify the right tool is running
          const childPids = children.split('\n').filter(Boolean);
          for (const childPid of childPids) {
            try {
              const procName = execSync(`ps -p ${childPid} -o comm= 2>/dev/null || true`, {
                encoding: 'utf8',
                timeout: 5000
              }).trim();

              if (procName && procName.includes(processName)) {
                return true;
              }
            } catch {
              // Process may have exited, continue checking
            }
          }
        }
      }
    } catch {
      // Session might not be ready yet, continue polling
    }

    // Wait before next poll
    await new Promise(resolve => setTimeout(resolve, pollIntervalMs));
  }

  return false;
}

function buildSpawnCommand(tool, promptFile, prompt, extraEnv = {}, model = null) {
  let cmd;
  // Escape single quotes in prompt for shell safety
  const escapedPrompt = prompt.replace(/'/g, "'\\''");

  // Build environment variable string
  const envStr = Object.entries(extraEnv)
    .filter(([_, v]) => v !== undefined && v !== null)
    .map(([k, v]) => `${k}="${v}"`)
    .join(' ');
  const envPrefix = envStr ? envStr + ' ' : '';
  const modelArg = model ? ` --model "${model}"` : '';

  if (tool === 'claude' || tool === 'claude-code') {
    // Claude stays interactive by default - pass prompt via stdin
    // Add --dangerously-skip-permissions to auto-approve file operations
    cmd = `${envPrefix}claude --dangerously-skip-permissions${modelArg} < "${promptFile}"`;
  } else if (tool === 'gemini') {
    // Gemini: use --prompt-interactive with the prompt text to execute and stay interactive
    cmd = `${envPrefix}gemini --yolo${modelArg} --prompt-interactive '${escapedPrompt}'`;
  } else if (tool === 'codex' || tool === 'openai-codex') {
    // Codex: use exec for non-interactive mode, pass prompt via stdin
    cmd = `${envPrefix}codex exec --dangerously-bypass-approvals-and-sandbox${modelArg} < "${promptFile}"`;
  } else if (tool === 'opencode' || tool === 'open-code') {
    // OpenCode: pass prompt via stdin like Claude
    cmd = `${envPrefix}opencode${modelArg} < "${promptFile}"`;
  }

  return cmd;
}

async function spawnInNewTmuxWindow(tool, worktreePath, prompt, sessionName, enableHeartbeat = false, parentSessionId = null, customCwd = null, model = null) {
  const sessionId = `${TMUX_SESSION_PREFIX}${sessionName}`;
  const promptFile = `/tmp/coders-prompt-${Date.now()}.txt`;
  fs.writeFileSync(promptFile, prompt);

  // Auto-detect parent session if running inside a coder session
  const effectiveParentSessionId = parentSessionId || process.env.CODERS_SESSION_ID || null;

  // Determine the effective working directory: customCwd > worktreePath > process.cwd()
  const effectiveCwd = customCwd || worktreePath || process.cwd();

  // Get the user's shell from the environment (e.g., fish, zsh, bash)
  const userShell = process.env.SHELL || '/bin/bash';

  const cmd = buildSpawnCommand(tool, promptFile, prompt, {
    WORKSPACE_DIR: effectiveCwd,
    CODERS_SESSION_ID: sessionId,
    CODERS_PARENT_SESSION_ID: effectiveParentSessionId
    // TEMP DISABLED: CODERS_TASK_DESC causing shell escaping issues in tmux command
    // CODERS_TASK_DESC: prompt.split('\n')[0].replace('TASK: ', '')
  }, model);

  log(`Creating NEW tmux window for: ${sessionId}`, 'blue');

  // Kill existing session if it exists
  try {
    execSync(`tmux kill-session -t ${sessionId} 2>/dev/null`);
  } catch {}

  // Create new session (this opens a WINDOW)
  // Use shell command that keeps session alive after codex exits
  // Use the user's shell explicitly instead of relying on $SHELL expansion
  const fullCmd = `tmux new-session -s "${sessionId}" -d "cd ${effectiveCwd}; ${cmd}; exec ${userShell}"`;

  try {
    execSync(fullCmd);
    log(`✅ Created tmux session: ${sessionId}`, 'green');

    // Wait for the CLI process to be ready before returning
    const cliReady = await waitForCliReady(sessionId, tool);
    if (cliReady) {
      log(`✅ ${tool} process is running`, 'green');
    } else {
      log(`⚠️  Timeout waiting for ${tool} process (session created but process may still be starting)`, 'yellow');
    }

    // Start heartbeat in background if enabled
    if (enableHeartbeat) {
      // Check if redis is available before starting heartbeat
      if (!checkRedisDependency()) {
        log(`⚠️  Heartbeat requires redis dependency.`, 'yellow');
        log(`   Run 'coders dashboard' to auto-install dependencies.`, 'yellow');
      } else {
        try {
          const scriptDir = path.dirname(new URL(import.meta.url).pathname);
          const heartbeatScript = path.join(scriptDir, '../../assets/heartbeat.js');
          const taskDesc = prompt.split('\n')[0].replace('TASK: ', '');
          const heartbeatEnv = [
            `SESSION_ID="${sessionId}"`,
            `CODERS_PARENT_SESSION_ID="${effectiveParentSessionId || ''}"`,
            `CODERS_TASK_DESC="${taskDesc.replace(/"/g, '\\"')}"`
          ].join(' ');
          execSync(`${heartbeatEnv} nohup node ${heartbeatScript} "${sessionId}" > /dev/null 2>&1 &`);
          log(`💓 Heartbeat enabled (dashboard will show status)`, 'green');
        } catch (e) {
          log(`⚠️  Heartbeat failed to start: ${e.message}`, 'yellow');
        }
      }
    }

    log(`💡 Attach: coders attach ${sessionName}`, 'yellow');
    log(`💡 Or: tmux attach -t ${sessionId}`, 'yellow');
  } catch (e) {
    log(`❌ Failed: ${e.message}`, 'red');
  }
}

function spawnInITerm(tool, worktreePath, prompt, sessionName, model = null) {
  const cmd = buildSpawnCommand(tool, `/tmp/coders-prompt-${Date.now()}.txt`, { WORKSPACE_DIR: worktreePath }, model);
  fs.writeFileSync(`/tmp/coders-prompt-${Date.now()}.txt`, prompt);
  
  log(`Creating NEW iTerm2 window for: ${sessionName}`, 'blue');
  
  // AppleScript to open new iTerm2 window with command
  const applescript = `
    tell application "iTerm2"
      create window with profile "Default"
      tell current session of first window
        write text "${cmd.replace(/"/g, '\\"')}"
      end tell
    end tell
  `;
  
  try {
    execSync(`osascript -e '${applescript}'`);
    log(`✅ Created iTerm2 window!`, 'green');
  } catch (e) {
    log(`❌ iTerm2 not available: ${e.message}`, 'red');
  }
}

function listSessions() {
  try {
    const sessions = execSync('tmux list-sessions 2>/dev/null || echo "No tmux sessions"')
      .toString()
      .split('\n')
      .filter(s => s.includes(TMUX_SESSION_PREFIX));
    
    if (sessions.length === 0) {
      log('No coder sessions found.', 'yellow');
    } else {
      log('\n📋 Active Coder Sessions:\n', 'blue');
      sessions.forEach(s => console.log(s));
    }
  } catch {
    log('tmux not available', 'yellow');
  }
}

function attachSession(sessionName) {
  const fullName = `${TMUX_SESSION_PREFIX}${sessionName}`;
  
  if (process.env.TERM_PROGRAM === 'iTerm.app') {
    // Open iTerm and attach to tmux session
    const applescript = `
      tell application "iTerm2"
        create window with profile "Default"
        tell current session of first window
          write text "tmux attach-session -t ${fullName}"
        end tell
      end tell
    `;
    try {
      execSync(`osascript -e '${applescript}'`);
    } catch {
      execSync(`tmux attach-session -t ${fullName}`);
    }
  } else {
    execSync(`tmux attach-session -t ${fullName}`);
  }
}

function killSession(sessionName) {
  const fullName = `${TMUX_SESSION_PREFIX}${sessionName}`;
  const tmuxSocket = resolveTmuxSocketFromEnv();

  // Kill associated heartbeat process first
  try {
    execSync(`pkill -f "heartbeat.js.*${fullName}"`);
  } catch {} // May not exist

  // Kill process tree for the tmux session to avoid orphaned CLI processes
  try {
    const panePids = listTmuxPanePids(fullName, tmuxSocket);
    if (panePids.length > 0) {
      const { children } = getProcessTable();
      const tree = collectDescendants(panePids, children);
      killPidList([...tree], 'TERM');
      sleepMs(300);
      const remaining = filterExistingPids(tree);
      if (remaining.length > 0) {
        killPidList(remaining, 'KILL');
      }
    }
  } catch {}

  try {
    execSync(`tmux kill-session -t ${fullName}`);
    log(`✅ Killed session: ${fullName}`, 'green');
  } catch (e) {
    log(`❌ Failed: ${e.message}`, 'red');
  }
}

function listTmuxPanePids(sessionName = null, tmuxSocket = null) {
  try {
    const socketArg = tmuxSocket ? `-S "${tmuxSocket}"` : '';
    const target = sessionName ? `-t "${sessionName}"` : '-a';
    const output = execSync(`tmux ${socketArg} list-panes ${target} -F "#{pane_pid}" 2>/dev/null`, {
      encoding: 'utf8'
    });
    return output
      .split('\n')
      .map((s) => s.trim())
      .filter(Boolean)
      .map((s) => Number(s))
      .filter((n) => !Number.isNaN(n));
  } catch {
    return [];
  }
}

function getProcessTable() {
  const output = execSync('ps -axo pid=,ppid=,command=', { encoding: 'utf8' });
  const children = new Map();
  const commands = new Map();

  output
    .split('\n')
    .map((line) => line.trim())
    .filter(Boolean)
    .forEach((line) => {
      const match = line.match(/^(\d+)\s+(\d+)\s+(.*)$/);
      if (!match) return;
      const pid = Number(match[1]);
      const ppid = Number(match[2]);
      const cmd = match[3];
      commands.set(pid, cmd);
      if (!children.has(ppid)) {
        children.set(ppid, []);
      }
      children.get(ppid).push(pid);
    });

  return { children, commands };
}

function collectDescendants(rootPids, children) {
  const visited = new Set();
  const stack = [...rootPids];
  while (stack.length > 0) {
    const pid = stack.pop();
    if (visited.has(pid)) continue;
    visited.add(pid);
    const kids = children.get(pid);
    if (kids && kids.length > 0) {
      kids.forEach((child) => stack.push(child));
    }
  }
  return visited;
}

function killPidList(pids, signal = 'TERM') {
  if (!pids || pids.length === 0) return;
  const chunkSize = 100;
  for (let i = 0; i < pids.length; i += chunkSize) {
    const chunk = pids.slice(i, i + chunkSize);
    try {
      execSync(`kill -${signal} ${chunk.join(' ')}`);
    } catch {}
  }
}

function filterExistingPids(pids) {
  if (!pids || pids.size === 0) return [];
  const output = execSync('ps -axo pid=', { encoding: 'utf8' });
  const live = new Set(
    output
      .split('\n')
      .map((line) => line.trim())
      .filter(Boolean)
      .map((pid) => Number(pid))
  );
  const remaining = [];
  for (const pid of pids) {
    if (live.has(pid)) remaining.push(pid);
  }
  return remaining;
}

function sleepMs(ms) {
  try {
    const seconds = Math.max(ms / 1000, 0.001);
    execSync(`sleep ${seconds}`);
  } catch {}
}

function resolveTmuxSocketFromEnv() {
  if (process.env.CODERS_TMUX_SOCKET) {
    return process.env.CODERS_TMUX_SOCKET;
  }
  if (!process.env.TMUX) return null;
  const raw = process.env.TMUX;
  const commaIndex = raw.indexOf(',');
  if (commaIndex === -1) return null;
  return raw.slice(0, commaIndex);
}

function resolveTmuxSocketFromArgs(args) {
  for (let i = 1; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--tmux-socket' && args[i + 1]) {
      return args[i + 1];
    }
    if (arg.startsWith('--tmux-socket=')) {
      return arg.split('=')[1] || null;
    }
  }
  return null;
}

function isTmuxAvailable(tmuxSocket = null) {
  try {
    const socketArg = tmuxSocket ? `-S "${tmuxSocket}"` : '';
    execSync(`tmux ${socketArg} list-sessions 2>/dev/null`, { encoding: 'utf8' });
    return true;
  } catch {
    return false;
  }
}

function isTargetOrphan(cmd, includeClaude, includeHeartbeat) {
  if (includeClaude && /\bclaude\b/.test(cmd)) return true;
  if (includeHeartbeat && cmd.includes('heartbeat.js')) return true;
  return false;
}

function pruneOrphaned(args) {
  let dryRun = true;
  let includeClaude = true;
  let includeHeartbeat = true;
  let allowEmptyTmux = false;

  for (let i = 1; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--force' || arg === '--kill') {
      dryRun = false;
    } else if (arg === '--dry-run') {
      dryRun = true;
    } else if (arg === '--no-claude') {
      includeClaude = false;
    } else if (arg === '--no-heartbeat') {
      includeHeartbeat = false;
    } else if (arg === '--allow-empty-tmux') {
      allowEmptyTmux = true;
    }
  }

  const tmuxSocket = resolveTmuxSocketFromArgs(args) || resolveTmuxSocketFromEnv();
  const tmuxAvailable = isTmuxAvailable(tmuxSocket);
  const panePids = tmuxAvailable ? listTmuxPanePids(null, tmuxSocket) : [];

  if (!tmuxAvailable) {
    log('⚠️  tmux server not available for the current socket.', 'yellow');
    if (!dryRun && !allowEmptyTmux) {
      log('Refusing to terminate processes without tmux visibility.', 'yellow');
      log('Tip: re-run with --tmux-socket <path> or --allow-empty-tmux if you are sure.', 'yellow');
      return;
    }
  } else if (panePids.length === 0) {
    log('⚠️  No tmux panes found for the current socket.', 'yellow');
    if (!dryRun && !allowEmptyTmux) {
      log('Refusing to terminate processes without tmux visibility.', 'yellow');
      log('Tip: re-run with --tmux-socket <path> or --allow-empty-tmux if you are sure.', 'yellow');
      return;
    }
  }

  const { children, commands } = getProcessTable();
  const inTmux = collectDescendants(panePids, children);
  const orphans = [];

  for (const [pid, cmd] of commands.entries()) {
    if (!isTargetOrphan(cmd, includeClaude, includeHeartbeat)) continue;
    if (!inTmux.has(pid)) {
      orphans.push({ pid, cmd });
    }
  }

  if (orphans.length === 0) {
    log('✅ No orphaned processes found.', 'green');
    return;
  }

  log(`⚠️  Found ${orphans.length} orphaned process(es):`, 'yellow');
  orphans.forEach((p) => console.log(`${p.pid}\t${p.cmd}`));

  if (dryRun) {
    log(`Dry run only. Re-run with --force to terminate them.`, 'yellow');
    return;
  }

  const orphanPids = orphans.map((p) => p.pid);
  killPidList(orphanPids, 'TERM');
  sleepMs(300);
  const remaining = filterExistingPids(new Set(orphanPids));
  if (remaining.length > 0) {
    killPidList(remaining, 'KILL');
  }
  log(`✅ Terminated ${orphans.length} orphaned process(es).`, 'green');
}

/**
 * Get list of active coder sessions (tmux sessions with the coder- prefix)
 * @returns {string[]} Array of session names (without the coder- prefix)
 */
function getActiveCoderSessions() {
  try {
    const output = execSync('tmux list-sessions -F "#{session_name}" 2>/dev/null || echo ""', { encoding: 'utf8' });
    return output
      .split('\n')
      .filter(s => s.startsWith(TMUX_SESSION_PREFIX))
      .map(s => s.trim());
  } catch {
    return [];
  }
}

/**
 * Send a plugin update command to all active coder sessions
 * @param {string} pluginName - Name of the plugin to update (default: 'coders')
 */
function updatePluginInSessions(pluginName = 'coders') {
  const sessions = getActiveCoderSessions();

  if (sessions.length === 0) {
    log('No active coder sessions found.', 'yellow');
    return;
  }

  log(`\n📦 Broadcasting plugin update to ${sessions.length} session(s)...\n`, 'blue');

  const updated = [];
  const failed = [];

  for (const sessionId of sessions) {
    try {
      // Send the /plugin update command followed by Enter key
      const command = `/plugin update ${pluginName}`;
      execSync(`tmux send-keys -t "${sessionId}" '${command}' Enter`, { encoding: 'utf8' });
      updated.push(sessionId);
      log(`  ✅ ${sessionId}`, 'green');
    } catch (e) {
      failed.push({ sessionId, error: e.message });
      log(`  ❌ ${sessionId}: ${e.message}`, 'red');
    }
  }

  log('', 'reset');

  if (updated.length > 0) {
    log(`✅ Successfully sent update command to ${updated.length} session(s)`, 'green');
  }

  if (failed.length > 0) {
    log(`⚠️  Failed to update ${failed.length} session(s)`, 'yellow');
  }

  // Show short session names for convenience
  if (updated.length > 0) {
    const shortNames = updated.map(s => s.replace(TMUX_SESSION_PREFIX, ''));
    log(`\n📋 Updated sessions: ${shortNames.join(', ')}`, 'blue');
  }
}

async function startOrAttachOrchestrator() {
  const sessionId = getOrchestratorSessionId();

  // Check if orchestrator session already exists
  try {
    const sessions = execSync('tmux list-sessions 2>/dev/null || echo ""', { encoding: 'utf8' });
    const exists = sessions.includes(sessionId);

    if (exists) {
      log(`Orchestrator session already exists, attaching...`, 'blue');
      try {
        execSync(`tmux attach-session -t ${sessionId}`, { stdio: 'inherit' });
      } catch (e) {
        log(`Failed to attach: ${e.message}`, 'red');
      }
      return;
    }
  } catch (e) {
    // tmux might not be available
  }

  // Create new orchestrator session
  log(`Creating orchestrator session: ${sessionId}`, 'blue');

  const orchestratorPrompt = `
╔════════════════════════════════════════════════════════════════════════════╗
║                      CODER ORCHESTRATOR SESSION                            ║
║                                                                            ║
║  This is a special persistent session for coordinating other coder        ║
║  sessions. You can use the following commands:                            ║
║                                                                            ║
║  - coders spawn <tool> [options]  : Spawn a new coder session             ║
║  - coders list                    : List all active sessions               ║
║  - coders promises                : Check completion status of sessions    ║
║  - coders attach <session>        : Attach to a session                    ║
║  - coders kill <session>          : Kill a session                         ║
║  - coders dashboard               : Open the dashboard                     ║
║                                                                            ║
║  Use Claude Code to orchestrate your AI coding sessions!                  ║
╚════════════════════════════════════════════════════════════════════════════╝

Welcome to the Orchestrator session. You have full permissions to spawn and manage
other coder sessions. Start by spawning your first session or listing existing ones.

📌 TIP: Use 'coders promises' to see which spawned sessions have completed their tasks.
`;

  const promptFile = `/tmp/coders-orchestrator-prompt.txt`;
  fs.writeFileSync(promptFile, orchestratorPrompt);

  // Spawn orchestrator with Claude Code
  // Get the user's shell from the environment (e.g., fish, zsh, bash)
  const userShell = process.env.SHELL || '/bin/bash';
  const cmd = `claude --dangerously-skip-permissions < "${promptFile}"`;
  const fullCmd = `tmux new-session -s "${sessionId}" -d "cd ${process.cwd()}; ${cmd}; exec ${userShell}"`;

  try {
    execSync(fullCmd);
    await markOrchestratorStarted();
    log(`✅ Created orchestrator session: ${sessionId}`, 'green');
    log(`💡 Attach: coders orchestrator`, 'yellow');
    log(`💡 Or: tmux attach -t ${sessionId}`, 'yellow');

    // Start heartbeat for orchestrator
    if (!checkRedisDependency()) {
      log(`⚠️  Heartbeat requires redis dependency.`, 'yellow');
      log(`   Run 'coders dashboard' to auto-install dependencies.`, 'yellow');
    } else {
      try {
        const scriptDir = path.dirname(new URL(import.meta.url).pathname);
        const heartbeatScript = path.join(scriptDir, '../../assets/heartbeat.js');
        execSync(`SESSION_ID="${sessionId}" nohup node ${heartbeatScript} "${sessionId}" > /dev/null 2>&1 &`);
        log(`💓 Heartbeat enabled for orchestrator`, 'green');
      } catch (e) {
        log(`⚠️  Heartbeat failed to start: ${e.message}`, 'yellow');
      }
    }

    // Auto-attach to the new session only if running in a TTY
    if (process.stdout.isTTY) {
      setTimeout(() => {
        try {
          execSync(`tmux attach-session -t ${sessionId}`, { stdio: 'inherit' });
        } catch (e) {
          log(`Failed to attach: ${e.message}`, 'red');
        }
      }, 500);
    }
  } catch (e) {
    log(`❌ Failed to create orchestrator: ${e.message}`, 'red');
  }
}

function usage() {
  console.log(`
${colors.blue}🤖 Coder Spawner - Spawn AI coding assistants in NEW tmux windows${colors.reset}

${colors.green}Usage:${colors.reset}
  coders spawn <tool> [options]
  coders orchestrator
  coders tui
  coders list
  coders attach <session>
  coders kill <session>
  coders prune [--force] [--no-heartbeat] [--no-claude] [--tmux-socket <path>] [--allow-empty-tmux]
  coders promise "summary" [--status <status>] [--blockers "reason"]
  coders resume [session-name]
  coders dashboard
  coders restart-dashboard
  coders update-plugin [--plugin <name>]
  coders help

${colors.green}Tools:${colors.reset}
  claude    - Anthropic Claude Code CLI
  gemini    - Google Gemini CLI
  codex     - OpenAI Codex CLI
  opencode  - OpenCode CLI

${colors.green}Orchestrator:${colors.reset}
  coders orchestrator    - Start/attach to the orchestrator session
                          (persistent session for coordinating other coders)

${colors.green}TUI:${colors.reset}
  coders tui             - Open the terminal UI for managing sessions
                          (spawns in its own tmux session: coders-tui)

${colors.green}Promise/Resume:${colors.reset}
  coders promise "summary"      - Mark session as completed with a summary
    --status <status>           Status: completed (default), blocked, needs-review
    --blockers "reason"         Reason for being blocked
  coders resume [session-name]  - Resume a completed session (make active again)

${colors.green}Cleanup:${colors.reset}
  coders prune                 - List orphaned Claude/heartbeat processes
    --force                    Terminate orphans (otherwise dry-run)
    --no-heartbeat             Skip heartbeat.js processes
    --no-claude                Skip claude processes
    --tmux-socket <path>       Use a specific tmux socket
    --allow-empty-tmux         Allow prune even if tmux panes are not visible

${colors.green}Plugin Update:${colors.reset}
  coders update-plugin   - Broadcast '/plugin update' to all active sessions
    --plugin <name>      Plugin name to update (default: coders)

${colors.green}Options:${colors.reset}
  --name <name>          Session name (auto-generated if omitted)
  --model <model>        Model identifier to pass to the tool CLI
  --worktree <branch>    Create git worktree for this branch
  --base <branch>        Base branch for worktree (default: main)
  --prd <file>           Read PRD/spec file and prime the AI
  --spec <file>          Alias for --prd
  --task <description>   Task description
  --cwd <path>           Working directory for the session (default: git root)
  --dir <path>           Alias for --cwd
  --no-heartbeat         Disable heartbeat tracking (enabled by default)

${colors.green}Examples:${colors.reset}
  coders orchestrator
  coders spawn claude --worktree feature/auth --prd docs/prd.md
  coders spawn gemini --name my-session --task "Fix the login bug"
  coders spawn claude --model claude-3-5-sonnet --task "Review the PR"
  coders spawn claude --cwd ~/projects/myapp --task "Refactor the API"
  coders list
  coders attach feature-auth
  coders kill feature-auth
  coders prune --force
  coders dashboard
  coders restart-dashboard
  coders update-plugin
  coders update-plugin --plugin beads

${colors.green}How it works:${colors.reset}
  1. Creates NEW tmux window (visible!)
  2. Runs Claude/Gemini/Codex in it
  3. Attach with: coders attach <name>
`);
}

async function isDashboardRunning(port) {
  try {
    const response = await fetch(`http://localhost:${port}/api/sessions`);
    return response.ok;
  } catch {
    return false;
  }
}

async function waitForDashboard(port, timeoutMs = 5000) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    if (await isDashboardRunning(port)) return true;
    await new Promise(resolve => setTimeout(resolve, 250));
  }
  return false;
}

function startDashboardServer(port) {
  const scriptDir = path.dirname(new URL(import.meta.url).pathname);
  const dashboardScript = path.join(scriptDir, '../../assets/dashboard-server.js');
  const logPath = path.join(os.tmpdir(), 'coders-dashboard.log');
  const logHandle = fs.openSync(logPath, 'a');

  const child = spawn('node', [dashboardScript], {
    detached: true,
    stdio: ['ignore', logHandle, logHandle],
    env: { ...process.env, DASHBOARD_PORT: String(port) }
  });
  child.unref();
  return logPath;
}

function openDashboard(url) {
  try {
    if (process.platform === 'darwin') {
      execSync(`open "${url}"`);
    } else if (process.platform === 'win32') {
      execSync(`start "" "${url}"`, { shell: 'cmd.exe' });
    } else {
      execSync(`xdg-open "${url}"`);
    }
  } catch (e) {
    log(`⚠️  Failed to open browser: ${e.message}`, 'yellow');
    log(`Open manually: ${url}`, 'yellow');
  }
}

function checkRedisDependency() {
  try {
    // Get plugin root directory and check if redis exists in node_modules
    const scriptDir = path.dirname(new URL(import.meta.url).pathname);
    const pluginRoot = path.resolve(scriptDir, '../../..');
    const redisPath = path.join(pluginRoot, 'node_modules', 'redis');

    return fs.existsSync(redisPath);
  } catch {
    return false;
  }
}

async function ensureDependencies() {
  // Check if redis is installed
  if (checkRedisDependency()) {
    return true;
  }

  log(`📦 Redis dependency not found. Installing dependencies...`, 'yellow');

  // Get plugin root directory (go up from scripts/ -> coders/ -> skills/ -> root)
  const scriptDir = path.dirname(new URL(import.meta.url).pathname);
  const pluginRoot = path.resolve(scriptDir, '../../..');

  try {
    log(`   Running npm install in ${pluginRoot}...`, 'blue');
    execSync('npm install', {
      cwd: pluginRoot,
      stdio: 'inherit'
    });

    log(`✅ Dependencies installed successfully!`, 'green');
    return true;
  } catch (e) {
    log(`❌ Failed to install dependencies: ${e.message}`, 'red');
    log(`   Please run 'npm install' manually in: ${pluginRoot}`, 'yellow');
    return false;
  }
}

async function launchDashboard() {
  // Ensure dependencies are installed before starting dashboard
  const depsOk = await ensureDependencies();
  if (!depsOk) {
    log(`❌ Cannot start dashboard without dependencies.`, 'red');
    return;
  }

  const port = process.env.DASHBOARD_PORT || '3030';
  const url = `http://localhost:${port}`;

  if (!(await isDashboardRunning(port))) {
    const logPath = startDashboardServer(port);
    const started = await waitForDashboard(port);
    if (started) {
      log(`✅ Dashboard server started on ${url}`, 'green');
      log(`📝 Logs: ${logPath}`, 'yellow');
    } else {
      log(`⚠️  Dashboard server may not have started yet.`, 'yellow');
      log(`📝 Logs: ${logPath}`, 'yellow');
    }
  } else {
    log(`✅ Dashboard already running on ${url}`, 'green');
  }

  openDashboard(url);
}

function killDashboardServer() {
  try {
    // Find and kill the dashboard server process
    const scriptDir = path.dirname(new URL(import.meta.url).pathname);
    const dashboardScript = path.join(scriptDir, '../../assets/dashboard-server.js');

    // Kill by script name pattern
    execSync(`pkill -f "node.*dashboard-server.js" 2>/dev/null || true`, { encoding: 'utf8' });
    log(`✅ Stopped existing dashboard server`, 'green');
    return true;
  } catch (e) {
    // pkill returns non-zero if no processes matched, which is fine
    return true;
  }
}

async function restartDashboard() {
  log(`🔄 Restarting dashboard server...`, 'blue');

  // Kill existing dashboard
  killDashboardServer();

  // Wait a moment for the port to be released
  await new Promise(resolve => setTimeout(resolve, 500));

  // Ensure dependencies are installed before starting dashboard
  const depsOk = await ensureDependencies();
  if (!depsOk) {
    log(`❌ Cannot start dashboard without dependencies.`, 'red');
    return;
  }

  const port = process.env.DASHBOARD_PORT || '3030';
  const url = `http://localhost:${port}`;

  // Start fresh dashboard
  const logPath = startDashboardServer(port);
  const started = await waitForDashboard(port);

  if (started) {
    log(`✅ Dashboard server restarted on ${url}`, 'green');
    log(`📝 Logs: ${logPath}`, 'yellow');
    openDashboard(url);
  } else {
    log(`⚠️  Dashboard server may not have started yet.`, 'yellow');
    log(`📝 Check logs: ${logPath}`, 'yellow');
  }
}

function launchTui() {
  const scriptDir = path.dirname(new URL(import.meta.url).pathname);

  // 1. Check for local development paths first (monorepo dev mode)
  const tuiDevPath = path.resolve(scriptDir, '../../../../tui/src/cli.tsx');
  const tuiBuiltPath = path.resolve(scriptDir, '../../../../tui/dist/cli.js');

  if (fs.existsSync(tuiBuiltPath)) {
    log(`🖥️  Launching TUI...`, 'blue');
    runTui('node', tuiBuiltPath);
    return;
  }

  if (fs.existsSync(tuiDevPath)) {
    log(`📦 Using development mode (tsx)`, 'yellow');
    runTui('tsx', tuiDevPath);
    return;
  }

  // 2. Check cache directory for installed TUI
  const cacheDir = path.join(os.homedir(), '.cache', 'coders-tui');
  const cachedTui = path.join(cacheDir, 'node_modules', '@jayphen', 'coders-tui', 'dist', 'cli.js');

  if (fs.existsSync(cachedTui)) {
    log(`🖥️  Launching TUI...`, 'blue');
    runTui('node', cachedTui);
    return;
  }

  // 3. Install TUI on first use
  log(`📦 Installing TUI (first time only)...`, 'yellow');

  try {
    fs.mkdirSync(cacheDir, { recursive: true });

    execSync('npm install @jayphen/coders-tui@latest', {
      cwd: cacheDir,
      stdio: 'inherit'
    });

    if (fs.existsSync(cachedTui)) {
      log(`🖥️  Launching TUI...`, 'blue');
      runTui('node', cachedTui);
    } else {
      log(`❌ TUI installation failed - cli.js not found`, 'red');
    }
  } catch (e) {
    log(`❌ Failed to install TUI: ${e.message}`, 'red');
    log(`   You can try manually: npm install -g @jayphen/coders-tui`, 'yellow');
  }
}

function runTui(runner, script) {
  try {
    const result = spawnSync(runner, [script], {
      stdio: 'inherit',
      env: process.env
    });
    if (result.error) {
      throw result.error;
    }
  } catch (e) {
    log(`❌ Failed to launch TUI: ${e.message}`, 'red');
  }
}

// Main
const args = process.argv.slice(2);
const command = args[0];

if (command === 'help' || !command) {
  usage();
} else if (command === 'orchestrator') {
  startOrAttachOrchestrator().catch((err) => {
    log(`❌ Failed to start orchestrator: ${err.message}`, 'red');
  });
} else if (command === 'tui') {
  launchTui();
} else if (command === 'list') {
  listSessions();
} else if (command === 'attach') {
  const sessionName = args[1];
  if (!sessionName) {
    log('Usage: coders attach <session-name>', 'red');
  } else {
    attachSession(sessionName);
  }
} else if (command === 'kill') {
  const sessionName = args[1];
  if (!sessionName) {
    log('Usage: coders kill <session-name>', 'red');
  } else {
    killSession(sessionName);
  }
} else if (command === 'prune') {
  pruneOrphaned(args);
} else if (command === 'dashboard') {
  launchDashboard().catch((err) => {
    log(`❌ Failed to launch dashboard: ${err.message}`, 'red');
  });
} else if (command === 'restart-dashboard') {
  restartDashboard().catch((err) => {
    log(`❌ Failed to restart dashboard: ${err.message}`, 'red');
  });
} else if (command === 'update-plugin') {
  // Parse --plugin flag, default to 'coders'
  let pluginName = 'coders';
  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--plugin' && args[i + 1]) {
      pluginName = args[i + 1];
      i++;
    }
  }
  updatePluginInSessions(pluginName);
} else if (command === 'spawn') {
  // Valid tool names
  const VALID_TOOLS = ['claude', 'claude-code', 'gemini', 'codex', 'openai-codex', 'opencode', 'open-code'];

  // Default to 'claude' if no tool specified or if tool looks like a flag
  let tool = args[1];
  let argStartIndex = 2; // Default: args start after tool name

  if (!tool || tool.startsWith('--')) {
    tool = 'claude';
    argStartIndex = 1; // No tool specified, args start at index 1
  }

  // Validate tool name
  if (!VALID_TOOLS.includes(tool)) {
    log(`❌ Invalid tool: "${tool}"`, 'red');
    log(`   Valid tools: ${VALID_TOOLS.filter(t => !t.includes('-')).join(', ')}`, 'yellow');
    log(``, 'yellow');
    log(`   Examples:`, 'blue');
    log(`   • coders spawn claude --task "your task"`, 'blue');
    log(`   • coders spawn gemini --task "your task"`, 'blue');
    log(`   • coders spawn codex --task "your task"`, 'blue');
    log(`   • coders spawn opencode --task "your task"`, 'blue');
    log(``, 'yellow');
    log(`   Tip: Use "claude" (not "sonnet") to spawn Claude Code`, 'yellow');
    process.exit(1);
  }

  let sessionName = null; // Will be generated from task if not provided
  let worktreeBranch = null;
  let baseBranch = 'main';
  let prdFile = null;
  let taskDesc = 'Complete the assigned task';
  let enableHeartbeat = true; // Enabled by default for dashboard tracking
  let customCwd = null; // Optional working directory
  let model = null;

  for (let i = argStartIndex; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--name' && args[i+1]) {
      sessionName = args[i+1];
      i++;
    } else if (arg === '--worktree' && args[i+1]) {
      worktreeBranch = args[i+1];
      i++;
    } else if (arg === '--base' && args[i+1]) {
      baseBranch = args[i+1];
      i++;
    } else if ((arg === '--prd' || arg === '--spec') && args[i+1]) {
      prdFile = args[i+1];
      i++;
    } else if (arg === '--task' && args[i+1]) {
      taskDesc = args[i+1];
      i++;
    } else if (arg === '--model' && args[i+1]) {
      model = args[i+1];
      i++;
    } else if ((arg === '--cwd' || arg === '--dir') && args[i+1]) {
      // Store raw path arg - will be resolved later with zoxide support
      customCwd = args[i+1];
      i++;
    } else if (arg === '--heartbeat' || arg === '--dashboard') {
      enableHeartbeat = true;
    } else if (arg === '--no-heartbeat') {
      enableHeartbeat = false;
    }
  }

  // Generate session name from task description if not explicitly provided
  if (!sessionName) {
    sessionName = generateSessionName(tool, taskDesc);
  }

  // Resolve and validate custom working directory if provided
  let resolvedCwd = null;
  if (customCwd) {
    const pathResult = resolvePathWithZoxide(customCwd);

    if (!pathResult) {
      // Path resolution failed
      const hasZoxide = isZoxideAvailable();
      log(`❌ Invalid path: "${customCwd}"`, 'red');
      log(`   Path does not exist and could not be resolved.`, 'red');
      if (hasZoxide) {
        log(`   Note: zoxide was checked but found no match.`, 'yellow');
      } else {
        log(`   Tip: Install zoxide (https://github.com/ajeetdsouza/zoxide) for smart directory jumping.`, 'yellow');
      }
      process.exit(1);
    }

    // Validate the resolved path
    const validation = validatePath(pathResult.resolved);
    if (!validation.valid) {
      log(`❌ ${validation.error}`, 'red');
      process.exit(1);
    }

    resolvedCwd = pathResult.resolved;

    // Log resolution method
    if (pathResult.method === 'zoxide') {
      log(`🔍 Resolved "${customCwd}" → ${resolvedCwd} (via zoxide)`, 'blue');
    } else if (customCwd !== resolvedCwd) {
      log(`📁 Working directory: ${resolvedCwd}`, 'blue');
    }
  }

  // Create worktree if requested
  let worktreePath = null;
  if (worktreeBranch) {
    worktreePath = createWorktree(worktreeBranch, baseBranch);
  }

  // Build context from PRD
  const contextFiles = prdFile ? [prdFile] : [];
  const prompt = generateInitialPrompt(tool, taskDesc, contextFiles);

  // Spawn in new tmux window
  // Always use tmux for reliability
  (async () => {
    await spawnInNewTmuxWindow(tool, worktreePath, prompt, sessionName, enableHeartbeat, null, resolvedCwd, model);

    log(`\n✅ Session "${sessionName}" is ready!`, 'green');
    // Show parent info if spawned from another session
    const effectiveParentSessionId = process.env.CODERS_SESSION_ID || null;
    if (effectiveParentSessionId) {
      log(`👪 Parent session: ${effectiveParentSessionId}`, 'blue');
    }
    log(`💡 Attach: coders attach ${sessionName}`, 'yellow');
    if (enableHeartbeat) {
      log(`💡 View dashboard: coders dashboard`, 'yellow');
    }
  })().catch((err) => {
    log(`❌ Failed to spawn session: ${err.message}`, 'red');
  });
} else if (command === 'promise') {
  // Parse promise arguments
  let summary = null;
  let status = 'completed';
  let blockers = null;

  for (let i = 1; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--status' && args[i + 1]) {
      status = args[i + 1];
      i++;
    } else if (arg === '--blockers' && args[i + 1]) {
      blockers = args[i + 1];
      i++;
    } else if (!arg.startsWith('--') && !summary) {
      summary = arg;
    }
  }

  if (!summary) {
    log('Usage: coders promise "summary of what was done" [--status completed|blocked|needs-review] [--blockers "reason"]', 'red');
    process.exit(1);
  }

  // Validate status
  if (!['completed', 'blocked', 'needs-review'].includes(status)) {
    log(`Invalid status: ${status}. Must be one of: completed, blocked, needs-review`, 'red');
    process.exit(1);
  }

  (async () => {
    const depsOk = await ensureDependencies();
    if (!depsOk) {
      log(`❌ Cannot publish promise without redis dependency.`, 'red');
      return;
    }

    // Dynamic import of redis
    const { createClient } = await import('redis');
    const REDIS_URL = process.env.REDIS_URL || 'redis://localhost:6379';
    const PROMISES_CHANNEL = 'coders:promises';
    const PROMISE_KEY_PREFIX = 'coders:promise:';

    const client = createClient({ url: REDIS_URL });
    await client.connect();

    const sessionId = process.env.CODERS_SESSION_ID || 'coder-unknown';
    const promise = {
      sessionId,
      timestamp: Date.now(),
      summary,
      status,
      blockers: blockers ? [blockers] : undefined
    };

    // Store the promise
    const key = `${PROMISE_KEY_PREFIX}${sessionId}`;
    await client.set(key, JSON.stringify(promise), { EX: 86400 }); // 24h TTL

    // Publish to channel for real-time updates
    await client.publish(PROMISES_CHANNEL, JSON.stringify(promise));

    await client.quit();

    const statusEmoji = status === 'blocked' ? '🚫' :
                        status === 'needs-review' ? '👀' : '✅';
    log(`\n${statusEmoji} Promise published for: ${sessionId}`, 'green');
    log(`\n   Summary: ${summary}`, 'blue');
    log(`   Status: ${status}`, 'blue');
    if (blockers) {
      log(`   Blockers: ${blockers}`, 'yellow');
    }
    log(`\nThe orchestrator and dashboard have been notified.`, 'green');
  })().catch((err) => {
    log(`❌ Failed to publish promise: ${err.message}`, 'red');
  });
} else if (command === 'promises' || command === 'check-promises') {
  // List all promises (completion summaries)
  (async () => {
    const depsOk = await ensureDependencies();
    if (!depsOk) {
      log(`❌ Cannot check promises without redis dependency.`, 'red');
      return;
    }

    const { createClient } = await import('redis');
    const REDIS_URL = process.env.REDIS_URL || 'redis://localhost:6379';
    const PROMISE_KEY_PREFIX = 'coders:promise:';

    const client = createClient({ url: REDIS_URL });
    await client.connect();

    try {
      const keys = await client.keys(`${PROMISE_KEY_PREFIX}*`);

      if (keys.length === 0) {
        log(`\n📋 No completion promises found.`, 'yellow');
        log(`   Sessions will publish promises when they complete their tasks.`, 'blue');
        await client.quit();
        return;
      }

      log(`\n📋 Completion Promises (${keys.length}):\n`, 'blue');

      for (const key of keys) {
        const data = await client.get(key);
        if (data) {
          const promise = JSON.parse(data);
          const sessionId = key.replace(PROMISE_KEY_PREFIX, '').replace('coder-', '');
          const statusEmoji = promise.status === 'blocked' ? '🚫' :
                            promise.status === 'needs-review' ? '👀' : '✅';
          const timeAgo = getTimeAgo(promise.timestamp);

          log(`${statusEmoji} ${sessionId}`, 'green');
          log(`   ${promise.summary}`, 'reset');
          log(`   Status: ${promise.status} • ${timeAgo}`, 'blue');
          if (promise.blockers && promise.blockers.length > 0) {
            log(`   Blockers: ${promise.blockers.join(', ')}`, 'yellow');
          }
          if (promise.filesChanged && promise.filesChanged.length > 0) {
            log(`   Files: ${promise.filesChanged.slice(0, 3).join(', ')}${promise.filesChanged.length > 3 ? '...' : ''}`, 'blue');
          }
          log('');
        }
      }

      await client.quit();
    } catch (err) {
      log(`❌ Failed to fetch promises: ${err.message}`, 'red');
      await client.quit();
    }
  })().catch((err) => {
    log(`❌ Failed to check promises: ${err.message}`, 'red');
  });
} else if (command === 'loop') {
  // Start recursive loop for auto-spawning tasks from todolist
  let todolistPath = null;
  let loopCwd = null;
  let loopTool = 'claude';
  let loopModel = null;
  let maxConcurrent = 1;
  let stopOnBlocked = false;
  let background = true;

  for (let i = 1; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--todolist' && args[i+1]) {
      todolistPath = args[i+1];
      i++;
    } else if ((arg === '--cwd' || arg === '--dir') && args[i+1]) {
      loopCwd = args[i+1];
      i++;
    } else if (arg === '--tool' && args[i+1]) {
      loopTool = args[i+1];
      i++;
    } else if (arg === '--model' && args[i+1]) {
      loopModel = args[i+1];
      i++;
    } else if (arg === '--max-concurrent' && args[i+1]) {
      maxConcurrent = parseInt(args[i+1]);
      i++;
    } else if (arg === '--stop-on-blocked') {
      stopOnBlocked = true;
    } else if (arg === '--foreground') {
      background = false;
    }
  }

  if (!todolistPath || !loopCwd) {
    log('Usage: coders loop --todolist <path> --cwd <dir> [options]', 'red');
    log('Example: coders loop --todolist tasks.txt --cwd ~/project', 'yellow');
    process.exit(1);
  }

  const scriptDir = path.dirname(new URL(import.meta.url).pathname);
  const loopRunner = path.join(scriptDir, 'loop-runner.js');

  const loopArgs = [
    '--todolist', todolistPath,
    '--cwd', loopCwd,
    '--tool', loopTool
  ];

  if (loopModel) loopArgs.push('--model', loopModel);
  if (stopOnBlocked) loopArgs.push('--stop-on-blocked');

  log(`🔄 Starting recursive loop`, 'blue');
  log(`📂 Todolist: ${todolistPath}`, 'blue');
  log(`📁 Working directory: ${loopCwd}`, 'blue');

  if (background) {
    log(`🔧 Running in background (use 'coders loop-status' to check progress)`, 'yellow');
    execSync(`nohup node "${loopRunner}" ${loopArgs.join(' ')} > /tmp/coders-loop.log 2>&1 &`);
    log(`✅ Loop started! Log: /tmp/coders-loop.log`, 'green');
  } else {
    log(`🔧 Running in foreground`, 'yellow');
    execSync(`node "${loopRunner}" ${loopArgs.join(' ')}`, { stdio: 'inherit' });
  }
} else if (command === 'resume') {
  const sessionName = args[1];

  (async () => {
    const depsOk = await ensureDependencies();
    if (!depsOk) {
      log(`❌ Cannot resume without redis dependency.`, 'red');
      return;
    }

    const { createClient } = await import('redis');
    const REDIS_URL = process.env.REDIS_URL || 'redis://localhost:6379';
    const PROMISE_KEY_PREFIX = 'coders:promise:';

    const client = createClient({ url: REDIS_URL });
    await client.connect();

    // Determine session ID
    let sessionId;
    if (sessionName) {
      sessionId = sessionName.startsWith('coder-') ? sessionName : `coder-${sessionName}`;
    } else {
      sessionId = process.env.CODERS_SESSION_ID;
    }

    if (!sessionId) {
      log('Usage: coders resume [session-name]', 'red');
      log('   If no session name is provided, the current session ID must be set in CODERS_SESSION_ID', 'yellow');
      await client.quit();
      process.exit(1);
    }

    // Delete the promise
    const key = `${PROMISE_KEY_PREFIX}${sessionId}`;
    const deleted = await client.del(key);

    await client.quit();

    if (deleted > 0) {
      log(`\n🔄 Session resumed: ${sessionId}`, 'green');
      log(`\nThe session has been marked as active again.`, 'blue');
    } else {
      log(`\n⚠️  No promise found for session: ${sessionId}`, 'yellow');
      log(`   The session may already be active.`, 'yellow');
    }
  })().catch((err) => {
    log(`❌ Failed to resume session: ${err.message}`, 'red');
  });
} else {
  log(`Unknown command: ${command}`, 'red');
  usage();
}
