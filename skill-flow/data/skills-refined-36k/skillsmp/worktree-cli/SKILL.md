---
name: worktree-cli
description: Git worktree management with worktree.py CLI. Use for creating worktrees, teardown, merging PRs, syncing branches, and Docker service management.
---

# worktree-cli Skill

**Auto-generated reference for `./worktree.py` commands.**

> This is the SOURCE OF TRUTH for worktree.py flags and options.
> Regenerate with: `.claude/scripts/generate-cli-docs.sh`

## When to Use This Skill

- Setting up new worktrees for issues
- Tearing down worktrees after PR merge
- Managing Docker services across worktrees
- Syncing worktrees after merges
- Troubleshooting worktree issues

## Quick Reference

| Command | Purpose | Key Flags |
|---------|---------|-----------|
| `setup <issue>` | Create worktree from GH issue | `--skip-db-import`, `--no-start`, `--build` |
| `complete <pr>` | **RECOMMENDED**: Full lifecycle completion | - |
| `teardown <name>` | Remove worktree only | `-f/--force`, `--keep-branch` |
| `list` | Show all worktrees | `-c/--compact` |
| `merge-pr <num>` | Merge PR + teardown | `--skip-sync`, `--skip-teardown` |
| `cleanup` | Remove merged branches | `-f/--force` (required to execute) |
| `logs` | View Docker logs | `-n <lines>`, `-f/--follow` |

**Prefer `complete` over `merge-pr`** - it handles issue closure and sync automatically.

## Common Workflows

### Start New Work
```bash
./worktree.py setup 42              # From issue number
cd ../42-feature-name
./worktree.py health                # Verify services
```

### Complete Work

**Automatic.** After PR merges, the `merge-teardown` hook runs automatically:
1. Closes GitHub issue
2. Switches to main
3. Runs `./worktree.py teardown`

Manual (if needed):
```bash
./worktree.py teardown 123/feature-name --force
```

### Maintenance
```bash
./worktree.py cleanup               # Dry-run: show what would be cleaned
./worktree.py cleanup --force       # Actually clean up merged branches
./worktree.py prune                 # Remove stale registry entries
```

---

## Command Reference

### auth-status

```
                                                                                
 Usage: worktree.py auth-status [OPTIONS]                                       
                                                                                
 Show auth status and token expiration.                                         
                                                                                
 Checks the shared auth file (.gts-auth.json) and displays:                     
 - Whether authentication is valid                                              
 - Username and T3K ID                                                          
 - Token expiration time                                                        
 - Hours/days remaining until expiration                                        
                                                                                
 This command is also useful for hooks to check auth before operations.         
 With --quiet, only returns exit code (0=valid, 1=invalid/expired).             
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --quiet  -q        Suppress output, exit code only (for hooks)               │
│ --help             Show this message and exit.                               │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### auth-login

```
                                                                                
 Usage: worktree.py auth-login [OPTIONS]                                        
                                                                                
 Open browser to login via T3K OAuth.                                           
                                                                                
 This starts the OAuth flow by opening your browser to the T3K login page.      
 After successful authentication, tokens are automatically saved to the         
 shared auth file (.gts-auth.json).                                             
                                                                                
 All worktrees will then be able to use these credentials.                      
                                                                                
 Args:                                                                          
     backend_port: Port of the backend to use for OAuth callback.               
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --port  -p      INTEGER  Backend port for OAuth callback [default: 8000]     │
│ --help                   Show this message and exit.                         │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### auth-restore

```
                                                                                
 Usage: worktree.py auth-restore [OPTIONS]                                      
                                                                                
 Restore session from saved auth file.                                          
                                                                                
 Reads T3K tokens from the shared auth file and creates a session in            
 the current worktree's backend. This is automatically called during            
 worktree setup if valid auth exists.                                           
                                                                                
 Run this after 'auth-login' to activate auth in the current worktree.          
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --port  -p      INTEGER  Backend port (auto-detected if not specified)       │
│ --help                   Show this message and exit.                         │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### seed

```
                                                                                
 Usage: worktree.py seed [OPTIONS]                                              
                                                                                
 Import database from main worktree.                                            
                                                                                
 Creates a fresh backup of the main worktree's database (including all          
 development data) and imports it into this worktree.                           
                                                                                
 This drops the existing schema and imports a clean copy.                       
                                                                                
 Examples:                                                                      
     ./worktree.py seed                      # Import from main worktree        
     ./worktree.py seed --backup path.sql.gz # Import specific backup           
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --backup  -b      TEXT  Import from specific backup file (path to .sql.gz)   │
│ --help                  Show this message and exit.                          │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### backup

