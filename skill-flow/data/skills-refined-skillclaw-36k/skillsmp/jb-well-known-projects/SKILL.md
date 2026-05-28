---
name: jb-well-known-projects
description: |
  Canonical Juicebox project IDs and names. Use when: (1) user asks about REV,
  Revnet Network, NANA, JBX, or other well-known projects, (2) need to look up
  a popular project, (3) user mentions a token symbol like $REV, $NANA, $JBX.
  CRITICAL: These are THE major projects in the ecosystem - always check this
  mapping before searching. REV is project 3 on ALL chains.
author: Claude Code
version: 1.0.0
date: 2026-01-19
---

# Juicebox Well-Known Projects

## Problem
The assistant failed to find "Revnet Network" / $REV even though it's one of the most
important projects in the ecosystem with a well-known, fixed project ID. This caused
a poor user experience where the assistant asked clarifying questions instead of just
looking it up.

## Context / Trigger Conditions
- User asks about a well-known project by name or token symbol
- User mentions REV, NANA, JBX, Bananapus, Revnet Network, etc.
- Need to query project data for a popular project
- Looking for "the" canonical example of a pattern (e.g., "the revnet")

## Solution: Well-Known Project Mappings

### CRITICAL - Memorize These

| Project Name | Token | Project ID | Chains | Notes |
|-------------|-------|------------|--------|-------|
| **Revnet Network** | $REV | **3** | ETH, OP, Base, Arbitrum (ALL) | THE canonical revnet. Same ID on ALL chains. |
| **NANA / Bananapus** | $NANA | **1** | ETH, OP, Base, Arbitrum (ALL) | First revnet. Same ID on ALL chains. |
| **JuiceboxDAO** | $JBX | **1** | ETH mainnet (V3 only) | The OG project. V3 on mainnet only. |
| **Juicy Vision** | $JUICY | **1** | OP, Base, Arbitrum | This app's project. |

### Query Strategy

1. **If user mentions a well-known name/symbol**: Look up by project ID directly
2. **For REV**: Always query project ID 3 - it exists on ALL chains with same ID
3. **For NANA**: Always query project ID 1 - it exists on ALL chains with same ID
4. **Don't search by name first** - use the known ID

### Example Queries

```typescript
// For REV on any chain
const revProjectId = 3n
// Works on: ETH, Optimism, Base, Arbitrum

// For NANA on any chain
const nanaProjectId = 1n
// Works on: ETH, Optimism, Base, Arbitrum

// Query directly - don't search
const project = await getProject(chainId, revProjectId)
```

## Verification
- REV (project 3) should return "Revnet Network" or "$REV" in metadata
- NANA (project 1) should return "Bananapus" or "$NANA" in metadata
- Both exist on all 4 chains with identical project IDs

## Notes

### Why Same ID on All Chains?
Revnets use CREATE2 deployment with deterministic addresses and the REVDeployer
reserves specific project IDs. Projects 1, 2, 3 are reserved across all chains.

### Common Mistakes to Avoid
1. **Don't ask "which chain?"** for REV/NANA - they're on ALL chains, same ID
2. **Don't search by name** - use the known project ID
3. **Don't say "I need to find it"** - you know exactly where it is
4. **Don't guess project IDs** - these mappings are canonical

### Expanding This List
When a user tells you a project's ID, remember it. Popular projects tend to have
low IDs (1-100) as they were created early.

## Anti-Pattern: What NOT To Do

❌ "Let me search for the Revnet Network project..."
❌ "Which chain is REV on?"
❌ "I found Project #21 which might be associated with REV..."
❌ "Can you share a link to help me find it?"

## Correct Pattern

✅ "REV is project 3. Let me fetch its current state from [chain]..."
✅ "NANA is project 1 on all chains. Here's the treasury balance..."
✅ Directly query the known project ID without searching
