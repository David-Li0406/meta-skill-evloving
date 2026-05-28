---
description: 계획서가 있는 이슈를 TDD 방식으로 해결
argument-hint: <issue-number>
---

# Issue Resolver

입력: $ARGUMENTS

## Phase 0: 사전 확인

1. 이슈 조회:
   ```bash
   gh issue view $ARGUMENTS --json title,body,state
   ```

2. 계획서 존재 확인:
   - body에 `## 1. 문제 정의` 또는 `## 2. 해결 방안` 섹션이 있는지 확인
   - 없으면 `/make-issue $ARGUMENTS`로 계획서 작성 안내 후 중단

---

## Phase 1: 계획서 파싱

이슈 body에서 다음 정보 추출:
- 작업 체크리스트 (`## 5. 작업 체크리스트`)
- 영향받는 파일 (`## 3. 영향받는 파일`)
- 테스트 케이스 (`## 4. 테스트 전략`)

---

## Phase 2: 작업 환경 준비

1. 작업 브랜치 생성:
   ```bash
   ISSUE_TITLE=$(gh issue view $ARGUMENTS --json title -q '.title')
   BRANCH_SUFFIX=$(echo "$ISSUE_TITLE" | sed 's/[^가-힣a-zA-Z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//' | cut -c1-50)
   git checkout -b "${ARGUMENTS}-${BRANCH_SUFFIX}"
   ```

---

## Phase 3: TDD 개발

`tdd-worker` sub-agent를 Task tool로 호출하여 개발 수행:

- 계획서 기반 RED-GREEN-REFACTOR 사이클 반복
- 커밋당 변경사항 100줄 이하 유지
- edge case 위주 테스트, approval case 1개 이상

---

## Phase 4: 브랜치 분리 처리

tdd-worker가 누적 800줄 초과를 보고하면:

1. `/manage-project draft-pr` 호출하여 현재 작업 PR 생성
2. `/manage-project link-pr` 호출하여 이슈에 PR 연결
3. 사용자에게 알림: "코드 리뷰 후 계속 진행하거나 `/pr-review-resolver`로 리뷰 처리"
4. 파이프라인 일시 중단

---

## Phase 5: 작업 완료

tdd-worker가 작업 완료를 보고하면:

1. `/manage-project draft-pr` 호출하여 Draft PR 생성
2. `/manage-project link-pr` 호출하여 이슈에 PR 연결
3. 사용자에게 self code review 안내

---

## 출력

각 Phase 완료시 진행 상황 요약:
- 완료된 작업
- 생성된 커밋/PR
- 다음 단계 안내
