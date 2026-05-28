import { execSync } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path/posix';
import { getActiveTaskId } from './claude-md';
import { type EditValidationConfig, getConfig, getLintConfig, getTestConfig } from './config';
import { isWipCommit } from './git-helpers';
import { getLintParser } from './lint-parsers';
import { createLogger } from './logger';
import { getActiveSpecDirectory, readMetadata, type SpecFileOperations } from './spec-helpers';

const logger = createLogger('validation');

interface ValidationResult {
  typescript?: {
    passed: boolean;
    errors?: string;
    errorCount?: number;
  };
  lint?: {
    passed: boolean;
    errors?: string;
    issueCount?: number;
  };
  tests?: {
    passed: boolean;
    errors?: string;
    failCount?: number;
  };
  knip?: {
    passed: boolean;
    unusedFiles?: number;
    unusedExports?: number;
    unusedDeps?: number;
    details?: string;
  };
}

interface GitStatus {
  hasUncommittedChanges: boolean;
  modifiedFiles: string[];
  wipCommitCount: number;
  currentBranch: string;
  isTaskBranch: boolean;
}

interface TaskInfo {
  exists: boolean;
  taskId?: string;
  taskTitle?: string;
  status?: string;
  filePath?: string;
}

export interface PreparationResult {
  success: boolean;
  readyForCompletion: boolean;
  task: TaskInfo;
  validation: ValidationResult;
  git: GitStatus;
  warnings: string[];
  error?: string;
}

/**
 * Run TypeScript validation
 */
function runTypeScriptCheck(projectRoot: string, deps: ValidationDeps = {}): ValidationResult['typescript'] {
  const getConfigFn = deps.getConfig || getConfig;
  const exec = deps.execSync || execSync;
  const log = deps.logger || logger;

  try {
    const config = getConfigFn();
    const editValidation = config.hooks?.edit_validation as EditValidationConfig | undefined;
    const tsConfig = editValidation?.typecheck;

    if (!tsConfig?.enabled) {
      log.info('TypeScript check disabled');
      return { passed: true };
    }

    const command = tsConfig?.command || 'bunx tsc --noEmit';

    log.info('Running TypeScript check', { command });
    exec(command, { cwd: projectRoot, encoding: 'utf-8' });

    return { passed: true };
  } catch (error) {
    const err = error as { stdout?: string; stderr?: string };
    const output = err.stdout || err.stderr || 'TypeScript check failed';
    const errorCount = (output.match(/error TS/g) || []).length;

    log.error('TypeScript check failed', { errorCount });
    return {
      passed: false,
      errors: output.substring(0, 2000), // Limit output size
      errorCount,
    };
  }
}

/**
 * Run linting and auto-formatting
 */
function runLintCheck(projectRoot: string, deps: ValidationDeps = {}): ValidationResult['lint'] {
  const getLintConfigFn = deps.getLintConfig || getLintConfig;
  const exec = deps.execSync || execSync;
  const getParserFn = deps.getLintParser || getLintParser;
  const log = deps.logger || logger;

  try {
    const lintConfig = getLintConfigFn();
    if (!lintConfig || !lintConfig.enabled) {
      log.info('Lint check disabled');
      return { passed: true };
    }

    // First, run auto-formatter if configured
    if (lintConfig.autoFixCommand) {
      try {
        log.info('Running lint auto-formatter', { command: lintConfig.autoFixCommand });
        exec(lintConfig.autoFixCommand, { cwd: projectRoot, encoding: 'utf-8' });
      } catch {
        // Auto-formatter might fail if there are syntax errors, continue to check
      }
    }

    // Now run the lint check
    const command = lintConfig.command;
    log.info('Running lint check', { command, tool: lintConfig.tool || 'biome' });
    exec(command, { cwd: projectRoot, encoding: 'utf-8' });

    return { passed: true };
  } catch (error) {
    const err = error as { stdout?: string; stderr?: string };
    const output = err.stdout || err.stderr || 'Lint check failed';

    // Parse output using the appropriate parser
    const lintConfig = getLintConfigFn();
    const parser = getParserFn(lintConfig?.tool || 'biome');
    const parseResult = parser.parseOutput(output);

    log.error('Lint check failed', { issueCount: parseResult.issueCount });
    return {
      passed: false,
      errors: output.substring(0, 2000),
      issueCount: parseResult.issueCount,
    };
  }
}

