# Output Contracts

standardized response schema for all external agent calls. the contract ensures predictable, lean responses that don't pollute the orchestrating agent's context.

## the problem

```
WITHOUT CONTRACT:
┌─────────────────────────────────────────────────────────────┐
│ claude code → pair → codex (30 min task)                    │
│                          ↓                                  │
│                    10-15K lines of reasoning                │
│                    exploration logs                         │
│                    file reads                               │
│                    thinking blocks                          │
│                          ↓                                  │
│                    ALL pulled into context                  │
│                          ↓                                  │
│                    context window destroyed                 │
└─────────────────────────────────────────────────────────────┘

WITH CONTRACT:
┌─────────────────────────────────────────────────────────────┐
│ claude code → pair → codex (30 min task)                    │
│                          ↓                                  │
│                    agent works internally                   │
│                    (reasoning stays private)                │
│                          ↓                                  │
│                    STRUCTURED JSON ONLY                     │
│                          ↓                                  │
│                    ~200-500 tokens returned                 │
└─────────────────────────────────────────────────────────────┘
```

## universal response schema

every external agent call MUST return this structure:

```json
{
  "mode": "consult | delegate | review",
  "status": "success | partial | blocked | failed",
  "summary": "50-200 words describing what was done/found",
  "confidence": 8,
  "artifacts": [
    {
      "type": "analysis | code | recommendation | decision | issues",
      "content": "the actual deliverable",
      "path": "optional/file/path.ts",
      "language": "typescript"
    }
  ],
  "next_steps": ["optional follow-up actions"],
  "blockers": ["issues preventing completion"],
  "escalate": false,
  "escalate_reason": "only if escalate=true"
}
```

## field definitions

### required fields

