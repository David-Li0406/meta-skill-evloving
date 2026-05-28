---
name: research
description: Self-healing documentation lookup. Use when wondering how something
  in the Awareness project works, where files live, or how to do something technical.
  Queries tech RAG and spawns improvement agents for gaps.
---

# Research Skill (Self-Healing Documentation)

When you need to know how something works in this project, use this process:

## 1. Query Tech RAG First

```
mcp__pps__tech_search(query="your question")
```

Evaluate the results:
- **Score > 0.5 + clear answer**: Use it, you're done
- **Score 0.3-0.5 or partial answer**: Use what's there, flag for improvement
- **Score < 0.3 or missing answer**: Note the gap, answer from code/memory if possible

## 2. If Answer Was Insufficient

Don't let a bad answer block you. Do both:

**A. Answer the question anyway** - read code, check files, use your knowledge

**B. Spawn a background doc-fixer** (optional, for significant gaps):

```
Task tool with:
  subagent_type: "general-purpose"
  model: "haiku"
  run_in_background: true
  prompt: |
    Documentation gap found. Question: "[the question]"
    Tech RAG returned score [X] with incomplete answer.

    Your task:
    1. Find the actual answer by reading relevant code/files
    2. Identify which doc should contain this info (check mcp__pps__tech_list())
    3. Either:
       - If doc exists: note what section needs adding
       - If no doc covers this: draft a new doc
    4. Report your findings (don't actually edit files - just report)
```

## 3. Common Questions Worth Checking

Before grepping through code, try tech_search for:
- "How does [feature] work?"
- "Where does [thing] live?"
- "How do I [action]?"
- "What is [concept]?"

The tech RAG has 20+ docs and 584 chunks. Often faster than code exploration.

## 4. Known Gap Areas (from audit)

These topics currently have poor tech RAG coverage:
- Scene file locations and management
- Daemon restart procedures
- Inventory database schema and location
- Word-photo creation workflow (tool vs manual)
- MCP tool signatures and return formats

If your question touches these areas, expect to read code directly.

## 5. Improving Coverage Over Time

Every time you find an answer that SHOULD have been in the docs:
- Note it mentally
- When convenient, update the relevant doc
- Re-ingest with `mcp__pps__tech_ingest(filepath, category)`

The goal: documentation that heals itself through use.

## Remember

- Don't block on bad docs - answer first, improve later
- Background agents can fix gaps while you keep working
- Log patterns of missing info - they reveal systematic gaps
- The tech RAG is a tool, not a crutch - code is always authoritative
