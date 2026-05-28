---
name: continuous-learning
description: Automatically extract reusable patterns from Claude Code sessions and save them as learned skills for future use.
---

# Continuous Learning Skill

Automatically evaluates Claude Code sessions to extract reusable patterns that can be saved as learned skills.

## How It Works

This skill runs as a **Stop hook** at the end of each session:

1. **Session Evaluation**: Checks if the session has enough messages (default: 10+).
2. **Pattern Detection**: Identifies extractable patterns from the session.
3. **Skill Extraction**: Saves useful patterns to a specified path.

## Configuration

Edit `config.json` to customize:

```json
{
  "min_session_length": 10,
  "extraction_threshold": "medium",
  "auto_approve": false,
  "learned_skills_path": "~/.claude/skills/learned/",
  "patterns_to_detect": [
    "error_resolution",
    "user_corrections",
    "workarounds",
    "debugging_techniques",
    "project_specific"
  ],
  "ignore_patterns": [
    "simple_typos",
    "one_time_fixes",
    "external_api_issues"
  ]
}
```

## Pattern Types

| Pattern                | Description                           |
|------------------------|---------------------------------------|
| `error_resolution`     | How specific errors were resolved     |
| `user_corrections`     | Patterns from user corrections        |
| `workarounds`          | Solutions to framework/library quirks |
| `debugging_techniques` | Effective debugging approaches        |
| `project_specific`     | Project-specific conventions          |

## Hook Setup

Add to your `~/.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/continuous-learning/evaluate-session.sh"
      }]
    }]
  }
}
```

## Why Stop Hook?

- **Lightweight**: Runs once at session end.
- **Non-blocking**: Doesn't add latency to every message.
- **Complete context**: Has access to the full session transcript.

## Related

- [The Longform Guide](https://x.com/affaanmustafa/status/2014040193557471352) - Section on continuous learning.
- `/learn` command - Manual pattern extraction mid-session.

## Philosophy

Every session is a learning opportunity:
- Error resolutions → Future prevention
- User corrections → Preference learning
- Workarounds → Knowledge base
- Debugging techniques → Reusable strategies
- Project-specific patterns → Team knowledge

## Confidence Scoring

Patterns are scored for reliability based on various factors, including base score, frequency, recency, and source reliability.

### Confidence Thresholds

| Level | Score | Treatment |
|-------|-------|-----------|
| High  | 0.85+ | Apply automatically |
| Medium| 0.65-0.84 | Suggest with context |
| Low   | 0.40-0.64 | Available for search |
| Experimental | <0.40 | Flag for review |

## Best Practices

### DO
1. Review high-frequency patterns.
2. Adjust confidence when wrong.
3. Export valuable patterns.
4. Clean stale patterns.
5. Categorize correctly.

### DON'T
1. Trust low-confidence blindly.
2. Store one-time fixes.
3. Keep outdated patterns.
4. Ignore user corrections.
5. Over-generalize.

## Privacy & Security

### Sensitive Data Handling
Patterns never stored:
- API keys, tokens, secrets
- Passwords or credentials
- Personal information

### Local Storage Only
All learnings stored locally and not synced to the cloud by default.