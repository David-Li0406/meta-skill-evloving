# Research Workflow

## Purpose

Delegate research to subagents to keep main context clean while gathering external patterns, documentation, and best practices.

---

## Research Strategy

**Always research for:**
1. Domain-specific patterns
2. Library/API documentation
3. Latest best practices
4. Relevant examples

**Token budget:** ~2000 tokens per subagent, ~500 tokens returned

---

## Research Subagent Template

```python
Task(
    subagent_type="prompt-researcher",
    description="Research for $TOPIC",
    prompt="""
    # Research Task: $TOPIC

    ## Context
    - Mode: $MODE (transform/debug/create)
    - Domain: $DOMAIN
    - Task type: $TASK_TYPE

    ## Research Questions
    1. $QUESTION_1
    2. $QUESTION_2
    3. $QUESTION_3

    ## Tools to Use
    - mcp__Ref__ref_search_documentation: For library docs
    - mcp__mcp-server-firecrawl__firecrawl_search: For web patterns
    - Read .claude/shared-imports/prompt-engineering-examples.md

    ## Output Format
    Return condensed findings in max 500 tokens:

    ### Top Patterns (2-3)
    - Pattern 1: [brief description + when to use]
    - Pattern 2: [brief description + when to use]

    ### Relevant Examples
    - [condensed example 1]
    - [condensed example 2]

    ### Key Optimizations
    - [optimization 1]
    - [optimization 2]

    ### Pitfalls to Avoid
    - [pitfall 1]
    - [pitfall 2]
    """
)
```

---

## Research by Domain

### Technical/API Prompts

```python
Task(
    subagent_type="prompt-researcher",
    description="Research API prompt patterns",
    prompt="""
    Research API integration prompts:

    1. Search Ref MCP for: "$API_NAME documentation"
    2. Find: Parameter handling, error responses, rate limits
    3. Look for: ReAct pattern examples for API tools

    Return: API-specific prompt elements, tool definition format
    """
)
```

### Agent/Subagent Prompts

```python
Task(
    subagent_type="prompt-researcher",
    description="Research agent prompt patterns",
    prompt="""
    Research agent architecture prompts:

    1. Search: "Claude Code subagent patterns"
    2. Read: prompt-engineering-examples.md sections on Meta-Prompting
    3. Find: Agent orchestration patterns

    Return: Agent prompt structure, handoff patterns
    """
)
```

### Creative/Generation Prompts

```python
Task(
    subagent_type="prompt-researcher",
    description="Research creative prompts",
    prompt="""
    Research creative generation prompts:

    1. Search: Self-Refine patterns for quality
    2. Find: Style guide integration examples
    3. Look for: Constraint specification patterns

    Return: Quality control patterns, style enforcement
    """
)
```

---

## Parallel Research

**For complex prompts, launch multiple research subagents:**

```python
# Launch in parallel (single message, multiple Task calls)

# Pattern research
Task(
    subagent_type="prompt-researcher",
    description="Research patterns",
    prompt="..."
)

# Domain research
Task(
    subagent_type="prompt-researcher",
    description="Research domain",
    prompt="..."
)

# Example research
Task(
    subagent_type="prompt-researcher",
    description="Find examples",
    prompt="..."
)
```

---

## Research Aggregation

**After subagents return:**

```markdown
## Research Summary

### Subagent 1: Patterns
[Condensed findings]

### Subagent 2: Domain
[Condensed findings]

### Subagent 3: Examples
[Condensed findings]

### Synthesis
- Primary pattern: [selected]
- Key optimizations: [list]
- Examples to adapt: [list]
```

---

## MCP Tool Usage

### Ref MCP (Documentation)

```python
mcp__Ref__ref_search_documentation(
    query="$LIBRARY $TOPIC documentation"
)

mcp__Ref__ref_read_url(
    url="$DOC_URL"  # From search results
)
```

### Firecrawl (Web Patterns)

```python
mcp__mcp-server-firecrawl__firecrawl_search(
    query="prompt engineering $PATTERN $DOMAIN 2024 2025",
    limit=5
)
```

---

## Version

**Version**: 1.0.0
