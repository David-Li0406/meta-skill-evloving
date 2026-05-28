# Issue Templates

> feedback 스킬 이슈 템플릿 (SEMO 공통)

## 버그 리포트 템플릿

```markdown
## 버그 리포트

### 질문/프롬프트
{사용자가 입력한 질문 또는 명령}

### 실제 결과
{실제로 발생한 동작}

### 기대 결과
{사용자가 원했던 동작}

### 재현 단계
1. {단계 1}
2. {단계 2}
3. ...

### 환경
- 패키지: {package}
- 버전: {version}
- 관련 Agent/Skill: {이름}

---
🤖 SEMO Feedback Skill (semo-core)로 자동 생성됨
```

## 개선 제안 템플릿

```markdown
## 개선 제안

### 제안 내용
{개선 아이디어 설명}

### 현재 동작
{현재 어떻게 동작하는지}

### 제안 동작
{어떻게 개선되면 좋을지}

### 추가 컨텍스트
{추가 설명}

---
🤖 SEMO Feedback Skill (semo-core)로 자동 생성됨
```

## 이슈 제목 형식

### 버그

```
[Bug] {간결한 문제 요약}
```

예시:
- `[Bug] assign-task 스킬에서 Slack 알림이 발송되지 않음`
- `[Bug] Orchestrator가 피드백 키워드를 인식하지 못함`

### 제안

```
[Enhancement] {간결한 제안 요약}
```

예시:
- `[Enhancement] feedback 스킬에 스크린샷 첨부 기능 추가`
- `[Enhancement] 버그 리포트 시 자동으로 버전 정보 수집`

## 라벨 설정

### 버그

```bash
--label "bug,{package}"
```

### 제안

```bash
--label "enhancement,{package}"
```

### 패키지별 라벨

| 패키지 | 라벨 |
|--------|------|
| semo-po | `semo-po` |
| semo-next | `semo-next` |
| semo-pm | `semo-pm` |
| semo-qa | `semo-qa` |
| semo-infra | `semo-infra` |
| semo-meta | `semo-meta` |
| semo-core | `semo-core` |

## gh issue create 명령어

### 버그 이슈

```bash
PACKAGE="semo-po"
VERSION="0.5.0"

gh issue create \
  --repo "semicolon-devteam/${PACKAGE}" \
  --title "[Bug] {요약된 제목}" \
  --body "$(cat <<'EOF'
## 버그 리포트

### 질문/프롬프트
{사용자 입력}

### 실제 결과
{실제 동작}

### 기대 결과
{원하는 동작}

### 환경
- 패키지: PACKAGE_PLACEHOLDER
- 버전: VERSION_PLACEHOLDER
- 관련 Agent/Skill: {이름}

---
🤖 SEMO Feedback Skill (semo-core)로 자동 생성됨
EOF
)" \
  --label "bug,${PACKAGE}"
```

### 제안 이슈

```bash
PACKAGE="semo-po"

gh issue create \
  --repo "semicolon-devteam/${PACKAGE}" \
  --title "[Enhancement] {요약된 제목}" \
  --body "$(cat <<'EOF'
## 개선 제안

### 제안 내용
{개선 아이디어}

### 현재 동작
{현재 동작}

### 제안 동작
{제안 동작}

---
🤖 SEMO Feedback Skill (semo-core)로 자동 생성됨
EOF
)" \
  --label "enhancement,${PACKAGE}"
```
