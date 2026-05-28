# Changelog

All notable changes to the **skill-manager** skill will be documented in this file.

## [1.0.0] - 2025-12-23

### Added

- Initial skill-manager implementation
- Pattern observation hooks (PostToolUse, UserPromptSubmit, Notification, Stop)
- Learning engine for detecting workflow patterns
- Skill generation from approved candidates
- Auto-improvement engine with confidence-based application
- Git-based versioning for all generated skills
- CLI commands: list, learn, candidates, approve, reject, history, rollback, stats, improve, refine
- Configuration system with domain markers
- Analytics tracking

### Features

- **Auto-learning**: Detects repeated tool sequences and domain patterns
- **Complete skill packages**: Generates SKILL.md, metadata, references, and changelogs
- **Versioned history**: Each skill is a Git repository with tags
- **Auto-improvement**: Skills evolve based on effectiveness metrics
- **Domain support**: DevOps, security, data science, frontend, backend, git workflows
