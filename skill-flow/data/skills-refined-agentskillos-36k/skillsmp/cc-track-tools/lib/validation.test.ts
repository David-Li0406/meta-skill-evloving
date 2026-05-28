// ABOUTME: Comprehensive tests for validation module covering all validation functions.
// ABOUTME: Tests TypeScript, lint, tests, Knip checks, git status, and task info helpers.

import { afterEach, beforeEach, describe, expect, mock, test } from 'bun:test';
import { createMockLogger } from '../test-utils/command-mocks';
import { runValidationChecks, type ValidationDeps } from './validation';

describe('validation', () => {
  beforeEach(() => {
    mock.restore();
  });

  afterEach(() => {
    mock.restore();
  });

  // Helper to create common spec-related mocks
  function createSpecMocks() {
    return {
      getActiveSpecDirectory: mock(() => '/test/project/.cc-track/specs/001-test-task'),
      readMetadata: mock(() => ({
        task_id: '001',
        feature_name: 'test-task',
        branch: 'main',
        status: 'in_progress',
        started: '2025-01-01T00:00:00.000Z',
      })),
    };
  }

  describe('runValidationChecks', () => {
    test('passes validation when TypeScript is disabled', async () => {
      // Mock dependencies
      const mockExecSync = mock(() => '');
      const mockExistsSync = mock(() => true);
      const mockReadFileSync = mock((path: string) => {
        if (path.includes('package.json')) {
          return JSON.stringify({ scripts: {} }); // No test script
        }
        if (path.includes('TASK_001.md')) {
          return '# Test Task\n\n**Status:** in_progress';
        }
        return '';
      });

      const deps: ValidationDeps = {
        execSync: mockExecSync,
        fileOps: {
          existsSync: mockExistsSync,
          readFileSync: mockReadFileSync,
        },
        getConfig: mock(() => ({
          hooks: {
            edit_validation: {
              typecheck: { enabled: false },
              lint: { enabled: false },
            },
          },
        })),
        getLintConfig: mock(() => ({ enabled: false })),
        getTestConfig: mock(() => ({ enabled: false })),
        getActiveTaskId: mock(() => 'TASK_001'),
        ...createSpecMocks(),
        isWipCommit: mock(() => false),
        getLintParser: mock(() => ({ parseOutput: () => ({ issueCount: 0 }) })),
        logger: createMockLogger(),
      };

      const result = await runValidationChecks('/test/project', deps);

      expect(result.success).toBe(true);
      expect(result.readyForCompletion).toBe(true);
      expect(result.validation.typescript?.passed).toBe(true);
      expect(result.validation.lint?.passed).toBe(true);

      // TypeScript command should never be called when disabled
      expect(mockExecSync).not.toHaveBeenCalledWith(expect.stringContaining('tsc'), expect.any(Object));
    });

    test('fails validation when TypeScript is enabled and has errors', async () => {
      // Mock TypeScript failure
      const mockExecSync = mock((command: string) => {
        if (command.includes('tsc')) {
          const error = new Error('TypeScript compilation failed') as any;
          error.stderr = 'src/test.ts(5,10): error TS2304: Cannot find name "foo".';
          throw error;
        }
        if (command.includes('git status')) {
          return '';
        }
        if (command.includes('git branch')) {
          return 'main';
        }
        if (command.includes('git log')) {
          return '';
        }
        return '';
      });

      const mockExistsSync = mock(() => true);
      const mockReadFileSync = mock((path: string) => {
        if (path.includes('package.json')) {
          return JSON.stringify({ scripts: {} });
        }
        if (path.includes('TASK_001.md')) {
          return '# Test Task\n\n**Status:** in_progress';
        }
        return '';
      });

      const deps: ValidationDeps = {
        execSync: mockExecSync,
        fileOps: {
          existsSync: mockExistsSync,
          readFileSync: mockReadFileSync,
        },
        getConfig: mock(() => ({
          hooks: {
            edit_validation: {
              typecheck: { enabled: true, command: 'bunx tsc --noEmit' },
              lint: { enabled: false },
            },
          },
        })),
        getLintConfig: mock(() => ({ enabled: false })),
        getTestConfig: mock(() => ({ enabled: false })),
        getActiveTaskId: mock(() => 'TASK_001'),
        ...createSpecMocks(),
        isWipCommit: mock(() => false),
        getLintParser: mock(() => ({ parseOutput: () => ({ issueCount: 0 }) })),
        logger: createMockLogger(),
      };

      const result = await runValidationChecks('/test/project', deps);

      expect(result.success).toBe(true);
      expect(result.readyForCompletion).toBe(false); // Should fail due to TypeScript errors
      expect(result.validation.typescript?.passed).toBe(false);
      expect(result.validation.typescript?.errorCount).toBe(1);

      // TypeScript command should be called when enabled
      expect(mockExecSync).toHaveBeenCalledWith('bunx tsc --noEmit', expect.objectContaining({ cwd: '/test/project' }));
    });

    test('passes validation when TypeScript is enabled and has no errors', async () => {
      // Mock successful TypeScript check
      const mockExecSync = mock((command: string) => {
        if (command.includes('git status')) {
          return '';
        }
        if (command.includes('git branch')) {
          return 'main';
        }
        if (command.includes('git log')) {
          return '';
        }
        return ''; // TypeScript success returns empty
      });

      const mockExistsSync = mock(() => true);
      const mockReadFileSync = mock((path: string) => {
        if (path.includes('package.json')) {
          return JSON.stringify({ scripts: {} });
        }
        if (path.includes('TASK_001.md')) {
          return '# Test Task\n\n**Status:** in_progress';
        }
        return '';
      });

      const deps: ValidationDeps = {
        execSync: mockExecSync,
        fileOps: {
          existsSync: mockExistsSync,
          readFileSync: mockReadFileSync,
        },
        getConfig: mock(() => ({
          hooks: {
            edit_validation: {
              typecheck: { enabled: true, command: 'bunx tsc --noEmit' },
              lint: { enabled: false },
            },
          },
        })),
        getLintConfig: mock(() => ({ enabled: false })),
        getTestConfig: mock(() => ({ enabled: false })),
        getActiveTaskId: mock(() => 'TASK_001'),
        ...createSpecMocks(),
        isWipCommit: mock(() => false),
        getLintParser: mock(() => ({ parseOutput: () => ({ issueCount: 0 }) })),
        logger: createMockLogger(),
      };

      const result = await runValidationChecks('/test/project', deps);

      expect(result.success).toBe(true);
      expect(result.readyForCompletion).toBe(true);
      expect(result.validation.typescript?.passed).toBe(true);

      // TypeScript command should be called when enabled
      expect(mockExecSync).toHaveBeenCalledWith('bunx tsc --noEmit', expect.objectContaining({ cwd: '/test/project' }));
    });

    test('handles missing active task', async () => {
      const deps: ValidationDeps = {
        execSync: mock(() => ''),
        fileOps: {
          existsSync: mock(() => true),
          readFileSync: mock(() => ''),
        },
        getConfig: mock(() => ({})),
        getLintConfig: mock(() => ({ enabled: false })),
        getTestConfig: mock(() => ({ enabled: false })),
        getActiveTaskId: mock(() => null), // No active task
        isWipCommit: mock(() => false),
        getLintParser: mock(() => ({ parseOutput: () => ({ issueCount: 0 }) })),
        logger: createMockLogger(),
      };

      const result = await runValidationChecks('/test/project', deps);

      expect(result.success).toBe(false);
      expect(result.error).toBe('No active task found');
      expect(result.task.exists).toBe(false);
    });

    test('uses custom TypeScript command when configured', async () => {
      const customCommand = 'npx tsc --strict --noEmit';

      const mockExecSync = mock((command: string) => {
        if (command.includes('git status')) {
          return '';
        }
        if (command.includes('git branch')) {
          return 'main';
        }
        if (command.includes('git log')) {
          return '';
        }
        return '';
      });

      const mockExistsSync = mock(() => true);
      const mockReadFileSync = mock((path: string) => {
        if (path.includes('package.json')) {
          return JSON.stringify({ scripts: {} });
        }
        if (path.includes('TASK_001.md')) {
          return '# Test Task\n\n**Status:** in_progress';
        }
        return '';
      });

      const deps: ValidationDeps = {
        execSync: mockExecSync,
        fileOps: {
          existsSync: mockExistsSync,
          readFileSync: mockReadFileSync,
        },
        getConfig: mock(() => ({
          hooks: {
            edit_validation: {
              typecheck: { enabled: true, command: customCommand },
              lint: { enabled: false },
            },
          },
        })),
        getLintConfig: mock(() => ({ enabled: false })),
        getTestConfig: mock(() => ({ enabled: false })),
        getActiveTaskId: mock(() => 'TASK_001'),
        ...createSpecMocks(),
        isWipCommit: mock(() => false),
        getLintParser: mock(() => ({ parseOutput: () => ({ issueCount: 0 }) })),
        logger: createMockLogger(),
      };

      const result = await runValidationChecks('/test/project', deps);

      expect(result.success).toBe(true);
      expect(result.validation.typescript?.passed).toBe(true);

      // Should use the custom command
      expect(mockExecSync).toHaveBeenCalledWith(customCommand, expect.objectContaining({ cwd: '/test/project' }));
    });

    test('passes validation when tests are disabled', async () => {
      const mockExecSync = mock((command: string) => {
        if (command.includes('git status')) {
          return '';
        }
        if (command.includes('git branch')) {
          return 'main';
        }
        if (command.includes('git log')) {
          return '';
        }
        return '';
      });

      const mockExistsSync = mock(() => true);
      const mockReadFileSync = mock((path: string) => {
        if (path.includes('package.json')) {
          return JSON.stringify({ scripts: { test: 'bun test' } });
        }
        if (path.includes('TASK_001.md')) {
          return '# Test Task\n\n**Status:** in_progress';
        }
        return '';
      });

      const deps: ValidationDeps = {
        execSync: mockExecSync,
        fileOps: {
          existsSync: mockExistsSync,
          readFileSync: mockReadFileSync,
        },
        getConfig: mock(() => ({})),
        getLintConfig: mock(() => ({ enabled: false })),
        getTestConfig: mock(() => ({ enabled: false })),
        getActiveTaskId: mock(() => 'TASK_001'),
        ...createSpecMocks(),
        isWipCommit: mock(() => false),
        getLintParser: mock(() => ({ parseOutput: () => ({ issueCount: 0 }) })),
        logger: createMockLogger(),
      };

      const result = await runValidationChecks('/test/project', deps);

      expect(result.success).toBe(true);
      expect(result.readyForCompletion).toBe(true);
      expect(result.validation.tests?.passed).toBe(true);

      // Tests should not be executed when disabled
      expect(mockExecSync).not.toHaveBeenCalledWith(expect.stringContaining('test'), expect.any(Object));
    });

    test('uses custom test command when configured', async () => {
      const customTestCommand = 'npm test';

      const mockExecSync = mock((command: string) => {
        if (command.includes('git status')) {
          return '';
        }
        if (command.includes('git branch')) {
          return 'main';
        }
        if (command.includes('git log')) {
          return '';
        }
        return '';
      });

      const mockExistsSync = mock(() => true);
      const mockReadFileSync = mock((path: string) => {
        if (path.includes('package.json')) {
          return JSON.stringify({ scripts: { test: 'npm test' } });
        }
        if (path.includes('TASK_001.md')) {
          return '# Test Task\n\n**Status:** in_progress';
        }
        return '';
      });

      const deps: ValidationDeps = {
        execSync: mockExecSync,
        fileOps: {
          existsSync: mockExistsSync,
          readFileSync: mockReadFileSync,
        },
        getConfig: mock(() => ({})),
        getLintConfig: mock(() => ({ enabled: false })),
        getTestConfig: mock(() => ({ enabled: true, command: customTestCommand })),
        getActiveTaskId: mock(() => 'TASK_001'),
        ...createSpecMocks(),
        isWipCommit: mock(() => false),
        getLintParser: mock(() => ({ parseOutput: () => ({ issueCount: 0 }) })),
        logger: createMockLogger(),
      };

      const result = await runValidationChecks('/test/project', deps);

      expect(result.success).toBe(true);
      expect(result.validation.tests?.passed).toBe(true);

      // Should use the custom test command
      expect(mockExecSync).toHaveBeenCalledWith(
        customTestCommand,
        expect.objectContaining({
          cwd: '/test/project',
          stdio: ['pipe', 'ignore', 'ignore'],
        }),
      );
    });

    test('detects test failures when tests are enabled', async () => {
      const mockExecSync = mock((command: string, options?: Record<string, unknown>) => {
        if (command === 'npm test') {
          // First call (silent check) throws to indicate failure
          if (options?.stdio) {
            const error = new Error('Tests failed') as NodeJS.ErrnoException;
            (error as NodeJS.ErrnoException & { status: number }).status = 1;
            throw error;
          }
          // Second call (to get details) throws with output
          const error = new Error('Tests failed') as Error & { stdout: string };
          error.stdout =
            '✗ test/example.test.js › should work (fail)\n    AssertionError: expected 1 to equal 2\n\n1 fail\n0 pass';
          throw error;
        }
        if (command.includes('git status')) {
          return '';
        }
        if (command.includes('git branch')) {
          return 'main';
        }
        if (command.includes('git log')) {
          return '';
        }
        return '';
      });

      const mockExistsSync = mock(() => true);
      const mockReadFileSync = mock((path: string) => {
        if (path.includes('package.json')) {
          return JSON.stringify({ scripts: { test: 'npm test' } });
        }
        if (path.includes('TASK_001.md')) {
          return '# Test Task\n\n**Status:** in_progress';
        }
        return '';
      });

      const deps: ValidationDeps = {
        execSync: mockExecSync,
        fileOps: {
          existsSync: mockExistsSync,
          readFileSync: mockReadFileSync,
        },
        getConfig: mock(() => ({})),
        getLintConfig: mock(() => ({ enabled: false })),
        getTestConfig: mock(() => ({ enabled: true, command: 'npm test' })),
        getActiveTaskId: mock(() => 'TASK_001'),
        ...createSpecMocks(),
        isWipCommit: mock(() => false),
        getLintParser: mock(() => ({ parseOutput: () => ({ issueCount: 0 }) })),
        logger: createMockLogger(),
      };

      const result = await runValidationChecks('/test/project', deps);

      expect(result.success).toBe(true);
      expect(result.readyForCompletion).toBe(false); // Should fail due to test failures
      expect(result.validation.tests?.passed).toBe(false);
      expect(result.validation.tests?.failCount).toBe(1);
      expect(result.validation.tests?.errors).toContain('should work');
    });

    test('falls back to default bun test command when no custom command configured', async () => {
      const mockExecSync = mock((command: string) => {
        if (command.includes('git status')) {
          return '';
        }
        if (command.includes('git branch')) {
          return 'main';
        }
        if (command.includes('git log')) {
          return '';
        }
        return '';
      });

      const mockExistsSync = mock(() => true);
      const mockReadFileSync = mock((path: string) => {
        if (path.includes('package.json')) {
          return JSON.stringify({ scripts: { test: 'bun test' } });
        }
        if (path.includes('TASK_001.md')) {
          return '# Test Task\n\n**Status:** in_progress';
        }
        return '';
      });

      const deps: ValidationDeps = {
        execSync: mockExecSync,
        fileOps: {
          existsSync: mockExistsSync,
          readFileSync: mockReadFileSync,
        },
        getConfig: mock(() => ({})),
        getLintConfig: mock(() => ({ enabled: false })),
        getTestConfig: mock(() => ({ enabled: true })), // No command specified
        getActiveTaskId: mock(() => 'TASK_001'),
        ...createSpecMocks(),
        isWipCommit: mock(() => false),
        getLintParser: mock(() => ({ parseOutput: () => ({ issueCount: 0 }) })),
        logger: createMockLogger(),
      };

      const result = await runValidationChecks('/test/project', deps);

      expect(result.success).toBe(true);
      expect(result.validation.tests?.passed).toBe(true);

      // Should use the default 'bun test' command
      expect(mockExecSync).toHaveBeenCalledWith(
        'bun test',
        expect.objectContaining({
          cwd: '/test/project',
          stdio: ['pipe', 'ignore', 'ignore'],
        }),
      );
    });

    test('handles incomplete spec structure gracefully', async () => {
      const deps: ValidationDeps = {
        execSync: mock(() => ''),
        fileOps: {
          existsSync: mock(() => false), // spec dir doesn't exist
          readFileSync: mock(() => ''),
        },
        getConfig: mock(() => ({})),
        getLintConfig: mock(() => ({ enabled: false })),
        getTestConfig: mock(() => ({ enabled: false })),
        getActiveTaskId: mock(() => 'TASK_001'),
        getActiveSpecDirectory: mock(() => null), // No spec directory
        readMetadata: mock(() => null), // No metadata
        isWipCommit: mock(() => false),
        getLintParser: mock(() => ({ parseOutput: () => ({ issueCount: 0 }) })),
        logger: createMockLogger(),
      };

      const result = await runValidationChecks('/test/project', deps);

      expect(result.success).toBe(false);
      expect(result.task.exists).toBe(false);
      expect(result.error).toBe('No active task found');
    });

    test('warns when task status is not in_progress', async () => {
      const mockExecSync = mock((command: string) => {
        if (command.includes('git status')) {
          return '';
        }
        if (command.includes('git branch')) {
          return 'main';
        }
        if (command.includes('git log')) {
          return '';
        }
        return '';
      });

      const mockExistsSync = mock(() => true);
      const mockReadFileSync = mock((path: string) => {
        if (path.includes('package.json')) {
          return JSON.stringify({ scripts: {} });
        }
        if (path.includes('spec.md')) {
          return '# Test Task\n\nTest description';
        }
        return '';
      });

      const deps: ValidationDeps = {
        execSync: mockExecSync,
        fileOps: {
          existsSync: mockExistsSync,
          readFileSync: mockReadFileSync,
        },
        getConfig: mock(() => ({
          hooks: {
            edit_validation: {
              typecheck: { enabled: false },
              lint: { enabled: false },
            },
          },
        })),
        getLintConfig: mock(() => ({ enabled: false })),
        getTestConfig: mock(() => ({ enabled: false })),
        getActiveTaskId: mock(() => 'TASK_001'),
        getActiveSpecDirectory: mock(() => '/test/project/.cc-track/specs/001-test'),
        readMetadata: mock(() => ({
          task_id: '001',
          feature_name: 'test-task',
          status: 'pending', // Not in_progress
        })),
        isWipCommit: mock(() => false),
        getLintParser: mock(() => ({ parseOutput: () => ({ issueCount: 0 }) })),
        logger: createMockLogger(),
      };

      const result = await runValidationChecks('/test/project', deps);

      expect(result.success).toBe(true);
      expect(result.readyForCompletion).toBe(true);
      expect(result.warnings).toContain("Task status is 'pending', expected 'in_progress'");
    });

    test('reports all validation failures comprehensively', async () => {
      const mockExecSync = mock((command: string, options?: Record<string, unknown>) => {
        if (command.includes('tsc')) {
          const error = new Error('TypeScript failed') as Error & { stderr: string };
          error.stderr = 'error TS2304: Cannot find name "foo".\nerror TS2304: Cannot find name "bar".';
          throw error;
        }
        if (command.includes('biome lint')) {
          const error = new Error('Lint failed') as Error & { stderr: string };
          error.stderr = 'file.ts:1:1 lint error';
          throw error;
        }
        if (command === 'npm test') {
          // First call (with stdio) for silent check - throws to indicate failure
          if (options?.stdio) {
            throw new Error('Tests failed');
          }
          // Second call (without stdio) for details - throws with output
          const error = new Error('Tests failed') as Error & { stdout: string };
          error.stdout = '✗ test 1 (fail)\n✗ test 2 (fail)\n2 fail';
          throw error;
        }
        if (command.includes('git status')) {
          return '';
        }
        if (command.includes('git branch')) {
          return 'main';
        }
        if (command.includes('git log')) {
          return '';
        }
        return '';
      });

      const deps: ValidationDeps = {
        execSync: mockExecSync,
        fileOps: {
          existsSync: mock(() => true),
          readFileSync: mock((path: string) => {
            if (path.includes('package.json')) {
              return JSON.stringify({ scripts: { test: 'npm test' } });
            }
            if (path.includes('spec.md')) {
              return '# Test Task';
            }
            return '';
          }),
        },
        getConfig: mock(() => ({
          hooks: {
            edit_validation: {
              typecheck: { enabled: true, command: 'bunx tsc --noEmit' },
              lint: { enabled: true, command: 'biome lint' },
            },
          },
        })),
        getLintConfig: mock(() => ({
          enabled: true,
          command: 'biome lint',
          tool: 'biome',
        })),
        getTestConfig: mock(() => ({ enabled: true, command: 'npm test' })),
        getActiveTaskId: mock(() => 'TASK_001'),
        getActiveSpecDirectory: mock(() => '/test/.cc-track/specs/001-test'),
        readMetadata: mock(() => ({
          task_id: '001',
          feature_name: 'test',
          status: 'in_progress',
        })),
        isWipCommit: mock(() => false),
        getLintParser: mock(() => ({
          parseOutput: () => ({ issueCount: 2 }),
        })),
        logger: createMockLogger(),
      };

      const result = await runValidationChecks('/test/project', deps);

      expect(result.success).toBe(true);
      expect(result.readyForCompletion).toBe(false);
      expect(result.validation.typescript?.passed).toBe(false);
      expect(result.validation.typescript?.errorCount).toBe(2);
      expect(result.validation.lint?.passed).toBe(false);
      expect(result.validation.lint?.issueCount).toBe(2);
      expect(result.validation.tests?.passed).toBe(false);
      expect(result.validation.tests?.failCount).toBe(2);
    });

    test('handles git status check failures gracefully', async () => {
      const mockExecSync = mock((command: string) => {
        if (command.includes('git status')) {
          throw new Error('git not initialized');
        }
        if (command.includes('git branch')) {
          throw new Error('git not initialized');
        }
        if (command.includes('git log')) {
          throw new Error('git not initialized');
        }
        return '';
      });

      const deps: ValidationDeps = {
        execSync: mockExecSync,
        fileOps: {
          existsSync: mock(() => true),
          readFileSync: mock((path: string) => {
            if (path.includes('package.json')) {
              return JSON.stringify({ scripts: {} });
            }
            if (path.includes('spec.md')) {
              return '# Test';
            }
            return '';
          }),
        },
        getConfig: mock(() => ({
          hooks: {
            edit_validation: {
              typecheck: { enabled: false },
              lint: { enabled: false },
            },
          },
        })),
        getLintConfig: mock(() => ({ enabled: false })),
        getTestConfig: mock(() => ({ enabled: false })),
        getActiveTaskId: mock(() => 'TASK_001'),
        getActiveSpecDirectory: mock(() => '/test/.cc-track/specs/001-test'),
        readMetadata: mock(() => ({
          task_id: '001',
          feature_name: 'test',
          status: 'in_progress',
        })),
        isWipCommit: mock(() => false),
        getLintParser: mock(() => ({ parseOutput: () => ({ issueCount: 0 }) })),
        logger: createMockLogger(),
      };

      const result = await runValidationChecks('/test/project', deps);

      expect(result.success).toBe(true);
      expect(result.git.currentBranch).toBe('unknown');
      expect(result.git.hasUncommittedChanges).toBe(false);
      expect(result.git.wipCommitCount).toBe(0);
    });

    test('detects WIP commits in git history', async () => {
      const mockExecSync = mock((command: string) => {
        if (command.includes('git status --porcelain')) {
          return '';
        }
        if (command.includes('git branch --show-current')) {
          return 'feature/task-001';
        }
        if (command.includes('git log')) {
          return 'abc1234 wip: work in progress\nxyz5678 feat: added feature\nabc9999 wip: another work item\n';
        }
        return '';
      });

      const deps: ValidationDeps = {
        execSync: mockExecSync,
        fileOps: {
          existsSync: mock(() => true),
          readFileSync: mock((path: string) => {
            if (path.includes('package.json')) {
              return JSON.stringify({ scripts: {} });
            }
            if (path.includes('spec.md')) {
              return '# Test';
            }
            return '';
          }),
        },
        getConfig: mock(() => ({
          hooks: {
            edit_validation: {
              typecheck: { enabled: false },
              lint: { enabled: false },
            },
          },
        })),
        getLintConfig: mock(() => ({ enabled: false })),
        getTestConfig: mock(() => ({ enabled: false })),
        getActiveTaskId: mock(() => '001'),
        getActiveSpecDirectory: mock(() => '/test/.cc-track/specs/001-test'),
        readMetadata: mock(() => ({
          task_id: '001',
          feature_name: 'test',
          status: 'in_progress',
        })),
        isWipCommit: mock((line: string) => line.toLowerCase().includes('wip:')),
        getLintParser: mock(() => ({ parseOutput: () => ({ issueCount: 0 }) })),
        logger: createMockLogger(),
      };

      const result = await runValidationChecks('/test/project', deps);

      expect(result.success).toBe(true);
      expect(result.git.wipCommitCount).toBe(2);
      expect(result.git.currentBranch).toBe('feature/task-001');
      expect(result.git.isTaskBranch).toBe(true);
    });

    test('skips tests when no test script in package.json', async () => {
      const mockExecSync = mock(() => '');

      const deps: ValidationDeps = {
        execSync: mockExecSync,
        fileOps: {
          existsSync: mock(() => true),
          readFileSync: mock((path: string) => {
            if (path.includes('package.json')) {
              return JSON.stringify({ scripts: { build: 'tsc' } }); // No test script
            }
            if (path.includes('spec.md')) {
              return '# Test';
            }
            return '';
          }),
        },
        getConfig: mock(() => ({
          hooks: {
            edit_validation: {
              typecheck: { enabled: false },
              lint: { enabled: false },
            },
          },
        })),
        getLintConfig: mock(() => ({ enabled: false })),
        getTestConfig: mock(() => ({ enabled: true })), // Tests enabled
        getActiveTaskId: mock(() => 'TASK_001'),
        getActiveSpecDirectory: mock(() => '/test/.cc-track/specs/001-test'),
        readMetadata: mock(() => ({
          task_id: '001',
          feature_name: 'test',
          status: 'in_progress',
        })),
        isWipCommit: mock(() => false),
        getLintParser: mock(() => ({ parseOutput: () => ({ issueCount: 0 }) })),
        logger: createMockLogger(),
      };

      const result = await runValidationChecks('/test/project', deps);

      expect(result.success).toBe(true);
      expect(result.validation.tests?.passed).toBe(true);
      // Tests should not be executed
      expect(mockExecSync).not.toHaveBeenCalledWith(expect.stringContaining('bun test'), expect.any(Object));
    });

    test('handles Knip check with unused code detected', async () => {
      const mockExecSync = mock((command: string) => {
        if (command.includes('bunx knip')) {
          return 'Unused files     2\nUnused exports   5\nUnused dependencies 1\n';
        }
        if (command.includes('git status')) {
          return '';
        }
        if (command.includes('git branch')) {
          return 'main';
        }
        if (command.includes('git log')) {
          return '';
        }
        return '';
      });

      const deps: ValidationDeps = {
        execSync: mockExecSync,
        fileOps: {
          existsSync: mock(() => true),
          readFileSync: mock((path: string) => {
            if (path.includes('package.json')) {
              return JSON.stringify({ scripts: {} });
            }
            if (path.includes('spec.md')) {
              return '# Test';
            }
            return '';
          }),
        },
        getConfig: mock(() => ({
          hooks: {
            edit_validation: {
              typecheck: { enabled: false },
              lint: { enabled: false },
              knip: { enabled: true, command: 'bunx knip' },
            },
          },
        })),
        getLintConfig: mock(() => ({ enabled: false })),
        getTestConfig: mock(() => ({ enabled: false })),
        getActiveTaskId: mock(() => 'TASK_001'),
        getActiveSpecDirectory: mock(() => '/test/.cc-track/specs/001-test'),
        readMetadata: mock(() => ({
          task_id: '001',
          feature_name: 'test',
          status: 'in_progress',
        })),
        isWipCommit: mock(() => false),
        getLintParser: mock(() => ({ parseOutput: () => ({ issueCount: 0 }) })),
        logger: createMockLogger(),
      };

      const result = await runValidationChecks('/test/project', deps);

      expect(result.success).toBe(true);
      expect(result.readyForCompletion).toBe(true); // Knip is only warning
      expect(result.validation.knip?.passed).toBe(false);
      expect(result.validation.knip?.unusedFiles).toBe(2);
      expect(result.validation.knip?.unusedExports).toBe(5);
      expect(result.validation.knip?.unusedDeps).toBe(1);
      expect(result.warnings).toContainEqual(expect.stringContaining('Knip found:'));
    });

    test('handles Knip check when disabled', async () => {
      const mockExecSync = mock(() => '');

      const deps: ValidationDeps = {
        execSync: mockExecSync,
        fileOps: {
          existsSync: mock(() => true),
          readFileSync: mock((path: string) => {
            if (path.includes('package.json')) {
              return JSON.stringify({ scripts: {} });
            }
            if (path.includes('spec.md')) {
              return '# Test';
            }
            return '';
          }),
        },
        getConfig: mock(() => ({
          hooks: {
            edit_validation: {
              typecheck: { enabled: false },
              lint: { enabled: false },
              knip: { enabled: false }, // Disabled
            },
          },
        })),
        getLintConfig: mock(() => ({ enabled: false })),
        getTestConfig: mock(() => ({ enabled: false })),
        getActiveTaskId: mock(() => 'TASK_001'),
        getActiveSpecDirectory: mock(() => '/test/.cc-track/specs/001-test'),
        readMetadata: mock(() => ({
          task_id: '001',
          feature_name: 'test',
          status: 'in_progress',
        })),
        isWipCommit: mock(() => false),
        getLintParser: mock(() => ({ parseOutput: () => ({ issueCount: 0 }) })),
        logger: createMockLogger(),
      };

      const result = await runValidationChecks('/test/project', deps);

      expect(result.success).toBe(true);
      expect(result.readyForCompletion).toBe(true);
      expect(result.validation.knip?.passed).toBe(true);
      expect(mockExecSync).not.toHaveBeenCalledWith(expect.stringContaining('knip'), expect.any(Object));
    });

    test('parses multiple TypeScript errors correctly', async () => {
      const mockExecSync = mock((command: string) => {
        if (command.includes('tsc')) {
          const error = new Error('TypeScript failed') as any;
          error.stderr = `src/app.ts(10,5): error TS2322: Type 'string' is not assignable to type 'number'.
src/utils.ts(25,10): error TS2304: Cannot find name 'foo'.
src/types.ts(5,1): error TS1005: ';' expected.`;
          throw error;
        }
        if (command.includes('git status')) {
          return '';
        }
        if (command.includes('git branch')) {
          return 'main';
        }
        if (command.includes('git log')) {
          return '';
        }
        return '';
      });

      const deps: ValidationDeps = {
        execSync: mockExecSync,
        fileOps: {
          existsSync: mock(() => true),
          readFileSync: mock((path: string) => {
            if (path.includes('package.json')) {
              return JSON.stringify({ scripts: {} });
            }
            if (path.includes('spec.md')) {
              return '# Test';
            }
            return '';
          }),
        },
        getConfig: mock(() => ({
          hooks: {
            edit_validation: {
              typecheck: { enabled: true, command: 'bunx tsc --noEmit' },
              lint: { enabled: false },
            },
          },
        })),
        getLintConfig: mock(() => ({ enabled: false })),
        getTestConfig: mock(() => ({ enabled: false })),
        getActiveTaskId: mock(() => 'TASK_001'),
        getActiveSpecDirectory: mock(() => '/test/.cc-track/specs/001-test'),
        readMetadata: mock(() => ({
          task_id: '001',
          feature_name: 'test',
          status: 'in_progress',
        })),
        isWipCommit: mock(() => false),
        getLintParser: mock(() => ({ parseOutput: () => ({ issueCount: 0 }) })),
        logger: createMockLogger(),
      };

      const result = await runValidationChecks('/test/project', deps);

      expect(result.success).toBe(true);
      expect(result.readyForCompletion).toBe(false);
      expect(result.validation.typescript?.passed).toBe(false);
      expect(result.validation.typescript?.errorCount).toBe(3);
    });

    test('handles lint auto-fix failure without blocking check', async () => {
      const mockExecSync = mock((command: string) => {
        if (command.includes('biome format')) {
          const error = new Error('Formatter failed') as any;
          throw error;
        }
        if (command.includes('biome lint')) {
          return ''; // Lint passes
        }
        if (command.includes('git status')) {
          return '';
        }
        if (command.includes('git branch')) {
          return 'main';
        }
        if (command.includes('git log')) {
          return '';
        }
        return '';
      });

      const deps: ValidationDeps = {
        execSync: mockExecSync,
        fileOps: {
          existsSync: mock(() => true),
          readFileSync: mock((path: string) => {
            if (path.includes('package.json')) {
              return JSON.stringify({ scripts: {} });
            }
            if (path.includes('spec.md')) {
              return '# Test';
            }
            return '';
          }),
        },
        getConfig: mock(() => ({})),
        getLintConfig: mock(() => ({
          enabled: true,
          command: 'biome lint',
          autoFixCommand: 'biome format --write src',
          tool: 'biome',
        })),
        getTestConfig: mock(() => ({ enabled: false })),
        getActiveTaskId: mock(() => 'TASK_001'),
        getActiveSpecDirectory: mock(() => '/test/.cc-track/specs/001-test'),
        readMetadata: mock(() => ({
          task_id: '001',
          feature_name: 'test',
          status: 'in_progress',
        })),
        isWipCommit: mock(() => false),
        getLintParser: mock(() => ({ parseOutput: () => ({ issueCount: 0 }) })),
        logger: createMockLogger(),
      };

      const result = await runValidationChecks('/test/project', deps);

      expect(result.success).toBe(true);
      expect(result.readyForCompletion).toBe(true);
      expect(result.validation.lint?.passed).toBe(true);
    });

    test('limits output size to prevent bloat', async () => {
      const longErrorOutput = 'error TS2304: Cannot find name "foo".\n'.repeat(500);
      const mockExecSync = mock((command: string) => {
        if (command.includes('tsc')) {
          const error = new Error('TypeScript failed') as any;
          error.stderr = longErrorOutput;
          throw error;
        }
        if (command.includes('git status')) {
          return '';
        }
        if (command.includes('git branch')) {
          return 'main';
        }
        if (command.includes('git log')) {
          return '';
        }
        return '';
      });

      const deps: ValidationDeps = {
        execSync: mockExecSync,
        fileOps: {
          existsSync: mock(() => true),
          readFileSync: mock((path: string) => {
            if (path.includes('package.json')) {
              return JSON.stringify({ scripts: {} });
            }
            if (path.includes('spec.md')) {
              return '# Test';
            }
            return '';
          }),
        },
        getConfig: mock(() => ({
          hooks: {
            edit_validation: {
              typecheck: { enabled: true, command: 'bunx tsc --noEmit' },
              lint: { enabled: false },
            },
          },
        })),
        getLintConfig: mock(() => ({ enabled: false })),
        getTestConfig: mock(() => ({ enabled: false })),
        getActiveTaskId: mock(() => 'TASK_001'),
        getActiveSpecDirectory: mock(() => '/test/.cc-track/specs/001-test'),
        readMetadata: mock(() => ({
          task_id: '001',
          feature_name: 'test',
          status: 'in_progress',
        })),
        isWipCommit: mock(() => false),
        getLintParser: mock(() => ({ parseOutput: () => ({ issueCount: 0 }) })),
        logger: createMockLogger(),
      };

      const result = await runValidationChecks('/test/project', deps);

      expect(result.success).toBe(true);
      expect(result.validation.typescript?.passed).toBe(false);
      expect(result.validation.typescript?.errors?.length).toBeLessThanOrEqual(2000);
    });
  });
});
