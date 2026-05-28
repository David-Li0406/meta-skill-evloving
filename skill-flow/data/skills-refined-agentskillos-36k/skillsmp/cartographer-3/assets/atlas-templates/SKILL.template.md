---
name: atlas
description: Codebase navigation for {{project_name}}. Use FIRST for "where is", "find", "locate", "what file", "how does X work", pattern lookup, or exploring unfamiliar code. Routes to domain docs without file searches.
---

# {{project_name}} Codebase Discovery

## Project Structure

```
{{project_structure}}
```

{{#if dependency_notes}}
{{dependency_notes}}
{{/if}}

## Domain Router

Read ONLY the relevant reference based on query keywords:

| Keywords | Reference |
|----------|-----------|
{{#each domain_router_rows}}
| {{this.keywords}} | [{{this.reference}}]({{this.reference}}) |
{{/each}}

## Pattern Router

For implementation tasks, read the relevant pattern guide:

| Task | Pattern Guide |
|------|---------------|
{{#each pattern_router_rows}}
| {{this.task}} | [{{this.guide}}]({{this.guide}}) |
{{/each}}

## Schema Reference

For file patterns, technologies, validation commands, and anti-patterns: [references/schema.yaml](references/schema.yaml)

## Implementation Pre-flight

When asked to **implement, create, add, or modify** code (not just questions or exploration):

### Step 1: Check Pattern Match

Read `keyword_index` from [references/schema.yaml](references/schema.yaml) and match against the request.

### Step 2: Surface Context (if matched)

If patterns match, briefly note:
- Matched pattern(s) and their `file_convention`
- Any `anti_patterns_summary` as warnings
- Location of `example_files` for reference

Example output:
```
📚 Atlas: This task matches the **controllers** pattern
- File location: `src/controllers/{Name}Controller.ts`
- Example: `src/controllers/UserController.ts`
- Avoid: 3 documented anti-patterns (direct DAO imports, etc.)

For full spec workflow: `/navigator:plan <task>`
```

### Step 3: Quick Reference Mode

For fast implementation with atlas guidance (without full spec):
1. Read the pattern's `file_convention` and `test_convention`
2. Study one `example_file` as reference
3. Keep `anti_patterns_summary` visible during implementation
4. Follow `registration` steps if creating new files

### Skip Conditions

Skip pre-flight when:
- Request is exploratory ("where is", "how does", "what is")
- User already invoked `/navigator:plan` or `/navigator:build`
- User explicitly says "skip atlas" or "just do it"

{{#if task_quick_reference}}
## Task-Type Quick Reference

When working on specific task types, prioritize these references:

| Task | Primary References |
|------|-------------------|
{{#each task_quick_reference}}
| {{this.task}} | {{this.references}} |
{{/each}}
{{/if}}