```
                                                                                
 Usage: worktree.py backup [OPTIONS]                                            
                                                                                
 Create a database backup from the main worktree.                               
                                                                                
 This command:                                                                  
 1. Creates a timestamped backup of the main worktree's database                
 2. Verifies the backup integrity (optional)                                    
 3. Prunes old backups based on retention policy (optional)                     
                                                                                
 Exit codes:                                                                    
     0: Success                                                                 
     1: Failure                                                                 
                                                                                
 Examples:                                                                      
     ./worktree.py backup                  # Create backup with defaults        
     ./worktree.py backup --no-prune       # Create backup without pruning old  
 ones                                                                           
     ./worktree.py backup --retention-days 7  # Keep only 7 days of backups     
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --prune             --no-prune              Prune old backups after creating │
│                                             new one (default: True)          │
│                                             [default: prune]                 │
│ --verify            --no-verify             Verify backup integrity after    │
│                                             creation (default: True)         │
│                                             [default: verify]                │
│ --retention-days                   INTEGER  Days to keep old backups when    │
│                                             pruning (default: 14)            │
│                                             [default: 14]                    │
│ --help                                      Show this message and exit.      │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### db-reset

```
                                                                                
 Usage: worktree.py db-reset [OPTIONS]                                          
                                                                                
 Drop database, recreate, and import from main. Clean slate for testing.        
                                                                                
 This command:                                                                  
 1. Stops the backend container (prevents connection errors)                    
 2. Drops and recreates the database                                            
 3. Runs alembic migrations                                                     
 4. Imports data from main worktree (unless --empty is specified)               
 5. Restarts backend and verifies health                                        
                                                                                
 Examples:                                                                      
     ./worktree.py db-reset           # Reset and import from main              
     ./worktree.py db-reset --empty   # Reset with empty database (no data)     
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --from-main    --empty      Import data from main worktree after reset       │
│                             (default: True)                                  │
│                             [default: from-main]                             │
│ --help                      Show this message and exit.                      │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### sync

```
                                                                                
 Usage: worktree.py sync [OPTIONS]                                              
                                                                                
 Sync all worktrees with main (fetch, update main, rebase feature branches).    
                                                                                
 This is CRITICAL after any PR is merged to prevent divergence.                 
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### prune

```
                                                                                
 Usage: worktree.py prune [OPTIONS]                                             
                                                                                
 Remove stale registry entries for non-existent worktrees.                      
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### prune-branches

```
                                                                                
 Usage: worktree.py prune-branches [OPTIONS]                                    
                                                                                
 Delete local branches whose remote tracking branch no longer exists.           
                                                                                
 After PRs are squash-merged, GitHub deletes the remote branch but the          
 local branch remains with tracking status "gone". This command cleans          
 up those stale local branches.                                                 
                                                                                
 Equivalent to: git branch -vv | grep gone | xargs git branch -D                
                                                                                
 Protected branches (main, master, develop, development) are never deleted.     
                                                                                
 Examples:                                                                      
     ./worktree.py prune-branches           # Delete stale branches             
     ./worktree.py prune-branches --dry-run # Show what would be deleted        
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --dry-run  -n        Show what would be deleted without actually deleting    │
│ --help               Show this message and exit.                             │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### orphans

```
                                                                                
 Usage: worktree.py orphans [OPTIONS] [ACTION]                                  
                                                                                
 Manage orphaned git worktrees (exist in git but not in registry).              
                                                                                
 Orphans occur when:                                                            
 - Registry database was reset or corrupted                                     
 - Worktree was created manually with git worktree add                          
 - Setup failed partway through                                                 
                                                                                
 Actions:                                                                       
     list   - Show all orphaned worktrees (default)                             
     adopt  - Add orphan(s) to registry with auto-assigned ports                
     remove - Delete orphan(s) from git (removes worktree directory)            
                                                                                
 Examples:                                                                      
     ./worktree.py orphans                    # List all orphans                
     ./worktree.py orphans adopt --name main  # Adopt specific orphan           
     ./worktree.py orphans adopt --all        # Adopt all orphans               
     ./worktree.py orphans remove --name old-branch --force  # Remove without   
 confirm                                                                        
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│   action      [ACTION]  Action: list (show orphans), adopt (add to           │
│                         registry), remove (delete from git)                  │
│                         [default: list]                                      │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --name   -n      TEXT  Orphan name (directory name) to act on                │
│ --all    -a            Apply action to all orphans (use with adopt or        │
│                        remove)                                               │
│ --force  -f            Force removal without confirmation                    │
│ --help                 Show this message and exit.                           │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### list

