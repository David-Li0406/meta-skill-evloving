/**
 * Coder Spawner Skill for Claude Code
 *
 * Spawn AI coding assistants in isolated tmux sessions with optional git worktrees.
 * Supports Redis heartbeat and pub/sub for inter-agent communication.
 * 
 * Usage:
 * import { coders } from '@jayphen/coders';
 * 
 * // Interactive mode - asks for missing info
 * await coders.spawn({ tool: 'claude' });
 * 
 * // Direct mode - all options upfront
 * await coders.spawn({
 *   tool: 'claude',
 *   task: 'Refactor the authentication module',
 *   worktree: 'feature/auth-refactor',
 *   prd: 'docs/auth-prd.md'
 * });
 * 
 * // With Redis heartbeat enabled
 * await coders.spawn({
 *   tool: 'claude',
 *   task: 'Fix the bug',
 *   redis: { url: 'redis://localhost:6379' }
 * });
 * 
 * // Quick helpers
 * await coders.claude('Fix the bug', { worktree: 'fix-auth' });
 * await coders.gemini('Research JWT approaches');
 */

import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';
import {
  RedisManager,
  getPaneId,
  injectPaneIdContext,
  RedisConfig,
  HEARTBEAT_CHANNEL,
  PROMISES_CHANNEL,
  CoderPromise
} from './redis';
import { generateSessionName } from './scripts/session-name.js';
import { generateSmartSessionName } from './scripts/ai-name-generator.js';
import { snapshot, restore, listSnapshots } from './tmux-resurrect';

const WORKTREE_BASE = '../worktrees';
const SESSION_PREFIX = 'coder-';

// Types
export interface SpawnOptions {
  tool: 'claude' | 'gemini' | 'codex' | 'opencode';
  task?: string;
  name?: string;
  /** Optional model identifier passed to the tool CLI */
  model?: string;
  worktree?: string;
  baseBranch?: string;
  prd?: string;
  interactive?: boolean;
  redis?: RedisConfig;
  enableHeartbeat?: boolean;
  paneId?: string;
  parentSessionId?: string;
  /** Custom working directory for the session (overrides worktree path) */
  cwd?: string;
  /** Use Claude Haiku to generate AI-powered session names (default: true) */
  useAI?: boolean;
}

export interface CoderSession {
  id: string;
  tool: string;
  worktree?: string;
  task: string;
  createdAt: Date;
  paneId?: string;
  displayName?: string;
}

export interface CodersConfig {
  redis?: RedisConfig;
  snapshotDir?: string;
}

/**
 * Global config for coders skill
 */
let globalConfig: CodersConfig = {
  snapshotDir: '~/.coders/snapshots'
};

/**
 * Configure the coders skill globally
 */
export function configure(config: CodersConfig): void {
  globalConfig = { ...globalConfig, ...config };
}

/**
 * Get the git root directory
 */
function getGitRoot(): string {
  try {
    return execSync('git rev-parse --show-toplevel', { encoding: 'utf8' }).trim();
  } catch {
    return process.cwd();
  }
}

/**
 * Get the current git branch
 */
function getCurrentBranch(): string {
  try {
    return execSync('git rev-parse --abbrev-ref HEAD', { encoding: 'utf8' }).trim();
  } catch {
    return 'main';
  }
}

/**
 * Read file content
 */
function readFile(filePath: string): string | null {
  try {
    const absPath = path.isAbsolute(filePath) ? filePath : path.join(getGitRoot(), filePath);
    return fs.readFileSync(absPath, 'utf8');
  } catch {
    return null;
  }
}

/**
 * Create a git worktree for the given branch
 */
function createWorktree(branchName: string, baseBranch: string = 'main'): string {
  const gitRoot = getGitRoot();
  const worktreePath = path.join(gitRoot, WORKTREE_BASE, branchName);
  
  try {
    fs.mkdirSync(path.dirname(worktreePath), { recursive: true });
    execSync(`git worktree add ${worktreePath} ${baseBranch}`, { cwd: gitRoot });
    return `✅ Worktree created: ${worktreePath}`;
  } catch (e: any) {
    return `⚠️  Worktree: ${e.message}`;
  }
}

/**
 * Build the spawn command for a tool with optional pane ID injection
 */
