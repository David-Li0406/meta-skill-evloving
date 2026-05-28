import type { execSync } from 'node:child_process';
import type { getActiveTaskId } from '../lib/claude-md';
import type { getConfig, getGitHubConfig, isGitHubIntegrationEnabled } from '../lib/config';
import type { getCurrentBranch, getDefaultBranch, getMergeBase } from '../lib/git-helpers';
import type { pushCurrentBranch } from '../lib/github-helpers';
import type { createLogger } from '../lib/logger';
import type {
  getActiveMetadata,
  getActiveSpecDirectory,
  getSpecDirectory,
  readSpecFile,
  SpecFileOperations,
  updateMetadata,
} from '../lib/spec-helpers';
import type { runValidationChecks } from '../lib/validation';
import type { CommandDeps, CommandResult, FileSystemLike } from './context';

/**
 * Cross-platform delay function that works on Windows, Mac, and Linux
 * Uses busy-wait for synchronous delay without requiring shell commands
 * @param ms - Milliseconds to delay
 */
function crossPlatformDelay(ms: number): void {
  const start = Date.now();
  while (Date.now() - start < ms) {
    // Busy wait - not ideal for long delays but works cross-platform
    // For short delays (2-3 seconds) this is acceptable
  }
}

export interface CompleteTaskOptions {
  noSquash?: boolean;
  noBranch?: boolean;
  skipValidation?: boolean;
  message?: string;
}

export interface CompleteTaskResultData {
  taskId?: string;
  taskTitle?: string;
  updates: {
    taskFile?: string;
    claudeMd?: string;
    noActiveTask?: string;
  };
  validation: {
    preflightPassed?: boolean;
    typescript?: string;
    lint?: string;
    tests?: string;
    knip?: string;
  };
  git: {
    squashed?: boolean;
    commitMessage?: string;
    branchMerged?: boolean;
    branchPushed?: boolean;
    branchSwitched?: boolean;
    defaultBranch?: string;
    notes?: string;
    safetyCommit?: boolean;
    wipCommitCount?: number;
    reverted?: boolean;
  };
  github?: {
    prWorkflow?: boolean;
    prCreated?: boolean;
    prExists?: boolean;
    prUrl?: string;
    issueNumber?: number;
    branchName?: string;
  };
  filesChanged?: string[];
}

interface CompleteTaskState extends CompleteTaskResultData {
  originalTaskContent?: string;
  originalClaudeMdContent?: string;
  originalNoActiveTaskContent?: string;
  originalMetadataContent?: string; // For spec structure revert
  activeSpecDir?: string; // Track which spec directory was being completed
}

export interface CompleteTaskDeps {
  cwd: () => string;
  fs: Pick<FileSystemLike, 'existsSync' | 'readFileSync' | 'writeFileSync'>;
  path: CommandDeps['path'];
  execSync: typeof execSync;
  getActiveTaskId: typeof getActiveTaskId;
  getConfig: typeof getConfig;
  getGitHubConfig: typeof getGitHubConfig;
  isGitHubIntegrationEnabled: typeof isGitHubIntegrationEnabled;
  getCurrentBranch: typeof getCurrentBranch;
  getDefaultBranch: typeof getDefaultBranch;
  getMergeBase: typeof getMergeBase;
  pushCurrentBranch: typeof pushCurrentBranch;
  runValidationChecks: typeof runValidationChecks;
  todayISO: () => string;
  logger: ReturnType<typeof createLogger>;
  // Spec-helpers functions
  getActiveSpecDirectory: typeof getActiveSpecDirectory;
  getActiveMetadata: typeof getActiveMetadata;
  getSpecDirectory: typeof getSpecDirectory;
  readSpecFile: typeof readSpecFile;
  updateMetadata: typeof updateMetadata;
  specFileOps: SpecFileOperations;
}

interface ExistingPullRequest {
  number: number;
  url: string;
  state: string;
}

interface BranchContext {
  currentBranch?: string;
  taskBranchName?: string;
  existingPr?: ExistingPullRequest | null;
  remoteHasCommits: boolean;
}

interface CompletionMessages {
  messages: string[];
  warnings: string[];
  error?: string;
  exitCode?: number;
}

function createBaseState(): CompleteTaskState {
  return {
    updates: {},
    validation: {},
    git: {},
  };
}

