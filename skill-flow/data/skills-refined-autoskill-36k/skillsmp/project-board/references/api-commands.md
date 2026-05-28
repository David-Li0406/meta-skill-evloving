# Project Board API Commands

> 프로젝트 보드 연동을 위한 상세 API 명령어

## 전제 조건

```yaml
organization: semicolon-devteam
project_number: 1  # "이슈관리" 프로젝트
```

## 1. 이슈를 프로젝트에 추가

### 기본 명령

```bash
# 이슈 URL로 프로젝트에 추가
ISSUE_URL="https://github.com/semicolon-devteam/${REPO}/issues/${ISSUE_NUM}"
gh project item-add 1 --owner semicolon-devteam --url "${ISSUE_URL}"
```

### 출력 예시

```json
{
  "id": "PVTI_xxx",
  "title": "이슈 제목",
  "number": 123
}
```

## 2. 프로젝트 메타데이터 조회

### Project ID 및 Status 필드 조회

```bash
gh api graphql -f query='
query($org: String!, $projectNumber: Int!) {
  organization(login: $org) {
    projectV2(number: $projectNumber) {
      id
      title
      field(name: "Status") {
        ... on ProjectV2SingleSelectField {
          id
          name
          options {
            id
            name
            color
          }
        }
      }
    }
  }
}' -f org="semicolon-devteam" -F projectNumber=1 --jq '.'
```

### 출력 예시

```json
{
  "data": {
    "organization": {
      "projectV2": {
        "id": "PVT_xxx",
        "title": "이슈관리",
        "field": {
          "id": "PVTSSF_xxx",
          "name": "Status",
          "options": [
            { "id": "xxx1", "name": "검수대기", "color": "GRAY" },
            { "id": "xxx2", "name": "검수완료", "color": "BLUE" },
            { "id": "xxx3", "name": "작업중", "color": "YELLOW" },
            { "id": "xxx4", "name": "리뷰요청", "color": "ORANGE" },
            { "id": "xxx5", "name": "테스트중", "color": "PURPLE" },
            { "id": "xxx6", "name": "병합됨", "color": "GREEN" }
          ]
        }
      }
    }
  }
}
```

## 3. 이슈의 Project Item 조회

### Item ID 및 현재 상태 조회

```bash
gh api graphql -f query='
query($owner: String!, $repo: String!, $issueNumber: Int!) {
  repository(owner: $owner, name: $repo) {
    issue(number: $issueNumber) {
      title
      projectItems(first: 10) {
        nodes {
          id
          project {
            title
            number
          }
          fieldValueByName(name: "Status") {
            ... on ProjectV2ItemFieldSingleSelectValue {
              name
              optionId
            }
          }
        }
      }
    }
  }
}' -f owner="semicolon-devteam" -f repo="${REPO}" -F issueNumber=${ISSUE_NUM} --jq '.'
```

### 출력 예시

```json
{
  "data": {
    "repository": {
      "issue": {
        "title": "이슈 제목",
        "projectItems": {
          "nodes": [
            {
              "id": "PVTI_xxx",
              "project": {
                "title": "이슈관리",
                "number": 1
              },
              "fieldValueByName": {
                "name": "작업중",
                "optionId": "xxx3"
              }
            }
          ]
        }
      }
    }
  }
}
```

## 4. 날짜 필드 조회

### 시작일/종료일 필드 ID 조회

```bash
gh api graphql -f query='
query($org: String!, $projectNumber: Int!) {
  organization(login: $org) {
    projectV2(number: $projectNumber) {
      id
      field(name: "시작일") {
        ... on ProjectV2Field {
          id
          name
        }
      }
    }
  }
}' -f org="semicolon-devteam" -F projectNumber=1 --jq '.data.organization.projectV2.field.id'
```

> **Note**: `종료일` 필드도 동일한 방식으로 조회 (name: "종료일")

## 5. 날짜 필드 업데이트 (Mutation)

### 시작일 설정 (작업중 상태 변경 시)

```bash
gh api graphql -f query='
mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $date: Date!) {
  updateProjectV2ItemFieldValue(
    input: {
      projectId: $projectId
      itemId: $itemId
      fieldId: $fieldId
      value: { date: $date }
    }
  ) {
    projectV2Item {
      id
    }
  }
}' \
  -f projectId="PVT_xxx" \
  -f itemId="PVTI_xxx" \
  -f fieldId="PVTF_시작일_xxx" \
  -f date="$(date +%Y-%m-%d)"
```

### 종료일 설정 (리뷰요청 상태 변경 시)

