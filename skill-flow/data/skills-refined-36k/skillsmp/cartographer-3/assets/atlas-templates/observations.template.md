# {{project_name}} - Technology Observations

> Observed technologies and patterns in this codebase. Documents WHAT is used, not WHY it was chosen.

**Generated:** {{timestamp}}
**Note:** Decision rationale cannot be extracted from code. For architectural decisions, consult team documentation or ADRs if available.

---

{{#each observations}}
## {{this.category}}

**Observed:** {{this.technology}}

**Evidence:**
{{#each this.evidence}}
- {{this}}
{{/each}}

{{#if this.configuration}}
**Configuration:** `{{this.configuration}}`
{{/if}}

{{#if this.notable_patterns}}
**Notable Patterns:**
{{#each this.notable_patterns}}
- {{this}}
{{/each}}
{{/if}}

---

{{/each}}

## What This Document Does NOT Include

The following cannot be reliably extracted from code analysis:

- **Decision rationale** - Why this technology was chosen over alternatives
- **Trade-off analysis** - What was gained or sacrificed
- **Historical context** - What preceded current implementations
- **Future plans** - Intended migrations or deprecations

For this information, consult:
- Team documentation
- Architecture Decision Records (ADRs)
- Git commit history and PR discussions
- Team members with historical context