function buildCommand(
  tool: string,
  promptFile: string,
  worktreePath?: string,
  paneId?: string,
  redisConfig?: RedisConfig,
  sessionId?: string,
  parentSessionId?: string,
  model?: string
): string {
  const envVars: string[] = [];

  if (worktreePath) {
    envVars.push(`WORKSPACE_DIR="${worktreePath}"`);
  }

  if (paneId) {
    envVars.push(`CODERS_PANE_ID="${paneId}"`);
  }

  if (sessionId) {
    envVars.push(`CODERS_SESSION_ID="${sessionId}"`);
  }

  if (parentSessionId) {
    envVars.push(`CODERS_PARENT_SESSION_ID="${parentSessionId}"`);
  }

  if (redisConfig?.url) {
    envVars.push(`REDIS_URL="${redisConfig.url}"`);
  }

  const env = envVars.length > 0 ? envVars.join(' ') + ' ' : '';
  const modelArg = model ? ` --model "${model}"` : '';
  
  if (tool === 'claude' || tool === 'claude-code') {
    return `${env}claude --dangerously-spawn-permission${modelArg} -f "${promptFile}"`;
  } else if (tool === 'gemini') {
    return `${env}gemini${modelArg} -f "${promptFile}"`;
  } else if (tool === 'codex') {
    return `${env}codex${modelArg} -f "${promptFile}"`;
  } else if (tool === 'opencode') {
    return `${env}opencode${modelArg} -f "${promptFile}"`;
  }
  throw new Error(`Unknown tool: ${tool}`);
}

/**
 * Generate a prompt file with task, context, and pane ID injection
 */
function createPrompt(task: string, contextFiles?: string[], paneId?: string, redisConfig?: RedisConfig): string {
  let prompt = '';
  
  // Inject pane ID context if provided
  if (paneId) {
    prompt += injectPaneIdContext('', paneId);
  }
  
  prompt += `TASK: ${task}\n\n`;
  
  if (contextFiles && contextFiles.length > 0) {
    prompt += 'CONTEXT:\n';
    contextFiles.forEach(file => {
      const content = readFile(file);
      if (content) {
        prompt += `\n--- ${file} ---\n${content}\n`;
      }
    });
    prompt += '\n';
  }
  
  // Add Redis info to prompt if configured
  if (redisConfig?.url) {
    prompt += `
<!-- REDIS CONFIG -->
<!-- HEARTBEAT_CHANNEL: ${HEARTBEAT_CHANNEL} -->

Redis is configured for this session. Publish heartbeats for session monitoring.

Heartbeat format:
{
  "paneId": "${paneId || '<your-pane-id>'}",
  "status": "alive",
  "timestamp": Date.now()
}

Publish to Redis channel: ${HEARTBEAT_CHANNEL}
`;
  }
  
  return prompt;
}

/**
 * Spawn a new AI coding assistant in a tmux session
 */
export async function spawn(options: SpawnOptions): Promise<string> {
  const {
    tool,
    task = '',
    name,
    worktree,
    baseBranch = 'main',
    prd,
    interactive = true,
    redis: redisConfig,
    enableHeartbeat = !!redisConfig?.url,
    paneId: providedPaneId,
    parentSessionId: providedParentSessionId,
    cwd: customCwd,
    useAI = true,
    model
  } = options;

  // Auto-detect parent session if running inside a coder session
  const parentSessionId = providedParentSessionId || process.env.CODERS_SESSION_ID || undefined;

  if (!task) {
    return '❌ Task description is required. Pass `task: "..."` or use interactive mode.';
  }

  // Generate session name (AI-powered or fallback to regex)
  let sessionName: string;
  let displayName: string;

  if (name) {
    // Custom name provided - use it for both
    sessionName = name;
    displayName = name.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
  } else {
    // Generate smart name using AI or fallback
    const nameResult = await generateSmartSessionName(tool, task, useAI);
    sessionName = nameResult.sessionName;
    displayName = nameResult.displayName;
  }

  const sessionId = `${SESSION_PREFIX}${sessionName}`;
  const paneId = providedPaneId || getPaneId();
  
  // Create worktree if requested
  let worktreePath: string | undefined;
  if (worktree) {
    const gitRoot = getGitRoot();
    worktreePath = path.join(gitRoot, WORKTREE_BASE, worktree);
    try {
      fs.mkdirSync(path.dirname(worktreePath), { recursive: true });
      execSync(`git worktree add ${worktreePath} ${baseBranch}`, { cwd: gitRoot });
    } catch (e: any) {
      // Worktree might exist
    }
  }
  
  // Determine effective working directory: customCwd > worktreePath > current directory
  const effectiveCwd = customCwd
    ? (path.isAbsolute(customCwd) ? customCwd : path.resolve(process.cwd(), customCwd))
    : (worktreePath || process.cwd());

  // Build prompt with optional PRD and Redis context
  const contextFiles = prd ? [prd] : [];
  const prompt = createPrompt(task, contextFiles, paneId, redisConfig);
  const promptFile = `/tmp/coders-prompt-${Date.now()}.txt`;
  fs.writeFileSync(promptFile, prompt);

  // Build command with environment variables (use effectiveCwd for WORKSPACE_DIR)
  const cmd = buildCommand(tool, promptFile, effectiveCwd, paneId, redisConfig, sessionId, parentSessionId, model);

  try {
    // Clean up existing session if any
    try { execSync(`tmux kill-session -t ${sessionId}`); } catch {}

    // Create new tmux session with cd to effectiveCwd
    execSync(`tmux new-session -s "${sessionId}" -d "cd ${effectiveCwd}; ${cmd}"`);

    // Store pane info for Redis if configured (including displayName)
    if (redisConfig?.url) {
      const redis = new RedisManager(redisConfig);
      await redis.connect();
      await redis.setPaneId(paneId);
      // Store session metadata including displayName
      await redis.setSessionMetadata(sessionId, {
        displayName,
        tool,
        task: task.substring(0, 200),
        createdAt: Date.now()
      });
      await redis.disconnect();
      // Note: heartbeat is handled separately by heartbeat.js spawned in main.js
    }

    return `
🤖 Spawned **${tool}** in new tmux window!

**Name:** ${displayName}
**Session:** ${sessionId}
**Pane ID:** ${paneId}
**Parent:** ${parentSessionId || 'none (root session)'}
**Working Directory:** ${effectiveCwd}
**Worktree:** ${worktreePath || 'none'}
**Task:** ${task}
**Model:** ${model || 'default'}
**PRD:** ${prd || 'none'}
**Redis:** ${redisConfig?.url || 'disabled'}
**Heartbeat:** ${enableHeartbeat ? 'enabled' : 'disabled'}

To attach:
\`coders attach ${sessionName}\`
or
\`tmux attach -t ${sessionId}\`
`;
  } catch (e: any) {
    return `❌ Failed: ${e.message}`;
  }
}

