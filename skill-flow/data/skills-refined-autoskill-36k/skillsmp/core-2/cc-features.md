# Claude Code 2.1.6 Features Used

This document tracks which Claude Code features this PAI uses, for compatibility tracking.

## Current Version

- **CC Version:** 2.1.6 (Latest stable, released 2026-01-13)
- **Last Audit:** 2026-01-14
- **Recent Enhancements:** CC 2.1.6 context percentage fields, intelligent assistance features (checkpoint hints, context monitoring, error learning, skill suggestions)

## Feature Usage Matrix

| Feature | Min Version | Status | Usage Location |
|---------|-------------|--------|----------------|
| Subagents | 1.0.80 | **Adopted** | `.claude/agents/` (17 agents) |
| Checkpoints | 2.0.0 | **Adopted** | `checkpoint-protocol.md` |
| Hooks (settings.json) | 2.1.0 | **Adopted** | `.claude/settings.json` (8 events) |
| Skills System | 2.0.40 | **Adopted** | `.claude/skills/` (16 skills) |
| Plan Mode | 2.0.50 | **Available** | Used on-demand |
| Model Routing | 2.1.0 | **Adopted** | `frontend-design`, `research` skills |
| Status Line | 2.1.0 | **Adopted** | Custom status via hooks |
| WebSearch | 2.1.0 | **Adopted** | `research` skill |
| AskUserQuestion | 2.1.0 | **Adopted** | `delegation-guide.md` |
| Background Tasks | 2.1.0 | **Adopted** | `delegation-guide.md` |
| Task Resume | 2.1.0 | **Adopted** | `delegation-guide.md` |
| PreCompact Hook | 2.1.x | **Adopted** | `settings.json` |
| Skill Invocation | 2.1.0 | **Adopted** | All skills via `context:` field |
| Context Percentage Fields | 2.1.6 | **Adopted** | `statusline-command.sh` |
| Nested Skills Discovery | 2.1.6 | **Supported** | Flat structure compatible |

## Hooks Configuration

All 8 CC hook events are configured:

| Hook Event | Scripts | Enhanced Features |
|------------|---------|-------------------|
| PreToolUse | `pre-tool-use-security.ts`, `capture-all-events.ts` | Checkpoint hints (2026-01-14) |
| PostToolUse | `post-tool-use-audit.ts`, `capture-all-events.ts` | Error pattern learning (2026-01-14) |
| SessionStart | `session-start.ts`, `capture-all-events.ts` | Skill suggestions (2026-01-14) |
| SessionEnd | `capture-all-events.ts` | - |
| UserPromptSubmit | `update-tab-titles.ts`, `capture-all-events.ts` | - |
| Stop | `stop-hook.ts`, `capture-all-events.ts` | - |
| SubagentStop | `subagent-stop-hook.ts`, `capture-all-events.ts` | - |
| PreCompact | `capture-all-events.ts` | - |

## Skills with Model Routing

| Skill | Model | Reason |
|-------|-------|--------|
| frontend-design | sonnet | Design requires creativity |
| research | sonnet | Complex reasoning needed |

## 12-Factor Compliance

| Factor | Status | Score |
|--------|--------|-------|
| 1. Natural Language to Tools | Full | 2/2 |
| 2. Own Your Prompts | Full | 2/2 |
| 3. Own Your Context Window | Full | 2/2 |
| 4. Tools Are Structured Outputs | Full | 2/2 |
| 5. Unify Execution State | Full | 2/2 |
| 6. Launch/Pause/Resume | Full | 2/2 |
| 7. Contact Humans with Tools | Full | 2/2 |
| 8. Own Your Control Flow | Full | 2/2 |
| 9. Compact Errors | Full | 2/2 |
| 10. Small Focused Agents | Full | 2/2 |
| 11. Trigger from Anywhere | Full | 2/2 |
| 12. Stateless Reducer | Full | 2/2 |

**Total Score: 100%** (24/24)

## CC 2.1.x New Features Adopted

### CC 2.1.0-2.1.5
1. **Image metadata** - Supported via hooks
2. **File hyperlinks** - Supported in output
3. **PreCompact hook** - Configured for event capture
4. **Error compaction** - Implemented in `stop-hook.ts`

