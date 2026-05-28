# Graphite CLI Command Reference

## Global Flags

- `--help` - Show help for a command
- `--cwd` - Working directory for operations
- `--debug` - Write debug output
- `--interactive` / `--no-interactive` - Enable/disable prompts (default: enabled)
- `--verify` / `--no-verify` - Enable/disable git hooks (default: enabled)
- `--quiet` - Minimize output, implies `--no-interactive`

## Branch Creation & Modification

### gt create [name]

Create a new branch stacked on current branch with staged changes.

**Flags:**
- `-a, --all` - Stage all unstaged changes including untracked files
- `-m, --message` - Commit message
- `-i, --insert` - Insert between current branch and its child
- `-p, --patch` - Pick hunks to stage
- `-u, --update` - Stage updates to tracked files only
- `-v, --verbose` - Show diff in commit template
- `--ai` / `--no-ai` - AI-generate branch name and message

### gt modify

Amend current branch's commit or create new commit. Auto-restacks descendants.

**Flags:**
- `-a, --all` - Stage all changes
- `-c, --commit` - Create new commit instead of amending
- `-e, --edit` - Open editor for commit message
- `-m, --message` - New commit message
- `-p, --patch` - Pick hunks to stage
- `-u, --update` - Stage tracked file updates
- `--into` - Amend into specified downstack branch
- `--interactive-rebase` - Start git interactive rebase
- `--reset-author` - Set commit author to current user

### gt absorb

Amend staged changes to relevant commits in current stack.

**Flags:**
- `-a, --all` - Stage all unstaged changes (not untracked)
- `-d, --dry-run` - Print what would happen
- `-f, --force` - Skip confirmation
- `-p, --patch` - Pick hunks to stage

### gt squash

Squash all commits in current branch into single commit.

**Flags:**
- `-m, --message` - Commit message
- `--edit` - Modify existing message
- `-n, --no-edit` - Keep existing message

### gt fold

Fold branch's changes into parent, restack descendants.

**Flags:**
- `-k, --keep` - Keep current branch name instead of parent's

### gt split

Split current branch into multiple branches.

**Flags:**
- `-c, --commit, --by-commit` - Split by commit history
- `-h, --hunk, --by-hunk` - Split by hunk interactively
- `-f, --file, --by-file` - Split files matching pathspecs

## Submitting PRs

### gt submit

Push branches and create/update PRs on GitHub.

**Flags:**
- `-s, --stack` - Include descendant branches
- `-d, --draft` - Create PRs as drafts
- `-p, --publish` - Publish draft PRs
- `-e, --edit` / `-n, --no-edit` - Edit/skip PR metadata
- `--edit-title` / `--no-edit-title` - Edit/skip title
- `--edit-description` / `--no-edit-description` - Edit/skip description
- `-r, --reviewers` - Set reviewers (comma-separated or prompt)
- `-t, --team-reviewers` - Team slugs for review
- `-m, --merge-when-ready` - Auto-merge when requirements met
- `-c, --confirm` - Confirm before submitting
- `--dry-run` - Report what would happen
- `-f, --force` - Force push (vs --force-with-lease)
- `-u, --update-only` - Only update existing PRs
- `-v, --view` - Open PR in browser after
- `-w, --web` - Edit metadata in browser
- `--cli` - Edit metadata via CLI
- `--ai` / `--no-ai` - AI-generate title/description
- `--comment` - Add comment to PR
- `--restack` - Restack before submitting
- `--rerequest-review` - Rerequest from current reviewers
- `--always` - Push even if unchanged
- `--branch` - Run from specified branch
- `--target-trunk` - PR target trunk

### gt merge

Merge PRs from trunk to current branch via Graphite.

**Flags:**
- `-c, --confirm` - Confirm before merging
- `--dry-run` - Report what would merge

## Navigation

### gt checkout [branch]

Switch to branch. Interactive selector if no branch provided.

**Flags:**
- `-a, --all` - Show all trunks in selection
- `-u, --show-untracked` - Include untracked branches
- `-s, --stack` - Only show current stack
- `-t, --trunk` - Checkout trunk

### gt up [steps]

Switch to child of current branch.

**Flags:**
- `-n, --steps` - Levels to traverse
- `--to` - Target branch to navigate toward

### gt down [steps]

Switch to parent of current branch.