```
                                                                                
 Usage: worktree.py list [OPTIONS]                                              
                                                                                
 List all registered worktrees with full details.                               
                                                                                
 By default shows expanded view with containers, ports, and credentials.        
 Use --compact for a simple table view.                                         
                                                                                
 Also checks for orphaned git worktrees (worktrees in git but not in registry). 
 Use --no-orphans to skip this check.                                           
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --compact  -c                    Show compact table view                     │
│ --orphans      --no-orphans      Check for orphaned git worktrees            │
│                                  [default: orphans]                          │
│ --help                           Show this message and exit.                 │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### status

```
                                                                                
 Usage: worktree.py status [OPTIONS]                                            
                                                                                
 Show detailed status of current worktree.                                      
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### health

```
                                                                                
 Usage: worktree.py health [OPTIONS]                                            
                                                                                
 Check health of current worktree. Auto-fixes frontend staleness by default.    
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --check-only          Report only, don't auto-fix issues (for CI/scripts)    │
│ --help                Show this message and exit.                            │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### ports

```
                                                                                
 Usage: worktree.py ports [OPTIONS]                                             
                                                                                
 Show port allocations for all worktrees.                                       
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### merge-pr

```
                                                                                
 Usage: worktree.py merge-pr [OPTIONS] PR_NUMBER                                
                                                                                
 Merge a PR and sync all worktrees (RECOMMENDED workflow).                      
                                                                                
 This command:                                                                  
 1. Checks if PR is already merged (handles gracefully if so)                   
 2. Merges the PR via gh CLI (squash merge) if not yet merged                   
 3. Auto-tears down the merged worktree (prevents rebase issues)                
 4. Updates main branch                                                         
 5. Rebases all active feature worktrees onto new main                          
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    pr_number      INTEGER  PR number to merge [required]                   │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --skip-sync              Skip syncing other worktrees                        │
│ --skip-teardown          Skip auto-teardown of merged worktree               │
│ --help                   Show this message and exit.                         │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### complete

```
                                                                                
 Usage: worktree.py complete [OPTIONS] PR_NUMBER                                
                                                                                
 ATOMIC: Complete a PR lifecycle (merge + close issue + teardown).              
                                                                                
 This is the recommended way to finish work on a PR. It handles:                
 1. Verify/merge the PR                                                         
 2. Update main branch (pull merged changes immediately)                        
 3. Close the linked GitHub issue                                               
 4. Teardown the worktree (stop Docker, remove files, delete branch)            
                                                                                
 All steps are tracked in a state file. On failure, reports exactly what        
 succeeded and what failed.                                                     
                                                                                
 Exit codes:                                                                    
     0 = All steps completed successfully                                       
     1 = One or more steps failed (see output for details)                      
                                                                                
 Examples:                                                                      
     ./worktree.py complete 227                                                 
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    pr_number      INTEGER  PR number to complete [required]                │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### cleanup

```
                                                                                
 Usage: worktree.py cleanup [OPTIONS]                                           
                                                                                
 Clean up merged branches and orphaned Docker resources.                        
                                                                                
 By default runs in dry-run mode. Use --force to actually clean up.             
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --force  -f        Actually perform cleanup (default: dry-run)               │
│ --help             Show this message and exit.                               │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### version

```
                                                                                
 Usage: worktree.py version [OPTIONS]                                           
                                                                                
 Show version information.                                                      
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### hooks

