# Prompt Templates

Structured prompts for copilot swarm and codex.

## copilot: Analysis Prompts

### Priority Analysis

```xml
<role>Work prioritization analyst for a Convex project.</role>

<context>
Repository: {{repo}}
Team: {{team}}
Linear issues: {{linear_issues_json}}
TODOs found: {{todos_text}}
Git status: {{git_status}}
Recent commits: {{recent_commits}}
</context>

<task>
Analyze the work queue and prioritize by:
1. Explicit priority (P1 > P2 > P3)
2. Dependencies (unblocking work first)
3. Momentum (continue hot areas)
4. Effort (quick wins early)
</task>

<output_contract>
Respond with ONLY this JSON:
{
  "priority_order": ["ARB-45", "todo-auth-42", "ARB-52"],
  "rationale": "ARB-45 is P1 and unblocks notifications. todo-auth-42 is quick win in hot area. ARB-52 is P2 but larger scope.",
  "deferred": ["branch-stale-experiment"],
  "deferred_reason": "Stale experiment branch, needs triage"
}
</output_contract>
```

### Pattern Extraction

```xml
<role>Code quality analyst learning from git history.</role>

<context>
Commit messages (last 50):
{{commit_messages}}

Commit stats (last 20):
{{commit_stats}}

Test file changes:
{{test_changes}}
</context>

<task>
Extract quality patterns from this repository's history:
1. Testing approach (TDD? coverage expectations?)
2. Commit message style
3. Code organization patterns
4. Common file groupings
</task>

<output_contract>
Respond with ONLY this JSON:
{
  "patterns": [
    "TDD approach: tests written alongside implementation",
    "Commit prefix convention: feat/fix/refactor/test/docs",
    "Convex functions colocated with tests"
  ],
  "test_approach": "vitest + convex-test, tests in same directory as source",
  "commit_style": "feat(scope): description - imperative mood, lowercase",
  "coverage_expectation": "~85% based on recent trends"
}
</output_contract>
```

### Review Prompt

```xml
<role>Code reviewer assessing implementation quality.</role>

<context>
Task: {{task_description}}
Codex output: {{codex_response_json}}
Expected patterns: {{quality_patterns}}
Verification results: {{verification_output}}
</context>

<task>
Review the codex implementation:
1. Did verification pass? (codegen, types, tests, build)
2. Does it follow repository patterns?
3. Is the confidence justified?
4. Any concerns or improvements needed?
</task>

<output_contract>
Respond with ONLY this JSON:
{
  "approved": true,
  "issues": [],
  "suggestions": ["Consider adding edge case test for empty preferences"],
  "confidence": 9,
  "ready_to_merge": true
}
</output_contract>
```

### Group Decision Prompt

```xml
<role>Technical advisor providing perspective on approach.</role>

<context>
Decision needed: {{decision_description}}
Options:
{{options_list}}

Repository context:
{{repo_context}}
</context>

<task>
Evaluate the options and provide your perspective:
1. Technical trade-offs
2. Alignment with repository patterns
3. Risk assessment
4. Recommendation
</task>

<output_contract>
Respond with ONLY this JSON:
{
  "recommendation": "Option A",
  "confidence": 8,
  "reasoning": "Option A aligns with existing patterns and has lower risk",
  "trade_offs": {
    "Option A": {"pros": ["familiar pattern"], "cons": ["more boilerplate"]},
    "Option B": {"pros": ["less code"], "cons": ["new dependency"]}
  },
  "risks": ["Option B dependency may have breaking changes"]
}
</output_contract>
```

## copilot: Synthesis Prompt

```xml
<role>Technical synthesizer combining multiple analyses.</role>

<context>
Priority analysis:
{{priority_json}}

Pattern extraction:
{{patterns_json}}

Additional context:
{{additional_context}}
</context>

<task>
Synthesize analyses into a work plan with codex-ready context:
1. Order tasks by priority
2. Include relevant patterns for each task
3. Build context string for codex prompts
</task>

<output_contract>
Respond with ONLY this JSON:
{
  "tasks": [
    {
      "id": "ARB-45",
      "title": "Add notification preferences",
      "priority": 1,
      "approach": "Create Convex mutation updateNotificationPrefs, add React hook useNotificationPrefs, write tests first",
      "estimated_effort": "medium",
      "relevant_patterns": ["TDD", "hooks in packages/web/src/hooks/"]
    }
  ],
  "codex_context": "This repo uses TDD with vitest + convex-test. Tests colocated with source. Commit style: feat(scope): description. Recent work focused on convex/ and hooks/. Coverage target ~85%."
}
</output_contract>
```

## codex: Implementation Prompt

The master template for codex implementation:

```xml
<role>Senior engineer implementing a feature in a Convex + React project.</role>

<context>
## Repository Patterns (learned from git history)
{{codex_context}}

## Similar Past Work
{{similar_commits}}

## Current Focus Areas
{{hot_files}}
</context>

<task>
## Issue
{{task_id}}: {{task_title}}

## Requirements
{{task_requirements}}

## Approach (pre-resolved)
{{task_approach}}

## Files Likely Involved
{{suggested_files}}
</task>

<verification>
Run these commands and ensure all pass:

```bash
npx convex codegen    # Convex schema coherence
pnpm typecheck        # TypeScript type safety
verify --format=summary  # All tests pass
pnpm build            # Production bundle builds
```

If any gate fails, fix the issue before reporting completion.
</verification>

<output_contract>
CRITICAL: After completing ALL work and verification, respond with ONLY this JSON:
{
  "mode": "delegate",
  "status": "success",
  "summary": "Implemented notification preferences with Convex mutation, React hook, and comprehensive tests. Added email/push/sms toggles with persistence. All verification gates pass.",
  "confidence": 9,
  "artifacts": [
    {
      "type": "code",
      "path": "convex/notifications.ts",
      "language": "typescript",
      "content": "// mutation and query for notification prefs"
    },
    {
      "type": "code",
      "path": "convex/notifications.test.ts",
      "language": "typescript",
      "content": "// tests for notification prefs"
    }
  ],
  "verification": {
    "codegen": "pass",
    "types": "pass",
    "tests": "pass",
    "build": "pass"
  },
  "commits": [
    {
      "hash": "abc123",
      "message": "feat(notifications): add user preference management"
    }
  ],
  "next_steps": ["Add UI components in packages/web"],
  "blockers": []
}
</output_contract>
```

## Template Variables

| Variable | Source | Example |
|----------|--------|---------|
| `{{repo}}` | `basename $(pwd)` | `arbor-xyz` |
| `{{team}}` | `.loop.json` | `ARB` |
| `{{linear_issues_json}}` | `linear issue list --json` | `[{...}]` |
| `{{todos_text}}` | `grep TODO` output | `CLAUDE.md:42:TODO: refactor` |
| `{{recent_commits}}` | `git log --oneline -50` | `abc123 feat: add auth` |
| `{{codex_context}}` | copilot synthesis | `"This repo uses TDD..."` |
| `{{task_id}}` | work item ID | `ARB-45` |
| `{{task_approach}}` | copilot plan | `"Create mutation, add hook..."` |

## Prompt Size Guidelines

| Prompt Type | Target Size | Max Size |
|-------------|-------------|----------|
| copilot quick | 500-1000 tokens | 2000 tokens |
| copilot thorough | 1000-2000 tokens | 4000 tokens |
| codex implementation | 2000-4000 tokens | 8000 tokens |

Keep prompts focused. More context isn't always better - copilot's job is to distill relevant context, not dump everything.
