# Removed Opinionated Items from SKILL.md

## Previous Description
- Analyze any repository for AI agent development efficiency. Scores 8 key aspects (documentation, architecture, testing, type safety, agent instructions, file structure, context optimization, security) from 1-100 with ASCII progress bars. Evaluates 140 sub-criteria including E2E anti-flake practices, multi-agent configs (Cursor/Windsurf/Cline/Aider), MCP integration, Atomic Design patterns, Screenplay testing, and kebab-case conventions. Highlights problems by severity (Critical/Warning/Info), provides overall A-F grade, surveys user on issues to fix, then enters plan mode to create a phased refactoring roadmap. Use when evaluating repository readiness for AI-assisted development or preparing a codebase for Claude Code.

## Removed Criteria Rows
- (Transferred back into SKILL.md)

## Removed "How to check" Items
- (Transferred back into SKILL.md)

## Removed Severity/Classifications and Examples
- CRITICAL: Files over 1000 LOC
- WARNING: Files 500-1000 LOC; Deep nesting (>5 levels); >20 files per directory
- INFO: Files 400-500 LOC; Missing llms.txt; No llms-full.txt; No hierarchical context (router pattern); Missing prompts/ directory; No event-driven decoupling
- Example issue: [C2] File Structure: src/utils/helpers.ts has 1,247 lines (Impact: Too large for AI context window, hard to understand)
- Example issue: [W3] File Structure: src/components/ has 28 files (Impact: Hard to navigate, consider subdirectories)
- Example issue: [I1] Context Optimization: llms.txt is missing (Impact: No optimized entry point for AI tools)

## Removed Survey Items and Phase Mapping
- Warning prompt: [W3] Reorganize src/components/? (y/N)
- Info prompts: [I1] Create llms.txt? (y/N)
- Issue-to-Phase mapping entry: **Phase 1:** Create files (CLAUDE.md, llms.txt, .aiignore)
- Issue-to-Phase mapping entry: **Phase 2:** Split files
- Issue-to-Phase mapping entry: **Phase 3:** Implement event bus; add branded types

## Removed Roadmap Snippets
- Phase 1 task: Create llms.txt (Generate index; Include key entry points; Add navigation hints)
- Phase 2 task: Split large files (>500 LOC) with example breakdowns

## Removed Template
- llms.txt Template section

## Removed Quick Fixes
- [W1] Files over 500 LOC → split helpers.ts/date/string/validation
- [I1] Missing llms.txt → generate from current structure
