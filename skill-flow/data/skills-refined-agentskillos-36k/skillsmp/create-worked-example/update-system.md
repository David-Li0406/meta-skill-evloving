# Update Worked Example System

Use this when making changes to the worked example creation system itself (prompts, templates, architecture) - NOT when creating a new worked example deck.

---

## ⛔ STOP AND READ THESE FILES

**You MUST read all four files below using the Read tool BEFORE doing anything else.**

```
Read: .claude/skills/create-worked-example-sg/skill.md
Read: src/app/scm/workedExamples/create/README.md
Read: src/app/scm/workedExamples/create/lib/types.ts
Read: src/app/scm/workedExamples/create/lib/prompts.ts
```

**⛔ Do NOT continue past this point until you have read all four files.**

---

## System Overview

The worked example system has TWO parallel implementations:

| System | Location | Updates |
|--------|----------|---------|
| **CLI Skill** | `.claude/skills/create-worked-example-sg/` | Edit files directly |
| **Browser Wizard** | `src/app/scm/workedExamples/create/` | Manual updates required |

**Changes often need to be made in BOTH places.**

---

## STEP 2: Identify What Needs Updating

| Change Type | CLI Skill File | Browser File |
|-------------|----------------|--------------|
| Analysis instructions | `phases/01-collect-and-analyze/analyze-problem.md` | `lib/prompts.ts` (ANALYZE_PROBLEM_SYSTEM_PROMPT) |
| JSON output schema | `phases/01-collect-and-analyze/analyze-problem.md` | `lib/prompts.ts` + `lib/types.ts` |
| Slide generation | `phases/03-generate-slides/01-slide-by-slide.md` | `lib/prompts.ts` (buildGenerateSlidesPrompt) |
| New data fields | `phases/*.md` | `lib/types.ts` + `lib/prompts.ts` |
| UI display | N/A | `components/*.tsx` |
| State management | N/A | `lib/types.ts` + `hooks/useWizardState.ts` |

---

## STEP 3: Make Changes

### For CLI Skill Changes:
1. Edit the relevant file in `.claude/skills/create-worked-example-sg/`
2. Run `npm run sync-skill-content` to propagate to TypeScript module

### For Browser Wizard Changes:
1. Edit `lib/types.ts` if adding new data fields
2. Edit `lib/prompts.ts` if changing what Claude receives
3. Edit `components/*.tsx` if changing UI
4. Edit `hooks/useWizardState.ts` if adding new state/actions

---

## STEP 4: Sync (if CLI skill files changed)

```bash
npm run sync-skill-content
```

This syncs:
- `card-patterns/*.html` → `src/skills/worked-example/content/templates.ts`
- `reference/*.md` → `src/skills/worked-example/content/*.ts`

This does NOT sync:
- `src/app/scm/workedExamples/create/*` (browser wizard - manual only)

---

## Update Checklist

Before completing, verify:

- [ ] CLI skill files updated (if applicable)
- [ ] Browser wizard files updated (if applicable)
- [ ] Types match between CLI instructions and TypeScript interfaces
- [ ] `npm run sync-skill-content` ran (if CLI files changed)
- [ ] `npm run prebuild` passes (no TypeScript errors)

---

## Example: Adding a New Field to Scenarios

When we added `graphPlan` to each scenario:

**1. CLI Skill (source of truth for instructions):**
```
Edit: phases/01-collect-and-analyze/analyze-problem.md  → Add graphPlan to scenario creation
Edit: phases/02-confirm-and-plan/index.md               → Include graphPlan in output template
Edit: phases/03-generate-slides/01-slide-by-slide.md    → Which graphPlan to use for which slides
```

**2. Browser Wizard (manual sync):**
```
Edit: lib/types.ts              → Add `graphPlan?: GraphPlan` to Scenario interface
Edit: lib/prompts.ts            → Update buildGenerateSlidesPrompt to use scenario graphPlans
Edit: components/Step2Analysis.tsx → Display graphPlan in scenario accordions
```

**3. Sync:**
```bash
npm run sync-skill-content
```
