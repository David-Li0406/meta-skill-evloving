# 팀 컨텍스트 설정

> semo-help 스킬에서 Semicolon 팀 컨텍스트를 제공하는 방법

## Semicolon 팀 기본 정보

### 조직 정보

| 항목 | 값 |
|------|-----|
| **Organization** | semicolon-devteam |
| **응답 언어** | 한글 |
| **기본 브랜치** | main |
| **이슈 템플릿** | .github/ISSUE_TEMPLATE |

### 주요 레포지토리

| 레포 | 용도 |
|------|------|
| docs | 팀 위키 및 문서 |
| core-supabase | Supabase DB 관리 |
| core-backend | 백엔드 API |
| core-next-web | Next.js 웹앱 |

## TEAM_RULES.md 참조

### 조회 방법

```bash
# 로컬 semo-core
cat semo-core/TEAM_RULES.md

# docs 레포 (원격)
gh api repos/semicolon-devteam/docs/contents/sax/core/TEAM_RULES.md \
  --jq '.content' | base64 -d
```

### 주요 규칙 요약

1. **응답 언어**: 항상 한글 사용
2. **커밋 메시지**: 깃모지 + 이슈 번호 포함
3. **이슈 라벨**: 표준 라벨 셋 사용
4. **PR 리뷰**: 최소 1명 승인 필요

## Slack 채널 정보

| 채널 | 용도 |
|------|------|
| #_협업 | 기본 알림 채널 |
| #_개발 | 개발 논의 |
| #_qa | QA 관련 |

## 응답 템플릿

### 팀 규칙 질문

```markdown
[SEMO] Skill: semo-help 응답

## Semicolon 팀 규칙

### 기본 설정
- **응답 언어**: 한글
- **기본 Organization**: semicolon-devteam
- **이슈 템플릿**: .github/ISSUE_TEMPLATE 기반

### 커밋 규칙
- 깃모지 사용 (예: ✨ 기능 추가, 🐛 버그 수정)
- 이슈 번호 포함 (예: `✨ #123: 기능 추가`)

### 참고 문서
- docs 위키: https://github.com/semicolon-devteam/docs/wiki
- 팀 규칙: semo-core/TEAM_RULES.md

---
📚 상세 정보: TEAM_RULES.md
```

### 레포 정보 질문

```markdown
[SEMO] Skill: semo-help 응답

## Semicolon 레포지토리

| 레포 | 용도 | 담당자 |
|------|------|--------|
| docs | 팀 위키 | 전원 |
| core-supabase | DB 관리 | Backend |
| core-backend | API 서버 | Backend |
| core-next-web | 웹앱 | Frontend |

---
📚 상세 정보: docs 위키 참조
```

## 팀원 정보 조회

### Slack ID 조회 (동적)

```bash
curl -s "https://slack.com/api/users.list" \
  -H "Authorization: Bearer xoxb-891491331223-9421307124626-IytLQOaiaN2R97EMUdElgdX7" \
  | jq '.members[] | select(.deleted == false and .is_bot == false) | {name, real_name}'
```

### GitHub 사용자 조회

```bash
gh api orgs/semicolon-devteam/members --jq '.[].login'
```