```bash
gh api graphql -f query='
mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $date: Date!) {
  updateProjectV2ItemFieldValue(
    input: {
      projectId: $projectId
      itemId: $itemId
      fieldId: $fieldId
      value: { date: $date }
    }
  ) {
    projectV2Item {
      id
    }
  }
}' \
  -f projectId="PVT_xxx" \
  -f itemId="PVTI_xxx" \
  -f fieldId="PVTF_종료일_xxx" \
  -f date="$(date +%Y-%m-%d)"
```

## 6. 상태 변경 (Mutation)

### Status 업데이트

```bash
gh api graphql -f query='
mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
  updateProjectV2ItemFieldValue(
    input: {
      projectId: $projectId
      itemId: $itemId
      fieldId: $fieldId
      value: { singleSelectOptionId: $optionId }
    }
  ) {
    projectV2Item {
      id
      fieldValueByName(name: "Status") {
        ... on ProjectV2ItemFieldSingleSelectValue {
          name
        }
      }
    }
  }
}' \
  -f projectId="PVT_xxx" \
  -f itemId="PVTI_xxx" \
  -f fieldId="PVTSSF_xxx" \
  -f optionId="xxx4"  # 리뷰요청
```

### 출력 예시

```json
{
  "data": {
    "updateProjectV2ItemFieldValue": {
      "projectV2Item": {
        "id": "PVTI_xxx",
        "fieldValueByName": {
          "name": "리뷰요청"
        }
      }
    }
  }
}
```

## 7. 전체 워크플로우 스크립트

### 이슈 추가 + 상태 설정 통합

```bash
#!/bin/bash
# Usage: ./project-board.sh <repo> <issue_number> <target_status>

REPO=$1
ISSUE_NUM=$2
TARGET_STATUS=$3
ORG="semicolon-devteam"
PROJECT_NUM=1

ISSUE_URL="https://github.com/${ORG}/${REPO}/issues/${ISSUE_NUM}"

# Step 1: 프로젝트에 이슈 추가 (이미 있으면 무시됨)
echo "📋 프로젝트에 이슈 추가 중..."
gh project item-add ${PROJECT_NUM} --owner ${ORG} --url "${ISSUE_URL}" 2>/dev/null || true

# Step 2: 프로젝트 메타데이터 조회
echo "🔍 프로젝트 정보 조회 중..."
PROJECT_INFO=$(gh api graphql -f query='
query($org: String!, $projectNumber: Int!) {
  organization(login: $org) {
    projectV2(number: $projectNumber) {
      id
      field(name: "Status") {
        ... on ProjectV2SingleSelectField {
          id
          options { id name }
        }
      }
    }
  }
}' -f org="${ORG}" -F projectNumber=${PROJECT_NUM})

PROJECT_ID=$(echo "$PROJECT_INFO" | jq -r '.data.organization.projectV2.id')
FIELD_ID=$(echo "$PROJECT_INFO" | jq -r '.data.organization.projectV2.field.id')
OPTION_ID=$(echo "$PROJECT_INFO" | jq -r ".data.organization.projectV2.field.options[] | select(.name == \"${TARGET_STATUS}\") | .id")

# Step 3: Item ID 조회
echo "🔍 이슈 Item ID 조회 중..."
ITEM_INFO=$(gh api graphql -f query='
query($owner: String!, $repo: String!, $issueNumber: Int!) {
  repository(owner: $owner, name: $repo) {
    issue(number: $issueNumber) {
      projectItems(first: 10) {
        nodes {
          id
          project { number }
        }
      }
    }
  }
}' -f owner="${ORG}" -f repo="${REPO}" -F issueNumber=${ISSUE_NUM})

ITEM_ID=$(echo "$ITEM_INFO" | jq -r ".data.repository.issue.projectItems.nodes[] | select(.project.number == ${PROJECT_NUM}) | .id")

# Step 4: 상태 변경
echo "🔄 상태 변경 중: → ${TARGET_STATUS}"
gh api graphql -f query='
mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
  updateProjectV2ItemFieldValue(
    input: {
      projectId: $projectId
      itemId: $itemId
      fieldId: $fieldId
      value: { singleSelectOptionId: $optionId }
    }
  ) {
    projectV2Item { id }
  }
}' -f projectId="${PROJECT_ID}" -f itemId="${ITEM_ID}" -f fieldId="${FIELD_ID}" -f optionId="${OPTION_ID}"

# Step 5: 날짜 속성 설정 (상태에 따라)
TODAY=$(date +%Y-%m-%d)

if [ "${TARGET_STATUS}" = "작업중" ]; then
  echo "📅 시작일 설정 중: ${TODAY}"
  # 시작일 필드 ID 조회
  START_DATE_FIELD_ID=$(gh api graphql -f query='
  query($org: String!, $projectNumber: Int!) {
    organization(login: $org) {
      projectV2(number: $projectNumber) {
        field(name: "시작일") {
          ... on ProjectV2Field { id }
        }
      }
    }
  }' -f org="${ORG}" -F projectNumber=${PROJECT_NUM} --jq '.data.organization.projectV2.field.id')

  # 시작일 설정
  gh api graphql -f query='
  mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $date: Date!) {
    updateProjectV2ItemFieldValue(
      input: {
        projectId: $projectId
        itemId: $itemId
        fieldId: $fieldId
        value: { date: $date }
      }
    ) {
      projectV2Item { id }
    }
  }' -f projectId="${PROJECT_ID}" -f itemId="${ITEM_ID}" -f fieldId="${START_DATE_FIELD_ID}" -f date="${TODAY}"
  echo "✅ 시작일 설정 완료"
fi

if [ "${TARGET_STATUS}" = "리뷰요청" ]; then
  echo "📅 종료일 설정 중: ${TODAY}"
  # 종료일 필드 ID 조회
  END_DATE_FIELD_ID=$(gh api graphql -f query='
  query($org: String!, $projectNumber: Int!) {
    organization(login: $org) {
      projectV2(number: $projectNumber) {
        field(name: "종료일") {
          ... on ProjectV2Field { id }
        }
      }
    }
  }' -f org="${ORG}" -F projectNumber=${PROJECT_NUM} --jq '.data.organization.projectV2.field.id')

  # 종료일 설정
  gh api graphql -f query='
  mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $date: Date!) {
    updateProjectV2ItemFieldValue(
      input: {
        projectId: $projectId
        itemId: $itemId
        fieldId: $fieldId
        value: { date: $date }
      }
    ) {
      projectV2Item { id }
    }
  }' -f projectId="${PROJECT_ID}" -f itemId="${ITEM_ID}" -f fieldId="${END_DATE_FIELD_ID}" -f date="${TODAY}"
  echo "✅ 종료일 설정 완료"
fi

echo "✅ 완료: ${REPO}#${ISSUE_NUM} → ${TARGET_STATUS}"
```

