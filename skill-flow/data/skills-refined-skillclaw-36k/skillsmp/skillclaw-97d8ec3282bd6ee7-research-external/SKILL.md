---
name: research-external
description: Use this skill when you need to gather information from external sources such as documentation, web, and APIs, focusing on libraries, best practices, and general topics.
---

# External Research Workflow

Research external sources (documentation, web, APIs) for libraries, best practices, and general topics.

> **Note:** The current year is 2025. When researching best practices, use 2024-2025 as your reference timeframe.

## Invocation

```
/research-external <focus> [options]
```

## Question Flow (No Arguments)

If the user types just `/research-external` with no or partial arguments, guide them through this question flow. Use AskUserQuestion for each phase.

### Phase 1: Research Type

```yaml
question: "What kind of information do you need?"
header: "Type"
options:
  - label: "How to use a library/package"
    description: "API docs, examples, patterns"
  - label: "Best practices for a task"
    description: "Recommended approaches, comparisons"
  - label: "General topic research"
    description: "Comprehensive multi-source search"
  - label: "Compare options/alternatives"
    description: "Which tool/library/approach is best"
```

**Mapping:**
- "How to use library" → library focus
- "Best practices" → best-practices focus
- "General topic" → general focus
- "Compare options" → best-practices with comparison framing

### Phase 2: Specific Topic

```yaml
question: "What specifically do you want to research?"
header: "Topic"
options: []  # Free text input
```

Examples of good answers:
- "How to use Prisma ORM with TypeScript"
- "Best practices for error handling in Python"
- "React vs Vue vs Svelte for dashboards"

### Phase 3: Library Details (if library focus)

If user selected library focus:

```yaml
question: "Which package registry?"
header: "Registry"
options:
  - label: "npm (JavaScript/TypeScript)"
    description: "Node.js packages"
  - label: "PyPI (Python)"
    description: "Python packages"
  - label: "crates.io (Rust)"
    description: "Rust crates"
  - label: "Go modules"
    description: "Go packages"
```

Then ask for specific library name if not already provided.

### Phase 4: Depth

```yaml
question: "How thorough should the research be?"
header: "Depth"
options:
  - label: "Quick answer"
    description: "Just the essentials"
  - label: "Thorough research"
    description: "Multiple sources, examples, edge cases"
```

**Mapping:**
- "Quick answer" → --depth shallow
- "Thorough" → --depth thorough

### Phase 5: Output

```yaml
question: "What format do you want the output in?"
header: "Output Format"
options:
  - label: "Summary"
    description: "Concise overview of findings"
  - label: "Detailed report"
    description: "In-depth analysis with references"
```