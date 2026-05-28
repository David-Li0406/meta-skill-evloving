# Agent Instructions

This project uses **bd** (beads) for issue tracking.

Record a `bd` comment/notes update for major items of work or significant changes in design/content (brief rationale + links to relevant files/PRs).

Never overwrite or delete `.beads/issues.jsonl` directly. Always use the `bd` CLI to make changes.

Never overwrite a beads descritption or comments made by other team members (human or AI). Always append new information either as a new comment or an addition to the description.

Before starting a session that will change something other than `.beads/issues.jsonl`, ensure you are on a branch named `<beads_prefix>-<id>/<short-desc>` and that it is up to date with `origin/main`. Verify `git status` is clean. If it is not clean (exception: uncommitted changes are allowed in `.beads/issues.jsonl`, carry them into the work) then pause and check with the Producer before proceeding.

## Issue Tracking with bd (beads)

**IMPORTANT**: This project uses **bd (beads)** for ALL issue tracking. Do NOT use markdown TODOs, task lists, or other tracking methods.

### Why bd?

- Dependency-aware: Track blockers and relationships between issues
- Git-friendly: Auto-syncs to JSONL for version control
- Agent-optimized: JSON output, ready work detection, discovered-from links
- Prevents duplicate tracking systems and confusion

**Bead Lifecycle Overview**

Beads maintain their stage and stage though a combination of status and labels. Status is a single value representing the current state of the bead, while labels provide additional context and categorization. To set the status of a bead, use the `--status` flag with the `bd update` command. To add or remove labels, use the `--add-label` and `--remove-label` flags respectively. 

Whenever a bead moves between stages, ensure that the appropriate stage label is added and any previous stage labels are removed to accurately reflect its current state.

Status Values:
  - open - Ready to be worked on
  - in_progress - Currently being worked on
  - blocked - Cannot proceed (waiting on dependencies)
  - deferred - Deliberately put on ice for later
  - closed - Work completed
  - tombstone - Deleted issue (suppresses resurrections)

