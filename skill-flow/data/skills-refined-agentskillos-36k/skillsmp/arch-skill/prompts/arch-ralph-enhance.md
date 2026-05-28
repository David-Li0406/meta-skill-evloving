---
description: "Ralph enhance pass: re-review SPEC_PATH + existing @fix_plan.md/@AGENT.md and make tasks more granular + complete (PROMPT.md is template-owned)."
argument-hint: "<Optional. Slang ok. Include docs/<...>.md or specs/<...>.md to pin DOC_PATH.>"
---
# /prompts:arch-ralph-enhance — $ARGUMENTS
Execution rule: ignore unrelated dirty git files; if committing, stage only what you touched.
Do not preface with a plan. Begin work immediately.

Hard gate (Ralph bootstrap must already exist; do NOT create these files):
- Ralph is “set up” iff BOTH exist at repo root:
  - `PROMPT.md`
  - `@fix_plan.md`
- If either is missing: STOP immediately and print ONLY:
  - `ERROR: Ralph is not set up in this repo (expected PROMPT.md + @fix_plan.md at repo root). Run Ralph setup/bootstrap first, then rerun /prompts:arch-ralph-enhance.`

Hard gate (repo AGENTS.md must exist):
- You MUST have `AGENTS.md` at repo root.
- If it is missing: STOP immediately and print ONLY:
  - `ERROR: Repo is missing AGENTS.md at repo root; cannot set @AGENT.md. Add/restore AGENTS.md, then rerun /prompts:arch-ralph-enhance.`

Core rule (UPDATE ONLY; PROMPT.md is template-owned):
- You MUST UPDATE the existing Ralph files in-place.
- Do NOT replace them with templates (this is not initial setup).
- Do NOT rewrite them “from scratch”.
- Do NOT edit `PROMPT.md` (treat it as template-owned / read-only).
- Preserve existing structure/formatting; make minimal, surgical edits to the specific parts described below.
- If an expected anchor section is missing and you can’t safely patch it, STOP and report what anchor is missing (do not invent a new file format).

Goal:
Do a “second pass” on an existing Ralph setup:
- Re-read the plan/spec doc (DOC_PATH) and the current Ralph control files.
- Make the Ralph loop more effective: tasks are smaller, more explicit, more idiomatic, and more complete.
- Find what’s missing (coverage gaps, call sites, cleanup/deletes, invariants, checks).
- Ensure the plan won’t get stuck on manual QA / screenshot proof burdens.

This prompt edits ONLY:
- `@fix_plan.md`
- `@AGENT.md` (set to exact copy of `AGENTS.md`)
- a copied spec file in `specs/` (see SPEC_PATH below)
DO NOT modify product code. You may read code/search to ground file anchors and call-site completeness.

Git policy (required; commit only Ralph+spec files):
- After you update the Ralph control files and create/update `SPEC_PATH`, you MUST create a git commit that includes ONLY:
  - `@fix_plan.md`
  - `@AGENT.md` (only if it exists AND was modified)
  - `SPEC_PATH` (the spec copy in `specs/`)
- Ignore all other dirty/untracked files in the repo, even if present.
- Do NOT stage or commit archive directories or Ralph loop state files (`.call_count`, `status.json`, etc).
- Use explicit `git add <file>` per file; never `git add .` / `git add -A`.
- If there are no changes to those files (nothing to commit), skip the commit.

$ARGUMENTS is freeform steering. Treat it as intent + constraints + random thoughts.

DOC_PATH:
- If $ARGUMENTS includes a `docs/<...>.md` or `specs/<...>.md` path, use it.
- Else, if `@fix_plan.md` already contains a “Spec (SSOT)” reference, use that.
- Else infer from conversation/repo.
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

Ground truth policy (inescapable; repeat it everywhere it matters):
- Before rewriting tasks, identify the “ground truth set” for this effort:
  - Spec SSOT: `SPEC_PATH`
  - Source doc (copied into specs): `DOC_PATH` (only if different from SPEC_PATH)
  - Any additional docs referenced by SPEC_PATH that constrain behavior (list the exact doc paths)
  - Code anchors (entry points / primitives / central SSOT implementation) with file paths
  - If parity work: upstream reference file(s) (e.g., RN tokens, canonical implementations) with file paths
- Patch the Ralph files so the loop can’t drift:
  - Do NOT modify `PROMPT.md` for ground-truth links (it is template-owned).
  - Do NOT add extra sections to `@AGENT.md` (it must remain an exact copy of `AGENTS.md`).
  - In `@fix_plan.md`: the `Spec (SSOT)` line must reference `SPEC_PATH`, and each `## Phase N (...)` should mention the relevant spec anchor once (e.g., `Spec anchor: SPEC_PATH — <section name>`). Each `###` subsection should include at least one code anchor path.
- Any question you ask must include the exact spec/code anchor that makes it ambiguous, plus your default recommendation.

Question policy (strict: no cryptic questions):

- You MUST answer anything discoverable from code/tests/fixtures/logs or by running repo tooling; do not ask me.
- Allowed questions only:
  - Product/UX decisions not encoded in repo/docs
  - External constraints not in repo/docs (policies, launch dates, KPIs, access)
  - Doc-path ambiguity (top 2-3 candidates)
  - Missing access/permissions
- If you think you need to ask, first state where you looked; ask only after exhausting repo evidence.


# COMMUNICATING WITH AMIR (IMPORTANT)