/**
 * Run tests
 */
function runTests(projectRoot: string, deps: ValidationDeps = {}): ValidationResult['tests'] {
  const fs = deps.fileOps || { existsSync, mkdirSync, readFileSync, writeFileSync };
  const exec = deps.execSync || execSync;
  const getTestConfigFn = deps.getTestConfig || getTestConfig;
  const log = deps.logger || logger;

  try {
    const testConfig = getTestConfigFn();
    if (!testConfig || !testConfig.enabled) {
      log.info('Tests disabled');
      return { passed: true };
    }

    const command = testConfig.command || 'bun test';

    // Check if test script exists in package.json
    const packageJsonPath = join(projectRoot, 'package.json');
    if (fs.existsSync(packageJsonPath)) {
      const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf-8'));
      if (!packageJson.scripts?.test) {
        log.info('No test script found in package.json');
        return { passed: true };
      }
    }

    log.info('Running tests', { command });
    // Run tests silently and just check exit code
    // Use stdio options to suppress output cross-platform
    try {
      exec(command, {
        cwd: projectRoot,
        encoding: 'utf-8',
        stdio: ['pipe', 'ignore', 'ignore'], // Suppress stdout/stderr cross-platform
      });
      // If exec doesn't throw, tests passed
      log.info('All tests passed');
      return { passed: true };
    } catch (_testError) {
      // Tests failed - run again to get details for the error report
      let output: string;
      try {
        output = exec(command, {
          cwd: projectRoot,
          encoding: 'utf-8',
        });
      } catch (err) {
        const execErr = err as { stdout?: string; stderr?: string };
        output = execErr.stdout || execErr.stderr || '';
      }

      // Extract fail count and failed test details
      const failMatch = output.match(/(\d+)\s+fail/);
      const failCount = failMatch ? parseInt(failMatch[1], 10) : 1;

      // Extract only the failed test lines
      const failedTests = output
        .split('\n')
        .filter((line) => line.includes('(fail)'))
        .map((line) => line.trim())
        .join('\n');

      return {
        passed: false,
        errors: failedTests || 'Test failures detected',
        failCount: failCount,
      };
    }
  } catch (error) {
    const err = error as { stdout?: string; stderr?: string };
    const output = err.stdout || err.stderr || 'Tests failed';

    const failMatch = output.match(/(\d+)\s+fail/);
    const failCount = failMatch ? parseInt(failMatch[1], 10) : undefined;

    log.error('Tests failed', { failCount });
    return {
      passed: false,
      errors: output.substring(0, 2000),
      failCount,
    };
  }
}

/**
 * Run Knip for unused code detection
 */
function runKnipCheck(projectRoot: string, deps: ValidationDeps = {}): ValidationResult['knip'] {
  const getConfigFn = deps.getConfig || getConfig;
  const exec = deps.execSync || execSync;
  const log = deps.logger || logger;

  try {
    const config = getConfigFn();
    const editValidation = config.hooks?.edit_validation as EditValidationConfig | undefined;
    const knipConfig = editValidation?.knip;

    if (!knipConfig?.enabled) {
      log.info('Knip check disabled');
      return { passed: true };
    }

    const command = knipConfig.command || 'bunx knip';
    log.info('Running Knip check', { command });

    const output = exec(command, { cwd: projectRoot, encoding: 'utf-8' });

    // Parse Knip output
    const filesMatch = output.match(/Unused files\s+(\d+)/);
    const exportsMatch = output.match(/Unused exports\s+(\d+)/);
    const depsMatch = output.match(/Unused dependencies\s+(\d+)/);

    const unusedFiles = filesMatch ? parseInt(filesMatch[1], 10) : 0;
    const unusedExports = exportsMatch ? parseInt(exportsMatch[1], 10) : 0;
    const unusedDeps = depsMatch ? parseInt(depsMatch[1], 10) : 0;

    if (unusedFiles > 0 || unusedExports > 0 || unusedDeps > 0) {
      return {
        passed: false,
        unusedFiles,
        unusedExports,
        unusedDeps,
        details: output.substring(0, 1000),
      };
    }

    return { passed: true };
  } catch (error) {
    const err = error as { stdout?: string; stderr?: string };
    const output = err.stdout || err.stderr || '';

    // Parse even from error output
    const filesMatch = output.match(/Unused files\s+(\d+)/);
    const exportsMatch = output.match(/Unused exports\s+(\d+)/);
    const depsMatch = output.match(/Unused dependencies\s+(\d+)/);

    log.warn('Knip check completed with issues');
    return {
      passed: false,
      unusedFiles: filesMatch ? parseInt(filesMatch[1], 10) : undefined,
      unusedExports: exportsMatch ? parseInt(exportsMatch[1], 10) : undefined,
      unusedDeps: depsMatch ? parseInt(depsMatch[1], 10) : undefined,
      details: output.substring(0, 1000),
    };
  }
}

