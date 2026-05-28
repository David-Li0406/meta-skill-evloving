---
name: skill-creator
description: >
  Creates new AI agent skills for Angular following the Angular Agent Skills spec.
  Trigger: When user asks to create a new skill, add agent instructions, document Angular patterns for AI, or create skill documentation.
metadata:
  version: "1.0.0"
  author: 
    - name: Alan Buscaglia
      url: https://github.com/Gentleman-Programming

---

## When to Create a Skill

Create an Angular skill when:
- An Angular pattern is used repeatedly and AI needs guidance
- Angular version-specific conventions need documentation
- Complex Angular workflows need step-by-step instructions
- Migration paths between Angular versions require clarity
- Decision trees help AI choose between Angular patterns (e.g., Reactive vs Signal Forms)

**Don't create a skill when:**
- Official Angular documentation already covers it thoroughly (reference instead)
- Pattern is trivial or self-explanatory
- It's a one-off Angular task
- The pattern applies to only one Angular version without evolution

---

## Skill Structure

```
skills/
├── angular/
│   ├── core/
│   │   └── your-skill-name.md
│   ├── forms/
│   │   ├── reactive-forms/
│   │   │   └── SKILL.md
│   │   └── signal-forms/
│   │       └── SKILL.md
│   ├── router/
│   ├── http/
│   ├── performance/
│   ├── testing/
│   └── migrations/
│       ├── pattern-migrations/
│       │   └── feature-to-feature/
│       │       └── SKILL.md
│       └── version-upgrades/
│           └── v18-to-v19/
│               └── SKILL.md
├── ngrx/
├── rxjs/
└── skill-creator/
    └── SKILL.md
```

---

## SKILL.md Template for Angular

```markdown
---
name: your-skill-name
description: >
  Brief description of what this Angular skill covers.
  Trigger: When working with [Angular feature], when building [type of component/service], when using [Angular API].
metadata:
  version: "1.0.0"
  author:
    - name: Your Name
      url: https://your-website-or-github
  angular:
    minVersion: "15.0.0"
    maxVersion: "21.0.0"
    supportedVersions: ["15", "16", "17", "18", "19", "20", "21"]
---

## Version Support

**Minimum Angular Version:** 15.0.0  
**Maximum Angular Version:** 21.0.0  
**Supported Versions:** 15, 16, 17, 18, 19, 20, 21

## When to Use

Load this skill when:
- [Condition 1, e.g., "Working with Reactive Forms"]
- [Condition 2, e.g., "Implementing form validation"]
- [Condition 3, e.g., "Using FormBuilder or FormControl"]

## Critical Patterns

### Pattern 1: [Name]

**Supported in:** v15+

[Explanation of the pattern]

```typescript
// ✅ GOOD - Modern Angular pattern
import { Component } from '@angular/core';

@Component({
  selector: 'app-example',
  standalone: true,
  template: `...`
})
export class ExampleComponent {
  // Your code here
}
```

### Pattern 2: [Name]

**Supported in:** v17+

[Explanation of the pattern and what changed from previous versions]

```typescript
// ✅ GOOD - Angular v17+ with built-in control flow
import { Component } from '@angular/core';

@Component({
  selector: 'app-example',
  standalone: true,
  template: `
    @if (condition) {
      <div>Content</div>
    }
  `
})
export class ExampleComponent {
  condition = true;
}
```

## Real-World Examples

### Example 1: [Use Case]

**Context:** [When/where to use this]

```typescript
// Complete working example
import { Component, signal } from '@angular/core';

