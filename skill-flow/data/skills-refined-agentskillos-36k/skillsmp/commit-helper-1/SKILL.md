---
name: commit-helper
description: |
  커밋 메시지 생성 스킬. 다음 상황에서 자동 호출:
  - "커밋", "commit", "커밋 메시지", "커밋해줘", "커밋 부탁"
  - "변경사항 커밋", "staged 커밋", "git commit"
---

# Commit Message Generator

## Auto-trigger Keywords

commit, 커밋, 커밋해줘, 커밋 부탁, 커밋 메시지

## Instructions

| Tag Name         | Description                                                                                            |
| ---------------- | ------------------------------------------------------------------------------------------------------ |
| Feat             | Add new feature                                                                                        |
| Fix              | Fix bug                                                                                                |
| Design           | Change user UI design such as CSS                                                                      |
| !BREAKING CHANGE | Major API changes                                                                                      |
| !HOTFIX          | Urgent fix for critical bug                                                                            |
| Style            | Code format changes, missing semicolons, no code changes                                               |
| Refactor         | Refactor production code                                                                               |
| Comment          | Add or modify necessary comments                                                                       |
| Docs             | Modify documentation                                                                                   |
| Test             | Add test code, refactor test code, no Production Code changes                                          |
| Chore            | Modify build tasks, package manager, package manager configuration updates, no Production Code changes |
| Rename           | Only rename or move files or folders                                                                   |
| Remove           | Only delete files                                                                                      |

### 2: Analyze Changes

```bash
git diff --staged --stat
```

### 3: Determine if Body is Needed

**Include Body if** (any of the following):

- 3 or more files changed
- Can list specific changes (name changes, configuration changes, etc.)
- Need to explain reason for changes

**Use single line only**:

- Simple typo fix
- One clear change

### 4: Generate Message

**Single line format**:

```
{type}: {summary: 한글}
```

**Format with body**:

```
{type}: {summary: 한글}

- {specific change 1: 한글}
- {specific change 2: 한글}
```

## Examples

**Single line** (simple change):

```
fix: 로그인 버튼 이름 수정
```

**With body** (specific changes):

```
feat: 커밋 메세지 생성 스킬 개선

- Step 접두사 제거 (Step 1: → 1:)
- 프로젝트 특화 예시를 범용 예시로 교체
- Body 판단 기준 명확화
```

**With body** (name/structure changes):

```
Refactor: Ch 3 폴더 번호를 task.json과 일치시킴

- t08_conditionals_intent → t09_conditionals_intent
- t09_loops_batch → t10_loops_batch
- t10_exception_api_error → t11_exception_api_error
```

## Rules

- Summary within 50 characters
- Present tense ("add" not "added")
- Follow existing project style
