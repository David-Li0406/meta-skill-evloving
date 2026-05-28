---
name: git-branch-management
description: Manage Git branches with proper naming conventions and workflows
tags: [git, workflow, branches]
---

# Git Branch Management Skill

You are an expert in Git workflows, especially for creating, renaming, and managing branches following project conventions.

## Branch Naming Convention

For this project (11h.dev blog), all feature branches MUST follow this pattern:

```
claude/<descriptive-name>-<sessionID>
```

**Rules:**
- Always start with `claude/`
- Use kebab-case for the descriptive name
- End with the session ID (e.g., `-tL11U`)
- Keep descriptive name short but clear (2-4 words max)
- Use English for the descriptive name

**Examples:**
- ✅ `claude/effort-trap-article-tL11U`
- ✅ `claude/add-dark-mode-tL11U`
- ✅ `claude/fix-navbar-bug-tL11U`
- ❌ `claude/format-laziness-article-tL11U` (descriptive name doesn't match content)
- ❌ `feature/new-post` (wrong prefix)
- ❌ `claude/article` (missing session ID)

## When to Rename a Branch

Rename when:
1. **Content evolved significantly**: Started as "format article" but became "rewrite article"
2. **Language changed**: Branch named in French but content is English
3. **Scope changed**: Started as small fix, became major feature
4. **Clarity improved**: Generic name can be more specific

## How to Rename a Branch

### Option 1: Create New Branch (Recommended)
```bash
# Create new branch from current position
git checkout -b claude/new-name-<sessionID>

# Push new branch
git push -u origin claude/new-name-<sessionID>

# Optional: Delete old branch
git push origin --delete claude/old-name-<sessionID>
git branch -d claude/old-name-<sessionID>
```

**Pros:** Clean history, clear PR link
**Cons:** Creates duplicate branches temporarily

### Option 2: Rename Existing Branch
```bash
# Rename local branch
git branch -m claude/old-name-<sessionID> claude/new-name-<sessionID>

# Delete old remote branch
git push origin --delete claude/old-name-<sessionID>

# Push renamed branch
git push -u origin claude/new-name-<sessionID>
```

**Pros:** No duplicate branches
**Cons:** Breaks existing PR links

## Descriptive Name Guidelines

Match the branch name to the PRIMARY content/change:

| Content | Good Name | Bad Name |
|---------|-----------|----------|
| New article: "The Effort Trap" | `effort-trap-article` | `format-laziness-article` |
| French to English translation | `translate-to-english` | `update-post` |
| Add Jekyll config | `jekyll-config` | `update-config` |
| Fix navigation bug | `fix-navbar-bug` | `bug-fix` |

## Common Patterns

**For blog posts:**
- `<article-slug>-post-<sessionID>` for new articles
- `update-<article-slug>-<sessionID>` for major rewrites
- `translate-<article-slug>-<sessionID>` for translations

**For features:**
- `add-<feature-name>-<sessionID>`
- `implement-<feature-name>-<sessionID>`

**For fixes:**
- `fix-<issue-description>-<sessionID>`

**For refactoring:**
- `refactor-<component-name>-<sessionID>`

## Before Renaming Checklist

- [ ] Is the new name more accurate than the old one?
- [ ] Does it follow the `claude/<descriptive-name>-<sessionID>` pattern?
- [ ] Is the descriptive part clear and concise?
- [ ] Is it in English?
- [ ] Have I preserved the session ID?

## After Renaming

1. Update any local documentation
2. Update CLAUDE.md if branch name is referenced
3. Create PR from new branch name
4. Optionally delete old remote branch

---

When invoked, this skill will:
1. Analyze current branch name
2. Suggest better name if needed
3. Execute rename with proper commands
4. Verify successful push to remote
