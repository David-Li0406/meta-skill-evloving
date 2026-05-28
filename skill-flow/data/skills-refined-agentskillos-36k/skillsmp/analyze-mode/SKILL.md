---
name: analyze-mode
description: Deep analysis mode. Gather comprehensive context before diving deep. Use for investigation, debugging, and understanding complex systems.
---

# Analyze Mode

> **ACTIVATION**: When loaded, gather comprehensive context before any deep analysis.

## Protocol

**ANALYSIS MODE - Context First, Conclusions Second**

### Phase 1: Context Gathering (Parallel)

Deploy 2-4 agents for comprehensive context:

```
// Internal context (1-2 agents)
task(agent="explore", prompt="Find all implementations of [topic]", background=true)
task(agent="explore", prompt="Find tests and usage patterns for [topic]", background=true)

// External context (if libraries involved)
task(agent="researcher", prompt="Find official docs for [library]", background=true)
task(agent="researcher", prompt="Find known issues and solutions", background=true)
```

### Phase 2: Direct Analysis

While agents run, use direct tools:

| Tool | Purpose |
|------|---------|
| `search_semantic` | Natural language code search |
| `find_similar` | Find similar code patterns |
| `find_dependencies` | What depends on X? |
| `call_graph` | Function caller/callee relationships |
| `impact_analysis` | Change risk assessment |
| `grep` | Find specific patterns |
| `ast_grep_search` | Structural analysis |
| `lsp_goto_definition` | Jump to symbol definition |
| `lsp_find_references` | Find all usages |
| `lsp_symbols` | Document/workspace symbol search |
| `lsp_diagnostics` | Type errors before build |
| `git log -S` | History evolution |
| `git blame` | Change attribution |

### Phase 3: Oracle Consultation (If Complex)

**Escalate to Oracle when:**
- Architecture spans multiple systems
- Debugging has failed 2+ times
- Trade-off analysis needed
- Root cause remains unclear

```
task(agent="oracle", prompt="Analyze [problem] given context...")
```

## Analysis Framework

### For Debugging

1. **Reproduce** - Can you trigger the issue?
2. **Isolate** - Where exactly does it fail?
3. **Hypothesize** - What could cause this?
4. **Test** - Verify each hypothesis
5. **Fix** - Address root cause, not symptom

### For Investigation

1. **Scope** - What are the boundaries?
2. **Dependencies** - What does it depend on?
3. **Dependents** - What depends on it?
4. **Patterns** - How is it typically used?
5. **Edge Cases** - What are the limits?

### For Architecture

1. **Current State** - What exists today?
2. **Requirements** - What must be satisfied?
3. **Options** - What approaches are viable?
4. **Trade-offs** - What are the costs/benefits?
5. **Recommendation** - What should we do?

## Output Requirements

Synthesize analysis into:

```markdown
## Analysis Summary

**Subject:** [What was analyzed]

**Context Gathered:**
- [Finding 1 from explore/researcher]
- [Finding 2]

**Key Observations:**
- [Observation 1]
- [Observation 2]

**Root Cause / Conclusion:**
[Clear statement]

**Recommended Action:**
[Specific next steps]

**Confidence Level:** [High/Medium/Low] - [Reasoning]
```
