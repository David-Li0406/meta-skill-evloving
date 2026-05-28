# {{pattern_name}} Pattern

> {{description}}

## Purpose

{{purpose}}

## File Convention

**Location:** `{{file_location}}`
**Naming:** `{{naming_convention}}`
{{#if test_location}}
**Tests:** `{{test_location}}`
{{/if}}

## Structure

```
{{directory_structure}}
```

## Critical Conventions

<!-- Top 3-5 must-follow rules extracted from codebase analysis -->

{{#each critical_conventions}}
{{@index}}. **{{this.name}}**: {{this.explanation}}
{{/each}}

## Anti-Patterns

| Don't | Do Instead | Why |
|-------|------------|-----|
{{#each anti_patterns}}
| {{this.dont}} | {{this.do_instead}} | {{this.why}} |
{{/each}}

## Template (This Codebase)

```{{language}}
{{codebase_template}}
```

## Implementation Checklist

{{#each checklist_items}}
- [ ] {{this}}
{{/each}}

{{#if registration_steps}}
### Registration

{{#each registration_steps}}
- [ ] {{this.action}} in `{{this.file}}`
{{/each}}
{{/if}}

## Reference Implementations

| File | Demonstrates |
|------|--------------|
{{#each reference_files}}
| `{{this.file}}` | {{this.demonstrates}} |
{{/each}}

## Validation

```bash
{{#each validation_commands}}
{{this}}
{{/each}}
```

{{#if related_patterns}}
## Related Patterns

{{#each related_patterns}}
- [{{this.name}}]({{this.path}}) - {{this.relationship}}
{{/each}}
{{/if}}
