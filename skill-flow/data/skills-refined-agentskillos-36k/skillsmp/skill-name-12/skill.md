---
name: "<skill-name>"
description: "<One-line description of what this skill does and when to use it>"
triggers: ["<keyword1>", "<keyword2>", "<phrase>"]
tags: ["<tag1>", "<tag2>", "<tag3>"]
priority: <low|medium|high>
scope: <global|module|file|selection>
output: <code|markdown|json|files|analysis>
---

# <Skill Name>

## Instructions

- <Step 1: What inputs/context to collect>
- <Step 2: Key constraints or rules to follow>
- <Step 3: Output format or structure>
- <Step 4: Additional guidelines>

## Example

- Input: "<Sample user request>"
- Output: <Brief description of expected result>

```<language>
// Code example (if applicable)
```

<!--
TEMPLATE GUIDANCE (Remove this section when filling):

## name (frontmatter)
- Kebab-case identifier (e.g., "frontend-design")
- Short, descriptive (2-4 words)
- Used for file naming

## description (frontmatter)
- Single sentence explaining: WHAT + WHEN
- Include trigger phrases users might say
- Max 120 characters

## triggers (frontmatter)
- Array of keywords/phrases that should activate this skill
- Include verbs, nouns, common user phrases
- 3-8 triggers recommended
- Examples: ["build UI", "create component", "React", "dashboard"]

## tags (frontmatter)
- Cross-cutting categories for filtering/grouping
- Technology stack, domain, concern type
- 2-5 tags recommended
- Examples: ["frontend", "typescript", "angular", "testing"]

## priority (frontmatter)
- low: Background skills, rarely auto-selected
- medium: Standard skills, context-dependent selection
- high: Frequently needed, prefer in ambiguous cases

## scope (frontmatter)
- global: Applies to entire codebase/project
- module: Applies to specific module/package
- file: Applies to single file
- selection: Applies to code selection/region

## output (frontmatter)
- code: Generates code files/snippets
- markdown: Generates documentation/reports
- json: Generates structured data
- files: Creates/modifies multiple files
- analysis: Produces insights/recommendations

## Instructions section
- Bullet points only
- Action-oriented (start with verbs)
- Include inputs to collect
- Specify constraints/rules
- Define output structure
- Keep to 4-8 bullets max

## Example section
- Show realistic user input
- Show expected output format
- Include code snippet if skill involves code generation
- Use language-appropriate syntax highlighting
-->
