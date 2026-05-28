import { beforeEach, describe, expect, mock, test } from 'bun:test';
import type { StandaloneValidationResult } from '../lib/validation';
import { type CodeReviewDeps, codeReviewAction } from './code-review';

function createPassingValidationResult(): StandaloneValidationResult {
  return {
    success: true,
    readyForReview: true,
    validation: {
      typescript: { passed: true },
      lint: { passed: true },
      tests: { passed: true, passCount: 10, failCount: 0 },
      knip: { passed: true },
    },
    git: {
      hasUncommittedChanges: false,
      modifiedFiles: [],
      wipCommitCount: 0,
      currentBranch: 'main',
      isTaskBranch: false,
    },
    warnings: [],
  };
}

function createFailingValidationResult(
  failures: { typescript?: boolean; lint?: boolean; tests?: boolean; knip?: boolean } = {},
): StandaloneValidationResult {
  return {
    success: true,
    readyForReview: false,
    validation: {
      typescript: failures.typescript
        ? { passed: false, errors: 'Type error in file.ts(1,1)', errorCount: 1 }
        : { passed: true },
      lint: failures.lint ? { passed: false, errors: 'Lint error at line 5', issueCount: 2 } : { passed: true },
      tests: failures.tests ? { passed: false, errors: 'Test failure output', failCount: 3 } : { passed: true },
      knip: failures.knip ? { passed: false, unusedFiles: 1, unusedExports: 2, unusedDeps: 0 } : { passed: true },
    },
    git: {
      hasUncommittedChanges: true,
      modifiedFiles: ['src/app.ts', 'src/utils.ts'],
      wipCommitCount: 0,
      currentBranch: 'feature-branch',
      isTaskBranch: true,
    },
    warnings: [],
  };
}

