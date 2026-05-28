---
name: create-pr
description: Skill for pushing branch and creating pull requests with proper target branch detection and draft support.
---

# Create PR Skill

This skill handles the finalization phase of ticket resolution: pushing the branch and creating a pull request.

## Capabilities

1. **Push to remote** with upstream tracking
2. **Detect target branch** from multiple sources
3. **Create PR** with auto-generated title and body
4. **Draft mode** support (when available)
5. **Idempotent** - skip if PR already exists

---

## Target Branch Detection

Priority order for determining the PR target branch:

### 1. Explicit Argument
```bash
--base main
```

### 2. Status File (from worktree creation)
Read from `.claude/feature/{ticket-id}/status.json`:
```json
{
  "options": {
    "base_branch": "develop"
  }
}
```

This is set by `resolve-worktree.sh` when creating the worktree, preserving the original base branch.

### 3. Ticket Metadata
Some tickets specify target branch:
- YouTrack: custom field "Target Branch" or "Fix versions", or parsed from Milestone
- GitHub: base branch in linked PR

Check in ticket.md or analysis.md for:
```markdown
Target Branch: develop
Fix Version: release/2.0
```

### 4. Branch Pattern Matching
Detect from current branch name:
```
hotfix/* → main (or master)
release/* → main
feature/* → develop (if exists) or main
fix/* → develop (if exists) or main
```

### 5. Project Configuration
From `.claude/ticket-config.json`:
```json
{
  "pr": {
    "default_target": "main"
  }
}
```

### 6. Git Default Branch
```bash
git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@'
```

### 7. Fallback
Try in order: `main`, `master`, `develop`

---

## PR Title Generation

Format: `{type}: {ticket_title} ({ticket_id})`

Examples:
```
feat: Add CSV export for users (PROJ-123)
fix: Null pointer in login flow (PROJ-456)
refactor: Extract validation service (PROJ-789)
```

### Type Detection
From branch prefix:
- `feat/` → `feat`
- `fix/` → `fix`
- `refactor/` → `refactor`
- `docs/` → `docs`
- `chore/` → `chore`

---

## PR Body Generation

Template:
```markdown
## Summary

{Brief description from ticket or plan}

## Ticket

- **ID**: {ticket_id}
- **Source**: {YouTrack|GitHub}
- **Link**: {ticket_url}

## Changes

{List of main changes from plan phases}

## Test Plan

{Validation steps from plan}

---
*Created via `/resolve` workflow*
```

### Customization
From config:
```json
{
  "pr": {
    "body_template": "custom template with {{ticket_id}} placeholders",
    "include_ticket_link": true,
    "include_test_plan": true
  }
}
```

---

## Draft Mode

### Detection
Check if repository supports draft PRs:
```bash
# GitHub - always supports drafts
gh pr create --draft ...

# GitLab - check version
# Bitbucket - check settings
```

### Configuration
```json
{
  "pr": {
    "draft_by_default": true
  }
}
```

### Behavior
| Mode | draft_by_default | Result |
|------|------------------|--------|
| Auto | true | Create as draft |
| Auto | false | Create as ready |
| Interactive | - | Ask user |

---

## Process

### Step 1: Pre-flight Checks

```bash
# Check if on feature branch (not main/master)
CURRENT_BRANCH=$(git branch --show-current)
if [[ "$CURRENT_BRANCH" =~ ^(main|master|develop)$ ]]; then
    echo "Error: Cannot create PR from protected branch"
    exit 1
fi

# Check for uncommitted changes
if [[ -n $(git status --porcelain) ]]; then
    echo "Warning: Uncommitted changes detected"
    # In interactive: ask to commit or stash
    # In auto: fail or stash
fi

# Check if remote exists
git remote get-url origin || exit 1
```

### Step 2: Push Branch

```bash
# Push with upstream tracking
git push -u origin "$CURRENT_BRANCH"
```

If push fails:
- Check authentication
- Check branch protection rules
- Suggest `git pull --rebase` if behind

### Step 3: Check Existing PR

```bash
# Check if PR already exists for this branch
EXISTING_PR=$(gh pr view "$CURRENT_BRANCH" --json number,url 2>/dev/null)

if [[ -n "$EXISTING_PR" ]]; then
    PR_URL=$(echo "$EXISTING_PR" | jq -r '.url')
    echo "PR already exists: $PR_URL"
    # Option: update existing PR description
    exit 0
fi
```

### Step 4: Determine Target Branch

Apply detection priority (see above).

```bash
# Verify target branch exists
git ls-remote --heads origin "$TARGET_BRANCH" || {
    echo "Error: Target branch '$TARGET_BRANCH' not found"
    # Suggest alternatives
}
```

### Step 5: Generate PR Content

