---
name: migrate-component
description: 'Migrate a component from raw HTML to design system components'
targets: ["*"]
claudecode:
  allowed-tools:
    - "Bash"
    - "Read"
    - "Write"
    - "Glob"
    - "Grep"
---

# Migrate Component Skill

This skill migrates components from raw HTML to design system components.

## Usage

Invoke when:
- A component uses raw HTML elements (div, button, span, etc.)
- A component needs to adopt design system patterns
- Lint errors flag `prefer-design-system` violations

## Process

### Step 1: Analyze Current Component

Read the component and identify:
- Raw HTML elements used
- Current styling approach (CSS, Tailwind, inline)
- Component structure and logic
- Props and state

### Step 2: Map to Design System

| Raw HTML | Design System Replacement |
|----------|--------------------------|
| `<div>` | `Box`, `VStack`, `HStack`, `Stack` |
| `<button>` | `Button`, `IconButton` |
| `<input>` | `Input`, `TextArea` |
| `<form>` | `Form`, `FormField` |
| `<span>`, `<p>` | `Text` |
| `<h1>`-`<h6>` | `Heading` |
| `<ul>`, `<ol>` | `List`, `ListItem` |
| `<a>` | `Link`, `ButtonLink` |
| `<img>` | `Image`, `Avatar` |
| Flex container | `HStack`, `VStack`, `Stack` |
| Grid container | `Grid`, `GridItem` |

### Step 3: Preserve Functionality

Ensure:
- All event handlers remain connected
- Accessibility attributes are maintained or improved
- Styling intent is preserved with tokens
- Loading/error/empty states are handled

### Step 4: Migrate Step by Step

1. Import design system components
2. Replace elements from innermost to outermost
3. Convert inline styles to design tokens
4. Add missing accessibility attributes
5. Test functionality after each change

### Step 5: Update Tests

- Verify component still renders
- Check accessibility
- Test interactions
- Verify state handling

## Example Migration

### Before (Raw HTML)

```tsx
const UserCard = ({ user, onEdit }) => (
  <div className="flex items-center p-4 border rounded-lg">
    <img
      src={user.avatar}
      className="w-12 h-12 rounded-full"
      alt={user.name}
    />
    <div className="ml-4 flex-1">
      <h3 className="font-semibold">{user.name}</h3>
      <span className="text-gray-500">{user.email}</span>
    </div>
    <button
      onClick={onEdit}
      className="px-4 py-2 bg-blue-500 text-white rounded"
    >
      Edit
    </button>
  </div>
);
```

### After (Design System)

```tsx
import { HStack, VStack, Box } from '@contractspec/lib.design-system';
import { Avatar, Text, Heading, Button } from '@contractspec/lib.ui-kit-web';

const UserCard = ({ user, onEdit }) => (
  <HStack
    padding="md"
    borderWidth="1px"
    borderRadius="lg"
    alignItems="center"
    gap="md"
  >
    <Avatar
      src={user.avatar}
      name={user.name}
      size="lg"
    />
    <VStack flex={1} alignItems="flex-start" gap="xs">
      <Heading size="sm">{user.name}</Heading>
      <Text color="muted">{user.email}</Text>
    </VStack>
    <Button onClick={onEdit} variant="primary">
      Edit
    </Button>
  </HStack>
);
```

### Key Changes Made

1. `<div className="flex">` → `<HStack>` (semantic flex container)
2. `<img>` → `<Avatar>` (handles fallback, accessibility)
3. `<h3>` → `<Heading>` (semantic, styled)
4. `<span>` → `<Text>` (typography tokens)
5. `<button>` → `<Button>` (accessibility, variants)
6. Tailwind classes → Design tokens (padding, gap, etc.)

## Verification Checklist

- [ ] No raw HTML elements remain
- [ ] Component renders correctly
- [ ] Accessibility is maintained/improved
- [ ] Interactions work as before
- [ ] Loading/error states handled
- [ ] Tests pass
- [ ] Lint passes (no prefer-design-system errors)

## Output

After migration, report:
- Elements migrated
- Design system components used
- Any compromises or notes
- Test status