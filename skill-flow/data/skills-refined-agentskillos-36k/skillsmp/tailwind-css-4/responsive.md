# Responsive Design Patterns

## Breakpoints

Tailwind v4 default breakpoints:

| Breakpoint | Min Width | CSS |
|------------|-----------|-----|
| `sm` | 640px | `@media (min-width: 640px)` |
| `md` | 768px | `@media (min-width: 768px)` |
| `lg` | 1024px | `@media (min-width: 1024px)` |
| `xl` | 1280px | `@media (min-width: 1280px)` |
| `2xl` | 1536px | `@media (min-width: 1536px)` |

### Custom Breakpoints

```css
@theme {
  --breakpoint-xs: 475px;
  --breakpoint-3xl: 1920px;
  --breakpoint-4xl: 2560px;
}
```

## Mobile-First Approach

Always start with mobile styles, then add larger breakpoints:

```tsx
<div className="
  p-4        /* Mobile (default) */
  sm:p-6     /* Small screens (640px+) */
  md:p-8     /* Medium screens (768px+) */
  lg:p-10    /* Large screens (1024px+) */
  xl:p-12    /* Extra large (1280px+) */
">
  Responsive padding
</div>
```

## Common Patterns

### Responsive Grid

```tsx
// Product grid: 1 col mobile → 2 col tablet → 3 col desktop → 4 col wide
<div className="
  grid
  grid-cols-1
  sm:grid-cols-2
  lg:grid-cols-3
  xl:grid-cols-4
  gap-4
  md:gap-6
">
  {products.map(product => (
    <ProductCard key={product.id} product={product} />
  ))}
</div>
```

### Responsive Navigation

```tsx
function Navigation() {
  return (
    <nav className="flex items-center justify-between px-4 md:px-6 lg:px-8 py-4">
      <Logo />

      {/* Desktop navigation */}
      <div className="hidden md:flex items-center gap-6">
        <NavLinks />
        <AuthButtons />
      </div>

      {/* Mobile menu button */}
      <button className="md:hidden p-2">
        <MenuIcon />
      </button>
    </nav>
  );
}
```

### Responsive Typography

```tsx
<article>
  <h1 className="
    text-2xl
    sm:text-3xl
    md:text-4xl
    lg:text-5xl
    font-bold
    leading-tight
  ">
    Article Title
  </h1>

  <p className="
    text-base
    md:text-lg
    lg:text-xl
    text-gray-600
    mt-4
    md:mt-6
  ">
    Article excerpt that adjusts size for readability.
  </p>
</article>
```

### Responsive Layout

```tsx
// Sidebar layout: stacked on mobile, side-by-side on desktop
<div className="
  flex
  flex-col
  lg:flex-row
  gap-6
  lg:gap-8
">
  {/* Main content */}
  <main className="flex-1 order-2 lg:order-1">
    <Content />
  </main>

  {/* Sidebar */}
  <aside className="
    w-full
    lg:w-80
    order-1
    lg:order-2
    lg:sticky
    lg:top-4
    lg:self-start
  ">
    <Sidebar />
  </aside>
</div>
```

### Responsive Card

```tsx
<div className="
  bg-white
  rounded-lg
  shadow-sm
  hover:shadow-md
  transition-shadow

  /* Padding */
  p-4
  sm:p-6

  /* Layout changes */
  flex
  flex-col
  sm:flex-row
  gap-4
">
  <img
    src={image}
    className="
      w-full
      sm:w-32
      h-32
      object-cover
      rounded
    "
  />

  <div className="flex-1">
    <h3 className="font-semibold text-lg">{title}</h3>
    <p className="text-gray-600 mt-2">{description}</p>
  </div>
</div>
```

## Show/Hide Elements

### Hide on Mobile

```tsx
// Hidden on mobile, visible on tablet+
<div className="hidden md:block">
  Desktop sidebar
</div>

// Hidden on mobile, flex on tablet+
<div className="hidden md:flex gap-4">
  Desktop navigation
</div>
```

### Hide on Desktop

```tsx
// Visible on mobile, hidden on tablet+
<button className="block md:hidden">
  Mobile menu
</button>

// Mobile-only banner
<div className="sm:hidden bg-blue-500 text-white p-2 text-center">
  Download our app!
</div>
```

### Conditional Display Types