@Component({
  selector: 'app-example',
  standalone: true,
  template: `
    <div>{{ value() }}</div>
  `
})
export class ExampleComponent {
  value = signal(0);
}
```

### Example 2: [Use Case]

**Context:** [When/where to use this]

```typescript
// Another complete example
```

## Common Mistakes

### ❌ Don't: [Anti-pattern name]

**Why this is problematic:** [Explanation]

```typescript
// ❌ BAD - Don't do this
export class BadComponent {
  // What NOT to do
}
```

**✅ Instead, do this:**

```typescript
// ✅ GOOD - Correct approach
export class GoodComponent {
  // Correct implementation
}
```

## Quick Reference

| Task | Pattern | Version |
|------|---------|---------|
| [Task 1] | `code snippet` | v15+ |
| [Task 2] | `code snippet` | v17+ |
| [Task 3] | `code snippet` | v19+ |

## Resources

- [Official Angular Documentation](https://angular.dev)
- [Angular Update Guide](https://update.angular.io)
- [Relevant API Reference](https://angular.dev/api)
```

---

## Naming Conventions

| Type | Pattern | Examples |
|------|---------|----------|
| Core feature | `{feature-name}` | `signal-inputs`, `standalone-components`, `defer-loading` |
| Forms skill | `{form-type}` | `reactive-forms`, `signal-forms`, `template-driven-forms` |
| Router skill | `router-{feature}` | `router-guards`, `router-resolvers`, `lazy-loading` |
| Migration pattern | `{old}-to-{new}` | `ng-module-to-standalone`, `reactive-forms-to-signal-forms` |
| Version upgrade | `v{x}-to-v{y}` | `v18-to-v19`, `v19-to-v20` |
| Testing skill | `testing-{type}` | `testing-components`, `testing-services`, `testing-http` |

---

## Decision: Where to Place the Skill

```
Core Angular feature?           → skills/angular/core/
Forms-related?                  → skills/angular/forms/
Router-related?                 → skills/angular/router/
HTTP/API calls?                 → skills/angular/http/
Performance optimization?       → skills/angular/performance/
Testing patterns?               → skills/angular/testing/
Pattern migration?              → skills/angular/migrations/pattern-migrations/
Version upgrade?                → skills/angular/migrations/version-upgrades/
NgRx/state management?          → skills/ngrx/
RxJS patterns?                  → skills/rxjs/
```

---

## Decision: Single File vs Folder Structure

```
Simple skill (one concept)?                  → Single .md file
Complex skill (multiple sub-patterns)?       → Folder with SKILL.md + examples/
Migration guide (before/after)?              → Folder with SKILL.md + assets/
Needs templates or schemas?                  → Folder with assets/ subfolder
Multiple related examples?                   → Folder with examples/ subfolder
```

**Examples:**
- `skills/angular/core/signal-inputs.md` - Simple, single file
- `skills/angular/forms/reactive-forms/SKILL.md` - Complex, needs folder
- `skills/angular/migrations/v18-to-v19/SKILL.md` - Migration, needs assets

---

## Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Skill identifier (lowercase, hyphens) |
| `description` | Yes | What + Trigger in one block |
| `metadata.version` | Yes | Semantic version as string |
| `metadata.angular.minVersion` | Yes | Minimum Angular version (e.g., "15.0.0") |
| `metadata.angular.maxVersion` | Yes | Maximum tested Angular version |
| `metadata.angular.supportedVersions` | Yes | Array of supported major versions |

---

## Content Guidelines

### DO
- **Version Label Everything**: Mark each pattern with Angular version
- **Show Evolution**: When patterns changed between versions, show both
- **Complete Examples**: Include all imports, decorators, and types
- **Use Latest APIs**: Prefer standalone, signals, built-in control flow
- **Migration Paths**: Show how to migrate from old to new
- **TypeScript Strict**: All examples should compile with strict mode
- **Real-World Context**: Explain when and why to use each pattern

### DON'T
- Duplicate Angular documentation (reference instead)
- Mix patterns from different versions without labels
- Use deprecated APIs without migration notes
- Include incomplete code that won't compile
- Skip TypeScript types
- Use NgModule when standalone is available (v14+)
- Ignore Angular Style Guide conventions
- Add outdated patterns without historical context

