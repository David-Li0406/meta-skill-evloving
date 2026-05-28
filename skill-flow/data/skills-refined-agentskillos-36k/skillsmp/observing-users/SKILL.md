---
name: observing-users
description: Diagnose user feedback using Mom Test framework - extracts Level 3 goals from bug reports and feature requests
allowed-tools:
  - Read
  - Write
  - WebFetch
  - Glob
  - Grep
---

# Observing Users Skill

Capture user feedback as structured diagnostic observations using the Level 3 framework.

---

## Core Principle

```
Quote → Profile → Level 3 Goal → Hypothesis Space → Validate → Act
```

Most feedback stops at surface level. This skill digs to the actionable truth: **What are they trying to accomplish?**

---

## When to Use

- User reports an issue or request
- Feedback appears in Discord/Telegram/support channels
- You notice behavioral patterns worth investigating
- Before building features based on user requests

---

## Auto-Trigger Detection

This skill should activate automatically when detecting:

| Pattern | Example | Action |
|---------|---------|--------|
| Bug report keywords | "not working", "missing", "can't find", "broken" | Start diagnostic |
| User quote blocks | `> "I can't see my..."` | Extract Level 3 goal |
| Discord/Telegram paste | `username — timestamp` format | Begin observation |
| "User says" framing | "A user reported that..." | Apply Mom Test |
| Support request | "How do I ask them...", "help diagnose" | Load this skill |

---

## Verify Before Asking

**Principle**: Don't ask what you can verify. Query first, ask only for client-side state.

| Type | Examples | Action |
|------|----------|--------|
| **Verifiable** | Vault deposits, stake amounts, transaction history, balances | Query on-chain/indexer FIRST |
| **Not Verifiable** | Browser/wallet type, console errors, what they see, network | Ask user |

**Anti-Pattern**: Asking "Did you complete the deposit?" when you can verify on-chain.
**Correct**: Query first, then ask "I see your deposit at block X. What are you seeing in the UI?"

---

## Anti-Patterns

| Bad Pattern | Why It's Bad | Do Instead |
|-------------|--------------|------------|
| Jump into code investigation | Builds understanding of system, not user | Ask Mom Test opener first |
| "Did you mean X?" | Leading, puts words in their mouth | "Tell me more about what you saw" |
| "What does [specific UI] show?" | Asks user to debug for us | "Walk me through what happened" |
| Correct their terminology | Dismissive, misses their mental model | Note discrepancy, ask for experience |
| Ask about verifiable data | Wastes a support round-trip | Query on-chain/indexer first |
| Propose solutions before diagnosis | May build the wrong thing | Extract Level 3 goal first |

---

## The Three Levels

| Level | Question | Example | Value |
|-------|----------|---------|-------|
| **Level 1** | What did they say? | "Rewards aren't updating" | Surface symptom |
| **Level 2** | What do they want? | "I want to see my rewards" | Stated desire |
| **Level 3** | What are they trying to accomplish? | "Decide when to burn based on accumulation" | Actionable truth |

**Always dig to Level 3.** Level 1-2 lead to building the wrong thing.

---

## Workflow

### Step 1: Capture Initial Quote

Preserve the exact user quote with context:

```markdown
### Initial Report
> "Im planning some henlo burns so gud to know how much im receiving"

**Source**: Discord #feedback
**Date**: 2026-01-19
**User**: papa_flavio
```

### Step 2: Profile the User

Classify based on behavioral evidence, not assumptions:

| Type | Evidence Signals |
|------|-----------------|
| **Decision-maker** | "planning X", "deciding when", "calculating" |
| **Builder-minded** | Technical details, API mentions, implementation ideas |
| **Trust-checker** | "just checking", frequent visits, verification behavior |
| **Casual** | Infrequent, basic questions, simple needs |

