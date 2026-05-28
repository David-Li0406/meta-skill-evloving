---
name: css-development
description: Use this skill when working with CSS, creating components, styling elements, or reviewing CSS code. It routes to specialized workflows for creation, validation, or refactoring.
---

# CSS Development Skill

## Overview

Comprehensive workflow for CSS development using Tailwind and semantic component patterns. This skill automatically routes you to the appropriate specialized workflow based on context.

**Sub-skills invoked by this skill:**
- `css-development:create-component` - Creating new CSS components
- `css-development:validate` - Reviewing existing CSS
- `css-development:refactor` - Transforming CSS to semantic patterns

## When This Skill Applies

Use this skill when:
- Creating new CSS components or styles
- Reviewing or validating existing CSS code
- Refactoring inline styles or utility classes
- Working with component styling in any framework
- Adding dark mode support
- Writing CSS tests

## CSS Development Patterns

All sub-skills follow these core patterns. Reference this section when working with CSS.

### Core Principles

1. **Semantic Naming** - Use descriptive class names (e.g., `.button-primary`, `.card-header`) instead of utility names (e.g., `.btn-blue`, `.card-hdr`).
2. **Tailwind Composition** - Leverage Tailwind utilities via the `@apply` directive.
3. **Dark Mode by Default** - Include `dark:` variants for all colored/interactive elements.
4. **Composition Over Creation** - Reuse existing classes before creating new ones.
5. **Test Coverage** - Ensure static CSS tests and component rendering tests are in place.
6. **Documentation** - Include usage comments above each component class.

### Component Class Pattern

```css
/* Button component - Primary action button with hover states
   Usage: <button className="button-primary">Click me</button> */
.button-primary {
  @apply bg-indigo-500 hover:bg-indigo-700 dark:bg-indigo-600 dark:hover:bg-indigo-800;
  @apply px-6 py-3 rounded-lg font-medium text-white;
  @apply transition-all duration-200 hover:-translate-y-0.5;
}
```

### File Structure Convention

```
styles/
├── components.css      # All semantic component classes
└── __tests__/
    └── components.test.ts  # CSS and component tests
```

### Markup Integration (Framework-Agnostic)

Works with React, Vue, Svelte, or vanilla HTML:

**React:**
```tsx
const classes = `button-primary ${className}`.trim();
<button className={classes}>...</button>
```

**Vanilla HTML:**
```html
<button class="button-primary custom-class">...</button>
```

**Vue:**
```vue
<button :class="['button-primary', customClass]">...</button>
```

### Atomic Design Levels

- **Atoms:** Basic building blocks (e.g., `.button`, `.input`, `.badge`, `.spinner`)
- **Molecules:** Composed components (e.g., `.card`, `.form-field`, `.empty-state`)
- **Organisms:** Complex components (e.g., `.page-layout`, `.session-card`, `.conversation-timeline`)

### Testing Pattern

**Static CSS Tests:**
```typescript
it('should have button component classes', () => {
  const content = readFileSync('styles/components.css', 'utf-8');
  expect(content).toContain('.button-primary');
});
```

**Component Rendering Tests:**
```typescript
it('applies semantic class and custom className', () => {
  render(<Button variant="primary" className="custom" />);
  expect(screen.getByRole('button')).toHaveClass('button-primary', 'custom');
});
```

## Workflow: Context Detection and Routing

When this skill is invoked, follow these steps to route to the appropriate sub-skill:

### Step 1: Analyze Context

Look at the user's request and recent conversation to determine intent:

**Creating new components?**
- Keywords: "create", "add", "new component", "build a", "make a"
- Files: Mention of components.css or new component names
- Intent: User wants to add new CSS

**Validating existing CSS?**
- Keywords: "review", "validate", "check", "audit", "look at"
- Files: Reference to existing CSS files or components
- Intent: User wants feedback on existing CSS

**Refactoring CSS?**
- Keywords: "refactor", "clean up", "extract", "improve", "convert"
- Code: Inline styles or utility classes in markup visible
- Intent: User wants to transform existing CSS patterns

### Step 2: Choose Sub-Skill

Based on context analysis:

**If creating:** Use the Skill tool to invoke `css-development:create-component`

**If validating:** Use the Skill tool to invoke `css-development:validate`

**If refactoring:** Use the Skill tool to invoke `css-development:refactor`

**If ambiguous:** Ask the user using the AskUserQuestion tool:

```
Question: "What would you like to do with CSS?"
Options:
  - "Create new component" (Guide creating new semantic CSS component classes)
  - "Validate existing CSS" (Review CSS against established patterns)
  - "Refactor CSS" (Transform inline/utility styles to semantic components)
```

### Step 3: Invoke Sub-Skill

Use the Skill tool to invoke the chosen sub-skill:

**Example:**
```
I'm routing you to the create-component workflow.
[Invoke Skill tool with skill: "css-development:create-component"]
```

### Step 4: Hand Off Control

Once the sub-skill is invoked, it takes over. The main skill's job is complete.

## Important Notes

- **Don't skip routing:** Always analyze context and choose the right sub-skill.
- **Don't duplicate sub-skill logic:** Let sub-skills handle their workflows.
- **Reference pattern documentation:** Sub-skills will reference the patterns documented above.
- **User can invoke directly:** User can call sub-skills directly (e.g., "use css-development:validate").