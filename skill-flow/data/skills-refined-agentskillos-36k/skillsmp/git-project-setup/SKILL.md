---
name: git-project-setup
description: Proper git setup and hygiene for new projects. Handles .gitignore creation, staging verification, commit messages, and avoiding common pitfalls like committing build artifacts. Use when starting a new project or when git operations need careful attention.
---

# Git Project Setup and Hygiene Skill

Ensure proper version control setup and avoid common git mistakes when setting up new projects or managing changes.

## Core Principles

**Critical Rules:**
- Create `.gitignore` BEFORE generating any build artifacts
- Always verify what's staged before committing
- Never commit build artifacts, IDE files, or user-specific configs
- Use descriptive, well-formatted commit messages
- Clean up artifacts before git operations

## Workflow

Make a todo list for all the tasks in this workflow and work on them one after another.

### 1. Create .gitignore First

**CRITICAL: Do this as the FIRST step in any new project**

Create `.gitignore` appropriate for the project type before running ANY build commands.

**Why this matters:**
- Running build tools before `.gitignore` exists creates artifacts
- `git add -A` will stage all those artifacts
- Requires cleanup and reset to fix
- Prevention is easier than cleanup

**Common patterns to exclude:**

```gitignore
# Build outputs (adapt to your language)
/target/          # Rust
/dist/            # JavaScript
/build/           # Many languages
*.pyc             # Python
__pycache__/      # Python
*.class           # Java
bin/              # C#/Java
obj/              # C#

# Dependencies
node_modules/     # JavaScript
vendor/           # Go/PHP
.bundle/          # Ruby

# IDE and Editor files
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# User-specific configs (keep .example versions)
config.toml
.env
*.local.json

# Logs and databases
*.log
*.sqlite
*.db
```

### 2. Initialize Repository (if needed)

If starting fresh:

```bash
git init
git add .gitignore
git commit -m "Initial commit with .gitignore"
```

If joining existing repo:
```bash
git checkout -b <your-branch-name>
# Verify .gitignore exists and is comprehensive
```

### 3. Stage Changes Carefully

**NEVER blindly run `git add -A` without verification**

**Safe staging workflow:**

```bash
# See what would be staged
git status

# If anything unexpected appears (build artifacts, IDE files):
# 1. Add them to .gitignore
# 2. Run git status again to verify they're ignored
```

**Selective staging:**
```bash
# Stage specific directories
git add src/ docs/ config.example.json

# Or stage by pattern
git add *.md Cargo.toml package.json
```

### 4. Pre-Commit Verification

**CRITICAL CHECKS before every commit:**

Run this verification:
```bash
git status
```

**What you SHOULD see staged:**
- ✅ Source code files
- ✅ Configuration files (package.json, Cargo.toml, pyproject.toml, etc.)
- ✅ Lock files (Cargo.lock for apps, package-lock.json, etc.)
- ✅ Documentation (README.md, docs/, etc.)
- ✅ Example/template config files (config.example.json, .env.example)
- ✅ Project metadata files
- ✅ `.gitignore` itself

**What you should NOT see staged:**
- ❌ Build output directories (target/, dist/, build/, bin/, obj/)
- ❌ Compiled artifacts (*.o, *.so, *.dll, *.exe, *.rlib)
- ❌ Dependency directories (node_modules/, vendor/, .bundle/)
- ❌ IDE/editor files (.vscode/, .idea/, *.swp)
- ❌ OS files (.DS_Store, Thumbs.db)
- ❌ User-specific configs (actual config.toml, .env)
- ❌ Log files (*.log)
- ❌ Temporary files (*.tmp, *.cache)

**If you see unexpected files staged:**

```bash
# Unstage everything
git reset

# Fix .gitignore to exclude the unwanted files
echo "unwanted-pattern/" >> .gitignore

# Stage only what you want
git add src/ README.md Cargo.toml .gitignore

# Verify
git status
```

### 5. Recovery from Common Mistakes

#### Mistake 1: Build Artifacts Already Staged

**Symptoms:** `git status` shows `target/`, `node_modules/`, `dist/`, etc.

**Recovery:**
```bash
# Unstage everything
git reset

# Clean build artifacts
rm -rf target/        # Rust
# OR
rm -rf node_modules/  # JavaScript
# OR
rm -rf build/ dist/   # General

# Ensure .gitignore is correct
cat .gitignore  # Verify patterns are there

# Re-stage properly
git add .gitignore src/ Cargo.toml README.md

# Verify clean staging
git status
```

#### Mistake 2: IDE Files in Staging

**Symptoms:** `.vscode/`, `.idea/`, `*.swp` appear in `git status`

**Recovery:**
```bash
git reset

# Add to .gitignore
cat >> .gitignore << 'EOF'
.vscode/
.idea/
*.swp
*.swo
*~
EOF

# Re-stage without IDE files
git add -A
git status  # Verify they're gone
```

