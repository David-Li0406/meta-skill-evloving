# Slash Command Structure Reference

## Understanding Slash Commands as Snippets

**Commands are templates/snippets that get inserted into the chat conversation.** When a user invokes a slash command in Cursor IDE, the entire command file content is inserted into the chat. The user then fills in placeholder areas (like the "Input Context:" section) with their specific information.

This means:
- Commands should be self-contained and ready to paste into a chat
- Placeholders should be clear and easy to fill in
- Instructions can guide what information is needed, but the actual input area should be simple (typically a single "Input Context:" section)
- Avoid complex multi-field forms; instead, provide guidance in instructions and use a simple placeholder that users can fill with their context

## Example Command Template

Most DevAgent commands follow this structure, but workflows may require variations based on their specific needs. Use this as a starting point and adapt as necessary:

```markdown
# Command Name (Command)

## Instructions

1. You will receive a prompt or context for this workflow.

2. Using only `.devagent/**`, follow the workflow steps and write outputs under `.devagent/workspace/` as the workflow specifies.

3. Follow the `.devagent/core/workflows/[workflow-name].md` workflow and execute it based on the following input:

---

**Input Context:**
```

**Note**: Some workflows may have different logical requirements that call for variations in structure. However, remember that commands are snippets—they get inserted into chat as-is. Keep the structure simple and focused:
- Provide workflow-specific guidance in the Instructions section
- Use a single "Input Context:" placeholder (or a simple template structure) for user input
- Avoid complex multi-field forms; instead, explain in instructions what information is needed and let users provide it in the input context area

## Command File Location

- **Source**: `.agents/commands/[command-name].md`
- **Symlink**: `.cursor/commands/[command-name].md` (symlinked from source)

## Naming Conventions

- **Format**: Kebab-case (lowercase with hyphens)
- **Examples**: `create-plan.md`, `research.md`, `clarify-feature.md`
- **Avoid**: Generic names like `help.md` or `test.md`

## Common Components

These components are typically present in commands, but may vary based on workflow needs:

1. **Command Title**: Title case version of command name with "(Command)" suffix
2. **Instructions Section**: Execution instructions that guide the agent; can include workflow-specific guidance about what inputs are needed
3. **Workflow Reference**: Path to corresponding workflow in `.devagent/core/workflows/`
4. **Input Context Placeholder**: Simple placeholder for user input (typically a single "Input Context:" section). Since commands are snippets, keep this simple—users will fill it in after the command is inserted into chat

## Workflow Correspondence

Commands should reference a corresponding workflow file:
- Workflow location: `.devagent/core/workflows/[workflow-name].md`
- Default: Workflow name matches command name
- Override: Can specify different workflow name if needed

## Symlink Requirements

Commands must be symlinked to `.cursor/commands/` for Cursor IDE integration:

```bash
# Relative symlink path
../../.agents/commands/[command-name].md → .cursor/commands/[command-name].md
```

## Integration Checklist

When creating a new command:

- [ ] Command file created in `.agents/commands/[command-name].md`
- [ ] Command structure matches workflow requirements (use template as starting point)
- [ ] Workflow file referenced correctly
- [ ] Instructions clearly guide agent to execute the workflow
- [ ] Symlink created in `.cursor/commands/[command-name].md`
- [ ] Command added to `.agents/commands/README.md`

## Example: Complete Command Creation

```bash
# 1. Create command file
python3 scripts/create_command.py my-new-command

# 2. Create symlink
python3 scripts/create_symlink.py my-new-command

# 3. Update README (manual step)
# Add entry to .agents/commands/README.md
```
