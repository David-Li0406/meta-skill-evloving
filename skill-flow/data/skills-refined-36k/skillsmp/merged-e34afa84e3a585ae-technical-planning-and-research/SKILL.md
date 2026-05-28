---
name: technical-planning-and-research
description: Use this skill when you need to research, analyze, and create detailed technical implementation plans for scalable, secure, and maintainable solutions.
---

# Technical Planning and Research

Create comprehensive technical implementation plans through research, codebase analysis, solution design, and documentation.

## When to Use

Use this skill when:
- Planning new feature implementations
- Architecting system designs
- Evaluating technical approaches
- Creating implementation roadmaps
- Breaking down complex requirements
- Assessing technical trade-offs

## Core Responsibilities & Rules

Always honor **YAGNI**, **KISS**, and **DRY** principles. Be honest, brutal, straight to the point, and concise.

### Workflow Process

1. **Initial Analysis** → Read codebase documentation to understand context.
2. **Research Phase** → Define research scope and gather information.
3. **Synthesis** → Analyze gathered reports and identify optimal solutions.
4. **Design Phase** → Create architecture and implementation design.
5. **Plan Documentation** → Write a comprehensive plan.
6. **Review & Refine** → Ensure completeness, clarity, and actionability.

## Research Methodology

### Phase 1: Scope Definition
- Identify key terms and concepts to investigate.
- Determine recency requirements for information.
- Establish evaluation criteria for sources.

### Phase 2: Systematic Information Gathering
- Employ a multi-source research strategy, including:
  - Using `gemini` or `WebSearch` tools for information gathering.
  - Crafting precise search queries with relevant keywords.
  - Prioritizing results from recognized authorities.

### Phase 3: Analysis and Synthesis
- Analyze gathered information to identify common patterns and best practices.
- Evaluate pros and cons of different approaches, considering security and performance.

### Phase 4: Report Generation
Create a comprehensive markdown report with sections for:
- Executive Summary
- Research Methodology
- Key Findings
- Implementation Recommendations
- Resources & References

## Output Requirements

- DO NOT implement code - only create plans and reports.
- Ensure plans are self-contained with necessary context.
- Include code snippets or pseudocode when clarifying.
- Provide multiple options with trade-offs when appropriate.
- Save reports using a specified path with a descriptive filename.

## Quality Standards

- Be thorough and specific.
- Consider long-term maintainability.
- Validate against existing codebase patterns.
- Ensure all research meets accuracy, currency, completeness, and clarity standards.

## Important Notes

- Always create plans or reports in the CURRENT WORKING PROJECT DIRECTORY.
- Track the current working plan via session state to prevent version proliferation.
- Include a final review task to assess the work done and identify any necessary fixes or enhancements.

**Remember:** The quality of your plans and research directly impacts implementation success. Be comprehensive and consider all aspects of the solution.