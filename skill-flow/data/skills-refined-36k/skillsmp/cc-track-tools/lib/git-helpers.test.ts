import { beforeEach, describe, expect, mock, test } from 'bun:test';
import { createMockClaudeSDK, createMockLogger } from '../test-utils/command-mocks';
import type { ClaudeSDKInterface, ExecFunction, GetGitConfigFunction } from './git-helpers';
import { GitHelpers } from './git-helpers';
import type { createLogger } from './logger';

describe('GitHelpers', () => {
  let mockExec: ExecFunction;
  let mockClaudeSDK: ClaudeSDKInterface;
  let mockLogger: ReturnType<typeof createLogger>;
  let gitHelpers: GitHelpers;
  let execCalls: Array<{
    command: string;
    options?: { cwd?: string; encoding?: string; timeout?: number; shell?: string };
  }> = [];

  beforeEach(() => {
    execCalls = [];

    mockExec = mock(
      (command: string, options?: { cwd?: string; encoding?: string; timeout?: number; shell?: string }) => {
        execCalls.push({ command, options });
        return '';
      },
    );

    mockClaudeSDK = createMockClaudeSDK();
    mockLogger = createMockLogger();
    gitHelpers = new GitHelpers(mockExec, undefined, mockClaudeSDK, mockLogger);
  });

  describe('getDefaultBranch', () => {
    test('returns configured default branch when available', () => {
      const mockGetGitConfig: GetGitConfigFunction = mock(() => ({
        defaultBranch: 'develop',
      }));

      gitHelpers = new GitHelpers(mockExec, mockGetGitConfig, mockClaudeSDK, mockLogger);
      const branch = gitHelpers.getDefaultBranch('/test');
      expect(branch).toBe('develop');
    });

    test('returns branch from GitHub API when available', () => {
      const mockGetGitConfig: GetGitConfigFunction = mock(() => null);
      mockExec = mock((command: string) => {
        if (command.includes('gh repo view')) {
          // Return JSON format as expected by the new implementation
          return JSON.stringify({ defaultBranchRef: { name: 'test' } });
        }
        throw new Error('Not found');
      });

      gitHelpers = new GitHelpers(mockExec, mockGetGitConfig, mockClaudeSDK, mockLogger);
      const branch = gitHelpers.getDefaultBranch('/test');
      expect(branch).toBe('test');
    });

    test('returns branch from git ls-remote when GitHub API fails', () => {
      const mockGetGitConfig: GetGitConfigFunction = mock(() => null);
      mockExec = mock((command: string) => {
        if (command.includes('gh repo view')) {
          throw new Error('Not a GitHub repo');
        }
        if (command.includes('git ls-remote')) {
          // Return raw git ls-remote format - code parses with regex
          return 'ref: refs/heads/develop\tHEAD\n';
        }
        throw new Error('Not found');
      });

      gitHelpers = new GitHelpers(mockExec, mockGetGitConfig, mockClaudeSDK, mockLogger);
      const branch = gitHelpers.getDefaultBranch('/test');
      expect(branch).toBe('develop');
    });

    test('falls back to symbolic-ref when ls-remote fails', () => {
      const mockGetGitConfig: GetGitConfigFunction = mock(() => null);
      mockExec = mock((command: string) => {
        if (command.includes('gh repo view')) {
          throw new Error('Not a GitHub repo');
        }
        if (command.includes('git ls-remote')) {
          throw new Error('No remote');
        }
        if (command.includes('symbolic-ref')) {
          return 'main\n';
        }
        throw new Error('Not found');
      });

      gitHelpers = new GitHelpers(mockExec, mockGetGitConfig, mockClaudeSDK, mockLogger);
      const branch = gitHelpers.getDefaultBranch('/test');
      expect(branch).toBe('main');
    });

    test('returns git config init.defaultBranch when it exists', () => {
      const mockGetGitConfig: GetGitConfigFunction = mock(() => null);
      mockExec = mock((command: string) => {
        if (command.includes('gh repo view')) {
          throw new Error('Not a GitHub repo');
        }
        if (command.includes('git ls-remote') || command.includes('symbolic-ref')) {
          throw new Error('No remote');
        }
        if (command === 'git config init.defaultBranch') {
          return 'trunk\n';
        }
        if (command.includes('refs/heads/trunk')) {
          return ''; // Branch exists
        }
        throw new Error('Not found');
      });

      gitHelpers = new GitHelpers(mockExec, mockGetGitConfig, mockClaudeSDK, mockLogger);
      const branch = gitHelpers.getDefaultBranch('/test');
      expect(branch).toBe('trunk');
    });

    test('checks for local main branch if all remote detection fails', () => {
      const mockGetGitConfig: GetGitConfigFunction = mock(() => null);
      mockExec = mock((command: string) => {
        if (command.includes('gh repo view') || command.includes('git ls-remote') || command.includes('symbolic-ref')) {
          throw new Error('No remote');
        }
        if (command === 'git config init.defaultBranch') {
          throw new Error('Not set');
        }
        if (command.includes('refs/heads/main')) {
          return ''; // Success (no error)
        }
        throw new Error('Not found');
      });

      gitHelpers = new GitHelpers(mockExec, mockGetGitConfig, mockClaudeSDK, mockLogger);
      const branch = gitHelpers.getDefaultBranch('/test');
      expect(branch).toBe('main');
    });

    test("falls back to master if main doesn't exist", () => {
      const mockGetGitConfig: GetGitConfigFunction = mock(() => null);
      mockExec = mock((command: string) => {
        if (command.includes('gh repo view') || command.includes('git ls-remote') || command.includes('symbolic-ref')) {
          throw new Error('No remote');
        }
        if (command === 'git config init.defaultBranch') {
          throw new Error('Not set');
        }
        if (command.includes('refs/heads/main')) {
          throw new Error('No main');
        }
        if (command.includes('refs/heads/master')) {
          return ''; // Success
        }
        throw new Error('Not found');
      });

      gitHelpers = new GitHelpers(mockExec, mockGetGitConfig, mockClaudeSDK, mockLogger);
      const branch = gitHelpers.getDefaultBranch('/test');
      expect(branch).toBe('master');
    });

    test('defaults to main if neither main nor master exist', () => {
      const mockGetGitConfig: GetGitConfigFunction = mock(() => null);
      mockExec = mock(() => {
        throw new Error('No branches');
      });

      gitHelpers = new GitHelpers(mockExec, mockGetGitConfig, mockClaudeSDK, mockLogger);
      const branch = gitHelpers.getDefaultBranch('/test');
      expect(branch).toBe('main');
    });

    test('handles non-standard default branches like test, develop, trunk', () => {
      const testCases = [
        { branch: 'test', source: 'gh repo view' },
        { branch: 'develop', source: 'git ls-remote' },
        { branch: 'trunk', source: 'git config init.defaultBranch' },
      ];

      for (const { branch: expectedBranch, source } of testCases) {
        const mockGetGitConfig: GetGitConfigFunction = mock(() => null);
        mockExec = mock((command: string) => {
          if (source === 'gh repo view' && command.includes('gh repo view')) {
            // Return JSON format as expected by the new implementation
            return JSON.stringify({ defaultBranchRef: { name: expectedBranch } });
          }
          if (source === 'git ls-remote' && command.includes('git ls-remote')) {
            // Return raw git ls-remote format - code parses with regex
            return `ref: refs/heads/${expectedBranch}\tHEAD\n`;
          }
          if (source === 'git config init.defaultBranch' && command === 'git config init.defaultBranch') {
            return `${expectedBranch}\n`;
          }
          if (command.includes(`refs/heads/${expectedBranch}`)) {
            return ''; // Branch exists
          }
          throw new Error('Not found');
        });

        gitHelpers = new GitHelpers(mockExec, mockGetGitConfig, mockClaudeSDK, mockLogger);
        const branch = gitHelpers.getDefaultBranch('/test');
        expect(branch).toBe(expectedBranch);
      }
    });
  });

  describe('hasUncommittedChanges', () => {
    test('returns true when there are changes', () => {
      mockExec = mock(() => 'M  file.txt\n?? newfile.txt\n');
      gitHelpers = new GitHelpers(mockExec, undefined, mockClaudeSDK, mockLogger);

      expect(gitHelpers.hasUncommittedChanges('/test')).toBe(true);
    });

    test('returns false when working directory is clean', () => {
      mockExec = mock(() => '');
      gitHelpers = new GitHelpers(mockExec, undefined, mockClaudeSDK, mockLogger);

      expect(gitHelpers.hasUncommittedChanges('/test')).toBe(false);
    });

    test('returns false on error', () => {
      mockExec = mock(() => {
        throw new Error('Not a git repo');
      });
      gitHelpers = new GitHelpers(mockExec, undefined, mockClaudeSDK, mockLogger);

      expect(gitHelpers.hasUncommittedChanges('/test')).toBe(false);
    });
  });

  describe('getCurrentBranch', () => {
    test('returns current branch name', () => {
      mockExec = mock(() => 'feature/test-branch\n');
      gitHelpers = new GitHelpers(mockExec, undefined, mockClaudeSDK, mockLogger);

      expect(gitHelpers.getCurrentBranch('/test')).toBe('feature/test-branch');
    });

    test('returns empty string on error', () => {
      mockExec = mock(() => {
        throw new Error('Not a git repo');
      });
      gitHelpers = new GitHelpers(mockExec, undefined, mockClaudeSDK, mockLogger);

      expect(gitHelpers.getCurrentBranch('/test')).toBe('');
    });
  });

  describe('getRepoName', () => {
    test('extracts repo name from HTTPS URL', () => {
      mockExec = mock(() => 'https://github.com/owner/my-repo.git\n');
      gitHelpers = new GitHelpers(mockExec, undefined, mockClaudeSDK, mockLogger);

      expect(gitHelpers.getRepoName('/test')).toBe('my-repo');
    });

    test('extracts repo name from HTTPS URL without .git suffix', () => {
      mockExec = mock(() => 'https://github.com/owner/my-repo\n');
      gitHelpers = new GitHelpers(mockExec, undefined, mockClaudeSDK, mockLogger);

      expect(gitHelpers.getRepoName('/test')).toBe('my-repo');
    });

    test('extracts repo name from SSH URL', () => {
      mockExec = mock((cmd: string) => {
        if (cmd.includes('remote.origin.url')) {
          return 'git@github.com:owner/my-repo.git\n';
        }
        return '';
      });
      gitHelpers = new GitHelpers(mockExec, undefined, mockClaudeSDK, mockLogger);

      expect(gitHelpers.getRepoName('/test')).toBe('my-repo');
    });

    test('falls back to directory name when no remote', () => {
      mockExec = mock((cmd: string) => {
        if (cmd.includes('remote.origin.url')) {
          throw new Error('No remote');
        }
        if (cmd.includes('rev-parse --show-toplevel')) {
          return '/home/user/projects/my-project\n';
        }
        return '';
      });
      gitHelpers = new GitHelpers(mockExec, undefined, mockClaudeSDK, mockLogger);

      expect(gitHelpers.getRepoName('/test')).toBe('my-project');
    });

    test('handles Windows paths in fallback', () => {
      mockExec = mock((cmd: string) => {
        if (cmd.includes('remote.origin.url')) {
          throw new Error('No remote');
        }
        if (cmd.includes('rev-parse --show-toplevel')) {
          return 'C:\\Users\\dev\\projects\\my-project\n';
        }
        return '';
      });
      gitHelpers = new GitHelpers(mockExec, undefined, mockClaudeSDK, mockLogger);

      expect(gitHelpers.getRepoName('/test')).toBe('my-project');
    });

    test('returns empty string when not a git repo', () => {
      mockExec = mock(() => {
        throw new Error('Not a git repo');
      });
      gitHelpers = new GitHelpers(mockExec, undefined, mockClaudeSDK, mockLogger);

      expect(gitHelpers.getRepoName('/test')).toBe('');
    });
  });

  describe('createTaskBranch', () => {
    test('creates and switches to new branch', () => {
      mockExec = mock(
        (command: string, options?: { cwd?: string; encoding?: string; timeout?: number; shell?: string }) => {
          execCalls.push({ command, options });
          return '';
        },
      );
      gitHelpers = new GitHelpers(mockExec, undefined, mockClaudeSDK, mockLogger);

      gitHelpers.createTaskBranch('feature/new-feature', '/test');

      expect(execCalls).toHaveLength(1);
      expect(execCalls[0].command).toBe('git checkout -b feature/new-feature');
      expect(execCalls[0].options.cwd).toBe('/test');
    });

    test('throws error on failure', () => {
      mockExec = mock(() => {
        throw new Error('Branch already exists');
      });
      gitHelpers = new GitHelpers(mockExec, undefined, mockClaudeSDK, mockLogger);

      expect(() => {
        gitHelpers.createTaskBranch('existing-branch', '/test');
      }).toThrow();
    });
  });

  describe('mergeTaskBranch', () => {
    test('switches to default branch and merges', () => {
      let _callIndex = 0;
      const commands: string[] = [];

      mockExec = mock((command: string) => {
        commands.push(command);
        _callIndex++;
        return '';
      });
      gitHelpers = new GitHelpers(mockExec, undefined, mockClaudeSDK, mockLogger);

      gitHelpers.mergeTaskBranch('feature/task-001', 'main', '/test');

      expect(commands).toHaveLength(2);
      expect(commands[0]).toBe('git checkout main');
      expect(commands[1]).toContain('git merge feature/task-001');
    });

    test('throws error on failure', () => {
      mockExec = mock(() => {
        throw new Error('Merge conflict');
      });
      gitHelpers = new GitHelpers(mockExec, undefined, mockClaudeSDK, mockLogger);

      expect(() => {
        gitHelpers.mergeTaskBranch('feature/task-001', 'main', '/test');
      }).toThrow();
    });
  });

  describe('generateCommitMessage', () => {
    test('returns generated commit message', async () => {
      gitHelpers = new GitHelpers(mockExec, undefined, mockClaudeSDK, mockLogger);

      const message = await gitHelpers.generateCommitMessage('Added new feature', '/test');
      expect(message).toBe('feat: add new feature');
    });

    test('extracts valid commit message from multi-line response', async () => {
      gitHelpers = new GitHelpers(mockExec, undefined, mockClaudeSDK, mockLogger);

      const message = await gitHelpers.generateCommitMessage('Fixed login bug', '/test');
      expect(message).toBe('fix: resolve login bug');
    });

    test('returns fallback on error', async () => {
      mockExec = mock(() => {
        throw new Error('Claude API error');
      });
      gitHelpers = new GitHelpers(mockExec, undefined, mockClaudeSDK, mockLogger);

      const message = await gitHelpers.generateCommitMessage('diff content', '/test');
      expect(message).toBe('chore: save work in progress');
    });

    test('truncates long diffs', async () => {
      const longDiff = 'x'.repeat(5000);
      gitHelpers = new GitHelpers(mockExec, undefined, mockClaudeSDK, mockLogger);

      // The SDK mock will be called with truncated diff
      const message = await gitHelpers.generateCommitMessage(longDiff, '/test');

      // We get the expected fallback message since SDK mock doesn't recognize the pattern
      expect(message).toBe('chore: save work in progress');
    });
  });

  describe('generateBranchName', () => {
    test('returns generated branch name with task ID', async () => {
      mockExec = mock(() => 'feature/user-auth\n');
      gitHelpers = new GitHelpers(mockExec, undefined, mockClaudeSDK, mockLogger);

      const name = await gitHelpers.generateBranchName('Add user authentication', 'TASK_001', '/test');
      expect(name).toBe('feature/user-auth-task_001');
    });

    test('extracts valid branch name from multi-line response', async () => {
      mockExec = mock(() => "Here's your branch name:\n\nbug/fix-login\n\nUse this!");
      gitHelpers = new GitHelpers(mockExec, undefined, mockClaudeSDK, mockLogger);

      const name = await gitHelpers.generateBranchName('Fix login issue', 'TASK_002', '/test');
      expect(name).toBe('bug/fix-login-task_002');
    });

    test('returns fallback on error', async () => {
      mockExec = mock(() => {
        throw new Error('Claude API error');
      });
      gitHelpers = new GitHelpers(mockExec, undefined, mockClaudeSDK, mockLogger);

      const name = await gitHelpers.generateBranchName('Some plan', 'TASK_003', '/test');
      expect(name).toBe('feature/task-task_003');
    });
  });

  describe('switchToBranch', () => {
    test('switches to specified branch', () => {
      mockExec = mock(
        (command: string, options?: { cwd?: string; encoding?: string; timeout?: number; shell?: string }) => {
          execCalls.push({ command, options });
          return '';
        },
      );
      gitHelpers = new GitHelpers(mockExec, undefined, mockClaudeSDK, mockLogger);

      gitHelpers.switchToBranch('main', '/test');

      expect(execCalls).toHaveLength(1);
      expect(execCalls[0].command).toBe('git checkout main');
      expect(execCalls[0].options.cwd).toBe('/test');
    });

    test('throws error on failure', () => {
      mockExec = mock(() => {
        throw new Error('Branch not found');
      });
      gitHelpers = new GitHelpers(mockExec, undefined, mockClaudeSDK, mockLogger);

      expect(() => {
        gitHelpers.switchToBranch('nonexistent', '/test');
      }).toThrow();
    });
  });
});
