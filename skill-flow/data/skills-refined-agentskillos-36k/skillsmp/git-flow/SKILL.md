---
name: git-flow
description: Git workflow automation for commits, cherry-picks, branch comparison, and rebasing. Use when user mentions commit, cherry-pick, branch diff, or git operations like "커밋해줘", "체리픽", "브랜치 비교".
---

# Git Flow

Automate common Git workflows based on user patterns.

## Trigger Patterns

- `/git-flow` command
- Keywords: "커밋", "체리픽", "브랜치 비교", "리베이스"
- Requests: "변경사항을 커밋해줘", "커밋 메시지는 ~"

## Operations

### 1. Smart Commit

**Trigger**: "커밋해줘", "변경사항을 커밋"

**Workflow**:
```bash
# 1. Check status
git status

# 2. Show diff summary
git diff --stat

# 3. Stage and commit
git add <files>
git commit -m "<message>"
```

**Options**:
- Split commits: "커밋을 쪼개서" → use `git add -p` to stage by hunk/line

**Commit Message Format**:
- 프리픽스 없이 간결하게 작성
- 변경 내용을 명확히 설명

예시: "throttle 호출 순서 변경"

### 2. Split Commits (Line/Chunk Level)

**Trigger**: "커밋을 쪼개서", "청크별로 커밋", "라인 단위로 커밋"

**Workflow**:
```bash
# 1. Show diff to understand changes
git diff

# 2. Use patch mode to stage specific hunks/lines
git add -p <file>
# Interactive options:
# y - stage this hunk
# n - skip this hunk
# s - split into smaller hunks
# e - manually edit the hunk

# 3. Verify staged changes
git diff --cached

# 4. Commit the staged hunks
git commit -m "<description>"

# 5. Repeat for remaining changes
```

**Key Point**: 파일 단위가 아닌 **라인/청크(hunk) 단위**로 커밋하여 논리적으로 관련된 변경사항만 묶어서 커밋

### 3. Cherry-Pick Range

**Trigger**: "체리픽 해오고 싶어", "~ 부터 ~ 까지"

**Workflow**:
```bash
# 1. Show commits in range
git log --oneline <start>..<end>

# 2. Cherry-pick range
git cherry-pick <start>^..<end>

# Or one by one with message modification
git cherry-pick <hash> --edit
```

**With Message Modification**:
```bash
# Replace pattern in commit messages
git cherry-pick <hash>
git commit --amend -m "$(git log -1 --format='%B' | sed 's/OLD/NEW/g')"
```

### 4. Branch Comparison

**Trigger**: "브랜치 비교", "차이가 얼마나"

**Workflow**:
```bash
# Line count diff
git diff --stat origin/develop..HEAD | tail -1

# File list
git diff --name-only origin/develop..HEAD

# Commit count
git rev-list --count origin/develop..HEAD
```

**Output Format**:
```markdown
## Branch Comparison: current vs origin/develop

- **Commits**: {n} commits ahead
- **Files Changed**: {n} files
- **Lines**: +{added} / -{removed}

### Changed Files:
- file1.swift
- file2.swift
```

### 5. Interactive Rebase Helper

**Trigger**: "커밋 메시지 수정", "NEWMU-1081 을 1100 으로"

**Workflow**:
```bash
# Find commits to modify
git log --oneline -n 10

# Rebase with message filter
git filter-branch --msg-filter 'sed "s/PATTERN/REPLACEMENT/g"' HEAD~N..HEAD
```

**Safer Alternative**:
```bash
# Reword commits one by one
git rebase -i HEAD~N
# Then edit commit messages manually
```

## Quick Commands

| User Says | Action |
|-----------|--------|
| "git status" | Run `git status` |
| "git push" | Run `git push` |
| "!git push" | Run `git push` immediately |

## Important Rules (MUST FOLLOW)

- **Co-Authored-By 절대 금지**: 커밋 메시지에 `Co-Authored-By` 라인을 절대 추가하지 말 것
- 커밋 메시지는 순수하게 변경 내용만 기술

## Safety Rules

- Never force push without explicit request
- Always show diff before committing
- Ask before rewriting history
- Warn about uncommitted changes before checkout

## Examples

### Example 1: Simple Commit
```
User: 변경사항을 커밋해줘. 커밋 메시지는 "throttle 호출 순서 변경."
```
→ Stage all, commit with message

### Example 2: Split Commit (Line/Chunk)
```
User: 이 파일에서 버그 수정한 부분만 먼저 커밋해줘
```
→ Use `git add -p` to stage only the bug fix hunks, then commit

### Example 3: Cherry-Pick with Modification
```
User: e83fb2a 부터 2eee28f 까지 체리픽하고, 1081 을 1100 으로 바꿔줘
```
→ Cherry-pick range, modify commit messages

### Example 4: Branch Diff
```
User: 현재 브랜치랑 origin/develop 이랑 라인 수 차이
```
→ Show line count comparison

## Notes

- Use HEREDOC for multi-line commit messages
- Always verify before destructive operations
