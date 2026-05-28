# Severity Classification

## CRITICAL (Blocks AI effectiveness)

Must fix - AI cannot work effectively without these:

- Missing CLAUDE.md/AGENTS.md
- Missing README.md
- Hardcoded secrets found
- No .gitignore
- Circular dependencies
- No tests at all
- Files >1000 LOC

## WARNING (Impacts efficiency)

Should fix - AI works but inefficiently:

- Incomplete agent instructions
- Missing ARCHITECTURE.md
- Test coverage <50%
- No type safety
- No llms.txt
- Missing ASK FIRST boundaries

## INFO (Optimization opportunities)

Nice to have - minor improvements:

- Missing CONTRIBUTING.md
- Could add more why-comments
- Missing executable specs
- No architecture enforcement
- No AI commit attribution
- >200 instructions (consider trimming)
