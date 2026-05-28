# Querying Reference

Patterns for answering questions about past work.

## Time-Based Queries

Read the relevant day files directly:

- "scribe, what did we do today?" → read `.scribe/YYYY-MM-DD.md` (today)
- "scribe, show me yesterday's work" → read yesterday's file
- "scribe, summarize last week" → read the last 7 day files

For multi-day queries, use Glob + Read:

1. Use `Glob` with pattern `.scribe/*.md` to list log files (sorted by name = sorted by date)
2. Use `Read` on the most recent files

## Topic-Based Queries

Use Grep tool first, then read matching files:

- "scribe, what did we try for the null problem?" → `Grep` with pattern `null` in path `.scribe/`, then Read matches
- "scribe, when did we last touch the ETL?" → `Grep` with pattern `ETL` in path `.scribe/`, then Read matches

## Thread Queries

Find entries that reference a given entry:

- "scribe, what entries build on the feature engineering work?" → find the entry's ID, then `Grep` for that ID in `.scribe/` to find entries that reference it in their **Related** section

## Asset Queries

Use the list command, then Grep logs if needed:

- "scribe, show me archives of the notebook" → `python {SKILL_DIR}/scripts/assets.py list notebook`
- "scribe, what version of clustering.ipynb worked?" → `Grep` for "clustering" and "worked" in `.scribe/`, then Read matches

## Process

1. Determine if time-based or topic-based
2. For time-based: read the relevant day files directly
3. For topic-based: use Grep tool for keywords, then read matching files
4. Synthesize an answer from the entries

## Example Questions

- "scribe, what did we do today?"
- "scribe, what's still unresolved?"
- "scribe, what did we try for the null value problem?"
- "scribe, when did we last touch the ETL pipeline?"
- "scribe, show me last week's work"
- "scribe, what archives do we have of the notebook?"
