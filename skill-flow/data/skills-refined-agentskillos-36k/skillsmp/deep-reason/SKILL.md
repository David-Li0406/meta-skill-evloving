---
name: deep-reason
description: Esta skill debe usarse cuando el usuario pide "pensemos esto a fondo", "analicemos paso a paso", "evaluemos opciones", "razonemos sobre esto", "pensemos detenidamente", "meditemos", "qué me sugieres", "qué me recomiendas", "esto es complejo", "esto es complicado", "problema grande", o ante problemas que requieren análisis profundo, afectan múltiples componentes del sistema, tienen implicaciones arquitectónicas importantes, o representan decisiones de diseño con impacto significativo. IMPORTANTE: Invocar esta skill en lugar de usar sequential-thinking MCP directamente - la skill proporciona workflow estructurado con generación de documentos de análisis.
model: claude-opus-4-5-20251101
version: 0.1.0
user-invocable: true
---

To engage in deep, structured reasoning for complex problems, apply the sequential-thinking approach with these guidelines:

## Thought Process Guidelines

During the sequential thinking process:

### 1. Initial Thoughts: Problem Space Definition

- **Reduce scope** if the problem is too broad or unfocused
- **Create the problem space**: Define the problem itself WITHOUT any influence from solutions or tools
  - See the problem as it truly is, not through the lens of potential solutions
  - Identify core constraints, requirements, and success criteria
  - Separate facts from assumptions

### 2. Solution Generation

- Generate **multiple options or solutions** to the stated problem
- Consider diverse approaches, not just the most obvious ones
- Think creatively about different paths to the goal

### 3. Information Gathering

- **Gather information** as needed throughout the thought process
- Use tools (Read, Grep, Glob, WebFetch, MCPs, specialized agents, etc.) to understand:
  - The problem better
  - Existing code/patterns
  - Any proposed solutions
  - Technical constraints or documentation

### 4. Option Evaluation

- **Evaluate each option** thoroughly, considering:
  - **Pros**: Benefits, strengths, advantages
  - **Cons**: Drawbacks, risks, limitations
  - Trade-offs between options
  - Implementation complexity
  - Long-term maintainability

### 5. Use Branches for Multiple Options

- When thinking through **multiple distinct options or solutions**, use the **branch feature** of the MCP:
  - `branchFromThought`: Specify which thought number is the branching point
  - `branchId`: Give each branch a descriptive identifier (e.g., "option-redis", "option-inmemory")
- This allows parallel exploration of different approaches

## After Completing the Thought Chain

After completing the sequential thinking process and reaching a conclusion:

1. Present findings to the user concisely
2. Ask if they want a summary document using the `AskUserQuestion` tool:
   - Question: "Would you like me to generate a summary document of the knowledge and analysis generated during this reasoning process?"
   - Options:
     - "Yes, generate summary" (description: "I'll create a detailed document with the complete analysis, evaluated options, and conclusions")
     - "No, continue without summary" (description: "We'll proceed without generating the summary document")

3. When user chooses "Yes, generate summary":
   - Use the template from [`summary-template.md`](summary-template.md) in this skill directory
   - Fill template sections with information from the thought chain
   - Save to an appropriate location (`docs/`, project root, or user-specified)
   - Use descriptive filename with timestamp (e.g., `sequential-reasoning-summary-2026-01-14.md`)

## Important Notes

- **Be thorough but efficient**: Don't add thoughts just to increase the count
- **Revise when needed**: Use `isRevision: true` and `revisesThought` if earlier thinking was flawed
- **Branch when exploring**: Use branches to explore multiple paths simultaneously
- **Gather context**: Don't hesitate to use tools mid-thought-chain to gather necessary information
- **Express uncertainty**: If unsure, express it and explore alternatives
- **Stop when done**: Set `nextThoughtNeeded: false` only when truly satisfied with the solution

## Resources

### Summary Template

- **[`summary-template.md`](summary-template.md)** - Comprehensive template for knowledge synthesis documents including:
  - Problem space definition
  - Options generation and evolution tracking
  - Comparative analysis (tables for 2 options, lists for 3+)
  - Conclusions with pros/cons
  - Recommendations and next steps
