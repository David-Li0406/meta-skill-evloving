---
name: bloat-detector
description: Use this skill to detect and eliminate codebase bloat through progressive analysis, focusing on dead code, duplication, complexity, and documentation issues.
---

# Bloat Detector

Systematically detect and eliminate codebase bloat through progressive analysis tiers.

## Bloat Categories

| Category          | Examples                                             |
| ----------------- | ---------------------------------------------------- |
| **Code**          | Dead code, God classes, Lava flow, duplication       |
| **AI-Generated**  | Tab-completion bloat, vibe coding, hallucinated deps |
| **Documentation** | Redundancy, verbosity, stale content, slop           |
| **Dependencies**  | Unused imports, dependency bloat, phantom packages   |
| **Git History**   | Stale files, low-churn code, massive single commits  |

## Quick Start

### Tier 1: Quick Scan (2-5 min, no tools)

```bash
/bloat-scan
```
Detects: Large files, stale code, old TODOs, commented blocks, basic duplication.

### Tier 2: Targeted Analysis (10-20 min, optional tools)

```bash
/bloat-scan --level 2 --focus code   # or docs, deps
```
Adds: Static analysis (Vulture/Knip), git churn hotspots, doc similarity.

### Tier 3: Deep Audit (30-60 min, full tooling)

```bash
/bloat-scan --level 3 --report audit.md
```
Adds: Cross-file redundancy, dependency graphs, readability metrics.

## When to Use

| Do                       | Don't                        |
| ------------------------ | ---------------------------- |
| Context usage > 30%      | Active feature development   |
| Quarterly maintenance    | Time-sensitive bugs          |
| Pre-release cleanup      | Codebase < 1000 lines        |
| Before major refactoring | Tools unavailable (Tier 2/3) |

## Confidence Levels

| Level  | Confidence | Action         |
| ------ | ---------- | -------------- |
| HIGH   | 90-100%    | Safe to remove |
| MEDIUM | 70-89%     | Review first   |
| LOW    | 50-69%     | Investigate    |

## Prioritization

```
Priority = (Token_Savings × 0.4) + (Maintenance × 0.3) + (Confidence × 0.2) + (Ease × 0.1)
```

## Module Architecture

**Tier 1** (always available):

- `@module:quick-scan` - Heuristics, no tools
- `@module:git-history-analysis` - Staleness, churn, vibe coding signatures

**Tier 2** (optional tools):

- `@module:code-bloat-patterns` - Anti-patterns (God class, Lava flow)
- `@module:ai-generated-bloat` - AI-specific patterns (Tab bloat, hallucinations)
- `@module:documentation-bloat` - Redundancy, readability, slop detection
- `@module:static-analysis-integration` - Vulture, Knip

**Shared**:

- `@module:remediation-types` - DELETE, REFACTOR, CONSOLIDATE, ARCHIVE

## Auto-Exclusions

Always excludes: `.venv`, `__pycache__`, `.git`, `node_modules`, `dist`, `build`, `vendor`.

Also respects: `.gitignore`, `.bloat-ignore`.

## Safety

- **Never auto-delete** - all changes require approval.
- **Dry-run support** - `--dry-run` for previews.
- **Backup branches** - created before bulk changes.

## Related

- `bloat-auditor` agent - Executes scans.
- `unbloat-remediator` agent - Safe remediation.
- `context-optimization` skill - MECW principles.