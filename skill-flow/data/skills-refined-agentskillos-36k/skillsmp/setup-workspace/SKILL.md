---
name: setup-workspace
description: Skill for creating feature branches or git worktrees for ticket implementation. Handles branch naming, base branch selection, and workspace isolation.
---

# Setup Workspace Skill

This skill prepares the git workspace for ticket implementation by creating appropriately named branches or worktrees.

## Workspace Types

### 1. Branch (Default)
Standard git branch created from base branch.
- **Pros**: Simple, familiar, no extra disk space
- **Cons**: Must switch context, can conflict with current work

### 2. Worktree (Only if tooling detected)
Separate working directory with its own checkout.
- **Pros**: Parallel work, no context switching, isolated
- **Cons**: Requires project-specific setup (docker, env, etc.)

**IMPORTANT**: Worktree mode is ONLY available if the project has explicit tooling to support it. Raw `git worktree` is NOT sufficient - the project needs scripts to handle environment setup (docker-compose, .env files, dependencies, etc.).

---

## Worktree Capability Detection

Before offering worktree as an option, detect if the project supports it.

### Detection Strategy

Search for worktree-related tooling in this order:

#### 1. Makefile Targets
```bash
# Search for worktree-related targets
grep -E "^worktree|^wt-|^new-worktree|worktree:" Makefile makefile GNUmakefile 2>/dev/null
```

Look for patterns:
- `worktree:`, `worktree-setup:`, `worktree-create:`
- `wt-new:`, `wt-setup:`, `wt-init:`
- `new-worktree:`, `create-worktree:`

#### 2. Scripts Directory
```bash
# Search for worktree scripts
ls -la scripts/*worktree* bin/*worktree* tools/*worktree* 2>/dev/null
ls -la scripts/*wt* bin/*wt* 2>/dev/null
```

#### 3. Package.json Scripts
```bash
# Search in npm scripts
grep -E "worktree|wt:" package.json 2>/dev/null
```

#### 4. Composer Scripts
```bash
# Search in composer scripts
grep -E "worktree|wt:" composer.json 2>/dev/null
```

#### 5. Documentation
```bash
# Search for worktree documentation
grep -ri "worktree" README.md CONTRIBUTING.md docs/ .github/ 2>/dev/null | head -5
```

#### 6. Existing Worktrees
```bash
# Check if project already uses worktrees
git worktree list 2>/dev/null | wc -l
```

### Detection Result

```json
{
  "worktree_supported": true|false,
  "detection_method": "makefile|script|package.json|documentation|existing",
  "setup_command": "make worktree-new TICKET=xxx" | null,
  "details": "Found 'make worktree-setup' target in Makefile"
}
```

### Decision Logic

```
IF worktree tooling detected:
    → Offer worktree as option (with detected command)
    → Show: "Worktree disponible via: {setup_command}"

ELSE IF config.workspace.prefer_worktree == true:
    → Warn: "Worktree prefere mais aucun outil detecte"
    → Suggest: "Creez un target Makefile 'worktree-setup' pour activer"
    → Fallback to branch mode

ELSE:
    → Use branch mode (default)
    → Don't mention worktree option
```

---

## Branch Naming Convention

```
{prefix}/{ticket-id}-{slug}
```

### Components

1. **Prefix**: Derived from ticket type
   ```
   bug → fix
   feature → feat
   task → feat
   improvement → feat
   refactoring → refactor
   documentation → docs
   ```
   Configurable via `branches.prefix_mapping`

2. **Ticket ID**: Lowercase version of ticket identifier
   ```
   PROJ-123 → proj-123
   #456 → 456
   ```

3. **Slug**: Sanitized ticket title
   - Lowercase
   - Spaces → hyphens
   - Remove special characters
   - Truncate to `slug_max_length` (default: 50)

### Examples
```
feat/proj-123-add-user-authentication
fix/proj-456-null-pointer-in-login
refactor/proj-789-extract-validation-service
```

---

## Setup Process

### Step 0: Detect Worktree Capability

Run detection strategy above. Store result for later decision.

### Step 1: Determine Base Branch

Priority order:
1. Explicit argument (`--base-branch`)
2. Ticket metadata (if branch specified)
3. Project config (`branches.default_base`)
4. Fallback: `main`

### Step 2: Pre-flight Checks

```bash
# Check for uncommitted changes
git status --porcelain

# If changes exist and auto_stash enabled:
git stash push -m "auto-stash for {ticket-id}"
```

### Step 3: Update Base Branch

```bash
# Fetch latest from remote
git fetch origin

# If on base branch, pull
git pull origin {base-branch}
```

### Step 4: Create Workspace

#### Branch Mode (Default)
```bash
# Ensure we're on base branch
git checkout {base-branch}

# Create and switch to feature branch
git checkout -b {branch-name}
```

#### Worktree Mode (Only if tooling detected)

**Using detected project command**:
```bash
# Example with Makefile
make worktree-new TICKET={ticket-id} BRANCH={branch-name}

# Example with script
./scripts/create-worktree.sh {ticket-id} {branch-name}
```

**If no specific command but tooling exists**:
```bash
# Create worktree directory
mkdir -p {worktree_parent}

# Create worktree with new branch
git worktree add {worktree_parent}/{ticket-id} -b {branch-name} {base-branch}

# Warn user about manual setup needed
echo "⚠️  Worktree cree mais setup manuel requis:"
echo "   cd {worktree_parent}/{ticket-id}"
echo "   # Copier .env, docker-compose, etc."
```

### Step 5: Verify Setup

```bash
# Confirm branch creation
git branch --show-current

# Should output: {branch-name}
```

---

## Interactive Mode Questions

When in interactive mode, the questions depend on detection:

### If Worktree Tooling Detected

