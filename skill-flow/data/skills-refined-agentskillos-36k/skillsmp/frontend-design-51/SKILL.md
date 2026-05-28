---
name: frontend-design
description: UI/UX design principles and patterns for building intuitive, accessible, and beautiful web interfaces
---

# Frontend Design Principles

This skill covers design principles and patterns for creating excellent user interfaces and experiences.

## Core Design Principles

### 1. Clarity

Make interfaces self-explanatory:
- **Clear labels**: Button says what it does
- **Obvious feedback**: User knows what happened
- **Consistent patterns**: Same action, same result
- **Simple language**: Avoid jargon

### 2. Consistency

Maintain predictable patterns:
- **Visual consistency**: Same things look the same
- **Functional consistency**: Same interactions work the same
- **Internal consistency**: Within your app
- **External consistency**: With platform conventions

### 3. Feedback

Always respond to user actions:
- **Immediate**: React within 100ms
- **Visual**: Show state changes
- **Appropriate**: Match action importance
- **Clear**: User understands what happened

### 4. Efficiency

Help users accomplish tasks quickly:
- **Shortcuts**: For frequent actions
- **Smart defaults**: Most common choice selected
- **Bulk actions**: Act on multiple items
- **Progressive disclosure**: Show advanced options when needed

## Layout Patterns

### Pattern 1: Container Sizing

```css
/* ✅ Do: Use max-width for readability */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* For text content, even narrower */
.prose {
  max-width: 65ch; /* ~65 characters per line */
  margin: 0 auto;
}
```

### Pattern 2: Spacing Scale

Use consistent spacing:

```css
/* Define spacing scale */
:root {
  --space-xs: 0.25rem;  /* 4px */
  --space-sm: 0.5rem;   /* 8px */
  --space-md: 1rem;     /* 16px */
  --space-lg: 1.5rem;   /* 24px */
  --space-xl: 2rem;     /* 32px */
  --space-2xl: 3rem;    /* 48px */
  --space-3xl: 4rem;    /* 64px */
}

/* Use consistently */
.card {
  padding: var(--space-md);
  margin-bottom: var(--space-lg);
}
```

### Pattern 3: Responsive Grid

```css
/* Flexible grid */
.grid {
  display: grid;
  gap: var(--space-lg);
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}
```

### Pattern 4: Visual Hierarchy

```typescript
// Clear hierarchy in components
export function Article({ article }: { article: Article }) {
  return (
    <article>
      {/* Primary: Article title */}
      <h1 className="text-3xl font-bold">{article.title}</h1>
      
      {/* Secondary: Metadata */}
      <div className="text-sm text-gray-600">
        By {article.author} · {article.date}
      </div>
      
      {/* Tertiary: Content */}
      <div className="text-base">{article.content}</div>
    </article>
  );
}
```

## Color System

### Pattern 1: Semantic Colors

```css
:root {
  /* Brand colors */
  --color-primary: #3b82f6;
  --color-primary-dark: #2563eb;
  
  /* Semantic colors */
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  --color-info: #3b82f6;
  
  /* Neutrals */
  --color-gray-50: #f9fafb;
  --color-gray-100: #f3f4f6;
  --color-gray-500: #6b7280;
  --color-gray-900: #111827;
}
```

### Pattern 2: Color Contrast

Ensure accessibility:

```typescript
// Check contrast ratios
// Text: 4.5:1 minimum
// Large text: 3:1 minimum
// UI components: 3:1 minimum

// ✅ Good contrast
<div className="bg-blue-600 text-white">
  {/* White on blue-600 has 4.5:1 ratio */}
</div>

// ❌ Poor contrast
<div className="bg-gray-200 text-gray-300">
  {/* Barely readable */}
</div>
```

### Pattern 3: Dark Mode

```css
/* Light mode (default) */
:root {
  --color-background: #ffffff;
  --color-text: #111827;
  --color-border: #e5e7eb;
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  :root {
    --color-background: #111827;
    --color-text: #f9fafb;
    --color-border: #374151;
  }
}

/* Usage */
body {
  background: var(--color-background);
  color: var(--color-text);
}
```

## Typography

### Pattern 1: Type Scale

```css
:root {
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.25rem;    /* 20px */
  --text-2xl: 1.5rem;    /* 24px */
  --text-3xl: 1.875rem;  /* 30px */
  --text-4xl: 2.25rem;   /* 36px */
}
```

### Pattern 2: Line Height

```css
/* Tighter for headings */
h1, h2, h3 {
  line-height: 1.2;
}

/* Comfortable for body text */
p {
  line-height: 1.6;
}

/* Spacious for UI text */
button {
  line-height: 1.5;
}
```

### Pattern 3: Font Loading