/**
 * Get git status information
 */
function getGitStatus(projectRoot: string, taskId?: string, deps: ValidationDeps = {}): GitStatus {
  const exec = deps.execSync || execSync;
  const isWipCommitFn = deps.isWipCommit || isWipCommit;
  const log = deps.logger || logger;

  try {
    // Check for uncommitted changes
    const statusOutput = exec('git status --porcelain', {
      cwd: projectRoot,
      encoding: 'utf-8',
    }).trim();

    const modifiedFiles = statusOutput
      .split('\n')
      .filter((line) => line.trim())
      .map((line) => line.substring(3).trim());

    // Get current branch
    const currentBranch = exec('git branch --show-current', {
      cwd: projectRoot,
      encoding: 'utf-8',
    }).trim();

    // Count WIP commits
    const gitLog = exec('git log --oneline -20', {
      cwd: projectRoot,
      encoding: 'utf-8',
    });

    const wipCommitCount = gitLog
      .split('\n')
      .filter((line) => line.trim())
      .filter((line) => isWipCommitFn(line)).length;

    // Check if on task branch
    const isTaskBranch = taskId ? currentBranch.includes(taskId.toLowerCase()) : false;

    log.info('Git status', {
      hasUncommittedChanges: modifiedFiles.length > 0,
      modifiedFileCount: modifiedFiles.length,
      wipCommitCount,
      currentBranch,
      isTaskBranch,
    });

    return {
      hasUncommittedChanges: modifiedFiles.length > 0,
      modifiedFiles,
      wipCommitCount,
      currentBranch,
      isTaskBranch,
    };
  } catch (error) {
    log.error('Failed to get git status', { error });
    return {
      hasUncommittedChanges: false,
      modifiedFiles: [],
      wipCommitCount: 0,
      currentBranch: 'unknown',
      isTaskBranch: false,
    };
  }
}

/**
 * Get task information
 */
