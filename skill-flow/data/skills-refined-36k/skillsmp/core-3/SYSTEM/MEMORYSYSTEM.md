# Memory System

**The unified system memory - what happened, what we learned, what we're working on.**

**Version:** 7.0 (Projects-native architecture, 2026-01-12)
**Location:** `~/.claude/MEMORY/`

---

## Architecture

**Claude Code's `projects/` is the source of truth. Hooks capture domain-specific events directly. Harvesting tools extract learnings from session transcripts.**

```
User Request
    ↓
Claude Code projects/ (native transcript storage - 30-day retention)
    ↓
Hook Events trigger domain-specific captures:
    ├── AutoWorkCreation → WORK/
    ├── ResponseCapture → WORK/
    ├── ImplicitSentimentCapture → SIGNALS/, SENTIMENT/ (ratings ≤4)
    ├── WorkCompletionLearning → WORK/*/SUMMARY.md
    └── SecurityValidator → SECURITY/
    ↓
Observability reads from projects/
```

**Key insight:** Hooks write directly to specialized directories. There is no intermediate "firehose" layer - Claude Code's `projects/` serves that purpose natively.

---

## Directory Structure

```
~/.claude/MEMORY/
├── WORK/                   # PRIMARY work tracking
│   └── {work_id}/
│       ├── META.yaml       # Status, session, lineage
│       ├── IDEAL.md        # Success criteria
│       ├── SUMMARY.md      # Session completion summary (auto-generated)
│       ├── IdealState.jsonl
│       ├── items/          # Individual work items
│       ├── agents/         # Sub-agent work
│       ├── research/       # Research findings
│       ├── scratch/        # Iterative artifacts (diagrams, prototypes, drafts)
│       ├── verification/   # Evidence
│       └── children/       # Nested work
├── LEARNINGS/              # Curated learnings (future: AI-driven capture)
│   └── YYYY-MM/
├── SENTIMENT/              # Low rating captures (≤4) from sentiment detection
│   └── YYYY-MM/
├── SIGNALS/                # User satisfaction ratings
│   └── ratings.jsonl
├── SECURITY/               # Security audit events
│   └── YYYY/MM/
├── STATE/                  # Operational state
│   └── current-work.json   # Active work directory pointer
└── README.md
```

---

## Directory Details

### Claude Code projects/ - Native Session Storage

**Location:** `~/.claude/projects/-Users-<username>--<project>/`
**What populates it:** Claude Code automatically (every conversation)
**Content:** Complete session transcripts in JSONL format
**Format:** `{uuid}.jsonl` - one file per session
**Retention:** 30 days (Claude Code manages cleanup)
**Purpose:** Source of truth for all session data; Observability and harvesting tools read from here

This is the actual "firehose" - every message, tool call, and response. PAI leverages this native storage rather than duplicating it.

### WORK/ - Primary Work Tracking

**What populates it:**
- `AutoWorkCreation.hook.ts` on UserPromptSubmit (creates work dir)
- `ResponseCapture.hook.ts` on Stop (updates work items)
- `WorkCompletionLearning.hook.ts` on SessionEnd (creates SUMMARY.md)
- `SessionSummary.hook.ts` on SessionEnd (marks COMPLETED)

**Content:** Work directories with metadata, items, summary, verification artifacts
**Format:** `WORK/{work_id}/` with META.yaml, items/, verification/, etc.
**Purpose:** Track all discrete work units with lineage, verification, and feedback

**Work Directory Lifecycle:**
1. `UserPromptSubmit` → AutoWorkCreation creates work dir + first item
2. `Stop` → ResponseCapture updates item with response summary
3. `SessionEnd` → SessionSummary marks work COMPLETED, clears state

### LEARNINGS/ - Curated Learnings

**What populates it:** Reserved for future AI-driven capture methodology

**Structure:** `LEARNINGS/YYYY-MM/*.md` - Substantive learning files
**Purpose:** High-value learnings worth preserving long-term (methodology TBD)

### SENTIMENT/ - Low Rating Sentiment Captures

**What populates it:** `ImplicitSentimentCapture.hook.ts` (ratings ≤4 only)

**Structure:** `SENTIMENT/YYYY-MM/*.md` - Sentiment-triggered captures for review
**Purpose:** Captures frustration signals for pattern analysis and improvement

### SIGNALS/ - User Satisfaction Ratings

**What populates it:** `ImplicitSentimentCapture.hook.ts` (every interaction)
**Content:** All ratings (1-10 scale) with timestamps and session IDs
**Format:** `SIGNALS/ratings.jsonl`

### SECURITY/ - Security Events

**What populates it:** `SecurityValidator.hook.ts` on tool validation
**Content:** Security audit events (blocks, confirmations, alerts)
**Format:** `SECURITY/security-events.jsonl`
**Purpose:** Security decision audit trail

### STATE/ - Fast Runtime Data

