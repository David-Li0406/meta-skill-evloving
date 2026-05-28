# Specialist Briefs

Prompts for each ecosystem-audit specialist.

## CLI Validator

```
<role>CLI validator specialist</role>
<context>
You are validating a CLI tool against its documentation.
CLI: {{cli_name}}
Rule file: ~/.agents/rules/{{cli_name}}.md
</context>
<task>
1. Run {{cli_name}} --help and capture output
2. Compare documented flags to actual flags in --help
3. Test 2-3 documented command examples
4. Identify any discrepancies between docs and reality
</task>
<output_contract>
{
  "cli": "{{cli_name}}",
  "status": "pass | warn | fail",
  "help_matches_docs": true | false,
  "tested_examples": [
    {"command": "...", "result": "pass | fail", "note": "..."}
  ],
  "discrepancies": [
    {"type": "missing_flag | wrong_output | broken_example", "details": "..."}
  ],
  "recommendations": [],
  "confidence": 8
}
</output_contract>
```

## Skill Validator

```
<role>Skill validator specialist</role>
<context>
You are validating a Claude Code skill's structure and quality.
Skill: {{skill_name}}
Path: ~/.agents/skills/{{skill_name}}/
</context>
<task>
1. Check SKILL.md exists and has valid frontmatter
2. Verify description starts with "This skill should be used when..."
3. Check for required sections (when to use, workflow, tool integration)
4. Count lines and compare to complexity tier
5. Verify references are linked and exist
</task>
<output_contract>
{
  "skill": "{{skill_name}}",
  "status": "pass | warn | fail",
  "structure": {
    "has_skill_md": true | false,
    "has_frontmatter": true | false,
    "has_description": true | false,
    "line_count": 0,
    "complexity_tier": "simple | medium | full-featured"
  },
  "sections_present": ["when to use", "workflow", ...],
  "sections_missing": [],
  "issues": [],
  "recommendations": [],
  "confidence": 8
}
</output_contract>
```

## Rule Validator

```
<role>Rule validator specialist</role>
<context>
You are validating CLI documentation accuracy.
CLI: {{cli_name}}
Rule file: ~/.agents/rules/{{cli_name}}.md
</context>
<task>
1. Read the rule file content
2. Run {{cli_name}} --help
3. Compare documented commands/flags to actual
4. Identify outdated or incorrect documentation
</task>
<output_contract>
{
  "cli": "{{cli_name}}",
  "rule_file": "{{cli_name}}.md",
  "status": "pass | warn | fail",
  "accuracy": {
    "documented_commands_exist": true | false,
    "flags_match": true | false,
    "examples_work": true | false
  },
  "drift_detected": [
    {"type": "missing_command | wrong_flag | outdated_example", "details": "..."}
  ],
  "recommendations": [],
  "confidence": 8
}
</output_contract>
```

## Prompt Validator

```
<role>Prompt validator specialist</role>
<context>
You are validating the prompts CLI and command library.
</context>
<task>
1. Run prompts commands list --json -q
2. For each command, test export functionality
3. Check @file resolution works
4. Verify key commands exist (/prime, /map, /tdd, etc.)
</task>
<output_contract>
{
  "domain": "prompts",
  "status": "pass | warn | fail",
  "command_count": 0,
  "key_commands": {
    "/prime": "present | missing",
    "/map": "present | missing",
    "/tdd": "present | missing",
    "/agent": "present | missing"
  },
  "export_works": true | false,
  "at_file_resolution": true | false,
  "issues": [],
  "recommendations": [],
  "confidence": 8
}
</output_contract>
```

## Role Validator

```
<role>Role validator specialist</role>
<context>
You are validating the roles CLI and persona library.
</context>
<task>
1. Run roles list --json -q
2. Check category coverage (design, engineering, architecture, philosophy, visionary)
3. Test export for key roles (jony, margaret, dieter, bret)
4. Verify groups work
</task>
<output_contract>
{
  "domain": "roles",
  "status": "pass | warn | fail",
  "role_count": 0,
  "categories": {
    "design": 0,
    "engineering": 0,
    "architecture": 0,
    "philosophy": 0,
    "visionary": 0
  },
  "key_roles": {
    "jony": "present | missing",
    "margaret": "present | missing",
    "dieter": "present | missing",
    "bret": "present | missing"
  },
  "export_works": true | false,
  "groups_work": true | false,
  "issues": [],
  "recommendations": [],
  "confidence": 8
}
</output_contract>
```

## Agent Validator

```
<role>Agent validator specialist</role>
<context>
You are validating agent CLI availability and basic functionality.
Agents: claude, codex, copilot
</context>
<task>
1. Check each agent CLI is on PATH
2. Verify --version works
3. Check basic invocation doesn't error
4. Note any configuration issues
</task>
<output_contract>
{
  "domain": "agents",
  "status": "pass | warn | fail",
  "agents": {
    "claude": {"on_path": true, "version": "...", "status": "ok | error"},
    "codex": {"on_path": true, "version": "...", "status": "ok | error"},
    "copilot": {"on_path": true, "version": "...", "status": "ok | error"}
  },
  "issues": [],
  "recommendations": [],
  "confidence": 8
}
</output_contract>
```

## Meta Validator

```
<role>Meta validator specialist</role>
<context>
You are validating ecosystem meta-documentation.
Files: ~/.agents/AGENTS.md, ~/.agents/GLOSSARY.md
</context>
<task>
1. Check AGENTS.md exists and is not stale
2. Check GLOSSARY.md references are valid
3. Verify CLI inventory matches reality
4. Check skill inventory matches ~/.agents/skills/
</task>
<output_contract>
{
  "domain": "meta",
  "status": "pass | warn | fail",
  "files": {
    "AGENTS.md": {"exists": true, "last_modified": "...", "stale": false},
    "GLOSSARY.md": {"exists": true, "last_modified": "...", "stale": false}
  },
  "inventory_accuracy": {
    "clis_documented": 0,
    "clis_actual": 0,
    "skills_documented": 0,
    "skills_actual": 0
  },
  "issues": [],
  "recommendations": [],
  "confidence": 8
}
</output_contract>
```

## Specialist Invocation Pattern

```bash
# Generic pattern for specialist invocation
SPECIALIST_PROMPT=$(cat <<'EOF'
<role>{{role}}</role>
<context>{{context}}</context>
<task>{{task}}</task>
<output_contract>{{schema}}</output_contract>
EOF
)

echo "$SPECIALIST_PROMPT" | copilot -p --model gemini-3-pro --output-format json
```

## Response Handling

```bash
# Parse specialist response
RESPONSE=$(copilot -p --model gemini-3-pro --output-format json <<< "$PROMPT")
STATUS=$(echo "$RESPONSE" | jq -r '.status')
CONFIDENCE=$(echo "$RESPONSE" | jq -r '.confidence')

# Route based on confidence
if [ "$CONFIDENCE" -lt 7 ]; then
  echo "Low confidence ($CONFIDENCE) - escalating to human"
fi
```
