# AGENTS.md Validation Checklist

Use this checklist when creating or auditing an AGENTS.md file.

## Size Constraints

- [ ] Total lines < 300 (strict maximum)
- [ ] Total lines < 100 (recommended)
- [ ] Total lines < 60 (optimal)

## Content Quality

### Universality Check

For each instruction, ask: "Does this apply to EVERY task in this project?"

- [ ] No task-specific instructions (move to custom commands)
- [ ] No conditional logic ("if doing X, then Y")
- [ ] No role-specific content ("for frontend work..." / "for backend work...")
- [ ] No feature-specific details (move to agent_docs/)

### What NOT to Include

- [ ] No code style guidelines (use linters)
- [ ] No formatting rules (use formatters)
- [ ] No code snippets (use file:line pointers)
- [ ] No auto-generated content from init commands
- [ ] No detailed API documentation (move to agent_docs/)
- [ ] No database schema details (move to agent_docs/)
- [ ] No architecture diagrams in ASCII (move to agent_docs/)

### Three Pillars Present

- [ ] WHAT: Stack and technologies listed
- [ ] WHAT: Project structure documented
- [ ] WHY: Project purpose stated
- [ ] HOW: Essential commands provided
- [ ] HOW: Verification steps included

## Structure Quality

- [ ] Clear section headers
- [ ] Scannable format (lists, not prose)
- [ ] Commands are copy-pasteable
- [ ] No redundant information
- [ ] Consistent formatting throughout

## Progressive Disclosure

- [ ] agent_docs/ directory exists (or equivalent)
- [ ] AGENTS.md references agent_docs/ files
- [ ] Each reference has brief description
- [ ] No duplicated content between AGENTS.md and agent_docs/

## Common Anti-Patterns

Check that these are NOT present:

- [ ] "Always use X pattern when..." (conditional)
- [ ] "Code style: use single quotes..." (linter job)
- [ ] "Example implementation:" followed by code (snippet)
- [ ] "When working on the API..." (task-specific)
- [ ] Multi-paragraph explanations (too verbose)
- [ ] Commented-out sections (cruft)
- [ ] TODO items (not actionable by AI agent)

## Verification Script

Run this to check basic metrics:

```bash
#!/bin/bash
FILE="AGENTS.md"

if [ ! -f "$FILE" ]; then
    echo "AGENTS.md not found"
    exit 1
fi

LINES=$(wc -l < "$FILE")
WORDS=$(wc -w < "$FILE")
CODE_BLOCKS=$(grep -c '```' "$FILE" || echo 0)
CODE_BLOCKS=$((CODE_BLOCKS / 2))

echo "AGENTS.md Metrics"
echo "===================="
echo "Lines:        $LINES $([ $LINES -lt 100 ] && echo 'OK' || echo 'Consider reducing')"
echo "Words:        $WORDS"
echo "Code blocks:  $CODE_BLOCKS $([ $CODE_BLOCKS -lt 5 ] && echo 'OK' || echo 'Too many?')"

# Check for anti-patterns
echo ""
echo "Anti-Pattern Check"
echo "===================="

grep -n "always use\|when working on\|code style\|for example:" "$FILE" -i && echo "Possible anti-patterns found" || echo "No obvious anti-patterns"

# Check for agent_docs reference
echo ""
grep -q "agent_docs" "$FILE" && echo "References agent_docs/" || echo "No agent_docs/ reference found"
```

## Quick Fixes

| Problem | Fix |
|---------|-----|
| File too long | Extract to agent_docs/, keep only pointers |
| Style guidelines | Move to .eslintrc / ruff.toml / etc. |
| Code examples | Replace with file:line references |
| Task instructions | Create custom command |
| Conditional content | Split into separate agent_docs/ files |
| Verbose prose | Convert to bullet points or remove |
