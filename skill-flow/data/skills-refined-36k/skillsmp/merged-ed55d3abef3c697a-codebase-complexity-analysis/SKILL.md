---
name: codebase-complexity-analysis
description: Use this skill to analyze a codebase for complexity and architectural issues based on Ousterhout's principles, identifying areas for improvement and technical debt.
---

# Codebase Complexity Analysis

This skill utilizes John Ousterhout's principles from "A Philosophy of Software Design" to evaluate the complexity of a codebase. It is designed for architecture reviews and identifying technical debt.

## Workflow

1. **Spawn an Analysis Agent**: Use the Task tool to create an `ousterhout-codebase-review` agent.
2. **Analyze the Codebase**: The agent will assess the specified codebase or directories for systemic complexity issues, including:
   - Module depth assessment
   - Leaky abstractions and information hiding violations
   - Consistency issues and complexity hotspots
   - Layer quality and abstraction boundaries
   - Signs of tactical vs strategic programming

3. **Output**: The agent will provide a summary, a module depth assessment table, and prioritized findings based on the analysis.

## Ousterhout's Principles

### Module Depth
- A deep module hides complexity behind a simple interface. Depth is qualitative, not quantitative.
- **Red flags**: Classes with many public methods but little internal logic, "Manager" or "Helper" classes, and wrapper methods that do not add value.

### Information Hiding
- Good modules should hide implementation details from callers.
- **Red flags**: Exposed internal types, configuration options revealing implementation choices, and temporal coupling.

### Pull Complexity Downward
- Complexity should be managed within the module rather than pushed onto callers.
- **Red flags**: Duplicated error handling and validation logic across callers.

### Change Amplification
- Poor abstraction boundaries lead to extensive changes across multiple files for simple modifications.
- **Red flags**: Changes requiring updates in many places and scattered similar code.

### Cognitive Load
- Code should minimize the mental burden on readers.
- **Red flags**: Magic parameters, implicit assumptions, and non-obvious ordering requirements.

### Interface Design
- General-purpose interfaces often outperform specialized ones.
- **Red flags**: APIs designed for a single caller and many similar functions with slight variations.

### Layer Quality
- Each layer should provide a distinct abstraction.
- **Red flags**: Pass-through layers and adjacent layers at similar abstraction levels.

### Consistency
- Similar operations should be performed similarly to avoid confusion.
- **Red flags**: Multiple patterns for the same operation and inconsistent naming conventions.

### Error Strategy
- Handle errors where context exists to provide meaningful responses.
- **Red flags**: Generic exceptions without context and forced error handling across callers.

### Comments as Design
- Comments should clarify the abstraction rather than restate implementation details.
- **Red flags**: Comments that describe code line-by-line and missing documentation of contracts.

### Strategic vs Tactical
- Strategic programming focuses on good design, while tactical programming leads to accumulated complexity.
- **Red flags**: Quick fixes that become permanent and lack of design consideration.

Use this skill to systematically evaluate and improve the architecture of your codebase.