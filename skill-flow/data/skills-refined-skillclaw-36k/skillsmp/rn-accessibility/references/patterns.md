# Accessibility - Implementation Patterns

Implementation patterns for web accessibility.

## Pattern: Use Semantic HTML

Use appropriate HTML elements.

✅ **Good:**
\`\`\`typescript
<button onClick={handleClick}>Submit</button>
<a href="/about">About</a>
<nav>
  <ul>
    <li><a href="/">Home</a></li>
  </ul>
</nav>
\`\`\`

❌ **Bad:**
\`\`\`typescript
<div onClick={handleClick}>Submit</div>
<span onClick={goTo}>About</span>
<div>
  <div>
    <div onClick={goHome}>Home</div>
  </div>
</div>
\`\`\`

**Why:** Semantic HTML:
- Screen reader support
- Keyboard navigation
- SEO benefits
- Accessibility by default

## Pattern: Provide ARIA Labels

Add labels for interactive elements.

✅ **Good:**
\`\`\`typescript
<button aria-label="Close dialog" onClick={onClose}>
  ×
</button>

<input
  aria-label="Email address"
  aria-describedby="email-error"
/>
\`\`\`

❌ **Bad:**
\`\`\`typescript
<button onClick={onClose}>×</button>
<input />
\`\`\`

**Why:** ARIA labels:
- Screen reader context
- Clear purpose
- Better UX for assistive tech

## Pattern: Manage Focus

Control focus for modals and forms.

✅ **Good:**
\`\`\`typescript
const inputRef = useRef<HTMLInputElement>(null);

useEffect(() => {
  inputRef.current?.focus();
}, []);
\`\`\`

**Why:** Focus management:
- Keyboard navigation
- Better UX
- Accessibility compliance

## Pattern: Support Keyboard Navigation

Handle keyboard events.

✅ **Good:**
\`\`\`typescript
const handleKeyDown = (e: KeyboardEvent) => {
  if (e.key === 'Enter' || e.key === ' ') {
    handleClick();
  }
};

<div
  role="button"
  tabIndex={0}
  onKeyDown={handleKeyDown}
  onClick={handleClick}
>
  Click me
</div>
\`\`\`

❌ **Bad:**
\`\`\`typescript
<div onClick={handleClick}>
  Click me
</div>
\`\`\`

**Why:** Keyboard support:
- Accessibility requirement
- Power users
- No mouse users

## Summary

**Key Patterns:**
- Use semantic HTML
- Provide ARIA labels
- Manage focus
- Support keyboard navigation
- Use proper roles
- Test with screen readers

**Anti-Patterns:**
- Div soup
- Missing labels
- No keyboard support
- Poor focus management