Stage Labels:
  - stage:idea - Initial idea stage`
  - stage:prd_complete - PRD/requirements complete
  - stage:milestones_defined - Milestones (top level epics for the PRD) defined
  - stage:planned - Full implementation plan, in the form of subtasks, created   
  - stage:in_progress - Work in progress
  - stage:in_review - code complete, PR created, working on passing review/QA
  - stage:done - Completed work, PR merged

**Create new issues:**

1. Before creating a new issue ensure that all details are clear. Pause and ask the user for more information and clarifications as necessary; provide advice and guidance when possible;
2. The description should include clear acceptance criteria (definition of done), suggestions for how to implement, and any relevant context or links to related issues/PRs. It should also include a list of files/doc paths that may be created, edited, or deleted while working the issue.
3. Search the existing issues to avoid duplicates:
   ```bash
   bd search "search terms" --json
   ``` 
4. Use clear markdown formatting (in string form) in issue content; Use templates when possible (discoverable with `bd template list` and viewable with `bd template show $NAME`)
5. Select a team member (see `docs/dev/team.md`) as ASSIGNEE. If in doubt use `$USER`.
6. Always provide a state label (use `--add-label stage:idea` as default if unsure).
7. Only epics can be created without a parent; all other issue types must have a parent specified with `--parent <parent-id>`.
8. Create the issue and capture the ISSUE_ID with a command such as:
   ```bash
   bd create "Issue title" -t bug|feature|task -p 0-4 --description "Issue description" --assignee <assignee> --add-label stage:idea --validate --json
   bd create "Issue title" -p 1 --deps discovered-from:bd-123 --description "Issue description" --validate --assignee <assignee> --add-label stage:idea --json
   bd create "Subtask" --parent <epic-id> --description "Issue description" --assignee <assignee> --add-label stage:idea --validate --json  # Hierarchical subtask (gets ID like epic-id.1)
   ```
9. Assign the issue to the chosen owner:
   ```bash
   bd update <bead-id> --assignee <assignee> --json
   ```

**Claim and update:**
```bash
bd update bd-42 --status in_progress --add-label stage:in_progress --remove-label stage:plan_complete --json
bd update bd-42 --add-label stage:in_review --remove-label stage:in_progress --json
bd update bd-42 --priority 1 --json
```

***Add Comments to Issue:**
```bash
bd comments add bd-42 "The content of the comment" --actor @your-agent-name --json
bd comments add bd-42 --file /tmp/comment.md --actor @your-agent-name --json
```

**Complete work:**

Issues should only be closed when ALL acceptance criteria are met, all child issues (if any) are also complete and any associated PRs have been merged.

```bash
bd close bd-42 --reason "Completed" --add-label stage:done --remove-label stage:in_review --json
```

### Issue Types

- `bug` - Something broken
- `feature` - New functionality
- `task` - Work item (tests, docs, refactoring)
- `epic` - Large feature with subtasks
- `chore` - Maintenance (dependencies, tooling)

### Priorities

- `0` - Critical (security, data loss, broken builds)
- `1` - High (major features, important bugs)
- `2` - Medium (default, nice-to-have)
- `3` - Low (polish, optimization)
- `4` - Backlog (future ideas)

### Workflow for AI Agents

1. **Check issue is ready**: ensure the issue to be worked on appears in the output of `bd ready`
2. **Claim your task**: `bd update <id> --status in_progress --assignee @your-agent-name`
3. **View details**: `bd show <id> --json` to get all info, including acceptance criteria and related files/paths
4. **Understand context**: Run `waif context` to get a comprehensive view of the objectives of the project you are working on. Review, at least, `README.md` and any relevant beads linked from the issue for the requested change;
5. **Work on it**: Implement, test, document, etc.
6. **Discover new work?** Create linked issue:
   - `bd create "Found bug" -p 1 --deps discovered-from:<parent-id>`
7. **Complete**: `bd close <id> --reason "Done"`
8. **Commit together**: Always commit the `.beads/issues.jsonl` file together with the code changes so issue state stays in sync with code state

### Boundaries
- Ask first:
  - Re-scoping milestones, high-priority work, or cross-team commitments set by the Producer.
  - Retiring/repurposing agents or redefining their roles.
  - Approving multi-issue rewrites or new epics that materially change roadmap assumptions.
- Never:
  - Create parallel tracking systems outside `bd`.
  - Run destructive git commands (`reset`, `push --force`, branch deletions) or merge changes yourself unless given explicit permission.

### Auto-Sync

bd automatically syncs with git:
- Exports to `.beads/issues.jsonl` after changes (5s debounce)
- Imports from JSONL when newer (e.g., after `git pull`)
- No manual export/import needed!

### GitHub Copilot Integration

If using GitHub Copilot, also create `.github/copilot-instructions.md` for automatic instruction loading. Run `bd onboard` to get the content, or see step 2 of the onboard instructions.

### MCP Server (Recommended)

If using Claude or MCP-compatible clients, install the beads MCP server:

```bash
pip install beads-mcp
```

Add to MCP config (e.g., `~/.config/claude/config.json`):
```json
{
  "beads": {
    "command": "beads-mcp",
    "args": []
  }
}
```

Then use `mcp__beads__*` functions instead of CLI commands.

### Managing AI-Generated Planning Documents

AI assistants often create planning and design documents during development:
- PLAN.md, IMPLEMENTATION.md, ARCHITECTURE.md
- DESIGN.md, CODEBASE_SUMMARY.md, INTEGRATION_PLAN.md
- TESTING_GUIDE.md, TECHNICAL_DESIGN.md, and similar files

**Best Practice: Use a dedicated directory for these ephemeral files**

**Recommended approach:**
- Create a `history/` directory in the project root
- Store ALL AI-generated planning/design docs in `history/`
- Keep the repository root clean and focused on permanent project files
- Only access `history/` when explicitly asked to review past planning

**Example .gitignore entry (optional):**
```
# AI planning documents (ephemeral)
history/
```

**Benefits:**
- ✅ Clean repository root
- ✅ Clear separation between ephemeral and permanent documentation
- ✅ Easy to exclude from version control if desired
- ✅ Preserves planning history for archeological research
- ✅ Reduces noise when browsing the project

### CLI Help

Run `bd <command> --help` to see all available flags for any command.
For example: `bd create --help` shows `--parent`, `--deps`, `--assignee`, etc.

### Important Rules

- ✅ Use bd for ALL task tracking
- ✅ Always use `--json` flag for programmatic use
- ✅ Link discovered work with discovered-from dependencies
- ✅ Check `waif in-progress` before asking "what should I work on?"
- ✅ Store AI planning docs in `history/` directory
- ✅ Run `bd <cmd> --help` to discover available flags
- ❌ Do NOT create markdown TODO lists
- ❌ Do NOT use external issue trackers
- ❌ Do NOT duplicate tracking systems
- ❌ Do NOT clutter repo root with planning documents

## Quick Reference

```bash
waif next             # Find available work
bd show <id>          # View issue details
bd update <id> --status in_progress  # Claim work
bd close <id>         # Complete work
bd sync               # Sync with git
```

## Landing the Plane (Session Completion)

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY once a remote is configured:
   ```bash
   git pull --rebase
   bd sync
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- NEVER close, or recommend closing, beads unless work is fully complete, including children and sub-tasks per acceptance criteria
- Whenever listing a bead ID ALWAYS add the title in parentheses
- ALWAYS run `bd sync` after any git operation that changes `.beads/issues.jsonl
- Work is NOT complete until changes are pushed to the canonical remote
- If no remote is configured yet, configure it first, then push
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
- When offering a list of options for next steps always use numbered lists
