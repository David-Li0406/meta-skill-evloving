// ABOUTME: Script for creating spec infrastructure - git branch, spec folder, metadata, CLAUDE.md update
// ABOUTME: Used by /cc-track:specify command to set up new feature development

import type { CommandResult } from './context';

export interface SpecifyOptions {
  title: string;
}

export interface SpecifyResultData {
  taskId: string;
  featureName: string;
  branch: string;
  specDir: string;
  metadataPath: string;
  claudeMdUpdated: boolean;
  github?: {
    issue: number;
    url: string;
  };
}

export interface SpecifyDeps {
  cwd: () => string;
  fs: {
    existsSync: (path: string) => boolean;
    readFileSync: (path: string, encoding?: string) => string;
    writeFileSync: (path: string, content: string) => void;
    mkdirSync: (path: string, options?: { recursive?: boolean }) => void;
  };
  path: {
    join: (...args: string[]) => string;
  };
  time: {
    nowISO: () => string;
    todayISO: () => string;
  };
  logger: (scope: string) => {
    info: (msg: string, data?: unknown) => void;
    warn: (msg: string, data?: unknown) => void;
    error: (msg: string, data?: unknown) => void;
    debug: (msg: string, data?: unknown) => void;
  };
  specHelpers: {
    getNextTaskId: (projectRoot: string, fileOps?: unknown, readDirs?: unknown) => string;
    generateFeatureName: (title: string) => string;
    createSpecDirectory: (projectRoot: string, taskId: string, featureName: string, fileOps?: unknown) => string;
    createMetadata: (specDir: string, metadata: unknown, fileOps?: unknown) => void;
  };
  git: {
    createTaskBranch: (branchName: string, cwd: string) => void;
    getCurrentBranch: (cwd: string) => string | null;
    branchExists: (branchName: string, cwd: string) => boolean;
  };
  github: {
    createGitHubIssue: (title: string, body: string, cwd: string) => { number: number; url: string } | null;
  };
  config: {
    isGitHubIntegrationEnabled: () => boolean;
  };
}

/**
 * Run the specify script to create spec infrastructure.
 *
 * Operations performed (in order):
 * 1. Validate inputs (title required, .cc-track exists, CLAUDE.md exists)
 * 2. Generate task ID (use getNextTaskId if not provided)
 * 3. Generate feature name from title (use generateFeatureName)
 * 4. Check spec directory doesn't already exist
 * 5. Check branch doesn't already exist
 * 6. Create git branch: `{taskId}-{featureName}`
 * 7. Create spec directory
 * 8. Create .metadata.json
 * 9. Update CLAUDE.md to reference new spec
 * 10. Create GitHub issue (if enabled) - non-blocking
 * 11. Return structured result
 */
