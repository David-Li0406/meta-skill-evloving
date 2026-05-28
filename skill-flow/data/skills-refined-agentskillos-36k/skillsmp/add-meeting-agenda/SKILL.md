---
name: add-meeting-agenda
description: |
  회의록에 안건 추가. 자연어로 요청하여 GitHub Discussion 회의록에 안건을 추가합니다.
  Use when (1) "회의록에 안건 추가해줘", (2) "이번 주 회의에서 논의할 내용 추가",
  (3) "회의 안건으로 OOO 넣어줘", (4) 회의 안건 등록 요청.
tools: [Bash, Read]
model: inherit
---

> **시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: add-meeting-agenda 호출` 시스템 메시지를 첫 줄에 출력하세요.

# add-meeting-agenda Skill

> 자연어로 회의 안건을 추가하는 스킬

## Purpose

GitHub Discussion (command-center repository)의 Meeting-Minutes에 **자연어로 요청받은 안건을 추가**합니다. 가장 최근 회의록에 자동으로 추가하거나, 특정 Discussion 번호를 지정할 수 있습니다.

## NON-NEGOTIABLE RULES

### 대상 Repository

| 항목 | 값 |
|------|-----|
| Owner | `semicolon-devteam` |
| Repository | `command-center` |
| Category | `Meeting-Minutes` |

### 안건 추가 위치

회의록 본문의 `### 📝 회의 안건` 섹션 내에 새 항목을 추가합니다.

```markdown
### 📝 회의 안건

#### 이터레이션 리뷰
- [ ] 기존 안건 1
- [ ] 기존 안건 2

#### 추가 안건  ← 여기에 추가됨
- [ ] 새로 추가된 안건
```

## Execution Flow

```text
1. 사용자 요청에서 안건 내용 추출
   ↓
2. 대상 Discussion 결정
   - 번호 지정 시: 해당 Discussion 사용
   - 미지정 시: 가장 최근 Meeting-Minutes Discussion 조회
   ↓
3. 기존 Discussion body 조회
   ↓
4. 안건 섹션에 새 항목 추가
   ↓
5. Discussion body 업데이트 (gh api graphql)
   ↓
6. 완료 메시지 반환
```

## 사용 예시

### 기본 사용 (최근 회의록에 추가)

```bash
"이번 주 회의에서 신규 기능 배포 일정 논의해야 해"

# 출력:
[SEMO] Skill: add-meeting-agenda 호출

안건 추출: "신규 기능 배포 일정 논의"

최근 회의록 조회 중...
- 대상: [1월 3/5] 정기 회고 & 회의 (#211)

안건 추가 중...
✅ 안건 추가 완료

**추가된 안건**: 신규 기능 배포 일정 논의
**회의록**: https://github.com/semicolon-devteam/command-center/discussions/211
```

### 특정 Discussion 지정

```bash
"#210 회의록에 QA 테스트 결과 공유 안건 추가해줘"

# 출력:
[SEMO] Skill: add-meeting-agenda 호출

안건 추출: "QA 테스트 결과 공유"
대상 Discussion: #210

안건 추가 중...
✅ 안건 추가 완료

**추가된 안건**: QA 테스트 결과 공유
**회의록**: https://github.com/semicolon-devteam/command-center/discussions/210
```

### 여러 안건 한 번에 추가

```bash
"회의 안건으로 1. API 성능 개선 2. 신규 인력 온보딩 3. 스프린트 회고 추가해줘"

# 출력:
[SEMO] Skill: add-meeting-agenda 호출

안건 추출:
1. API 성능 개선
2. 신규 인력 온보딩
3. 스프린트 회고

최근 회의록 조회 중...
- 대상: [1월 3/5] 정기 회고 & 회의 (#211)

안건 추가 중...
✅ 3개 안건 추가 완료

**회의록**: https://github.com/semicolon-devteam/command-center/discussions/211
```

## GitHub API 사용

### 최근 Meeting-Minutes Discussion 조회

```bash
# 가장 최근 Meeting-Minutes Discussion 조회
gh api graphql -f query='
query {
  repository(owner: "semicolon-devteam", name: "command-center") {
    discussions(
      first: 1
      categoryId: "DIC_kwDOOdzh984Cw9Lp"
      orderBy: {field: CREATED_AT, direction: DESC}
    ) {
      nodes {
        number
        title
        body
        url
      }
    }
  }
}'
```

### Discussion Body 업데이트

```bash
# Discussion 업데이트
DISCUSSION_ID="D_kwDOOdzh984..."  # Discussion의 node ID

gh api graphql -f query='
mutation($discussionId: ID!, $body: String!) {
  updateDiscussion(input: {
    discussionId: $discussionId
    body: $body
  }) {
    discussion {
      number
      url
    }
  }
}' \
  -f discussionId="$DISCUSSION_ID" \
  -f body="$NEW_BODY"
```

## 안건 추가 로직

### Bash 스크립트

```bash
#!/bin/bash
# 안건을 기존 body에 추가하는 로직

EXISTING_BODY="$1"
NEW_AGENDA="$2"

# "### 📝 회의 안건" 섹션 찾기
# "#### 추가 안건" 섹션이 있으면 그 아래에 추가
# 없으면 새로 생성

if echo "$EXISTING_BODY" | grep -q "#### 추가 안건"; then
  # 기존 "추가 안건" 섹션에 추가
  NEW_BODY=$(echo "$EXISTING_BODY" | sed "/#### 추가 안건/a\\
- [ ] $NEW_AGENDA")
else
  # "### 📝 회의 안건" 섹션 끝에 "추가 안건" 섹션 생성
  NEW_BODY=$(echo "$EXISTING_BODY" | sed "/### 📝 회의 안건/,/### [^#]/{
    /### [^#]/i\\
\\
#### 추가 안건\\
- [ ] $NEW_AGENDA
  }")
fi

echo "$NEW_BODY"
```

## Output

```markdown
[SEMO] Skill: add-meeting-agenda 완료

✅ 안건 추가 완료

**추가된 안건**: {agenda_item}
**회의록**: https://github.com/semicolon-devteam/command-center/discussions/{number}
```

## 에러 처리

| 에러 | 원인 | 해결 |
|------|------|------|
| gh 인증 오류 | GitHub CLI 미로그인 | `gh auth login` 실행 |
| Discussion not found | 잘못된 번호 | Discussion 번호 확인 |
| 회의록 없음 | Meeting-Minutes 카테고리에 Discussion 없음 | 먼저 회의록 생성 필요 |
| 안건 추출 실패 | 요청 내용이 불명확 | 명확한 안건 내용 재요청 |

## Related

- `create-meeting-minutes` - 정기 회의록 생성
- `summarize-meeting` - 녹취록 기반 회의록 생성
- `create-decision-log` - 의사결정 로그 생성
