# Changelog

All notable changes to the mojo-best-practices skill are documented here.

## [4.0.0] - 2026-01-24

### Added
- **Dual version support**: Now supports both stable (v25.7) and nightly (v0.26.1) Mojo
- **Version subdirectories**: `rules/stable/` and `rules/nightly/` for version-specific rules
- **CHANGELOG.md**: New changelog file for tracking skill changes
- Sandbox test environments for both stable and nightly

### Changed
- **Clarified version differences**: v25.7 stable and v0.26.x nightly share most syntax
  - Main difference: `alias` (stable) vs `comptime` (nightly) for constants
  - Both use: `@fieldwise_init`, `var`/`deinit`, `Writable` trait
- Updated `references/breaking-changes.md` with accurate version compatibility
- Updated `SKILL.md` with version detection instructions
- Updated `metadata.json` with `supported_versions` structure
- Moved `meta-comptime-values.md` to `rules/nightly/`
- Added `rules/stable/meta-alias-constants.md` for alias syntax
- Bumped skill version from 3.0.0 to 4.0.0

## [3.0.0] - 2026-01-24

### Added
- 107 rules across 12 categories
- GPU programming rules for SM90/SM100 tensor cores
- Updated for Mojo v0.26.1 nightly
- Comprehensive breaking-changes.md reference

### Changed
- Updated all rules for v0.26.1 syntax (`@fieldwise_init`, `comptime`, `var`)
- Added `Writable` trait patterns

## [2.0.0] - 2025-12-15

### Added
- 63 rules across 10 categories
- Initial GPU programming rules
- BLAS/Accelerate integration patterns

## [1.0.0] - 2025-11-01

### Added
- Initial release with 40 rules
- Core memory safety patterns
- Basic type system rules