describe('code-review script', () => {
  beforeEach(() => {
    mock.restore();
  });

  describe('happy path - validation passes', () => {
    test('returns success with readyForReview true when all checks pass', async () => {
      const deps: CodeReviewDeps = {
        runStandaloneValidation: mock(async () => createPassingValidationResult()),
        cwd: () => '/project',
      };

      const result = await codeReviewAction(deps);

      expect(result.success).toBe(true);
      expect(result.exitCode).toBe(0);
      expect(result.data?.readyForReview).toBe(true);
      expect(result.messages.some((m) => m.includes('Validation Passed'))).toBe(true);
      expect(result.messages.some((m) => m.includes('Ready for code review agents'))).toBe(true);
    });
  });

  describe('validation failures', () => {
    test('reports TypeScript errors when typescript fails', async () => {
      const deps: CodeReviewDeps = {
        runStandaloneValidation: mock(async () => createFailingValidationResult({ typescript: true })),
        cwd: () => '/project',
      };

      const result = await codeReviewAction(deps);

      expect(result.success).toBe(true);
      expect(result.data?.readyForReview).toBe(false);
      expect(result.messages.some((m) => m.includes('Validation Issues Found'))).toBe(true);
      expect(result.messages.some((m) => m.includes('TypeScript Errors'))).toBe(true);
    });

    test('reports lint errors when lint fails', async () => {
      const deps: CodeReviewDeps = {
        runStandaloneValidation: mock(async () => createFailingValidationResult({ lint: true })),
        cwd: () => '/project',
      };

      const result = await codeReviewAction(deps);

      expect(result.success).toBe(true);
      expect(result.data?.readyForReview).toBe(false);
      expect(result.messages.some((m) => m.includes('Linting Issues'))).toBe(true);
    });

    test('reports test failures when tests fail', async () => {
      const deps: CodeReviewDeps = {
        runStandaloneValidation: mock(async () => createFailingValidationResult({ tests: true })),
        cwd: () => '/project',
      };

      const result = await codeReviewAction(deps);

      expect(result.success).toBe(true);
      expect(result.data?.readyForReview).toBe(false);
      expect(result.messages.some((m) => m.includes('Test Failures'))).toBe(true);
    });

    test('reports knip warnings when knip fails', async () => {
      const deps: CodeReviewDeps = {
        runStandaloneValidation: mock(async () => createFailingValidationResult({ knip: true })),
        cwd: () => '/project',
      };

      const result = await codeReviewAction(deps);

      expect(result.success).toBe(true);
      expect(result.data?.readyForReview).toBe(false);
      expect(result.messages.some((m) => m.includes('Unused Code'))).toBe(true);
    });

    test('reports multiple failures together', async () => {
      const deps: CodeReviewDeps = {
        runStandaloneValidation: mock(async () =>
          createFailingValidationResult({ typescript: true, lint: true, tests: true }),
        ),
        cwd: () => '/project',
      };

      const result = await codeReviewAction(deps);

      expect(result.success).toBe(true);
      expect(result.data?.readyForReview).toBe(false);
      expect(result.messages.some((m) => m.includes('TypeScript Errors'))).toBe(true);
      expect(result.messages.some((m) => m.includes('Linting Issues'))).toBe(true);
      expect(result.messages.some((m) => m.includes('Test Failures'))).toBe(true);
    });
  });

  describe('git status information', () => {
    test('displays git status when uncommitted changes exist', async () => {
      const validationResult = createFailingValidationResult({ lint: true });
      validationResult.git.hasUncommittedChanges = true;
      validationResult.git.currentBranch = 'feature-xyz';
      validationResult.git.modifiedFiles = ['a.ts', 'b.ts', 'c.ts'];

      const deps: CodeReviewDeps = {
        runStandaloneValidation: mock(async () => validationResult),
        cwd: () => '/project',
      };

      const result = await codeReviewAction(deps);

      expect(result.messages.some((m) => m.includes('Git Status'))).toBe(true);
      expect(result.messages.some((m) => m.includes('feature-xyz'))).toBe(true);
      expect(result.messages.some((m) => m.includes('3 modified files'))).toBe(true);
    });

    test('does not display git status when no uncommitted changes', async () => {
      const validationResult = createPassingValidationResult();
      validationResult.git.hasUncommittedChanges = false;

      const deps: CodeReviewDeps = {
        runStandaloneValidation: mock(async () => validationResult),
        cwd: () => '/project',
      };

      const result = await codeReviewAction(deps);

      expect(result.messages.some((m) => m.includes('Git Status'))).toBe(false);
    });
  });

  describe('error handling', () => {
    test('returns failure with exitCode 1 on ENOENT error', async () => {
      const error = new Error('Command not found') as Error & { code: string };
      error.code = 'ENOENT';

      const deps: CodeReviewDeps = {
        runStandaloneValidation: mock(async () => {
          throw error;
        }),
        cwd: () => '/project',
      };

      const result = await codeReviewAction(deps);

      expect(result.success).toBe(false);
      expect(result.exitCode).toBe(1);
      expect(result.error).toBeDefined();
      expect(result.messages.some((m) => m.includes('Could not run validation checks'))).toBe(true);
      expect(result.messages.some((m) => m.includes('bun install'))).toBe(true);
    });

    test('returns failure with exitCode 1 on status 127 error', async () => {
      const error = new Error('Command not found') as Error & { status: number };
      error.status = 127;

      const deps: CodeReviewDeps = {
        runStandaloneValidation: mock(async () => {
          throw error;
        }),
        cwd: () => '/project',
      };

      const result = await codeReviewAction(deps);

      expect(result.success).toBe(false);
      expect(result.exitCode).toBe(1);
      expect(result.messages.some((m) => m.includes('validation command not found'))).toBe(true);
    });

    test('returns failure with error details on generic error', async () => {
      const error = new Error('Something went wrong') as Error & { stderr: string };
      error.stderr = 'Detailed error info';

      const deps: CodeReviewDeps = {
        runStandaloneValidation: mock(async () => {
          throw error;
        }),
        cwd: () => '/project',
      };

      const result = await codeReviewAction(deps);

      expect(result.success).toBe(false);
      expect(result.exitCode).toBe(1);
      expect(result.error).toBe('Something went wrong');
      expect(result.messages.some((m) => m.includes('Something went wrong'))).toBe(true);
      expect(result.messages.some((m) => m.includes('Detailed error info'))).toBe(true);
    });

    test('handles validation result with error field', async () => {
      const deps: CodeReviewDeps = {
        runStandaloneValidation: mock(async () => ({
          success: false,
          readyForReview: false,
          validation: {},
          git: {
            hasUncommittedChanges: false,
            modifiedFiles: [],
            wipCommitCount: 0,
            currentBranch: 'main',
            isTaskBranch: false,
          },
          warnings: [],
          error: 'Validation initialization failed',
        })),
        cwd: () => '/project',
      };

      const result = await codeReviewAction(deps);

      expect(result.success).toBe(false);
      expect(result.exitCode).toBe(1);
      expect(result.error).toBe('Validation initialization failed');
    });
  });

  describe('next steps guidance', () => {
    test('shows fix instructions when validation fails', async () => {
      const deps: CodeReviewDeps = {
        runStandaloneValidation: mock(async () => createFailingValidationResult({ typescript: true })),
        cwd: () => '/project',
      };

      const result = await codeReviewAction(deps);

      expect(result.messages.some((m) => m.includes('Fix the validation issues'))).toBe(true);
      expect(result.messages.some((m) => m.includes('/cc-track:code-review'))).toBe(true);
    });

    test('shows ready for review message when validation passes', async () => {
      const deps: CodeReviewDeps = {
        runStandaloneValidation: mock(async () => createPassingValidationResult()),
        cwd: () => '/project',
      };

      const result = await codeReviewAction(deps);

      expect(result.messages.some((m) => m.includes('Ready for code review agents'))).toBe(true);
    });
  });

  describe('uses provided cwd', () => {
    test('passes cwd to runStandaloneValidation', async () => {
      const mockValidation = mock(async () => createPassingValidationResult());
      const deps: CodeReviewDeps = {
        runStandaloneValidation: mockValidation,
        cwd: () => '/custom/project/path',
      };

      await codeReviewAction(deps);

      expect(mockValidation).toHaveBeenCalledWith('/custom/project/path');
    });
  });
});
