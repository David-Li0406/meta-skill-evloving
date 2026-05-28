---
name: live-test
description: Run comprehensive live API tests against Honeycomb. Manages test environments, validates documentation snippets, and tests CRUD operations. Use when you need to verify the SDK against the real API.
allowed-tools: Bash(direnv exec:*), Bash(poetry run:*), Read, Grep, Glob, Write
---

# Live API Testing Skill

This skill provides comprehensive integration testing against the real Honeycomb API.

## Prerequisites

1. **Management Key** - Set in `.envrc`:
   ```bash
   cp .envrc.example .envrc
   # Edit .envrc with your management key
   direnv allow
   ```

2. **Or Direct API Key** - For simpler testing without environment creation

## Quick Start

```bash
# Run full test suite
direnv exec . poetry run python scripts/test_live_api.py

# Verify API key credentials (v1 auth)
direnv exec . bash -c 'curl -s -H "X-Honeycomb-Team: $HONEYCOMB_API_KEY" https://api.honeycomb.io/1/auth | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"API Key: {d[\"type\"]} for team {d[\"team\"][\"slug\"]}, env {d[\"environment\"][\"slug\"]}\")"'

# Verify management key credentials (v2 auth)
direnv exec . bash -c 'curl -s -H "Authorization: Bearer $HONEYCOMB_MANAGEMENT_KEY:$HONEYCOMB_MANAGEMENT_SECRET" https://api.honeycomb.io/2/auth | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"Management Key: {d[\"data\"][\"attributes\"][\"name\"]} for team {d[\"data\"][\"relationships\"][\"team\"][\"data\"][\"id\"]}\")"'
```

## Test Scopes

| Scope | Description |
|-------|-------------|
| `all` | Full suite: environment setup, CRUD, doc snippets |
| `crud` | CRUD tests for all resources |
| `docs` | Documentation snippet validation only |
| `triggers` | Test triggers resource only |
| `queries` | Test queries resource only |
| (etc) | Any resource name |

## Session Management

The live-tester agent manages test sessions:

1. **New session**: Creates environment + API key via Management API
2. **Resume session**: Reuses existing credentials from `.claude/secrets/`
3. **Cleanup**: Deletes test resources and environments

Session state is stored in:
- `.claude/secrets/session.json` - Environment/key IDs (no secrets)
- `.claude/secrets/test.env` - The actual API key (gitignored)

## Resource Dependency Order

Tests run in this order to satisfy dependencies:

```
1. Dataset
2. Columns
3. Events (+ 30s wait for ingestion)
4. Recipients, Queries
5. Triggers, Boards, SLOs, Markers
6. Burn Alerts
```

## What Gets Tested

### CRUD Operations
- Create with Builder pattern (where applicable)
- Create with manual/dict pattern
- Read (get by ID)
- Update
- Delete + verify deletion

### Documentation Snippets
- Extracts Python code blocks from `docs/usage/*.md`
- Substitutes placeholders with real test values
- Executes both complete and partial snippets
- Reports which docs have bugs

## Security

- Credentials loaded via direnv (never hardcoded)
- Secrets stored only in `.claude/secrets/` (gitignored)
- Session files contain IDs only, not secrets
- Keys never printed to console
