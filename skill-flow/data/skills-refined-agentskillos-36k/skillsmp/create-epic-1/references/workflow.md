# Workflow Reference

## 🔴 Step 0: 개발자 관점 체크리스트 검토 (필수)

> **Epic 생성 전 반드시 [dev-checklist.md](dev-checklist.md)를 검토합니다.**

### 검토 항목

1. **데이터 흐름**: 충돌 해결, 멀티플랫폼 동기화, 삭제 정책
2. **시간/계산**: 집계 기준, 일할 계산, 타임존
3. **플랫폼 제약**: PWA/웹/네이티브 제약사항 및 대안
4. **도메인 지식**: 업계 표준, 엣지 케이스
5. **엣지 케이스**: 빈 상태, 대량 데이터, 동시 접속

### 검토 결과 반영

- 누락된 항목이 있으면 Epic 본문의 해당 User Story에 **인라인 주석**으로 추가
- 예시:
  ```markdown
  - 사용자는 매출을 입력할 수 있다
    - **데이터 충돌**: 최신 타임스탬프 우선
    - **오프라인**: 로컬 저장 후 온라인 시 동기화
  ```

---

## 입력 스키마

epic-master로부터 전달받는 정보:

```yaml
domain_name: string      # 도메인명 (예: Comments)
domain_description: string
problems: string[]       # 해결하려는 문제
benefits: string[]       # 기대 효과
user_stories:
  required: string[]     # 필수 User Stories
  optional: string[]     # 선택 User Stories
acceptance_criteria: string[]
target_repos: string[]   # 대상 레포지토리
dependencies: string[]
priority: string         # P0/P1/P2/P3/P4 (기본: P2)
complexity: string       # High/Medium/Low
```

## 우선순위 선택 프롬프트

Epic 생성 시 사용자에게 우선순위를 물어봅니다:

```markdown
**우선순위를 선택해주세요** (기본: P2 보통)

| 우선순위 | 설명 |
|----------|------|
| P0(긴급) | 즉시 처리 필요 |
| P1(높음) | 이번 스프린트 내 |
| P2(보통) | 일반 백로그 |
| P3(낮음) | 여유 있을 때 |
| P4(매우 낮음) | 나중에 |
```

> 미지정 시 **P2(보통)** 이 자동 적용됩니다.

## 동작 상세

### 1. 템플릿 로드

```bash
# 템플릿 경로
.claude/semo-po/templates/epic-template.md
```

### 2. 템플릿 렌더링

입력 데이터로 템플릿의 플레이스홀더 치환

### 3. GitHub Issue 생성

```bash
gh issue create \
  --repo semicolon-devteam/docs \
  --title "[Epic] {DOMAIN_NAME} · {short_description}" \
  --body "{rendered_template}" \
  --label "epic"
```

### 4. Projects 연동 + Issue Type/우선순위 설정 (필수)

```bash
# 1. Issue의 node_id 조회
ISSUE_NODE_ID=$(gh api repos/semicolon-devteam/docs/issues/{issue_number} \
  --jq '.node_id')

# 2. 이슈관리 Projects (#1)에 추가 및 Item ID 획득
ITEM_ID=$(gh api graphql -f query='
  mutation($projectId: ID!, $contentId: ID!) {
    addProjectV2ItemById(input: {
      projectId: $projectId
      contentId: $contentId
    }) {
      item {
        id
      }
    }
  }
' -f projectId="PVT_kwDOC01-Rc4AtDz2" -f contentId="$ISSUE_NODE_ID" \
  --jq '.data.addProjectV2ItemById.item.id')

# 3. 🔴 GitHub Issue Type을 "Epic"으로 설정 (필수)
gh api graphql -f query='
  mutation {
    updateIssue(input: {
      id: "'"$ISSUE_NODE_ID"'"
      issueTypeId: "IT_kwDOC01-Rc4BvVz5"
    }) {
      issue { id title }
    }
  }
'

# 4. 우선순위 필드 설정
gh api graphql -f query='
  mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
    updateProjectV2ItemFieldValue(input: {
      projectId: $projectId
      itemId: $itemId
      fieldId: $fieldId
      value: { singleSelectOptionId: $optionId }
    }) {
      projectV2Item { id }
    }
  }
' -f projectId="PVT_kwDOC01-Rc4AtDz2" \
  -f itemId="$ITEM_ID" \
  -f fieldId="PVTSSF_lADOC01-Rc4AtDz2zg0YPyI" \
  -f optionId="{priority_option_id}"
```

> **Note**: `PVT_kwDOC01-Rc4AtDz2`는 semicolon-devteam의 `이슈관리` Projects (#1) ID입니다.

### GitHub Issue Type ID

> **Projects 커스텀 필드 '타입' 대신 GitHub Issue Type을 사용합니다.**

| Issue Type | ID |
|------------|-----|
| Task | `IT_kwDOC01-Rc4BdOub` |
| Bug | `IT_kwDOC01-Rc4BdOuc` |
| Feature | `IT_kwDOC01-Rc4BdOud` |
| Epic | `IT_kwDOC01-Rc4BvVz5` |

### 우선순위 Option ID 매핑

| 우선순위 | Option ID |
|----------|-----------|
| P0(긴급) | `a20917be` |
| P1(높음) | `851dbd77` |
| P2(보통) | `e3b68a2a` |
| P3(낮음) | `2ba68eff` |
| P4(매우 낮음) | `746928cf` |

## 제약 사항

- docs 레포지토리에만 Epic 생성
- 기술 상세는 포함하지 않음
- **Projects 연동은 필수** (실패 시 재시도 필요)
