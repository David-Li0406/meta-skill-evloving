# Degradation Fixes by Symptom

Quick fixes for specific degradation patterns.

## Symptom: Not Delegating

**Signs**: Writing implementation code, building components directly, editing files without spawning agents.

**Fix**:
1. Stop current work
2. Identify task type (frontend/backend/research/test)
3. Spawn appropriate agent with clear task description
4. Wait for agent to return results

## Symptom: Forgetting Tools

**Signs**: Making assumptions about database, not verifying UI changes, guessing at file contents.

**Fix**:
1. Supabase CLI for ANY database question: `docker exec -i supabase_db_EnhancedHR psql -U postgres -c "..."`
2. Playwright MCP for ANY UI verification
3. Grep/Glob/Read for file exploration

## Symptom: Missing Safety Rules

**Signs**: Considering `supabase db reset`, thinking about dropping tables, not injecting safety rules into agents.

**Fix**:
1. Re-read safety rules in CLAUDE.md section 2
2. Find alternative approach (targeted SQL, admin client, incremental migration)
3. Ask user if unsure

## Symptom: Skipping Doc Review

**Signs**: Planning without `/doc-discovery`, implementing without checking invariants, not updating docs after.

**Fix**:
1. Run `/doc-discovery` before any plan
2. Extract invariants from loaded docs
3. Run `/doc-update` after changes

## Proactive Schedule

| Time | Action |
|------|--------|
| 0-30 min | Normal operation |
| 30-45 min | Consider /remember |
| 45-60 min | /remember recommended |
| 60+ min | /remember + /checkpoint |
| 90+ min | /context-status, consider /compact |
