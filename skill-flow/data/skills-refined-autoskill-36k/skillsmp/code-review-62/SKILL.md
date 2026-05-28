---
name: code-review
description: |
  코드 리뷰 스킬. Git 변경사항, PR, 특정 파일을 분석하여 품질/보안/성능 관점에서 리뷰를 제공합니다.
  사용 시기: (1) /review - 현재 staged/unstaged 변경사항 리뷰 (2) /review <file> - 특정 파일 리뷰
  (3) /review-pr <number> - GitHub PR 리뷰 (4) 코드 품질 검토 요청 시 (5) 보안 취약점 검토 요청 시 (project)
---

# Code Review Skill

## Quick Start

```bash
/review              # 현재 변경사항 리뷰
/review src/file.js  # 특정 파일 리뷰
/review-pr 123       # PR #123 리뷰
```

## Workflow

### 1. 변경사항 수집

```bash
# staged + unstaged 변경사항
git diff HEAD

# PR인 경우
gh pr view <number> --json files,commits,body
gh pr diff <number>
```

### 2. 리뷰 수행

각 변경사항에 대해 다음 관점으로 분석:

**필수 체크**
- [ ] 버그 가능성 (null 처리, 경계값, 예외 처리)
- [ ] 보안 취약점 (injection, XSS, 인증/인가)
- [ ] 성능 이슈 (N+1 쿼리, 불필요한 연산, 메모리 누수)

**권장 체크**
- [ ] 코드 가독성 (네이밍, 복잡도)
- [ ] 테스트 커버리지
- [ ] 기존 패턴과의 일관성

**프로젝트 규칙 확인**
- [ ] `.claude/rules/` 디렉토리의 프로젝트별 규칙 적용

### 3. 결과 출력 형식

```markdown
## Code Review Summary

### Critical Issues (Must Fix)
- 🔴 [보안] SQL Injection 위험: `UserRepository.js:45`
  - 문제: 사용자 입력이 직접 쿼리에 삽입됨
  - 해결: Parameterized query 사용

### Warnings (Should Fix)
- 🟡 [성능] N+1 쿼리 패턴: `OrderService.js:78`
  - 문제: 루프 내에서 개별 쿼리 실행
  - 해결: Batch 조회 또는 JOIN 사용

### Suggestions (Nice to Have)
- 🟢 [가독성] 함수 분리 권장: `PaymentController.js:120`
  - 이유: 함수가 50줄 이상으로 단일 책임 위반

### Positive Highlights
- ✨ 적절한 예외 처리
- ✨ 명확한 테스트 케이스 추가

### Statistics
- Files reviewed: 5
- Critical: 1 | Warnings: 2 | Suggestions: 3
```

상세 체크리스트: [references/checklist.md](references/checklist.md)