```tsx
// Different display types at different breakpoints
<div className="
  hidden       /* Hidden by default */
  sm:block     /* Block on small+ */
  lg:flex      /* Flex on large+ */
  xl:grid      /* Grid on xl+ */
">
  Responsive display
</div>
```

## Responsive Spacing

### Container Patterns

```tsx
// Standard container
<div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
  Content with responsive horizontal padding
</div>

// Section spacing
<section className="py-12 md:py-16 lg:py-24">
  Content with responsive vertical padding
</section>
```

### Gap Scaling

```tsx
<div className="
  flex
  flex-wrap
  gap-2
  sm:gap-4
  md:gap-6
  lg:gap-8
">
  {items.map(item => <Item key={item.id} />)}
</div>
```

## Responsive Images

```tsx
// Full width on mobile, constrained on larger screens
<img
  src={image}
  className="
    w-full
    md:w-auto
    md:max-w-md
    lg:max-w-lg
    h-auto
    rounded-lg
  "
/>

// Aspect ratio responsive
<div className="
  aspect-video
  md:aspect-[4/3]
  lg:aspect-[16/9]
  overflow-hidden
  rounded-lg
">
  <img src={image} className="w-full h-full object-cover" />
</div>
```

## Hero Section Example

```tsx
function Hero() {
  return (
    <section className="
      relative
      overflow-hidden
      bg-gradient-to-br
      from-blue-600
      to-purple-700

      /* Responsive padding */
      px-4
      py-16
      sm:px-6
      sm:py-20
      md:py-24
      lg:px-8
      lg:py-32
    ">
      <div className="mx-auto max-w-4xl text-center">
        <h1 className="
          text-3xl
          sm:text-4xl
          md:text-5xl
          lg:text-6xl
          font-bold
          text-white
          tracking-tight
        ">
          Build amazing products
        </h1>

        <p className="
          mt-4
          sm:mt-6
          text-lg
          sm:text-xl
          md:text-2xl
          text-blue-100
          max-w-2xl
          mx-auto
        ">
          The all-in-one platform for modern teams.
        </p>

        <div className="
          mt-8
          sm:mt-10
          flex
          flex-col
          sm:flex-row
          justify-center
          gap-4
        ">
          <Button size="lg" className="w-full sm:w-auto">
            Get Started
          </Button>
          <Button
            variant="outline"
            size="lg"
            className="w-full sm:w-auto border-white text-white hover:bg-white/10"
          >
            Learn More
          </Button>
        </div>
      </div>
    </section>
  );
}
```

## Dashboard Layout Example

```tsx
function DashboardLayout({ children }) {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Mobile header */}
      <header className="
        lg:hidden
        sticky
        top-0
        z-50
        bg-white
        border-b
        px-4
        py-3
      ">
        <div className="flex items-center justify-between">
          <Logo />
          <MobileMenuButton />
        </div>
      </header>

      <div className="flex">
        {/* Desktop sidebar */}
        <aside className="
          hidden
          lg:flex
          lg:flex-col
          lg:w-64
          lg:fixed
          lg:inset-y-0
          border-r
          bg-white
        ">
          <Logo className="p-4 border-b" />
          <nav className="flex-1 p-4 space-y-1">
            <SidebarNavigation />
          </nav>
        </aside>

        {/* Main content */}
        <main className="
          flex-1
          lg:pl-64
        ">
          <div className="
            px-4
            py-6
            sm:px-6
            lg:px-8
          ">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
```

## Testing Responsive Designs

### Browser DevTools

1. Open DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Test common breakpoints: 375px, 640px, 768px, 1024px, 1280px

### Common Device Widths

| Device | Width |
|--------|-------|
| iPhone SE | 375px |
| iPhone 12/13 | 390px |
| iPad Mini | 768px |
| iPad Pro | 1024px |
| Laptop | 1280px |
| Desktop | 1440px+ |

### Responsive Testing Checklist

- [ ] Mobile (320-639px)
- [ ] Small tablet (640-767px)
- [ ] Tablet (768-1023px)
- [ ] Small laptop (1024-1279px)
- [ ] Desktop (1280px+)
- [ ] Large desktop (1536px+)
- [ ] Touch interactions work
- [ ] Text remains readable
- [ ] Images scale properly
- [ ] Navigation accessible
- [ ] Forms usable
