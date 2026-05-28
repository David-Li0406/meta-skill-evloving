# Changelog - speckit-author

All notable changes to the SpecKit Author skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Enhanced as-built deviation detection
- Automated metrics collection from test results

## [5.0.0] - 2025-10-23

### Added
- Interactive callable tool for creating specifications
- Automatic BMAD planning context detection
- Adaptive Q&A based on BMAD availability (5-8 vs 10-15 questions)
- TODO file task parsing and frontmatter updates
- As-built feedback loop via `update_asbuilt.py`
- Template-based spec.md and plan.md generation
- Compliant directory structure creation

### Changed
- Converted from inline workflow to standalone Python scripts
- SpecKit now runs in worktrees (not main repo)
- Specifications created after worktree creation
- Integration with BMAD planning for context reuse

### Token Efficiency
- **With BMAD:** 5-8 questions, ~1,500 tokens
- **Without BMAD:** 10-15 questions, ~2,500 tokens
- **Savings (with BMAD):** ~1,700-2,700 tokens per feature

---

## Related Documentation

- **[SKILL.md](SKILL.md)** - Complete skill documentation
- **[README.md](README.md)** - Human-readable overview
- **[../../CHANGELOG.md](../../CHANGELOG.md)** - Repository-wide changelog
- **[../../CONTRIBUTING.md](../../CONTRIBUTING.md)** - Contribution guidelines
