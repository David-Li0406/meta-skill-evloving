import type { ExecSyncOptions } from 'node:child_process';
import { execSync as nodeExecSync } from 'node:child_process';
import { getGitConfig as defaultGetGitConfig } from './config';
import { createLogger } from './logger';

// Interface for dependency injection
export type ExecFunction = (command: string, options?: ExecSyncOptions & { encoding?: BufferEncoding }) => string;

export type GetGitConfigFunction = typeof defaultGetGitConfig;

// SDK interface for dependency injection
export interface ClaudeSDKInterface {
  generateCommitMessage(changes: string): Promise<string>;
  generateBranchName(taskTitle: string, taskId: string): Promise<string>;
}

const defaultExec: ExecFunction = (command, options) => {
  return nodeExecSync(command, { encoding: 'utf-8', ...options });
};

export class GitHelpers {
  private exec: ExecFunction;
  private getGitConfig: GetGitConfigFunction;
  private claudeSDK?: ClaudeSDKInterface;
  private logger: ReturnType<typeof createLogger>;

  constructor(
    exec?: ExecFunction,
    getGitConfig?: GetGitConfigFunction,
    claudeSDK?: ClaudeSDKInterface,
    logger?: ReturnType<typeof createLogger>,
  ) {
    this.exec = exec || defaultExec;
    this.getGitConfig = getGitConfig || defaultGetGitConfig;
    this.claudeSDK = claudeSDK;
    this.logger = logger || createLogger('git-helpers');
  }

  private async ensureClaudeSDK(): Promise<ClaudeSDKInterface> {
    if (this.claudeSDK) return this.claudeSDK;
    const mod = await import('./claude-sdk');
    // Type assertion is safe here - we're importing our own module with known exports
    this.claudeSDK = (mod as unknown as { ClaudeSDK: ClaudeSDKInterface }).ClaudeSDK;
    return this.claudeSDK;
  }

  /**
   * Get the default branch name (main or master)
   */
  getDefaultBranch(cwd: string): string {
    // First check if there's a configured default branch in track.config.json
    const gitConfig = this.getGitConfig();
    if (gitConfig?.defaultBranch) {
      this.logger.debug(`Default branch from track.config.json: ${gitConfig.defaultBranch}`);
      return gitConfig.defaultBranch;
    }

    // Try GitHub API if available (most reliable for GitHub repos)
    try {
      const ghOutput = this.exec('gh repo view --json defaultBranchRef', {
        cwd,
        stdio: ['pipe', 'pipe', 'ignore'], // Suppress stderr cross-platform
      }).trim();

      if (ghOutput) {
        const parsed = JSON.parse(ghOutput);
        const githubDefault = parsed?.defaultBranchRef?.name;
        if (githubDefault && githubDefault !== 'null') {
          this.logger.debug(`Default branch from GitHub API: ${githubDefault}`);
          return githubDefault;
        }
      }
    } catch {
      // GitHub CLI not available or not a GitHub repo
    }

    // Try git ls-remote to get the remote HEAD (more reliable than symbolic-ref)
    try {
      const lsRemoteOutput = this.exec('git ls-remote --symref origin HEAD', {
        cwd,
        stdio: ['pipe', 'pipe', 'ignore'], // Suppress stderr cross-platform
      }).trim();

      // Parse output: "ref: refs/heads/main\tHEAD" - extract branch name
      const firstLine = lsRemoteOutput.split('\n')[0] || '';
      const match = firstLine.match(/^ref: refs\/heads\/([^\t]+)/);
      if (match) {
        const remoteHead = match[1];
        this.logger.debug(`Default branch from git remote HEAD: ${remoteHead}`);
        return remoteHead;
      }
    } catch {
      // Fall through to next method
    }

    // Fallback to the old symbolic-ref method (kept for compatibility)
    try {
      const symbolicRef = this.exec('git symbolic-ref refs/remotes/origin/HEAD', {
        cwd,
        stdio: ['pipe', 'pipe', 'ignore'], // Suppress stderr cross-platform
      }).trim();

      // Parse output: "refs/remotes/origin/main" - extract branch name
      const prefix = 'refs/remotes/origin/';
      if (symbolicRef.startsWith(prefix)) {
        const defaultBranch = symbolicRef.slice(prefix.length);
        this.logger.debug(`Default branch from symbolic-ref: ${defaultBranch}`);
        return defaultBranch;
      }
    } catch {
      // Fall through to check git config
    }

    // Check git config for the default branch name
    try {
      const configDefault = this.exec('git config init.defaultBranch', { cwd }).trim();
      if (configDefault) {
        // Verify this branch actually exists
        try {
          this.exec(`git show-ref --verify --quiet refs/heads/${configDefault}`, { cwd });
          this.logger.debug(`Default branch from git config: ${configDefault}`);
          return configDefault;
        } catch {
          // Configured default doesn't exist, continue checking
        }
      }
    } catch {
      // No config set, fall through to check common defaults
    }

    // Check if main exists
    try {
      this.exec('git show-ref --verify --quiet refs/heads/main', { cwd });
      this.logger.debug('Default branch: main (exists locally)');
      return 'main';
    } catch {
      // Fall through to master
    }

    // Check if master exists
    try {
      this.exec('git show-ref --verify --quiet refs/heads/master', { cwd });
      this.logger.debug('Default branch: master (exists locally)');
      return 'master';
    } catch {
      // Default to main if neither exists (follows modern git convention)
      this.logger.debug('Default branch: main (fallback - no branch detected)');
      return 'main';
    }
  }

