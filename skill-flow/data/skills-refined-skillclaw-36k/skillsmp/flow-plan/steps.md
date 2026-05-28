# Flow Plan Steps

**IMPORTANT**: Steps 1-3 (research, gap analysis, depth) ALWAYS run regardless of input type.
The Beads alternative in Step 4 is only about OUTPUT format, not skipping research.

## Success criteria

- Plan references existing files/patterns with line refs
- Reuse points are explicit (centralized code called out)
- Acceptance checks are testable
- Open questions are listed

## Step 1: Fast research (parallel)

**If input is a Beads ID**: First fetch it with `bd show <id>` to get the request context.

**Based on user's choice in SKILL.md setup:**

**If user chose context-scout (RepoPrompt)**:
Run these subagents in parallel using the Task tool:
- Task flow:context-scout(<request>) - uses RepoPrompt builder for AI-powered file discovery
- Task flow:practice-scout(<request>)
- Task flow:docs-scout(<request>)

**If user chose repo-scout (default/faster)** OR rp-cli unavailable:
Run these subagents in parallel using the Task tool:
- Task flow:repo-scout(<request>) - uses standard Grep/Glob/Read
- Task flow:practice-scout(<request>)
- Task flow:docs-scout(<request>)

Must capture:
- File paths + line refs
- Existing centralized code to reuse
- Similar patterns / prior work
- External docs links
- Project conventions (CLAUDE.md, CONTRIBUTING, etc)
- Architecture patterns and data flow (especially with context-scout)

## Step 2: Flow gap check

Run the gap analyst subagent:
- Task flow:flow-gap-analyst(<request>, research_findings)

Fold gaps + questions into the plan.

## Step 3: Pick depth

Default to short unless complexity demands more.

**SHORT** (bugs, small changes)
- Problem or goal
- Acceptance checks
- Key context

**STANDARD** (most features)
- Overview + scope
- Approach
- Risks / dependencies
- Acceptance checks
- Test notes
- References

**DEEP** (large/critical)
- Detailed phases
- Alternatives considered
- Non-functional targets
- Rollout/rollback
- Docs + metrics
- Risks + mitigations

## Step 4: Write the plan

**Route A - Input WAS a Beads ID**: Plan goes INTO that issue, no confirmation needed.

1. Update the existing issue with plan summary: `bd update <id> --body "..." --json`
2. Create child tasks under it based on complexity:
   - Simple: 1-3 tasks as children (auto-numbered `.1`, `.2`, `.3`)
   - Standard: tasks with clear acceptance criteria
   - Complex: tasks with subtasks (up to 3 levels)
   - Always include `--description="<why and what>"` for context
3. Add dependencies between tasks: `bd dep add <child> <depends-on>`
4. Output: `bd show <id> --json` - ready for `/flow:work <id>`

**Route B - Input was text AND Beads detected** (.beads/ exists, CLAUDE.md mentions it):

1. **Probe** (read-only): `bd --version` succeeds
2. **Confirm**: "Create Beads epic instead of markdown plan? [Y/n]"
3. If yes, create structure:
   - `bd create "Title" -t epic -p <priority> --description="<context>" --json`
   - Add child tasks with descriptions (auto-numbered `.1`, `.2`, `.3`)
   - Add dependencies inline: `bd create "Title" --deps blocks:<other-id> --description="<context>" --json`
4. Output: `bd show <id> --json` - user can run `/flow:work <id>` directly

**Route C - No Beads**: Create `plans/<slug>.md`
- Slug = kebab-case title
- Use clear headings, short bullets
- Put file paths + links under References
- Include code sketches only if needed, with fake filenames
- If schema changes, include a Mermaid ERD

**On Beads failure after epic/tasks created**:
- Report what was created (epic ID, any tasks)
- Offer options: (A) retry failed tasks, (B) close epic, (C) leave for manual handling
- Do not silently fall back to markdown

## Step 5: Review (if chosen at start)

If user chose "Yes" to review in SKILL.md setup question:
1. Invoke `/flow:plan-review` with the plan/Beads ID
2. If review returns "Needs Work" or "Major Rethink":
   - **Immediately fix the issues** (do NOT ask for confirmation — user already consented)
   - Re-run `/flow:plan-review`
3. Repeat until review returns "Ship"

**No human gates here** — the review-fix-review loop is fully automated.

## Step 6: Offer next step

**If Route A (existing Beads issue updated)**:
"Plan added to `<id>` with N child tasks. Start `/flow:work <id>`?"

**If Route B (new Beads epic created)**:
"Epic created: `<id>`. Start `/flow:work <id>`?"

**If Route C (markdown plan)**:
"Plan ready at `plans/<slug>.md`. Next?"
1) Start `/flow:work` with this plan
2) Create issue in tracker (GitHub/Linear/Other)
3) Refine the plan