**Profile Template**:
```markdown
## User Profile

| Field | Value |
|-------|-------|
| **Type** | Decision-maker |
| **Behavior** | Checks daily for burn planning |
| **Stakes** | Real money — planning token burns |
| **Engagement** | High — reports issues with specific timing |
```

### Step 3: Extract Level 3 Goal

Parse the quote for the underlying goal:

```
Quote: "Im planning some henlo burns so gud to know how much im receiving"
       ↓
Level 1: Wants to know how much they're receiving
       ↓
Level 2: Wants accumulation data
       ↓
Level 3: Needs data to make burn timing decisions
```

**Goal Format**:
```markdown
### Goal (Level 3)
**What are they trying to accomplish?**
- Planning burn timing based on accumulation data
- Needs to know current/projected amounts to decide when to act
```

### Step 4: Generate Diagnostic Questions

Create questions following Mom Test principles:

**Good Questions** (about their life):
- "How do you decide when to burn? What info do you need to make that call?"
- "Walk me through the last time you did this."
- "What do you check before making that decision?"

**Bad Questions** (about your idea):
- "Would you use a burn calculator?"
- "Is the sidebar useful?"
- "Do you want a notification feature?"

**Question Template**:
```markdown
### Questions to Ask

- [ ] "How do you decide when to burn? What info do you need to make that call?"
- [ ] "The sidebar shows accumulation — is that not updating, or is it something else you need?"

### What We're Trying to Learn

| Question | What it reveals |
|----------|-----------------|
| What triggers burn decision? | Threshold vs calculation vs gut feel |
| Does sidebar serve the need? | Bug vs discoverability vs feature gap |
| Do they track elsewhere? | Workarounds we should absorb |
```

### Step 5: Map Hypothesis Space

Pre-map possible responses to gap types and actions:

```markdown
## Hypothesis Space

| If they say... | Gap type | Action |
|----------------|----------|--------|
| "I burn when I hit X amount" | Feature | Target tracking UI |
| "I calculate with price data" | Feature | Burn calculator |
| "I track in spreadsheet" | Feature | We're missing something |
| "Sidebar works but not updating" | Bug | Fix sidebar refresh |
| "Didn't know sidebar showed that" | Discoverability | Surface it better |
| "Need to see history to project" | Feature | Accumulation history chart |
```

### Step 6: Await and Record Responses

Track the conversation:

```markdown
### Responses

**2026-01-19** — papa_flavio:
> "I usually burn when I hit around 50k HENLO, but the sidebar stopped showing updates"

**Classification**: Bug (sidebar not updating) + Feature (threshold tracking)
```

### Step 7: Classify and Act

| Gap Type | Next Step |
|----------|-----------|
| **Bug** | File issue, fix immediately |
| **Discoverability** | `/craft` UI improvement with context |
| **Feature** | Add to PRD, prioritize based on user type |

**Link to /craft**:
```
/craft "accumulation threshold tracker" @grimoires/sigil/observations/papa_flavio-diagnostic.md
```

### Step 8: Update User Insights

After validation, extract confirmed insights:

```markdown
# grimoires/sigil/observations/user-insights.md

## Confirmed User Types

| User | Type | Evidence | Needs |
|------|------|----------|-------|
| papa_flavio | Decision-maker | "planning burns" | Accumulation data + threshold |

## Confirmed Gaps

| Gap | Type | Evidence | Resolution |
|-----|------|----------|------------|
| Sidebar not updating | Bug | User reports, reproduced | Fix refresh logic |
| No threshold tracking | Feature | "burn when I hit X" | Build tracker |
```

---

## File Structure

```
grimoires/sigil/observations/
├── {username}-diagnostic.md     # Individual diagnostic logs
├── user-insights.md             # Aggregated confirmed findings
└── open-questions.md            # Questions awaiting answers
```

---

## Integration with /craft

When running `/craft` for a user-facing component:

1. Check `observations/` for relevant diagnostics
2. Extract user type for physics adjustment
3. Reference specific gaps being addressed
4. Include diagnostic context in analysis box

