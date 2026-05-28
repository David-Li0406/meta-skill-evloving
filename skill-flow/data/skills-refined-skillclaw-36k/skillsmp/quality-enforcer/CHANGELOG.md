# Changelog - quality-enforcer

All notable changes to the Quality Enforcer skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Incremental coverage reporting (delta from baseline)
- Integration with CI/CD pipelines

## [5.0.0] - 2025-10-23

### Added
- `run_quality_gates.py` - Comprehensive quality gate runner
- `check_coverage.py` - Test coverage validation (≥80% required)
- Quality gate enforcement before PR creation
- Support for pytest, ruff, mypy, uv build
- Container health checks (optional)

### Changed
- Quality gates now enforced consistently across all workflow types
- Coverage threshold standardized at 80%

### Requirements
- Test coverage ≥ 80%
- All tests passing
- Linting clean (ruff)
- Type checking clean (mypy)
- Build successful

---

## Related Documentation

- **[SKILL.md](SKILL.md)** - Complete skill documentation
- **[README.md](README.md)** - Human-readable overview
- **[../../CHANGELOG.md](../../CHANGELOG.md)** - Repository-wide changelog
- **[../../CONTRIBUTING.md](../../CONTRIBUTING.md)** - Contribution guidelines
