/**
 * Git diff summarization utility using Claude SDK
 * Provides concise summaries of code changes for commit messages, PRs, and reviews
 */

import { createLogger } from './logger';

// Interface for dependency injection
export interface ClaudeSDKInterface {
  prompt(
    text: string,
    model: 'haiku' | 'sonnet' | 'opus',
    options?: { maxTurns?: number; allowedTools?: string[]; disallowedTools?: string[]; timeoutMs?: number },
  ): Promise<{ text: string; success: boolean; error?: string }>;
}

export interface DiffSummaryInterface {
  summarizeDiff(diff: string): Promise<string>;
  summarizeDiffs(diffs: string[]): Promise<string>;
}

const MAX_DIFF_LENGTH = 3000;
const DEFAULT_TIMEOUT_MS = 15000;

export class DiffSummary implements DiffSummaryInterface {
  private claudeSDK?: ClaudeSDKInterface;
  private logger: ReturnType<typeof createLogger>;

  constructor(claudeSDK?: ClaudeSDKInterface, logger?: ReturnType<typeof createLogger>) {
    this.claudeSDK = claudeSDK;
    this.logger = logger || createLogger('diff-summary');
  }

  private async ensureClaudeSDK(): Promise<ClaudeSDKInterface> {
    if (this.claudeSDK) return this.claudeSDK;
    const mod = await import('./claude-sdk');
    // Type assertion is safe here - we're importing our own module with known exports
    this.claudeSDK = (mod as unknown as { ClaudeSDK: ClaudeSDKInterface }).ClaudeSDK;
    return this.claudeSDK;
  }

  private truncateDiff(diff: string): string {
    if (diff.length <= MAX_DIFF_LENGTH) return diff;

    // Try to truncate at a reasonable boundary
    const truncated = diff.substring(0, MAX_DIFF_LENGTH);
    const lastNewline = truncated.lastIndexOf('\n');
    if (lastNewline > MAX_DIFF_LENGTH * 0.8) {
      return `${truncated.substring(0, lastNewline)}\n... (diff truncated)`;
    }
    return `${truncated}\n... (diff truncated)`;
  }

  private buildSingleDiffPrompt(diff: string): string {
    return `You are a git diff summarizer. Your ONLY job is to summarize code changes.
DO NOT mention any tools, commands, or actions you might take.
DO NOT say what you will do - just provide the summary directly.

Summarize this git diff in 2-3 concise bullet points. Focus on WHAT changed, not HOW.
Ignore formatting, whitespace, and minor refactoring. Group related changes together.

${this.truncateDiff(diff)}

Respond with ONLY bullet points (use • character), no headers or explanations. Keep total under 300 characters.`;
  }

  private buildMultipleDiffPrompt(diffs: string[]): string {
    const truncatedDiffs = diffs.map((diff, i) => `=== Diff ${i + 1} ===\n${this.truncateDiff(diff)}`).join('\n\n');

    return `You are a git diff summarizer. Your ONLY job is to summarize code changes.
DO NOT mention any tools, commands, or actions you might take.
DO NOT say what you will do - just provide the summary directly.

Summarize these ${diffs.length} git diffs. Create a unified summary that groups related changes.
Focus on user-visible functionality and significant technical changes.

${truncatedDiffs}

Respond with a single paragraph summary (max 500 chars) that captures the overall changes across all diffs.
Be specific about what was added/fixed/improved but stay concise. Do not mention using any tools or what you're going to do.`;
  }

  async summarizeDiff(diff: string): Promise<string> {
    if (!diff || diff.trim().length === 0) {
      this.logger.debug('Empty diff provided, returning default message');
      return '• No changes detected';
    }

    try {
      this.logger.debug('Summarizing single diff', { diffLength: diff.length });

      const sdk = await this.ensureClaudeSDK();
      const prompt = this.buildSingleDiffPrompt(diff);

      const response = await sdk.prompt(prompt, 'haiku', {
        timeoutMs: DEFAULT_TIMEOUT_MS,
        disallowedTools: ['*'],
      });

      if (!response.success) {
        this.logger.error('Failed to summarize diff', { error: response.error });
        throw new Error(`Diff summary failed: ${response.error || 'Unknown error'}`);
      }

      const summary = response.text.trim();
      this.logger.debug('Diff summary generated', { summaryLength: summary.length });

      return summary || '• Changes made to the codebase';
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      this.logger.error('Error summarizing diff', { error: errorMsg });
      throw new Error(`Failed to summarize diff: ${errorMsg}`);
    }
  }

  async summarizeDiffs(diffs: string[]): Promise<string> {
    if (!diffs || diffs.length === 0) {
      this.logger.debug('No diffs provided, returning default message');
      return 'No changes to summarize';
    }

    // Filter out empty diffs
    const nonEmptyDiffs = diffs.filter((d) => d && d.trim().length > 0);

    if (nonEmptyDiffs.length === 0) {
      this.logger.debug('All diffs were empty, returning default message');
      return 'No substantial changes detected';
    }

    if (nonEmptyDiffs.length === 1) {
      // For single diff, use the bullet point format
      const summary = await this.summarizeDiff(nonEmptyDiffs[0]);
      // Convert bullet points to paragraph format
      return summary.replace(/^• /gm, '').replace(/\n/g, '. ').replace(/\.\./g, '.');
    }

    try {
      this.logger.debug('Summarizing multiple diffs', { count: nonEmptyDiffs.length });

      const sdk = await this.ensureClaudeSDK();
      const prompt = this.buildMultipleDiffPrompt(nonEmptyDiffs);

      const response = await sdk.prompt(prompt, 'haiku', {
        timeoutMs: DEFAULT_TIMEOUT_MS * 2, // Allow more time for multiple diffs
        disallowedTools: ['*'],
      });

      if (!response.success) {
        this.logger.error('Failed to summarize diffs', { error: response.error });
        throw new Error(`Diff summary failed: ${response.error || 'Unknown error'}`);
      }

      const summary = response.text.trim();
      this.logger.debug('Multi-diff summary generated', { summaryLength: summary.length });

      return summary || 'Multiple changes made to the codebase';
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : String(error);
      this.logger.error('Error summarizing diffs', { error: errorMsg });
      throw new Error(`Failed to summarize diffs: ${errorMsg}`);
    }
  }
}
