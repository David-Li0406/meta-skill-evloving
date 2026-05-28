# Tailwind Workflows Reference

## Contents
- Adding New Components
- Modifying the Design System
- Creating Responsive Layouts
- Adding Custom Animations
- Form Styling Workflow

---

## Adding New Components

### Workflow: Creating a New Page

Copy this checklist and track progress:
- [ ] Step 1: Create page file at `app/[route]/page.tsx`
- [ ] Step 2: Add `'use client'` directive if page has interactivity
- [ ] Step 3: Import Navigation and Footer components
- [ ] Step 4: Apply standard page container structure
- [ ] Step 5: Verify dark theme consistency

```tsx
'use client'

import Navigation from '@/app/components/Navigation'
import Footer from '@/app/components/Footer'

export default function NewPage() {
  return (
    <div className="min-h-screen bg-black text-white">
      <Navigation />
      
      <section className="px-6 py-16">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-4xl md:text-6xl font-bold text-center mb-6">
            Page Title
          </h1>
          <p className="text-xl text-gray-300 text-center mb-12 max-w-3xl mx-auto">
            Page description
          </p>
          
          {/* Page content */}
        </div>
      </section>
      
      <Footer />
    </div>
  )
}
```

### Workflow: Creating a Card Grid

Copy this checklist and track progress:
- [ ] Step 1: Define data array with card content
- [ ] Step 2: Create responsive grid container
- [ ] Step 3: Map items to card components
- [ ] Step 4: Add animation delays for stagger effect
- [ ] Step 5: Test responsive breakpoints

```tsx
const items = [
  { title: 'Item 1', description: 'Description 1' },
  { title: 'Item 2', description: 'Description 2' },
  // ...
]

// Render
<div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
  {items.map((item, index) => (
    <div
      key={index}
      className="bg-gray-900 border border-gray-800 rounded-lg p-6 animate-fadeIn"
      style={{ animationDelay: `${(index + 1) * 0.1}s` }}
    >
      <h3 className="text-xl font-semibold mb-3 group-hover:text-green-400 transition-colors">
        {item.title}
      </h3>
      <p className="text-gray-400">{item.description}</p>
    </div>
  ))}
</div>
```

---

## Modifying the Design System

### Workflow: Adding a New Color

1. Add to `tailwind.config.js` if it's a custom color:

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          green: '#8BC34A',
        }
      }
    }
  }
}
```

2. Validate by running build:
```bash
npm run build
```

3. If build fails, check for syntax errors in config
4. Only proceed when build passes

### Workflow: Extending Animations

Add custom keyframes and classes to `app/globals.css`:

```css
/* 1. Define keyframes */
@keyframes newAnimation {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 2. Create utility class */
.animate-newAnimation {
  animation: newAnimation 0.6s ease-out forwards;
}
```

---

## Creating Responsive Layouts

### Workflow: Mobile-First Development

Copy this checklist and track progress:
- [ ] Step 1: Build mobile layout first (no breakpoint prefixes)
- [ ] Step 2: Add `md:` prefix for tablet adjustments
- [ ] Step 3: Add `lg:` prefix for desktop adjustments
- [ ] Step 4: Test at each breakpoint using browser devtools
- [ ] Step 5: Verify touch targets are at least 44x44px on mobile

```tsx
// Mobile-first responsive example
<div className="
  flex flex-col          /* Mobile: stack vertically */
  md:flex-row            /* Tablet+: horizontal */
  gap-4 
  md:gap-8              /* Larger gap on tablet+ */
">
  <div className="
    w-full               /* Mobile: full width */
    md:w-1/2             /* Tablet+: half width */
  ">
    Content A
  </div>
  <div className="w-full md:w-1/2">
    Content B
  </div>
</div>
```

### Responsive Text Sizing

```tsx
// Hero text pattern
<h1 className="
  text-3xl              /* Mobile */
  sm:text-4xl           /* Small tablet */
  md:text-5xl           /* Tablet */
  lg:text-6xl           /* Desktop */
  font-bold
">

// Body text pattern
<p className="
  text-base             /* Mobile */
  md:text-lg            /* Tablet+ */
  lg:text-xl            /* Desktop */
  text-gray-300
">
```

---

## Adding Custom Animations

### Workflow: New Animation Class

1. Define keyframes in `app/globals.css`:

```css
@keyframes bounce-subtle {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-5px);
  }
}

