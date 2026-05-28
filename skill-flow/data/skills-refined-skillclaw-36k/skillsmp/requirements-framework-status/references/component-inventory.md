# Component Inventory

Detailed inventory of all Requirements Framework components with line counts and purposes.

## Hooks (9 total)

| Hook File | Type | Purpose | Lines |
|-----------|------|---------|-------|
| `check-requirements.py` | PreToolUse | Blocks Edit/Write if requirements unsatisfied | 374 |
| `handle-session-start.py` | SessionStart | Injects context, shows status on session start | 183 |
| `handle-stop.py` | Stop | Verifies requirements before Claude stops | 155 |
| `handle-session-end.py` | SessionEnd | Cleanup stale sessions | 123 |
| `handle-plan-exit.py` | PostToolUse (ExitPlanMode) | Shows status after planning phase | 139 |
| `auto-satisfy-skills.py` | PostToolUse (Skill) | Auto-satisfy requirements when skills complete | 137 |
| `clear-single-use.py` | PostToolUse (Bash) | Clear single_use requirements after action | 136 |
| `ruff_check.py` | PreToolUse | Python linting integration | 182 |

**Total Hook Lines**: ~1,429

---

## Core Libraries (hooks/lib/)

| Module | Purpose | Lines |
|--------|---------|-------|
| `requirements.py` | Core BranchRequirements API | 452 |
| `config.py` | Configuration cascade loader | 865 |
| `state_storage.py` | JSON state persistence in `.git/requirements/` | 272 |
| `session.py` | Session tracking & registry management | 312 |
| `registry_client.py` | Session registry client | 200 |

**Total Core Lines**: ~2,101

---

## Strategy Libraries

| Module | Purpose | Lines |
|--------|---------|-------|
| `strategy_registry.py` | Central dispatch mechanism for requirement types | 148 |
| `base_strategy.py` | Abstract base class for strategies | 92 |
| `blocking_strategy.py` | Blocking requirement implementation | 186 |
| `dynamic_strategy.py` | Dynamic requirement with calculators | 224 |
| `guard_strategy.py` | Guard requirement (condition checks) | 178 |
| `strategy_utils.py` | Shared strategy utilities | 87 |

**Total Strategy Lines**: ~915

---

## Utility Libraries

| Module | Purpose | Lines |
|--------|---------|-------|
| `branch_size_calculator.py` | Dynamic branch size calculation | 352 |
| `calculation_cache.py` | TTL-based results caching (30-sec default) | 154 |
| `calculator_interface.py` | Abstract calculator base class | 73 |
| `message_dedup_cache.py` | Message deduplication (5-min TTL) | 285 |
| `git_utils.py` | Git operations (branch, repo detection) | 160 |
| `config_utils.py` | Configuration utility functions | 98 |
| `colors.py` | Terminal colors (NO_COLOR support) | 157 |
| `logger.py` | Structured JSON logging | 151 |

**Total Utility Lines**: ~1,430

---

## Interactive Libraries

| Module | Purpose | Lines |
|--------|---------|-------|
| `init_presets.py` | Initialization wizard presets | 463 |
| `interactive.py` | Interactive UI components | 219 |
| `feature_selector.py` | Feature selection logic | 148 |

**Total Interactive Lines**: ~830

---

## CLI Tool

| File | Purpose | Lines |
|------|---------|-------|
| `requirements-cli.py` | `req` command implementation | 1,839 |

**Commands** (11 total):
- `req status` - Show requirement status
- `req satisfy` - Mark requirement satisfied
- `req clear` - Clear a requirement
- `req init` - Interactive project setup
- `req config` - View/modify configuration
- `req doctor` - Verify installation & sync
- `req verify` - Quick installation check
- `req sessions` - View active sessions
- `req list` - List all requirements
- `req prune` - Clean stale data
- `req enable` / `req disable` - Toggle requirements
- `req logging` - Configure logging

---

## Test Suite

| File | Purpose | Lines |
|------|---------|-------|
| `test_requirements.py` | Comprehensive test suite | 3,792 |
| `test_branch_size_calculator.py` | Branch size calculator tests | 312 |

**Total Tests**: 544 tests (100% pass rate)

**Test Categories** (16+):
- Session management (77 tests)
- Configuration loading (cascade, inheritance)
- State storage (atomic writes, locking)
- Requirement strategies (Blocking, Dynamic, Guard)
- Hook integration (PreToolUse, PostToolUse, Stop, SessionStart)
- CLI commands (all 11 commands)
- Branch size calculator
- Message deduplication
- Auto-satisfaction
- Single-use requirements
- Error handling & fail-open
- Edge cases & race conditions

---

## Plugin Components

### Agents (17 total)

| Agent | Purpose |
|-------|---------|
| `adr-guardian.md` | ADR compliance validation |
| `backward-compatibility-checker.md` | Breaking change detection |
| `code-reviewer.md` | General code review |
| `code-simplifier.md` | Complexity reduction |
| `codex-review-agent.md` | OpenAI Codex integration |
| `comment-analyzer.md` | Comment quality review |
| `comment-cleaner.md` | Remove stale/unnecessary comments |
| `commit-planner.md` | Plan commits before making them |
| `exception-auditor.md` | Exception handling audit |
| `import-organizer.md` | Organize and clean imports |
| `silent-failure-hunter.md` | Find silent failures |
| `solid-checker.md` | SOLID principles checker |
| `test-analyzer.md` | Test coverage analysis |
| `test-pyramid-checker.md` | Test pyramid compliance |
| `tool-validator.md` | Tool usage validation |
| `type-checker.md` | Type coverage checker |
| `type-design-analyzer.md` | Type system analysis |

### Commands (5 total)

| Command | Purpose |
|---------|---------|
| `codex-review.md` | Codex-powered review |
| `commit-checks.md` | Pre-commit quality checks |
| `plan-review.md` | Review plan before implementation |
| `pre-commit.md` | Quick pre-commit review |
| `quality-check.md` | Comprehensive PR review |

### Skills (4 total)

| Skill | Purpose |
|-------|---------|
| `requirements-framework-usage` | Usage help and configuration |
| `requirements-framework-status` | Status reporting |
| `requirements-framework-development` | Development workflow |
| `requirements-framework-builder` | Extension guidance |

---

## Summary

| Category | Count | Lines |
|----------|-------|-------|
| Hooks | 9 | ~1,429 |
| Core Libraries | 5 | ~2,101 |
| Strategy Libraries | 6 | ~915 |
| Utility Libraries | 8 | ~1,430 |
| Interactive Libraries | 3 | ~830 |
| CLI Tool | 1 | ~1,839 |
| Test Suite | 2 | ~4,104 |
| **Total Production Code** | - | **~8,544** |
| **Total with Tests** | - | **~12,648** |

| Plugin Components | Count |
|-------------------|-------|
| Agents | 17 |
| Commands | 5 |
| Skills | 4 |
