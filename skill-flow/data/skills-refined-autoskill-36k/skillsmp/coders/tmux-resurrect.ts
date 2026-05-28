/**
 * Tmux Resurrect - Snapshot and Restore Utility
 * 
 * Snapshots entire tmux sessions and restores them from saved snapshots.
 * Useful for backup, migration, and session recovery.
 * 
 * Usage:
 *   // Snapshot all coder sessions
 *   await tmuxResurrect.snapshot();
 *   
 *   // Restore from latest snapshot
 *   await tmuxResurrect.restore();
 *   
 *   // List available snapshots
 *   const snapshots = tmuxResurrect.listSnapshots();
 */

import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

const SNAPSHOT_DIR = os.homedir() + '/.coders/snapshots';
const SESSION_PREFIX = 'coder-';

// Types
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
  snapshotDir?: string;
  includeEnvironment?: boolean;
  dryRun?: boolean;
  sessionFilter?: string[];
}

export interface ListOptions {
  sortBy?: 'date' | 'name' | 'size';
  reverse?: boolean;
}

/**
 * Ensure snapshot directory exists
 */
function ensureSnapshotDir(snapshotDir: string): void {
  fs.mkdirSync(snapshotDir, { recursive: true });
}

/**
 * Get current timestamp in ISO format
 */
function getTimestamp(): string {
  return new Date().toISOString();
}

/**
 * Get snapshot filename
 */
function getSnapshotFilename(timestamp?: number): string {
  const ts = timestamp || Date.now();
  return `snapshot-${new Date(ts).toISOString().replace(/[:.]/g, '-')}.json`;
}

/**
 * Get list of tmux sessions
 */
function getTmuxSessions(): string[] {
  try {
    const output = execSync('tmux list-sessions -F "#{session_name}"', { encoding: 'utf8' });
    return output.trim().split('\n').filter(Boolean);
  } catch {
    return [];
  }
}

/**
 * Get windows for a session
 */
function getSessionWindows(sessionName: string): string[] {
  try {
    const output = execSync(`tmux list-windows -t "${sessionName}" -F "#{window_id}"`, { encoding: 'utf8' });
    return output.trim().split('\n').filter(Boolean);
  } catch {
    return [];
  }
}

/**
 * Get panes for a window
 */
function getWindowPanes(sessionName: string, windowId: string): string[] {
  try {
    const output = execSync(`tmux list-panes -t "${sessionName}:${windowId}" -F "#{pane_id}"`, { encoding: 'utf8' });
    return output.trim().split('\n').filter(Boolean);
  } catch {
    return [];
  }
}

/**
 * Get pane command
 */
function getPaneCommand(sessionName: string, paneId: string): string {
  try {
    return execSync(`tmux display-message -t "${sessionName}:${paneId}" -F "#{pane_current_command}"`, { encoding: 'utf8' }).trim();
  } catch {
    return '';
  }
}

/**
 * Get pane working directory
 */
function getPaneCwd(sessionName: string, paneId: string): string {
  try {
    return execSync(`tmux display-message -t "${sessionName}:${paneId}" -F "#{pane_current_path}"`, { encoding: 'utf8' }).trim();
  } catch {
    return '';
  }
}

/**
 * Get pane environment variable
 */
function getPaneEnv(sessionName: string, paneId: string, varName: string): string {
  try {
    return execSync(`tmux show-environment -t "${sessionName}:${paneId}" -g "${varName}" 2>/dev/null || echo ""`, { encoding: 'utf8' }).trim();
  } catch {
    return '';
  }
}

/**
 * Get all pane environment variables
 */
function getPaneEnvironment(sessionName: string, paneId: string): Record<string, string> {
  const env: Record<string, string> = {};
  const importantVars = ['HOME', 'USER', 'PATH', 'SHELL', 'TERM', 'CODERS_PANE_ID', 'CODERS_SESSION_ID', 'REDIS_URL'];
  
  for (const varName of importantVars) {
    const value = getPaneEnv(sessionName, paneId, varName);
    if (value) {
      const [key, ...rest] = value.split('=');
      env[key] = rest.join('=');
    }
  }
  
  return env;
}

