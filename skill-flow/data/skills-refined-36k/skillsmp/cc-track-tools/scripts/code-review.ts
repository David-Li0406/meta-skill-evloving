import { formatValidationResults, runStandaloneValidation, type StandaloneValidationResult } from '../lib/validation';
import type { CommandResult } from './context';

export interface CodeReviewDeps {
  runStandaloneValidation?: typeof runStandaloneValidation;
  cwd?: () => string;
}

export interface CodeReviewResultData {
  validation?: StandaloneValidationResult;
  readyForReview?: boolean;
  error?: string;
}

/**
 * Standalone code review validation action
 * Runs validation checks without requiring an active task/spec
 */
export async function codeReviewAction(deps: CodeReviewDeps = {}): Promise<CommandResult<CodeReviewResultData>> {
  const { runStandaloneValidation: runValidation = runStandaloneValidation } = deps;

  const projectRoot = deps.cwd ? deps.cwd() : process.cwd();
  const messages: string[] = [];
  const warnings: string[] = [];

  try {
    const result: StandaloneValidationResult = await runValidation(projectRoot);

    if (!result.success && result.error) {
      throw new Error(result.error);
    }

    messages.push('## Standalone Code Review\n');

    const validationPassed = result.readyForReview;

    if (validationPassed) {
      messages.push('### ✅ Validation Passed\n');
      messages.push('All validation checks have passed successfully!\n');
    } else {
      messages.push('### ⚠️ Validation Issues Found\n');
      messages.push('The following issues need to be resolved before code review:\n');
      messages.push(...formatValidationResults(result.validation));
    }

    // Git status information
    if (result.git?.hasUncommittedChanges) {
      messages.push('#### Git Status');
      messages.push(`On branch: \`${result.git.currentBranch}\``);
      messages.push(`${result.git.modifiedFiles?.length || 0} modified files.\n`);
    }

    messages.push('### Next Steps\n');
    if (!validationPassed) {
      messages.push('1. Fix the validation issues listed above');
      messages.push('2. Run `/cc-track:code-review` again to verify all issues are resolved\n');
    } else {
      messages.push('**✅ Validation passed! Ready for code review agents.**\n');
    }

    return {
      success: true,
      messages,
      warnings,
      data: {
        validation: result,
        readyForReview: validationPassed,
      },
      exitCode: 0,
    };
  } catch (error) {
    messages.push('## ❌ Validation Check Failed\n');

    const err = error as { code?: string; status?: number; message?: string; stderr?: string };
    if (err.code === 'ENOENT') {
      messages.push('Error: Could not run validation checks.\n');
      messages.push('Please ensure plugin dependencies are installed: `bun install` in the plugin directory');
    } else if (err.status === 127) {
      messages.push('Error: validation command not found.\n');
      messages.push('Please ensure plugin dependencies are installed properly.');
    } else {
      messages.push(`Error running validation checks: ${err.message || 'Unknown error'}\n`);
      if (err.stderr) {
        messages.push('Error details:');
        messages.push(err.stderr);
      }
    }

    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
      messages,
      warnings,
      data: {
        error: error instanceof Error ? error.message : 'Unknown error',
      },
      exitCode: 1,
    };
  }
}

// CLI entrypoint
if (import.meta.main) {
  codeReviewAction()
    .then((result) => {
      console.log(JSON.stringify(result, null, 2));
      process.exitCode = result.exitCode ?? 0;
    })
    .catch((error) => {
      console.error(
        JSON.stringify({
          success: false,
          error: error instanceof Error ? error.message : String(error),
        }),
      );
      process.exitCode = 1;
    });
}
