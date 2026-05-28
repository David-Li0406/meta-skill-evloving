# Changelog - bmad-planner

All notable changes to the BMAD Planner skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- None currently planned

## [5.1.0] - 2025-10-23

### Added
- Database migration strategy Q&A in architecture persona
- Enhanced epic breakdown with complexity reasoning
- Improved template placeholder matching with regex

### Changed
- Epic generation logic now uses AI-analyzed requirements
- Template processing more robust with multiple placeholder formats

### Fixed
- Template rendering edge cases
- YAML frontmatter parsing in certain scenarios

### Token Efficiency
- No change from 5.0.0 (already optimized)
- Savings: ~2,300 tokens per feature (92% reduction vs manual)

## [5.0.0] - 2025-10-23

### Added
- Interactive callable tool architecture
- Three-persona Q&A system (Analyst, Architect, PM)
- Automatic epic breakdown generation
- Template-based document generation
- Compliant directory structure creation
- Automatic git commit

### Changed
- Converted from inline workflow to standalone Python script
- BMAD now runs in main repo (not worktree)
- Planning documents created before worktree creation

### Token Efficiency
- **Previous (manual):** ~2,500 tokens per feature
- **New (callable tool):** ~200 tokens per feature
- **Savings:** ~2,300 tokens (92% reduction)

---

## Related Documentation

- **[SKILL.md](SKILL.md)** - Complete skill documentation
- **[README.md](README.md)** - Human-readable overview
- **[../../CHANGELOG.md](../../CHANGELOG.md)** - Repository-wide changelog
- **[../../CONTRIBUTING.md](../../CONTRIBUTING.md)** - Contribution guidelines
