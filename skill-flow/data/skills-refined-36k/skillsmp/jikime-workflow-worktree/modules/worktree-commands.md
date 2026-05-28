# Worktree Commands Module

Purpose: Complete CLI command reference for Git worktree management with detailed usage examples and advanced options.

Version: 2.0.0
Last Updated: 2026-01-06

---

## Quick Reference (30 seconds)

Command Categories:
- Creation: new - Create isolated worktree
- Navigation: list, go - Browse and navigate
- Management: sync, remove, clean, done - Maintain worktrees
- Status: status - Check worktree state
- Configuration: config, recover - Manage settings

Quick Start:
1. Create worktree: jikime worktree new SPEC-001
2. List worktrees: jikime worktree list
3. Go to worktree: eval $(jikime worktree go SPEC-001)

---

## Creation Commands

### jikime worktree new - Create Worktree

Create a new isolated Git worktree for SPEC development.

Syntax: jikime worktree new <spec-id> [options]

Arguments:
- spec-id: SPEC identifier (e.g., SPEC-001, SPEC-AUTH-001)

Options:
- --branch, -b <name>: Custom branch name (default: feature/{spec-id})
- --base <branch>: Base branch for new worktree (default: main)
- --force, -f: Force creation even if worktree exists
- --llm-config <path>: Path to custom LLM config file

Examples:
- Basic creation: jikime worktree new SPEC-001
- Custom branch: jikime worktree new SPEC-002 --branch feature/payment-gateway
- From develop: jikime worktree new SPEC-003 --base develop
- Force recreate: jikime worktree new SPEC-001 --force
- With LLM config: jikime worktree new SPEC-001 --llm-config ~/.claude/my-settings.json

Auto-Generated Branch Pattern:
- Format: feature/{SPEC-ID}
- Example: SPEC-001 becomes feature/SPEC-001

LLM Settings Auto-Copy:
- If .claude/settings.local.json exists in main repo, it's automatically copied to the new worktree

---

## Navigation Commands

### jikime worktree list - List Worktrees

Display all registered worktrees with their status and metadata.

Syntax: jikime worktree list [options]

Options:
- --format <format>: Output format (table, json, csv)
- --status <status>: Filter by status (active, merged, stale)
- --sort <field>: Sort by field (name, created, modified, status)
- --reverse: Reverse sort order
- --verbose: Show detailed information

Examples:
- Table format: jikime worktree list
- JSON output: jikime worktree list --format json
- Active only: jikime worktree list --status active
- Sort by date: jikime worktree list --sort created
- Detailed: jikime worktree list --verbose

### jikime worktree go - Navigate to Worktree

Output the worktree path for shell navigation.

Syntax: jikime worktree go <spec-id>

Arguments:
- spec-id: SPEC identifier to navigate to

Shell Integration:
- eval pattern (recommended): eval $(jikime worktree go SPEC-001)

Examples:
- Navigate to worktree: eval $(jikime worktree go SPEC-001)
- Get path only: jikime worktree go SPEC-001

---

## Management Commands

### jikime worktree sync - Synchronize Worktree

Synchronize worktree with its base branch.

Syntax: jikime worktree sync <spec-id> [options]

Arguments:
- spec-id: Worktree identifier (or --all for all worktrees)

Options:
- --base <branch>: Base branch to sync from (default: main)
- --rebase: Use rebase instead of merge
- --ff-only: Only sync if fast-forward is possible
- --squash: Squash all commits into a single commit
- --auto-resolve: Automatically resolve conflicts
- --all: Sync all worktrees

Sync Strategies:
- merge (default): Preserve history with merge commit
- rebase: Linear history by replaying commits
- squash: Combine all changes into single commit
- fast-forward: Only sync if no divergence

Examples:
- Sync specific: jikime worktree sync SPEC-001
- Sync all: jikime worktree sync --all
- With rebase: jikime worktree sync SPEC-001 --rebase
- Fast-forward only: jikime worktree sync SPEC-001 --ff-only
- Squash merge: jikime worktree sync SPEC-001 --squash
- From develop: jikime worktree sync SPEC-001 --base develop
- Auto-resolve conflicts: jikime worktree sync SPEC-001 --auto-resolve

Conflict Auto-Resolution (3-stage):
1. Try --ours (keep worktree version)
2. Try --theirs (accept base version)
3. Remove conflict markers

### jikime worktree remove - Remove Worktree

Remove a worktree and clean up its registration.

Syntax: jikime worktree remove <spec-id> [options]

