import { execSync } from 'node:child_process';
import {
  appendFileSync,
  copyFileSync,
  existsSync,
  mkdirSync,
  readdirSync,
  readFileSync,
  unlinkSync,
  writeFileSync,
} from 'node:fs';
import * as path from 'node:path';
import process from 'node:process';
import { ClaudeMdHelpers, getActiveTaskId } from '../lib/claude-md';
import { ClaudeSDK } from '../lib/claude-sdk';
import { getConfig, getGitHubConfig, isCodeReviewEnabled, isGitHubIntegrationEnabled } from '../lib/config';
import { getCurrentBranch, getDefaultBranch, getMergeBase, isWipCommit } from '../lib/git-helpers';
import { GitHubHelpers, pushCurrentBranch } from '../lib/github-helpers';
import { ClaudeLogParser } from '../lib/log-parser';
import { createLogger } from '../lib/logger';
import { runValidationChecks } from '../lib/validation';

export interface ConsoleLike {
  log: (...args: unknown[]) => void;
  error: (...args: unknown[]) => void;
  warn: (...args: unknown[]) => void;
}

export interface ProcessLike {
  cwd: () => string;
  env: NodeJS.ProcessEnv;
  getExitCode: () => number | undefined;
  setExitCode: (code: number) => void;
}

export interface FileSystemLike {
  existsSync: typeof existsSync;
  readFileSync: typeof readFileSync;
  writeFileSync: typeof writeFileSync;
  appendFileSync: typeof appendFileSync;
  mkdirSync: typeof mkdirSync;
  readdirSync: typeof readdirSync;
  unlinkSync: typeof unlinkSync;
  copyFileSync: typeof copyFileSync;
}

export interface ChildProcessLike {
  execSync: typeof execSync;
}

export interface TimeProvider {
  now: () => Date;
  todayISO: () => string;
}

export type LoggerFactory = (scope: string) => ReturnType<typeof createLogger>;

export interface GitHelperBindings {
  getCurrentBranch: typeof getCurrentBranch;
  getDefaultBranch: typeof getDefaultBranch;
  getMergeBase: typeof getMergeBase;
  isWipCommit: typeof isWipCommit;
}

export interface GitHubBindings {
  createHelpers: (exec?: ConstructorParameters<typeof GitHubHelpers>[0]) => GitHubHelpers;
  pushCurrentBranch: typeof pushCurrentBranch;
}

export interface ConfigBindings {
  getConfig: typeof getConfig;
  getGitHubConfig: typeof getGitHubConfig;
  isGitHubIntegrationEnabled: typeof isGitHubIntegrationEnabled;
  isCodeReviewEnabled: typeof isCodeReviewEnabled;
}

export interface ClaudeMdBindings {
  getActiveTaskId: typeof getActiveTaskId;
  createHelpers: (fileOps?: ConstructorParameters<typeof ClaudeMdHelpers>[0]) => ClaudeMdHelpers;
}

export interface ValidationBindings {
  runValidationChecks: typeof runValidationChecks;
}

export interface LogParserBindings {
  create: (file: string) => ClaudeLogParser;
}

export interface CommandDeps {
  console: ConsoleLike;
  process: ProcessLike;
  fs: FileSystemLike;
  path: typeof path;
  childProcess: ChildProcessLike;
  time: TimeProvider;
  logger: LoggerFactory;
  git: GitHelperBindings;
  github: GitHubBindings;
  config: ConfigBindings;
  claudeMd: ClaudeMdBindings;
  validation: ValidationBindings;
  claudeSdk: typeof ClaudeSDK;
  logParser: LogParserBindings;
}

export interface PartialCommandDeps {
  console?: Partial<ConsoleLike>;
  process?: Partial<ProcessLike>;
  fs?: Partial<FileSystemLike>;
  path?: CommandDeps['path'];
  childProcess?: Partial<ChildProcessLike>;
  time?: Partial<TimeProvider>;
  git?: Partial<GitHelperBindings>;
  github?: Partial<GitHubBindings>;
  config?: Partial<ConfigBindings>;
  claudeMd?: Partial<ClaudeMdBindings>;
  validation?: Partial<ValidationBindings>;
  claudeSdk?: CommandDeps['claudeSdk'];
  logParser?: Partial<LogParserBindings>;
  logger?: CommandDeps['logger'];
}

