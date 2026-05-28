# Git Update Repository Workflow

**Purpose**: Safe and systematic git workflow for committing and pushing changes to Qara repositories with mandatory security checks.

---

## 🎯 Trigger Phrases

Invoke this workflow when Jean-Marc says:
- "update the Qara repo"
- "commit and push to Qara"
- "push to Qara repo"
- "push these changes"
- "commit these changes"
- "git push"

---

## 🚨 PRE-FLIGHT CHECKS (MANDATORY)

**STOP AND RUN THESE BEFORE ANYTHING ELSE**

### 1. Verify Repository Location
```bash
# Check current directory
pwd

# Verify git remote
git remote -v
```

**Expected outputs**:
- **Private Qara**: `github.com/[username]/.private-qara` or `github.com/[username]/qara` (if private)
- **Public PAI**: `github.com/[username]/qara` or similar (if public template)

**🚨 RED FLAG**: If you see a public remote from `~/.claude/` directory, **STOP IMMEDIATELY** and confirm with Jean-Marc.

### 2. Check Current Branch
```bash
git branch --show-current
```

Expected: `main` or `master` (or feature branch if working on one)

### 3. Verify No Sensitive Data
```bash
# Search for API keys (rg is 10-50x faster than grep)
rg "sk-|api_key.*=.*[a-zA-Z0-9]" --glob '!.git' --glob '!node_modules' 2>/dev/null

# Search for secrets/tokens
rg "SECRET|TOKEN|PASSWORD" --glob '!.git' --glob '!node_modules' --glob '!*.md' 2>/dev/null

# Search for email addresses (real ones, not examples)
rg "@" --glob '!.git' --glob '!node_modules' --glob '!*.md' 2>/dev/null | rg -v "example.com"
```

**If ANY matches found**: Review each one carefully. Ensure they're in gitignored files or are example values only.

---

## 📋 STANDARD WORKFLOW

### Step 1: Status Check
```bash
git status
```

**Review**:
- What files are modified?
- What files are untracked?
- Are any sensitive files showing up that should be gitignored?

### Step 2: Review Changes
```bash
# See detailed diff of all changes
git diff

# Or review specific file
git diff path/to/file
```

**Look for**:
- ❌ API keys, tokens, passwords
- ❌ Personal email addresses
- ❌ Business-specific information
- ❌ Hardcoded paths like `/home/jean-marc/specific-project/`
- ✅ Generic, sanitized content
- ✅ Proper use of placeholders

### Step 3: Stage Files

**Option A: Stage specific files** (recommended)
```bash
git add path/to/file1
git add path/to/file2
```

**Option B: Stage all changes** (use with caution)
```bash
git add .
```

**After staging, review what will be committed**:
```bash
git diff --cached
```

### Step 4: Commit with Descriptive Message
```bash
git commit -m "type: brief description"
```

**Commit Message Convention**:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation only
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks
- `perf:` Performance improvements
- `style:` Code style changes (formatting, etc.)

**Examples**:
```bash
git commit -m "feat: add security-protocols.md documentation"
git commit -m "fix: correct identity references in SKILL.md"
git commit -m "docs: update README with installation instructions"
git commit -m "refactor: reorganize workflow directory structure"
```

### Step 5: Verify Commit
```bash
# View last commit with file stats
git log -1 --stat

# View last commit with full diff
git log -1 -p
```

**Final check**:
- Commit message clear and descriptive?
- Files included are correct?
- No sensitive data in the diff?

### Step 6: Push to Remote
```bash
# Push current branch
git push origin $(git branch --show-current)

# Or if on main/master
git push origin main
# or
git push origin master
```

**After push**:
```bash
# Verify push succeeded
git status
```

Should show: "Your branch is up to date with 'origin/main'"

---

## 🛡️ SAFETY GATES

### Three-Check Rule
1. **Check #1**: When reviewing `git diff` (before staging)
2. **Check #2**: When reviewing `git diff --cached` (after staging)
3. **Check #3**: When reviewing `git log -1 -p` (after commit, before push)

**If ANY check fails, fix before proceeding.**

### Questions to Ask at Each Gate

**Before staging (git add)**:
- [ ] Are these the right files to commit?
- [ ] Have I reviewed all changes?
- [ ] Is any sensitive data visible?

**Before committing (git commit)**:
- [ ] Is the commit message clear?
- [ ] Are only intended files staged?
- [ ] Did I run `git diff --cached` to verify?

**Before pushing (git push)**:
- [ ] Is this the correct repository?
- [ ] Is this the correct branch?
- [ ] Have I verified the commit contents?
- [ ] Am I sure this is safe to push?

---

## 🔄 COMMON SCENARIOS

