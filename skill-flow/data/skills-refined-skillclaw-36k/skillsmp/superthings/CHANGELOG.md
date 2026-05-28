# Changelog

All notable changes to SuperThings will be documented in this file.

## [2.0.0] - 2025-12-31

### Major Features

**Learning System**
- Learns from your corrections to improve title and project suggestions over time
- Stores patterns in `data/patterns.json` with confidence scoring
- Logs all corrections to `data/history.jsonl` for pattern extraction
- Shows `[learned: Nx]` indicator when suggestions come from learned patterns
- Confidence thresholds: <3 = ask, >=3 = auto-apply, >=10 = high confidence

**GTD Research Workflow**
- New `/gtd` command for batch research on Computer and Deep Work tasks
- Research results cached to `data/research-cache.json` (persists 7 days)
- URL task handling: visits links first, summarizes actual content
- Rich TLDR bullet summaries with as many points as needed

**Triage Commands**
- `C` - Complete task in Things
- `C [note]` - Complete with note
- `D [person]` - Delegate via Zapier MCP email
- `D [person] [modifier]` - Delegate with context (e.g., "D Brianna within the next week")
- `DD` - Deep Dive for more research
- `DD [focus]` - Deep Dive with specific focus

**Inbox Triage Improvements**
- Grouped card format showing before/after titles
- URL resolution using Firecrawl/WebFetch
- Automatic project assignment with learned patterns
- Build/Make software tasks default to Deep Work
- Fix/maintenance tasks auto-reformat as "Delegate to Brianna: [task]"

### Technical Changes

- Renamed from `things-mcp-silent` to `SuperThings`
- Consolidated MCP server, commands, and skills into single plugin
- Commands moved into plugin (`commands/`) with symlinks to `~/claudesync/commands/`
- Added `data/` directory for patterns, history, and research cache
- Added `SKILL.md` for Claude Code skill documentation
- Updated package name to `superthings` version 2.0.0

### From Original Fork (v1.x)

**Silent Operations** (from things-mcp-silent)
- AppleScript-based write operations prevent Things from stealing focus
- Background task creation and updates
- Silent project and todo management

---

## [1.0.0] - Original Fork

Initial fork from [hildersantos/things-mcp](https://github.com/hildersantos/things-mcp) with AppleScript modifications for silent background operations.

### Added
- `src/scripts/create-todo.applescript` - Creates todos silently
- `src/scripts/update-todo.applescript` - Updates todos silently
- `src/scripts/create-project.applescript` - Creates projects silently
- `src/scripts/update-project.applescript` - Updates projects silently

### Changed
- `src/lib/json-builder.ts` - Uses AppleScript instead of URL schemes

### Known Limitations
- Headings cannot be added to existing projects via AppleScript (only during initial creation)
- Some edge cases in scheduling may behave slightly differently
