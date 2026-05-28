import { beforeEach, describe, expect, mock, test } from 'bun:test';
import type { SpecifyDeps, SpecifyOptions, SpecifyResultData } from './specify';
import { runSpecify } from './specify';

function createMockDeps(overrides: Partial<SpecifyDeps> = {}): SpecifyDeps {
  const files = new Map<string, string>();
  const createdDirs = new Set<string>();

  // Default CLAUDE.md content with no_active_task reference
  files.set('/project/CLAUDE.md', '# Project\n\n## Active Task\n@.cc-track/no_active_task.md\n');
  // Mark .cc-track directory as existing
  createdDirs.add('/project/.cc-track');
  createdDirs.add('/project/.cc-track/specs');

  return {
    cwd: () => '/project',
    fs: {
      existsSync: mock((path: string) => files.has(path) || createdDirs.has(path)),
      readFileSync: mock((path: string) => files.get(path) || ''),
      writeFileSync: mock((path: string, content: string) => {
        files.set(path, content);
      }),
      mkdirSync: mock((path: string) => {
        createdDirs.add(path);
      }),
    },
    path: {
      join: (...args: string[]) => args.join('/').replace(/\/+/g, '/'),
    },
    time: {
      nowISO: () => '2025-01-15T12:00:00Z',
      todayISO: () => '2025-01-15',
    },
    logger: mock(() => ({
      info: mock(() => {}),
      warn: mock(() => {}),
      error: mock(() => {}),
      debug: mock(() => {}),
    })),
    specHelpers: {
      getNextTaskId: mock(() => '001'),
      generateFeatureName: mock((title: string) =>
        title
          .toLowerCase()
          .replace(/[^a-z0-9]+/g, '-')
          .replace(/^-|-$/g, '')
          .substring(0, 50),
      ),
      createSpecDirectory: mock(
        (_projectRoot: string, taskId: string, featureName: string) =>
          `/project/.cc-track/specs/${taskId}-${featureName}`,
      ),
      createMetadata: mock(() => {}),
    },
    git: {
      createTaskBranch: mock(() => {}),
      getCurrentBranch: mock(() => 'main'),
      branchExists: mock(() => false),
    },
    github: {
      createGitHubIssue: mock(() => ({ number: 42, url: 'https://github.com/test/repo/issues/42' })),
    },
    config: {
      isGitHubIntegrationEnabled: mock(() => false),
    },
    ...overrides,
  };
}