### Scenario 1: Committing Multiple Files
```bash
# 1. Check what changed
git status

# 2. Review all changes
git diff

# 3. Stage specific files
git add file1.md file2.ts file3.json

# 4. Verify staged changes
git diff --cached

# 5. Commit
git commit -m "feat: add multiple documentation files"

# 6. Verify and push
git log -1 --stat
git push origin main
```

### Scenario 2: Amending Last Commit
```bash
# If you forgot something in last commit (before pushing)
git add forgotten-file.md
git commit --amend --no-edit

# Or to change the commit message
git commit --amend -m "fix: corrected commit message"

# Then push (may need force if already pushed)
git push origin main --force-with-lease
```

### Scenario 3: Committing from Wrong Directory
```bash
# Oh no, I'm in the wrong repo!

# 1. Check where you are
pwd
git remote -v

# 2. Stash changes if needed
git stash

# 3. Navigate to correct repo
cd /correct/repo/path

# 4. Apply stashed changes (if stashing)
git stash pop

# 5. Proceed with normal workflow
```

### Scenario 4: Unstaging Files
```bash
# Unstage specific file
git reset HEAD file-to-unstage.md

# Unstage all files
git reset HEAD
```

### Scenario 5: Discarding Changes
```bash
# Discard changes in specific file (DANGEROUS - cannot undo)
git checkout -- file-to-discard.md

# Discard all uncommitted changes (VERY DANGEROUS)
git reset --hard HEAD
```

---

## 🚨 ROLLBACK PROCEDURES

### Undo Last Commit (Keep Changes)
```bash
# Reset to previous commit, keep changes staged
git reset --soft HEAD~1

# Now you can modify files and recommit
```

### Undo Last Commit (Discard Changes)
```bash
# DANGEROUS: This will delete your changes
git reset --hard HEAD~1
```

### Undo Last Push (VERY DANGEROUS)
```bash
# Only use if you pushed sensitive data and caught it immediately
git reset --hard HEAD~1
git push --force origin main

# Then follow security-protocols.md incident response
```

### Revert a Commit (Safe)
```bash
# Creates a new commit that undoes changes from specific commit
git revert <commit-hash>

# This is safer than reset when working with shared branches
```

---

## 📊 STATUS INDICATORS

### Clean Working Directory
```bash
$ git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```
✅ All changes committed and pushed

### Changes Not Staged
```bash
$ git status
On branch main
Changes not staged for commit:
  modified:   file.md
```
⚠️ Files modified but not staged (need `git add`)

### Changes Staged
```bash
$ git status
On branch main
Changes to be committed:
  modified:   file.md
```
⚠️ Files staged but not committed (need `git commit`)

### Commits Not Pushed
```bash
$ git status
On branch main
Your branch is ahead of 'origin/main' by 1 commit.
```
⚠️ Commits made but not pushed (need `git push`)

---

## 🔗 INTEGRATION WITH SECURITY PROTOCOLS

**Always consult** `security-protocols.md` for:
- Pre-commit security checklist (detailed version)
- Two repository strategy (private vs public)
- Prompt injection defense
- API key management
- Incident response procedures

**This workflow enforces**:
- Three-check rule from security-protocols.md
- Repository verification before commits
- Sensitive data scanning
- Safe rollback procedures

---

## 📝 QUICK REFERENCE CARD

```bash
# Standard workflow
git status              # Check status
git diff                # Review changes
git add <files>         # Stage files
git diff --cached       # Verify staged
git commit -m "msg"     # Commit
git log -1 --stat       # Verify commit
git push origin main    # Push

# Safety checks
pwd                     # Verify location
git remote -v           # Verify remote
rg "API_KEY"            # Check for secrets

# Rollback
git reset --soft HEAD~1 # Undo commit (keep changes)
git reset --hard HEAD~1 # Undo commit (discard changes)
git revert <hash>       # Safe undo (creates new commit)
```

---

## ❓ TROUBLESHOOTING

### "Permission denied (publickey)"
```bash
# Check SSH key is loaded
ssh-add -l

# Add SSH key if needed
ssh-add ~/.ssh/id_ed25519
```

### "Merge conflict"
```bash
# See conflicted files
git status

# Edit files to resolve conflicts (look for <<< === >>> markers)
# Then:
git add <resolved-files>
git commit -m "fix: resolve merge conflicts"
```

### "Diverged branches"
```bash
# Pull remote changes first
git pull origin main

# Resolve conflicts if any
# Then push
git push origin main
```

### "Nothing to commit"
- All changes already committed
- Check `git status` to confirm
- Maybe you meant to modify different files?

---

**Remember**: It takes 3 seconds to verify, but hours to fix a leaked API key. Always run the pre-flight checks.

**When in doubt, DON'T push. Ask Jean-Marc first.**