**What populates it:** Various tools and hooks
**Content:** High-frequency read/write JSON files for runtime state
**Key Property:** Ephemeral - can be rebuilt from RAW or other sources. Optimized for speed, not permanence.

**Files:**
- `current-work.json` - Active work directory pointer (session → work dir mapping)

This is mutable state that changes during execution - not historical records. If deleted, system recovers gracefully.

---

## Hook Integration

| Hook | Trigger | Writes To |
|------|---------|-----------|
| AutoWorkCreation.hook.ts | UserPromptSubmit | WORK/, STATE/current-work.json |
| WorkCompletionLearning.hook.ts | SessionEnd | WORK/*/SUMMARY.md |
| SessionSummary.hook.ts | SessionEnd | WORK/META.yaml (status), clears STATE |
| ImplicitSentimentCapture.hook.ts | UserPromptSubmit | SIGNALS/, SENTIMENT/ (ratings ≤4) |
| SecurityValidator.hook.ts | PreToolUse | SECURITY/ |

---

## Data Flow

```
User Request
    ↓
Claude Code → projects/{uuid}.jsonl (native transcript)
    ↓
AutoWorkCreation → WORK/{id}/ + STATE/current-work.json
    ↓
[Work happens - all tool calls captured in projects/]
    ↓
ImplicitSentimentCapture → SIGNALS/ (all ratings) + LEARNINGS/ (low ratings)
    ↓
WorkCompletionLearning → WORK/{id}/SUMMARY.md (for significant work)
    ↓
SessionSummary → WORK/META.yaml (COMPLETED), clears STATE/current-work.json
```

---

## Quick Reference

### Check current work
```bash
cat ~/.claude/MEMORY/STATE/current-work.json
ls ~/.claude/MEMORY/WORK/ | tail -5
```

### Check ratings
```bash
tail ~/.claude/MEMORY/SIGNALS/ratings.jsonl
```

### Check learnings
```bash
ls ~/.claude/MEMORY/LEARNINGS/
```

---

## Migration History

**2026-01-24:** v8.1 - Work completion summaries
- WorkCompletionLearning now writes SUMMARY.md into work directories (not LEARNINGS/)
- Moved 9 existing work_*.md files from LEARNINGS/ to WORK/*/SUMMARY.md
- Work session metadata now lives with the work, not in a separate directory

**2026-01-24:** v8.0 - Memory system simplification
- Renamed LEARNING/ to LEARNINGS/ (clearer naming)
- Moved SIGNALS/ to top-level (was LEARNING/SIGNALS/)
- Removed SYSTEM/ category (was duplicating git history)
- Removed SYNTHESIS/, SessionHarvester, LearningPatternSynthesis (unused)
- Removed ResponseCapture, ExplicitRatingCapture hooks (simplified to ImplicitSentimentCapture)
- Removed CAPTURES/, README.md (unused)

**2026-01-12:** v7.0 - Projects-native architecture
- Eliminated RAW/ directory entirely - Claude Code's `projects/` is the source of truth
- Removed EventLogger.hook.ts (was duplicating what projects/ already captures)
- Created SessionHarvester.ts to extract learnings from projects/ transcripts
- Created WorkCompletionLearning.hook.ts for session-end learning capture
- Created LearningPatternSynthesis.ts for rating pattern aggregation
- Added LEARNING/SYNTHESIS/ for pattern reports
- Updated Observability to read from projects/ instead of RAW/
- Updated ActivityParser.ts to use projects/ as data source
- Removed archive functionality from pai.ts (Claude Code handles 30-day cleanup)

**2026-01-11:** v6.1 - Removed RECOVERY system
- Deleted RECOVERY/ directory (5GB of redundant snapshots)
- Removed RecoveryJournal.hook.ts, recovery-engine.ts, snapshot-manager.ts
- Git provides all necessary rollback capability

**2026-01-11:** v6.0 - Major consolidation
- WORK is now the PRIMARY work tracking system (not SESSIONS)
- Deleted SESSIONS/ directory entirely
- Merged SIGNALS/ into LEARNING/SIGNALS/
- Merged PROGRESS/ into STATE/progress/
- Merged integrity-checks/ into STATE/integrity/
- Fixed AutoWorkCreation hook (prompt vs user_prompt field)
- Updated all hooks to use correct paths

**2026-01-10:** v5.0 - Documentation consolidation
- Consolidated WORKSYSTEM.md into MEMORYSYSTEM.md

**2026-01-09:** v4.0 - Major restructure
- Moved BACKUPS to `~/.claude/BACKUPS/` (outside MEMORY)
- Renamed RAW-OUTPUTS to RAW
- All directories now ALL CAPS

**2026-01-05:** v1.0 - Unified Memory System migration
- Previous: `~/.claude/history/`, `~/.claude/context/`, `~/.claude/progress/`
- Current: `~/.claude/MEMORY/`
- Files migrated: 8,415+

---

## Related Documentation

- **Hook System:** `THEHOOKSYSTEM.md`
- **Architecture:** `PAISYSTEMARCHITECTURE.md`
