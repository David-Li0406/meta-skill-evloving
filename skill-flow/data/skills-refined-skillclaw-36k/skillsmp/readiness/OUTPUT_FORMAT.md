# Output Format Specification

Visual ASCII report format with ANSI colors for terminal display.

## Color Scheme

| Score Range | Color | ANSI Code |
|-------------|-------|-----------|
| 80-100% | Green | `\x1b[32m` |
| 50-79% | Yellow | `\x1b[33m` |
| 0-49% | Red | `\x1b[31m` |
| Reset | - | `\x1b[0m` |

## Progress Bar Characters

- Filled: `█` (U+2588)
- Empty: `░` (U+2591)
- Bar width: 20 characters

## Report Structure

```
╔══════════════════════════════════════════════════════════════════╗
║                   AGENT READINESS REPORT                         ║
║                      {repository_name}                           ║
╠══════════════════════════════════════════════════════════════════╣
║  LEVEL: {level}          SCORE: {score}%          APPS: {count}  ║
╚══════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────┐
│ PILLAR OVERVIEW                                                 │
├─────────────────────────────────────────────────────────────────┤
│ Code Quality    ██████████████████░░ 90%  (9/10)  ✓            │
│ Build           ████████████░░░░░░░░ 60%  (6/10)  ⚠            │
│ Testing         ████████████████████ 100% (8/8)   ✓            │
│ Documentation   ████████░░░░░░░░░░░░ 40%  (4/10)  ✗            │
│ Dev Environment ██████████████░░░░░░ 70%  (7/10)  ⚠            │
│ Quality Gates   ████████████████░░░░ 80%  (8/10)  ✓            │
│ Security        ██████████░░░░░░░░░░ 50%  (5/10)  ⚠            │
│ Observability   ████████████████████ 100% (6/6)   ✓            │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ LEVEL PROGRESSION                                               │
├─────────────────────────────────────────────────────────────────┤
│ L1 Functional   ████████████████████ 100%  ✓ ACHIEVED          │
│ L2 Documented   ████████████████░░░░  82%  ✓ ACHIEVED          │
│ L3 Standardized ██████████████░░░░░░  72%  ⚠ IN PROGRESS       │
│ L4 Optimized    ████████░░░░░░░░░░░░  45%  ✗ NOT STARTED       │
│ L5 Autonomous   ░░░░░░░░░░░░░░░░░░░░   0%  ✗ NOT STARTED       │
└─────────────────────────────────────────────────────────────────┘
```

## Detailed Criteria Section

```
┌─────────────────────────────────────────────────────────────────┐
│ ▼ CODE QUALITY (90%)                                            │
├─────────────────────────────────────────────────────────────────┤
│ ✓ lint_config        Linter configured (ESLint)                │
│ ✓ type_check         TypeScript strict mode enabled            │
│ ✓ formatter          Prettier configured                        │
│ ✗ dead_code_analysis No dead code detection found              │
└─────────────────────────────────────────────────────────────────┘
```

## Status Icons

| Status | Icon | Meaning |
|--------|------|---------|
| Pass | `✓` | Criterion satisfied |
| Fail | `✗` | Criterion not met |
| Skip | `○` | Not applicable |
| Warning | `⚠` | Partial/needs attention |

## Priority Actions Section

```
┌─────────────────────────────────────────────────────────────────┐
│ TOP 5 PRIORITY ACTIONS                                          │
├─────────────────────────────────────────────────────────────────┤
│ 1. [HIGH] Add AGENTS.md                                         │
│    Document agent-specific instructions for autonomous use      │
│                                                                  │
│ 2. [HIGH] Configure test coverage thresholds                    │
│    Add coverage enforcement to prevent regression               │
│                                                                  │
│ 3. [MED]  Add pre-commit hooks                                  │
│    Prevent commits that fail linting or tests                   │
│                                                                  │
│ 4. [MED]  Document build commands                               │
│    Add build instructions to README or AGENTS.md                │
│                                                                  │
│ 5. [LOW]  Add CODEOWNERS file                                   │
│    Define code ownership for automated review assignment        │
└─────────────────────────────────────────────────────────────────┘
```

## Priority Levels

| Priority | Criteria |
|----------|----------|
| HIGH | L1-L2 criteria, blocks level progression |
| MED | L3 criteria, improves standardization |
| LOW | L4-L5 criteria, optimization opportunities |

## Footer

```
─────────────────────────────────────────────────────────────────
Generated: {timestamp}
Repository: {repo_path}
Apps analyzed: {app_count}
─────────────────────────────────────────────────────────────────
```
