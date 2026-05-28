---
description: "Ralph retarget (bootstrap-safe): seed PROMPT/@fix_plan from ~/.ralph/templates, set @AGENT.md = repo AGENTS.md, copy the spec into specs/, then rewrite @fix_plan into granular phased tasks (manual QA non-blocking)."
argument-hint: "<Slang ok. Include docs/<...>.md or specs/<...>.md that is the plan/spec (SSOT).>"
---
# /prompts:arch-ralph-retarget — $ARGUMENTS
# COMMUNICATING WITH AMIR (IMPORTANT)

- Start console output with a 1 line reminder of our North Star.
- Then give the punch line in plain English.
- Then give me bulleted data (3-10 bullets). If I want more data, I'll ask.
- Never be pedantic. Assume shorthand is intentional (long day); optimize for the real goal.
- Put deep details (commands, logs, exhaustive lists) in DOC_PATH / WORKLOG_PATH, not in console output.

Execution rule: ignore unrelated dirty git files; if committing, stage only what you touched.
Do not preface with a plan. Begin work immediately.

Hard gate (Ralph templates must exist):
- You MUST have these template files present locally:
  - `~/.ralph/templates/PROMPT.md`
  - `~/.ralph/templates/fix_plan.md`
- If any are missing: STOP immediately and print ONLY:
  - `ERROR: Ralph templates are missing (expected ~/.ralph/templates/PROMPT.md + fix_plan.md). Restore/install Ralph templates, then rerun /prompts:arch-ralph-retarget.`

Hard gate (repo AGENTS.md must exist):
- You MUST have `AGENTS.md` at repo root.
- If it is missing: STOP immediately and print ONLY:
  - `ERROR: Repo is missing AGENTS.md at repo root; cannot set @AGENT.md. Add/restore AGENTS.md, then rerun /prompts:arch-ralph-retarget.`

Core rule (PROMPT.md is template-owned; customize via a small overlay patch):
- This is the “initial setup / retarget” prompt: it seeds Ralph control files from `~/.ralph/templates/` so we don’t lose critical template guidance.
- You MUST copy these templates into repo root (overwriting whatever is there; after backing up):
  - `~/.ralph/templates/PROMPT.md` → `PROMPT.md`
  - `~/.ralph/templates/fix_plan.md` → `@fix_plan.md`
- You MUST set `@AGENT.md` to the repo’s authoritative agent instructions:
  - Copy `AGENTS.md` → `@AGENT.md` (exact copy; overwrite after backup; do not append extra sections).
- After copying, you MUST make PROMPT.md project-aware WITHOUT rewriting it.
  - Allowed PROMPT.md edits are LIMITED to:
    1) Replace the placeholder `[YOUR PROJECT NAME]` project line under `## Context` (make it real).
    2) Insert/replace a single, replaceable project block under `## Context`:
       - `<!-- arch_skill:block:ralph_project_context:start -->`
       - `<!-- arch_skill:block:ralph_project_context:end -->`
    3) Remove mixed signals about batching:
       - Change any `TASKS_COMPLETED_THIS_LOOP: 2` or `: 3` examples to `: 1`.
    4) Make task selection unambiguous:
       - Patch `## Current Task` (or equivalent) to say: “pick the first unchecked checkbox in @fix_plan.md; do not reorder; exactly one checkbox per loop”.
  - Do NOT rewrite other sections of PROMPT.md.
  - Do NOT paste PROMPT.md contents into console output.

Goal:
Given a planning/spec doc (DOC_PATH), retarget the repo’s existing Ralph setup to execute that plan.
This prompt edits ONLY:
- `PROMPT.md` (seed from template, then apply the minimal overlay patch above)
- `@fix_plan.md` (copied from template, then rewritten)
- `@AGENT.md` (exact copy of `AGENTS.md`)
- a copied spec file in `specs/` (see SPEC_PATH below)
- archival backups + clearing Ralph loop state files
DO NOT modify product code.

Git policy (required; commit only Ralph+spec files):
- After you update the Ralph control files and create/update `SPEC_PATH`, you MUST create a git commit that includes ONLY:
  - `PROMPT.md`
  - `@fix_plan.md`
  - `@AGENT.md` (if modified)
  - `SPEC_PATH` (the spec copy in `specs/`)
- Ignore all other dirty/untracked files in the repo, even if present.
- Do NOT stage or commit archive directories or Ralph loop state files (`.call_count`, `status.json`, etc).
- Use explicit `git add <file>` per file; never `git add .` / `git add -A`.
- If there are no changes to those files (nothing to commit), skip the commit.

