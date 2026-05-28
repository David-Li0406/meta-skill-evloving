---

name: code-quality
description: AI Skill that enables coding agents to automatically learn, understand, and enforce code quality patterns within a codebase. The skill uses a sub-agent architecture for distributed pattern analysis, integrates with existing configuration files (ESLint, Prettier, etc.), and provides interactive MCQ-based confirmation flows for pattern resolution. Includes anti-pattern detection, code smell identification, and complexity metrics.

---

# Code Quality Skill

## Purpose

Enable coding agents to learn and enforce project-specific code quality patterns via automated scanning, config discovery, conflict resolution, anti-pattern detection, and persisted outputs.

## When to use

- User asks for code quality, coding patterns, style guide, conventions, consistency, linting rules, or code standards.
- Before generating code to align with existing patterns.
- After detecting inconsistent patterns or conflicting configs.
- During greenfield setup to seed best-practice configs.
- When reviewing code for potential issues or technical debt.
- To identify anti-patterns, code smells, or complexity hotspots.

## Inputs

| Parameter | Default | Description |
|-----------|---------|-------------|
| `root` | workspace root | Root directory to analyze |
| `directories` | auto-detect | Specific directories or glob patterns |
| `thoroughness` | medium | Analysis depth: `quick` \| `medium` \| `thorough` |
| `resume_from` | — | Agent ID for resumable runs |
| `include_antipatterns` | true | Enable anti-pattern detection |
| `include_metrics` | true | Enable code metrics collection |

## Outputs

- **patterns.md** — Detailed pattern report
- **.code-quality.json** — Machine-readable patterns and rules
- **Linter suggestions** — ESLint/Prettier config fragments
- **Anti-pattern report** — Code smells and complexity issues
- **Metrics summary** — LOC, function lengths, nesting depths
- **Conflict MCQs** — Interactive resolution for ambiguous patterns

## OS detection (run once per session)

- Unix/macOS: `uname -s` => Linux/Darwin; prefer bash/zsh; use jq for JSON if available.
- Windows: `$env:OS` => Windows_NT; use PowerShell JSON cmdlets.
- If jq is unavailable on Unix, fall back to Node.js one-liner merges.

## Workflow

### Phase 1: Configuration Discovery (config-reader agent)
- Scan for ESLint, Prettier, EditorConfig, TSConfig, pyproject, etc.
- Normalize rules; detect conflicts (indent, semi, quotes, line endings, strictness).
- Build priority-ordered rule set.

### Phase 2: Distributed Pattern Scanning (pattern-scanner agents)
- For each major directory (src, lib, apps, packages, tests): spawn haiku agent.
- **Structure analysis**: File organization, module boundaries, dependency flow.
- **Pattern detection**: Naming, imports, API calls, state management, components, errors, tests, docs.
- **Anti-pattern detection**: Code smells, complexity, coupling, duplication, security issues.
- **Metrics collection**: LOC, function length, nesting depth, import counts.

### Phase 3: Consolidation & Scoring
- Merge pattern data from all agents.
- Compute confidence scores using multi-factor algorithm:
  - Occurrence frequency (25%)
  - Consistency ratio (25%)
  - File coverage (20%)
  - Recency weight (10%)
  - Author distribution (8%)
  - Context consistency (7%)
  - Config alignment (5%)
- Tag confidence tiers: High (85-100), Medium-High (70-84), Medium (50-69), Low (25-49), Very Low (0-24).

### Phase 4: Conflict & Ambiguity Resolution (conflict-resolver agent)
- If conflicts or medium confidence: invoke sonnet agent to craft MCQs.
- Provide pros/cons and recommended option.
- Offer "Dig Deeper" when 5+ variations exist.
- Allow custom responses.

### Phase 5: Output Generation
- Write **patterns.md** using template.
- Write or merge **.code-quality.json** with:
  - Confirmed/detected/custom patterns
  - Custom rules
  - Excluded paths
  - Integration settings
  - Anti-pattern baseline
- Generate recommended linter/formatter rule changes.
- Create anti-pattern report with severity levels and fix suggestions.

## Thoroughness Levels

| Level | Description | Use Case |
|-------|-------------|----------|
| `quick` | Config scan + top-level patterns only | Pre-commit checks, CI gates |
| `medium` | Full pattern scan, sampling for metrics | Regular analysis, code reviews |
| `thorough` | Deep analysis, all files, full metrics | Initial setup, major refactors |

## Resumable sessions

- Each pattern-scanner returns agent_id and optional checkpoint.
- Resume interrupted scans with `resume_from` parameter.
- Checkpoints: `phase_1_complete`, `phase_2_partial`, `phase_3_complete`, etc.

## Best-practice source priority

1. User-defined (.code-quality.json custom_rules)
2. Project configs (EditorConfig > ESLint > Prettier > TSConfig > language-specific)
3. Detected patterns (high confidence)
4. Model inference for stack version
5. Industry standards for detected framework/library

## Interaction rules

- **Read-only** on source files; only write output files.
- **MCQ confirmation** for medium confidence or conflicts.
- **Auto-apply** only for high confidence patterns.
- **Context-aware**: respect boundaries (auth vs public, tests vs prod, components vs utils).
- **Persist decisions** to .code-quality.json for future runs.

## File conventions

- Outputs live at repo root unless user specifies otherwise.
- Default exclusions: node_modules, dist, build, coverage, .git, vendor, __pycache__, tmp.

## Error handling

- If config parse fails: report file and error; continue scanning others.
- If no patterns detected (<100 LOC): switch to greenfield flow with best-practice bundle.
- If agent fails: log checkpoint; allow resume from last known state.
- Surface all errors in final report with suggested remediation.

## Anti-Pattern Severity Levels

| Level | Score | Action Required |
|-------|-------|-----------------|
| Critical | >1.5 | Must fix before merge |
| High | 1.0-1.5 | Should fix, warn in report |
| Medium | 0.5-1.0 | Note in report |
| Low | <0.5 | Informational only |
