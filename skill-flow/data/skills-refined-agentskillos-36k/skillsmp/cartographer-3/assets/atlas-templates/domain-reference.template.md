# {{domain_name}}

> **Location**: `{{location}}`
> **File Count**: {{count}}
> **Confidence**: {{confidence}}

## Purpose

{{purpose}}

## Directory Structure

```
{{directory_tree}}
```

## Key Files

| File | Purpose |
|------|---------|
{{#each key_files}}
| `{{this.path}}` | {{this.purpose}} |
{{/each}}

## File Patterns

| Pattern | Example | Count |
|---------|---------|-------|
{{#each file_patterns}}
| `{{this.pattern}}` | `{{this.example}}` | {{this.count}} |
{{/each}}

{{#if common_tasks}}
## Common Tasks

{{#each common_tasks}}
### {{this.name}}

{{this.description}}

**Files involved:**
{{#each this.files}}
- `{{this}}`
{{/each}}

{{/each}}
{{/if}}

{{#if related_domains}}
## Related Domains

{{#each related_domains}}
- [{{this.name}}]({{this.path}}) - {{this.relationship}}
{{/each}}
{{/if}}

{{#if observations}}
## Observations

{{#each observations}}
- {{this}}
{{/each}}
{{/if}}