Read from feature directory:
```bash
FEATURE_DIR=".claude/feature/$TICKET_ID"
TICKET_FILE="$FEATURE_DIR/ticket.md"
PLAN_FILE="$FEATURE_DIR/plan.md"
```

Extract:
- Title from ticket
- Summary from plan
- Changes from plan phases
- Validation from plan

### Step 6: Create PR

```bash
# Draft mode
DRAFT_FLAG=""
if [[ "$DRAFT" == "true" ]]; then
    DRAFT_FLAG="--draft"
fi

# Create PR
gh pr create \
    --title "$PR_TITLE" \
    --body "$PR_BODY" \
    --base "$TARGET_BRANCH" \
    $DRAFT_FLAG
```

### Step 7: Update Status

Update `.claude/feature/{ticket-id}/status.json`:
```json
{
  "phases": {
    "finalize": "completed"
  },
  "pr": {
    "number": 123,
    "url": "https://github.com/owner/repo/pull/123",
    "draft": true,
    "target": "main"
  }
}
```

---

## Interactive Mode Questions

### Question 1: Push Confirmation
```
AskUserQuestion:
  question: "Pousser la branche et creer une PR ?"
  header: "Finalisation"
  options:
    - label: "Oui, push + PR"
      description: "Pousser la branche et creer la pull request"
    - label: "Push seulement"
      description: "Pousser sans creer de PR"
    - label: "Non, plus tard"
      description: "Terminer sans push"
```

### Question 2: Draft Mode (if creating PR)
```
AskUserQuestion:
  question: "Creer la PR en mode draft ?"
  header: "Draft"
  options:
    - label: "Oui, draft (Recommended)"
      description: "PR en brouillon, a marquer ready apres review"
    - label: "Non, ready for review"
      description: "PR prete pour review immediate"
```

### Question 3: Target Branch (if ambiguous)
```
AskUserQuestion:
  question: "Quelle branche cible pour la PR ?"
  header: "Target"
  options:
    - label: "main (Recommended)"
      description: "Branche principale"
    - label: "develop"
      description: "Branche de developpement"
    - label: "{ticket_target}"
      description: "Specifie dans le ticket"
```

---

## Error Handling

### Push Failed - Authentication
```
Erreur: Authentification echouee

Solutions:
1. Verifiez vos credentials git
2. Pour HTTPS: gh auth login
3. Pour SSH: ssh-add ~/.ssh/id_rsa
```

### Push Failed - Branch Protection
```
Erreur: Push refuse par protection de branche

La branche '{branch}' a des regles de protection.
Verifiez les settings du repository.
```

### PR Creation Failed - No Permission
```
Erreur: Impossible de creer la PR

Verifiez que vous avez les droits sur le repository.
Tentez: gh auth refresh
```

### Target Branch Not Found
```
Erreur: Branche cible '{branch}' introuvable

Branches disponibles:
- main
- develop
- release/2.0

Utilisez --base pour specifier la cible.
```

---

## Configuration Reference

Full PR configuration in `.claude/ticket-config.json`:

```json
{
  "pr": {
    "draft_by_default": true,
    "default_target": "main",
    "include_ticket_link": true,
    "include_test_plan": true,
    "auto_push": true,
    "title_format": "{type}: {title} ({ticket_id})",
    "body_template": null
  }
}
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `draft_by_default` | `true` | Create PRs as draft |
| `default_target` | `"main"` | Fallback target branch |
| `include_ticket_link` | `true` | Add ticket link in body |
| `include_test_plan` | `true` | Add validation steps |
| `auto_push` | `true` | Push before creating PR |
| `title_format` | `"{type}: {title} ({ticket_id})"` | PR title template |
| `body_template` | `null` | Custom body template |

---

## Output Format

### Success
```markdown
## PR Created

- **Branch**: feat/proj-123-add-csv-export
- **Target**: main
- **PR**: #456
- **URL**: https://github.com/owner/repo/pull/456
- **Status**: Draft

### Next Steps
1. Review the changes
2. Request reviews
3. Mark as ready when done
```

### Already Exists
```markdown
## PR Already Exists

- **PR**: #456
- **URL**: https://github.com/owner/repo/pull/456
- **Status**: Open

No action needed.
```

---

## Integration with /resolve

This skill is invoked at the end of the `/resolve` workflow:

```
/resolve PROJ-123
    │
    ├─► ... existing phases ...
    ├─► Implementation
    │
    └─► Finalize (this skill)
        ├─► Push branch
        └─► Create PR
```

### Auto Mode
- Always push
- Always create PR (if not exists)
- Use `draft_by_default` setting

### Interactive Mode
- Ask about push + PR
- Ask about draft mode
- Ask about target branch (if ambiguous)

---

## Language

User-facing messages in French.
Git commands and PR content in English.

