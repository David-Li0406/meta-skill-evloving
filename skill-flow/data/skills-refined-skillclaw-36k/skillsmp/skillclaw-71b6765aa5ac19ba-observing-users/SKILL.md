---
name: observing-users
description: Use this skill when you need to diagnose user feedback and extract actionable insights from bug reports and feature requests using the Mom Test framework.
---

# Skill body

## Core Principle

```
Quote → Profile → Level 3 Goal → Hypothesis Space → Validate → Act
```

Most feedback stops at surface level. This skill digs to the actionable truth: **What are they trying to accomplish?**

## When to Use

- User reports an issue or request
- Feedback appears in Discord/Telegram/support channels
- You notice behavioral patterns worth investigating
- Before building features based on user requests

## Auto-Trigger Detection

This skill should activate automatically when detecting:

| Pattern | Example | Action |
|---------|---------|--------|
| Bug report keywords | "not working", "missing", "can't find", "broken" | Start diagnostic |
| User quote blocks | `> "I can't see my..."` | Extract Level 3 goal |
| Discord/Telegram paste | `username — timestamp` format | Begin observation |
| "User says" framing | "A user reported that..." | Apply Mom Test |
| Support request | "How do I ask them...", "help diagnose" | Load this skill |

## Verify Before Asking

**Principle**: Don't ask what you can verify. Query first, ask only for client-side state.

| Type | Examples | Action |
|------|----------|--------|
| **Verifiable** | Vault deposits, stake amounts, transaction history, balances | Query on-chain/indexer FIRST |
| **Not Verifiable** | Browser/wallet type, console errors, what they see, network | Ask user |

**Anti-Pattern**: Asking "Did you complete the deposit?" when you can verify on-chain.  
**Correct**: Query first, then ask "I see your deposit at block X. What are you seeing in the UI?"

## Anti-Patterns

| Bad Pattern | Why It's Bad | Do Instead |
|-------------|--------------|------------|
| Jump into code investigation | Builds understanding of system, not user | Ask Mom Test opener first |
| "Did you mean X?" | Leading, puts words in their mouth | "Tell me more about what you saw" |
| "What does [specific UI] show?" | Asks user to debug for us | "Walk me through what happened" |
| Correct their terminology | Dismissive, misses their mental model | Note discrepancy, ask for experience |
| Ask about verifiable data | Wastes a support round-trip | Query on-chain/indexer first |