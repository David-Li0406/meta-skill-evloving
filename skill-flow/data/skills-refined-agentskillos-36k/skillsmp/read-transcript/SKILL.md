---
name: read-transcript
description: "Search and retrieve context from previous Angainor iteration transcripts. Use when you need detailed context about what happened in a previous iteration beyond what's in progress.txt. Triggers on: read transcript, previous iteration, what happened in, search transcripts."
---

# Read Transcript

Search and retrieve full context from previous Angainor iteration transcripts.

---

## When to Use

Use this skill when:
- `progress.txt` mentions something but lacks detail
- You need to understand HOW something was implemented, not just WHAT
- You're debugging an issue that may relate to a previous iteration's work
- You want to see the full conversation from a specific iteration

---

## The Job

1. Read the transcript index at `transcripts/index.json`
2. Search for relevant transcripts by story ID, date, branch, or keyword
3. Read the full transcript file(s) for detailed context
4. Extract and present the relevant information

---

## Index Format

The index at `transcripts/index.json` has this structure:

```json
{
  "transcripts": [
    {
      "file": "2026-01-17-14-30-00-iteration-1.txt",
      "timestamp": "2026-01-17-14-30-00",
      "iteration": 1,
      "branch": "angainor/feature-name",
      "storyId": "US-001"
    }
  ]
}
```

---

## Search Methods

### By Story ID
Find all iterations that worked on a specific story:
```
Search transcripts for story US-003
```

### By Date Range
Find iterations from a specific time period:
```
Search transcripts from 2026-01-15 to 2026-01-17
```

### By Branch
Find all iterations for a feature branch:
```
Search transcripts for branch angainor/auth-system
```

### By Iteration Number
Get a specific iteration:
```
Read transcript from iteration 5
```

---

## Step-by-Step Process

1. **Read the index:**
   ```
   Read transcripts/index.json
   ```

2. **Find matching entries:**
   - Filter by the search criteria (storyId, timestamp, branch, iteration)
   - List matching transcripts with their metadata

3. **Read relevant transcripts:**
   ```
   Read transcripts/[filename].txt
   ```

4. **Extract key information:**
   - What was implemented
   - Key decisions made
   - Errors encountered and how they were resolved
   - Files that were modified

---

## Example Usage

**User asks:** "What approach did the previous iteration use for the database migration?"

**Your process:**

1. Read `transcripts/index.json` to find recent iterations
2. Identify iterations that might involve database work (check storyId patterns)
3. Read the relevant transcript file
4. Extract and summarize the migration approach

---

## Output Format

When presenting transcript information:

```markdown
## Transcript: [filename]
**Iteration:** [N] | **Date:** [timestamp] | **Story:** [storyId]

### Summary
[Brief summary of what happened in this iteration]

### Key Details
- [Relevant detail 1]
- [Relevant detail 2]

### Files Modified
- [file1.ts]
- [file2.ts]
```

---

## Tips

- Start with the index to narrow down which transcripts to read
- Transcripts can be long - focus on the sections relevant to the query
- The metadata at the end of each transcript includes iteration number and branch
- Cross-reference with `progress.txt` for additional context
- Multiple iterations may have worked on the same story (if it failed and retried)

---

## Checklist

Before responding:

- [ ] Read `transcripts/index.json` first
- [ ] Identified relevant transcripts based on search criteria
- [ ] Read the full transcript file(s)
- [ ] Extracted and presented the relevant information
- [ ] Provided context about which iteration/story the information came from