/**
 * List all active coder sessions
 */
export function list(): string {
  try {
    const output = execSync('tmux list-sessions 2>/dev/null', { encoding: 'utf8' });
    const sessions = output.split('\n').filter((s: string) => s.includes(SESSION_PREFIX));
    
    if (sessions.length === 0) {
      return 'No coder sessions active.';
    }
    
    return '📋 Active Coder Sessions:\n\n' + sessions.join('\n');
  } catch {
    return 'tmux not available or no sessions';
  }
}

/**
 * Attach to a coder session
 */
export function attach(sessionName: string): string {
  const sessionId = `${SESSION_PREFIX}${sessionName}`;
  return `Run: \`tmux attach -t ${sessionId}\``;
}

/**
 * Kill a coder session
 */
export function kill(sessionName: string): string {
  const sessionId = `${SESSION_PREFIX}${sessionName}`;
  try {
    execSync(`tmux kill-session -t ${sessionId}`);
    return `✅ Killed session: ${sessionId}`;
  } catch (e: any) {
    return `❌ Failed: ${e.message}`;
  }
}

/**
 * Quick spawn helpers - minimal options for speed
 */
export async function claude(
  task: string,
  options?: {
    name?: string;
    model?: string;
    worktree?: string;
    prd?: string;
    redis?: RedisConfig;
    enableHeartbeat?: boolean;
    cwd?: string;
  }
): Promise<string> {
  return spawn({ tool: 'claude', task, ...options });
}

export async function gemini(
  task: string,
  options?: {
    name?: string;
    model?: string;
    worktree?: string;
    prd?: string;
    redis?: RedisConfig;
    enableHeartbeat?: boolean;
    cwd?: string;
  }
): Promise<string> {
  return spawn({ tool: 'gemini', task, ...options });
}

export async function codex(
  task: string,
  options?: {
    name?: string;
    model?: string;
    worktree?: string;
    prd?: string;
    redis?: RedisConfig;
    enableHeartbeat?: boolean;
    cwd?: string;
  }
): Promise<string> {
  return spawn({ tool: 'codex', task, ...options });
}

export async function opencode(
  task: string,
  options?: {
    name?: string;
    model?: string;
    worktree?: string;
    prd?: string;
    redis?: RedisConfig;
    enableHeartbeat?: boolean;
    cwd?: string;
  }
): Promise<string> {
  return spawn({ tool: 'opencode', task, ...options });
}

/**
 * Alias for spawn with worktree - quick syntax
 */
export async function worktree(
  branchName: string,
  task: string,
  options?: {
    tool?: 'claude' | 'gemini' | 'codex' | 'opencode';
    model?: string;
    prd?: string;
    redis?: RedisConfig;
    enableHeartbeat?: boolean;
    cwd?: string;
  }
): Promise<string> {
  return spawn({
    tool: options?.tool || 'claude',
    task,
    worktree: branchName,
    model: options?.model,
    prd: options?.prd,
    redis: options?.redis,
    enableHeartbeat: options?.enableHeartbeat,
    cwd: options?.cwd
  });
}

