---
name: research
description: Use this skill when current web information is needed to avoid broken implementations and ensure secure coding practices.
---

# Skill body

## Philosophy
Research when getting it right matters. When current information saves hours of debugging, ensures secure implementations, or guides you to the right abstraction—research first.

## Natural Triggers
Clear signals that research is needed:
- Hitting an error that smells like an API change
- Implementing something security-critical (auth, payments, file handling)
- Making architecture decisions you'll live with for months
- Working with libraries you know evolve rapidly
- That moment of "wait, is this still how we do this?"

## Quick Check
- **When:** Mid-flow verification
- **Time:** Under a minute

**Examples:** 
- "Is useEffect still the way to handle this in React 18?"
- "Did Stripe change their webhook payload?"
- "What's the current Node LTS version?"

Just search, grab the answer, keep coding. No storage, no ceremony, no permission needed.

## Deep Dive
- **When:** The decision really matters
- **Time:** 5-15 minutes

**Examples:** 
- Choosing between competing technologies
- Understanding a new architectural pattern
- Debugging something that doesn't match documentation

Always ask first: "This needs deeper research (5-15 min). Should I dig into this now?" Let the user decide if they want to pause for research or continue with existing knowledge.

Research thoroughly, save findings in `research/[topic].md` for team reference.

## Tool Selection
Always use the best available web search. Priority order:
1. MCP servers (preferred when available):
   - Tavily MCP server
   - Exa MCP server
   - Other specialized search MCP servers
2. Built-in tools (fallback):
   - Cursor: web_search tool
   - Claude Code: Built-in web search

Tell the user which you're using:
- "Using Tavily MCP server for enhanced search capabilities"
- "Using Exa MCP server for code-focused research"
- "Using built-in web search (no MCP servers configured)"

This transparency helps users understand tool selection and configure MCP servers if desired.

## Search Strategy
Start with official sources - docs, changelogs, GitHub releases. Then expand to community discussions if needed.

## Output Format
Output should be scannable and actionable. Skip the fluff, get to what matters.

**Good pattern:**
## Stripe Checkout v4 Migration
**Breaking change:** redirectToCheckout() removed in v4

**New pattern:**
- Use Payment Element (unified UI)
- Or Checkout