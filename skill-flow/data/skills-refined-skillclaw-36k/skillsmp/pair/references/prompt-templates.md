# Prompt Templates

XML metaprompt templates for each pair mode. these templates enforce the output contract and ensure lean, structured responses.

## template architecture

```
┌─────────────────────────────────────────────────────────────┐
│ PROMPT GENERATION                                           │
│                                                             │
│ 1. select template (consult | delegate | review)            │
│ 2. inject context packet                                    │
│ 3. inject task-specific parameters                          │
│ 4. output contract is BAKED IN (not optional)               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ EXECUTION                                                   │
│                                                             │
│ codex:        cat prompt | codex exec - --full-auto -o out  │
│ copilot: cat prompt | copilot -p --output-format json │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ RESPONSE                                                    │
│                                                             │
│ { mode, status, summary, confidence, artifacts, ... }       │
│ ~200-500 tokens                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## consult template

for getting advice, analysis, or recommendations.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<metaprompt name="pair-consult" version="1.0">

  <role>
    Senior technical advisor providing analysis and recommendations.
    You think deeply but respond concisely.
  </role>

  <context>
    <codebase>
      {{CODEBASE_CONTEXT}}
      <!-- layer output, relevant file summaries -->
    </codebase>

    <session>
      {{SESSION_CONTEXT}}
      <!-- issue ID, current phase, recent actions -->
    </session>

    <question>
      {{QUESTION}}
    </question>
  </context>

  <instructions>
    1. Analyze the question in context of the codebase
    2. Consider multiple approaches if relevant
    3. Provide a clear recommendation with reasoning
    4. Rate your confidence honestly

    DO NOT:
    - Include your exploration process in the response
    - Return anything other than the JSON schema below
    - Hedge excessively - commit to a recommendation
  </instructions>

  <output_contract>
    CRITICAL: Your ENTIRE response must be this JSON structure.
    No text before. No text after. No markdown wrapper.

    {
      "mode": "consult",
      "status": "success",
      "summary": "50-200 words: your recommendation and key reasoning",
      "confidence": 8,
      "artifacts": [
        {
          "type": "analysis",
          "content": "## Analysis\n\n[detailed analysis in markdown]\n\n## Recommendation\n\n[clear recommendation]"
        }
      ],
      "next_steps": ["optional follow-up actions"],
      "escalate": false
    }

    If blocked or need clarification:
    {
      "mode": "consult",
      "status": "blocked",
      "summary": "Cannot provide recommendation because...",
      "confidence": 3,
      "artifacts": [],
      "blockers": ["what's missing"],
      "escalate": true,
      "escalate_reason": "Need human input on X"
    }
  </output_contract>

</metaprompt>
```

### consult quick (copilot)

```bash
cat <<'PROMPT' | copilot -p --model gemini-3-pro --output-format json
<role>Technical advisor. Concise analysis.</role>

<context>
{{CONTEXT_PACKET_JSON}}
</context>

<question>{{QUESTION}}</question>

<output_contract>
Respond with ONLY this JSON:
{
  "mode": "consult",
  "status": "success",
  "summary": "50-100 words",
  "confidence": 1-10,
  "artifacts": [{"type": "analysis", "content": "your analysis"}],
  "next_steps": [],
  "escalate": false
}
</output_contract>
PROMPT
```

### consult thorough (codex)

```bash
cat <<'PROMPT' > /tmp/consult-prompt.md
<role>Senior technical advisor with deep expertise.</role>

<context>
<codebase>
$(layer . --format=json 2>/dev/null | head -100)
</codebase>

<session>
{{SESSION_CONTEXT}}
</session>

<question>
{{QUESTION}}
</question>
</context>

<instructions>
1. Thoroughly analyze the question
2. Consider trade-offs and alternatives
3. Provide definitive recommendation
4. Be honest about confidence level
</instructions>

<output_contract>
CRITICAL: Respond with ONLY this JSON. Nothing else.

{
  "mode": "consult",
  "status": "success | blocked",
  "summary": "100-200 words",
  "confidence": 1-10,
  "artifacts": [
    {
      "type": "analysis",
      "content": "## Analysis\n\n[detailed]\n\n## Options\n\n[if multiple]\n\n## Recommendation\n\n[clear choice]"
    }
  ],
  "next_steps": ["follow-up actions"],
  "escalate": false
}
</output_contract>
PROMPT

cat /tmp/consult-prompt.md | codex exec - --full-auto -o /tmp/consult-response.json --json
```

