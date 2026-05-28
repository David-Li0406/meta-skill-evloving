# TODO Issue Template

Use this template for quick, standalone tasks.

## Template

```markdown
**Title:** {Action verb} {component} - {description}
**Labels:** task
**Priority:** {Based on urgency}

## Action
{What needs to be done}

## Context (Auto-gathered)
**Files to modify:**
- `{path/to/file.ts}` - {what changes needed}

**Existing patterns:**
{How similar things are done in the codebase}

**Related code:**
```{language}
{Relevant snippet}
```

## Verification
```bash
{Test command}
```
```

## Example

**User says:** "We need to add a loading spinner to the submit button"

**Created issue:**
```markdown
**Title:** Add loading state to SubmitButton component
**Labels:** task
**Priority:** Medium

## Action
Add loading spinner while form submission is in progress.

## Context (Auto-gathered)
**Files to modify:**
- `src/components/forms/SubmitButton.tsx` - Add isLoading prop and spinner

**Existing patterns:**
Other components use `<Spinner />` from `src/components/ui/Spinner.tsx`

**Related code:**
```tsx
// src/components/forms/SubmitButton.tsx
export function SubmitButton({ children, ...props }) {
  return <button type="submit" {...props}>{children}</button>
}
```

## Verification
```bash
npm test -- SubmitButton.test.tsx
```
```