**Flags:**
- `-n, --steps` - Levels to traverse

### gt top

Switch to tip of current stack. Prompts if ambiguous.

### gt bottom

Switch to branch closest to trunk in current stack.

## Stack Management

### gt restack

Ensure each branch has parent in Git history, rebasing if needed.

**Flags:**
- `--branch` - Run from specified branch
- `--downstack` - Only restack branch and ancestors
- `--upstack` - Only restack branch and descendants
- `--only` - Only restack this branch

### gt move

Rebase current branch onto target, restack descendants.

**Flags:**
- `-o, --onto` - Target branch
- `--source` - Branch to move (default: current)
- `-a, --all` - Show all trunks in selection

### gt reorder

Reorder branches between trunk and current via editor.

## Syncing

### gt sync

Sync all branches with remote, clean merged/closed PRs, restack.

**Flags:**
- `-a, --all` - Sync across all trunks
- `-f, --force` - Skip confirmations
- `--restack` / `--no-restack` - Restack after sync (default: true)

### gt get [branch]

Sync branches from trunk to specified branch/PR from remote.

**Flags:**
- `-d, --downstack` - Don't sync upstack branches
- `-f, --force` - Overwrite with remote
- `--restack` / `--no-restack` - Restack after (default: true)
- `-U, --unfrozen` - Checkout as unfrozen

## Branch Operations

### gt delete [name]

Delete branch and Graphite metadata. Children restack to parent.

**Flags:**
- `-f, --force` - Delete even if not merged/closed
- `-c, --close` - Close associated PR on GitHub
- `--downstack` - Also delete ancestors
- `--upstack` - Also delete children

### gt rename [name]

Rename branch. Removes PR association.

**Flags:**
- `-f, --force` - Allow rename with open PR

### gt track [branch]

Start tracking branch with Graphite by selecting parent.

**Flags:**
- `-f, --force` - Use most recent tracked ancestor as parent
- `-p, --parent` - Specify parent branch

### gt untrack [branch]

Stop tracking branch. Children also untracked.

**Flags:**
- `-f, --force` - Skip confirmation

### gt pop

Delete current branch but keep working tree state.

### gt freeze [branch]

Freeze branch and downstack - prevents local modifications.

### gt unfreeze [branch]

Unfreeze branch and upstack.

## Information

### gt log [command]

Show stacks. Forms: `gt log`, `gt log short`, `gt log long`.

**Flags:**
- `-a, --all` - Show all trunks
- `-r, --reverse` - Print upside down
- `-u, --show-untracked` - Include untracked
- `-s, --stack` - Only current stack
- `-n, --steps` - Levels to show (implies --stack)
- `--classic` - Old style

### gt info [branch]

Display branch information.

**Flags:**
- `-b, --body` - Show PR body
- `-d, --diff` - Show diff vs parent
- `-p, --patch` - Show commit changes
- `-s, --stat` - Show diffstat

### gt parent / gt children / gt trunk

Show parent, children, or trunk of current branch.

`gt trunk` flags:
- `--add` - Add trunk
- `-a, --all` - Show all trunks

### gt pr [branch]

Open PR page for branch or PR number.

**Flags:**
- `--stack` - Open stack page

## Conflict Resolution

### gt continue

Continue command halted by rebase conflict.

**Flags:**
- `-a, --all` - Stage all changes first

### gt abort

Abort current command halted by conflict.

**Flags:**
- `-f, --force` - Skip confirmation

### gt undo

Undo most recent Graphite mutations.

**Flags:**
- `-f, --force` - Skip confirmation

## Setup

### gt init

Initialize Graphite by selecting trunk branch.

**Flags:**
- `--trunk` - Trunk branch name
- `--reset` - Untrack all branches

### gt auth

Add auth token for GitHub.

**Flags:**
- `-t, --token` - Auth token from https://app.graphite.com/activate

### gt config

Configure Graphite CLI (interactive).

### gt upgrade

Update CLI to latest stable version.

## Git Passthroughs

These pass arguments directly to git:
- `gt add [args..]`
- `gt cherry-pick [args..]`
- `gt rebase [args..]`
- `gt reset [args..]`
- `gt restore [args..]`

### gt revert [sha]

Create branch reverting a trunk commit.

**Flags:**
- `-e, --edit` - Edit commit message