---

## delegate template

for handing off implementation work.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<metaprompt name="pair-delegate" version="1.0">

  <role>
    Senior engineer executing delegated implementation task.
    You implement thoroughly but report concisely.
  </role>

  <context>
    <codebase>
      {{CODEBASE_CONTEXT}}
    </codebase>

    <task>
      {{TASK_DESCRIPTION}}
    </task>

    <constraints>
      {{PATTERNS_TO_FOLLOW}}
      {{THINGS_TO_AVOID}}
    </constraints>

    <verification>
      {{TEST_COMMANDS}}
      {{SUCCESS_CRITERIA}}
    </verification>
  </context>

  <instructions>
    1. Explore codebase to understand patterns (use layer, outline)
    2. Implement the requested changes
    3. Verify with provided commands
    4. Report results in structured format

    DO NOT:
    - Include exploration logs in response
    - Return partial work without noting it
    - Skip verification steps
  </instructions>

  <output_contract>
    CRITICAL: Your ENTIRE response must be this JSON structure.

    {
      "mode": "delegate",
      "status": "success | partial | blocked | failed",
      "summary": "100-200 words: what was implemented, verification results",
      "confidence": 8,
      "artifacts": [
        {
          "type": "code",
          "path": "path/to/file.ts",
          "language": "typescript",
          "content": "// summary of changes or key code"
        }
      ],
      "next_steps": ["remaining work if partial"],
      "blockers": ["if blocked"],
      "escalate": false
    }
  </output_contract>

</metaprompt>
```

### delegate quick (copilot)

for small, focused changes.

```bash
cat <<'PROMPT' | copilot -p --model gemini-3-pro --output-format json
<role>Engineer implementing focused change.</role>

<task>{{TASK}}</task>

<context>
{{RELEVANT_FILE_CONTENT}}
</context>

<constraints>
- Follow existing patterns
- {{SPECIFIC_CONSTRAINTS}}
</constraints>

<output_contract>
Respond with ONLY:
{
  "mode": "delegate",
  "status": "success | partial | blocked",
  "summary": "50-100 words",
  "confidence": 1-10,
  "artifacts": [{"type": "code", "path": "file.ts", "content": "changes"}],
  "next_steps": []
}
</output_contract>
PROMPT
```

### delegate thorough (codex)

for substantial implementation work.

```bash
cat <<'PROMPT' > /tmp/delegate-prompt.md
<role>
Senior engineer with full codebase access.
Implement thoroughly, verify completely, report concisely.
</role>

<codebase>
$(layer . --format=json 2>/dev/null | head -100)

Key files:
$(outline {{RELEVANT_PATHS}} --format=yaml 2>/dev/null | head -200)
</codebase>

<task>
{{DETAILED_REQUIREMENTS}}
</task>

<patterns>
Reference implementations:
- {{PATTERN_FILE_1}}
- {{PATTERN_FILE_2}}

Avoid:
- {{ANTI_PATTERN_1}}
- {{ANTI_PATTERN_2}}
</patterns>

