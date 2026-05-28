# Code Quality Skill

## Purpose
Enable coding agents to learn and enforce project-specific code quality patterns via automated scanning, config discovery, conflict resolution, and persisted outputs.

## When to use
- User asks for code quality, coding patterns, style guide, conventions, consistency, linting rules, or code standards.
- Before generating code to align with existing patterns.
- After detecting inconsistent patterns or conflicting configs.
- During greenfield setup to seed best-practice configs.

## Inputs
- Root directory (default: workspace root).
- Optional: directories or glob patterns to scan; resume_from agentId for resumable runs; thoroughness (quick|medium|thorough).

## Outputs
- Pattern report (patterns.md)
- Generated/merged .code-quality.json
- Optional linter rule suggestions (e.g., ESLint flat config fragment)
- Conflict MCQs when confidence is medium or conflicting

## OS detection (run once per session)
- Unix/macOS: `uname -s` => Linux/Darwin; prefer bash/zsh; use jq for JSON if available.
- Windows: `$env:OS` => Windows_NT; use PowerShell JSON cmdlets.
- If jq is unavailable on Unix, fall back to Node.js one-liner merges.

## Workflow
1) Configuration discovery (config-reader)
   - Scan for ESLint, Prettier, EditorConfig, TSConfig, pyproject, etc.
   - Normalize rules; detect conflicts (indent, semi, quotes, line endings, strictness).
2) Distributed pattern scanning (pattern-scanner)
   - For each major directory (src, lib, apps, packages, tests): spawn haiku agent.
   - Collect occurrences, locations, examples by category (naming, imports, api_calls, state_management, component_structure, error_handling, testing, documentation).
3) Consolidation
   - Merge pattern data; compute scores (frequency, consistency_ratio, recency_weight, author_distribution).
   - Tag confidence tier: High (>=5 and >90%), Medium (>=5 and 70-90%), Low (<5 or <70%), Conflicting (multiple patterns with 5+ each).
4) Conflict handling
   - If conflicts or medium confidence: invoke conflict-resolver (sonnet) to craft MCQs with pros/cons and recommended option.
   - Offer Dig Deeper when 5+ variations exist.
5) Output generation
   - Write patterns.md using template.
   - Write or merge .code-quality.json (version 1.0) with confirmed/detected/custom patterns, custom_rules, excluded_paths, integrations.
   - Surface recommended linter/formatter rules aligned to configs and patterns.

## Resumable sessions
- Each pattern-scanner returns agent_id and optional checkpoint. Resume with resume_from.

## Best-practice source priority
1) User-defined (.code-quality.json custom_rules)
2) Project configs (EditorConfig > ESLint > Prettier > TSConfig > language-specific)
3) Detected patterns (high confidence)
4) Model inference for stack version
5) (Future) remote curated libraries

## Interaction rules
- Do not modify source files; operate read-only except when writing outputs.
- Prefer MCQ when confidence is medium or conflicts detected; auto-apply only for high confidence.
- Respect contextual boundaries (auth vs public, tests vs prod, components vs utils).
- Persist user decisions into .code-quality.json.

## File conventions
- Outputs live at repo root unless user specifies otherwise.
- Exclude node_modules, dist, build, coverage, .git by default.

## Error handling
- If config parse fails, report file and rule; continue scanning others.
- If no patterns detected (<100 LOC), switch to greenfield flow and propose best-practice bundle.
