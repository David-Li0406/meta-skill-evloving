---
name: compound-components
description: Use this skill when building UI components with the compound component pattern in React, especially when creating new components, refactoring, or discussing composable UI elements.
---

# Compound Components Pattern

This is the **REQUIRED** pattern for ALL UI components. Always use compound components by default.

## What are Compound Components?

Compound components are small, single-purpose components that compose together. Each component wraps exactly ONE HTML element and has ONE responsibility. They are combined like building blocks.

For more information, see the [components.build docs](https://www.components.build/llms.txt).

## Core Rules

1. **Each component = one element** - A component wraps exactly one HTML element.
2. **Use `children` for content** - Never use props like `title`, `description`, `label` - pass content as children.
3. **Use `className` for customization** - Allow consumers to override styles.
4. **Use `data-slot` for CSS coordination** - Style child components based on parent context using `data-slot` attributes and Tailwind's `has-*` or `group-*` selectors.
5. **Make components generic** - Name components for what they ARE, not what they're FOR. A component used for multiple domains should have a generic name like `MediaCard`, not `CourseHeader`.

## Context/Provider - LAST RESORT

**Do NOT use React Context by default.** Most compound components don't need it. Context is only for:

- Shared state that MULTIPLE children need to read/write (like form state, open/close state).
- When props would need to pass through 3+ levels.

If you find yourself reaching for Context, first ask: "Can I solve this with just composition and CSS?" Usually, the answer is yes.

## Example: The Right Way

```tsx
// Each component wraps ONE element, uses children, no context needed
<MediaCard>
  <MediaCardTrigger>
    <MediaCardImage>
      <Image src={...} />
    </MediaCardImage>
    <MediaCardContent>
      <MediaCardTitle>{title}</MediaCardTitle>
      <MediaCardDescription>{description}</MediaCardDescription>
    </MediaCardContent>
    <MediaCardIndicator />
  </MediaCardTrigger>
  <MediaCardPopover>
    <MediaCardPopoverText>{fullDescription}</MediaCardPopoverText>
    <MediaCardPopoverMeta>
      <MediaCardPopoverSource>{source}</MediaCardPopoverSource>
    </MediaCardPopoverMeta>
  </MediaCardPopover>
</MediaCard>
```