function getTaskInfo(projectRoot: string, deps: ValidationDeps = {}): TaskInfo {
  const getActiveTaskIdFn = deps.getActiveTaskId || getActiveTaskId;
  const getActiveSpecDirFn = deps.getActiveSpecDirectory || getActiveSpecDirectory;
  const readMetadataFn = deps.readMetadata || readMetadata;
  const fs = deps.fileOps || { existsSync, mkdirSync, readFileSync, writeFileSync };
  const log = deps.logger || logger;

  try {
    const taskId = getActiveTaskIdFn(projectRoot);
    if (!taskId) {
      return { exists: false };
    }

    const specDir = getActiveSpecDirFn(projectRoot, fs);
    if (!specDir) {
      return { exists: false };
    }

    const metadata = readMetadataFn(specDir, fs);
    if (!metadata) {
      return { exists: false };
    }

    const specMdPath = join(specDir, 'spec.md');
    const specContent = fs.readFileSync(specMdPath, 'utf-8');

    const titleMatch = specContent.match(/^# (.+)$/m);
    const taskTitle = titleMatch ? titleMatch[1] : metadata.feature_name;

    log.info('Task info', {
      taskId: metadata.task_id,
      taskTitle,
      status: metadata.status,
    });

    return {
      exists: true,
      taskId: metadata.task_id,
      taskTitle,
      status: metadata.status,
      filePath: specMdPath,
    };
  } catch (error) {
    log.error('Failed to get task info', { error });
    return { exists: false };
  }
}

export interface ValidationDeps {
  execSync?: typeof execSync;
  fileOps?: SpecFileOperations;
  getConfig?: typeof getConfig;
  getLintConfig?: typeof getLintConfig;
  getTestConfig?: typeof getTestConfig;
  getActiveTaskId?: typeof getActiveTaskId;
  getActiveSpecDirectory?: typeof getActiveSpecDirectory;
  readMetadata?: typeof readMetadata;
  isWipCommit?: typeof isWipCommit;
  getLintParser?: typeof getLintParser;
  logger?: ReturnType<typeof createLogger>;
}

interface CoreValidationResult {
  validation: ValidationResult;
  allPassed: boolean;
  knipWarnings: string[];
}

/**
 * Run core validation checks (shared between task-aware and standalone validation)
 */
function runCoreValidationChecks(projectRoot: string, deps: ValidationDeps = {}): CoreValidationResult {
  const validation: ValidationResult = {};

  // TypeScript check
  validation.typescript = runTypeScriptCheck(projectRoot, deps);

  // Lint check
  validation.lint = runLintCheck(projectRoot, deps);

  // Test check
  validation.tests = runTests(projectRoot, deps);

  // Knip check
  validation.knip = runKnipCheck(projectRoot, deps);

  // Determine if all validation passed
  const allPassed =
    validation.typescript?.passed !== false && validation.lint?.passed !== false && validation.tests?.passed !== false;

  // Build Knip warnings (non-blocking)
  const knipWarnings: string[] = [];
  if (validation.knip?.passed === false) {
    const knipIssues = [];
    if (validation.knip.unusedFiles) {
      knipIssues.push(`${validation.knip.unusedFiles} unused files`);
    }
    if (validation.knip.unusedExports) {
      knipIssues.push(`${validation.knip.unusedExports} unused exports`);
    }
    if (validation.knip.unusedDeps) {
      knipIssues.push(`${validation.knip.unusedDeps} unused dependencies`);
    }
    if (knipIssues.length > 0) {
      knipWarnings.push(`Knip found: ${knipIssues.join(', ')}`);
    }
  }

  return { validation, allPassed, knipWarnings };
}

export interface ValidationFormatOptions {
  getLintConfig?: typeof getLintConfig;
}

/**
 * Format validation results into user-friendly messages
 * Shared between prepare-completion and code-review scripts
 */
export function formatValidationResults(validation: ValidationResult, options: ValidationFormatOptions = {}): string[] {
  const messages: string[] = [];
  const getLintConfigFn = options.getLintConfig || getLintConfig;

  // TypeScript errors
  if (validation.typescript?.passed === false) {
    messages.push('#### TypeScript Errors');
    messages.push(`Found ${validation.typescript.errorCount || 'multiple'} TypeScript errors.\n`);
    if (validation.typescript.errors) {
      messages.push('```');
      messages.push(validation.typescript.errors.substring(0, 1000));
      if (validation.typescript.errors.length > 1000) {
        messages.push('... (truncated)');
      }
      messages.push('```\n');
    }
    messages.push(
      '**Action:** Fix all TypeScript errors by updating type definitions and resolving type mismatches.\n',
    );
  }

  // Linting issues
  if (validation.lint?.passed === false) {
    messages.push('#### Linting Issues');
    messages.push(`Found ${validation.lint.issueCount || 'multiple'} linting issues.\n`);
    if (validation.lint.errors) {
      messages.push('```');
      messages.push(validation.lint.errors.substring(0, 1000));
      if (validation.lint.errors.length > 1000) {
        messages.push('... (truncated)');
      }
      messages.push('```\n');
    }

    const lintConfig = getLintConfigFn();
    const tool = lintConfig?.tool || 'biome';
    let fixAdvice = 'Fix linting issues';

    if (lintConfig?.autoFixCommand) {
      fixAdvice = `Fix linting issues. Many can be auto-fixed with \`${lintConfig.autoFixCommand}\``;
    } else if (tool === 'biome') {
      fixAdvice = 'Fix linting issues. Many can be auto-fixed with `bunx biome check --write`';
    } else if (tool === 'eslint') {
      fixAdvice = 'Fix linting issues. Many can be auto-fixed with `npx eslint --fix`';
    }

    messages.push(`**Action:** ${fixAdvice}.\n`);
  }

  // Test failures
  if (validation.tests?.passed === false) {
    messages.push('#### Test Failures');
    messages.push(`Found ${validation.tests.failCount || 'multiple'} failing tests.\n`);
    if (validation.tests.errors) {
      messages.push('```');
      messages.push(validation.tests.errors.substring(0, 1000));
      if (validation.tests.errors.length > 1000) {
        messages.push('... (truncated)');
      }
      messages.push('```\n');
    }
    messages.push('**Action:** Fix failing tests or update test expectations as needed.\n');
  }

  // Knip unused code warnings (non-blocking)
  if (validation.knip?.passed === false) {
    messages.push('#### Unused Code (Optional)');
    const issues = [];
    if (validation.knip.unusedFiles) {
      issues.push(`${validation.knip.unusedFiles} unused files`);
    }
    if (validation.knip.unusedExports) {
      issues.push(`${validation.knip.unusedExports} unused exports`);
    }
    if (validation.knip.unusedDeps) {
      issues.push(`${validation.knip.unusedDeps} unused dependencies`);
    }
    messages.push(`Knip found: ${issues.join(', ')}\n`);
    messages.push("**Note:** These are warnings and won't block, but consider cleaning them up.\n");
  }

  return messages;
}

/**
 * Run validation checks and return the result
 * This function can be called by other commands or used directly
 */
export async function runValidationChecks(
  projectRoot: string = process.cwd(),
  deps: ValidationDeps = {},
): Promise<PreparationResult> {
  const result: PreparationResult = {
    success: false,
    readyForCompletion: false,
    task: { exists: false },
    validation: {},
    git: {
      hasUncommittedChanges: false,
      modifiedFiles: [],
      wipCommitCount: 0,
      currentBranch: '',
      isTaskBranch: false,
    },
    warnings: [],
  };

  const log = deps.logger || logger;

  try {
    // Get task information
    result.task = getTaskInfo(projectRoot, deps);

    if (!result.task.exists) {
      result.error = 'No active task found';
      result.success = false;
      return result;
    }

    if (result.task.status !== 'in_progress') {
      result.warnings.push(`Task status is '${result.task.status}', expected 'in_progress'`);
    }

    // Get git status
    result.git = getGitStatus(projectRoot, result.task.taskId, deps);

    // Run validation checks
    log.info('Starting validation checks');
    const coreResult = runCoreValidationChecks(projectRoot, deps);
    result.validation = coreResult.validation;
    result.warnings.push(...coreResult.knipWarnings);
    result.readyForCompletion = coreResult.allPassed;
    result.success = true;

    log.info('Preparation check complete', {
      readyForCompletion: result.readyForCompletion,
      warnings: result.warnings,
    });
  } catch (error) {
    log.error('Preparation failed', { error });
    result.error = error instanceof Error ? error.message : 'Unknown error';
    result.success = false;
  }

  return result;
}

/**
 * Standalone validation result - no task info required
 */
export interface StandaloneValidationResult {
  success: boolean;
  readyForReview: boolean;
  validation: ValidationResult;
  git: GitStatus;
  warnings: string[];
  error?: string;
}

/**
 * Run validation checks without requiring an active task
 * Use this for standalone code review outside the spec workflow
 */
export async function runStandaloneValidation(
  projectRoot: string = process.cwd(),
  deps: ValidationDeps = {},
): Promise<StandaloneValidationResult> {
  const result: StandaloneValidationResult = {
    success: false,
    readyForReview: false,
    validation: {},
    git: {
      hasUncommittedChanges: false,
      modifiedFiles: [],
      wipCommitCount: 0,
      currentBranch: '',
      isTaskBranch: false,
    },
    warnings: [],
  };

  const log = deps.logger || logger;

  try {
    // Get git status (no task ID needed)
    result.git = getGitStatus(projectRoot, undefined, deps);

    // Run validation checks
    log.info('Starting standalone validation checks');
    const coreResult = runCoreValidationChecks(projectRoot, deps);
    result.validation = coreResult.validation;
    result.warnings.push(...coreResult.knipWarnings);
    result.readyForReview = coreResult.allPassed;
    result.success = true;

    log.info('Standalone validation complete', {
      readyForReview: result.readyForReview,
      warnings: result.warnings,
    });
  } catch (error) {
    log.error('Standalone validation failed', { error });
    result.error = error instanceof Error ? error.message : 'Unknown error';
    result.success = false;
  }

  return result;
}
