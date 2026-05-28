---
name: Research
description: Multi-source parallel research using Perplexity, Gemini, and Claude. Three modes - Quick (1 query), Standard (3 queries), Extensive (8 queries). USE WHEN user says 'research', 'investigate', 'find out about', 'do research on', or requests comprehensive information gathering.
---

# Research Skill

## CRITICAL: Use the Research CLI for Multi-Source Research

**For ANY research request, use the `research` CLI via Bash:**

```bash
# All sources in parallel (RECOMMENDED - fastest)
~/.claude/bin/research --all "your research query"

# Individual sources
~/.claude/bin/research --perplexity "query"    # Fast web search
~/.claude/bin/research --gemini "query"        # Multi-perspective
~/.claude/bin/research --claude "query"        # Detailed analysis (slower)
```

**DO NOT use WebSearch directly for research requests - use the CLI above.**

---

## Three Research Modes

### QUICK RESEARCH MODE
- **Trigger:** User says "quick research" or simple queries
- **Method:** Single `research --all "query"` call
- **Time:** ~15-30 seconds
- **Result:** 3 source results (Perplexity, Claude, Gemini)

### STANDARD RESEARCH MODE (Default)
- **Trigger:** Default for most research requests
- **Method:** 3 parallel Bash calls with different query angles
- **Time:** ~30-45 seconds
- **Result:** 9 source results (3 angles × 3 sources)

### EXTENSIVE RESEARCH MODE
- **Trigger:** User says "extensive research" or "deep dive"
- **Method:** 8 parallel Bash calls covering diverse angles
- **Time:** ~45-90 seconds
- **Result:** 24 source results (8 angles × 3 sources)

---

## Standard Research Workflow

### Step 1: Decompose the Question

Break the user's question into 3 focused sub-questions:
- Core facts and recent developments
- Context, implications, and analysis
- Contrarian views, controversies, or edge cases

### Step 2: Launch Parallel Research (ONE MESSAGE)

**CRITICAL: Use a SINGLE message with multiple Bash tool calls for parallel execution**

```bash
# Launch all 3 in parallel (single message with 3 Bash calls)
~/.claude/bin/research --all "sub-question 1 focusing on core facts"
~/.claude/bin/research --all "sub-question 2 focusing on implications"
~/.claude/bin/research --all "sub-question 3 focusing on controversies"
```

### Step 3: Parse JSON Results

Each call returns JSON:
```json
{
  "source": "perplexity|claude|gemini",
  "query": "the query",
  "timestamp": "ISO timestamp",
  "success": true,
  "content": "research findings...",
  "citations": ["url1", "url2"],
  "duration_ms": 1234
}
```

For `--all`, returns array of 3 results.

### Step 4: Synthesize Findings

**Confidence Levels:**
- **HIGH CONFIDENCE**: Corroborated by 2+ sources
- **MEDIUM CONFIDENCE**: Found by one source, seems reliable
- **LOW CONFIDENCE**: Single source, needs verification

**Structure:**
```markdown
## Key Findings

### [Topic Area 1]
**High Confidence:**
- Finding X (Sources: perplexity, claude)

**Medium Confidence:**
- Finding Z (Source: gemini only)

## Source Attribution
- **Perplexity**: [web/current events]
- **Claude**: [detailed analysis]
- **Gemini**: [multi-perspective synthesis]

## Conflicting Information
- [Note any disagreements]
```

---

## Extensive Research Workflow

### Step 1: Generate 8 Diverse Angles

- Core facts and current state
- Historical context and evolution
- Technical deep-dive
- Practical implications and applications
- Contrarian views and criticisms
- Future predictions and trends
- Cross-domain connections
- Edge cases and unusual perspectives

### Step 2: Launch 8 Parallel Queries

```bash
# All 8 in parallel (single message)
~/.claude/bin/research --all "angle 1: core facts about [topic]"
~/.claude/bin/research --all "angle 2: historical context of [topic]"
~/.claude/bin/research --all "angle 3: technical deep-dive on [topic]"
~/.claude/bin/research --all "angle 4: practical implications of [topic]"
~/.claude/bin/research --all "angle 5: criticisms around [topic]"
~/.claude/bin/research --all "angle 6: future predictions for [topic]"
~/.claude/bin/research --all "angle 7: cross-domain connections to [topic]"
~/.claude/bin/research --all "angle 8: edge cases of [topic]"
```

---

## API Keys Required

Located in `~/.claude/.env`:

| Feature | API Key | Required |
|---------|---------|----------|
| Perplexity | `PERPLEXITY_API_KEY` | For --perplexity |
| Gemini | `GOOGLE_API_KEY` | For --gemini |
| Claude | None | Built-in WebSearch |

---

## Critical Rules

### Parallel Execution
- ✅ Launch ALL research queries in ONE message (parallel Bash calls)
- ✅ Each query covers a different angle
- ❌ DON'T launch sequentially (kills speed benefit)
- ❌ DON'T wait between queries

### Error Handling
- If a source fails, proceed with successful results
- Note failures in the final report
- Check `success: false` in JSON for errors

---

## Research Metrics Template

Include at end of every research report:

```markdown
**📈 RESEARCH METRICS:**
- **Mode:** [Quick/Standard/Extensive]
- **Total Queries:** [X] (angles × 3 sources)
- **Sources:** Perplexity, Claude, Gemini
- **Confidence Level:** [High/Medium/Low] ([%])
```

---

## Example: Standard Research

**User:** "Research quantum computing developments"

**Kai executes:**
```bash
# 3 parallel Bash calls in ONE message
~/.claude/bin/research --all "quantum computing recent breakthroughs 2026"
~/.claude/bin/research --all "quantum computing practical applications timeline"
~/.claude/bin/research --all "quantum computing challenges limitations"
```

**Result:** 9 source queries (3 angles × 3 sources) in ~30-45 seconds.
