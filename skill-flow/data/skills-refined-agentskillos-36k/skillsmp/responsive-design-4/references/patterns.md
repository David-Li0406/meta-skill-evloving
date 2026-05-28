# Responsive Design - Implementation Patterns

Implementation patterns for responsive web design.

## Pattern: Mobile-First Approach

Start with mobile styles, add desktop later.

✅ **Good:**
\`\`\`css
.container {
  width: 100%; /* Mobile first */
}

@media (min-width: 768px) {
  .container {
    width: 750px; /* Tablet */
  }
}
\`\`\`

❌ **Bad:**
\`\`\`css
.container {
  width: 1200px; /* Desktop first */
}

@media (max-width: 768px) {
  .container {
    width: 100%; /* Override for mobile */
  }
}
\`\`\`

**Why:** Mobile-first:
- Simpler code
- Better performance
- Progressive enhancement

## Pattern: Use Responsive Arrays

Use Zest responsive arrays.

✅ **Good:**
\`\`\`typescript
<Box
  width={['100%', '50%', '33.33%']}
  padding={['sm-1', 'md-1', 'lg-1']}
  flexDirection={['column', 'row']}
/>
\`\`\`

❌ **Bad:**
\`\`\`typescript
const isMobile = width < 768;
<Box
  width={isMobile ? '100%' : '50%'}
  padding={isMobile ? 'sm-1' : 'lg-1'}
/>
\`\`\`

**Why:** Arrays:
- Declarative
- Theme-based breakpoints
- Cleaner code

## Pattern: Use Window Size Hook

Track window dimensions.

✅ **Good:**
\`\`\`typescript
const { width } = useWindowSize();
const isMobile = width < 768;
\`\`\`

**Why:** Hook:
- Reactive to changes
- Reusable
- Clean implementation

## Summary

**Key Patterns:**
- Mobile-first approach
- Use responsive arrays
- Window size hook
- Relative units
- Test multiple sizes

**Anti-Patterns:**
- Desktop-first
- Hardcoded breakpoints
- No responsive testing
