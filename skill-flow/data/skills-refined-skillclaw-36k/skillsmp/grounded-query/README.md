# grounded-query Skill

Verifies factual claims against source documents to prevent hallucination.

## Overview

This skill ensures all factual claims in responses are supported by evidence from source documents. It prevents unsupported status claims and distinguishes between what was discussed versus what is actually true.

## Evidence Statuses

| Status | Meaning |
|--------|---------|
| SUPPORTED | Direct evidence found in source files |
| PARTIAL | Related mentions but not exact confirmation |
| NOT FOUND | No evidence located (doesn't mean false, just unverified) |

## When It Applies

The skill automatically applies when:
- Answering questions about what was discussed, decided, or planned
- Making claims about project status, timelines, or deliverables
- Summarizing meeting content or extracting information from transcripts
- Any query where accuracy matters and source files exist

## Testing the Skill

### Prerequisites

1. A context database with `data/` folder containing:
   - Transcripts (`data/transcripts/`)
   - Messages (`data/messages/`) - optional

### Running Evaluations

1. Navigate to your context database:
   ```bash
   cd ~/my-context   # or ~/other-context
   ```

2. Start Claude Code with the plugin:
   ```bash
   claude --plugin-dir ~/your-plugin
   ```

3. Ask questions that require factual verification:
   - "What database did the team choose?"
   - "Who suggested using Supabase?"
   - "When was the MVP deadline set?"

### Example Test Queries

| Test Case | Query | Expected Evidence Status |
|-----------|-------|-------------------------|
| Supported claim | Ask about documented decision | SUPPORTED with file reference |
| Partial evidence | Ask about vaguely mentioned topic | PARTIAL |
| Not found | Ask about never-discussed topic | NOT FOUND |

### Expected Output Format

Response should end with an evidence table:

```
### Evidence

| Claim | Status | Source |
|-------|--------|--------|
| Supabase as database | SUPPORTED | data/transcripts/granola/2025-12-22.md |
| PostgreSQL for queries | PARTIAL | data/transcripts/granola/2025-12-22.md |
| Launch date is March | NOT FOUND | - |
```

### Verification Checklist

- [ ] Every factual claim has evidence status
- [ ] SUPPORTED claims include file path
- [ ] Response distinguishes "discussed" from "implemented"
- [ ] Unverified claims noted with warning

## Critical Rules

1. **Never claim "Complete" or "Done"** based only on meeting discussions
2. **Distinguish between "discussed" and "implemented"**
3. **When in doubt**, mark as PARTIAL or NOT FOUND rather than SUPPORTED
4. **Always include the evidence table** at the end of responses with factual claims

## Evaluation Logs

Test results are stored in the context database (not the plugin):

```
~/my-context/evaluations/grounded-query/
~/other-context/evaluations/grounded-query/
```

Each evaluation run produces a timestamped JSON log with pass/fail results for each test case.

## Test Cases

See `evaluations/evaluation.json` for the full test suite covering:
- Evidence status scenarios (SUPPORTED, PARTIAL, NOT FOUND)
- Multiple claims verification
- Date and person attribution
- Status inflation prevention
- Output format validation
