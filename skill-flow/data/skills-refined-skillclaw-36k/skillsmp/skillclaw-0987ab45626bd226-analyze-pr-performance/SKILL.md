---
name: analyze-pr-performance
description: Use this skill when investigating slow PRs, identifying bottlenecks, or debugging performance issues in code reviews.
---

# Analyze PR Performance

Analyze code review pipeline performance for a specific PR.

## Usage

Run the analyze-pr-performance CLI script with the provided arguments:

```bash
npx ts-node scripts/analyze-pr-performance.cli.ts $ARGUMENTS
```

## Arguments

- `prNumber` (required): The PR number to analyze
- `orgId` (required): The organization ID

## Options

- `--days=N`: Number of days to search back (default: 7)
- `--legacy`: Also search in legacy collection (observability_logs)
- `--env=PATH`: Path to .env file (e.g., `--env=.env.prod`)

## Examples

```bash
# Analyze performance for PR #558 in production
/analyze-pr-performance 558 04bd288b-595a-4ee1-87cd-8bbbdc312b3c --env=.env.prod

# Analyze with extended date range
/analyze-pr-performance 723 97442318-9d2a-496b-a0d2-b45fb --days=14 --env=.env.prod

# Analyze with legacy logs included
/analyze-pr-performance 701 97442318-9d2a-496b-a0d2-b45fb --legacy --env=.env.prod
```

## What it analyzes

1. **Pipeline identification**: Finds the pipelineId and correlationId for the PR.
2. **Stage times**: Shows duration of each pipeline stage:
   - ValidateNewCommitsStage
   - ResolveConfigStage
   - FetchChangedFilesStage
   - PRLevelReviewStage
   - FileAnalysisStage
   - CreateFileCommentsStage
   - UpdateCommentsAndGenerateSummaryStage
   - And all other stages...
3. **LLM calls**: Details of each LLM operation:
   - Operation name (analyzeCodeWithAI, selectReviewMode, kodyRulesAnalyzeCodeWithAI, etc.)
   - Duration
   - Model used
   - Token counts (input/output)
4. **Summary metrics**:
   - Total pipeline duration
   - Total LLM calls count
   - Total tokens (input/output)
   - Slow calls count (> 60s)
   - Models used
5. **Bottlenecks**: Highlights stages and LLM calls taking > 60 seconds.
6. **Pipeline status**: Whether the pipeline completed, failed, or is unknown.

## Output

The script outputs:
- Pipeline and correlation IDs
- Organization and repository info
- Stage times table with duration and percentage of total
- LLM calls table with model, tokens, and duration
- Summary metrics
- Bottleneck list (stages and LLM calls > 60s)
- Final pipeline status

## How to Respond

- Identify the slowest stages and explain why they might be slow.