/**
 * Get window layout
 */
function getWindowLayout(sessionName: string, windowId: string): string {
  try {
    return execSync(`tmux display-message -t "${sessionName}:${windowId}" -F "#{window_layout}"`, { encoding: 'utf8' }).trim();
  } catch {
    return '';
  }
}

/**
 * Get window name
 */
function getWindowName(sessionName: string, windowId: string): string {
  try {
    return execSync(`tmux display-message -t "${sessionName}:${windowId}" -F "#{window_name}"`, { encoding: 'utf8' }).trim();
  } catch {
    return '';
  }
}

/**
 * Tmux Resurrect class for snapshot/restore operations
 */
export class TmuxResurrect {
  private snapshotDir: string;

  constructor(snapshotDir: string = SNAPSHOT_DIR) {
    this.snapshotDir = snapshotDir;
    ensureSnapshotDir(this.snapshotDir);
  }

  /**
   * Create a snapshot of all tmux sessions
   */
  snapshot(options: ResurrectOptions = {}): FullSnapshot {
    const { 
      includeEnvironment = true, 
      dryRun = false,
      sessionFilter 
    } = options;

    ensureSnapshotDir(this.snapshotDir);

    const sessions = getTmuxSessions();
    const sessionSnapshots: SessionSnapshot[] = [];

    for (const sessionName of sessions) {
      // Apply filter if provided
      if (sessionFilter && sessionFilter.length > 0) {
        if (!sessionFilter.some(f => sessionName.includes(f))) {
          continue;
        }
      }

      // Only snapshot coder sessions (or all if no filter)
      const isCoderSession = sessionName.startsWith(SESSION_PREFIX);
      if (sessionFilter && sessionFilter.length === 0 && !isCoderSession) {
        continue;
      }

      const windows = getSessionWindows(sessionName);
      const windowSnapshots: WindowSnapshot[] = [];

      for (const windowId of windows) {
        const panes = getWindowPanes(sessionName, windowId);
        const paneSnapshots: PaneSnapshot[] = [];

        for (const paneId of panes) {
          paneSnapshots.push({
            paneId,
            windowId,
            sessionName,
            command: getPaneCommand(sessionName, paneId),
            workingDirectory: getPaneCwd(sessionName, paneId),
            environment: includeEnvironment ? getPaneEnvironment(sessionName, paneId) : {}
          });
        }

        windowSnapshots.push({
          windowId,
          windowName: getWindowName(sessionName, windowId),
          panes: paneSnapshots,
          layout: getWindowLayout(sessionName, windowId)
        });
      }

      sessionSnapshots.push({
        sessionName,
        sessionId: `${SESSION_PREFIX}${Date.now()}`,
        createdAt: getTimestamp(),
        windows: windowSnapshots
      });
    }

    const snapshot: FullSnapshot = {
      metadata: {
        version: 1,
        timestamp: Date.now(),
        hostname: os.hostname(),
        platform: os.platform(),
        sessionCount: sessionSnapshots.length
      },
      sessions: sessionSnapshots,
      createdAt: getTimestamp()
    };

    // Save snapshot if not dry run
    if (!dryRun) {
      const filename = getSnapshotFilename();
      const filepath = path.join(this.snapshotDir, filename);
      fs.writeFileSync(filepath, JSON.stringify(snapshot, null, 2));
      
      // Also save as 'latest.json' for easy access
      const latestPath = path.join(this.snapshotDir, 'latest.json');
      fs.writeFileSync(latestPath, JSON.stringify(snapshot, null, 2));
    }

    return snapshot;
  }

