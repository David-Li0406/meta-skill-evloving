/**
 * Type definitions for Coder Spawner Skill
 */

// ============================================================================
// Main Spawn Options
// ============================================================================

export interface SpawnOptions {
  /** AI tool to spawn: claude, gemini, codex, or opencode */
  tool: 'claude' | 'gemini' | 'codex' | 'opencode';
  /** Task description for the AI to work on */
  task?: string;
  /** Custom session name */
  name?: string;
  /** Optional model identifier passed to the tool CLI */
  model?: string;
  /** Git branch name for worktree (optional) */
  worktree?: string;
  /** Base branch for worktree (default: main) */
  baseBranch?: string;
  /** PRD or spec file path to include as context */
  prd?: string;
  /** Enable interactive prompts for missing info (default: true) */
  interactive?: boolean;
  /** Redis configuration for heartbeat/pub/sub */
  redis?: RedisConfig;
  /** Enable heartbeat publishing (requires redis config) */
  enableHeartbeat?: boolean;
  /** Custom pane ID (auto-generated if not provided) */
  paneId?: string;
  /** Custom working directory for the session (overrides worktree path) */
  cwd?: string;
}

export interface CoderSession {
  /** Session ID */
  id: string;
  /** AI tool (claude, gemini, codex) */
  tool: string;
  /** Worktree path if applicable */
  worktree?: string;
  /** Task description */
  task: string;
  /** When the session was created */
  createdAt: Date;
  /** Pane ID for heartbeat monitoring */
  paneId?: string;
}

// ============================================================================
// Redis Types
// ============================================================================

export interface RedisConfig {
  /** Redis connection URL */
  url?: string;
  /** Redis host (default: localhost) */
  host?: string;
  /** Redis port (default: 6379) */
  port?: number;
  /** Redis password */
  password?: string;
}

export interface PaneInfo {
  paneId: string;
  sessionId: string;
  windowId: string;
  tool: string;
  task: string;
  pid: number;
  createdAt: number;
}

export interface HeartbeatData {
  paneId: string;
  sessionId: string;
  timestamp: number;
  status: 'alive' | 'processing' | 'idle';
  lastActivity: string;
}

export interface CodersConfig {
  /** Global Redis configuration */
  redis?: RedisConfig;
  /** Snapshot directory (default: ~/.coders/snapshots) */
  snapshotDir?: string;
}

// ============================================================================
// Tmux Resurrect Types
// ============================================================================

export interface SnapshotMetadata {
  version: number;
  timestamp: number;
  hostname: string;
  platform: string;
  sessionCount: number;
}

export interface PaneSnapshot {
  paneId: string;
  windowId: string;
  sessionName: string;
  command: string;
  workingDirectory: string;
  environment: Record<string, string>;
}

export interface WindowSnapshot {
  windowId: string;
  windowName: string;
  panes: PaneSnapshot[];
  layout: string;
}

export interface SessionSnapshot {
  sessionName: string;
  sessionId: string;
  createdAt: string;
  windows: WindowSnapshot[];
}

export interface FullSnapshot {
  metadata: SnapshotMetadata;
  sessions: SessionSnapshot[];
  createdAt: string;
}

export interface ResurrectOptions {
  /** Snapshot directory path */
  snapshotDir?: string;
  /** Include environment variables in snapshot */
  includeEnvironment?: boolean;
  /** Dry run - don't actually create/restore */
  dryRun?: boolean;
  /** Filter sessions to include */
  sessionFilter?: string[];
}

export interface ListOptions {
  /** Sort by: 'date', 'name', or 'size' */
  sortBy?: 'date' | 'name' | 'size';
  /** Reverse sort order */
  reverse?: boolean;
}

// ============================================================================
// Exports
// ============================================================================

/**
 * Coder Spawner - Spawn AI coding assistants in isolated tmux sessions
 */
