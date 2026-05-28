# Workflow

> version-manager의 10단계 버저닝 프로세스

## Input Schema

```json
{
  "changes": [
    {
      "type": "added|changed|removed|fixed",
      "component": "Agent|Skill|Command|Config",
      "name": "component-name",
      "description": "변경 사항 설명",
      "package": "semo-po|semo-next|semo-meta|semo-core"
    }
  ],
  "version_hint": "major|minor|patch|auto",
  "feedback_issues": [
    {
      "repo": "semo-po|semo-next|semo-meta|semo-core",
      "number": 123
    }
  ]
}
```

## Phase 1: 현재 버전 확인

```bash
# VERSION 파일 읽기
cat sax/VERSION
# 예: 3.7.0
```

## Phase 2: 버전 타입 판단

1. **version_hint 확인**:
   - `major|minor|patch` → 직접 사용
   - `auto` → Algorithm으로 자동 판단

2. **변경사항 분석**:
   - Added → MINOR
   - Removed → MINOR (또는 MAJOR if breaking)
   - Changed → MINOR (또는 PATCH if minor)
   - Fixed → PATCH

## Phase 3: 새 버전 계산

예시:
- 3.7.0 + MINOR → 3.8.0
- 3.8.0 + PATCH → 3.8.1
- 3.8.1 + MAJOR → 4.0.0

## Phase 4: CHANGELOG 파일 생성

**파일 위치**: `sax/CHANGELOG/{new_version}.md`

**날짜**: 현재 시스템 날짜 (`date +%Y-%m-%d`)

## Phase 5: INDEX.md 업데이트

1. **Latest Version 업데이트**:
   ```markdown
   **Latest Version**: [3.8.0](3.8.0.md) - 2025-11-26
   ```

2. **Version History 섹션에 추가**:
   ```markdown
   ### v3.x (2025-11-26)

   - [3.8.0](3.8.0.md) - SEMO-Meta 패키지 분리
   - [3.7.0](3.7.0.md) - CHANGELOG 구조 개선
   ```

3. **Breaking Changes 업데이트** (MAJOR만):
   ```markdown
   ## Breaking Changes

   - **v4.0.0**: {변경사항 설명}
   ```

## Phase 6: VERSION 파일 업데이트

```bash
# 새 버전 쓰기
echo "{new_version}" > sax/VERSION
```

## Phase 7: 커밋

```bash
# 변경사항 스테이징
git add sax/VERSION sax/CHANGELOG/

# 버전 커밋 (CLAUDE.md 버저닝 커밋 형식 준수)
git commit -m "🔖 [SEMO] {new_version}: {변경 요약}

- 상세 변경 내용 1
- 상세 변경 내용 2

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

**커밋 메시지 형식** (CLAUDE.md 규칙):

```text
🔖 [SEMO] {version}: {변경 요약}

- 상세 변경 내용 1
- 상세 변경 내용 2

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**포함 파일**:

- `sax/VERSION`
- `sax/CHANGELOG/{new_version}.md`
- `sax/CHANGELOG/INDEX.md`

## Phase 8: 푸시 (필수)

> **🔴 필수 단계**: 버저닝은 푸시까지 완료해야 완료로 간주됩니다.

```bash
# 원격 저장소에 푸시
git push origin main
```

**서브모듈 환경**: 각 패키지(semo-meta, semo-po, semo-next)가 별도 레포인 경우 개별 푸시 필요

```bash
cd semo-meta && git push origin main
cd semo-po && git push origin main
cd semo-next && git push origin main
```

> **⚠️ Phase 8 완료 즉시 Phase 9로 자동 진행합니다. 멈추지 마세요.**

## Phase 9: Slack 릴리스 알림 (필수) - 🔴 자동 체인

> **🔴 필수 단계**: 버저닝은 Slack 알림까지 완료해야 완료로 간주됩니다.

푸시 완료 후 `notify-slack` Skill을 호출하여 `#_협업` 채널에 릴리스 알림을 전송합니다.

### 알림 데이터 구성

```yaml
type: "release"
package: "{package_name}"  # semo-po, semo-next, semo-meta, semo-core
version: "{new_version}"
changelog: |
  {CHANGELOG 내용 요약}
```

### Slack 메시지 예시

```
🚀 SEMO 패키지 업데이트

📦 semo-po v0.16.0

변경 내역:
• report-bug: 버그 리포트 Skill 추가

🔗 GitHub
```

### notify-slack 호출

> 📖 **Slack 설정**: [semo-core/_shared/slack-config.md](../../../semo-core/_shared/slack-config.md) 참조

```bash
# notify-slack Skill이 다음을 수행:
# 1. CHANGELOG/{version}.md 파일 읽기
# 2. 메시지 블록 구성
# 3. Slack API 호출

# 토큰은 semo-core/_shared/slack-config.md 참조
# SLACK_BOT_TOKEN은 환경변수로 설정

curl -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "#_협업",
    "text": "🚀 SEMO 패키지 업데이트",
    "blocks": [...]
  }'
```

