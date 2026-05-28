---
name: council-gate
description: Use this skill for implementing an automated quality gate in CI/CD pipelines using LLM Council multi-model consensus.
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
  "verdict": "pass",
  "confidence": 0.85,
  "blocking_issues": [],
  "rationale": "All models agreed...",
  "exit_code": 0,
  "transcript_path": ".council/logs/2025-12-31T..."
}
```

## Example Usage

```bash
# Basic gate check
council-gate --snapshot $(git rev-parse HEAD)

# Security-focused gate
council-gate --rubric-focus Security --confidence-threshold 0.9

# Quick tier for faster feedback
council-gate --tier quick --timeout 60
```

## Progressive Disclosure

- **Level 1**: This metadata (~200 tokens)
- **Level 2**: Full instructions above (~800 tokens)
- **Level 3**: See `references/ci-cd-rubric.md` for CI/CD-specific scoring

## Related Skills

- `council-verify`: General verification
- `council-review`: Code review with feedback