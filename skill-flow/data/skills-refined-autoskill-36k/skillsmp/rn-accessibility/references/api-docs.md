# Accessibility - API Reference

API reference for web accessibility patterns.

## ARIA Attributes

### Common ARIA Labels

\`\`\`typescript
<button aria-label="Close dialog">×</button>
<img src="logo.png" alt="Company logo" />
<input aria-label="Email address" />
<div role="alert" aria-live="polite">Success!</div>
\`\`\`

### ARIA Roles

\`\`\`typescript
<nav role="navigation">
<main role="main">
<aside role="complementary">
<button role="button">
<div role="dialog" aria-modal="true">
\`\`\`

### ARIA States

\`\`\`typescript
<button aria-pressed="true">
<input aria-invalid="true" aria-describedby="error">
<div aria-expanded="false">
<button aria-disabled="true">
\`\`\`

## Semantic HTML

\`\`\`html
<header>
<nav>
<main>
<article>
<section>
<aside>
<footer>
\`\`\`

## Keyboard Navigation

\`\`\`typescript
const handleKeyDown = (e: KeyboardEvent) => {
  if (e.key === 'Enter' || e.key === ' ') {
    handleClick();
  }
  if (e.key === 'Escape') {
    handleClose();
  }
};
\`\`\`

## Focus Management

\`\`\`typescript
const inputRef = useRef<HTMLInputElement>(null);

useEffect(() => {
  inputRef.current?.focus();
}, []);

<input ref={inputRef} />
\`\`\`

## Best Practices

1. Use semantic HTML
2. Provide alt text for images
3. Ensure keyboard navigation
4. Maintain focus management
5. Use ARIA when semantic HTML insufficient
6. Test with screen readers
