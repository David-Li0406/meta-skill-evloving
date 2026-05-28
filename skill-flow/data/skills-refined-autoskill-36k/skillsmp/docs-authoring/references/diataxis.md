# Diátaxis Framework Details

## Decision Tree

Use this order to determine where documentation belongs:

1. **Is this about learning something new from scratch?** → `tutorials/`
   - Examples: "Learn idiomatic TQL", "Write a package", "Map data to OCSF"
   - Characteristics: Project-based, sequential, pedagogical

2. **Is this about doing a specific task?** → `guides/`
   - Examples: "Set up a node", "Load data from Kafka", "Configure enrichment"
   - Characteristics: Task-focused, practical, assumes some knowledge

3. **Is this about understanding how something works?** → `explanations/`
   - Examples: "Pipeline architecture", "TQL language design", "Secrets"
   - Characteristics: Conceptual, discusses "why", provides context

4. **Is this a technical specification?** → `reference/`
   - Examples: Function docs, operator docs, API specs, configuration options
   - Characteristics: Complete, accurate, structured, no tutorial content

## Section Writing Styles

| Section          | Writing style                                        |
| ---------------- | ---------------------------------------------------- |
| **Tutorials**    | Guide through a project; hold the reader's hand      |
| **Guides**       | Practical steps for a task; assume knowledge         |
| **Explanations** | Discuss concepts, architecture, design decisions     |
| **Reference**    | Accurate, complete technical descriptions; dry/terse |

## What NOT to Mix

- Don't add tutorial content to reference (no "let's learn" in function docs)
- Don't add reference material to tutorials (no exhaustive option lists)
- Don't add step-by-step guides to explanations (keep it conceptual)
- Don't add conceptual discussions to guides (just show how to do it)
