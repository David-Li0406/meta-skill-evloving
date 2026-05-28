# Changelog

All notable changes to the **git-commit-pr** skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Complete gh CLI authentication guide with device flow (6-character code)
- Troubleshooting section for authentication issues (401, 503 errors)
- Explicit --repo option documentation for proxy Git environments

### Planned
- Script automatique pour valider les messages de commit
- Support pour d'autres plateformes Git (GitLab, Bitbucket)
- Templates de PR personnalisables par projet

## [1.0.0] - 2026-01-23

### Added
- Initial release of git-commit-pr skill
- Complete Git workflow guide (verify, stage, commit, push, PR)
- Conventional Commits format support
- Pre-commit verification workflow
- Safe file staging guidelines (avoid committing secrets)
- Commit message templates with all types (feat, fix, docs, etc.)
- Push retry mechanism with exponential backoff (4 attempts)
- Pull Request template with comprehensive sections
- Breaking change documentation format
- Session URL integration for Claude Code commits
- Git hook handling guidelines
- Examples for commits, PRs, and workflows

### Documentation
- Complete SKILL.md with 5-step workflow
- README.md with usage examples
- references/PR_TEMPLATE.md for Pull Request template
- references/COMMIT_EXAMPLES.md with 15+ commit examples
- references/GIT_WORKFLOW.md with detailed workflow

### Best Practices
- Conventional Commits enforcement
- Atomic commits guidance
- Security checks (no .env, credentials)
- Comprehensive PR documentation
- Testing checklist before PR creation

---

## Version History

- **1.0.0** - Initial release with complete Git workflow

## How to Version

This skill follows [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible workflow changes
- **MINOR** version for new features (new commit types, PR templates)
- **PATCH** version for bug fixes and documentation improvements

### Examples
- Adding support for GitLab PRs → MINOR version bump
- Changing Conventional Commits format → MAJOR version bump
- Fixing typos in documentation → PATCH version bump
- Adding new commit examples → PATCH version bump