  /**
   * Restore sessions from a snapshot
   */
  restore(snapshotPath?: string, options: ResurrectOptions = {}): { restored: number; failed: number } {
    const { dryRun = false } = options;

    let snapshot: FullSnapshot;

    if (snapshotPath) {
      if (!fs.existsSync(snapshotPath)) {
        throw new Error(`Snapshot not found: ${snapshotPath}`);
      }
      snapshot = JSON.parse(fs.readFileSync(snapshotPath, 'utf8'));
    } else {
      // Use latest snapshot
      const latestPath = path.join(this.snapshotDir, 'latest.json');
      if (!fs.existsSync(latestPath)) {
        throw new Error('No snapshot found. Run snapshot() first or provide a snapshot path.');
      }
      snapshot = JSON.parse(fs.readFileSync(latestPath, 'utf8'));
    }

    let restored = 0;
    let failed = 0;

    for (const session of snapshot.sessions) {
      try {
        if (!dryRun) {
          // Kill existing session if it exists
          try { execSync(`tmux kill-session -t "${session.sessionName}"`); } catch {}

          // Create new detached session
          const firstWindow = session.windows[0];
          if (firstWindow && firstWindow.panes.length > 0) {
            const firstPane = firstWindow.panes[0];
            const cmd = firstPane.command || 'bash';
            execSync(`tmux new-session -d -s "${session.sessionName}" -c "${firstPane.workingDirectory}" "${cmd}"`);
          }
        }
        restored++;
      } catch (e: any) {
        console.error(`Failed to restore session ${session.sessionName}:`, e.message);
        failed++;
      }
    }

    return { restored, failed };
  }

  /**
   * List available snapshots
   */
  listSnapshots(options: ListOptions = {}): Array<{ filename: string; timestamp: number; size: number }> {
    const { sortBy = 'date', reverse = true } = options;

    ensureSnapshotDir(this.snapshotDir);

    const files = fs.readdirSync(this.snapshotDir)
      .filter(f => f.startsWith('snapshot-') && f.endsWith('.json'))
      .filter(f => f !== 'latest.json');

    const snapshots = files.map(filename => {
      const filepath = path.join(this.snapshotDir, filename);
      const stats = fs.statSync(filepath);
      return {
        filename,
        timestamp: parseInt(filename.match(/snapshot-(\d+)/)?.[1] || '0'),
        size: stats.size
      };
    });

    // Sort
    snapshots.sort((a, b) => {
      if (sortBy === 'date') {
        return reverse ? b.timestamp - a.timestamp : a.timestamp - b.timestamp;
      } else if (sortBy === 'name') {
        return reverse ? b.filename.localeCompare(a.filename) : a.filename.localeCompare(b.filename);
      } else if (sortBy === 'size') {
        return reverse ? b.size - a.size : a.size - b.size;
      }
      return 0;
    });

    return snapshots;
  }

  /**
   * Get the latest snapshot path
   */
  getLatestSnapshotPath(): string | null {
    const latestPath = path.join(this.snapshotDir, 'latest.json');
    return fs.existsSync(latestPath) ? latestPath : null;
  }

  /**
   * Delete a snapshot
   */
  deleteSnapshot(filename: string): boolean {
    const filepath = path.join(this.snapshotDir, filename);
    if (fs.existsSync(filepath)) {
      fs.unlinkSync(filepath);
      return true;
    }
    return false;
  }

  /**
   * Get snapshot directory path
   */
  getSnapshotDir(): string {
    return this.snapshotDir;
  }

  /**
   * Get session prefix
   */
  getSessionPrefix(): string {
    return SESSION_PREFIX;
  }
}

// Export singleton instance
export const tmuxResurrect = new TmuxResurrect();

// Quick functions
export function snapshot(options?: ResurrectOptions): FullSnapshot {
  return tmuxResurrect.snapshot(options);
}

export function restore(snapshotPath?: string, options?: ResurrectOptions): { restored: number; failed: number } {
  return tmuxResurrect.restore(snapshotPath, options);
}

export function listSnapshots(options?: ListOptions): Array<{ filename: string; timestamp: number; size: number }> {
  return tmuxResurrect.listSnapshots(options);
}

export default {
  TmuxResurrect,
  tmuxResurrect,
  snapshot,
  restore,
  listSnapshots,
  SNAPSHOT_DIR
};
