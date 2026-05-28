# Angular-Nx Skill

This skill provides specialized knowledge for working with Angular 19 and Nx in the Sentinel monorepo.

## Structure

```
.agent/nx/
├── skill.md                              # Main skill file (entry point)
├── README.md                             # This file
├── examples/
│   ├── signal-forms.md                   # Signal Forms examples and patterns
│   └── component-generation.md           # Component generation examples
└── templates/
    └── (future component templates)
```

## How It Works

The main [skill.md](skill.md) file contains:
- Quick reference commands
- Key patterns and guidelines
- **Markdown links** to detailed examples

### Progressive Disclosure

Claude loads files **only when needed**:
1. Initially loads only `skill.md` (concise overview)
2. When Signal Forms are needed → loads `examples/signal-forms.md`
3. When generating components → loads `examples/component-generation.md`

This approach:
- Reduces initial token usage
- Provides context only when relevant
- Keeps the main skill file clean and readable

## Referencing Code Files

### In Skill Files

Use **Markdown link syntax** to reference files:

```markdown
# Link to example file (relative path)
See [signal-forms.md](examples/signal-forms.md)

# Link to actual codebase file
Reference: [login.component.ts](../../sentinel-frontend/libs/shared/login/src/lib/login/login.component.ts)
```

### In Example Files

Include code examples directly in fenced code blocks:

````markdown
## Example

```typescript
import { form, signal } from '@angular/forms/signals';

const formState = signal({ email: '' });
const myForm = form(formState);
```
````

Also link to actual implementation files for complete examples:

```markdown
See full implementation: [login.component.ts](../../../sentinel-frontend/libs/shared/login/src/lib/login/login.component.ts)
```

## Adding New Examples

1. Create a new file in `examples/`:
   ```bash
   touch .agent/nx/examples/my-example.md
   ```

2. Add content with code examples and links to real files

3. Link from `skill.md`:
   ```markdown
   For more details, see [my-example.md](examples/my-example.md).
   ```

## Best Practices

1. **Keep skill.md concise**: High-level overview only
2. **Detailed examples in examples/**: In-depth patterns and code
3. **Use Markdown links**: Enable progressive disclosure
4. **Link to real code**: Reference actual implementations in the codebase
5. **Organize by topic**: Separate concerns into different example files

## When Claude Invokes This Skill

This skill is automatically used when:
- Generating Angular components, services, or other artifacts
- Running tests or builds in the frontend
- Working with the Nx monorepo structure
- Questions about Angular 19 patterns or Signal Forms
