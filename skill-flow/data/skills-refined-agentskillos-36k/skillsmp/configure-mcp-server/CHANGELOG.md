# Changelog

All notable changes to the **configure-mcp-server** skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- CHANGELOG.md for tracking version history
- Requirements section in README.md

## [1.2.0] - 2025-01-XX

### Added
- Support for Railway MCP configuration type
- SERVEURS_ORBIT.md example with 14 real-world MCP servers
- Enhanced documentation for Supabase Edge Functions
- TYPES_CONFIGURATION.md reference guide

### Changed
- Marked Supabase Edge Functions as recommended method (⭐)
- Improved validation script documentation

### Fixed
- Clarified placeholder usage in configuration examples

## [1.1.0] - 2025-01-XX

### Added
- validate-mcp-config.sh script for configuration validation
- Support for streamable-http type (n8n)
- Enhanced security warnings for secrets management

### Changed
- Updated examples to use generic placeholders
- Improved documentation structure

## [1.0.0] - 2025-01-XX

### Added
- Initial release of configure-mcp-server skill
- Support for 4 configuration types: URL, streamable-http, command, Railway
- MCP configuration guide for Cursor (~/.cursor/mcp.json)
- SERVEURS_MCP.md template for documenting MCP servers
- Validation script for mcp.json syntax and structure
- Support for Supabase Edge Functions as primary method
- Support for n8n MCP integration
- Support for local npx-based servers (development)

### Documentation
- Complete SKILL.md with configuration types and examples
- README.md with overview and validation instructions
- Template for documenting project-specific MCP servers

---

## Version History

- **1.2.0** - Current version with Railway support and enhanced examples
- **1.1.0** - Added validation script and streamable-http support
- **1.0.0** - Initial release

## How to Version

This skill follows [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible configuration format changes
- **MINOR** version for new configuration types or features
- **PATCH** version for backwards compatible bug fixes

### Examples
- Adding a new MCP server type → MINOR version bump
- Changing mcp.json structure → MAJOR version bump
- Fixing documentation or validation script bugs → PATCH version bump