<verification>
Commands to run:
\`\`\`bash
{{TEST_COMMAND}}
{{BUILD_COMMAND}}
\`\`\`

Success criteria:
- {{CRITERION_1}}
- {{CRITERION_2}}
</verification>

<output_contract>
CRITICAL: After completing work, respond with ONLY this JSON.
Do not include exploration logs, thinking, or intermediate steps.

{
  "mode": "delegate",
  "status": "success | partial | blocked | failed",
  "summary": "100-200 words: what was done, verification results",
  "confidence": 1-10,
  "artifacts": [
    {
      "type": "code",
      "path": "path/to/created/file.ts",
      "language": "typescript",
      "content": "// key implementation or diff summary"
    }
  ],
  "next_steps": ["if partial, what remains"],
  "blockers": ["if blocked, what's needed"],
  "escalate": false
}
</output_contract>
PROMPT

cat /tmp/delegate-prompt.md | codex exec - --full-auto -o /tmp/delegate-response.json --json
```

---

## review template

for code review and validation.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<metaprompt name="pair-review" version="1.0">

  <role>
    Senior code reviewer auditing for correctness, security, and quality.
    You review thoroughly but report structured findings.
  </role>

  <context>
    <changes>
      {{DIFF_OR_PR_SUMMARY}}
    </changes>

    <codebase>
      {{RELEVANT_CODEBASE_CONTEXT}}
    </codebase>
  </context>

  <audit_dimensions>
    1. Correctness: logic errors, edge cases, null hazards
    2. Security: injection, auth bypass, secrets exposure
    3. Performance: N+1 queries, hot paths, memory leaks
    4. Maintainability: naming, dead code, complexity
    5. Tests: coverage gaps, missing assertions
  </audit_dimensions>

  <instructions>
    1. Review all changes against audit dimensions
    2. Categorize issues by severity (blocking vs suggestion)
    3. Provide specific, actionable feedback
    4. Rate merge readiness
  </instructions>

  <output_contract>
    CRITICAL: Respond with ONLY this JSON.

    {
      "mode": "review",
      "status": "success",
      "summary": "100-200 words: overall assessment, merge readiness score",
      "confidence": 8,
      "artifacts": [
        {
          "type": "issues",
          "content": "## Blocking Issues\n\n[list with locations and fixes]\n\n## Suggestions\n\n[non-blocking improvements]\n\n## Merge Readiness: X/10"
        }
      ],
      "next_steps": ["fixes needed before merge"],
      "escalate": false
    }
  </output_contract>

</metaprompt>
```

### review quick (copilot)

for progress checks and sanity validation.

```bash
cat <<'PROMPT' | copilot -p --model gemini-3-pro --output-format json
<role>Code reviewer doing quick validation.</role>

<changes>
Task: {{TASK_DESCRIPTION}}
Files: {{FILE_LIST}}
Tests: {{TEST_STATUS}}
</changes>

<check>
1. Requirements met?
2. Tests adequate?
3. Obvious issues?
</check>

<output_contract>
{
  "mode": "review",
  "status": "success",
  "summary": "50-100 words",
  "confidence": 1-10,
  "artifacts": [{"type": "issues", "content": "issues or 'LGTM'"}],
  "next_steps": []
}
</output_contract>
PROMPT
```

### review thorough (codex)

for PR review before merge.

```bash
cat <<'PROMPT' > /tmp/review-prompt.md
<role>
Senior reviewer performing comprehensive audit.
Security, correctness, performance, maintainability.
</role>

<pr>
Title: {{PR_TITLE}}
Files changed: {{FILE_COUNT}}
Additions: {{ADDITIONS}}
Deletions: {{DELETIONS}}

Diff summary:
$(outline --pr={{PR_NUMBER}} --format=yaml 2>/dev/null)

Full diff:
$(git diff {{BASE}}...{{HEAD}} --stat)
</pr>

<audit_checklist>
- [ ] Correctness: logic, edge cases, error handling
- [ ] Security: OWASP top 10, auth, secrets
- [ ] Performance: queries, algorithms, caching
- [ ] Tests: coverage, assertions, edge cases
- [ ] Maintainability: naming, complexity, docs
</audit_checklist>

<output_contract>
CRITICAL: Respond with ONLY this JSON.