```
                                                                                
 Usage: worktree.py hooks [OPTIONS] ACTION                                      
                                                                                
 Manage git hooks for automatic sync.                                           
                                                                                
 Actions:                                                                       
     install   - Install post-commit hook for auto-sync                         
     uninstall - Remove post-commit hook                                        
     status    - Check if hooks are installed                                   
                                                                                
 The post-commit hook automatically rebases your feature branch onto            
 origin/main after every commit, keeping you in sync and preventing             
 merge conflicts.                                                               
                                                                                
 To temporarily disable auto-sync:                                              
     GTS_NO_AUTO_SYNC=1 git commit -m "message"                                 
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    action      TEXT  Action: install, uninstall, or status [required]      │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### check-stale

```
                                                                                
 Usage: worktree.py check-stale [OPTIONS]                                       
                                                                                
 Check for stale pending operations.                                            
                                                                                
 Returns exit code 1 if any operations have been pending for > 2 minutes,       
 indicating a failed setup or complete operation.                               
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### validate

```
                                                                                
 Usage: worktree.py validate [OPTIONS]                                          
                                                                                
 Validate environment and check for divergence.                                 
                                                                                
 Performs comprehensive checks:                                                 
 - Git configuration                                                            
 - Docker status                                                                
 - Port allocations                                                             
 - Main branch sync status                                                      
 - Feature branch divergence                                                    
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### is-fresh

```
                                                                                
 Usage: worktree.py is-fresh [OPTIONS]                                          
                                                                                
 Check if current worktree was recently created.                                
                                                                                
 Returns exit code 0 if worktree is "fresh" (created within threshold),         
 exit code 1 if older or not in a registered worktree.                          
                                                                                
 Useful for hooks to skip redundant checks after worktree setup.                
                                                                                
 Examples:                                                                      
     ./worktree.py is-fresh              # Default 5 minutes                    
     ./worktree.py is-fresh --minutes 10 # Custom threshold                     
     ./worktree.py is-fresh --quiet      # Just exit code                       
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --minutes  -m      INTEGER  Threshold in minutes to consider fresh           │
│                             [default: 5]                                     │
│ --quiet    -q               Suppress output, exit code only                  │
│ --help                      Show this message and exit.                      │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### services-start

```
                                                                                
 Usage: worktree.py services-start [OPTIONS]                                    
                                                                                
 Start Docker services for current worktree.                                    
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### stop

```
                                                                                
 Usage: worktree.py stop [OPTIONS]                                              
                                                                                
 Stop Docker services for current worktree.                                     
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### logs

```
                                                                                
 Usage: worktree.py logs [OPTIONS]                                              
                                                                                
 Show Docker compose logs for current worktree.                                 
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --lines   -n      INTEGER  Number of lines to show [default: 50]             │
│ --follow  -f               Follow log output                                 │
│ --help                     Show this message and exit.                       │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### start

```
                                                                                
 Usage: worktree.py start [OPTIONS]                                             
                                                                                
 Start work session with full environment validation.                           
                                                                                
 This is the main entry point for development workflow. It:                     
 1. Validates local state (orphaned worktrees, uncommitted changes, stale ops)  
 2. Syncs with GitHub to fetch open issues                                      
 3. Analyzes issues by readiness (ready, blocked, in_progress)                  
 4. Presents work selection in interactive mode                                 
                                                                                
 Examples:                                                                      
     ./worktree.py start                    # Full interactive workflow         
     ./worktree.py start --non-interactive  # Just show status, no selection    
     ./worktree.py start --skip-github      # Skip GitHub sync (offline mode)   
     ./worktree.py start --auto-fix         # Auto-fix recoverable issues       
     ./worktree.py start --filter backend   # Filter issues by keyword          
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --interactive    --non-interactive          Run in interactive mode for work │
│                                             selection                        │
│                                             [default: interactive]           │
│ --skip-github                               Skip GitHub issue sync (use      │
│                                             cache only)                      │
│ --auto-fix                                  Automatically fix recoverable    │
│                                             issues                           │
│ --filter                              TEXT  Filter issues by label or        │
│                                             keyword                          │
│ --help                                      Show this message and exit.      │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### setup