export const coders: {
  /** Spawn a new AI coding assistant in a tmux session */
  spawn: (options: SpawnOptions) => Promise<string>;
  /** Spawn with Redis heartbeat enabled */
  spawnWithHeartbeat: (options: SpawnOptions) => Promise<string>;
  /** List all active coder sessions */
  list: () => string;
  /** Get instructions to attach to a session */
  attach: (sessionName: string) => string;
  /** Kill a coder session */
  kill: (sessionName: string) => string;
  /** Quick spawn Claude */
  claude: (task: string, options?: Omit<SpawnOptions, 'tool'>) => Promise<string>;
  /** Quick spawn Gemini */
  gemini: (task: string, options?: Omit<SpawnOptions, 'tool'>) => Promise<string>;
  /** Quick spawn Codex */
  codex: (task: string, options?: Omit<SpawnOptions, 'tool'>) => Promise<string>;
  /** Quick spawn OpenCode */
  opencode: (task: string, options?: Omit<SpawnOptions, 'tool'>) => Promise<string>;
  /** Quick spawn with worktree */
  worktree: (branchName: string, task: string, options?: Omit<SpawnOptions, 'tool'>) => Promise<string>;
  /** Create a git worktree */
  createWorktree: (branchName: string, baseBranch?: string) => string;
  /** Get all active sessions */
  getActiveSessions: () => CoderSession[];
  /** Configure global options */
  configure: (config: CodersConfig) => void;
  /** Send message to another agent via Redis */
  sendMessage: (channel: string, message: any, redisConfig?: RedisConfig) => Promise<void>;
  /** Listen for messages from other agents via Redis */
  listenForMessages: (channel: string, callback: (message: any) => void, redisConfig?: RedisConfig) => Promise<void>;
  /** Redis manager class */
  RedisManager: typeof import('./redis').RedisManager;
  /** Get pane ID helper */
  getPaneId: typeof import('./redis').getPaneId;
  /** Inject pane ID context helper */
  injectPaneIdContext: typeof import('./redis').injectPaneIdContext;
  /** Heartbeat channel name */
  HEARTBEAT_CHANNEL: string;
};

/**
 * Tmux Resurrect - Snapshot and restore tmux sessions
 */
export const tmuxResurrect: {
  /** Create snapshot of all tmux sessions */
  snapshot: (options?: ResurrectOptions) => FullSnapshot;
  /** Restore sessions from snapshot */
  restore: (snapshotPath?: string, options?: ResurrectOptions) => { restored: number; failed: number };
  /** List available snapshots */
  listSnapshots: (options?: ListOptions) => Array<{ filename: string; timestamp: number; size: number }>;
  /** Get latest snapshot path */
  getLatestSnapshotPath: () => string | null;
  /** Delete a snapshot */
  deleteSnapshot: (filename: string) => boolean;
  /** Get snapshot directory */
  getSnapshotDir: () => string;
  /** Get session prefix */
  getSessionPrefix: () => string;
};

/**
 * Redis Manager - Heartbeat, pub/sub, and connection management
 */
export class RedisManager {
  constructor(config?: RedisConfig);
  connect(): Promise<void>;
  disconnect(): Promise<void>;
  getPaneId(): string;
  setPaneId(id: string): void;
  publishHeartbeat(status?: HeartbeatData['status'], lastActivity?: string): Promise<void>;
  startHeartbeat(intervalMs?: number): void;
  stopHeartbeat(): void;
  publishMessage(channel: string, message: any): Promise<void>;
  subscribeToChannel(channel: string, callback: (message: any) => Promise<void>): Promise<void>;
  getActivePanes(): Promise<PaneInfo[]>;
  markPaneDead(paneId: string): Promise<void>;
}

/**
 * Quick create heartbeat session
 */
export function createHeartbeatSession(config?: RedisConfig): Promise<RedisManager>;

/**
 * Quick functions
 */
export function getPaneId(): string;
export function injectPaneIdContext(systemPrompt: string, paneId: string): string;
export function snapshot(options?: ResurrectOptions): FullSnapshot;
export function restore(snapshotPath?: string, options?: ResurrectOptions): { restored: number; failed: number };
export function listSnapshots(options?: ListOptions): Array<{ filename: string; timestamp: number; size: number }>;

/**
 * Constants
 */
export const SNAPSHOT_DIR: string;
export const HEARTBEAT_CHANNEL: string;

export default coders;
