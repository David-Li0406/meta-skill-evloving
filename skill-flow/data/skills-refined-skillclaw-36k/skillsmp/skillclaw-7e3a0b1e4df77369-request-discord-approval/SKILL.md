---
name: request-discord-approval
description: Use this skill when you need to request human approval for critical operations via Discord, especially for destructive or irreversible actions.
---

# Skill body

## When to Use

- Operation requires human review before execution
- Destructive or irreversible operations
- High-impact changes in production
- Keywords: approval, confirm, human, review, dangerous

## Prerequisites

Before applying this skill, verify:

- [ ] Operation genuinely requires human review
- [ ] DISCORD_MCP_URL is configured
- [ ] Approval channel exists
- [ ] Timeout duration is acceptable (default: 5 minutes)

## Input Schema

```json
{
  "action": "string - Description of the proposed action",
  "resource": "string - Target resource identifier",
  "namespace": "string - Optional Kubernetes namespace",
  "agent": "string - Name of the requesting agent",
  "reason": "string - Justification for the action",
  "channel_name": "string - Approval channel (default: kubani-alerts)",
  "timeout_seconds": "number - How long to wait (default: 300)"
}
```

## Actions

### 1. Format Approval Request

Build the approval embed with context:

```yaml
embed:
  color: 16753920  # Orange - attention required
  title: "🔐 Approval Required"
  description: $action
  fields:
    - name: "Action"
      value: $action
      inline: false
    - name: "Resource"
      value: $resource
      inline: true
    - name: "Namespace"
      value: $namespace
      inline: true
    - name: "Requesting Agent"
      value: $agent
      inline: false
    - name: "Reason"
      value: $reason
      inline: false
  footer:
    text: "React with ✅ to approve or ❌ to reject"
  timestamp: $current_timestamp
```

### 2. Post Approval Request

Send the approval request to the specified Discord channel:

```yaml
mcp_tool: discord-mcp-server/send_message_to_channel_name
params:
  channel_name: $channel_name
  embed: $approval_embed
timeout: 30s
store_result: message_result
```