/**
 * Get all active coder sessions
 */
export function getActiveSessions(): CoderSession[] {
  try {
    const output = execSync('tmux list-sessions 2>/dev/null', { encoding: 'utf8' });
    return output.split('\n')
      .filter((s: string) => s.includes(SESSION_PREFIX))
      .map((s: string) => {
        const match = s.match(/coder-([^:]+):/);
        return {
          id: match ? match[1] : 'unknown',
          tool: 'unknown',
          task: '',
          createdAt: new Date()
        } as CoderSession;
      });
  } catch {
    return [];
  }
}

/**
 * Spawn with Redis heartbeat enabled
 */
export async function spawnWithHeartbeat(
  options: SpawnOptions
): Promise<string> {
  return spawn({
    ...options,
    redis: options.redis || globalConfig.redis,
    enableHeartbeat: true
  });
}

/**
 * Send message to another agent via Redis pub/sub
 */
export async function sendMessage(
  channel: string,
  message: any,
  redisConfig?: RedisConfig
): Promise<void> {
  const config = redisConfig || globalConfig.redis;
  if (!config?.url) {
    throw new Error('Redis not configured. Pass redis config or set global config.');
  }
  
  const redis = new RedisManager(config);
  await redis.connect();
  await redis.publishMessage(channel, message);
  await redis.disconnect();
}

/**
 * Listen for messages from other agents via Redis pub/sub
 */
export async function listenForMessages(
  channel: string,
  callback: (message: any) => void,
  redisConfig?: RedisConfig
): Promise<void> {
  const config = redisConfig || globalConfig.redis;
  if (!config?.url) {
    throw new Error('Redis not configured. Pass redis config or set global config.');
  }

  const redis = new RedisManager(config);
  await redis.subscribeToChannel(channel, callback);
}

/**
 * Publish a promise (completion summary) for the current session
 */
export async function publishPromise(
  summary: string,
  options?: {
    status?: 'completed' | 'blocked' | 'needs-review';
    filesChanged?: string[];
    blockers?: string[];
    redisConfig?: RedisConfig;
  }
): Promise<string> {
  const config = options?.redisConfig || globalConfig.redis;
  if (!config?.url) {
    return '❌ Redis not configured. Promise requires Redis for coordination.';
  }

  const redis = new RedisManager(config);
  await redis.connect();

  try {
    await redis.publishPromise({
      summary,
      status: options?.status || 'completed',
      filesChanged: options?.filesChanged,
      blockers: options?.blockers
    });

    const sessionId = process.env.CODERS_SESSION_ID || 'unknown';
    const statusEmoji = options?.status === 'blocked' ? '🚫' :
                        options?.status === 'needs-review' ? '👀' : '✅';

    return `
${statusEmoji} Promise published for session: ${sessionId}

**Summary:** ${summary}
**Status:** ${options?.status || 'completed'}
${options?.filesChanged?.length ? `**Files Changed:** ${options.filesChanged.join(', ')}` : ''}
${options?.blockers?.length ? `**Blockers:** ${options.blockers.join(', ')}` : ''}

The orchestrator and dashboard have been notified.
`;
  } finally {
    await redis.disconnect();
  }
}

/**
 * Resume a session by clearing its promise (marking it as active again)
 */
export async function resumeSession(
  sessionName?: string,
  redisConfig?: RedisConfig
): Promise<string> {
  const config = redisConfig || globalConfig.redis;
  if (!config?.url) {
    return '❌ Redis not configured. Resume requires Redis for coordination.';
  }

  const sessionId = sessionName
    ? `${SESSION_PREFIX}${sessionName}`
    : process.env.CODERS_SESSION_ID;

  if (!sessionId) {
    return '❌ No session ID provided or detected.';
  }

  const redis = new RedisManager(config);
  await redis.connect();

  try {
    await redis.deletePromise(sessionId);
    return `
🔄 Session resumed: ${sessionId}

The session has been marked as active again. The promise has been cleared.
`;
  } finally {
    await redis.disconnect();
  }
}

/**
 * Main export with all functions
 */
export const coders = {
  spawn,
  spawnWithHeartbeat,
  list,
  attach,
  kill,
  claude,
  gemini,
  codex,
  opencode,
  worktree,
  createWorktree,
  getActiveSessions,
  configure,
  sendMessage,
  listenForMessages,
  // Promise functions
  publishPromise,
  resumeSession,
  // Re-export from redis.ts
  RedisManager,
  getPaneId,
  injectPaneIdContext,
  HEARTBEAT_CHANNEL,
  PROMISES_CHANNEL,
  // Tmux Resurrect
  snapshot,
  restore,
  listSnapshots
};

export default coders;