- Start console output with a 1 line reminder of our North Star.
- Then give the punch line in plain English.
- Then give me bulleted data (3-10 bullets). If I want more data, I'll ask.
- Never be pedantic. Assume shorthand is intentional (long day); optimize for the real goal.
- Put deep details (commands, logs, exhaustive lists) in DOC_PATH / WORKLOG_PATH, not in console output.

Manual QA / screenshots policy (non-blocking; no harness):
- Do NOT require screenshots/recordings/harnesses to declare code-complete.
- Manual QA can be listed as a human follow-up, but MUST NOT block EXIT_SIGNAL.
- In `@fix_plan.md`: manual QA must NOT appear as checkboxes. Put manual QA in a non-blocking follow-ups section using plain bullets (no `[ ]`).

What “good” looks like (second-pass criteria)
You are upgrading the Ralph files so they meet these standards (be explicit; do NOT leave vague big phase checkboxes behind):

1) Granularity (loop-sized)
- Each checkbox task is small enough to complete in a single Ralph loop.
- Each task has one responsibility and is anchored to code (file paths + symbols where possible).
- Avoid monster tasks (“implement X”). Split into tasks like: add API, add decoder, wire call site, delete old path, run check.

2) Completeness (coverage)
- Every plan phase has coverage in the fix plan.
- Call sites are explicitly audited (tasks include “find all call sites” + “migrate each call site” + “delete old path”).
- Drift-proofing exists (central SSOT pattern; no parallel paths; deletes/cleanup explicitly listed).

3) Idiomatic + enforceable
- Tasks drive the most idiomatic architecture by repo standards (not just “make it work”).
- Invariants must be stated in `SPEC_PATH` and reinforced via `@AGENT.md` / `@fix_plan.md` so the loop fails loudly when violated (tests/checks, typecheck, lint, build).

4) Execution clarity
- Phase references must be human-readable: never “Phase 2” with no meaning.
  - Always: `Phase N (<short descriptor so a human remembers what it is>)`

GOOD vs BAD (be concrete; include examples in the fix plan when you rewrite tasks)

GOOD attributes:
- One checkbox = one loop-sized, finishable change.
- File-anchored tasks (paths + symbols) so the loop never needs to ask “what do you want to do?”
- Prefer this decomposition when a checkbox is too big:
  - **introduce SSOT → migrate one bounded slice → migrate remaining call sites → delete old path → run a check**
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
- Manual QA is bullets in a non-blocking section, not checkboxes.
- Avoid “High/Medium/Low priority” buckets; convert to dependency-ordered phases.

BAD smells (must be eliminated in this enhance pass):
- One checkbox that bundles multiple unrelated changes.
- “Update call sites” with no call-site list or sweep task.
- “Align parity” tasks with no SSOT/migration/delete decomposition.
- “Performance optimization” / “extended feature set” filler tasks.
- Any screenshot/video/harness requirements that would block completion.

Concrete example: rewrite “big phase checkboxes” into loop-sized tasks (this is the style you should write into `@fix_plan.md`)

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

DO THIS WORK (read → diagnose gaps → patch Ralph files)

A) Read + diagnose
1) Read `SPEC_PATH` fully (treat as authoritative SSOT).
2) Read `PROMPT.md` (read-only), `@fix_plan.md`, and `AGENTS.md` (repo-authoritative).
3) Identify problems to fix, with evidence anchors:
   - Tasks too big / vague
   - Missing call sites / missing cleanup/deletes
   - Phases unnamed/unclear (e.g., “Phase 2” with no descriptor)
   - Manual QA incorrectly blocking completion (checkboxes or “must screenshot”)
   - Checks missing (typecheck/lint/tests/build) where they would prevent churn

B) Update `@fix_plan.md` (in-place; preserve style; refine and expand tasks)
Rules:
- Prefer adding specificity over adding more tasks; split only when a task cannot be done in one loop.
- Keep tasks ordered by dependency and plan phase order (no skipping).
- Explicitly add call-site audit tasks when the plan implies migrations.
- Explicitly add delete/cleanup tasks where the plan demands “no parallel path”.
- Insert small “quality backpressure” tasks at the right time (typecheck/lint/tests/build), but keep them incremental.

Checklist for each phase group you touch:
- Phase header includes descriptor: `Phase N (<descriptor>)`
- Tasks list contains:
  - <create/adjust primitive or SSOT>
  - <migrate one bounded slice / one set of call sites>
  - <delete old path / cleanup>
  - <run a relevant check>

Manual QA placement:
- Add/maintain a `Manual QA (HITL, non-blocking)` section using bullets only.
- Manual QA bullets can reference “Amir run” or “human check later” without blocking.

C) Ensure `@AGENT.md` matches repo rules (copy-only)
- Set `@AGENT.md` to an exact copy of `AGENTS.md` (overwrite; do not append extra sections).
- Do not synthesize or extend.

Stop conditions:
- If DOC_PATH is ambiguous: ask user to choose.
- If required anchors in @fix_plan.md are missing and you can’t patch safely: stop and report what’s missing.
- Otherwise do not ask questions.

OUTPUT FORMAT (console only; Amir-style):
<1 line north star reminder>
<1 line punchline>
- Done: <what you did / what changed>
- Issues/Risks: <none|what matters>
- Next: <next action>
- Need from Amir: <only if required>
- Pointers: <DOC_PATH/WORKLOG_PATH/other artifacts>
