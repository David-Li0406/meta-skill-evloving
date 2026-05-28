# Session Template

Use this template when adding a new session to the chronological SESSIONS section at the bottom of discussion.md.

## Template

```markdown
## Session X: [Short Title] (YYYY-MM-DD)

### Context
[Why this session happened, what triggered it]

### What Claude Did
- Research: [what research performed]
- Analysis: [what analysis done]
- Writing: [what drafted/revised]
- Tools: [what tools/scripts created]
- Skills used: [which skills invoked]

### User Decisions
- Decision 1: [what was decided and why]
- Decision 2: [what was decided and why]

### Outcomes
- ✅ What worked: [successes]
- ❌ What didn't: [failures]
- Files created/modified: [list]

### Next Steps
[What comes next]
```

## Example

```markdown
## Session 16: Publishing Part 3 to Ghost and Backlink Curation (2025-11-22)

### Context
User requested posting Part 3 as draft to Ghost, with tag validation first, then attempting to curate backlinks. After scheduling post for publication, updated repo version to match what will be published.

### What Claude Did
- Research: None (used existing SOLID research from Session 13)
- Analysis: Tag validation using tag-registry skill (found 8 tags, violations)
- Writing: None (post already drafted)
- Tools: Created create_part3_draft.js for Ghost posting
- Skills used: tag-registry, backlink_curating, using-ghost-admin-api

### User Decisions
- Tags: Approved LegalTech, SoloBuilder, Singapore, SOLID (4 tags)
- SOLID tag: Chose SOLID over OpenData (new tag justified by reusability)
- Backlinks: Declined adding backlinks to draft
- Publication: Scheduled for Nov 22, 8:32 PM SGT

### Outcomes
- ✅ Draft posted successfully to Ghost (Post ID: 692121a5acb37300016227a2)
- ✅ Tags validated and reduced from 8 to 4 (prevented tag sprawl)
- ✅ SOLID added to canonical registry with documentation
- ✅ Repo synced with Ghost edits (title, tags, metadata)
- ❌ Lexical→markdown auto-sync failed (incomplete conversion)
- Files created: create_part3_draft.js, sync_post_from_ghost.js
- Files modified: part-3-smu-and-decision.md (metadata updates)

### Next Steps
- Part 3 publishes tonight
- Series complete (3 parts published)
- Meta exercise on what worked/didn't work
```

## What to Include

**Context:**
- What triggered this session (user request, continuation of previous work, milestone)
- What problem we're solving
- Where this fits in overall project

**What Claude Did:**
- **Research:** Any research performed (git analysis, web search, document analysis)
- **Analysis:** Thinking/analysis done (validation, comparison, evaluation)
- **Writing:** Content created (drafts, revisions, sections)
- **Tools:** Scripts/automation created
- **Skills used:** Which skills were invoked and why

**User Decisions:**
- List each decision
- Include brief rationale where relevant
- Note if user overruled Claude's recommendation

**Outcomes:**
- ✅ **What worked:** Successes, achievements, good results
- ❌ **What didn't:** Failures, problems encountered, lessons learned
- **Files created/modified:** Track all file changes
- **Metrics:** Numbers where relevant (word count, time saved, etc.)

**Next Steps:**
- What happens next
- What's pending
- What needs follow-up

## Tips

**Be specific about attribution:**
- "Claude suggested X" vs. "User decided Y" - make it clear
- If user overruled recommendation, note it explicitly
- Show cause and effect: "Claude did A → User decided B"

**Track outcomes honestly:**
- ✅ Mark what worked
- ❌ Mark what failed (this is valuable learning)
- Unknown outcomes should be marked as pending

**Keep sessions focused:**
- One session = one working period
- If session gets too long, consider splitting
- Major decisions get separate AUDIT TRAIL entries

**Link to other sessions:**
- "See Session 3 for time estimate details"
- "Continuing work from Session 10"
- "Addresses feedback from Session 8"
