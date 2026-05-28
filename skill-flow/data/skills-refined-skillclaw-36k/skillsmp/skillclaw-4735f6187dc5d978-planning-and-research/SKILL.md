---
name: planning-and-research
description: Use this skill when you need to research, analyze, and create detailed technical implementation plans for scalable, secure, and maintainable solutions.
---

# Skill body

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
2. **Research Phase** → Define research scope:
   - Identify key terms and concepts.
   - Determine recency requirements.
   - Establish evaluation criteria for sources.
   - Set boundaries for research depth.
3. **Systematic Information Gathering**:
   - Use `gemini` or `WebSearch` tools to gather information.
   - Craft precise search queries with relevant keywords.
   - Prioritize results from recognized authorities.
4. **Deep Content Analysis**:
   - Analyze official documentation, API references, and technical specifications.
   - Review README files and changelogs from relevant repositories.
5. **Synthesis** → Analyze gathered information to identify optimal solutions.
6. **Solution Design** → Create architecture and implementation design.
7. **Plan Documentation** → Write a comprehensive plan, ensuring it is self-contained with necessary context.
8. **Review & Refine** → Ensure completeness, clarity, and actionability.

## Output Requirements

- DO NOT implement code - only create plans.
- Respond with the plan file path and summary.
- Include code snippets/pseudocode when clarifying.
- Provide multiple options with trade-offs when appropriate.
- Fully respect the `./docs/development-rules.md` file.

### Plan Directory Structure
```
plans/
└── {date}-plan-name/
    ├── research/
    │   ├── researcher-XX-report.md
    │   └── ...
    ├── reports/
    │   ├── XX-report.md
    │   └── ...
    ├── scout/
    │   ├── scout-XX-report.md
    │   └── ...
    ├── plan.md
    ├── phase-XX-phase-name-here.md
    └── ...
```

## Active Plan State

Track the current working plan via session state to prevent version proliferation.