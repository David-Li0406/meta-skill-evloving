import { beforeEach, describe, expect, mock, test } from 'bun:test';
import type { ExecFunction } from './github-helpers';
import { GitHubHelpers } from './github-helpers';

describe('GitHubHelpers', () => {
  let mockExec: ExecFunction;
  let gitHubHelpers: GitHubHelpers;

  beforeEach(() => {
    mockExec = mock(() => '');
    gitHubHelpers = new GitHubHelpers(mockExec);
  });

  describe('isGitHubCLIAvailable', () => {
    test('returns true when gh is available', () => {
      mockExec = mock(() => 'gh version 2.34.0');
      gitHubHelpers = new GitHubHelpers(mockExec);

      expect(gitHubHelpers.isGitHubCLIAvailable()).toBe(true);
    });

    test('returns false when gh is not available', () => {
      mockExec = mock(() => {
        throw new Error('command not found');
      });
      gitHubHelpers = new GitHubHelpers(mockExec);

      expect(gitHubHelpers.isGitHubCLIAvailable()).toBe(false);
    });
  });

  describe('isGitHubRepoConnected', () => {
    test('returns true when repo is connected', () => {
      mockExec = mock(() => 'repo info');
      gitHubHelpers = new GitHubHelpers(mockExec);

      expect(gitHubHelpers.isGitHubRepoConnected('/test')).toBe(true);
    });

    test('returns false when repo is not connected', () => {
      mockExec = mock(() => {
        throw new Error('no remote');
      });
      gitHubHelpers = new GitHubHelpers(mockExec);

      expect(gitHubHelpers.isGitHubRepoConnected('/test')).toBe(false);
    });
  });

  describe('getGitHubRepoInfo', () => {
    test('returns repo info when available', () => {
      mockExec = mock(() =>
        JSON.stringify({
          owner: { login: 'testuser' },
          name: 'testrepo',
        }),
      );
      gitHubHelpers = new GitHubHelpers(mockExec);

      const info = gitHubHelpers.getGitHubRepoInfo('/test');
      expect(info).toEqual({
        owner: 'testuser',
        repo: 'testrepo',
      });
    });

    test('returns null on error', () => {
      mockExec = mock(() => {
        throw new Error('not a repo');
      });
      gitHubHelpers = new GitHubHelpers(mockExec);

      const info = gitHubHelpers.getGitHubRepoInfo('/test');
      expect(info).toBeNull();
    });
  });

  describe('createGitHubIssue', () => {
    test('creates issue and returns data', () => {
      mockExec = mock(() => 'https://github.com/user/repo/issues/123\n');
      gitHubHelpers = new GitHubHelpers(mockExec);

      const issue = gitHubHelpers.createGitHubIssue('Test Issue', 'Body', '/test');

      expect(issue).toEqual({
        number: 123,
        title: 'Test Issue',
        url: 'https://github.com/user/repo/issues/123',
        state: 'open',
      });
    });

    test('returns null when URL extraction fails', () => {
      mockExec = mock(() => 'invalid output');
      gitHubHelpers = new GitHubHelpers(mockExec);

      const issue = gitHubHelpers.createGitHubIssue('Test', 'Body', '/test');
      expect(issue).toBeNull();
    });

    test('returns null on error', () => {
      mockExec = mock(() => {
        throw new Error('API error');
      });
      gitHubHelpers = new GitHubHelpers(mockExec);

      const issue = gitHubHelpers.createGitHubIssue('Test', 'Body', '/test');
      expect(issue).toBeNull();
    });
  });

  describe('createIssueBranch', () => {
    test('creates branch and returns name', () => {
      let callCount = 0;
      mockExec = mock(() => {
        callCount++;
        if (callCount === 1) return ''; // gh issue develop
        return 'feature/issue-123\n'; // git branch --show-current
      });
      gitHubHelpers = new GitHubHelpers(mockExec);

      const branch = gitHubHelpers.createIssueBranch(123, '/test');
      expect(branch).toBe('feature/issue-123');
    });

    test('returns null on error', () => {
      mockExec = mock(() => {
        throw new Error('Issue not found');
      });
      gitHubHelpers = new GitHubHelpers(mockExec);

      const branch = gitHubHelpers.createIssueBranch(123, '/test');
      expect(branch).toBeNull();
    });
  });

  describe('getIssue', () => {
    test('fetches issue by number and returns data', () => {
      const issueData = {
        number: 42,
        title: 'Test Issue',
        body: 'Issue description',
        url: 'https://github.com/user/repo/issues/42',
        state: 'open',
        labels: [{ name: 'bug' }, { name: 'high-priority' }],
        assignees: [{ login: 'user1' }],
        milestone: { title: 'v1.0.0' },
      };
      mockExec = mock(() => JSON.stringify(issueData));
      gitHubHelpers = new GitHubHelpers(mockExec);

      const issue = gitHubHelpers.getIssue(42, '/test');

      expect(issue).toEqual(issueData);
      expect(mockExec).toHaveBeenCalledWith(expect.stringContaining('gh issue view 42 --json'), { cwd: '/test' });
    });

    test('fetches issue by URL and returns data', () => {
      const issueData = {
        number: 99,
        title: 'URL Issue',
        body: 'From URL',
        url: 'https://github.com/user/repo/issues/99',
        state: 'closed',
      };
      mockExec = mock(() => JSON.stringify(issueData));
      gitHubHelpers = new GitHubHelpers(mockExec);

      const issue = gitHubHelpers.getIssue('https://github.com/user/repo/issues/99', '/test');

      expect(issue).toEqual(issueData);
      expect(mockExec).toHaveBeenCalledWith(expect.stringContaining('gh issue view 99 --json'), { cwd: '/test' });
    });

    test('returns null when issue number extraction fails from URL', () => {
      mockExec = mock(() => '');
      gitHubHelpers = new GitHubHelpers(mockExec);

      const issue = gitHubHelpers.getIssue('invalid-url', '/test');
      expect(issue).toBeNull();
    });

    test('returns null when gh command fails', () => {
      mockExec = mock(() => {
        throw new Error('Issue not found');
      });
      gitHubHelpers = new GitHubHelpers(mockExec);

      const issue = gitHubHelpers.getIssue(404, '/test');
      expect(issue).toBeNull();
    });

    test('returns null when JSON parsing fails', () => {
      mockExec = mock(() => 'invalid json');
      gitHubHelpers = new GitHubHelpers(mockExec);

      const issue = gitHubHelpers.getIssue(1, '/test');
      expect(issue).toBeNull();
    });
  });

  describe('createPullRequest', () => {
    test('creates PR and returns data', () => {
      mockExec = mock(() => 'https://github.com/user/repo/pull/456\n');
      gitHubHelpers = new GitHubHelpers(mockExec);

      const pr = gitHubHelpers.createPullRequest('Test PR', 'Body', '/test');

      expect(pr).toEqual({
        number: 456,
        title: 'Test PR',
        url: 'https://github.com/user/repo/pull/456',
        body: 'Body',
      });
    });

    test('includes draft flag when specified', () => {
      let capturedCommand = '';
      mockExec = mock((command: string) => {
        capturedCommand = command;
        return 'https://github.com/user/repo/pull/789\n';
      });
      gitHubHelpers = new GitHubHelpers(mockExec);

      gitHubHelpers.createPullRequest('Draft PR', 'Body', '/test', true);
      expect(capturedCommand).toContain('--draft');
    });

    test('returns null on error', () => {
      mockExec = mock(() => {
        throw new Error('PR creation failed');
      });
      gitHubHelpers = new GitHubHelpers(mockExec);

      const pr = gitHubHelpers.createPullRequest('Test', 'Body', '/test');
      expect(pr).toBeNull();
    });
  });

  describe('pushCurrentBranch', () => {
    test('returns true on simple push success', () => {
      let callCount = 0;
      mockExec = mock((cmd: string) => {
        callCount++;
        if (cmd.includes('git branch --show-current')) return 'feature-branch\n';
        if (cmd.includes('git fetch')) return '';
        if (cmd.includes('git status -sb')) return '## feature-branch...origin/feature-branch';
        if (cmd.includes('git push')) return '';
        return '';
      });
      gitHubHelpers = new GitHubHelpers(mockExec);

      expect(gitHubHelpers.pushCurrentBranch('/test')).toBe(true);
      expect(callCount).toBe(4); // branch, fetch, status, push
    });

    test('handles diverged branches with successful rebase', () => {
      let callCount = 0;
      mockExec = mock((cmd: string) => {
        callCount++;
        if (cmd.includes('git branch --show-current')) return 'feature-branch\n';
        if (cmd.includes('git fetch')) return '';
        if (cmd.includes('git status -sb'))
          return "## feature-branch...origin/feature-branch [ahead 1, behind 2]\nYour branch and 'origin/feature-branch' have diverged";
        if (cmd.includes('git pull --rebase')) return 'Successfully rebased and updated';
        if (cmd.includes('git push')) return '';
        return '';
      });
      gitHubHelpers = new GitHubHelpers(mockExec);

      expect(gitHubHelpers.pushCurrentBranch('/test')).toBe(true);
      expect(callCount).toBe(5); // branch, fetch, status, rebase, push
    });

    test('handles behind branch with successful rebase', () => {
      let callCount = 0;
      mockExec = mock((cmd: string) => {
        callCount++;
        if (cmd.includes('git branch --show-current')) return 'feature-branch\n';
        if (cmd.includes('git fetch')) return '';
        if (cmd.includes('git status -sb')) return '## feature-branch...origin/feature-branch [behind 2]';
        if (cmd.includes('git pull --rebase')) return 'Successfully rebased and updated';
        if (cmd.includes('git push')) return '';
        return '';
      });
      gitHubHelpers = new GitHubHelpers(mockExec);

      expect(gitHubHelpers.pushCurrentBranch('/test')).toBe(true);
      expect(callCount).toBe(5); // branch, fetch, status, rebase, push
    });

    test('handles rebase conflicts and aborts gracefully', () => {
      let callCount = 0;
      mockExec = mock((cmd: string, _options?: any) => {
        callCount++;
        if (cmd.includes('git branch --show-current')) return 'feature-branch\n';
        if (cmd.includes('git fetch')) return '';
        if (cmd.includes('git status -sb'))
          return "## feature-branch...origin/feature-branch [ahead 1, behind 2]\nYour branch and 'origin/feature-branch' have diverged";
        if (cmd.includes('git pull --rebase')) throw new Error('Merge conflict');
        if (cmd.includes('git status') && !cmd.includes('-sb')) return 'rebase in progress; onto abc123';
        if (cmd.includes('git rebase --abort')) return '';
        return '';
      });
      gitHubHelpers = new GitHubHelpers(mockExec);

      expect(gitHubHelpers.pushCurrentBranch('/test')).toBe(false);
      expect(callCount).toBe(6); // branch, fetch, status, rebase (fails), status check, abort
    });

    test('returns false on push error', () => {
      mockExec = mock((cmd: string) => {
        if (cmd.includes('git branch --show-current')) return 'feature-branch\n';
        if (cmd.includes('git fetch')) return '';
        if (cmd.includes('git status -sb')) return '## feature-branch...origin/feature-branch';
        if (cmd.includes('git push')) throw new Error('Push failed');
        return '';
      });
      gitHubHelpers = new GitHubHelpers(mockExec);

      expect(gitHubHelpers.pushCurrentBranch('/test')).toBe(false);
    });

    test('returns false on fetch error', () => {
      mockExec = mock((cmd: string) => {
        if (cmd.includes('git branch --show-current')) return 'feature-branch\n';
        if (cmd.includes('git fetch')) throw new Error('Network error');
        return '';
      });
      gitHubHelpers = new GitHubHelpers(mockExec);

      expect(gitHubHelpers.pushCurrentBranch('/test')).toBe(false);
    });
  });

  describe('validateGitHubIntegration', () => {
    test('returns valid when all checks pass', () => {
      mockExec = mock(() => 'success');
      gitHubHelpers = new GitHubHelpers(mockExec);

      const result = gitHubHelpers.validateGitHubIntegration('/test');
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    test('reports missing gh CLI', () => {
      let callCount = 0;
      mockExec = mock((command: string) => {
        callCount++;
        if (callCount === 1 && command.includes('--version')) {
          throw new Error('not found');
        }
        return '';
      });
      gitHubHelpers = new GitHubHelpers(mockExec);

      const result = gitHubHelpers.validateGitHubIntegration('/test');
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('GitHub CLI (gh) is not installed or not available in PATH');
    });

    test('reports auth issues', () => {
      const _callCount = 0;
      mockExec = mock((command: string) => {
        if (command.includes('auth status')) {
          throw new Error('not authenticated');
        }
        return '';
      });
      gitHubHelpers = new GitHubHelpers(mockExec);

      const result = gitHubHelpers.validateGitHubIntegration('/test');
      expect(result.errors).toContain('GitHub CLI is not authenticated. Run: gh auth login');
    });

    test('reports disconnected repo', () => {
      mockExec = mock((command: string) => {
        if (command.includes('repo view')) {
          throw new Error('no remote');
        }
        return '';
      });
      gitHubHelpers = new GitHubHelpers(mockExec);

      const result = gitHubHelpers.validateGitHubIntegration('/test');
      expect(result.errors).toContain('Repository is not connected to GitHub');
    });
  });

  describe('formatTaskForGitHub', () => {
    test('extracts title from heading', () => {
      const content = '# Task Title\n\nTask description\nMore details';
      const result = gitHubHelpers.formatTaskForGitHub(content);

      expect(result.title).toBe('Task Title');
      expect(result.body).toBe('Task description\nMore details');
    });

    test('uses first line as title when no heading', () => {
      const content = 'Task Title\n\nTask description';
      const result = gitHubHelpers.formatTaskForGitHub(content);

      expect(result.title).toBe('Task Title');
      expect(result.body).toBe('Task description');
    });

    test('handles empty content', () => {
      const result = gitHubHelpers.formatTaskForGitHub('');

      expect(result.title).toBe('New Task');
      expect(result.body).toBe('');
    });
  });
});
