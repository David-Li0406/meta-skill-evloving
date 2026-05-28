# Changelog

All notable changes to this project will be documented in this file.

## [1.0.23] - 2026-01-22

### Added
- Multi-client extension support (Claude Code, Cursor, Gemini CLI)
- `plugin.json` for Claude Code plugin system
- `.cursor/mcp.json` for Cursor IDE
- `AGENTS.md` generic agent instruction template
- Agent instruction file documentation in README

### Changed
- Moved Claude Code plugin to `.claude-plugin/plugin.json`
- Updated README with correct installation instructions
- Synced `gemini-extension.json` version

## [1.0.22] - 2026-01-22

### Added
- Symbol coverage metrics in audit output
- Optimized regex patterns for parser

### Fixed
- Handle async keyword in parser
- Improved route detection
- Ignore .trunk directory in indexer

## [1.0.0] - 2026-01-22

### Added
- Initial release of Atlas Guardrails
- `atlas index`: Recursive file indexing and symbol extraction (TS/JS, Python)
- `atlas pack`: Context packing with token budget and dependency graph expansion
- `atlas find-duplicates`: Intent-based duplicate detection
- `atlas check`: Public API drift detection
- `atlas mcp`: MCP server implementation
- `atlas ralphy-init`: Configuration generator for Ralphy
