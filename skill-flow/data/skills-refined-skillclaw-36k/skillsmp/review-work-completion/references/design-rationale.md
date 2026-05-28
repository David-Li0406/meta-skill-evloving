# Design Rationale

Settled decisions. Do not suggest changes to these patterns during reviews.

## Agent Abstraction (Alice/Bob/Carl)

Human names decouple workflow from tool names. Tools change; review process doesn't. Enables swapping implementations without rewriting skill. Names make logs readable.

## Task Agent Wrapping + Temp Files

Required for context isolation. Direct invocation would pollute context. The indirection is the feature, not overhead.

## Skill Dependencies (use-codex, use-gemini)

Intentionally reusable. These skills are shared across multiple workflows (e.g., `work` skill). DRY principle — don't inline what's already abstracted.

## Review Dimensions Checklist

Not generic — experience-driven. LLMs consistently miss these items without explicit prompting. The checklist exists because failures happened without it.

## Strict Output Format

LLMs must follow format instructions. If they can't, that's a model problem, not a skill problem. Structured output enables reliable parsing and consolidation.

## Branch Detection Logic

Explicit script handles edge cases that prose instructions miss. "Diff against main" fails when main doesn't exist, remote isn't configured, or branch naming varies.

## `.local/` Directory Structure

Prerequisite, not assumption. This skill operates within a defined workflow that guarantees the structure exists. Not meant for arbitrary projects.

## Optional Skill Invocations (catchup)

Failsafe pattern. Graceful degradation if unavailable. Minimal impact on core workflow.

## This File (design-rationale.md)

Exists to prevent repeated reviewer feedback on settled design decisions. Skill-creator guidelines discourage auxiliary files, but this file pays for itself by short-circuiting review cycles. The callout in SKILL.md directs skill reviewers here before suggesting changes.

## Dependency Discovery via Prerequisites

Dependencies (use-codex, use-gemini, catchup) are validated at runtime in step 1, not listed separately. Duplicating dependency info would create maintenance burden. Step 1's prerequisite checks ARE the dependency documentation — executable and always accurate.

## Cross-Reference Pattern (Single Source of Truth)

Multiple files reference output-formats.md rather than inlining formats. This creates indirection but ensures consistency. The alternative — inlining formats at point-of-use — caused drift in earlier iterations. One authoritative location beats convenient but divergent copies.

## Hardcoded Skill Dependency Paths

Paths like `~/.claude/skills/use-codex/scripts/codex-run.sh` are intentionally hardcoded. This skill operates within a defined ecosystem where these paths are guaranteed. Dynamic resolution would add complexity without benefit.

## Separate review-dimensions.md

Kept separate despite being always-loaded. The checklist will grow as new review blind spots are discovered. Separation makes iterating on dimensions independent of workflow changes.