#### Mistake 3: User Config Committed

**Symptoms:** Actual `config.toml` or `.env` staged (not the `.example` version)

**Recovery:**
```bash
git reset

# Add to .gitignore
echo "config.toml" >> .gitignore
echo ".env" >> .gitignore

# If already committed in history
git rm --cached config.toml .env

# Stage properly
git add -A
```

### 6. Write Descriptive Commit Messages

Use clear, well-structured commit messages:

```bash
git commit -m "$(cat <<'EOF'
Brief summary of changes (50 chars or less)

More detailed explanation of what changed and why. Wrap at 72 characters.
Focus on the "why" and "what", not the "how" (code shows the how).

Key changes:
- Change 1: brief description
- Change 2: brief description
- Change 3: brief description

Implementation details:
- Detail 1
- Detail 2

Notes: Any special considerations, dependencies, or follow-up needed.
EOF
)"
```

**Commit message guidelines:**
- First line: imperative mood ("Add feature" not "Added feature")
- Keep first line under 50 characters
- Blank line after first line
- Wrap body at 72 characters
- Use bullet points for clarity
- Explain WHY, not just WHAT

### 7. Push Changes

```bash
# First time pushing a branch
git push -u origin <branch-name>

# Subsequent pushes
git push
```

**Handle push failures:**

If push fails with 403 or permission error:
- Verify branch name matches required pattern (e.g., must start with `claude/`)
- Check you have write access
- Verify remote URL is correct

If push fails with network error:
- Retry with exponential backoff (wait 2s, 4s, 8s, 16s)
- Check network connectivity

```bash
# Retry logic
git push -u origin <branch> || \
  (sleep 2 && git push -u origin <branch>) || \
  (sleep 4 && git push -u origin <branch>) || \
  (sleep 8 && git push -u origin <branch>)
```

### 8. Branch Naming Conventions

Follow project-specific branch naming requirements:

**Common patterns:**
- `feature/<description>` - New features
- `fix/<description>` - Bug fixes
- `docs/<description>` - Documentation
- `claude/<session-id>` - Claude Code sessions
- `refactor/<description>` - Code refactoring

**Verify branch name requirements before pushing!**

## Pre-Flight Checklist

Before ANY commit, verify:

- [ ] `.gitignore` exists and is comprehensive
- [ ] `git status` shows no unexpected files
- [ ] No build artifacts staged
- [ ] No IDE/editor files staged
- [ ] No user-specific configs staged (only `.example` versions)
- [ ] Lock files included (if appropriate for project type)
- [ ] Commit message is descriptive
- [ ] Branch name follows conventions

## Common Gotchas

### Gotcha 1: "But I already ran the build!"

**Problem:** Created build artifacts before `.gitignore`

**Solution:** Clean, create `.gitignore`, re-stage
```bash
git reset
make clean  # or cargo clean, npm run clean, etc.
echo "/target/" >> .gitignore  # Add build dirs
git add -A
git status  # Verify clean
```

### Gotcha 2: "Git status shows 200+ files"

**Problem:** Missing or incomplete `.gitignore`

**Solution:** This is a RED FLAG - stop and fix `.gitignore` first
```bash
git reset
# Identify what shouldn't be there
git status | grep -E "(node_modules|target|\.pyc|\.class)"
# Add patterns to .gitignore
# Re-stage
```

### Gotcha 3: "Accidentally committed secrets"

**Problem:** Committed `.env` or config with API keys

**Solution:**
```bash
# If not pushed yet
git reset HEAD~1
git rm --cached .env
echo ".env" >> .gitignore
git add -A
git commit -m "Remove secrets, add to gitignore"

# If already pushed - ALERT THE USER to rotate secrets!
```

### Gotcha 4: Lock file questions

**When to commit lock files:**

| File | Type | Commit? |
|------|------|---------|
| `Cargo.lock` | Application | ✅ YES |
| `Cargo.lock` | Library | ❌ NO |
| `package-lock.json` | Any | ✅ YES |
| `yarn.lock` | Any | ✅ YES |
| `Pipfile.lock` | Any | ✅ YES |
| `composer.lock` | Any | ✅ YES |
| `go.sum` | Any | ✅ YES |

## Wrap Up

After completing git setup and committing:

**Git Status: ✅ Clean**

**What's committed:**
- Source files: [list key directories]
- Configuration: [list config files]
- Documentation: [list docs]
- Lock files: [if applicable]

**What's excluded:**
- Build artifacts: [patterns in .gitignore]
- IDE files: [patterns in .gitignore]
- User configs: [patterns in .gitignore]

**Branch:** `<branch-name>`
**Push status:** ✅ Pushed to remote

**Verification:**
```bash
git status
# Should show: "nothing to commit, working tree clean"

git log --oneline -1
# Shows your commit message
```

All clean and ready for the next step!
