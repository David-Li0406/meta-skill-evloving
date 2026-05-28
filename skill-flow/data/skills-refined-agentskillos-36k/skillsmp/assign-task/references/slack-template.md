# Slack Template

> 업무 할당 알림 메시지 템플릿 (assign-task Skill Reference)

## 메시지 구조

### Block Kit 형식

```json
{
  "channel": "C09KNL91QBZ",
  "text": "📋 새 업무가 할당되었습니다: #{issue_number}",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "📋 업무 할당 알림",
        "emoji": true
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*담당자*\n<@{slack_id}>"
        },
        {
          "type": "mrkdwn",
          "text": "*작업량*\n{total_points}점 (약 {days}일)"
        }
      ]
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Issue*\n<{issue_url}|#{issue_number} - {issue_title}>"
      }
    },
    {
      "type": "divider"
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*📊 작업 내역*\n{task_list}"
      }
    },
    {
      "type": "context",
      "elements": [
        {
          "type": "mrkdwn",
          "text": "🤖 SEMO assign-task Skill | {timestamp}"
        }
      ]
    }
  ]
}
```

## 변수 설명

| 변수 | 설명 | 예시 |
|------|------|------|
| `{slack_id}` | 담당자 Slack User ID | `U12345678` |
| `{total_points}` | 총 작업량 Point | `4` |
| `{days}` | 예상 소요일 (Point × 0.5) | `2` |
| `{issue_url}` | GitHub Issue URL | `https://github.com/...` |
| `{issue_number}` | Issue 번호 | `123` |
| `{issue_title}` | Issue 제목 | `Add user authentication` |
| `{task_list}` | 작업 목록 (mrkdwn) | `• API 구현: 2점\n• 테스트: 1점` |
| `{timestamp}` | 발송 시간 | `2024-01-15 14:30` |

## task_list 포맷

```
• {task_name_1}: {point_1}점
• {task_name_2}: {point_2}점
• {task_name_3}: {point_3}점
─────────────
*총점: {total_points}점*
```

## 발송 예시

### curl 명령어

```bash
TOKEN="xoxb-..."  # MCP에서 조회

curl -s -X POST 'https://slack.com/api/chat.postMessage' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json; charset=utf-8' \
  -d @- << 'EOF'
{
  "channel": "C09KNL91QBZ",
  "text": "📋 새 업무가 할당되었습니다: #123",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "📋 업무 할당 알림",
        "emoji": true
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*담당자*\n<@U12345678>"
        },
        {
          "type": "mrkdwn",
          "text": "*작업량*\n4점 (약 2일)"
        }
      ]
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Issue*\n<https://github.com/semicolon-devteam/repo/issues/123|#123 - Add user authentication>"
      }
    },
    {
      "type": "divider"
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*📊 작업 내역*\n• API 엔드포인트 구현: 2점\n• DTO 클래스 작성: 1점\n• 테스트 코드 작성: 1점\n─────────────\n*총점: 4점*"
      }
    },
    {
      "type": "context",
      "elements": [
        {
          "type": "mrkdwn",
          "text": "🤖 SEMO assign-task Skill | 2024-01-15 14:30"
        }
      ]
    }
  ]
}
EOF
```

## Slack ID 조회

### GitHub Username → Slack ID 매핑

```bash
# 1. Slack 사용자 목록 조회
curl -s 'https://slack.com/api/users.list' \
  -H "Authorization: Bearer $TOKEN" | \
  jq -r '.members[] | select(.deleted==false) | "\(.name)\t\(.id)\t\(.profile.display_name)"'

# 2. display_name 또는 real_name으로 검색
curl -s 'https://slack.com/api/users.list' \
  -H "Authorization: Bearer $TOKEN" | \
  jq -r '.members[] | select(.profile.display_name=="{name}" or .real_name | contains("{name}")) | .id'
```

### 매핑 캐시 (권장)

자주 사용하는 팀원은 `.claude/memory/` 에 캐시:

```yaml
# .claude/memory/slack-mapping.yaml
github_to_slack:
  username1: U12345678
  username2: U87654321
```

## 에러 처리

| 상황 | 처리 |
|------|------|
| Slack ID 미발견 | `@{github_username} (Slack ID 미확인)` 표시 |
| 채널 접근 불가 | 기본 채널(#_협업)로 발송 |
| API 실패 | 경고 로그, 할당은 계속 진행 |

## 참고

- [notify-slack SKILL](../../notify-slack/SKILL.md) - 공통 Slack 알림
- [Slack Block Kit Builder](https://app.slack.com/block-kit-builder) - 메시지 미리보기
