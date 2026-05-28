---
name: muebleria-mobile
description: >
  Mobile-responsive patterns for MuebleriaIris UI.
  Trigger: When working on mobile layouts, responsive design, or mobile-first components.
license: Apache-2.0
metadata:
  author: muebleria-iris
  version: "1.0"
  scope: [root]
  auto_invoke:
    - "Creating mobile layouts"
    - "Implementing responsive design"
    - "Working on mobile-first components"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## When to Use

Use this skill when:

- Creating mobile-specific layouts
- Implementing responsive design with Tailwind
- Optimizing for mobile performance
- Building mobile-first components
- Testing on different screen sizes

---

## Mobile-First Strategy

```
1. Design for mobile first (smallest screens)
2. Use Tailwind breakpoints to add desktop features
3. Test on actual devices
4. Optimize images and assets
5. Implement touch-friendly UI
```

---

## Critical Patterns

### Pattern 1: Tailwind Breakpoints

```tsx
// Mobile-first approach
<div className="
  w-full              {/* Mobile: full width */}
  p-4                 {/* Mobile: 16px padding */}
  sm:w-1/2            {/* Small: 50% width */}
  md:w-1/3            {/* Medium: 33% width */}
  lg:w-1/4            {/* Large: 25% width */}
  lg:p-8              {/* Large: 32px padding */}
">
  Content
</div>
```

**Breakpoints:**
- `sm:` 640px and up
- `md:` 768px and up
- `lg:` 1024px and up
- `xl:` 1280px and up
- `2xl:` 1536px and up

### Pattern 2: Component Structure

```
src/components/
├── mobile/
│   ├── MobileNav.tsx        # Mobile navigation
│   ├── MobileProductCard.tsx
│   └── MobileFilters.tsx
├── desktop/
│   ├── DesktopNav.tsx       # Desktop navigation
│   └── DesktopSidebar.tsx
└── ui/
    └── ProductCard.tsx       # Responsive component
```

### Pattern 3: Responsive Component

```tsx
// src/components/ui/ProductCard.tsx
export function ProductCard({ nombre, precio, imagen }: Props) {
  return (
    <div className="
      bg-white rounded-lg shadow-md
      p-3 sm:p-4 md:p-6                    {/* Responsive padding */}
      w-full sm:w-1/2 lg:w-1/3             {/* Responsive width */}
    ">
      <img 
        src={imagen} 
        alt={nombre}
        className="
          w-full h-32 sm:h-40 md:h-48      {/* Responsive height */}
          object-cover
        " 
      />
      <h3 className="
        text-base sm:text-lg md:text-xl    {/* Responsive text */}
        font-semibold mt-2
      ">
        {nombre}
      </h3>
      <p className="text-lg sm:text-xl text-green-600">
        ${precio}
      </p>
    </div>
  );
}
```

---

## Mobile Navigation Pattern

```tsx
// src/components/mobile/MobileNav.tsx
import { useState } from 'react';

export function MobileNav() {
  const [isOpen, setIsOpen] = useState(false);
  
  return (
    <>
      {/* Hamburger button (mobile only) */}
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="lg:hidden p-2"
      >
        <svg>...</svg>
      </button>
      
      {/* Drawer menu */}
      {isOpen && (
        <div className="
          fixed inset-0 z-50 bg-black bg-opacity-50
          lg:hidden
        ">
          <nav className="
            fixed right-0 top-0 h-full w-64
            bg-white shadow-lg
            transform transition-transform
          ">
            {/* Menu items */}
          </nav>
        </div>
      )}
      
      {/* Desktop nav (hidden on mobile) */}
      <nav className="hidden lg:flex gap-4">
        {/* Menu items */}
      </nav>
    </>
  );
}
```

---

## Touch-Friendly UI

```tsx
// Minimum touch target: 44x44px
<button className="
  min-h-[44px] min-w-[44px]     {/* Touch target */}
  p-3                            {/* Comfortable padding */}
  active:scale-95                {/* Touch feedback */}
  transition-transform
">
  Tap Me
</button>

// Spacing between interactive elements
<div className="space-y-4">      {/* 16px vertical space */}
  <button>Button 1</button>
  <button>Button 2</button>
</div>
```

---

## Performance Optimization

```astro
---
// src/pages/productos.astro

// Optimize images for mobile
import { Image } from 'astro:assets';
---

<Image
  src={producto.imagen}
  alt={producto.nombre}
  width={400}
  height={300}
  loading="lazy"                  {/* Lazy load images */}
  format="webp"                   {/* Modern format */}
/>
```

---

## Responsive Grid

```tsx
// Auto-responsive grid
<div className="
  grid
  grid-cols-1              {/* Mobile: 1 column */}
  sm:grid-cols-2           {/* Small: 2 columns */}
  md:grid-cols-3           {/* Medium: 3 columns */}
  lg:grid-cols-4           {/* Large: 4 columns */}
  gap-4
">
  {products.map(p => <ProductCard key={p.id} {...p} />)}
</div>
```

---

## Testing Mobile

```bash
# Chrome DevTools
1. Open DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Select device (iPhone, iPad, etc.)
4. Test touch interactions

# Real device testing
npm run dev -- --host
# Access from mobile: http://YOUR_IP:4321
```

---

## Common Patterns

### Show/Hide Based on Screen Size

```tsx
{/* Show only on mobile */}
<div className="block lg:hidden">
  <MobileSidebar />
</div>

{/* Show only on desktop */}
<div className="hidden lg:block">
  <DesktopSidebar />
</div>

{/* Different components for different sizes */}
<div className="block md:hidden">
  <MobileNav />
</div>
<div className="hidden md:block">
  <DesktopNav />
</div>
```

### Responsive Typography

```tsx
<h1 className="
  text-2xl sm:text-3xl md:text-4xl lg:text-5xl
  font-bold
">
  Heading
</h1>

<p className="
  text-sm sm:text-base md:text-lg
  leading-relaxed
">
  Body text
</p>
```

---

## QA Checklist

- [ ] Test on multiple screen sizes (320px, 768px, 1024px, 1920px)
- [ ] Touch targets minimum 44x44px
- [ ] Text is readable without zooming
- [ ] No horizontal scrolling
- [ ] Images load quickly (optimized)
- [ ] Forms are usable on mobile
- [ ] Navigation is accessible
- [ ] Test on actual mobile devices

---

## Resources

- **Tailwind Responsive**: https://tailwindcss.com/docs/responsive-design
- **Mobile Web Best Practices**: Web.dev mobile guide
