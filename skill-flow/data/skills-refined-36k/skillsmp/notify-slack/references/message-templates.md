# Slack Message Templates

> notify-slack Skill에서 사용하는 Slack Block Kit 메시지 템플릿

> 📖 **Slack 설정**: [semo-core/_shared/slack-config.md](../../../_shared/slack-config.md) 참조

## 릴리스 알림 템플릿 (표준)

> **🔴 필수**: version-manager 완료 후 반드시 이 템플릿으로 알림을 전송해야 합니다.

### 메시지 미리보기

```text
🚀 SEMO 패키지 업데이트

패키지             버전
semo-meta          v0.30.0

변경 내역
• version-manager SKILL.md에 Slack 알림 필수화 명시
• Quick Start 간소화 (9단계 → 6단계)
• 누락 시 미완료 상태 경고 추가

🔗 GitHub
```

### JSON 템플릿

```json
{
  "channel": "C09KNL91QBZ",
  "text": "🚀 SEMO 패키지 업데이트 - {package_name} v{version}",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "🚀 SEMO 패키지 업데이트",
        "emoji": true
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*패키지*\n{package_name}"
        },
        {
          "type": "mrkdwn",
          "text": "*버전*\n`v{version}`"
        }
      ]
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*변경 내역*\n{changelog_bullets}"
      }
    },
    {
      "type": "context",
      "elements": [
        {
          "type": "mrkdwn",
          "text": "🔗 <https://github.com/semicolon-devteam/{package_name}|GitHub>"
        }
      ]
    }
  ]
}
```

### 변수

| 변수 | 설명 | 예시 |
|------|------|------|
| `{package_name}` | 패키지 이름 | `semo-meta` |
| `{version}` | 새 버전 (v 접두사 없이) | `0.30.0` |
| `{changelog_bullets}` | 변경 내역 (• bullet 형식) | `• feature A 추가\n• bug B 수정` |

### curl 명령어 예시 (heredoc 방식 권장)

> **⚠️ 중요**: 쉘 이스케이프 문제를 방지하기 위해 **heredoc 방식**을 사용하세요.
> **토큰 획득**: `mcp__semo-integrations__semo_get_slack_token()` 호출 후 사용

```bash
# ✅ 권장: heredoc 방식 (쉘 이스케이프 문제 방지)
# TOKEN은 mcp__semo-integrations__semo_get_slack_token()에서 획득
curl -s -X POST 'https://slack.com/api/chat.postMessage' \
  -H 'Authorization: Bearer {TOKEN}' \
  -H 'Content-Type: application/json; charset=utf-8' \
  -d @- << 'EOF'
{
  "channel": "C09KNL91QBZ",
  "text": "SEMO 패키지 업데이트: semo-meta v0.30.0",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "SEMO 패키지 업데이트"
      }
    },
    {
      "type": "section",
      "fields": [
        {"type": "mrkdwn", "text": "*패키지*\nsemo-meta"},
        {"type": "mrkdwn", "text": "*버전*\nv0.30.0"}
      ]
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*변경 내역*\n• version-manager SKILL.md에 Slack 알림 필수화 명시\n• Quick Start 간소화 (9단계 → 6단계)\n• 누락 시 미완료 상태 경고 추가"
      }
    },
    {
      "type": "context",
      "elements": [{"type": "mrkdwn", "text": "<https://github.com/semicolon-devteam/semo-meta|GitHub>"}]
    }
  ]
}
EOF
```

> **🔴 주의**: `-d "{...}"` 형식 (쌍따옴표 + 이스케이프)은 한글, 특수문자에서 오류가 발생할 수 있습니다.

### 변경 내역 작성 규칙

| 규칙 | 설명 | 예시 |
|------|------|------|
| **Bullet 접두사** | `•` 문자 사용 | `• 기능 추가` |
| **줄바꿈** | `\n`으로 구분 | `• A\n• B\n• C` |
| **간결성** | 한 줄에 핵심 변경사항 1개 | `• agent-X 추가` |
| **CHANGELOG 기반** | CHANGELOG.md에서 주요 항목 추출 | Added, Changed, Fixed 섹션 |

### 복수 패키지 릴리스

여러 패키지를 동시에 릴리스할 때:

```json
{
  "text": "🚀 SEMO 릴리즈 - SEMO-Next 0.35.0 / SEMO-Backend 1.2.0",
  "blocks": [
    {
      "type": "header",
      "text": { "type": "plain_text", "text": "🚀 SEMO 릴리즈" }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*SEMO-Next 0.35.0 / SEMO-Backend 1.2.0*"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*공통 변경 내역*\n• 기능 A 추가\n• 버그 B 수정"
      }
    },
    {
      "type": "context",
      "elements": [
        {
          "type": "mrkdwn",
          "text": "<https://...|SEMO-Next CHANGELOG> | <https://...|SEMO-Backend CHANGELOG>"
        }
      ]
    }
  ]
}
```

## 이슈/태스크 알림 템플릿

### 기본 템플릿

```json
{
  "channel": "#_협업",
  "text": "📋 새로운 이슈가 생성되었습니다",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "📋 새로운 이슈가 생성되었습니다",
        "emoji": true
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*컨텍스트*\n<{context_url}|#{context_number} {context_title}>"
        },
        {
          "type": "mrkdwn",
          "text": "*프로젝트*\n{project_name}"
        }
      ]
    },
    {
      "type": "divider"
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*이슈 목록*"
      }
    }
  ]
}
```

### 이슈 항목 블록 (반복)

```json
{
  "type": "section",
  "text": {
    "type": "mrkdwn",
    "text": "• <{issue_url}|#{issue_number} {issue_title}> - {assignee_mention}"
  }
}
```

### Footer 블록

```json
{
  "type": "context",
  "elements": [
    {
      "type": "mrkdwn",
      "text": "구현을 시작해주세요! 🚀"
    }
  ]
}
```

## 커스텀 메시지 템플릿

```json
{
  "channel": "{channel}",
  "text": "{plain_text_fallback}",
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "{message_with_mentions}"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "📋 *이슈*: <{issue_url}|#{issue_number} {issue_title}>"
      }
    }
  ]
}
```

## curl 명령어 템플릿

### 토큰 획득

```
mcp__semo-integrations__semo_get_slack_token()
```

응답에서 `token:` 접두사 뒤의 토큰 값을 추출합니다.

### 파일 기반 방식

```bash
# message.json 파일에 메시지 저장 후 전송
# TOKEN은 mcp__semo-integrations__semo_get_slack_token()에서 획득
curl -s -X POST 'https://slack.com/api/chat.postMessage' \
  -H 'Authorization: Bearer {TOKEN}' \
  -H 'Content-Type: application/json; charset=utf-8' \
  -d '@message.json'
```

### heredoc 방식 (권장)

```bash
# 쉘 이스케이프 문제 없이 직접 전송
# TOKEN은 mcp__semo-integrations__semo_get_slack_token()에서 획득
curl -s -X POST 'https://slack.com/api/chat.postMessage' \
  -H 'Authorization: Bearer {TOKEN}' \
  -H 'Content-Type: application/json; charset=utf-8' \
  -d @- << 'EOF'
{
  "channel": "C09KNL91QBZ",
  "text": "메시지 내용"
}
EOF
```

## Block Kit Builder

메시지 미리보기 및 수정:
- https://app.slack.com/block-kit-builder