describe('specify script', () => {
  beforeEach(() => {
    mock.restore();
  });

  // T002: Test happy path - creates branch, folder, metadata, updates CLAUDE.md
  describe('T002: happy path', () => {
    test('creates branch, folder, metadata, and updates CLAUDE.md', () => {
      const deps = createMockDeps();
      const options: SpecifyOptions = { title: 'Add user authentication' };

      const result = runSpecify(options, deps);

      expect(result.success).toBe(true);
      expect(result.data).toBeDefined();

      const data = result.data as SpecifyResultData;
      expect(data.taskId).toBe('001');
      expect(data.featureName).toBe('add-user-authentication');
      expect(data.branch).toBe('001-add-user-authentication');
      expect(data.specDir).toBe('/project/.cc-track/specs/001-add-user-authentication');
      expect(data.claudeMdUpdated).toBe(true);

      // Verify git branch was created
      expect(deps.git.createTaskBranch).toHaveBeenCalledWith('001-add-user-authentication', '/project');

      // Verify spec directory was created
      expect(deps.specHelpers.createSpecDirectory).toHaveBeenCalledWith(
        '/project',
        '001',
        'add-user-authentication',
        expect.anything(),
      );

      // Verify metadata was created with correct values
      expect(deps.specHelpers.createMetadata).toHaveBeenCalledWith(
        '/project/.cc-track/specs/001-add-user-authentication',
        expect.objectContaining({
          task_id: '001',
          feature_name: 'add-user-authentication',
          branch: '001-add-user-authentication',
          status: 'specified',
          started: '2025-01-15T12:00:00Z',
        }),
        expect.anything(),
      );

      // Verify CLAUDE.md was updated
      const claudeMdContent = deps.fs.readFileSync('/project/CLAUDE.md', 'utf-8');
      expect(claudeMdContent).toContain('@.cc-track/specs/001-add-user-authentication/spec.md');
    });
  });

  // T003: Test auto-generates task ID when not provided
  describe('T003: auto-generates task ID', () => {
    test('auto-generates next task ID when not provided', () => {
      const deps = createMockDeps({
        specHelpers: {
          getNextTaskId: mock(() => '005'), // Simulating 4 existing tasks
          generateFeatureName: mock(() => 'new-feature'),
          createSpecDirectory: mock(() => '/project/.cc-track/specs/005-new-feature'),
          createMetadata: mock(() => {}),
        },
      });

      const options: SpecifyOptions = { title: 'New feature' };

      const result = runSpecify(options, deps);

      expect(result.success).toBe(true);
      expect(result.data?.taskId).toBe('005');
      expect(deps.specHelpers.getNextTaskId).toHaveBeenCalled();
    });
  });

  // T004: Test creates GitHub issue when enabled
  describe('T004: GitHub issue creation', () => {
    test('creates GitHub issue when integration is enabled', () => {
      const deps = createMockDeps({
        config: {
          isGitHubIntegrationEnabled: mock(() => true),
        },
        github: {
          createGitHubIssue: mock(() => ({
            number: 42,
            url: 'https://github.com/test/repo/issues/42',
          })),
        },
      });

      const options: SpecifyOptions = { title: 'Feature with GitHub issue' };

      const result = runSpecify(options, deps);

      expect(result.success).toBe(true);
      expect(result.data?.github).toBeDefined();
      expect(result.data?.github?.issue).toBe(42);
      expect(result.data?.github?.url).toBe('https://github.com/test/repo/issues/42');
      expect(deps.github.createGitHubIssue).toHaveBeenCalled();

      // Verify metadata includes GitHub info
      expect(deps.specHelpers.createMetadata).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({
          github: {
            issue: 42,
            url: 'https://github.com/test/repo/issues/42',
          },
        }),
        expect.anything(),
      );
    });

    test('does not create GitHub issue when integration is disabled', () => {
      const deps = createMockDeps({
        config: {
          isGitHubIntegrationEnabled: mock(() => false),
        },
      });

      const options: SpecifyOptions = { title: 'Feature without GitHub' };

      const result = runSpecify(options, deps);

      expect(result.success).toBe(true);
      expect(result.data?.github).toBeUndefined();
      expect(deps.github.createGitHubIssue).not.toHaveBeenCalled();
    });
  });

  // T005: Test fails gracefully when spec dir already exists
  describe('T005: spec directory already exists', () => {
    test('returns error when spec directory already exists', () => {
      const existingDirs = new Set(['/project/.cc-track/specs/001-existing-feature']);
      const deps = createMockDeps({
        fs: {
          existsSync: mock((path: string) => {
            if (path === '/project/CLAUDE.md') return true;
            if (path === '/project/.cc-track') return true;
            return existingDirs.has(path);
          }),
          readFileSync: mock(() => '# Project\n\n## Active Task\n@.cc-track/no_active_task.md\n'),
          writeFileSync: mock(() => {}),
          mkdirSync: mock(() => {}),
        },
        specHelpers: {
          getNextTaskId: mock(() => '001'),
          generateFeatureName: mock(() => 'existing-feature'),
          createSpecDirectory: mock(() => '/project/.cc-track/specs/001-existing-feature'),
          createMetadata: mock(() => {}),
        },
      });

      // Make the spec directory "exist"
      existingDirs.add('/project/.cc-track/specs/001-existing-feature');

      const options: SpecifyOptions = { title: 'Existing feature' };

      const result = runSpecify(options, deps);

      expect(result.success).toBe(false);
      expect(result.error).toContain('already exists');
    });
  });

  // T006: Test fails gracefully when branch already exists
  describe('T006: branch already exists', () => {
    test('returns error when git branch already exists', () => {
      const deps = createMockDeps({
        git: {
          createTaskBranch: mock(() => {}),
          getCurrentBranch: mock(() => 'main'),
          branchExists: mock(() => true), // Branch already exists
        },
      });

      const options: SpecifyOptions = { title: 'Feature with existing branch' };

      const result = runSpecify(options, deps);

      expect(result.success).toBe(false);
      expect(result.error).toContain('branch');
      expect(result.error?.toLowerCase()).toContain('already exists');
    });
  });

  // T007: Test fails gracefully when .cc-track directory is missing
  describe('T007: .cc-track directory missing', () => {
    test('returns error when .cc-track directory does not exist', () => {
      const deps = createMockDeps({
        fs: {
          existsSync: mock((path: string) => {
            if (path === '/project/CLAUDE.md') return true;
            if (path === '/project/.cc-track') return false; // .cc-track missing
            return false;
          }),
          readFileSync: mock(() => '# Project\n'),
          writeFileSync: mock(() => {}),
          mkdirSync: mock(() => {}),
        },
      });

      const options: SpecifyOptions = { title: 'Feature' };

      const result = runSpecify(options, deps);

      expect(result.success).toBe(false);
      expect(result.error).toContain('.cc-track');
    });
  });

  // T008: Test warns but continues when GitHub fails
  describe('T008: GitHub failure is non-blocking', () => {
    test('warns but continues when GitHub issue creation fails', () => {
      const deps = createMockDeps({
        config: {
          isGitHubIntegrationEnabled: mock(() => true),
        },
        github: {
          createGitHubIssue: mock(() => null), // Simulate failure
        },
      });

      const options: SpecifyOptions = { title: 'Feature with failed GitHub' };

      const result = runSpecify(options, deps);

      // Should still succeed
      expect(result.success).toBe(true);
      expect(result.data?.taskId).toBeDefined();
      expect(result.data?.specDir).toBeDefined();

      // But GitHub data should be undefined
      expect(result.data?.github).toBeUndefined();

      // Should have a warning
      expect(result.warnings).toBeDefined();
      expect(result.warnings?.length).toBeGreaterThan(0);
      expect(result.warnings?.some((w) => w.toLowerCase().includes('github'))).toBe(true);
    });
  });

  // Additional edge case: CLAUDE.md missing
  describe('CLAUDE.md missing', () => {
    test('returns error when CLAUDE.md does not exist', () => {
      const deps = createMockDeps({
        fs: {
          existsSync: mock((path: string) => {
            if (path === '/project/CLAUDE.md') return false; // CLAUDE.md missing
            return true;
          }),
          readFileSync: mock(() => ''),
          writeFileSync: mock(() => {}),
          mkdirSync: mock(() => {}),
        },
      });

      const options: SpecifyOptions = { title: 'Feature' };

      const result = runSpecify(options, deps);

      expect(result.success).toBe(false);
      expect(result.error).toContain('CLAUDE.md');
    });
  });

  // Edge case: Empty title
  describe('empty title', () => {
    test('returns error when title is empty', () => {
      const deps = createMockDeps();
      const options: SpecifyOptions = { title: '' };

      const result = runSpecify(options, deps);

      expect(result.success).toBe(false);
      expect(result.error).toContain('title');
    });
  });

  // Edge case: CLAUDE.md missing expected pattern
  describe('CLAUDE.md missing active task pattern', () => {
    test('returns error when CLAUDE.md lacks expected Active Task reference', () => {
      const deps = createMockDeps({
        fs: {
          existsSync: mock((path: string) => {
            if (path === '/project/CLAUDE.md') return true;
            if (path === '/project/.cc-track') return true;
            if (path === '/project/.cc-track/specs') return true;
            // Spec directory does NOT exist
            return false;
          }),
          readFileSync: mock(() => '# Project\n\nSome content without active task reference\n'),
          writeFileSync: mock(() => {}),
          mkdirSync: mock(() => {}),
        },
      });

      const options: SpecifyOptions = { title: 'Feature' };

      const result = runSpecify(options, deps);

      expect(result.success).toBe(false);
      expect(result.error).toContain('Active Task reference');
    });
  });
});