**Example Analysis**:
```
┌─ Craft Analysis ───────────────────────────────────────┐
│                                                        │
│  Target:       AccumulationTracker                     │
│  Effect:       Local State (display only)              │
│                                                        │
│  User Context: papa_flavio (Decision-maker)            │
│                → "planning burns, needs threshold"     │
│                → Observation: papa_flavio-diagnostic   │
│                                                        │
│  Behavioral    Immediate | 100ms | None                │
│  Animation     spring(700, 35) | snappy                │
│  Material      Elevated | Soft shadow | 8px            │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## Mom Test Quick Reference

### Five Rules

1. **Talk about their life, not your idea**
2. **Ask about specifics in the past, not generics about the future**
3. **Talk less, listen more**
4. **Seek disconfirming evidence**
5. **Push for commitment or advancement**

### Question Transforms

| Bad (Opinion) | Good (Behavior) |
|---------------|-----------------|
| "Would you use X?" | "How do you handle X today?" |
| "Is this useful?" | "When did you last need this?" |
| "Do you want Y?" | "Tell me about a time Y would have helped" |
| "How often would you..." | "How often did you..." |

### Red Flags in Responses

| Red Flag | What it means |
|----------|---------------|
| "I would probably..." | Hypothetical, not real behavior |
| "I think I might..." | Opinion, not evidence |
| "That sounds useful" | Politeness, not commitment |
| "Everyone wants..." | Projection, not personal experience |

### Green Flags

| Green Flag | What it means |
|------------|---------------|
| "Last week I..." | Specific past behavior |
| "I've been doing X workaround" | Real pain, evidence of need |
| "Let me show you my spreadsheet" | Commitment through action |
| "I check every morning before..." | Workflow integration |

---

## Example: Complete Diagnostic

```markdown
# Papa_Flavio Diagnostic Log

## User Profile

| Field | Value |
|-------|-------|
| **Type** | Decision-maker |
| **Behavior** | Checks daily for burn planning |
| **Stakes** | Real money — planning HENLO burns |
| **Engagement** | High — reports timing issues |

---

## Level 3 Diagnostic

### Initial Report
> "Im planning some henlo burns so gud to know how much im receiving"

### Goal (Level 3)
**What are they trying to accomplish?**
- Planning burn timing based on accumulation
- Decision: When to execute burn for optimal value

### Questions Asked

- [x] "How do you decide when to burn?"
- [x] "Does the sidebar show what you need?"

### Responses

**2026-01-19**:
> "I burn when I hit 50k, but sidebar stopped updating 2 days ago"

---

## Classification

| Gap | Type | Confidence | Action |
|-----|------|------------|--------|
| Sidebar not refreshing | Bug | Confirmed | Fix immediately |
| No threshold indicator | Feature | Implied | Consider for roadmap |

---

## Resolution

- **Bug**: Fixed in commit abc123 (sidebar WebSocket reconnect)
- **Feature**: Added to Sprint 5 backlog (threshold alerts)

---

## Insights Extracted

→ Added to user-insights.md:
- User type: Decision-maker (burn planning workflow)
- Workflow dependency: Accumulation data → burn decision
- Frequency: Daily check
```

---

## Agent Browser Integration

For web3 apps, use the agent-browser MCP to simulate user view:

| Capability | Use Case |
|------------|----------|
| **Connect as address** | View-only impersonation of user's wallet |
| **See what user sees** | Render the app as if we were that address |
| **Inspect data flow** | Check indexer response → hook processing → render |
| **Screenshot** | Capture actual UI state for comparison |

**Workflow**:
1. Get user's address from their report
2. Use HUD's Lens to impersonate their view
3. Query indexer/on-chain data for their address
4. Compare expected vs actual data at each layer
5. Only THEN ask about client-side state if needed

---

## Related

- `/craft` - Generate with observation context
- `/taste-synthesize` - Pattern detection from signals
- `/plan-and-analyze` - Full PRD discovery