function buildFailureResult(
  state: CompleteTaskState,
  details: CompletionMessages,
): CommandResult<CompleteTaskResultData> {
  return {
    success: false,
    error: details.error ?? 'Task completion failed',
    messages: details.messages,
    warnings: details.warnings,
    exitCode: details.exitCode ?? 1,
    data: state,
  };
}

function buildSuccessResult(
  state: CompleteTaskState,
  details: CompletionMessages,
): CommandResult<CompleteTaskResultData> {
  return {
    success: true,
    messages: details.messages,
    warnings: details.warnings,
    data: state,
  };
}

function detectBranchContext(projectRoot: string, deps: CompleteTaskDeps, options: CompleteTaskOptions): BranchContext {
  const context: BranchContext = {
    currentBranch: deps.getCurrentBranch(projectRoot) || undefined,
    remoteHasCommits: false,
  };

  context.taskBranchName = context.currentBranch;

  const githubConfig = deps.getGitHubConfig();
  const prWorkflow = deps.isGitHubIntegrationEnabled() && githubConfig?.auto_create_prs;

  if (!options.noBranch && prWorkflow && context.taskBranchName && context.currentBranch === context.taskBranchName) {
    try {
      const escapedBranch = context.taskBranchName.replace(/'/g, "'\\''");
      const output = deps.execSync(`gh pr list --head '${escapedBranch}' --json number,url,state`, {
        cwd: projectRoot,
        encoding: 'utf-8',
      });
      const prs = JSON.parse(output) as ExistingPullRequest[];
      context.existingPr = prs.find((pr) => pr.state === 'OPEN') ?? null;
    } catch (error) {
      deps.logger.debug('Failed to detect existing PR', { error });
    }
  }

  if (context.taskBranchName) {
    try {
      const remoteBranch = `origin/${context.taskBranchName}`;
      try {
        deps.execSync(`git rev-parse --verify ${remoteBranch}`, {
          cwd: projectRoot,
          stdio: 'pipe',
        });

        const defaultBranch = deps.getDefaultBranch(projectRoot);
        // Use origin/defaultBranch to ensure we get the latest merge-base
        // This prevents issues when local main is behind origin/main
        const mergeBase = deps
          .execSync(`git merge-base origin/${defaultBranch} ${remoteBranch}`, {
            cwd: projectRoot,
            encoding: 'utf-8',
          })
          .trim();

        if (mergeBase) {
          const remoteCommits = deps
            .execSync(`git rev-list ${mergeBase}..${remoteBranch}`, {
              cwd: projectRoot,
              encoding: 'utf-8',
            })
            .trim();

          context.remoteHasCommits = remoteCommits.length > 0;

          if (context.remoteHasCommits) {
            deps.logger.info('Remote branch has commits; squashing disabled', {
              branch: context.taskBranchName,
              commitCount: remoteCommits.split('\n').filter(Boolean).length,
            });
          }
        }
      } catch {
        context.remoteHasCommits = false;
      }
    } catch (error) {
      deps.logger.warn('Failed to determine remote branch state', { error });
      context.remoteHasCommits = true;
    }
  }

  return context;
}

function appendCompletedTaskEntry(content: string, entry: string): string {
  if (content.includes('## Completed Tasks:')) {
    return content.replace(/(## Completed Tasks:[\s\S]*?)(\n\n|\n$)/, `$1\n${entry}$2`);
  }

  return content.replace(
    'The following tasks are being tracked in this project:',
    `The following tasks are being tracked in this project:\n\n## Completed Tasks:\n${entry}`,
  );
}

function collectValidationWarnings(state: CompleteTaskState): string[] {
  const warnings: string[] = [];
  if (state.validation.typescript) {
    warnings.push(`TypeScript: ${state.validation.typescript}`);
  }
  if (state.validation.lint) {
    warnings.push(`Linting: ${state.validation.lint}`);
  }
  if (state.validation.tests) {
    warnings.push(`Tests: ${state.validation.tests}`);
  }
  if (state.validation.knip) {
    warnings.push(`Knip: ${state.validation.knip}`);
  }
  return warnings;
}

function buildValidationFailureMessage(state: CompleteTaskState): CompletionMessages {
  const messages = [
    '## ❌ Task Completion Failed\n',
    'Error: Pre-flight validation failed. Run /prepare-completion to fix issues.\n',
  ];
  const warnings = collectValidationWarnings(state);
  if (warnings.length > 0) {
    messages.push('Validation issues detected:');
    for (const warning of warnings) {
      messages.push(`- ${warning}`);
    }
  }
  return {
    messages,
    warnings: [],
    error: 'Pre-flight validation failed. Run /prepare-completion to fix issues.',
    exitCode: 1,
  };
}

function buildPushFailureMessages(state: CompleteTaskState, warnings: string[]): CompletionMessages {
  const messages = [
    '## ❌ Push Failed - Task Completion Reverted\n',
    'The push to origin failed, so the task completion has been reverted.\n',
    '**Next steps:**',
    '1. Check for merge conflicts or authentication issues',
    '2. Manually push the branch: `git push -u origin HEAD`',
    '3. Once push succeeds, run `/complete-task` again\n',
    '**Current state:**',
    `- Still on branch: ${state.github?.branchName || 'feature branch'}`,
    '- Task marked as in_progress',
    '- Commits were squashed but not pushed',
  ];
  return { messages, warnings, error: 'Failed to push branch to origin', exitCode: 1 };
}

function buildSuccessMessages(state: CompleteTaskState, warnings: string[]): CompletionMessages {
  const messages: string[] = [];
  messages.push('## Your Tasks\n');

  let summaryIndex = 1;

  if (state.github?.prCreated && state.github.prUrl) {
    messages.push(
      "Don't panic! You might have just seen a system reminder that a bucnh of files were reverted. This is completely normal because we've just switched back to main. All the work is safely pushed on the working branch and waiting to be merged in the pull request.\n",
    );
    messages.push('### 1. Enhance the Pull Request\n');
    messages.push('A PR was created automatically. Enhance its description with comprehensive details:\n');
    messages.push('```bash');
    messages.push(
      `gh pr edit ${state.github.prUrl} --body "## Summary\\nCompletes ${state.taskId}: ${state.taskTitle}\\n\\n## What Was Delivered\\n[List the key deliverables from this task]\\n\\n## Technical Implementation\\n[Describe important technical details, architecture decisions, patterns used]\\n\\n## Testing\\n[Explain how changes were tested and the results]"`,
    );
    messages.push('A PR was created automatically. Enhance its description with comprehensive details:\n');
    messages.push('```bash');
    messages.push(
      `gh pr edit ${state.github.prUrl} --body "## Summary\\nCompletes ${state.taskId}: ${state.taskTitle}\\n\\n## What Was Delivered\\n[List the key deliverables from this task]\\n\\n## Technical Implementation\\n[Describe important technical details, architecture decisions, patterns used]\\n\\n## Testing\\n[Explain how changes were tested and the results]"`,
    );
    messages.push('```\n');
    summaryIndex = 2;
  } else if (state.github?.prExists && state.github.prUrl) {
    messages.push('### 1. Pull Request Updated\n');
    messages.push(`Updated existing PR with new commits: ${state.github.prUrl}\n`);
    messages.push('The PR was not recreated since it already exists.\n');
    messages.push('If there were new changes, they have been pushed to the PR.\n');
    messages.push('No squashing was performed to preserve PR review history.\n');
    summaryIndex = 2;
  } else if (state.git.branchPushed) {
    messages.push('### 1. Note About Pull Request\n');
    messages.push('The branch was pushed but PR creation failed or was skipped.\n');
    messages.push('Manual PR creation may be needed.\n');
    summaryIndex = 2;
  }

  messages.push(`### ${summaryIndex}. Provide Summary to User\n`);
  messages.push('Report the completion status including:');
  messages.push(`- Task ${state.taskId} completed: ${state.taskTitle}`);
  if (state.git.squashed) {
    messages.push(`- Git: ${state.git.wipCommitCount || 'Multiple'} WIP commits squashed successfully`);
  } else if (state.github?.prExists) {
    messages.push('- Git: Pushed new commits to existing PR (no squashing to preserve history)');
  }
  if (state.github?.prCreated) {
    messages.push(`- PR created: ${state.github.prUrl}`);
  } else if (state.github?.prExists) {
    messages.push(`- PR updated: ${state.github.prUrl}`);
  }
  if (state.git.branchSwitched && state.git.defaultBranch) {
    messages.push(`- Switched to ${state.git.defaultBranch} branch`);
  }
  if (warnings.length > 0) {
    messages.push(`- Warnings: ${warnings.join(', ')}`);
  }

  return { messages, warnings };
}

function revertTaskChanges(projectRoot: string, state: CompleteTaskState, deps: CompleteTaskDeps): void {
  // Revert metadata for spec structure
  if (state.originalMetadataContent && state.activeSpecDir) {
    const metadataPath = deps.path.join(state.activeSpecDir, '.metadata.json');
    deps.fs.writeFileSync(metadataPath, state.originalMetadataContent);
  }

  // Restore CLAUDE.md (which contains the active spec reference)
  if (state.originalClaudeMdContent) {
    const claudeMdPath = deps.path.join(projectRoot, 'CLAUDE.md');
    deps.fs.writeFileSync(claudeMdPath, state.originalClaudeMdContent);
  }

  // Revert no_active_task.md if it was updated
  if (state.originalNoActiveTaskContent) {
    const noActiveTaskPath = deps.path.join(projectRoot, '.cc-track', 'no_active_task.md');
    deps.fs.writeFileSync(noActiveTaskPath, state.originalNoActiveTaskContent);
  }
}

function sanitizeCommitMessage(message: string): string {
  return message.replace(/'/g, "'\\''");
}

function commitUncommittedChanges(
  projectRoot: string,
  message: string,
  deps: CompleteTaskDeps,
  state: CompleteTaskState,
  warnings: string[],
): void {
  try {
    const gitStatus = deps
      .execSync('git status --porcelain', {
        cwd: projectRoot,
        encoding: 'utf-8',
      })
      .trim();

    if (gitStatus) {
      try {
        deps.execSync('git add -A', { cwd: projectRoot });
        deps.execSync(`git commit -m '${sanitizeCommitMessage(message)}'`, { cwd: projectRoot });
        state.git.safetyCommit = true;
        deps.logger.info('Created final documentation commit before squashing', { message });
      } catch (commitError) {
        warnings.push(
          `Failed to commit final changes: ${commitError instanceof Error ? commitError.message : commitError}`,
        );
      }
    }
  } catch (statusError) {
    deps.logger.debug('Failed to inspect git status before squashing', { error: statusError });
  }
}

function computeChangedFiles(projectRoot: string, reference: string, deps: CompleteTaskDeps): string[] {
  try {
    return deps
      .execSync(`git diff --name-only ${reference}`, { cwd: projectRoot, encoding: 'utf-8' })
      .trim()
      .split('\n')
      .filter(Boolean);
  } catch {
    return [];
  }
}

async function performSquashAndSummary(
  projectRoot: string,
  options: CompleteTaskOptions,
  deps: CompleteTaskDeps,
  state: CompleteTaskState,
  branchContext: BranchContext,
  warnings: string[],
): Promise<void> {
  const shouldSquash = !options.noSquash && !branchContext.existingPr && !branchContext.remoteHasCommits;

  const defaultBranch = deps.getDefaultBranch(projectRoot);
  const currentBranch = branchContext.currentBranch || deps.getCurrentBranch(projectRoot);

  if (shouldSquash) {
    commitUncommittedChanges(
      projectRoot,
      options.message || `docs: final ${state.taskId} documentation updates`,
      deps,
      state,
      warnings,
    );

    if (currentBranch && currentBranch !== defaultBranch) {
      const mergeBase = deps.getMergeBase(currentBranch, defaultBranch, projectRoot);

      if (mergeBase) {
        try {
          const commitCountRaw = deps.execSync(`git rev-list --count ${mergeBase}..HEAD`, {
            cwd: projectRoot,
            encoding: 'utf-8',
          });
          const commitCount = parseInt(commitCountRaw.trim(), 10);

          if (commitCount > 1) {
            const commitMessage = options.message || `feat: complete ${state.taskId} - ${state.taskTitle}`;
            deps.execSync(`git reset --soft ${mergeBase}`, { cwd: projectRoot });
            deps.execSync(`git commit -m '${sanitizeCommitMessage(commitMessage)}'`, { cwd: projectRoot });
            state.git.squashed = true;
            state.git.commitMessage = commitMessage;
            state.git.wipCommitCount = commitCount;
            state.git.notes = `Squashed ${commitCount} commits from branch into single commit`;
            deps.logger.info('Squashed commits for completion', { commitCount, commitMessage });
          } else if (commitCount === 1) {
            state.git.notes = 'Only one commit on branch - no squashing needed';
          } else {
            state.git.notes = 'No commits to squash on this branch';
          }

          state.filesChanged = computeChangedFiles(projectRoot, `${mergeBase}..HEAD`, deps);
        } catch (error) {
          warnings.push(`Failed to squash commits: ${error instanceof Error ? error.message : error}`);
          state.git.notes = 'Squash attempted but failed';
        }
      } else {
        state.git.notes = 'Could not determine merge base with default branch';
      }
    } else {
      state.git.notes = 'Already on default branch - no squashing needed';
      state.filesChanged = computeChangedFiles(projectRoot, 'HEAD~1..HEAD', deps);
    }
  } else {
    if (branchContext.remoteHasCommits) {
      state.git.notes = 'Remote branch has commits - skipping squash to preserve history';
    } else if (branchContext.existingPr) {
      state.git.notes = 'PR already exists - skipping squash';
    } else if (options.noSquash) {
      state.git.notes = 'Squashing disabled by --no-squash flag';
    }

    commitUncommittedChanges(
      projectRoot,
      options.message ||
        (branchContext.existingPr
          ? `docs: update ${state.taskId} based on PR feedback`
          : `docs: update ${state.taskId} documentation`),
      deps,
      state,
      warnings,
    );
  }
}

function handleGitHubWorkflow(
  projectRoot: string,
  taskContent: string,
  deps: CompleteTaskDeps,
  state: CompleteTaskState,
  branchContext: BranchContext,
  warnings: string[],
  options: CompleteTaskOptions,
): CompletionMessages | null {
  const githubConfig = deps.getGitHubConfig();
  const prWorkflow = deps.isGitHubIntegrationEnabled() && githubConfig?.auto_create_prs;
  if (!branchContext.taskBranchName || options.noBranch) {
    return null;
  }

  if (prWorkflow) {
    const issueMatch = taskContent.match(/<!-- github_issue: (\d+) -->/);

    // Warn if we're not on the expected branch, but continue with the current branch
    if (branchContext.currentBranch !== branchContext.taskBranchName) {
      warnings.push(
        `Not on expected task branch (current: ${branchContext.currentBranch}, expected: ${branchContext.taskBranchName})`,
      );
      deps.logger.warn('Branch name mismatch - using current branch for PR', {
        current: branchContext.currentBranch,
        expected: branchContext.taskBranchName,
      });
    }

    const pushSuccess = deps.pushCurrentBranch(projectRoot);
    if (!pushSuccess) {
      state.git.branchPushed = false;
      state.git.reverted = true;
      warnings.push('Failed to push branch to origin');
      return buildPushFailureMessages(state, warnings);
    }

    state.git.branchPushed = true;
    const defaultBranch = deps.getDefaultBranch(projectRoot);
    state.git.defaultBranch = defaultBranch;

    // Add a small delay after push to allow GitHub API to recognize the branch
    // This helps avoid "must first push" errors when creating PRs immediately after pushing
    deps.logger.debug('Waiting for GitHub to recognize pushed branch');
    crossPlatformDelay(2000); // 2 second delay

    if (branchContext.existingPr) {
      state.github = {
        prWorkflow: true,
        prExists: true,
        prUrl: branchContext.existingPr.url,
        branchName: branchContext.taskBranchName,
        issueNumber: issueMatch ? Number(issueMatch[1]) : undefined,
      };
      state.git.notes = `Updated existing PR: ${branchContext.existingPr.url}`;
    } else {
      const prTitle = `feat: complete ${state.taskId} - ${state.taskTitle}`;
      const prBody =
        '## Summary\n' +
        `Completes ${state.taskId}: ${state.taskTitle}\n\n` +
        '🤖 Generated with [Claude Code](https://claude.ai/code)';
      const escapedDefaultBranch = defaultBranch.replace(/'/g, "'\\''");
      const escapedBranchName = branchContext.taskBranchName.replace(/'/g, "'\\''");
      const escapedTitle = prTitle.replace(/'/g, "'\\''");
      const escapedBody = prBody.replace(/'/g, "'\\''");

      let prCreated = false;
      let prUrl = '';
      let lastError: unknown = null;

      // Try to create PR with retry logic for "must push" errors
      for (let attempt = 1; attempt <= 2; attempt++) {
        try {
          deps.logger.debug(`Attempting to create PR (attempt ${attempt}/2)`);
          prUrl = deps
            .execSync(
              `gh pr create --base '${escapedDefaultBranch}' --head '${escapedBranchName}' --title '${escapedTitle}' --body '${escapedBody}'`,
              { cwd: projectRoot, encoding: 'utf-8' },
            )
            .trim();
          prCreated = true;
          deps.logger.info('PR created successfully', { prUrl, attempt });
          break;
        } catch (error) {
          lastError = error;
          const errorMessage = error instanceof Error ? error.message : String(error);

          // Check if this is a "must push" error that might benefit from a retry
          if (attempt === 1 && errorMessage.includes('you must first push')) {
            deps.logger.warn('PR creation failed with push error, waiting and retrying', {
              error: errorMessage,
              attempt,
            });
            // Wait a bit longer before retry
            crossPlatformDelay(3000); // 3 second delay
            continue;
          }

          // For other errors or second attempt, don't retry
          deps.logger.warn('PR creation failed', { error: errorMessage, attempt });
          break;
        }
      }

      if (prCreated) {
        state.github = {
          prWorkflow: true,
          prCreated: true,
          prUrl,
          branchName: branchContext.taskBranchName,
          issueNumber: issueMatch ? Number(issueMatch[1]) : undefined,
        };
        state.git.notes = `Created PR: ${prUrl}`;
      } else {
        warnings.push(`Failed to create PR: ${lastError instanceof Error ? lastError.message : lastError}`);
        state.git.notes = `Pushed ${branchContext.taskBranchName} to origin - ready for manual PR creation`;
        state.github = {
          prWorkflow: true,
          branchName: branchContext.taskBranchName,
          issueNumber: issueMatch ? Number(issueMatch[1]) : undefined,
        };
      }
    }

    try {
      deps.execSync(`git checkout ${defaultBranch}`, { cwd: projectRoot });
      deps.execSync(`git pull origin ${defaultBranch}`, { cwd: projectRoot });
      state.git.branchSwitched = true;
    } catch (switchError) {
      deps.logger.warn('Failed to switch to default branch after push', { error: switchError });
    }

    return null;
  }

  const config = deps.getConfig();
  if (config.features?.git_branching?.enabled) {
    const branchMatch = taskContent.match(/<!-- branch: (.*?) -->/);
    if (branchMatch && branchContext.currentBranch === branchMatch[1]) {
      const defaultBranch = deps.getDefaultBranch(projectRoot);
      state.git.defaultBranch = defaultBranch;
      try {
        deps.execSync(`git checkout ${defaultBranch}`, { cwd: projectRoot });
        deps.execSync(`git merge ${branchMatch[1]} --no-ff -m "Merge branch '${branchMatch[1]}'"`, {
          cwd: projectRoot,
        });
        state.git.branchMerged = true;
        state.git.notes = `Merged ${branchMatch[1]} into ${defaultBranch}`;
      } catch (mergeError) {
        const message = mergeError instanceof Error ? mergeError.message : String(mergeError);
        warnings.push(`Failed to merge branch: ${message}`);
        state.git.branchMerged = false;
        try {
          deps.execSync(`git checkout ${branchMatch[1]}`, { cwd: projectRoot });
        } catch {}
      }
    } else {
      state.git.notes = branchMatch
        ? `Task branch ${branchMatch[1]} not currently checked out`
        : 'No branch information in task file';
    }
  }

  return null;
}

export async function runCompleteTask(
  options: CompleteTaskOptions,
  deps: CompleteTaskDeps,
): Promise<CommandResult<CompleteTaskResultData>> {
  const state = createBaseState();
  const warnings: string[] = [];
  const projectRoot = deps.cwd();
  const ccTrackDir = deps.path.join(projectRoot, '.cc-track');
  const claudeMdPath = deps.path.join(projectRoot, 'CLAUDE.md');
  const noActiveTaskPath = deps.path.join(ccTrackDir, 'no_active_task.md');

  try {
    if (!options.skipValidation) {
      const validation = await deps.runValidationChecks(projectRoot);
      state.validation.preflightPassed = validation.readyForCompletion;
      if (!validation.readyForCompletion) {
        if (validation.validation?.typescript?.errorCount) {
          state.validation.typescript = `${validation.validation.typescript.errorCount} errors`;
        }
        if (validation.validation?.lint?.issueCount) {
          state.validation.lint = `${validation.validation.lint.issueCount} issues`;
        }
        if (validation.validation?.tests?.failCount) {
          state.validation.tests = `${validation.validation.tests.failCount} tests failing`;
        }
        if (validation.validation?.knip && validation.validation.knip.passed === false) {
          const knipIssues: string[] = [];
          if (validation.validation.knip.unusedFiles) {
            knipIssues.push(`${validation.validation.knip.unusedFiles} unused files`);
          }
          if (validation.validation.knip.unusedExports) {
            knipIssues.push(`${validation.validation.knip.unusedExports} unused exports`);
          }
          if (validation.validation.knip.unusedDeps) {
            knipIssues.push(`${validation.validation.knip.unusedDeps} unused dependencies`);
          }
          state.validation.knip = knipIssues.join(', ');
        }

        return buildFailureResult(state, buildValidationFailureMessage(state));
      }
    } else {
      state.validation.preflightPassed = true;
    }
  } catch (error) {
    return buildFailureResult(state, {
      messages: [
        '## ❌ Task Completion Failed\n',
        `Error: Pre-flight validation check failed: ${error instanceof Error ? error.message : String(error)}\n`,
        'Please resolve validation tooling issues and retry `/complete-task`.\n',
      ],
      warnings,
      error: `Pre-flight validation check failed: ${error instanceof Error ? error.message : String(error)}`,
      exitCode: 1,
    });
  }

  if (!deps.fs.existsSync(claudeMdPath)) {
    return buildFailureResult(state, {
      messages: [
        '## ❌ Task Completion Failed\n',
        'Error: CLAUDE.md not found\n',
        'Please ensure cc-track is initialized. Run `/setup-cc-track` if needed, then retry.',
      ],
      warnings,
      error: 'CLAUDE.md not found',
    });
  }

  state.originalClaudeMdContent = deps.fs.readFileSync(claudeMdPath, 'utf-8');

  // Get active spec directory and metadata
  const activeSpecDir = deps.getActiveSpecDirectory(projectRoot, deps.specFileOps);
  const activeMetadata = activeSpecDir ? deps.getActiveMetadata(projectRoot, deps.specFileOps) : null;

  if (!activeSpecDir || !activeMetadata) {
    return buildFailureResult(state, {
      messages: [
        '## ❌ Task Completion Failed\n',
        'Error: No active task found in CLAUDE.md\n',
        'Ensure an active task is set before running `/complete-task`.',
      ],
      warnings,
      error: 'No active task found in CLAUDE.md',
    });
  }

  // Store active spec directory for potential revert
  state.activeSpecDir = activeSpecDir;

  // Use spec-driven structure
  const taskId = activeMetadata.task_id;

  // Read title from spec.md
  const specContent = deps.readSpecFile(activeSpecDir, 'spec.md', deps.specFileOps);
  const titleMatch = specContent?.match(/^# (.+)$/m);
  const taskTitle = titleMatch ? titleMatch[1] : `Feature ${taskId}`;

  // Check status
  if (activeMetadata.status !== 'in_progress') {
    warnings.push(`Task status is ${activeMetadata.status}, not in_progress - continuing anyway`);
  }

  // Store original metadata content for potential revert
  const metadataPath = deps.path.join(activeSpecDir, '.metadata.json');
  state.originalMetadataContent = deps.fs.readFileSync(metadataPath, 'utf-8');

  // Update metadata to completed
  const todayIso = deps.todayISO();
  deps.updateMetadata(activeSpecDir, { status: 'completed', completed: todayIso }, deps.specFileOps);
  state.updates.taskFile = 'metadata updated';
  state.taskId = taskId;
  state.taskTitle = taskTitle;

  // Use spec content for GitHub workflow
  const finalTaskContent = specContent || '';

  if (deps.fs.existsSync(noActiveTaskPath)) {
    const originalNoActiveTaskContent = deps.fs.readFileSync(noActiveTaskPath, 'utf-8');
    state.originalNoActiveTaskContent = originalNoActiveTaskContent;
    const entry = `- ${taskId}: ${state.taskTitle}`;
    const newContent = appendCompletedTaskEntry(originalNoActiveTaskContent, entry);
    deps.fs.writeFileSync(noActiveTaskPath, newContent);
    state.updates.noActiveTask = 'updated';
  } else {
    warnings.push('no_active_task.md not found');
  }

  // Clear active spec reference from CLAUDE.md BEFORE commit/push so it's included in the PR
  let updatedClaudeMd = deps.fs.readFileSync(claudeMdPath, 'utf-8');
  updatedClaudeMd = updatedClaudeMd.replace(/@\.cc-track\/specs\/\d+-[^/]+\/spec\.md/, '@.cc-track/no_active_task.md');
  deps.fs.writeFileSync(claudeMdPath, updatedClaudeMd);
  state.updates.claudeMd = 'cleared active spec';

  const branchContext = detectBranchContext(projectRoot, deps, options);
  await performSquashAndSummary(projectRoot, options, deps, state, branchContext, warnings);

  const failureResult = handleGitHubWorkflow(
    projectRoot,
    finalTaskContent,
    deps,
    state,
    branchContext,
    warnings,
    options,
  );

  if (failureResult) {
    state.git.reverted = true;
    revertTaskChanges(projectRoot, state, deps);
    return buildFailureResult(state, failureResult);
  }

  const messages = buildSuccessMessages(state, warnings);
  return buildSuccessResult(state, messages);
}

// CLI entrypoint
if (import.meta.main) {
  import('node:child_process').then(({ execSync }) => {
    import('node:path').then((path) => {
      import('node:fs').then(({ existsSync, readFileSync, writeFileSync }) => {
        import('../lib/claude-md').then(({ getActiveTaskId }) => {
          import('../lib/config').then(({ getConfig, getGitHubConfig, isGitHubIntegrationEnabled }) => {
            import('../lib/git-helpers').then(({ getCurrentBranch, getDefaultBranch, getMergeBase }) => {
              import('../lib/github-helpers').then(({ pushCurrentBranch }) => {
                import('../lib/validation').then(({ runValidationChecks }) => {
                  import('../lib/logger').then(({ createLogger }) => {
                    import('../lib/spec-helpers').then(
                      ({
                        getActiveSpecDirectory,
                        getActiveMetadata,
                        getSpecDirectory,
                        readSpecFile,
                        updateMetadata,
                      }) => {
                        const args = process.argv.slice(2);
                        const options: CompleteTaskOptions = {
                          noSquash: args.includes('--no-squash'),
                          noBranch: args.includes('--no-branch'),
                          skipValidation: args.includes('--skip-validation'),
                        };

                        import('node:fs').then(({ mkdirSync }) => {
                          const deps: CompleteTaskDeps = {
                            cwd: () => process.cwd(),
                            fs: { existsSync, readFileSync, writeFileSync },
                            path,
                            execSync,
                            getActiveTaskId,
                            getConfig,
                            getGitHubConfig,
                            isGitHubIntegrationEnabled,
                            getCurrentBranch,
                            getDefaultBranch,
                            getMergeBase,
                            pushCurrentBranch,
                            runValidationChecks,
                            todayISO: () => {
                              const now = new Date();
                              return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
                            },
                            logger: createLogger('complete-task'),
                            getActiveSpecDirectory,
                            getActiveMetadata,
                            getSpecDirectory,
                            readSpecFile,
                            updateMetadata,
                            specFileOps: { existsSync, mkdirSync, readFileSync, writeFileSync },
                          };

                          runCompleteTask(options, deps)
                            .then((result) => {
                              if (result.messages) {
                                for (const msg of result.messages) {
                                  console.log(msg);
                                }
                              }
                              if (result.warnings) {
                                for (const warn of result.warnings) {
                                  console.warn(warn);
                                }
                              }
                              if (!result.success && result.error) {
                                console.error(result.error);
                              }
                              process.exitCode = result.exitCode ?? (result.success ? 0 : 1);
                            })
                            .catch((error) => {
                              console.error(
                                'Unexpected error:',
                                error instanceof Error ? error.message : String(error),
                              );
                              process.exitCode = 1;
                            });
                        });
                      },
                    );
                  });
                });
              });
            });
          });
        });
      });
    });
  });
}
