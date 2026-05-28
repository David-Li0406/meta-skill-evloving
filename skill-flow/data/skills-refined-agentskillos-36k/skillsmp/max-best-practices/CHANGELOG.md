# Changelog

All notable changes to the max-best-practices skill are documented here.

## [2.0.0] - 2026-01-24

### Added
- **Dual version support**: Now supports both stable (v25.7) and nightly (v26.1) MAX
- **Version subdirectories**: `rules/stable/` and `rules/nightly/` for version-specific rules
- **Stable-specific rules**:
  - `stable/multigpu-batch-semantics.md` - Aggregate batch size semantics
  - `stable/driver-tensor-api.md` - Using `max.driver.Tensor`
- **Nightly-specific rules**:
  - `nightly/multigpu-batch-semantics.md` - Per-replica batch size semantics (moved)
  - `nightly/driver-buffer-api.md` - Using `max.driver.Buffer` (renamed from Tensor)

### Changed
- Updated `SKILL.md` with version detection instructions
- Updated `metadata.json` with `supported_versions` structure
- Updated `references/breaking-changes.md` with v26.1 changes
- Bumped skill version from 1.0.0 to 2.0.0

## [1.0.0] - 2026-01-24

### Added
- Initial release with 28 rules across 7 categories
- MAX Serve configuration rules
- Multi-GPU and tensor parallelism patterns
- MAX Engine and Graph API rules
- Performance optimization patterns
- Deployment and containerization guides
- Comprehensive breaking-changes.md reference
- CLI flags reference
