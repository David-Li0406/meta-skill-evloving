# Changelog

All notable changes to claude-reflect will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.4.0] - 2026-01-23

### Added
- **Capture Feedback** - Hooks now output confirmation when learnings are captured (#10)
  - Example: `📝 Learning captured: 'no, use gpt-5.1 not gpt-5' (confidence: 85%)`
  - Claude acknowledges captures in real-time
- **Confidence in /view-queue** - Queue display now shows confidence scores, patterns, and relative timestamps
  - Format: `[0.85] "message preview..." (pattern-name) - 2 days ago`
- **Guardrail Pattern Detection** - New pattern type for "don't do X" constraints
  - Detects: "don't add X unless", "only change what I asked", "stop refactoring unrelated", etc.
  - Higher confidence (0.85-0.90) for constraint-based corrections
  - Routes to new `## Guardrails` section in CLAUDE.md
- **Contradiction Detection** - Semantic analysis to find conflicting CLAUDE.md entries
  - New `detect_contradictions()` function in semantic_detector.py
  - Integrated into `/reflect --dedupe` workflow
  - Resolution options: keep first, keep second, merge, or keep both

### Changed
- `/reflect --dedupe` now checks for contradictions before similarity grouping
- Added `## Guardrails` to standard section headers

## [2.1.1] - 2026-01-06

### Fixed
- **Plugin installation error** - Removed duplicate hooks declaration from plugin.json (#9)
  - The `hooks/hooks.json` file is auto-loaded by Claude Code; explicitly declaring it in manifest caused "Duplicate hooks file detected" error

## [2.1.0] - 2026-01-05

### Added
- **Tool Error Extraction** - Scan session files for repeated tool execution errors and convert to CLAUDE.md guidelines (#7)
  - Extracts connection errors, environment issues, module not found errors
  - Filters out Claude Code guardrails and one-off errors
  - Usage: `/reflect --scan-history --include-tool-errors`
- **Mandatory TodoWrite Tracking** - `/reflect` workflow now uses TodoWrite to track all phases

### Changed
- Improved workflow visibility with real-time progress tracking

## [2.0.0] - 2026-01-04

### Added
- **Windows Support** - Native Python scripts replace bash, no WSL required (#1)
- **Semantic AI Detection** - Multi-language support via `claude -p` (#2, #3)
- **UserPromptSubmit Hook** - Automatic capture now properly registered
- **GitHub Actions CI** - Automated testing on Windows, macOS, Linux (Python 3.8 & 3.11)
- **Comparison Tool** - `scripts/compare_detection.py` for testing detection accuracy
- **90 Unit Tests** - Comprehensive test coverage with mocked Claude CLI calls

### Changed
- Hooks now use Python scripts instead of bash for cross-platform compatibility
- `/reflect` command validates queue items with semantic AI before presenting
- Detection uses hybrid approach: regex patterns (fast, real-time) + semantic AI (accurate, during /reflect)
- Updated documentation (README.md, CLAUDE.md) with new architecture

### Deprecated
- Bash scripts moved to `scripts/legacy/` (still available for reference)

### Fixed
- Hooks failing on Windows due to bash dependency (#1)
- False positives from English-only regex patterns (#2)
- Multi-language corrections not being detected (#3)
- UserPromptSubmit hook not registered in hooks.json

## [1.4.1] - 2025-12-xx

### Fixed
- Critical jq filter bug in distribution files
- Historical scan now ensures matches are always presented to user
- Queue items being ignored during history scan

## [1.4.0] - 2025-12-xx

### Added
- Confidence scoring for learnings (0.60-0.90)
- Positive feedback pattern detection
- AGENTS.md sync support
- Semantic deduplication (`/reflect --dedupe`)

## [1.3.5] - 2025-12-xx

### Changed
- PreCompact hook now informs and backs up instead of blocking

## [1.3.4] - 2025-12-xx

### Fixed
- Restored UserPromptSubmit hook for automatic capture