DOC_PATH:
- If $ARGUMENTS contains a `docs/<...>.md` or `specs/<...>.md` path, use it.
- Otherwise infer from conversation/repo.
- If ambiguous, ask the user to pick from the top 2–3 candidates.

SPEC_PATH (canonical SSOT; always materialize in `specs/`):
- Ralph should always reference a spec in `specs/` as SSOT (not `docs/`).
- Always ensure the SSOT doc exists at: `SPEC_PATH = specs/<DOC_BASENAME>.md`
  - Ensure `specs/` exists (create it if missing).
  - If `SPEC_PATH` does not exist: copy `DOC_PATH` → `SPEC_PATH` (exact copy; do not rewrite contents).
  - If `SPEC_PATH` exists:
    - If `DOC_PATH` and `SPEC_PATH` contents are identical: keep `SPEC_PATH` as-is.
    - If contents differ: STOP and ask which should be SSOT (show both paths + recommend creating a new uniquely named spec file in `specs/`).

From this point on:
- Treat `SPEC_PATH` as the authoritative “Spec (SSOT)” for Ralph.
- Treat `DOC_PATH` as the source doc that was copied (keep it as a reference anchor if helpful, but do not use it as SSOT).

Read SPEC_PATH and extract (as ground truth):
- TL;DR outcome
- Non-negotiables / invariants
- UX in-scope + out-of-scope
- Phase plan (depth-first phases)
- Call-site audit / migration map / delete list (if present)
- Evidence expectations, but treat manual QA as non-blocking (see policy below)

Ground truth policy (inescapable; repeat it everywhere it matters):
- Before writing tasks, identify the “ground truth set” for this plan:
  - Spec SSOT: `SPEC_PATH`
  - Source doc (copied into specs): `DOC_PATH` (only if different from SPEC_PATH)
  - Any additional docs referenced by SPEC_PATH that constrain behavior (list the exact doc paths)
  - Code anchors (entry points / primitives / central SSOT implementation) with file paths
  - If parity work: upstream reference file(s) (e.g., RN tokens, existing canonical implementations) with file paths
- When you update Ralph files, you MUST embed these references so the loop can’t drift:
  - In `PROMPT.md`: inside `<!-- arch_skill:block:ralph_project_context -->`, include:
    - `SPEC_PATH`
    - any additional docs referenced by SPEC_PATH
    - key code anchors
    - condensed non-negotiables
    - hard loop rules (one checkbox per loop)
  - Do NOT add extra sections to `@AGENT.md` (it must remain an exact copy of `AGENTS.md`).
  - In `@fix_plan.md`: the `Spec (SSOT)` line must reference `SPEC_PATH`, and each `## Phase N (...)` should mention the relevant spec anchor once (e.g., `Spec anchor: SPEC_PATH — <section name>`). Each `###` subsection should include at least one code anchor path.
- If the spec is ambiguous, link to the exact paragraph/section that is ambiguous and propose a default; do not ask a contextless question.

Manual QA / screenshots policy (non-blocking; no harness):
- Do NOT require screenshots/recordings/harnesses to declare code-complete.
- Manual QA can be listed as a human follow-up, but MUST NOT block EXIT_SIGNAL.
- In `@fix_plan.md`: manual QA must NOT appear as checkboxes that gate completion. Put manual QA in a non-blocking follow-ups section using plain bullets (no `[ ]`).

Task granularity examples (from your sandbox1/psmobile `@fix_plan.md` — follow this style):
GOOD (granular, loop-sized; one responsibility; anchored in code):
- `Add getChallenges() to apps/mobile/src/services/playVsAi/api/serviceClientCore.ts (GET /v1/challenges)`
- `Add decodeGetChallengesResponse to apps/mobile/src/services/playVsAi/api/decode.ts`
- `Wire Lobby challenge row tap → startChallengeSession(challengeId) → renders PlayVsAiJourneyScreen`
- `Refactor usePlayVsAiSession: subscribe/unsubscribe only; do not startSession() on mount`
- `Run make typecheck` (as a dedicated item after types/decoder work)

BAD (do NOT put these as checkboxes; too big or not autonomous):
- `Phase 2 — Play tab lobby (no auto-start)` ← fine as a heading/group, NOT a task checkbox
- `Implement the lobby` / `do onboarding` / `finish Phase 3` ← too vague; no file anchors; not loop-sized
- `Manual QA: entering Play tab shows Lobby; nothing starts until tap` ← belongs in non-blocking HITL follow-ups, not gating completion
- `Take screenshots / build screenshot harness` ← explicitly out; do not create proof harness busywork

Ralph task shape (be explicit; do NOT generate “big phase blocks”):

