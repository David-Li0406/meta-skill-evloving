# Workflow Patterns

## Sequential Workflows

For complex tasks, break operations into clear, sequential steps. It is often helpful to give an AI agent an overview of the process near the beginning of SKILL.md:

```markdown
Upgrading a dependency across a codebase involves these steps:

1. Inventory current usage (search, dependency graph)
2. Update versions and resolve peer dependencies
3. Apply mechanical refactors (codemods/scripts if needed)
4. Fix typecheck/build errors
5. Validate with tests and CI
```

## Conditional Workflows

For tasks with branching logic, guide an AI agent through decision points:

```markdown
1. Determine the modification type:
   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow: [steps]
3. Editing workflow: [steps]
```