### CC 2.1.6 (Released 2026-01-13)
5. **Context percentage fields** - `used_percentage` and `remaining_percentage` fields
   - Status: **Adopted** in `statusline-command.sh`
   - Implementation: Native CC 2.1.6 fields with fallback to manual calculation
   - Provides more accurate context tracking
6. **Nested skills discovery** - Support for nested `.claude/skills` directory structures
   - Status: **Supported** (current flat structure is compatible)
   - No changes required
7. **Search in /config command** - CLI feature only
   - Status: **N/A** (not applicable to PAI architecture)
8. **Date filtering in /stats** - CLI feature only
   - Status: **N/A** (not applicable to PAI architecture)
9. **Permission bypass security fix** - Improved hook permission handling
   - Status: **Protected** via `pre-tool-use-security.ts`

## Intelligent Assistance Features (2026-01-14)

Qara's proactive assistance systems for safer operations, better visibility, and faster error resolution:

### Safety & Reliability Features
1. **Checkpoint Hints** - Proactive safety reminders before destructive operations
   - PreToolUse hook monitors 13 high-risk patterns (rm -rf, git reset --hard, DROP TABLE, kubectl delete, etc.)
   - Suggests checkpoint creation if >5 minutes since last checkpoint
   - State tracking: `.claude/state/last-checkpoint.json`
   - Target: 95% checkpoint coverage on risky operations

2. **Context Window Intelligence** - Real-time visibility into effective context usage
   - Status line displays usage against effective budget (60% of stated 1M capacity)
   - **Enhanced with CC 2.1.6:** Native `used_percentage` field with fallback to manual calculation
   - Color-coded indicators: ✅ Green (0-60%), ⚠️ Yellow (60-80%), 🚨 Red (80%+)
   - Prevents context degradation through early warning
   - Target: 75% reduction in context-related issues

### Learning & Discovery Features
3. **Error Pattern Learning** - Institutional knowledge accumulation for faster problem resolution
   - Automatically logs errors to JSONL database with normalized codes
   - Suggests known solutions when similar errors recur
   - Seed patterns: ENOENT, TS2339, MODULE_NOT_FOUND, HTTP errors, git conflicts
   - State: `.claude/state/error-patterns.jsonl`, Library: `.claude/hooks/lib/error-patterns.ts`
   - Target: 30% reduction in error resolution time

4. **Skill Suggestion Engine** - Context-aware feature discovery
   - Analyzes current project context (package.json, session notes, directory structure)
   - Proactively suggests relevant skills at session start
   - 8 skill mappings covering web scraping, research, UI design, CLI tools, PAI optimization
   - Non-intrusive console display
   - Target: Shift from reactive to proactive skill usage

### Workflow Optimization Features
5. **Structured Exploration Pattern** - Systematic codebase understanding
   - Workflow routing: "explore codebase" → 3-agent parallel exploration
   - Documented pattern: codebase-locator + pattern-finder + analyzer + spotcheck synthesis
   - Located: `.claude/skills/CORE/workflows/exploration-pattern.md`

6. **Plan Mode Integration** - Formalized complex task handling
   - Workflow routing: "plan this out" → /plan mode with create_plan → implement_plan → validate_plan
   - Structured approach for multi-file changes and architectural decisions

## Upgrade Path

When new CC versions release:

1. Check CHANGELOG at `https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md`
2. Run `/cc-pai-optimiser` to audit against new features
3. Update this document with adoption status

## Success Metrics

Track for 2 weeks after 2026-01-14 implementation:

- **Checkpoint Usage**: 60% → 95% (before risky operations)
- **Context Issues**: 2/week → 0.5/week (75% reduction)
- **Error Iterations**: 5-7 → 3-4 (30% reduction)
- **Skill Discovery**: Reactive → Proactive

## Version Compatibility Matrix

| CC Version | Qara Compatibility | Notes |
|------------|-------------------|-------|
| 2.1.6 (current) | **Full** | All features supported |
| 2.1.5 | Full | Compatible |
| 2.1.4 | Full | DISABLE_BACKGROUND_TASKS respected |
| 2.1.3 | Full | Extended hook timeouts utilized |
| 2.1.0-2.1.2 | Full | All major features adopted |
| 2.0.40-2.0.99 | Partial | Missing some 2.1.x hooks |
| 2.0.0-2.0.39 | Partial | Basic features only |

---

**Last Updated:** 2026-01-14
