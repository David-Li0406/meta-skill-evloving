---
name: prd-generator
description: Use this skill to create detailed Product Requirements Documents (PRDs) for task orchestration, optimized for AI agent execution.
---

# Skill body

## The Job

1. Receive a feature description from the user.
2. Ask 3-5 essential clarifying questions (with lettered options) - one set at a time.
3. **Always ask about quality gates** (what commands must pass).
4. After each answer, ask follow-up questions if needed (adaptive exploration).
5. Generate a structured PRD when you have enough context.
6. Output the PRD wrapped in `[PRD]...[/PRD]` markers for TUI parsing.

**Important:** Do NOT start implementing. Just create the PRD.

## Step 1: Clarifying Questions (Iterative)

Ask questions one set at a time. Each answer should inform your next questions. Focus on:

- **Problem/Goal:** What problem does this solve?
- **Core Functionality:** What are the key actions?
- **Scope/Boundaries:** What should it NOT do?
- **Success Criteria:** How do we know it's done?
- **Integration:** How does it fit with existing features?
- **Quality Gates:** What commands must pass for each story? (REQUIRED)

### Format Questions Like This:

```
1. What is the primary goal of this feature?
   A. Improve user onboarding experience
   B. Increase user retention
   C. Reduce support burden
   D. Other: [please specify]

2. Who is the target user?
   A. New users only
   B. Existing users only
   C. All users
   D. Admin users only
```

This lets users respond with "1A, 2C" for quick iteration.

### Quality Gates Question (REQUIRED)

Always ask about quality gates - these are project-specific:

```
What quality commands must pass for each user story?
   A. pnpm typecheck && pnpm lint
   B. npm run typecheck && npm run lint
   C. bun run typecheck && bun run lint
   D. Other: [specify your commands]

For UI stories, should we include browser verification?
   A. Yes, use dev-browser skill to verify visually
   B. No, automated tests are sufficient
```

### Adaptive Questioning

After each response, decide whether to:
- Ask follow-up questions (if answers reveal complexity).
- Ask about a new aspect (if current area is clear).
- Generate the PRD (if you have enough context).

Typically 2-4 rounds of questioning are expected before generating the PRD.