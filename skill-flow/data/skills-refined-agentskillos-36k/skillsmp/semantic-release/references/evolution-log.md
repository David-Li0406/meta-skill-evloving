**Skill**: [semantic-release](../SKILL.md)

# Evolution Log

Reverse chronological record of significant changes to the semantic-release skill.

---

## 2026-01-16: Polyglot Monorepo Best Practices Alignment

**Context**: Multi-perspective analysis revealed gaps in monorepo support and cross-skill linking

**Changes**:

- Expanded monorepo-support.md from 38 to 230+ lines with Pants + mise integration
- Added Tool Selection by Scale table (< 10 packages → Pants + mise → Bazel)
- Added Affected-Only Release Pattern with mise.toml task examples
- Added Alternative Tools Comparison (Pants, Nx Release, Turborepo, Bazel, Changesets, Lerna-lite)
- Added Cross-Language Version Synchronization section
- Added cross-skill references to mise-tasks skill (polyglot-affected.md, bootstrap-monorepo.md)
- Updated plugin versions: @semantic-release/exec ^7.0.0, @semantic-release/github ^12.0.0
- Updated GitHub Actions: setup-node v4→v6, setup-python v5→v6
- Added caching to setup-node v6 examples (`cache: 'npm'`)

**Files affected**:

- `references/monorepo-support.md` - Major expansion
- `SKILL.md` - Added Cross-skill references section
- `assets/templates/shareable-config/package.json` - Version updates
- `assets/templates/github-workflow.yml` - setup-node v6 with cache
- `references/troubleshooting.md` - setup-node v6 example
- `references/python.md` - setup-node v6, setup-python v6

---

## 2026-01-10: Major Refactoring for Elegance

**Context**: Skill exceeded token efficiency targets (832 lines vs 300-350 target)

**Changes**:

- Extracted MAJOR confirmation workflow to dedicated reference (~200 lines)
- Consolidated reference files: 15 → 10 files
- Unified 3 Bash init scripts into single Bun-first Node.js script (`init-project.mjs`)
- Added project type detection for Node/Python/Rust/Rust+Python
- Added Rust+Python hybrid patterns from rangebar-py (Cargo build profiles for PyO3)
- Added Post-Change Checklist for self-maintenance
- Created this evolution-log.md per skill-architecture standards
- Slimmed verbose sections (mise detection, GitHub Actions policy, Documentation Linking)

**Files affected**:

- `SKILL.md` - Reduced from 832 to 352 lines, 4500 to 1728 words
- `references/major-confirmation.md` - NEW (extracted from SKILL.md)
- `references/evolution-log.md` - NEW (skill-architecture requirement)
- `references/python.md` - Renamed from `python-projects-nodejs-semantic-release.md`, added Rust+Python hybrid patterns
- `references/rust.md` - Renamed from `rust-release-plz.md`
- `references/troubleshooting.md` - Consolidated from authentication.md, local-release-workflow.md, 2025-updates.md
- `references/authentication.md` - Removed troubleshooting (moved to troubleshooting.md)
- `references/local-release-workflow.md` - Removed troubleshooting (moved to troubleshooting.md)
- `scripts/init-project.mjs` - NEW unified Bun-first script
- DELETED: `pypi-publishing-with-doppler.md`, `workflow-patterns.md`, `2025-updates.md`, `resources.md`

---

## 2025-12-19: HTTPS-First Authentication

**Context**: Multi-account GitHub setups needed better support

**Changes**:

- Added mise [env] GH_TOKEN pattern for directory-based account selection
- Updated authentication.md with HTTPS-first approach
- Deprecated SSH as legacy fallback

---

## 2025-12-07: Local-First Philosophy

**Context**: GitHub Actions releases too slow (2-5 minute wait)

**Changes**:

- Established local release as primary method
- Added successCmd auto-push pattern
- Added postrelease script for tracking ref sync

---

## Template

```markdown
## YYYY-MM-DD: Brief Title

**Context**: Why this change was needed

**Changes**:

- Bullet points of what changed

**Files affected**:

- List of modified files
```
