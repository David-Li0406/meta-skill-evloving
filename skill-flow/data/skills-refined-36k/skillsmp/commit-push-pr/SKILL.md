---
name: commit-push-pr
description: Git 커밋, Push, PR 생성 워크플로우를 표준화하는 스킬
allowed-tools:
  - Bash
  - Read
  - Grep
---

# Commit Push PR Skill

이 스킬은 ForkLore 프로젝트의 Git 워크플로우를 표준화합니다.

## 워크플로우

### 1. 커밋 전 준비

```bash
# 변경사항 확인
git status --short
git diff --stat

# 린트 및 테스트 실행
cd backend && poetry run ruff check apps/ && poetry run pytest -x
cd frontend && pnpm lint && pnpm test -- --run
```

### 2. 커밋 메시지 규칙

**형식**: `type(scope): message`

| Type | 설명 |
|------|------|
| `feat` | 새로운 기능 |
| `fix` | 버그 수정 |
| `refactor` | 코드 리팩토링 (기능 변경 없음) |
| `docs` | 문서 변경 |
| `test` | 테스트 추가/수정 |
| `chore` | 빌드, 설정 등 기타 변경 |

**예시**:
```bash
git commit -m "feat(novels): add chapter reordering API"
git commit -m "fix(auth): resolve token refresh race condition"
git commit -m "refactor(contents): extract text processing to service"
git commit -m "docs(api): update endpoint documentation"
git commit -m "test(novels): add integration tests for branching"
```

### 3. 브랜치 명명 규칙

**형식**: `type/#issue-description`

```bash
# 예시
feat/#123-novel-branching
fix/#456-auth-token-refresh
refactor/#789-service-extraction
docs/#101-api-documentation
```

### 4. Push

```bash
# 새 브랜치 첫 push
git push -u origin feat/#123-feature-name

# 이후 push
git push
```

### 5. PR 생성

```bash
gh pr create --title "feat(scope): 설명 (#이슈번호)" --body "$(cat <<'EOF'
## Summary
- 변경사항 1
- 변경사항 2

## Changes
- 파일 1: 설명
- 파일 2: 설명

## Test
- [ ] 단위 테스트 통과
- [ ] 통합 테스트 통과
- [ ] 수동 테스트 완료

Closes #이슈번호
EOF
)" --base develop
```

### 6. PR 머지

```bash
# Squash 머지 (권장)
gh pr merge {PR_NUMBER} --squash --delete-branch

# 일반 머지
gh pr merge {PR_NUMBER} --merge --delete-branch
```

## 전체 워크플로우 예시

```bash
# 1. develop에서 새 브랜치 생성
git checkout develop
git pull origin develop
git checkout -b feat/#204-mcp-skills-hooks

# 2. 작업 수행
# ... 코드 작성 ...

# 3. 변경사항 확인 및 테스트
git status --short
cd backend && poetry run pytest -x
cd frontend && pnpm test -- --run

# 4. 커밋
git add .
git commit -m "feat(claude): add MCP, Skills, Hooks configuration

- Add .mcp.json for PostgreSQL and Playwright
- Add 5 skills for development workflow
- Add 4 hooks for code quality enforcement

Closes #204"

# 5. Push
git push -u origin feat/#204-mcp-skills-hooks

# 6. PR 생성
gh pr create --title "feat(claude): MCP, Skills, Hooks 설정 (#204)" \
  --body "## Summary
- MCP 서버 설정 (PostgreSQL, Playwright)
- Skills 5개 생성 (TDD, PR Review, API, Frontend, Git)
- Hooks 4개 설정 (Lint, Test, Bash)

Closes #204" --base develop

# 7. PR 머지
gh pr merge --squash --delete-branch
```

## 금지 사항

| 명령어 | 사유 |
|--------|------|
| `git push -f` (main/develop) | 히스토리 손상 |
| `git commit --amend` (push 후) | 협업 충돌 |
| `git reset --hard` (공유 브랜치) | 다른 작업자 영향 |

## 체크리스트

- [ ] 브랜치가 이슈 번호를 포함하는가?
- [ ] 커밋 메시지가 규칙을 따르는가?
- [ ] 테스트가 통과하는가?
- [ ] PR이 `Closes #이슈번호`를 포함하는가?
- [ ] base 브랜치가 `develop`인가?
