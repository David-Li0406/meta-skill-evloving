---
name: gobby-merge
description: Use when user asks to "/gobby-merge", "merge branches", "resolve conflicts", "AI merge". AI-powered merge conflict resolution - start merges, resolve conflicts, and apply resolutions.
---

# /gobby-merge - AI-Powered Merge Conflict Resolution

This skill manages git merge operations with AI-powered conflict resolution via the gobby-merge MCP server. Parse the user's input to determine which subcommand to execute.

## Subcommands

### `/gobby-merge start <worktree-id> <source-branch>` - Start a merge

Call `gobby-merge.merge_start` with:
- `worktree_id`: (required) ID of the worktree to merge in
- `source_branch`: (required) Branch being merged in
- `target_branch`: Target branch (default: "main")
- `strategy`: Resolution strategy (auto, conflict_only, full_file, manual)

Starts a merge operation and attempts AI-powered conflict resolution.

Example: `/gobby-merge start wt-abc123 feature/auth`
-> `merge_start(worktree_id="wt-abc123", source_branch="feature/auth")`

Example: `/gobby-merge start wt-abc123 feature/auth --strategy conflict_only`
-> `merge_start(worktree_id="wt-abc123", source_branch="feature/auth", strategy="conflict_only")`

### `/gobby-merge status <resolution-id>` - Check merge status

Call `gobby-merge.merge_status` with:
- `resolution_id`: (required) The resolution ID returned from merge_start

Returns merge resolution status including:
- Resolution details (source/target branches, status, tier used)
- List of conflicts with their resolution status
- Counts of pending vs resolved conflicts

Example: `/gobby-merge status res-abc123`
-> `merge_status(resolution_id="res-abc123")`

### `/gobby-merge resolve <conflict-id>` - Resolve a specific conflict

Call `gobby-merge.merge_resolve` with:
- `conflict_id`: (required) The conflict ID
- `resolved_content`: Manual resolution content (skips AI)
- `use_ai`: Whether to use AI for resolution (default: true)

Resolves a specific conflict, either manually or with AI assistance.

Example: `/gobby-merge resolve conf-abc123`
-> `merge_resolve(conflict_id="conf-abc123", use_ai=true)`

Example with manual content:
-> `merge_resolve(conflict_id="conf-abc123", resolved_content="<resolved code>")`

### `/gobby-merge apply <resolution-id>` - Apply and complete merge

Call `gobby-merge.merge_apply` with:
- `resolution_id`: (required) The resolution ID

Applies all resolved conflicts and completes the merge. All conflicts must be resolved before calling apply.

Example: `/gobby-merge apply res-abc123`
-> `merge_apply(resolution_id="res-abc123")`

### `/gobby-merge abort <resolution-id>` - Abort the merge

Call `gobby-merge.merge_abort` with:
- `resolution_id`: (required) The resolution ID

Aborts the merge operation and restores the previous state. Cannot abort already-resolved merges.

Example: `/gobby-merge abort res-abc123`
-> `merge_abort(resolution_id="res-abc123")`

## Resolution Tiers

The AI merge resolver uses a tiered strategy, escalating from fastest to most thorough:

| Tier | Name | Description |
|------|------|-------------|
| 1 | `git_auto` | Git's built-in merge - fastest, handles simple merges |
| 2 | `conflict_only_ai` | AI resolves just the conflict markers/hunks |
| 3 | `full_file_ai` | AI considers full file context for resolution |
| 4 | `human_review` | Fallback requiring manual intervention |

The system automatically escalates through tiers if lower tiers fail. You can force a specific tier with the `strategy` parameter in `merge_start`:

- `auto` - Let the system decide (default)
- `conflict_only` - Force tier 2 (conflict_only_ai)
- `full_file` - Force tier 3 (full_file_ai)
- `manual` - Skip AI, require manual resolution

## Workflow Example

A typical merge workflow:

```text
1. Create worktree and work on feature
   /gobby-worktrees spawn feature/auth "Implement OAuth login"

2. When ready to merge, start the merge operation
   /gobby-merge start wt-abc123 feature/auth
   -> Returns resolution_id and initial resolution attempt

3. If conflicts exist, check status
   /gobby-merge status res-abc123
   -> Shows pending conflicts

4. Resolve individual conflicts (AI or manual)
   /gobby-merge resolve conf-001
   /gobby-merge resolve conf-002

5. Once all conflicts resolved, apply the merge
   /gobby-merge apply res-abc123
   -> Completes the merge

6. If something goes wrong, abort
   /gobby-merge abort res-abc123
   -> Restores previous state
```

## Response Format

After executing the appropriate MCP tool, present the results clearly:

- For start: Show resolution_id, tier used, success status, and any conflicts
- For status: Resolution details, conflict list with status, pending/resolved counts
- For resolve: Updated conflict status, resolution method (AI/manual)
- For apply: Confirmation with list of merged files
- For abort: Confirmation of abort

## Error Handling

Common errors:
- "worktree_id is required" - Provide the worktree ID
- "source_branch is required" - Provide the branch to merge
- "Resolution not found" - Invalid resolution_id
- "Cannot apply: X unresolved conflicts remaining" - Resolve conflicts first
- "Cannot abort: merge is already resolved" - Merge already completed

If the subcommand is not recognized, show available subcommands:
- start, status, resolve, apply, abort
