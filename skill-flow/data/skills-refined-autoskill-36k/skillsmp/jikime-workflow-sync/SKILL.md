---
name: jikime-workflow-sync
description: Documentation synchronization workflow specialist for code-to-docs sync, quality verification, and git operations
version: 1.0.0
tags: ["workflow", "sync", "documentation", "quality", "git", "living-docs"]
triggers:
  keywords: ["sync", "동기화", "documentation", "문서", "CODEMAP", "README", "commit"]
  phases: ["sync"]
  agents: ["manager-docs", "manager-quality", "manager-git"]
  languages: []
# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~2221
user-invocable: false
context: fork
agent: manager-docs
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - TodoWrite
---

# Documentation Synchronization Workflow

## Quick Reference

Documentation Synchronization provides a systematic approach for keeping documentation in sync with code changes. It follows the "Sync to Verify to Commit" philosophy.

Core Workflow Phases:

- Phase 0.5: Quality Verification (tests, linter, type checker)
- Phase 1: Analysis & Planning (git diff, documentation mapping)
- Phase 2: Execute Sync (document updates, SPEC status sync)
- Phase 3: Git Operations (commit, PR management)

When to Use Sync:

- After completing feature implementation
- Before creating pull requests
- When code structure changes significantly
- After SPEC completion
- During milestone completion

When NOT to Use Sync:

- During active development (sync after completion)
- For quick fixes without documentation impact
- When documentation is already up to date

---

## Core Philosophy

### Living Documentation Principle

Documentation should be generated from code as much as possible:

- Single Source of Truth: Code is authoritative
- Automated Generation: Minimize manual writing
- Freshness: Always include timestamps
- Traceability: Link docs to code locations

### Sync to Verify to Commit

The golden workflow ensures documentation quality:

- Sync: Update docs based on code changes
- Verify: Validate quality through TRUST 5
- Commit: Stage and commit documentation changes

---

## Phase 0.5: Quality Verification

Before syncing documentation, verify code quality.

### Language Detection

Detect project language by checking indicator files:

```yaml
python: [pyproject.toml, setup.py, requirements.txt]
typescript: [tsconfig.json, package.json with typescript]
javascript: [package.json]
go: [go.mod, go.sum]
rust: [Cargo.toml]
```

### Quality Tools by Language

| Language | Test | Lint | Type Check |
|----------|------|------|------------|
| Python | pytest | ruff | mypy/pyright |
| TypeScript | vitest/jest | eslint/biome | tsc --noEmit |
| JavaScript | vitest/jest | eslint/biome | - |
| Go | go test | golangci-lint | go vet |
| Rust | cargo test | cargo clippy | - |

### Quality Gate Criteria

```yaml
tests:
  required: true
  pass_rate: 100%

linter:
  required: true
  max_errors: 0
  max_warnings: 10

type_checker:
  required: language_specific
  max_errors: 0
```

### Failure Handling

When quality verification fails:

- Display failure details with specific errors
- Offer options: Fix issues, Skip verification, Abort sync
- Record skip decisions for audit trail

---

## Phase 1: Analysis & Planning

### Git Change Analysis

Analyze changes using git commands:

```bash
# Changed files since last commit
git diff --name-only HEAD

# Current status
git status --porcelain

# Recent commit messages (for context)
git log --oneline -10
```

### Documentation Mapping

Map code changes to documentation updates:

| Change Type | Documentation Action |
|-------------|---------------------|
| New file | Add to CODEMAP, update README if major |
| Modified file | Update relevant docs |
| Deleted file | Remove from CODEMAP |
| New API endpoint | Update API documentation |
| New feature | Update README features section |
| SPEC implementation | Update SPEC status |

### Sync Plan Generation

Create a sync plan documenting:

- Files requiring documentation updates
- New documents to create
- Documents to delete or mark as deprecated
- SPEC status changes

---

## Phase 2: Execute Sync

### Document Types

#### README.md

Project overview and setup guide:

```markdown
# Project Name

Brief description

## Quick Start
[Setup instructions]

## Architecture
See [docs/CODEMAPS/INDEX.md]

## Features
[Feature list with links to detailed docs]
```

#### CODEMAPS

Code architecture documentation:

```
docs/CODEMAPS/
├── INDEX.md       # Architecture overview
├── frontend.md    # Frontend structure
├── backend.md     # Backend structure
└── database.md    # Database schema
```