GOOD attributes (what you must produce):
- One checkbox = one loop-sized change (finishable in one Ralph cycle).
- Every checkbox is code-anchored (file path + symbol/function/route where possible).
- Prefer the canonical decomposition: **introduce SSOT → migrate one bounded slice → migrate remaining call sites → delete old path → run a check**.
- Phases are allowed, but phase headings must be human-readable:
  - Always: `Phase N (<descriptor>)` (never “Phase 2” with no meaning).
- `@fix_plan.md` MUST be structured into sections:
  - `## Phase 1 (<descriptor>)`
    - `### Phase 1.1 (<subsystem / slice>)`
      - `- [ ] <loop-sized task>`
  - Every subsection MUST have a strictly increasing phase number:
    - `Phase 1.1`, `Phase 1.2`, `Phase 1.3`, … then `Phase 2.1`, `Phase 2.2`, …
    - No `1A/1B` style subsection labels.
    - No unnumbered `###` subsections.
    - If the repo’s existing fix plan uses `####` for subsections, keep the heading depth but still use `Phase N.M (...)`.
  - Do NOT dump everything into one giant phase list; split into subsections per subsystem/slice.
  - If a subsection would exceed ~6–10 checkboxes, split it further.
- Manual QA is a non-blocking follow-up section using bullets only (no checkboxes).
- Avoid “High/Medium/Low priority” buckets; convert to phased, dependency-ordered work.

BAD smells (fix these during retarget):
- “Do X + Y + Z” in a single checkbox (multiple responsibilities).
- “Update call sites” without enumerating call sites or providing a sweep task.
- “Align parity” tasks with no decomposition into SSOT + migrations + deletes.
- “Performance optimization” / “extended feature set” style filler tasks.
- Any screenshot/video/harness requirements.

Concrete example: rewrite “priority buckets / big phase blocks” into phase sections + loop-sized tasks (this is the structure you should write into `@fix_plan.md`)

BAD structure (priority buckets + huge checkboxes; causes stalls + vague questions):
## High Priority (Phase 1 — global primitives)
- [ ] Replace StableHeader PNG icons with painter widgets + `'∞'` formatting in `apps/flutter/lib/ui/components/stable_header.dart`
- [ ] Align Flutter motion tokens to RN `apps/mobile/src/motion/tokens.ts` in `apps/flutter/lib/design_system/app_motion.dart` and update call sites using non-RN tokens

GOOD structure (phases + subsections + loop-sized tasks):
## Phase 1 (Global primitives: StableHeader + motion tokens)

### Phase 1.1 (StableHeader icons + `∞` formatting)
- [ ] Audit StableHeader icon call sites + PNG references (list paths) (Flutter)
- [ ] Add painter widget for ONE StableHeader icon in `apps/flutter/lib/ui/components/stable_header.dart` (no other changes)
- [ ] Switch that ONE icon to painter rendering in `apps/flutter/lib/ui/components/stable_header.dart`
- [ ] Add a `formatStableHeaderStreakCount()` helper and use it from `apps/flutter/lib/ui/components/stable_header.dart` (`∞` case + normal ints)
- [ ] Convert remaining StableHeader PNG icons → painter, then delete the PNG rendering path

### Phase 1.2 (Motion token parity (mirror RN → migrate → delete old path))
- [ ] Mirror RN motion tokens into `apps/flutter/lib/design_system/app_motion.dart` (SSOT mapping only; no call sites yet)
- [ ] Migrate ONE bounded call-site cluster to the mirrored tokens (e.g., StableHeader animations only)
- [ ] Migrate remaining parity-critical call sites to mirrored tokens, then delete/stop-export the old non-parity tokens

### Phase 1.3 (Checks (small + targeted))
- [ ] Run the smallest relevant check (typecheck/lint/test) and record result

Clear previous task (backup + reset previous Ralph state):
1) Create an archive directory (neat + predictable):
   - If `docs/` exists: `docs/ralph_archive/<YYYY-MM-DD_HHMMSS>/`
   - Else: `.ralph_archive/<YYYY-MM-DD_HHMMSS>/`
2) Copy the prior Ralph control files into the archive directory:
   - `PROMPT.md`
   - `@fix_plan.md`
   - `@AGENT.md` (if present)
3) Also archive these Ralph loop state files if present (repo root):
   - `.call_count`
   - `.circuit_breaker_state`
   - `.circuit_breaker_history`
   - `.exit_signals`
   - `.response_analysis`
   - `.ralph_session`
   - `.ralph_session_history`
   - `.last_reset`
   - `status.json`
   - `progress.json`
4) After backup, delete ONLY the files listed in (3) from repo root so the next loop starts clean.
   - Do NOT delete logs/ or any product files.