  /**
   * Check if there are uncommitted changes
   */
  hasUncommittedChanges(cwd: string): boolean {
    try {
      const status = this.exec('git status --porcelain', { cwd }).trim();
      return status.length > 0;
    } catch {
      return false;
    }
  }

  /**
   * Check if a commit message indicates a WIP commit
   */
  isWipCommit(commitLine: string): boolean {
    return commitLine.includes('[wip]') || Boolean(commitLine.match(/\s+wip:/));
  }

  /**
   * Get the merge base between two branches
   */
  getMergeBase(branch1: string, branch2: string, cwd: string): string {
    try {
      return this.exec(`git merge-base ${branch1} ${branch2}`, { cwd }).trim();
    } catch {
      return '';
    }
  }

  /**
   * Generate a commit message using Claude SDK with conventional commit format
   */
  async generateCommitMessage(diff: string, _cwd: string, taskId?: string): Promise<string> {
    const result = await this.generateCommitMessageWithMeta(diff, _cwd, taskId);
    return result.message;
  }

  /**
   * Generate a commit message with source metadata
   */
  async generateCommitMessageWithMeta(
    diff: string,
    _cwd: string,
    taskId?: string,
  ): Promise<{ message: string; source: 'sdk' | 'timeout' | 'error' }> {
    // Truncate diff if too long (Haiku has smaller context)
    const truncatedDiff = diff.substring(0, 3000);

    const taskContext = taskId ? `\nActive task: ${taskId}` : '';
    const changes = `${taskContext}\n\n${truncatedDiff}`;

    try {
      const fallbackMessage = 'chore: save work in progress';
      const timeoutMs = 10000; // Bounded SDK wait; hardcoded per project practice
      const sdkPromise = (async () => {
        const sdk = await this.ensureClaudeSDK();
        return sdk.generateCommitMessage(changes);
      })();
      const timeoutPromise = new Promise<string>((resolve) => {
        setTimeout(() => resolve(fallbackMessage), timeoutMs);
      });
      const message = await Promise.race<string>([sdkPromise, timeoutPromise]);

      // Extract just the commit message if Claude added any wrapper text
      // Look for a line that matches conventional commit format
      const lines = message.split('\n');
      for (const line of lines) {
        if (line.match(/^(feat|fix|docs|style|refactor|test|chore|build|ci|perf)(\([^)]+\))?:/)) {
          return { message: line, source: message === fallbackMessage ? 'timeout' : 'sdk' };
        }
      }

      // If no proper format found but we got something, use it
      if (message) {
        return { message, source: message === fallbackMessage ? 'timeout' : 'sdk' };
      }

      // Fallback if nothing works
      return { message: fallbackMessage, source: 'timeout' };
    } catch (error) {
      this.logger.error('Failed to generate commit message', { error });
      return { message: 'chore: save work in progress', source: 'error' };
    }
  }

  /**
   * Generate a branch name using Claude SDK
   */
  async generateBranchName(plan: string, taskId: string, _cwd: string): Promise<string> {
    // Extract key parts of the plan
    const planSummary = plan.substring(0, 1500);

    try {
      const sdk = await this.ensureClaudeSDK();
      const branchName = await sdk.generateBranchName(planSummary, taskId);

      // Extract just the branch name if Claude added any wrapper text
      const lines = branchName.split('\n');
      for (const line of lines) {
        if (line.match(/^(feature|bug)\//)) {
          // Add task ID if not already present
          if (!line.includes(taskId.toLowerCase())) {
            return `${line}-${taskId.toLowerCase()}`;
          }
          return line;
        }
      }

      // If we got something that looks like a branch name, use it
      if (branchName && !branchName.includes(' ')) {
        return branchName;
      }

      // Fallback to a generic name with task ID
      return `feature/task-${taskId.toLowerCase()}`;
    } catch (error) {
      this.logger.error('Failed to generate branch name', { error });
      // Fallback to a generic name with task ID
      return `feature/task-${taskId.toLowerCase()}`;
    }
  }

  /**
   * Check if a branch already exists (local or remote)
   */
  branchExists(branchName: string, cwd: string): boolean {
    try {
      // Check local branches
      const localResult = this.exec(`git branch --list ${branchName}`, { cwd });
      if (localResult.trim()) {
        return true;
      }
      // Check remote branches
      const remoteResult = this.exec(`git branch -r --list "origin/${branchName}"`, { cwd });
      return remoteResult.trim().length > 0;
    } catch {
      return false;
    }
  }

  /**
   * Create and switch to a new branch
   */
  createTaskBranch(branchName: string, cwd: string): void {
    try {
      // Create and switch to the new branch
      this.exec(`git checkout -b ${branchName}`, { cwd });
      this.logger.info(`Created and switched to branch: ${branchName}`);
    } catch (error) {
      this.logger.error(`Failed to create branch ${branchName}`, { error });
      throw error;
    }
  }

  /**
   * Merge a task branch back to the default branch
   */
  mergeTaskBranch(branchName: string, defaultBranch: string, cwd: string): void {
    try {
      // Switch to default branch
      this.exec(`git checkout ${defaultBranch}`, { cwd });

      // Merge the task branch
      this.exec(`git merge ${branchName} --no-ff -m "Merge branch '${branchName}'"`, { cwd });

      this.logger.info(`Merged ${branchName} into ${defaultBranch}`);
      // Note: Not deleting the branch per user request
    } catch (error) {
      this.logger.error(`Failed to merge branch ${branchName}`, { error });
      throw error;
    }
  }

  /**
   * Get the current branch name
   */
  getCurrentBranch(cwd: string): string {
    try {
      return this.exec('git branch --show-current', { cwd, stdio: ['pipe', 'pipe', 'ignore'] }).trim();
    } catch {
      return '';
    }
  }

  /**
   * Get the repository name from git remote URL or directory name
   */
  getRepoName(cwd: string): string {
    try {
      // Try to get repo name from git remote origin URL
      const remoteUrl = this.exec('git config --get remote.origin.url', {
        cwd,
        stdio: ['pipe', 'pipe', 'ignore'],
      }).trim();

      if (remoteUrl) {
        // Handle various URL formats:
        // https://github.com/owner/repo.git -> repo
        // git@github.com:owner/repo.git -> repo
        // https://github.com/owner/repo -> repo
        const match = remoteUrl.match(/\/([^/]+?)(?:\.git)?$/);
        if (match) {
          return match[1];
        }
      }
    } catch {
      // Fall through to directory name fallback
    }

    // Fallback: use the directory name
    try {
      const topLevel = this.exec('git rev-parse --show-toplevel', {
        cwd,
        stdio: ['pipe', 'pipe', 'ignore'],
      }).trim();
      if (topLevel) {
        // Extract directory name from path (works on both Windows and Unix)
        const parts = topLevel.split(/[/\\]/);
        return parts[parts.length - 1] || '';
      }
    } catch {
      // Not a git repo or other error
    }

    return '';
  }

  /**
   * Switch to a branch
   */
  switchToBranch(branchName: string, cwd: string): void {
    try {
      this.exec(`git checkout ${branchName}`, { cwd });
      this.logger.info(`Switched to branch: ${branchName}`);
    } catch (error) {
      this.logger.error(`Failed to switch to branch ${branchName}`, { error });
      throw error;
    }
  }
}

// Create a default instance for backward compatibility with the few functions still in use
let _defaultGitHelpers: GitHelpers | null = null;
function getDefaultGitHelpers(): GitHelpers {
  if (!_defaultGitHelpers) _defaultGitHelpers = new GitHelpers();
  return _defaultGitHelpers;
}

// Keep only the standalone functions that are actually used
export function getDefaultBranch(cwd: string): string {
  return getDefaultGitHelpers().getDefaultBranch(cwd);
}

export function getCurrentBranch(cwd: string): string {
  return getDefaultGitHelpers().getCurrentBranch(cwd);
}

export function getRepoName(cwd: string): string {
  return getDefaultGitHelpers().getRepoName(cwd);
}

export function isWipCommit(commitLine: string): boolean {
  return getDefaultGitHelpers().isWipCommit(commitLine);
}

export function getMergeBase(branch1: string, branch2: string, cwd: string): string {
  return getDefaultGitHelpers().getMergeBase(branch1, branch2, cwd);
}
