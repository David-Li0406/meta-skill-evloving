# Changelog

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-01-20

### Added

- **Dual-mode execution**:
  - `/smart-dev:dev` - Single-shot mode with readiness gating
  - `/smart-dev:loop` - Iterative mode with automatic retry until completion
  - `/smart-dev:cancel` - Graceful loop cancellation
- **95% Readiness Gate (Phase 3c)**:
  - Track A: Deterministic structural scoring (0-100 points)
    - 5 categories: structure, testability, interfaces, constraints, verification
    - Penalties for placeholders, TODOs, missing sections
    - Script: `score-spec.ts`
  - Track B: LLM-based semantic sufficiency check
    - 5 criteria rubric with evidence requirements
    - Goal clarity, success criteria, edge cases, assumptions
    - Script: `check-semantic.ts`
- **Question budget system**:
  - Max 2 Q&A rounds to prevent infinite ask-user loops
  - Assumptions pack fallback when budget exhausted
  - User accept/reject choice for documented assumptions
- **Loop control system**:
  - Stop hook (`loop-stop.sh`) blocks exit until completion
  - Iteration budget (default: 20, configurable)
  - Completion promise detection
  - Timeout reporting at max iterations
- **Spec lock enforcement**:
  - `spec.lock` file created after readiness gate passes
  - PreToolUse hook (`guard-writes.sh`) blocks edits to frozen specs
  - Prevents mid-implementation spec changes
- **Extended progress tracking**:
  - 14 new frontmatter fields in `progress.md`:
    - `mode`, `iteration`, `max_iterations`, `completion_promise`
    - `confidence_threshold`, `readiness_score`, `semantic_ok`, `semantic_skipped`
    - `spec_locked`, `question_round`, `question_budget`
    - `last_verification_status`, `last_error`, `assumptions_accepted`
- **New spec files**:
  - `qa.md` - Q&A log for question rounds
  - `score.json` - Track A scoring results
  - `semantic-check.json` - Track B check results
  - `verification.log` - Test/build output history
  - `assumptions.md` - Assumptions pack (conditional)
- **JSON configuration**:
  - `config/statemachine.json` - State machine formal definition
  - `config/scoring-rules.json` - Track A/B scoring rules
  - `config/phase-definitions.json` - Phase requirements and gates
  - `config/README.md` - Config usage guide
- **Example files**:
  - `examples/sample-score.json`
  - `examples/sample-semantic-check.json`
  - `examples/sample-assumptions.md`
  - Updated `examples/sample-progress.md` with new fields
- **Reference documentation**:
  - `references/readiness-gate.md` - Comprehensive readiness gate guide

### Changed

- Phase 3 split into 3 sub-phases: 3a (Documentation), 3b (Tasks), 3c (Readiness Gate)
- `init.sh` now creates 11 files (was 5)
- `update-progress.sh` supports `--set-field key=value` parameter
- Hooks configuration extended with Stop and PreToolUse hooks
- SKILL.md updated with Phase 3c workflow

### Fixed

- Prevented incomplete spec implementation via readiness gate
- Prevented infinite ask-user loops via question budget
- Prevented premature loop exit via Stop hook
- Prevented mid-implementation spec changes via write guard

## [1.0.0] - 2025-01-13

### Added

- Initial release of Feature Development Workflow skill
- 5-phase workflow: Discovery → Exploration → Documentation → Implementation → Review
- Multi-model agent support:
  - `product-thinker` (Opus) - Deep product decisions
  - `codebase-explorer` (Haiku) - Fast codebase exploration
  - `architect` (Sonnet) - Architecture design
  - `reviewer` (Sonnet) - Code quality review
- Progress persistence with `progress.md` (YAML frontmatter + markdown)
- Session recovery via `check-progress.sh` hook
- Automatic CHANGELOG.md updates on feature completion
- Spec file templates in `.works/spec/{feature}/`
- Scripts:
  - `init.sh` - Initialize feature workspace
  - `check-progress.sh` - Check for incomplete features
  - `update-progress.sh` - Update progress state
  - `update-changelog.sh` - Update CHANGELOG.md
- Reference documentation:
  - `workflow-phases.md` - Detailed phase instructions
  - `file-structure.md` - Spec file templates
  - `code-organization.md` - Code layer conventions
