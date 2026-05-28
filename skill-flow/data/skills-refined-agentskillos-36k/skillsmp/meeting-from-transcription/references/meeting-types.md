# Meeting Types

Valid values for the `meeting_type` argument.

## Enum Values

| Type | Description | Inference Signals |
|------|-------------|-------------------|
| `1-on-1` | Two people, personal/career discussion | Names mentioned, "1:1", "check-in", "career", "feedback" |
| `standup` | Quick status updates, blockers | "standup", "blockers", "yesterday", "today", "sync" |
| `planning` | Sprint planning, roadmap, scoping | "sprint", "planning", "backlog", "estimate", "roadmap", "scope" |
| `retro` | Retrospective | "retro", "retrospective", "went well", "improve", "action items" |
| `review` | Code/design review, demo | "review", "demo", "feedback", "PR", "pull request", "design" |
| `interview` | Job interview | "candidate", "interview", "role", "hiring", "position" |
| `stakeholder` | External stakeholders, business updates | "stakeholder", "client", "customer", "partner", "executive" |
| `general` | Default fallback | When none of the above patterns match |

## Inference Priority

1. Check for explicit meeting type mentions ("this is a standup", "retro meeting")
2. Look for characteristic vocabulary (see signals above)
3. Consider participant count (two people likely = 1-on-1)
4. Default to `general` if uncertain

## Override

User can specify `--type <TYPE>` to override inference:

```
/meeting-from-transcription transcription.md --type planning
```

The override takes precedence over any inference.