export function runSpecify(options: SpecifyOptions, deps: SpecifyDeps): CommandResult<SpecifyResultData> {
  const log = deps.logger('specify');
  const warnings: string[] = [];
  const projectRoot = deps.cwd();

  // 1. Validate inputs
  if (!options.title || options.title.trim() === '') {
    return {
      success: false,
      error: 'Title is required. Please provide a title for the specification.',
    };
  }

  const ccTrackDir = deps.path.join(projectRoot, '.cc-track');
  if (!deps.fs.existsSync(ccTrackDir)) {
    return {
      success: false,
      error: '.cc-track directory not found. Run /setup-cc-track to initialize cc-track first.',
    };
  }

  const claudeMdPath = deps.path.join(projectRoot, 'CLAUDE.md');
  if (!deps.fs.existsSync(claudeMdPath)) {
    return {
      success: false,
      error: 'CLAUDE.md not found. Run /setup-cc-track to initialize cc-track first.',
    };
  }

  // 2. Generate task ID
  const fileOps = {
    existsSync: deps.fs.existsSync,
    mkdirSync: deps.fs.mkdirSync,
    readFileSync: deps.fs.readFileSync,
    writeFileSync: deps.fs.writeFileSync,
  };

  const taskId = deps.specHelpers.getNextTaskId(projectRoot, fileOps);
  log.info('Using task ID', { taskId });

  // 3. Generate feature name
  const featureName = deps.specHelpers.generateFeatureName(options.title);
  log.info('Generated feature name', { featureName });

  // 4. Check spec directory doesn't already exist
  const specDir = deps.path.join(projectRoot, '.cc-track', 'specs', `${taskId}-${featureName}`);
  if (deps.fs.existsSync(specDir)) {
    return {
      success: false,
      error: `Spec directory already exists: ${specDir}. Delete it first to recreate.`,
    };
  }

  // 5. Check branch doesn't already exist
  const branchName = `${taskId}-${featureName}`;
  if (deps.git.branchExists(branchName, projectRoot)) {
    return {
      success: false,
      error: `Git branch already exists: ${branchName}. Delete the branch first to recreate.`,
    };
  }

  // 6. Create git branch
  try {
    deps.git.createTaskBranch(branchName, projectRoot);
    log.info('Created git branch', { branch: branchName });
  } catch (error) {
    return {
      success: false,
      error: `Failed to create git branch: ${error instanceof Error ? error.message : String(error)}`,
    };
  }

  // 7. Create spec directory
  let createdSpecDir: string;
  try {
    createdSpecDir = deps.specHelpers.createSpecDirectory(projectRoot, taskId, featureName, fileOps);
    log.info('Created spec directory', { specDir: createdSpecDir });
  } catch (error) {
    return {
      success: false,
      error: `Failed to create spec directory: ${error instanceof Error ? error.message : String(error)}`,
    };
  }

  // 10. Create GitHub issue (if enabled) - do this before metadata so we can include issue info
  let githubInfo: { issue: number; url: string } | undefined;
  if (deps.config.isGitHubIntegrationEnabled()) {
    const issueTitle = `[${taskId}] ${options.title}`;
    const issueBody = `Spec directory: \`.cc-track/specs/${taskId}-${featureName}/\`\nBranch: \`${branchName}\``;

    const result = deps.github.createGitHubIssue(issueTitle, issueBody, projectRoot);
    if (result) {
      githubInfo = { issue: result.number, url: result.url };
      log.info('Created GitHub issue', { issue: result.number, url: result.url });
    } else {
      warnings.push('Failed to create GitHub issue. Continuing without GitHub integration.');
      log.warn('GitHub issue creation failed');
    }
  }

  // 8. Create metadata
  const metadata = {
    task_id: taskId,
    feature_name: featureName,
    branch: branchName,
    status: 'specified' as const,
    started: deps.time.nowISO(),
    ...(githubInfo && { github: githubInfo }),
  };

  try {
    deps.specHelpers.createMetadata(createdSpecDir, metadata, fileOps);
    log.info('Created metadata', { metadata });
  } catch (error) {
    return {
      success: false,
      error: `Failed to create metadata: ${error instanceof Error ? error.message : String(error)}`,
    };
  }

  // 9. Update CLAUDE.md to reference new spec
  try {
    const claudeMdContent = deps.fs.readFileSync(claudeMdPath, 'utf-8');
    const pattern = /@\.cc-track\/(?:no_active_task\.md|specs\/[^/]+\/spec\.md)/;
    if (!pattern.test(claudeMdContent)) {
      return {
        success: false,
        error:
          'CLAUDE.md does not contain expected Active Task reference. Expected @.cc-track/no_active_task.md or @.cc-track/specs/.../spec.md',
      };
    }
    const updatedContent = claudeMdContent.replace(pattern, `@.cc-track/specs/${taskId}-${featureName}/spec.md`);
    deps.fs.writeFileSync(claudeMdPath, updatedContent);
    log.info('Updated CLAUDE.md with active spec reference');
  } catch (error) {
    return {
      success: false,
      error: `Failed to update CLAUDE.md: ${error instanceof Error ? error.message : String(error)}`,
    };
  }

  // 11. Return structured result
  const resultData: SpecifyResultData = {
    taskId,
    featureName,
    branch: branchName,
    specDir: createdSpecDir,
    metadataPath: deps.path.join(createdSpecDir, '.metadata.json'),
    claudeMdUpdated: true,
    ...(githubInfo && { github: githubInfo }),
  };

  return {
    success: true,
    messages: [
      `✅ Spec infrastructure created for: ${options.title}`,
      `   Task ID: ${taskId}`,
      `   Branch: ${branchName}`,
      `   Spec directory: ${createdSpecDir}`,
      ...(githubInfo ? [`   GitHub issue: ${githubInfo.url}`] : []),
    ],
    warnings: warnings.length > 0 ? warnings : undefined,
    data: resultData,
  };
}

// CLI entrypoint
if (import.meta.main) {
  const title = process.argv[2];

  if (!title) {
    console.error('Usage: bun specify.ts "<title>"');
    console.error('Example: bun specify.ts "Add user authentication"');
    process.exit(1);
  }

  // Dynamic imports for CLI execution
  Promise.all([
    import('node:path'),
    import('node:fs'),
    import('../lib/spec-helpers'),
    import('../lib/git-helpers'),
    import('../lib/github-helpers'),
    import('../lib/config'),
    import('../lib/logger'),
  ]).then(
    ([
      path,
      { existsSync, readFileSync, writeFileSync, mkdirSync },
      { getNextTaskId, generateFeatureName, createSpecDirectory, createMetadata },
      { GitHelpers },
      { GitHubHelpers },
      { isGitHubIntegrationEnabled },
      { createLogger },
    ]) => {
      const gitHelpers = new GitHelpers();
      const githubHelpers = new GitHubHelpers();
      const logger = createLogger('specify');

      const deps: SpecifyDeps = {
        cwd: () => process.cwd(),
        fs: { existsSync, readFileSync, writeFileSync, mkdirSync },
        path: { join: path.join },
        time: {
          nowISO: () => new Date().toISOString(),
          todayISO: () => {
            const now = new Date();
            return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
          },
        },
        logger: () => logger,
        specHelpers: {
          getNextTaskId,
          generateFeatureName,
          createSpecDirectory,
          createMetadata,
        },
        git: {
          createTaskBranch: (branchName: string, cwd: string) => gitHelpers.createTaskBranch(branchName, cwd),
          getCurrentBranch: (cwd: string) => gitHelpers.getCurrentBranch(cwd),
          branchExists: (branchName: string, cwd: string) => gitHelpers.branchExists(branchName, cwd),
        },
        github: {
          createGitHubIssue: (title: string, body: string, cwd: string) =>
            githubHelpers.createGitHubIssue(title, body, cwd),
        },
        config: {
          isGitHubIntegrationEnabled,
        },
      };

      const options: SpecifyOptions = { title };
      const result = runSpecify(options, deps);

      // Output JSON for parsing by the command
      console.log(JSON.stringify(result, null, 2));

      if (!result.success) {
        process.exit(1);
      }
    },
  );
}
