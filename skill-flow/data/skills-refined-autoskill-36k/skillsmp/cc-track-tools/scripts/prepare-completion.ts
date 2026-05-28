import { getConfig } from '../lib/config';
import { formatValidationResults, type PreparationResult, runValidationChecks } from '../lib/validation';
import type { CommandResult } from './context';

export interface PrepareCompletionDeps {
  getConfig?: typeof getConfig;
  runValidationChecks?: typeof runValidationChecks;
  cwd?: () => string;
}

/**
 * Prepare completion result data
 */
export interface PrepareCompletionResultData {
  validation?: PreparationResult;
  readyForCompletion?: boolean;
  error?: string;
}

/**
 * Prepare completion command action
 * Runs validation checks and generates dynamic instructions based on results
 *
 * Note: Code review is now handled by multi-agent review in prepare-completion.md command,
 * not by this script.
 */
export async function prepareCompletionAction(
  deps: PrepareCompletionDeps = {},
): Promise<CommandResult<PrepareCompletionResultData>> {
  const { runValidationChecks: runValidation = runValidationChecks, getConfig: getConf = getConfig } = deps;

  const projectRoot = deps.cwd ? deps.cwd() : process.cwd();
  const messages: string[] = [];
  const warnings: string[] = [];

  try {
    // Run validation checks directly
    const result: PreparationResult = await runValidation(projectRoot);

    // Handle case where validation failed to run
    if (!result.success && result.error) {
      throw new Error(result.error);
    }

    // Generate dynamic instructions based on the results
    messages.push('## Prepare Task for Completion\n');

    // Check if validation passed
    const validationPassed = result.readyForCompletion;

    // Show validation status
    if (validationPassed) {
      messages.push('### ✅ Validation Passed\n');
      messages.push('All validation checks have passed successfully!\n');
    } else {
      messages.push('### ⚠️ Validation Issues Found\n');
      messages.push('The following issues need to be resolved before task completion:\n');
      messages.push(...formatValidationResults(result.validation));
    }

    // Git status information
    if (result.git?.hasUncommittedChanges) {
      messages.push('#### Uncommitted Changes');
      messages.push(`Found ${result.git.modifiedFiles?.length || 'uncommitted'} modified files.\n`);
      messages.push('**Note:** These will be automatically committed during task completion.\n');
    }

    if (result.git?.wipCommitCount > 0) {
      messages.push('#### WIP Commits');
      messages.push(`Found ${result.git.wipCommitCount} WIP commits that will be squashed during completion.\n`);
    }

    // Task status check
    if (result.task?.status !== 'in_progress') {
      messages.push('#### Task Status');
      messages.push(`Task status is '${result.task?.status || 'unknown'}', expected 'in_progress'.\n`);
      messages.push("**Note:** This won't block completion but is unusual.\n");
    }

    // Note about code review
    if (validationPassed) {
      messages.push('### 🔍 Code Review\n');
      messages.push('Code review will be performed by multi-agent review system.');
      messages.push('The prepare-completion.md command will launch 6 specialized agents in parallel.\n');
    }

    // Documentation update reminder - only if validation passed
    if (validationPassed) {
      messages.push('### Documentation Updates\n');
      messages.push('Update the task documentation:');
      messages.push('1. Update "## Recent Progress" section in the task file, but do not update the status yet');
      messages.push('2. Note any significant decisions in decision_log.md');
      messages.push('3. Document any new patterns in system_patterns.md');
      messages.push('4. Update progress_log.md with what was accomplished');
      messages.push('5. If this task came from the backlog, remove it from backlog.md');
      messages.push('6. Commit your changes manually or wait for auto-commit\n');
    }

    // Journal reflection reminder (only if validation passed and private journal is enabled)
    const config = getConf();
    const hasPrivateJournal = config.features?.private_journal?.enabled === true;

    if (validationPassed && hasPrivateJournal) {
      messages.push('### Journal Reflection\n');
      messages.push('Consider recording insights about:');
      messages.push('- Technical challenges encountered and solutions');
      messages.push('- Patterns that worked well or poorly');
      messages.push('- Any learnings for future tasks\n');
    }

    messages.push('### Next Steps\n');
    if (!validationPassed) {
      messages.push('1. Fix the validation issues listed above');
      messages.push('2. Ask the user to run `/prepare-completion` again to verify all issues are resolved\n');
    } else {
      messages.push('1. Complete all documentation updates above');
      if (hasPrivateJournal) {
        messages.push('2. Record any insights in your journal');
        messages.push('3. Code review will run automatically (6 agents in parallel)');
        messages.push('4. Ask the user to run `/complete-task` to finalize the task\n');
      } else {
        messages.push('2. Code review will run automatically (6 agents in parallel)');
        messages.push('3. Ask the user to run `/complete-task` to finalize the task\n');
      }
      messages.push('**✅ Validation passed! Ready for code review.**\n');
    }

    return {
      success: true,
      messages,
      warnings,
      data: {
        validation: result,
        readyForCompletion: validationPassed,
      },
      exitCode: 0,
    };
  } catch (error) {
    // Handle cases where validation-checks command fails completely
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
      success: true,
      messages,
      warnings,
      data: {
        error: error instanceof Error ? error.message : 'Unknown error',
      },
      exitCode: 0,
    };
  }
}

// CLI entrypoint
if (import.meta.main) {
  prepareCompletionAction()
    .then((result) => {
      // Output as JSON for command parsing
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