.animate-bounce-subtle {
  animation: bounce-subtle 2s ease-in-out infinite;
}
```

2. Apply in component:

```tsx
<div className="animate-bounce-subtle">
  Bouncing content
</div>
```

### Workflow: Conditional Animation

```tsx
const [isVisible, setIsVisible] = useState(false)

// Use Intersection Observer or scroll trigger
useEffect(() => {
  // Set isVisible when element enters viewport
}, [])

return (
  <div className={`
    transition-all duration-500
    ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}
  `}>
    Content appears on scroll
  </div>
)
```

---

## Form Styling Workflow

### Workflow: Complete Form Implementation

Copy this checklist and track progress:
- [ ] Step 1: Create form container with `bg-gray-900 rounded-lg p-8`
- [ ] Step 2: Add input fields with consistent styling
- [ ] Step 3: Add focus states (`focus:border-green-500 focus:ring-1`)
- [ ] Step 4: Add error state container
- [ ] Step 5: Add success state container
- [ ] Step 6: Style submit button with loading state

```tsx
<div className="bg-gray-900 rounded-lg p-8">
  <form onSubmit={handleSubmit} className="space-y-6">
    {/* Text input */}
    <div>
      <label className="block text-sm font-medium mb-2">
        Field Label
      </label>
      <input
        type="text"
        className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg 
          focus:border-green-500 focus:ring-1 focus:ring-green-500 transition-colors"
      />
    </div>
    
    {/* Textarea */}
    <div>
      <label className="block text-sm font-medium mb-2">
        Message
      </label>
      <textarea
        rows={6}
        className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg 
          focus:border-green-500 focus:ring-1 focus:ring-green-500 transition-colors resize-none"
      />
    </div>
    
    {/* Error state */}
    {error && (
      <div className="bg-red-900/20 border border-red-500/30 rounded-lg p-4 text-red-300">
        {error}
      </div>
    )}
    
    {/* Success state */}
    {success && (
      <div className="bg-green-900/20 border border-green-500/30 rounded-lg p-4 text-green-300">
        Form submitted successfully!
      </div>
    )}
    
    {/* Submit button */}
    <button
      type="submit"
      disabled={isSubmitting}
      className="w-full bg-gradient-to-r from-purple-600 to-pink-600 
        hover:from-purple-500 hover:to-pink-500 
        disabled:opacity-50 disabled:cursor-not-allowed 
        px-6 py-4 rounded-full font-semibold transition-colors 
        flex items-center justify-center gap-2"
    >
      {isSubmitting ? (
        <>
          <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
          Sending...
        </>
      ) : (
        'Submit'
      )}
    </button>
  </form>
</div>
```

---

## Validation Workflow

### Iterate-Until-Pass: Build Validation

1. Make Tailwind changes
2. Validate: `npm run build`
3. If build fails:
   - Check for typos in class names
   - Verify `tailwind.config.js` syntax
   - Check `globals.css` for CSS errors
4. Repeat steps 2-3 until build passes
5. Verify visual output in browser

### Iterate-Until-Pass: Responsive Testing

1. Make responsive changes
2. Open browser devtools (F12)
3. Toggle device toolbar (Ctrl+Shift+M)
4. Test at breakpoints: 320px, 768px, 1024px, 1280px
5. If layout breaks:
   - Check breakpoint prefix order (mobile-first)
   - Verify flex/grid containers
   - Check for fixed widths that overflow
6. Repeat until all breakpoints work correctly