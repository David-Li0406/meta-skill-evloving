---
name: grounded-query
description: Verifies factual claims against source documents. Use when answering questions about meeting content, decisions, project details, or any assertion that should be grounded in data files.
---

## Purpose

Ensure all factual claims in responses are supported by evidence from source documents. Prevents hallucination and unsupported status claims.

## When to Use

Automatically apply this workflow when:
- Answering questions about what was discussed, decided, or planned
- Making claims about project status, timelines, or deliverables
- Summarizing meeting content or extracting information from transcripts
- Any query where accuracy matters and source files exist

## Workflow

### Step 1: Generate Initial Response
Answer the user's query based on your understanding of the data files.

### Step 2: Extract Verifiable Claims
Identify statements in your response that are factual assertions, such as:
- "The team decided to use X"
- "Feature Y is complete"
- "Person Z mentioned..."
- Dates, names, decisions, status claims

### Step 3: Search for Evidence
For each claim, search the data directory for supporting evidence:
- Use Grep to find relevant mentions
- Use Read to examine context around matches
- Note the file path and relevant line/section

### Step 4: Classify Evidence
For each claim, assign a status:
- `SUPPORTED` - Direct evidence found in source files
- `PARTIAL` - Related mentions but not exact confirmation
- `NOT FOUND` - No evidence located (doesn't mean false, just unverified)

### Step 5: Output Format

Always end your response with an evidence table:

```
### Evidence

| Claim | Status | Source |
|-------|--------|--------|
| [Brief claim] | SUPPORTED/PARTIAL/NOT FOUND | folder/filename |
```

If evidence is NOT FOUND for key claims, add a note:
> **Note:** Some claims could not be verified against available data files. Confidence is lower for unverified items.

## Example

**Query:** "What database did the team choose?"

**Response:**
The team chose Supabase as the primary database, with pgvector for embeddings support.

### Evidence

| Claim | Status | Source |
|-------|--------|--------|
| Supabase as primary database | SUPPORTED | granola/2025-12-22T02_50_00Z.md |
| pgvector for embeddings | SUPPORTED | apple-note-voice-memos/2025-12-21T04_48_00Z.md |

## Important

- Do NOT claim something is "Done" or "In Progress" based only on meeting discussions
- Distinguish between "discussed/triage" and "implemented"
- When in doubt, mark as PARTIAL or NOT FOUND rather than SUPPORTED

---

## After Output

This skill returns results to the calling context. **Do not stop execution.**
Continue with the next step in the workflow or TODO list.
