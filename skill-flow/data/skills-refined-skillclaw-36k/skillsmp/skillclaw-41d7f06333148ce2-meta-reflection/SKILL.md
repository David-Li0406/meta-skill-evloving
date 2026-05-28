---
name: meta-reflection
description: Use this skill when the agent believes it has satisfied a user request, triggering a session review to identify improvements for future interactions.
---

# Meta-Reflection

## Overview

Completing work without reflecting is a missed improvement opportunity. Every completed request is a learning opportunity; capture insights before context is lost.

## When to Trigger

```
AFTER satisfying a user request (or believing you have):

1. PAUSE before final response
2. REFLECT on the session
3. IDENTIFY potential improvements
4. PRESENT findings to user
5. IMPLEMENT if approved
```

## The Reflection Protocol

```
FOR each completed request:

1. SESSION REVIEW
   - What did the user ask for?
   - What steps did I take?
   - Where did I struggle or backtrack?
   - What assumptions did I make?
   - What context was missing?

2. FRICTION ANALYSIS
   - Where did I waste effort?
   - What caused confusion or errors?
   - What required multiple attempts?
   - What knowledge would have helped?

3. IMPROVEMENT IDENTIFICATION
   Categories to consider:
   - AGENTS.md: Missing triggers, unclear instructions, missing skills
   - CLAUDE.md / project configs: Wrong assumptions, missing context
   - Skills: Missing skill, skill gaps, skill improvements
   - Tools: Missing capabilities, configuration issues
   - Workflows: Inefficient patterns, missing automation

4. FINDING VALIDATION
   For each potential improvement:
   - Is this generalizable (not one-off)?
   - Would this help future sessions?
   - Is the fix clear and actionable?
   - Which file(s) would change?

5. PRESENTATION
   Present findings to user with:
   - What I observed (specific friction)
   - What I recommend (specific change)
   - Which file(s) to update
   - Ask: "Should I make these updates?"

6. IMPLEMENTATION (if approved)
   - Make the changes
   - Verify changes are correct
   - Summarize what was updated
```

## Categories of Improvements

| Category | Examples | Target Files |
|----------|----------|--------------|
| Missing skill trigger | Skill exists but wasn't invoked | AGENTS.md, skill description |
| Unclear instructions | Misunderstood what to do | SKILL.md, CLAUDE.md |
| Missing skill | No skill for common pattern | New skill creation |
| Wrong assumptions | Assumed incorrect defaults | CLAUDE.md, config files |
| Missing context | Needed project-specific info | CLAUDE.md, . |