```typescript
// Use system fonts for speed
const systemFonts = `-apple-system, BlinkMacSystemFont, "Segoe UI", 
  Roboto, "Helvetica Neue", Arial, sans-serif`;

// Or load custom fonts optimally
export default function RootLayout() {
  return (
    <html>
      <head>
        <link
          rel="preload"
          href="/fonts/inter.woff2"
          as="font"
          type="font/woff2"
          crossOrigin="anonymous"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

## Interactive Elements

### Pattern 1: Button States

```typescript
export function Button({ children, ...props }: ButtonProps) {
  return (
    <button
      className="
        px-4 py-2 rounded
        bg-blue-600 text-white
        hover:bg-blue-700
        active:bg-blue-800
        disabled:bg-gray-300 disabled:cursor-not-allowed
        focus:outline-none focus:ring-2 focus:ring-blue-500
        transition-colors duration-150
      "
      {...props}
    >
      {children}
    </button>
  );
}
```

**All buttons should have:**
- Default state (resting)
- Hover state (mouse over)
- Active state (being clicked)
- Focus state (keyboard navigation)
- Disabled state (when not available)

### Pattern 2: Loading States

```typescript
export function SubmitButton({ isLoading }: { isLoading: boolean }) {
  return (
    <button disabled={isLoading}>
      {isLoading ? (
        <>
          <Spinner className="mr-2" />
          Submitting...
        </>
      ) : (
        "Submit"
      )}
    </button>
  );
}
```

### Pattern 3: Form Validation

```typescript
export function Input({
  error,
  label,
  ...props
}: InputProps) {
  return (
    <div>
      <label className="block mb-1 font-medium">
        {label}
      </label>
      <input
        className={`
          border rounded px-3 py-2 w-full
          ${error ? 'border-red-500' : 'border-gray-300'}
          focus:outline-none focus:ring-2
          ${error ? 'focus:ring-red-500' : 'focus:ring-blue-500'}
        `}
        aria-invalid={error ? 'true' : 'false'}
        aria-describedby={error ? `${props.id}-error` : undefined}
        {...props}
      />
      {error && (
        <p id={`${props.id}-error`} className="text-red-500 text-sm mt-1">
          {error}
        </p>
      )}
    </div>
  );
}
```

## Accessibility (a11y)

### Pattern 1: Semantic HTML

```typescript
// ✅ Do: Use semantic elements
<header>
  <nav>
    <ul>
      <li><a href="/home">Home</a></li>
    </ul>
  </nav>
</header>
<main>
  <article>
    <h1>Title</h1>
    <p>Content</p>
  </article>
</main>
<footer>
  <p>© 2025</p>
</footer>

// ❌ Don't: Use divs for everything
<div className="header">
  <div className="nav">
    <div className="link">Home</div>
  </div>
</div>
```

### Pattern 2: ARIA Labels

```typescript
// Icon-only button needs label
<button aria-label="Close dialog">
  <XIcon />
</button>

// Image needs alt text
<img src="profile.jpg" alt="User profile picture" />

// Loading state announcement
<div role="status" aria-live="polite">
  {isLoading && "Loading..."}
</div>
```

### Pattern 3: Keyboard Navigation

```typescript
export function Dialog({ isOpen, onClose }: DialogProps) {
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    
    if (isOpen) {
      document.addEventListener("keydown", handleEscape);
      // Trap focus in dialog
      trapFocus();
    }
    
    return () => {
      document.removeEventListener("keydown", handleEscape);
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div role="dialog" aria-modal="true">
      {/* Dialog content */}
    </div>
  );
}
```

### Pattern 4: Focus Management

```typescript
// Move focus to first input when dialog opens
useEffect(() => {
  if (isOpen) {
    const firstInput = dialogRef.current?.querySelector('input');
    firstInput?.focus();
  }
}, [isOpen]);

// Restore focus when dialog closes
useEffect(() => {
  const previouslyFocused = document.activeElement;
  
  return () => {
    if (previouslyFocused instanceof HTMLElement) {
      previouslyFocused.focus();
    }
  };
}, []);
```

## Responsive Design

### Pattern 1: Mobile First

```css
/* Base styles (mobile) */
.card {
  padding: 1rem;
  font-size: 1rem;
}