## 8. GitHub Issue Type 설정 (필수)

> **⚠️ Projects 커스텀 필드 `타입` 대신 GitHub Issue 기본 `Type` 필드 사용**

### Issue Type ID Reference

| Type | ID | 용도 |
|------|-----|------|
| Task | `IT_kwDOC01-Rc4BdOub` | 일반 태스크 (기본값) |
| Bug | `IT_kwDOC01-Rc4BdOuc` | 버그 리포트 |
| Feature | `IT_kwDOC01-Rc4BdOud` | 기능 요청 |
| Epic | `IT_kwDOC01-Rc4BvVz5` | 에픽 |

### Issue Type 설정 (GraphQL Mutation)

```bash
# 1. Issue node_id 조회
ISSUE_NODE_ID=$(gh api repos/semicolon-devteam/{repo}/issues/{issue_number} --jq '.node_id')

# 2. Issue Type 설정
gh api graphql -f query='
  mutation {
    updateIssue(input: {
      id: "'"$ISSUE_NODE_ID"'"
      issueTypeId: "IT_kwDOC01-Rc4BdOub"
    }) {
      issue { id title }
    }
  }
'
```

### Issue Type 조회

```bash
# 현재 Issue의 Type 확인
gh api repos/semicolon-devteam/{repo}/issues/{issue_number} --jq '.type.name // "없음"'
```

### 사용 시점

| 이슈 생성 유형 | Issue Type |
|--------------|------------|
| Draft Task 생성 | Task |
| 버그 등록 | Bug |
| Epic 생성 | Epic |
| 기능 요청 | Feature |

> **Note**: Projects 커스텀 필드 `타입`은 더 이상 사용하지 않습니다. GitHub Issue 기본 Type 필드를 사용하세요.

## 에러 코드

| 에러 메시지 | 원인 | 해결 방법 |
|------------|------|----------|
| `Could not resolve to a ProjectV2` | 프로젝트 번호 오류 | `gh project list --owner semicolon-devteam`으로 확인 |
| `Resource not accessible by integration` | 권한 부족 | PAT에 `project` scope 추가 필요 |
| `Field was not found` | Status 필드 없음 | 프로젝트 설정에서 Status 필드 확인 |
| `Could not find single select option` | 상태값 없음 | 상태 목록 조회 후 정확한 이름 사용 |
| `Item was not found` | 이슈가 프로젝트에 없음 | `gh project item-add`로 먼저 추가 |
| `issueTypeId is invalid` | Issue Type ID 오류 | 위 Issue Type ID Reference 확인 |