UPDATE RULES (use sandbox1/psmobile as the “good” reference shape)
The “good” shape you’re aiming for looks like sandbox1/psmobile:

PROMPT.md:
- MUST start from `~/.ralph/templates/PROMPT.md`, then be patched minimally:
  - Replace the placeholder `[YOUR PROJECT NAME]`.
  - Add/replace the `<!-- arch_skill:block:ralph_project_context -->` block under `## Context`.
  - Change example `TASKS_COMPLETED_THIS_LOOP` values to eliminate batching (no `2`/`3`).
  - Patch `## Current Task` selection to “pick first unchecked checkbox”.
- Do NOT rewrite the rest of the template.

@fix_plan.md:
- Begins with:
  - `# Ralph Fix Plan — <topic> (<date>)`
  - `Spec (SSOT):` referencing `SPEC_PATH` (in `specs/`)
- Uses:
  - `## Phase N (<descriptor>)`
  - `### Phase N.M (<subsystem/slice>)` (strictly increasing)
  - loop-sized `- [ ]` tasks
- Includes a top note that clarifies execution:
  - “ONE checkbox per loop” and “Do NOT mark more than one checkbox [x] per loop.”

@AGENT.md:
- MUST be an exact copy of `AGENTS.md` (repo-authoritative). Do not synthesize or extend it.

Now do the updates (in order; no skipping):

0) Backup + reset
- Perform “Clear previous task (backup + reset previous Ralph state)” exactly as written above.

1) Seed templates (overwrite; after backup)
- Copy these files into repo root:
  - `~/.ralph/templates/PROMPT.md` → `PROMPT.md`
  - `~/.ralph/templates/fix_plan.md` → `@fix_plan.md`
- After copy: patch `PROMPT.md` minimally (do NOT rewrite it).
- Copy `AGENTS.md` → `@AGENT.md` (exact copy).

2) Materialize `SPEC_PATH`
- Ensure `SPEC_PATH = specs/<DOC_BASENAME>.md` exists (copy `DOC_PATH` if needed).

3) Patch `PROMPT.md` (minimal overlay patch; template remains intact)
- Replace the placeholder project name under `## Context` so it is not `[YOUR PROJECT NAME]`.
- Insert/replace this block under `## Context`:
  - `<!-- arch_skill:block:ralph_project_context:start -->`
  - `<!-- arch_skill:block:ralph_project_context:end -->`
  - Content must include:
    - Project name (repo name is fine)
    - `Spec (SSOT): SPEC_PATH`
    - Ground truth / References list (docs + code anchors)
    - Condensed non-negotiables from SPEC_PATH
    - Hard loop rules:
      - Exactly ONE checkbox per loop (max 1 new `[x]` per response)
      - `TASKS_COMPLETED_THIS_LOOP` must be `1` when a checkbox is completed, else `0`
      - Pick the first unchecked checkbox in `@fix_plan.md` (do not reorder)
- Remove mixed-signal batching examples:
  - Change any `TASKS_COMPLETED_THIS_LOOP: 2` or `: 3` in examples/scenarios to `: 1`.
- Patch `## Current Task` (or equivalent) to match the hard selection rule:
  - Pick the first unchecked checkbox in `@fix_plan.md`; do not reorder; do not batch.

4) Confirm `@AGENT.md` correctness
- Verify `@AGENT.md` is an exact copy of `AGENTS.md` (no extra sections injected).

5) Rewrite `@fix_plan.md` (in-place; replace task content)
- Replace template priority buckets with the phase+subsection structure above.
- `Spec (SSOT)` MUST point at `SPEC_PATH` (not `DOC_PATH`).
- Ensure tasks are loop-sized + code-anchored + dependency-ordered.
- Ensure every `###` is numbered `Phase N.M (...)` and numbers only go up.
- Manual QA belongs in a `Manual QA (HITL, non-blocking)` section using bullets only.

6) Git commit (Ralph control files + spec only)
- Commit ONLY: `PROMPT.md`, `@fix_plan.md`, `@AGENT.md`, and `SPEC_PATH` (if changed).
- Ignore all other dirty/untracked files in the repo.

STOP conditions:
- If DOC_PATH is ambiguous: ask user to choose.
- If template files are missing: bail with the template error above.
- If `DOC_PATH` vs `SPEC_PATH` mismatch is detected (same name, different contents): stop and ask which is SSOT.
- Otherwise, do not ask questions.

OUTPUT FORMAT (console only; Amir-style):
<1 line north star reminder>
<1 line punchline>
- Done: <what you did / what changed>
- Issues/Risks: <none|what matters>
- Next: <next action>
- Need from Amir: <only if required>
- Pointers: <DOC_PATH/WORKLOG_PATH/other artifacts>
