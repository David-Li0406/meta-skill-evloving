# Changelog

All notable changes to the **build-chatwindow** skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- CHANGELOG.md for tracking version history
- Requirements section in README.md

## [1.1.0] - 2025-01-XX

### Added
- Support for `summary_confirm` widget type
- WORKFLOW_INTEGRATION.md reference guide
- Enhanced validation process documentation

### Changed
- Improved widget examples in WIDGET_EXAMPLES.md
- Updated SKILL.md with clearer type descriptions

### Fixed
- Clarified that `input` type is not currently rendered

## [1.0.0] - 2025-01-XX

### Added
- Initial release of build-chatwindow skill
- Support for 6 widget types: button, form, select, checkbox, radio, summary_confirm
- ChatWidget contract definition (TypeScript + JSON)
- SSE transport documentation
- Widget validation workflow (Playground + ChatWindow)
- WIDGET_EXAMPLES.md with 8 copyable examples
- Integration guides for OpenAI Agent Builder and n8n

### Documentation
- Complete SKILL.md with architecture and usage
- README.md with overview and quick start
- WORKFLOW_INTEGRATION.md for workflow setup

---

## Version History

- **1.1.0** - Current version with summary_confirm support
- **1.0.0** - Initial release

## How to Version

This skill follows [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API/contract changes
- **MINOR** version for new functionality in a backwards compatible manner
- **PATCH** version for backwards compatible bug fixes

### Examples
- Adding a new widget type → MINOR version bump
- Changing ChatWidget interface → MAJOR version bump
- Fixing documentation typos → PATCH version bump
