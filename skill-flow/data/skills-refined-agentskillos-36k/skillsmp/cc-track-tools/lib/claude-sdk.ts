/**
 * Claude Code SDK wrapper for cc-track
 * Provides a clean interface for interacting with Claude using the TypeScript SDK
 * Uses Pro subscription authentication (no API key required)
 */

import { execSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { resolve } from 'node:path';
import { join } from 'node:path/posix';
import type {
  CanUseTool,
  PermissionResult,
  Query,
  SDKAssistantMessage,
  SDKResultMessage,
  SDKUserMessage,
} from '@anthropic-ai/claude-agent-sdk';
import { createLogger } from './logger';

export interface ClaudeResponse {
  text: string;
  success: boolean;
  error?: string;
  usage?: {
    inputTokens: number;
    outputTokens: number;
    costUSD: number;
  };
}

/**
 * Helper function to convert a string prompt into an AsyncIterable<SDKUserMessage>
 * Required when using canUseTool callback with the Claude Code SDK
 *
 * Note: session_id is set to 'temp-session' as these are single-use query sessions,
 * not persistent conversations. parent_tool_use_id is null as these are initial messages.
 */
export async function* createMessageStream(text: string): AsyncIterable<SDKUserMessage> {
  yield {
    type: 'user',
    session_id: 'temp-session',
    parent_tool_use_id: null,
    message: {
      role: 'user',
      content: [{ type: 'text', text }],
    },
  } as SDKUserMessage;
}

// Find the Claude Code executable cross-platform
export function findClaudeCodeExecutable(): string | undefined {
  // Prefer system-installed claude (often a compiled binary and faster)
  try {
    // Use 'command -v' which is POSIX standard, or 'where' on Windows
    const isWindows = process.platform === 'win32';
    const findCommand = isWindows ? 'where claude' : 'command -v claude';
    const claudePath = execSync(findCommand, { encoding: 'utf8' }).trim();

    if (claudePath) {
      // On Windows, 'where' might return multiple lines
      const paths = claudePath
        .split('\n')
        .map((p) => p.trim())
        .filter(Boolean);

      // On Unix, try to resolve symlinks for the first path
      if (!isWindows) {
        const firstPath = paths[0];
        try {
          const realPath = execSync(`readlink -f "${firstPath}"`, { encoding: 'utf8' }).trim();
          return realPath || firstPath;
        } catch {
          return firstPath;
        }
      }

      // On Windows, try each path until we find one that works
      // Skip fnm multishell paths - they exist on disk but are stale shims that fail to spawn
      // when the terminal session that created them is no longer active
      for (const path of paths) {
        // Skip fnm multishell paths - they're session-specific shims that become stale
        if (path.includes('fnm_multishells')) {
          continue;
        }
        if (existsSync(path)) {
          return path;
        }
      }
      // All non-fnm paths failed - fall through to other methods
    }
  } catch {
    // Command failed, claude is not in PATH
  }

  // Fallback to local project install
  try {
    const localCli = `${process.cwd()}/node_modules/@anthropic-ai/claude-agent-sdk/cli.js`;
    if (existsSync(localCli)) return localCli;
  } catch {}

  // If none found, return undefined and let SDK auto-detect
  return undefined;
}

async function prompt(
  text: string,
  model: 'haiku' | 'sonnet' | 'opus' = 'haiku',
  options?: {
    maxTurns?: number;
    allowedTools?: string[];
    disallowedTools?: string[];
    timeoutMs?: number;
    cwd?: string;
  },
): Promise<ClaudeResponse> {
  const logger = createLogger('claude-sdk');
  try {
    // Use generic model names - the API will use the latest versions
    const modelMap = {
      haiku: 'haiku',
      sonnet: 'sonnet',
      opus: 'opus',
    } as const;

    // Find Claude Code executable
    const pathToClaudeCodeExecutable = findClaudeCodeExecutable();

    const { query } = await import('@anthropic-ai/claude-agent-sdk');
    logger.debug('ClaudeSDK.prompt start', {
      model: modelMap[model],
      timeout_ms: options?.timeoutMs,
      pathToClaudeCodeExecutable,
    });
    // Note: we rely on stream.return() and a bounded timeout; avoid AbortController to keep types simple
    const stream = query({
      prompt: text,
      options: {
        model: modelMap[model],
        maxTurns: options?.maxTurns ?? 1,
        allowedTools: options?.allowedTools,
        disallowedTools: options?.disallowedTools ?? ['*'],
        pathToClaudeCodeExecutable,
        systemPrompt: { type: 'preset', preset: 'claude_code' },
        // Use provided cwd or default to temp directory to avoid triggering project hooks
        cwd: options?.cwd || tmpdir(),
        stderr: (data: string) => {
          try {
            const s = typeof data === 'string' ? data : String(data);
            logger.debug('Claude Code stderr', { data: s.substring(0, 500) });
          } catch {
            // ignore
          }
        },
      },
    });

    let responseText = '';
    let success = false;
    let usage: ClaudeResponse['usage'];
    let error: string | undefined;
    let timedOut = false;

    let timeout: ReturnType<typeof setTimeout> | null = null;
    if (options?.timeoutMs && options.timeoutMs > 0) {
      timeout = setTimeout(() => {
        timedOut = true;
        try {
          // Politely signal completion to underlying process
          // Type assertion is safe here as Query extends AsyncGenerator<SDKMessage, void>
          void (stream as Query).return(undefined);
        } catch {
          // ignore
        }
        // We already requested stream termination; child will exit shortly.
      }, options.timeoutMs);
    }

    try {
      for await (const message of stream) {
        if (message.type === 'assistant') {
          const assistantMsg = message as SDKAssistantMessage;
          const content = assistantMsg.message.content[0];
          if (content && 'text' in content) {
            responseText = content.text;
          }
        }

        if (message.type === 'result') {
          const resultMsg = message as SDKResultMessage;
          if (resultMsg.subtype === 'success') {
            success = true;
            usage = {
              inputTokens: resultMsg.usage.input_tokens || 0,
              outputTokens: resultMsg.usage.output_tokens || 0,
              costUSD: resultMsg.total_cost_usd,
            };
          } else if (resultMsg.subtype === 'error_max_turns' && responseText) {
            success = true;
            usage = {
              inputTokens: resultMsg.usage.input_tokens || 0,
              outputTokens: resultMsg.usage.output_tokens || 0,
              costUSD: resultMsg.total_cost_usd,
            };
          } else {
            error = `Claude returned error: ${resultMsg.subtype}`;
          }
        }
      }
    } finally {
      if (timeout) clearTimeout(timeout);
    }

    if (!success && timedOut) {
      logger.error('ClaudeSDK.prompt timeout', { timeout_ms: options?.timeoutMs });
      return {
        text: responseText.trim(),
        success: false,
        error: `timeout after ${options?.timeoutMs}ms`,
        usage,
      };
    }

    logger.debug('ClaudeSDK.prompt done', { success, usage });
    return { text: responseText.trim(), success, error, usage };
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    const logger = createLogger('claude-sdk');
    logger.error('ClaudeSDK.prompt error', { error: msg });
    return {
      text: '',
      success: false,
      error: msg,
    };
  }
}

async function generateCommitMessage(changes: string): Promise<string> {
  const p = `Generate a conventional commit message for these changes:
${changes}

Requirements:
- Use conventional commit format (feat:, fix:, docs:, chore:, etc.)
- Be concise but descriptive
- Focus on the "what" and "why", not the "how"
- Respond with JUST the commit message, no explanation`;

  const response = await prompt(p, 'haiku', { timeoutMs: 10000 });
  if (!response.success) throw new Error(`Failed to generate commit message: ${response.error}`);
  return response.text;
}

async function generateBranchName(taskTitle: string, taskId: string): Promise<string> {
  const p = `Generate a git branch name for this task:
Title: ${taskTitle}
Task ID: ${taskId}

Requirements:
- Use format: type/description-taskid (e.g., feature/add-auth-001)
- Keep it short (max 50 chars total)
- Use lowercase and hyphens only
- Types: feature, bug, chore, docs
- Respond with JUST the branch name`;

  const response = await prompt(p, 'haiku', { timeoutMs: 10000 });
  if (!response.success) throw new Error(`Failed to generate branch name: ${response.error}`);
  return response.text;
}

async function reviewCode(diff: string, requirements: string): Promise<{ hasIssues: boolean; review: string }> {
  const p = `Review these code changes against the requirements:

REQUIREMENTS:
${requirements}

CHANGES:
${diff}


You are a senior software engineer performing a code review on AI-generated changes. Be candid, precise, and action-oriented. Do not compliment, reassure, or claim "production-ready." Default to caution and evidence.

You have been provided with the task description and list of diffs. You have the ability to navigate the current codebase and review files in full as needed. You should review the current state of files, not just rely on the diffs, use the diffs to guide your review.

Note:
At the time of this review the code passes lint, typecheck, and all existing tests pass.

  Review principles:

  - Evidence over opinion. If unsure, say "Unknown—needs verification," and list how to verify.
  - Anchor every finding to file paths and lines or symbols (e.g., src/foo.ts:123,
  UserService.create()).
  - Rank by severity: P0 (blocker), P1 (serious), P2 (should fix), P3 (nit).
  - For each issue, provide: What, Why it matters, Where, Concrete Fix (patch or exact steps),
  Severity, Evidence.
  - Prefer small patch snippets for quick fixes; otherwise list exact steps.
  - No praise, no "LGTM," no "production-ready." State what would constitute sufficient evidence
  instead (tests, checks, metrics).

  AI-code failure modes to hunt:

  - Hallucinated or wrong APIs/imports; stale types/schemas; missing null/edge handling.
  - Over-broad catches, swallowed errors, disabled validation; brittle regex; unsafe deserialization.
  - Concurrency/race conditions; blocking calls in hot paths; N+1 or O(n²) patterns.
  - Secrets/keys in code or logs; PII in logs; insecure defaults; injection risks (SQL/NoSQL/LDAP/
  OS/HTML).
  - Dead code, duplicate logic, redundant wrappers; TODOs/placeholders left in.
  - Misleading comments or tests that re-implement logic instead of asserting behavior.

  Checks to perform (static reasoning is fine as you can't run code):

  - Spec alignment: map each acceptance criterion to concrete code and tests; mark Met/Partial/Unmet
  with evidence.
  - Correctness & edge cases: types, nullability, error surfacing, state/ordering, input validation.
  - Security & privacy: injection, SSRF/XSS/CSRF, path traversal, secrets handling, crypto usage,
  logging redaction.
  - Performance & scalability: complexity, memory growth, N+1s, I/O patterns, timeouts, backpressure.
  - Reliability: idempotency, retries with jitter, timeouts, resource cleanup, concurrency safety.
  - API & compatibility: contracts/schemas, versioning, migrations, deprecations, backward
  compatibility.
  - Tests: changed-code coverage, negative cases, flaky risks. Propose exact tests to add with names
  and expected assertions.
  - Observability: log levels, PII redaction, metrics, tracing.
  - Maintainability: complexity, duplication, naming, comments/docs, public surface area, file layout.
  - Dependencies: necessity, alternatives, pinning, supply-chain/licensing.

  Output format (use concise bullets, reference files/lines):

  1. Summary: 2-3 sentences on the main risks and areas touched.
  2. Verdict: Blocking | Non-blocking.
  3. Spec Alignment: numbered list of criteria with Met/Partial/Unmet + evidence.
  4. Critical Issues (P0/P1): for each, provide What/Why/Where/Fix/Evidence.
  5. Required Tests: concrete cases (test names, Arrange-Act-Assert outline; include short snippets if
  ≤15 lines).
  6. Security & Privacy: issues and required mitigations.
  7. Performance: risks and improvements with expected order-of-magnitude impact if applicable.
  8. Maintainability & Style: specific refactors or conventions to apply.
  9. Behavioral Diffs & Compatibility: any user-visible changes; migration notes if needed.
  10. Verification Plan: exact commands to run (build, lint, test, focused checks) and expected
  outcomes.
  12. Unknowns & Assumptions: call out anything you could not verify and how to de-risk it.

  Language constraints:

  - No compliments or filler. Avoid "looks good," "clean," "production-ready," "robust," etc.
  - Be specific and mechanical: short bullets, direct verbs, concrete references.
  - If a section has nothing to report, state "None found" rather than praising.

  Severity rubric:

  - P0: correctness/security breaks, build/test fails, backward-incompatible changes without
  migration.
  - P1: data loss risk, race conditions, privacy leaks, severe perf regressions.
  - P2: maintainability issues, incomplete tests, minor perf concerns.
  - P3: nits and stylistic polish.
`;

  const response = await prompt(p, 'sonnet', { timeoutMs: 60000 });
  if (!response.success) throw new Error(`Failed to review code: ${response.error}`);

  try {
    const result = JSON.parse(response.text);
    return { hasIssues: result.hasIssues || false, review: result.review || '' };
  } catch {
    return { hasIssues: false, review: response.text };
  }
}

async function extractErrorPatterns(transcript: string): Promise<string> {
  const p = `Extract error patterns and their solutions from this transcript:
${transcript}

Focus on:
- Actual errors encountered and how they were fixed
- Patterns to avoid in the future
- Successful recovery strategies

Format as markdown with clear headers. Be concise.`;

  const response = await prompt(p, 'haiku', { timeoutMs: 20000 });
  if (!response.success) return '<!-- Error pattern extraction failed -->';
  return response.text;
}

async function createValidationAgent(codebasePath: string, validationRules: string): Promise<Query> {
  const p = `You are a code validation agent. Your task is to review the codebase and identify issues.

Codebase path: ${codebasePath}
Validation rules:
${validationRules}

You can read files but cannot modify them. Provide a detailed analysis.`;

  // Find Claude Code executable
  const pathToClaudeCodeExecutable = findClaudeCodeExecutable();
  const { query } = await import('@anthropic-ai/claude-agent-sdk');
  const logger = createLogger('claude-sdk');
  logger.debug('ClaudeSDK.createValidationAgent start', { pathToClaudeCodeExecutable });
  return query({
    prompt: p,
    options: {
      model: 'claude-sonnet-4-5-20250929',
      maxTurns: 10,
      allowedTools: ['Read', 'Grep', 'Glob', 'TodoWrite'],
      pathToClaudeCodeExecutable,
      systemPrompt: { type: 'preset', preset: 'claude_code' },
      // Allow the agent to read the repository while preventing hook recursion
      cwd: tmpdir(),
      additionalDirectories: [codebasePath],
      stderr: (data: string) => {
        try {
          const s = typeof data === 'string' ? data : String(data);
          logger.debug('Claude Code stderr', { data: s.substring(0, 500) });
        } catch {
          // ignore
        }
      },
    },
  });
}

async function performCodeReview(
  taskId: string,
  taskTitle: string,
  taskRequirements: string,
  gitDiff: string,
  projectRoot: string,
): Promise<{ success: boolean; review: string; error?: string }> {
  const logger = createLogger('claude-sdk');

  const p = `You are performing a comprehensive code review for task ${taskId}.

# Task Information
- **Task ID:** ${taskId}
- **Title:** ${taskTitle}
- **Project Root:** ${projectRoot}

# Task Requirements
${taskRequirements}

# Changes to Review (Git Diff)
${gitDiff}

# Your Review Task

Perform a thorough code review analyzing:
1. **Requirements Alignment:** Do the changes fulfill all task requirements?
2. **Security:** Are there any security vulnerabilities or concerns?
3. **Code Quality:** Is the code well-structured, readable, and maintainable?
4. **Performance:** Are there any performance issues or optimizations needed?
5. **Architecture:** Does the implementation follow project patterns and conventions?
6. **Error Handling:** Is error handling comprehensive and appropriate?
7. **Testing:** Are the changes adequately tested? Are there missing test cases?
8. **Documentation:** Is the code properly documented? Are there missing explanations?

You have access to read any file in the project to understand context and patterns.
You can only write to the code-reviews/ directory.

Write your complete review to a file named: code-reviews/${taskId}_[DATE].md

Use the current UTC timestamp for [DATE] in format: YYYY-MM-DD_HHmm-UTC

Your review should be thorough, actionable, and constructive. Include specific file/line references where applicable.`;

  try {
    // Find Claude Code executable
    const pathToClaudeCodeExecutable = findClaudeCodeExecutable();
    const { query } = await import('@anthropic-ai/claude-agent-sdk');

    logger.info('Starting code review', { taskId, timeout: 600000, maxTurns: 30 });

    const stream = query({
      prompt: createMessageStream(p),
      options: {
        model: 'claude-sonnet-4-5-20250929',
        maxTurns: 30,
        allowedTools: ['Read', 'Grep', 'Glob', 'Write'],
        disallowedTools: ['*'], // Only allow the specific tools above
        pathToClaudeCodeExecutable,
        systemPrompt: { type: 'preset', preset: 'claude_code' },
        cwd: projectRoot,
        canUseTool: (async (toolName, input, _options) => {
          // Only restrict Write tool to code-reviews directory
          if (toolName === 'Write') {
            const requestedPath = (input as { file_path: string }).file_path;
            // Resolve the path relative to the project root to handle both absolute and relative paths
            // Normalize both paths to forward slashes for cross-platform comparison
            const filePath = resolve(projectRoot, requestedPath).replace(/\\/g, '/');
            const allowedDir = join(projectRoot, 'code-reviews').replace(/\\/g, '/');
            // Ensure trailing slash to prevent bypassing via sibling directories
            // (e.g., "code-reviews-hacker" would match "code-reviews" without the slash)
            const allowedDirWithSlash = allowedDir.endsWith('/') ? allowedDir : `${allowedDir}/`;

            if (!filePath.startsWith(allowedDirWithSlash)) {
              logger.warn('Blocked Write attempt outside code-reviews directory', {
                toolName,
                attemptedPath: filePath,
                requestedPath,
                allowedDir,
              });
              return {
                behavior: 'deny',
                message: `Write access is restricted to ${allowedDir}. You can only write code review files.`,
              } satisfies PermissionResult;
            }
          }

          // Allow all other configured tools
          return {
            behavior: 'allow',
            updatedInput: input,
          } satisfies PermissionResult;
        }) satisfies CanUseTool,
        stderr: (data: string) => {
          try {
            const s = typeof data === 'string' ? data : String(data);
            logger.debug('Claude Code stderr', { data: s.substring(0, 500) });
          } catch {
            // ignore
          }
        },
      },
    });

    let reviewText = '';
    let success = false;
    let error: string | undefined;
    let timedOut = false;

    // 10 minute timeout
    const timeout = setTimeout(() => {
      timedOut = true;
      try {
        // Type assertion is safe here as Query extends AsyncGenerator<SDKMessage, void>
        void (stream as Query).return(undefined);
      } catch {
        // ignore
      }
    }, 600000);

    try {
      for await (const message of stream) {
        if (message.type === 'assistant') {
          const assistantMsg = message as SDKAssistantMessage;
          const content = assistantMsg.message.content[0];
          if (content && 'text' in content) {
            reviewText = content.text;
          }
        }

        if (message.type === 'result') {
          const resultMsg = message as SDKResultMessage;
          if (resultMsg.subtype === 'success' || resultMsg.subtype === 'error_max_turns') {
            success = true;
            logger.info('Code review completed', {
              subtype: resultMsg.subtype,
              inputTokens: resultMsg.usage?.input_tokens,
              outputTokens: resultMsg.usage?.output_tokens,
              costUSD: resultMsg.total_cost_usd,
            });
          } else {
            error = `Code review failed: ${resultMsg.subtype}`;
            logger.error('Code review failed', { subtype: resultMsg.subtype });
          }
        }
      }
    } finally {
      clearTimeout(timeout);
    }

    if (timedOut) {
      logger.warn('Code review timed out after 10 minutes');
      return {
        success: false,
        review: reviewText || 'Code review timed out',
        error: 'timeout after 600000ms',
      };
    }

    return { success, review: reviewText, error };
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    logger.error('Code review error', { error: msg });
    return {
      success: false,
      review: '',
      error: msg,
    };
  }
}

export const ClaudeSDK = {
  prompt,
  generateCommitMessage,
  generateBranchName,
  reviewCode,
  extractErrorPatterns,
  createValidationAgent,
  performCodeReview,
};
