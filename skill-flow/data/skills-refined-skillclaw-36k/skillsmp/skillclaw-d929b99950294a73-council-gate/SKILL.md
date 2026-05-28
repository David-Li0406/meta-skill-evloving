---
name: council-gate
description: Use this skill when you need to implement an automated quality gate in CI/CD pipelines using LLM Council's multi-model consensus for approval workflows and quality checks.
---

# Council Gate Skill

Automated quality gate using multi-model consensus for CI/CD pipelines.

## When to Use

- Add AI-powered quality checks to GitHub Actions
- Automate PR approval workflows
- Gate deployments on multi-model verification
- Enforce quality standards in pipelines

## Exit Codes

| Code | Verdict | CI/CD Behavior |
|------|---------|----------------|
| `0` | PASS | Pipeline continues |
| `1` | FAIL | Pipeline fails |
| `2` | UNCLEAR | Pipeline pauses for human review |

## Transcript Location

All deliberations are saved for audit:

```
.council/logs/{timestamp}-{hash}/
├── request.json      # Input snapshot
├── stage1.json       # Model responses
├── stage2.json       # Peer reviews
├── stage3.json       # Synthesis
└── result.json       # Final verdict
```

## GitHub Actions Integration

```yaml
name: Council Quality Gate

on:
  pull_request:
    branches: [main, master]

jobs:
  council-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install LLM Council
        run: pip install 'llm-council-core[http]'

      - name: Run Council Gate
        env:
          OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
        run: |
          llm-council gate \
            --snapshot ${{ github.sha }} \
            --rubric-focus Security \
            --confidence-threshold 0.8

      - name: Upload Transcript
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: council-transcript
          path: .council/logs/
```

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `confidence_threshold` | 0.7 | Minimum confidence for PASS |
| `rubric_focus` | null | Focus area (Security, Performance) |
| `timeout` | 300s | Maximum execution time |
| `tier` | balanced | Council tier (quick, balanced, high) |

## Output Schema
```json
{
  "status": "string",
  "details": "string"
}
```