| field | type | description |
|-------|------|-------------|
| `mode` | enum | which mode was executed: consult, delegate, review |
| `status` | enum | outcome: success (done), partial (some done), blocked (can't proceed), failed (error) |
| `summary` | string | 50-200 word summary of what happened. human-readable. |
| `confidence` | 1-10 | how confident the agent is in the response |
| `artifacts` | array | the actual deliverables (see below) |

### artifact object

| field | type | required | description |
|-------|------|----------|-------------|
| `type` | enum | yes | analysis, code, recommendation, decision, issues |
| `content` | string | yes | the artifact content |
| `path` | string | no | file path if artifact is code that was written |
| `language` | string | no | programming language if code |

### optional fields

| field | type | description |
|-------|------|-------------|
| `next_steps` | string[] | suggested follow-up actions |
| `blockers` | string[] | what's preventing progress |
| `escalate` | boolean | should this escalate to HIL? |
| `escalate_reason` | string | why escalation needed |

## mode-specific schemas

### consult mode

primary artifact: analysis or recommendation

```json
{
  "mode": "consult",
  "status": "success",
  "summary": "Analyzed the authentication approach. JWT with refresh tokens is recommended over session cookies for this use case due to mobile client requirements.",
  "confidence": 9,
  "artifacts": [
    {
      "type": "analysis",
      "content": "## Options Evaluated\n\n### JWT + Refresh Tokens\n- Pros: stateless, mobile-friendly, scales horizontally\n- Cons: token revocation complexity\n\n### Session Cookies\n- Pros: simple, revocable\n- Cons: requires sticky sessions, doesn't work well for mobile\n\n## Recommendation\nJWT with refresh tokens. Use short-lived access tokens (15min) with refresh rotation."
    }
  ],
  "next_steps": ["implement token refresh endpoint", "add token rotation logic"]
}
```

### delegate mode

primary artifact: code or implementation summary

```json
{
  "mode": "delegate",
  "status": "success",
  "summary": "Implemented the user authentication flow. Created auth provider, login/logout mutations, and protected route wrapper. All tests passing.",
  "confidence": 9,
  "artifacts": [
    {
      "type": "code",
      "path": "convex/functions/auth.ts",
      "language": "typescript",
      "content": "// key implementation details or diff summary"
    },
    {
      "type": "code",
      "path": "packages/web/providers/AuthProvider.tsx",
      "language": "typescript",
      "content": "// key implementation details or diff summary"
    }
  ],
  "next_steps": ["add password reset flow", "implement OAuth providers"]
}
```

### review mode

primary artifact: issues list with ratings

```json
{
  "mode": "review",
  "status": "success",
  "summary": "Reviewed PR #123. Found 2 blocking issues (N+1 query, missing auth check) and 3 suggestions. Merge readiness: 6/10.",
  "confidence": 8,
  "artifacts": [
    {
      "type": "issues",
      "content": "## Blocking Issues\n\n1. **N+1 Query** (high severity)\n   - Location: `src/api/users.ts:45`\n   - Problem: fetching related data in loop\n   - Fix: use batch query or join\n\n2. **Missing Auth Check** (high severity)\n   - Location: `src/api/admin.ts:12`\n   - Problem: endpoint accessible without admin role\n   - Fix: add `requireAdmin` middleware\n\n## Suggestions\n\n1. Consider extracting validation logic\n2. Add test for edge case X\n3. Update API docs"
    }
  ],
  "next_steps": ["fix N+1 query", "add auth middleware", "re-request review"]
}
```

## status values

| status | meaning | typical response |
|--------|---------|------------------|
| `success` | task completed fully | proceed with results |
| `partial` | some progress made | iterate or accept partial |
| `blocked` | cannot proceed without input | check blockers, maybe escalate |
| `failed` | error or fundamental problem | escalate to HIL |

## confidence calibration

| confidence | meaning | action |
|------------|---------|--------|
| 9-10 | high certainty, verified | proceed |
| 7-8 | confident, minor caveats | proceed, note caveats |
| 5-6 | moderate confidence | consider escalation |
| 1-4 | low confidence | escalate to HIL |

## execution patterns

### codex (captures final response only)

```bash
# write prompt with embedded output contract
cat > /tmp/pair-prompt.md << 'PROMPT'
{metaprompt with output contract}
PROMPT

# execute with -o flag to capture final message
cat /tmp/pair-prompt.md | codex exec - --full-auto \
  -o /tmp/pair-response.json \
  --json

# read ONLY the structured response
RESPONSE=$(cat /tmp/pair-response.json)
```

key: `-o` writes the final message to file, not the full stream.

### copilot (captures JSON output)

```bash
# execute with JSON output format
RESPONSE=$(cat <<'PROMPT' | copilot -p --model gemini-3-pro --output-format json
{metaprompt with output contract}
PROMPT
)
```

key: `--output-format json` returns structured response.

## prompt injection pattern

every prompt MUST include this output contract block:

```xml
<output_contract>
  CRITICAL: Your ENTIRE response must be valid JSON matching this schema.
  Do NOT include any text before or after the JSON.
  Do NOT include reasoning, exploration logs, or intermediate steps.

  {
    "mode": "{mode}",
    "status": "success | partial | blocked | failed",
    "summary": "50-200 words describing what was done",
    "confidence": 1-10,
    "artifacts": [
      {
        "type": "{expected_artifact_type}",
        "content": "the deliverable",
        "path": "optional/file/path.ts",
        "language": "typescript"
      }
    ],
    "next_steps": ["optional"],
    "blockers": ["if any"],
    "escalate": false,
    "escalate_reason": "only if escalate=true"
  }

  REMEMBER: JSON only. No markdown wrapper. No explanation.
</output_contract>
```

## validation

after receiving response, validate:

```python
def validate_response(response: dict) -> bool:
    required = ["mode", "status", "summary", "confidence", "artifacts"]
    for field in required:
        if field not in response:
            return False

    if response["confidence"] < 1 or response["confidence"] > 10:
        return False

    if response["status"] not in ["success", "partial", "blocked", "failed"]:
        return False

    words = len(response["summary"].split())
    if words < 50 or words > 200:
        return False

    return True
```

## anti-patterns

| pattern | problem | fix |
|---------|---------|-----|
| no output contract in prompt | agent returns freeform text | always embed contract |
| using TaskOutput for codex | pulls 10K+ lines | use `-o` flag |
| accepting invalid JSON | unparseable responses | validate before using |
| ignoring status field | miss blocked/failed states | always check status first |
| ignoring confidence | miss low-confidence signals | route on confidence |