CODEMAP format:

```markdown
# [Domain] Codemap

**Last Updated:** YYYY-MM-DD
**Entry Points:** Main entry points

## Architecture
[ASCII diagram showing structure]

## Key Modules
| Module | Purpose | Exports | Dependencies |
|--------|---------|---------|--------------|

## Data Flow
[Description of data flow]
```

#### SPEC Status Sync

Update SPEC documents with implementation status:

```yaml
status_fields:
  - Status: Planning | In Progress | Completed
  - Progress: 0-100%
  - Last Updated: YYYY-MM-DD
  - Implementation Notes: Brief summary
```

### Agent Delegation

Delegate sync tasks to specialized agents:

```yaml
manager-docs:
  tasks:
    - README synchronization
    - CODEMAP generation and update
    - SPEC status sync
    - API documentation

manager-quality:
  tasks:
    - Link integrity verification
    - Consistency check
    - TRUST 5 validation
```

---

## Phase 3: Git Operations

### Staging Documentation

Stage only documentation files:

```bash
# Stage documentation
git add README.md docs/ .jikime/specs/*/spec.md
```

### Commit Message Template

```
docs: sync documentation with code changes

Synchronized:
- README.md (updated features section)
- docs/CODEMAPS/INDEX.md (new module added)
- SPEC-API-001 (status: Completed)

Quality verification:
- Tests: PASS
- Linter: PASS

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

### PR Management (Team Mode)

For team workflows:

```bash
# Create branch
git checkout -b docs/sync-update

# Commit changes
git commit -m "[message]"

# Create PR
gh pr create --title "docs: sync documentation" --body "[description]"
```

---

## Quality Standards

### TRUST 5 for Documentation

Apply TRUST 5 framework to documentation:

- **T**ested: All links working, code examples valid
- **R**eadable: Clear structure, proper formatting
- **U**nified: Consistent terminology and style
- **S**ecured: No sensitive data exposed
- **T**rackable: Timestamps, version info, change history

### Documentation Quality Checklist

Before marking sync complete:

- [ ] All internal links verified
- [ ] External links validated
- [ ] Code examples tested
- [ ] Timestamps updated
- [ ] Consistent formatting
- [ ] No sensitive data exposed
- [ ] SPEC status accurate

---

## Execution Modes

### Auto Mode (Default)

Sync changed files only:

- Analyze git diff
- Update only affected documentation
- Quick and focused

### Full Mode

Complete documentation regeneration:

- Rebuild all CODEMAPs
- Refresh all timestamps
- Verify all links
- Use when structure changes significantly

### Status Mode

Read-only health check:

- No changes made
- Report documentation health
- Identify stale documentation
- Quick assessment

---

## Worktree Integration

### Worktree Detection

Detect when running in git worktree:

```bash
git rev-parse --git-dir | grep -q "worktrees"
```

### Worktree-Specific Behavior

When in worktree:

- Auto-detect SPEC ID from directory name
- Update SPEC status automatically
- Offer worktree management options after sync

### Post-Sync Options

```yaml
worktree_options:
  - Return to main directory
  - Continue in worktree
  - Switch to another worktree
  - Remove this worktree
```

---

## Troubleshooting

### Common Issues

Documentation Out of Sync:

- Run `git diff` to identify changes
- Use `--full` mode to regenerate
- Verify git history for missing commits

Quality Verification Failing:

- Review specific failures in output
- Fix issues before syncing
- Use `--skip-quality` only when necessary

Link Integrity Failures:

- Check moved or renamed files
- Update references in affected documents
- Verify external URLs are accessible

### Recovery Procedures

When sync encounters issues:

- Sync creates backups before changes
- Use `git diff` to review changes
- Revert with `git checkout -- docs/`
- Re-run sync after fixing issues

---

## Integration Points

### With DDD Workflow

After DDD refactoring:

- Update CODEMAPs to reflect new structure
- Sync SPEC with implementation progress
- Document architectural changes

### With Testing Workflow

After test completion:

- Update coverage information
- Document test strategies
- Sync quality metrics

### With Quality Framework

Quality verification feeds sync:

- Gate sync on quality checks
- Record quality status in docs
- Track quality trends

---

Version: 1.0.0
Status: Active
Last Updated: 2026-01-22