```
AskUserQuestion:
  question: "Comment creer l'espace de travail ?"
  header: "Workspace"
  options:
    - label: "Branche simple (Recommended)"
      description: "Creer une branche sur le repo actuel"
    - label: "Worktree isole"
      description: "Via: {detected_command} - repertoire separe"
```

### If No Worktree Tooling

Don't ask - use branch mode directly. Only mention:

```
Mode: Branche (worktree non disponible - aucun outil detecte)
```

---

## Error Handling

### Branch Already Exists
```
Branch '{branch-name}' already exists.

Options:
1. Switch to existing branch: git checkout {branch-name}
2. Delete and recreate: git branch -D {branch-name}
3. Use different name: {branch-name}-2

Recommended: Option 1 if resuming work on same ticket
```

### Uncommitted Changes
```
Uncommitted changes detected.

Options:
1. Stash changes (auto_stash enabled): Proceeding...
2. Commit changes first
3. Discard changes: git checkout .

Proceeding with auto-stash...
```

### Base Branch Not Found
```
Base branch '{base-branch}' not found locally.

Attempting to fetch from remote...
git fetch origin {base-branch}:{base-branch}
```

### Worktree Setup Failed
```
Worktree creation failed.

Cause probable: Setup incomplet (docker, .env, etc.)

Fallback: Utilisation du mode branche standard.
```

---

## Output Format

### Branch Mode
```markdown
## Workspace Setup

### Configuration
- **Mode**: Branch
- **Base Branch**: main (from config)
- **Feature Branch**: feat/proj-123-add-user-authentication

### Actions Taken
1. [x] Fetched latest from origin
2. [x] Checked out base branch: main
3. [x] Created feature branch: feat/proj-123-add-user-authentication
4. [x] Switched to feature branch

### Current State
On branch feat/proj-123-add-user-authentication
Your branch is up to date with 'origin/main'.

### Next Steps
- Ready for implementation
- Feature files will be stored in: .claude/feature/proj-123/
```

### Worktree Mode
```markdown
## Workspace Setup

### Configuration
- **Mode**: Worktree
- **Base Branch**: main
- **Feature Branch**: feat/proj-123-add-user-authentication
- **Worktree Path**: ../worktrees/proj-123

### Actions Taken
1. [x] Detected worktree tooling: make worktree-new
2. [x] Executed: make worktree-new TICKET=proj-123
3. [x] Worktree created at: ../worktrees/proj-123
4. [x] Environment setup completed

### Current State
Worktree ready at: ../worktrees/proj-123

### Next Steps
- cd ../worktrees/proj-123
- Ready for implementation
```

---

## Configuration

From `.claude/ticket-config.json`:

```json
{
  "workspace": {
    "prefer_worktree": false,
    "worktree_parent": "../worktrees",
    "auto_stash": true,
    "worktree_command": null
  },
  "branches": {
    "default_base": "main",
    "prefix_mapping": {
      "bug": "fix",
      "feature": "feat"
    },
    "include_ticket_id": true,
    "slug_max_length": 50
  }
}
```

### `workspace.worktree_command`
If set, this command will be used for worktree creation instead of auto-detection.
Example: `"make worktree TICKET={{ticket_id}}"`

---

## Example Makefile for Worktree Support

For projects wanting to enable worktree mode, here's an example Makefile:

```makefile
# Worktree management
WORKTREE_DIR ?= ../worktrees

.PHONY: worktree-new worktree-remove worktree-list

worktree-new: ## Create a new worktree for a ticket
ifndef TICKET
	$(error TICKET is required. Usage: make worktree-new TICKET=PROJ-123)
endif
	@echo "Creating worktree for $(TICKET)..."
	@mkdir -p $(WORKTREE_DIR)
	git worktree add $(WORKTREE_DIR)/$(TICKET) -b feat/$(TICKET)
	@# Copy environment files
	@cp -n .env.example $(WORKTREE_DIR)/$(TICKET)/.env 2>/dev/null || true
	@cp -n docker-compose.override.yml.dist $(WORKTREE_DIR)/$(TICKET)/docker-compose.override.yml 2>/dev/null || true
	@echo "Worktree ready at: $(WORKTREE_DIR)/$(TICKET)"
	@echo "Next: cd $(WORKTREE_DIR)/$(TICKET) && make install"

worktree-remove: ## Remove a worktree
ifndef TICKET
	$(error TICKET is required. Usage: make worktree-remove TICKET=PROJ-123)
endif
	git worktree remove $(WORKTREE_DIR)/$(TICKET) --force
	@echo "Worktree removed"

worktree-list: ## List all worktrees
	git worktree list
```

---

## Integration with Workflow

This skill is invoked by:
1. `/resolve` command - after analysis, before planning
2. Other workflows needing workspace setup

---

## Safety Rules

1. **Never work on main/master directly**
   - Always create feature branch
   - Refuse to proceed if target is protected branch

2. **Preserve uncommitted work**
   - Auto-stash if enabled
   - Warn user and ask if not

3. **Don't force-push or rewrite history**
   - Create new commits only
   - Preserve existing branch history

4. **Verify before destructive operations**
   - Confirm before deleting branches
   - Confirm before removing worktrees

---

## Branch Name Sanitization

```python
def sanitize_slug(title):
    # Lowercase
    slug = title.lower()
    # Replace spaces and underscores with hyphens
    slug = re.sub(r'[\s_]+', '-', slug)
    # Remove non-alphanumeric (except hyphens)
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    # Collapse multiple hyphens
    slug = re.sub(r'-+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    # Truncate
    slug = slug[:max_length]
    # Remove trailing hyphen after truncation
    slug = slug.rstrip('-')
    return slug
```

---

## Language

User-facing messages in French.
Git commands and branch names in English.