---

## Version Support Guidelines

### Minimum Version Strategy

**Use v15 as minimum** for most skills because:
- Standalone APIs became stable in v15
- Still widely used in production
- Good baseline for modern Angular

**Use v16+** when skill requires:
- Signals (introduced in v16)
- Required inputs (v16+)
- Signal-based APIs

**Use v17+** when skill requires:
- Built-in control flow (@if, @for, @switch)
- @defer for lazy loading
- New application builder

### Version Labeling

Always label patterns with version introduced:

```typescript
// ✅ GOOD - Clear version label
### Pattern: Signal Inputs

**Supported in:** v17.1+

// ❌ BAD - No version context
### Pattern: Signal Inputs
```

---

## Migration Skills Best Practices

When creating migration guides:

1. **Show Before/After Side-by-Side**
```typescript
// ❌ BEFORE (v16)
export class OldComponent {
  @Input() value: string = '';
}

// ✅ AFTER (v17.1+)
export class NewComponent {
  value = input.required<string>();
}
```

2. **Provide Step-by-Step Instructions**
   - Step 1: Update Angular CLI
   - Step 2: Run schematic if available
   - Step 3: Manual changes needed
   - Step 4: Test and verify

3. **Note Breaking Changes**
   - What breaks in the migration
   - How to handle edge cases
   - Deprecation warnings

4. **CLI Support**
   - Mention if `ng update` handles it
   - Document manual steps
   - Link to official migration guide

---

## Registering the Skill

After creating the skill, add it to `AGENTS.md`:

```markdown
| `{skill-name}` | {Description} | [SKILL.md](skills/angular/{category}/{skill-name}/SKILL.md) | v15-v21 |
```

---

## Validation Checklist

Before creating a skill:

- [ ] Skill doesn't already exist (check `skills/`)
- [ ] Pattern is reusable (not one-off)
- [ ] Name follows conventions
- [ ] Frontmatter is complete with Angular version metadata
- [ ] Version Support section is clear
- [ ] Each pattern is labeled with version
- [ ] Critical patterns are clear
- [ ] At least 3 complete code examples
- [ ] Examples compile with TypeScript strict mode
- [ ] Common Mistakes section included
- [ ] Quick Reference table included
- [ ] Resources section with Angular.dev links
- [ ] Added to AGENTS.md

---

## Testing Your Skill

Before submitting:

1. **Create a test Angular project**
```bash
npx @angular/cli@latest new test-project
cd test-project
```

2. **Test each code example**
   - Copy code into project
   - Verify it compiles
   - Check runtime behavior
   - Test in supported Angular versions

3. **Use with an AI Agent**
   - Ask the agent to apply the skill
   - Verify it generates correct code
   - Check if examples are clear
   - Refine based on agent behavior

---

## Examples of Good Skills

### Example 1: Core Feature Skill

**File:** `skills/angular/core/signal-inputs.md`

- Clear version support (v17.1+)
- Shows required vs optional
- Migration from @Input()
- Complete, typed examples
- Common mistakes section

### Example 2: Migration Skill

**Folder:** `skills/angular/migrations/pattern-migrations/reactive-forms-to-signal-forms/`

- Before/after comparison
- Step-by-step migration
- Breaking changes noted
- CLI schematic info
- Real-world examples

### Example 3: Version Upgrade

**Folder:** `skills/angular/migrations/version-upgrades/v18-to-v19/`

- ng update command
- Breaking changes list
- New features overview
- Deprecation warnings
- Migration timeline

---

## Resources

- **Template**: See [template/SKILL_TEMPLATE.md](../../template/SKILL_TEMPLATE.md)
- **Angular Versions**: See [Angular Update Guide](https://update.angular.io)
- **Style Guide**: See [Angular Style Guide](https://angular.dev/style-guide)
- **Agent Skills Format**: See [agentskills.io](https://agentskills.io/)