export function createDefaultCommandDeps(): CommandDeps {
  return {
    console: {
      log: (...args: unknown[]) => console.log(...args),
      error: (...args: unknown[]) => console.error(...args),
      warn: (...args: unknown[]) => console.warn(...args),
    },
    process: {
      cwd: () => process.cwd(),
      env: process.env,
      getExitCode: () => (typeof process.exitCode === 'number' ? process.exitCode : undefined),
      setExitCode: (code: number) => {
        process.exitCode = code;
      },
    },
    fs: {
      existsSync,
      readFileSync,
      writeFileSync,
      appendFileSync,
      mkdirSync,
      readdirSync,
      unlinkSync,
      copyFileSync,
    },
    path,
    childProcess: {
      execSync,
    },
    time: {
      now: () => new Date(),
      todayISO: () => {
        const now = new Date();
        return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
      },
    },
    logger: (scope: string) => createLogger(scope),
    git: {
      getCurrentBranch,
      getDefaultBranch,
      getMergeBase,
      isWipCommit,
    },
    github: {
      createHelpers: (exec?: ConstructorParameters<typeof GitHubHelpers>[0]) => new GitHubHelpers(exec),
      pushCurrentBranch,
    },
    config: {
      getConfig,
      getGitHubConfig,
      isGitHubIntegrationEnabled,
      isCodeReviewEnabled,
    },
    claudeMd: {
      getActiveTaskId,
      createHelpers: (fileOps?: ConstructorParameters<typeof ClaudeMdHelpers>[0]) => new ClaudeMdHelpers(fileOps),
    },
    validation: {
      runValidationChecks,
    },
    claudeSdk: ClaudeSDK,
    logParser: {
      create: (file: string) => new ClaudeLogParser(file),
    },
  };
}

export function mergeCommandDeps(base: CommandDeps, overrides: PartialCommandDeps = {}): CommandDeps {
  return {
    ...base,
    ...overrides,
    console: {
      ...base.console,
      ...(overrides.console ?? {}),
    },
    process: {
      ...base.process,
      ...(overrides.process ?? {}),
    },
    fs: {
      ...base.fs,
      ...(overrides.fs ?? {}),
    },
    path: overrides.path ?? base.path,
    childProcess: {
      ...base.childProcess,
      ...(overrides.childProcess ?? {}),
    },
    time: {
      ...base.time,
      ...(overrides.time ?? {}),
    },
    git: {
      ...base.git,
      ...(overrides.git ?? {}),
    },
    github: {
      ...base.github,
      ...(overrides.github ?? {}),
    },
    config: {
      ...base.config,
      ...(overrides.config ?? {}),
    },
    claudeMd: {
      ...base.claudeMd,
      ...(overrides.claudeMd ?? {}),
    },
    validation: {
      ...base.validation,
      ...(overrides.validation ?? {}),
    },
    claudeSdk: overrides.claudeSdk ?? base.claudeSdk,
    logParser: {
      ...base.logParser,
      ...(overrides.logParser ?? {}),
    },
    logger: overrides.logger ?? base.logger,
  };
}

export function resolveCommandDeps(overrides?: PartialCommandDeps): CommandDeps {
  const base = createDefaultCommandDeps();
  if (!overrides) {
    return base;
  }
  return mergeCommandDeps(base, overrides);
}

export class CommandError extends Error {
  exitCode: number;
  details?: unknown;

  constructor(message: string, options: { exitCode?: number; cause?: unknown; details?: unknown } = {}) {
    super(message, { cause: options.cause });
    this.name = 'CommandError';
    this.exitCode = options.exitCode ?? 1;
    this.details = options.details;
  }
}

export interface CommandSuccess<T = unknown> {
  success: true;
  exitCode?: number;
  messages?: string[];
  warnings?: string[];
  data?: T;
}

export interface CommandFailure<T = unknown> {
  success: false;
  exitCode?: number;
  error: string;
  messages?: string[];
  warnings?: string[];
  details?: unknown;
  data?: T;
}

export type CommandResult<T = unknown> = CommandSuccess<T> | CommandFailure<T>;

export function isCommandSuccess<T>(result: CommandResult<T>): result is CommandSuccess<T> {
  return result.success;
}

export function applyCommandResult<T>(result: CommandResult<T>, deps: CommandDeps): void {
  const { console: cons, process: proc } = deps;

  const messages = result.messages ?? [];
  for (const message of messages) {
    cons.log(message);
  }

  const warnings = result.warnings ?? [];
  for (const warning of warnings) {
    cons.warn(warning);
  }

  if (result.success) {
    if (result.exitCode !== undefined) {
      proc.setExitCode(result.exitCode);
    }
    return;
  }

  cons.error(result.error);
  if (result.details && typeof result.details === 'string' && result.details.trim().length > 0) {
    cons.error(result.details);
  }

  if (result.exitCode !== undefined) {
    proc.setExitCode(result.exitCode);
  } else {
    proc.setExitCode(1);
  }
}

export function handleCommandException(error: unknown, deps: CommandDeps): void {
  const { console: cons, process: proc } = deps;

  if (error instanceof CommandError) {
    cons.error(error.message);
    if (error.details && typeof error.details === 'string' && error.details.trim()) {
      cons.error(error.details.trim());
    }
    proc.setExitCode(error.exitCode);
    return;
  }

  if (error instanceof Error) {
    cons.error(`Unexpected error: ${error.message}`);
  } else {
    cons.error('Unexpected error');
  }

  proc.setExitCode(1);
}