### 완료 메시지

```markdown
[SEMO] Skill: notify-slack 완료

✅ Slack 릴리스 알림 전송 완료

**채널**: #_협업
**패키지**: {package_name}
**버전**: v{new_version}
```

## Phase 10: 피드백 이슈 완료 처리 (조건부)

> **피드백 이슈 기반 버저닝일 때만 실행**

### 피드백 이슈 감지

**자동 감지** (커밋 메시지 분석):

```bash
# 커밋 메시지에서 이슈 참조 추출
git log -1 --format="%B" | grep -oE "(#[0-9]+|Fixes #[0-9]+|Closes #[0-9]+)" | grep -oE "[0-9]+"
```

**명시적 지정** (Input Schema):

```yaml
feedback_issues:
  - repo: "semo-po"
    number: 123
```

### 이슈 정보 조회

```bash
# 이슈 상세 정보 조회
gh issue view {이슈번호} --repo semicolon-devteam/{repo} --json author,labels,body

# 예시 출력:
# {
#   "author": {"login": "kyago"},
#   "labels": [{"name": "bug"}, {"name": "semo-po"}],
#   "body": "...\n🤖 SEMO Feedback Skill (semo-core)로 자동 생성됨"
# }
```

### 피드백 이슈 판별 조건

다음 조건을 **모두** 만족해야 피드백 이슈로 판별:

1. **라벨 조건**: `bug` 또는 `enhancement` 라벨 존재
2. **출처 조건**: 본문에 `SEMO Feedback Skill` 문구 포함

```bash
# 판별 스크립트
ISSUE_DATA=$(gh issue view {이슈번호} --repo semicolon-devteam/{repo} --json author,labels,body)

# 라벨 확인
HAS_FEEDBACK_LABEL=$(echo "$ISSUE_DATA" | jq '.labels[] | select(.name == "bug" or .name == "enhancement")' | head -1)

# 출처 확인
HAS_SAX_ORIGIN=$(echo "$ISSUE_DATA" | jq -r '.body' | grep -c "SEMO Feedback Skill")

if [ -n "$HAS_FEEDBACK_LABEL" ] && [ "$HAS_SAX_ORIGIN" -gt 0 ]; then
  echo "피드백 이슈 확인됨"
fi
```

### GitHub 이슈에 완료 코멘트 추가

```bash
# 이슈 작성자 조회
AUTHOR=$(gh issue view {이슈번호} --repo semicolon-devteam/{repo} --json author --jq '.author.login')

# 완료 코멘트 추가
gh issue comment {이슈번호} --repo semicolon-devteam/{repo} --body "$(cat <<EOF
✅ **피드백 반영 완료**

@${AUTHOR} 님의 피드백이 **v{new_version}**에 반영되었습니다.

**변경 내역**:
{CHANGELOG 요약 - 불릿 포인트}

SEMO를 사용해주셔서 감사합니다! 🙏

---
🤖 SEMO version-manager로 자동 생성됨
EOF
)"
```

### Slack 알림에 피드백 작성자 멘션 추가

기존 릴리스 알림에 피드백 작성자 섹션 추가:

```json
{
  "channel": "#_협업",
  "blocks": [
    // ... 기존 릴리스 알림 블록 ...
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "📣 *피드백 반영*: @{slack_user} 님의 제안이 반영되었습니다!"
      }
    }
  ]
}
```

**GitHub → Slack 사용자 매핑**:

```bash
# notify-slack의 동적 조회 활용
# 1. GitHub 사용자명으로 Slack 사용자 검색
# 2. 실명/이메일 기반 매핑 시도
# 3. 매핑 실패 시 GitHub 사용자명 표시 (@kyago)
```

### 완료 메시지

```markdown
[SEMO] Versioning: 피드백 이슈 처리 완료

✅ GitHub 이슈 #{이슈번호} 완료 코멘트 추가
✅ Slack 알림에 @{작성자} 멘션 포함

**피드백 작성자**: @{author}
**이슈**: semicolon-devteam/{repo}#{이슈번호}
```

### 피드백 이슈가 없는 경우

피드백 이슈가 감지되지 않으면 Phase 10은 스킵됩니다:

```markdown
[SEMO] Versioning: 피드백 이슈 없음 - Phase 10 스킵
```

## Validation

**버저닝 전**:

- ✅ VERSION 파일 존재
- ✅ CHANGELOG/ 디렉토리 존재
- ✅ INDEX.md 파일 존재
- ✅ changes 배열 비어있지 않음

**버저닝 후**:

- ✅ VERSION 파일 업데이트 확인
- ✅ CHANGELOG/{new_version}.md 생성 확인
- ✅ INDEX.md Latest Version 업데이트 확인
- ✅ Keep a Changelog 형식 준수 확인
- ✅ 커밋 완료 확인 (`git log -1`)
- ✅ **푸시 완료 확인** (`git status` - "Your branch is up to date")
- ✅ **Slack 알림 전송 확인**
- ✅ **피드백 이슈 완료 처리 확인** (조건부)
