# Changelog - tech-stack-adapter

All notable changes to the Tech Stack Adapter skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Auto-detection of additional frameworks (Django, FastAPI)
- Enhanced database stack detection

## [5.0.0] - 2025-10-23

### Added
- `detect_stack.py` - Automatic technology stack detection
- Python version detection (3.11+ required)
- Package manager detection (uv preferred, pip fallback)
- Container runtime detection (Podman)
- Testing framework detection (pytest)
- Database detection (SQLite, PostgreSQL)

### Changed
- Stack detection now automated at workflow start
- Configuration persisted for session

---

## Related Documentation

- **[SKILL.md](SKILL.md)** - Complete skill documentation
- **[README.md](README.md)** - Human-readable overview
- **[../../CHANGELOG.md](../../CHANGELOG.md)** - Repository-wide changelog
- **[../../CONTRIBUTING.md](../../CONTRIBUTING.md)** - Contribution guidelines