Options:
- --force: Force removal without confirmation
- --keep-branch: Keep the branch after removing worktree
- --backup: Create backup before removal
- --dry-run: Show what would be removed without doing it

Examples:
- Interactive: jikime worktree remove SPEC-001
- Force: jikime worktree remove SPEC-001 --force
- Keep branch: jikime worktree remove SPEC-001 --keep-branch
- With backup: jikime worktree remove SPEC-001 --backup
- Preview: jikime worktree remove SPEC-001 --dry-run

### jikime worktree clean - Clean Up Worktrees

Remove worktrees for merged branches or stale worktrees.

Syntax: jikime worktree clean [options]

Options:
- --merged-only: Only remove worktrees with merged branches
- --stale: Remove worktrees not updated in specified days
- --days <number>: Stale threshold in days (default: 30)
- --interactive: Interactive selection of worktrees to remove
- --dry-run: Show what would be cleaned without doing it
- --force: Skip confirmation prompts

Examples:
- Merged only: jikime worktree clean --merged-only
- Stale (30 days): jikime worktree clean --stale
- Custom threshold: jikime worktree clean --stale --days 14
- Interactive: jikime worktree clean --interactive

### jikime worktree done - Complete and Merge

Complete worktree workflow: merge to base and cleanup.

Syntax: jikime worktree done <spec-id> [options]

Arguments:
- spec-id: SPEC identifier to complete

Options:
- --push: Push to remote after merge
- --force: Force merge even with uncommitted changes

Examples:
- Complete and cleanup: jikime worktree done SPEC-001
- Complete and push: jikime worktree done SPEC-001 --push

### jikime worktree recover - Recover Registry

Rebuild registry from existing worktree directories on disk.

Syntax: jikime worktree recover

Examples:
- Recover registry: jikime worktree recover

---

## Status and Configuration

### jikime worktree status - Show Worktree Status

Display detailed status information about worktrees.

Syntax: jikime worktree status [spec-id] [options]

Arguments:
- spec-id: Specific worktree (optional, shows current if not specified)

Options:
- --all: Show status of all worktrees
- --sync-check: Check if worktrees need sync
- --detailed: Show detailed Git status
- --format <format>: Output format (table, json)

Examples:
- Current worktree: jikime worktree status
- Specific worktree: jikime worktree status SPEC-001
- All with sync check: jikime worktree status --all --sync-check
- Detailed Git status: jikime worktree status SPEC-001 --detailed
- JSON output: jikime worktree status --all --format json

Status Output Includes:
- Worktree path and branch
- Commits ahead/behind base
- Modified and untracked files
- Sync status and last sync time

### jikime worktree config - Configuration Management

Manage jikime worktree configuration settings.

Syntax: jikime worktree config <action> [key] [value]

Actions:
- get [key]: Get configuration value
- set <key> <value>: Set configuration value
- list: List all configuration
- reset [key]: Reset to default value
- edit: Open configuration in editor

Configuration Keys:
- worktree_root: Root directory for worktrees
- auto_sync: Enable automatic sync (true/false)
- cleanup_merged: Auto-cleanup merged worktrees (true/false)
- default_base: Default base branch (main/develop)
- template_dir: Directory for worktree templates
- sync_strategy: Sync strategy (merge, rebase, squash)

Examples:
- List all: jikime worktree config list
- Get value: jikime worktree config get worktree_root
- Set value: jikime worktree config set auto_sync true
- Reset: jikime worktree config reset worktree_root
- Edit: jikime worktree config edit

---

## Advanced Usage

### Batch Operations

Sync all active worktrees:
- Use shell loop with list --format json and jq to extract IDs
- Run sync for each ID in sequence or parallel

Clean all merged worktrees:
- jikime worktree clean --merged-only --force

Create worktrees from SPEC list:
- Read SPEC IDs from file
- Run new command for each

### Shell Aliases

Recommended aliases for .bashrc or .zshrc:
- jwl: jikime worktree list
- jwg: Navigate with eval pattern (jikime worktree go)
- jwsync: Sync current worktree
- jwclean: Clean merged worktrees

Note: The CLI also supports short alias `jikime wt` (e.g., `jikime wt list`)

### Git Hooks Integration

Post-checkout hook actions:
- Detect worktree environment
- Update last access time in registry
- Check if sync needed with base branch
- Load worktree-specific environment

Pre-push hook actions:
- Detect if pushing from worktree
- Check for uncommitted changes
- Verify sync status with base
- Update registry with push timestamp

---

Version: 2.0.0
Last Updated: 2026-01-06
Module: Complete CLI command reference with usage examples
