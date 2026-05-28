---
description: GitHub Project 기반 프로젝트 관리 (이슈 추가, 상태 변경, PR 관리)
allowed-tools: Bash(gh:*), Bash(git:*), Read, Edit
argument-hint: <command> [args] (status | add | update | draft-pr | link-pr)
---

# Project Manager

GitHub Project를 SSOT로 사용하는 프로젝트 관리 도구.

입력: $ARGUMENTS

---

## 사전 준비

GitHub Project 번호 확인:
```bash
# 프로젝트 목록 조회
gh project list --owner @me

# 또는 organization의 프로젝트
gh project list --owner <org-name>
```

프로젝트 번호를 `PROJECT_NUMBER` 변수로 사용 (예: `1`)

---

## Command: status

**사용법**: `/manage-project status`

현재 프로젝트 상태를 요약해서 보여준다.

### 워크플로우

1. GitHub Project 아이템 조회:
   ```bash
   gh project item-list <PROJECT_NUMBER> --owner @me --format json
   ```

2. 상태별 분류:
   - In Progress: 현재 작업 중인 이슈
   - Backlog: 대기 중인 이슈
   - Done: 완료된 이슈

3. 현재 브랜치 정보:
   ```bash
   BRANCH=$(git branch --show-current)
   ISSUE_NUMBER=$(echo "$BRANCH" | grep -oE '^[0-9]+')
   gh pr view --json number,state,url 2>/dev/null || echo "PR 없음"
   ```

### 출력 형식

```text
## 현재 작업 중 (In Progress)
- #70 스트리밍 서버 구현 (P1)

## 대기 중 (Backlog 상위 5개)
- #71 비디오 플레이어 구현 (P1)
- #72 결제 연동 (P2)

## 현재 브랜치
- 브랜치: 70-스트리밍-서버-구현
- 연결된 이슈: #70
- PR 상태: Draft
```

---

## Command: add

**사용법**: `/manage-project add [이슈번호]`

기존 GitHub 이슈를 Project에 추가한다.

### 워크플로우

1. 이슈 존재 확인:
   ```bash
   gh issue view <이슈번호> --json number,title,url
   ```

2. Project에 이슈 추가:
   ```bash
   gh project item-add <PROJECT_NUMBER> --owner @me --url <이슈URL>
   ```

3. 추가 완료 메시지 출력

---

## Command: update

**사용법**: `/manage-project update [이슈번호] [상태]`

이슈 상태를 변경한다. GitHub Project의 Status 필드를 업데이트.

### 상태 값

- `in-progress`: 작업 시작
- `done`: 작업 완료
- `backlog`: 대기열로 이동

### 워크플로우

1. 이슈 정보 조회:
   ```bash
   gh issue view <번호> --json title,state,labels
   ```

2. Project 아이템 ID 조회:
   ```bash
   gh project item-list <PROJECT_NUMBER> --owner @me --format json | \
     jq '.items[] | select(.content.number == <이슈번호>)'
   ```

3. Status 필드 업데이트:
   ```bash
   gh project item-edit \
     --project-id <PROJECT_ID> \
     --id <ITEM_ID> \
     --field-id <STATUS_FIELD_ID> \
     --single-select-option-id <OPTION_ID>
   ```

### 필드 ID 조회 방법

```bash
# 프로젝트 필드 목록
gh project field-list <PROJECT_NUMBER> --owner @me --format json
```

---

## Command: draft-pr

**사용법**: `/manage-project draft-pr`

현재 브랜치에서 Draft PR을 생성한다.

### 워크플로우

1. 브랜치명에서 이슈 번호 추출:
   ```bash
   ISSUE_NUMBER=$(git branch --show-current | grep -oE '^[0-9]+')
   ```

2. 이슈 정보 조회:
   ```bash
   gh issue view $ISSUE_NUMBER --json title,body,labels
   ```

3. Draft PR 생성:
   ```bash
   gh pr create --draft --title "<이슈제목>" --body "$(cat <<'EOF'
   ## Summary
   - <변경사항 요약>

   ## Related Issue
   Resolves #<이슈번호>

   ## Test Plan
   - [ ] 테스트 항목

   ---
   🤖 Generated with Claude Code
   EOF
   )"
   ```

---

## Command: link-pr

**사용법**: `/manage-project link-pr`

현재 브랜치의 PR을 관련 이슈에 연결한다.

### 워크플로우

1. 현재 PR 정보 확인:
   ```bash
   gh pr view --json number,title,url
   ```

2. 브랜치명에서 이슈 번호 추출:
   ```bash
   ISSUE_NUMBER=$(git branch --show-current | grep -oE '^[0-9]+')
   ```

3. 이슈 본문에 PR 링크 추가:
   ```bash
   # 기존 본문 가져오기
   BODY=$(gh issue view $ISSUE_NUMBER --json body -q '.body')

   # PR 링크 섹션 추가
   NEW_BODY="${BODY}

   ---
   ## Related PRs
   - #<PR번호>"

   # 이슈 업데이트
   gh issue edit $ISSUE_NUMBER --body "$NEW_BODY"
   ```

---

## 참고: GitHub Project 구조

```text
Project (GitHub Projects v2)
├── Status (Single Select Field)
│   ├── Backlog
│   ├── In Progress
│   └── Done
├── Priority (Single Select Field)
│   ├── P0, P1, P2, P3, P4
└── Items (Issues/PRs)
```

### 유용한 명령어

```bash
# 프로젝트 상세 조회
gh project view <NUMBER> --owner @me

# 특정 상태의 아이템만 조회
gh project item-list <NUMBER> --owner @me --format json | \
  jq '.items[] | select(.status == "In Progress")'

# 이슈를 프로젝트에 추가
gh project item-add <NUMBER> --owner @me --url <ISSUE_URL>
```