/* Tablet and up */
@media (min-width: 768px) {
  .card {
    padding: 1.5rem;
    font-size: 1.125rem;
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .card {
    padding: 2rem;
    font-size: 1.25rem;
  }
}
```

### Pattern 2: Responsive Images

```typescript
<img
  src="/image.jpg"
  srcSet="/image-300.jpg 300w,
          /image-600.jpg 600w,
          /image-1200.jpg 1200w"
  sizes="(max-width: 768px) 100vw,
         (max-width: 1200px) 50vw,
         33vw"
  alt="Description"
/>
```

### Pattern 3: Touch Targets

```css
/* Minimum 44x44px for touch targets */
button {
  min-width: 44px;
  min-height: 44px;
  padding: 0.5rem 1rem;
}

/* Spacing between touch targets */
.button-group button {
  margin: 0.5rem;
}
```

## Animation and Transitions

### Pattern 1: Subtle Transitions

```css
/* Smooth state changes */
button {
  transition: background-color 150ms ease-in-out;
}

/* Respect user preferences */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Pattern 2: Loading Skeletons

```typescript
export function PostSkeleton() {
  return (
    <div className="animate-pulse">
      <div className="h-6 bg-gray-200 rounded w-3/4 mb-2"></div>
      <div className="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
      <div className="h-4 bg-gray-200 rounded mb-2"></div>
      <div className="h-4 bg-gray-200 rounded mb-2"></div>
    </div>
  );
}

// Usage
{isLoading ? <PostSkeleton /> : <Post data={post} />}
```

### Pattern 3: Page Transitions

```typescript
// Simple fade transition
export function FadeTransition({ children }: { children: ReactNode }) {
  return (
    <div className="
      animate-in fade-in
      duration-200
    ">
      {children}
    </div>
  );
}
```

## Error States

### Pattern 1: Inline Errors

```typescript
export function FormField({ error, ...props }: FormFieldProps) {
  return (
    <div>
      <input
        {...props}
        className={error ? 'border-red-500' : 'border-gray-300'}
      />
      {error && (
        <p className="text-red-500 text-sm mt-1 flex items-center gap-1">
          <AlertIcon className="w-4 h-4" />
          {error}
        </p>
      )}
    </div>
  );
}
```

### Pattern 2: Empty States

```typescript
export function PostList({ posts }: { posts: Post[] }) {
  if (posts.length === 0) {
    return (
      <div className="text-center py-12">
        <InboxIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium mb-2">No posts yet</h3>
        <p className="text-gray-600 mb-4">
          Get started by creating your first post.
        </p>
        <button>Create Post</button>
      </div>
    );
  }

  return (
    <ul>
      {posts.map(post => <PostItem key={post.id} post={post} />)}
    </ul>
  );
}
```

### Pattern 3: Error Boundaries

```typescript
export function ErrorFallback({ error }: { error: Error }) {
  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <h2 className="text-red-800 font-bold text-lg mb-2">
            Something went wrong
          </h2>
          <p className="text-red-700 mb-4">
            {error.message}
          </p>
          <button
            onClick={() => window.location.reload()}
            className="bg-red-600 text-white px-4 py-2 rounded"
          >
            Reload page
          </button>
        </div>
      </div>
    </div>
  );
}
```

## Design Checklist

### Visual Design
- [ ] Consistent spacing scale
- [ ] Clear visual hierarchy
- [ ] Appropriate color contrast
- [ ] Readable typography
- [ ] Cohesive color palette

### Interaction Design
- [ ] All buttons have states (hover, active, focus, disabled)
- [ ] Loading states for async actions
- [ ] Error states for failures
- [ ] Success feedback for completions
- [ ] Undo for destructive actions

### Accessibility
- [ ] Semantic HTML elements
- [ ] ARIA labels where needed
- [ ] Keyboard navigation works
- [ ] Focus indicators visible
- [ ] Alt text for images
- [ ] Color not sole indicator

### Responsive
- [ ] Mobile-first approach
- [ ] Touch targets 44x44px minimum
- [ ] Readable on small screens
- [ ] No horizontal scrolling
- [ ] Images responsive

### Performance
- [ ] Smooth animations (60fps)
- [ ] No layout shifts
- [ ] Fast page loads
- [ ] Optimized images
- [ ] Reduced motion support

## Common Mistakes to Avoid

❌ **Don't:**
- Use color alone to convey information
- Make clickable elements too small
- Forget keyboard navigation
- Use low-contrast text
- Hide important actions
- Surprise users with unexpected behavior
- Ignore loading states
- Leave errors unexplained

✅ **Do:**
- Provide multiple information cues
- Make touch targets 44x44px minimum
- Support Tab navigation
- Ensure 4.5:1 contrast ratio
- Make primary actions obvious
- Meet user expectations
- Show loading indicators
- Explain errors with solutions

## Design Tools and Resources

**Colors:**
- Tailwind Colors: https://tailwindcss.com/docs/customizing-colors
- Color Contrast Checker: https://webaim.org/resources/contrastchecker/

**Typography:**
- Type Scale Generator: https://type-scale.com/
- Font Pairing: https://fontpair.co/

**Accessibility:**
- ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/
- WebAIM: https://webaim.org/

**Icons:**
- Lucide Icons: https://lucide.dev/
- Heroicons: https://heroicons.com/

**Design Systems:**
- shadcn/ui: https://ui.shadcn.com/
- Radix UI: https://www.radix-ui.com/
- Headless UI: https://headlessui.com/

## Further Reading

- Refactoring UI: https://www.refactoringui.com/
- Laws of UX: https://lawsofux.com/
- Inclusive Components: https://inclusive-components.design/
- Web Content Accessibility Guidelines: https://www.w3.org/WAI/WCAG21/quickref/