```
                                                                                
 Usage: worktree.py setup [OPTIONS] ISSUE_OR_BRANCH                             
                                                                                
 Create a new git worktree with isolated Docker environment.                    
                                                                                
 Examples:                                                                      
 ./worktree.py setup 42                                                         
 ./worktree.py setup 42/feature-audio-analysis                                  
 ./worktree.py setup main                                                       
 ./worktree.py setup https://github.com/.../issues/42                           
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    issue_or_branch      TEXT  Issue number, branch name, or GitHub issue   │
│                                 URL                                          │
│                                 [required]                                   │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --skip-db-import                       Skip importing database from main     │
│                                        worktree (start with fresh database)  │
│ --no-start                             Don't start Docker services after     │
│                                        setup                                 │
│ --build                                Build Docker images before starting   │
│ --force               -f               Skip blocking health check (expert    │
│                                        override - use with caution)          │
│ --health-timeout              INTEGER  Seconds to wait for services to       │
│                                        become healthy (default: 60)          │
│                                        [default: 60]                         │
│ --allow-stale-backup                   Allow using an existing backup if     │
│                                        fresh backup fails (NOT RECOMMENDED)  │
│ --help                                 Show this message and exit.           │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### sync-start

```
                                                                                
 Usage: worktree.py sync-start [OPTIONS]                                        
                                                                                
 Pull latest changes before starting work (session start hook).                 
                                                                                
 This command is called automatically by the SessionStart hook.                 
 It ensures the worktree is synced before work begins.                          
                                                                                
 Operations:                                                                    
 - Fetch from origin                                                            
 - Pull with rebase                                                             
                                                                                
 Safe: Gracefully handles conflicts by aborting rebase.                         
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --quiet  -q        Suppress output (for hooks)                               │
│ --help             Show this message and exit.                               │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### sync-stop

```
                                                                                
 Usage: worktree.py sync-stop [OPTIONS]                                         
                                                                                
 Save and push all work before ending session (stop hook).                      
                                                                                
 This command is called automatically by the Stop hook.                         
 It ensures all work is committed and pushed before the session ends.           
                                                                                
 Operations:                                                                    
 - Commit any uncommitted changes as WIP                                        
 - Push to remote (MUST succeed)                                                
                                                                                
 BLOCKING: This command will fail if push fails, preventing session end.        
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### teardown

```
                                                                                
 Usage: worktree.py teardown [OPTIONS] NAME_OR_BRANCH                           
                                                                                
 Remove a worktree and clean up all resources.                                  
                                                                                
 Stops containers, removes volumes, deletes git worktree,                       
 and optionally deletes branches (local and remote).                            
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    name_or_branch      TEXT  Worktree name or branch to tear down          │
│                                [required]                                    │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --force        -f        Force teardown even if branch not merged            │
│ --keep-branch            Keep the git branch after teardown                  │
│ --help                   Show this message and exit.                         │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### cleanup-orphans

```
                                                                                
 Usage: worktree.py cleanup-orphans [OPTIONS]                                   
                                                                                
 Find and remove orphaned Docker containers.                                    
                                                                                
 Orphaned containers are Docker containers from worktrees that no longer        
 exist in the registry. This can happen when:                                   
 - A worktree was deleted manually (rm -rf) without using teardown              
 - The registry database was reset or corrupted                                 
 - A setup failed partway through                                               
                                                                                
 Use --dry-run to see what would be cleaned without removing anything.          
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --dry-run  -n        Show what would be cleaned without doing it             │
│ --help               Show this message and exit.                             │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

## Auth Workflow

**Initial authentication (once):**
```bash
./worktree.py setup 42              # Creates worktree
./worktree.py auth-login --port 8030  # Login via browser (uses worktree's backend)
```

**After that, all worktrees share the auth:**
```bash
./worktree.py setup 123             # Auto-restores auth from shared file
```

**Check status anytime:**
```bash
./worktree.py auth-status
```

---

## Common Mistakes to Avoid

| Wrong | Right | Why |
|-------|-------|-----|
| `prune --force` | `prune` | prune has no --force flag |
| `cleanup` alone | `cleanup --force` | cleanup is dry-run by default |
| `teardown` on main | Never teardown main | main is the base worktree |
| Manual `git pull` after merge | `complete <num>` | complete handles sync + issue closure |
| `merge-pr` alone | `complete <num>` | complete is the recommended full lifecycle |