{
  "mode": "review",
  "status": "success",
  "summary": "100-200 words: overall assessment, key findings, merge readiness X/10",
  "confidence": 1-10,
  "artifacts": [
    {
      "type": "issues",
      "content": "## Blocking Issues\n\n1. **Issue** (severity)\n   - Location: `file:line`\n   - Problem: ...\n   - Fix: ...\n\n## Suggestions\n\n[non-blocking]\n\n## Merge Readiness: X/10"
    }
  ],
  "next_steps": ["required before merge"],
  "escalate": false
}
</output_contract>
PROMPT

cat /tmp/review-prompt.md | codex exec - --full-auto -o /tmp/review-response.json --json
```

---

## group template

for parallel multi-model synthesis.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<metaprompt name="pair-group" version="1.0">

  <role>
    Expert providing perspective on complex question.
    One of multiple models being consulted in parallel.
  </role>

  <context>
    {{SHARED_CONTEXT}}
  </context>

  <question>
    {{QUESTION}}
  </question>

  <instructions>
    1. Analyze from your unique perspective
    2. Identify insights others might miss
    3. Be specific about confidence and uncertainty
    4. Note any concerns or risks
  </instructions>

  <output_contract>
    {
      "mode": "consult",
      "status": "success",
      "summary": "your key insight in 50-100 words",
      "confidence": 1-10,
      "artifacts": [
        {
          "type": "analysis",
          "content": "## Perspective\n\n[your analysis]\n\n## Unique Insight\n\n[what you see that others might miss]\n\n## Concerns\n\n[risks or gaps]"
        }
      ],
      "escalate": false
    }
  </output_contract>

</metaprompt>
```

### group execution pattern

```bash
# prepare shared prompt
cat > /tmp/group-prompt.md << 'PROMPT'
{{GROUP_TEMPLATE_WITH_CONTEXT}}
PROMPT

# launch all 3 in parallel
# 1. opus via Task tool (claude code), run_in_background=true
# 2. gemini via copilot
cat /tmp/group-prompt.md | copilot -p --model gemini-3-pro --output-format json > /tmp/gemini-response.json &
GEMINI_PID=$!

# 3. gpt via codex
cat /tmp/group-prompt.md | codex exec - --full-auto -o /tmp/gpt-response.json --json &
GPT_PID=$!

# wait for external agents
wait $GEMINI_PID $GPT_PID

# read structured responses only
GEMINI=$(cat /tmp/gemini-response.json)
GPT=$(cat /tmp/gpt-response.json)
# OPUS from Task tool result

# synthesize: each response is ~200-500 tokens
# total context added: ~1000-1500 tokens (not 30K+)
```

---

## context packet schema

standard structure for session context in all templates:

```json
{
  "session": {
    "id": "uuid",
    "issue": "ARB-123",
    "started": "ISO timestamp"
  },
  "codebase": {
    "type": "convex + nextjs",
    "root": "/path/to/project",
    "layer": "layer output summary"
  },
  "progress": {
    "phase": "implement",
    "step": 3,
    "total": 5
  },
  "recent_actions": [
    "created auth provider",
    "added login mutation",
    "tests failing on logout"
  ],
  "current_focus": "fixing logout test failure"
}
```

---

## template selection

| signal | template | tier |
|--------|----------|------|
| "what do you think", "should I" | consult | quick or thorough |
| "implement", "build", "create" | delegate | thorough usually |
| "review", "check", "audit" | review | quick or thorough |
| "multiple perspectives", `pair group` | group | parallel |
| "quick" keyword | any | quick (copilot) |
| "thorough" keyword | any | thorough (codex) |

## anti-patterns

| pattern | problem | fix |
|---------|---------|-----|
| freeform prompts | unpredictable responses | use templates |
| missing output_contract | agent returns prose | always include contract |
| context bloat in prompt | wastes tokens | use structured packets |
| no verification section | delegate work unverified | always include verification |
| vague success criteria | unclear if done | be specific |
