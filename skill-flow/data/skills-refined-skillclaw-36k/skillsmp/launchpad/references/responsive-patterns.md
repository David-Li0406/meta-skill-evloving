# Responsive Design Patterns

Mobile-first, fluid responsive design for landing pages.

---

## Core Philosophy

### Mobile-First

Write base styles for mobile, enhance for larger screens:

```tsx
// Mobile-first: base is mobile, md: adds tablet/desktop
className="text-4xl md:text-5xl lg:text-6xl"
className="py-16 md:py-24 lg:py-32"
className="px-6 md:px-8"

// NOT desktop-first
className="text-6xl md:text-5xl sm:text-4xl"  // Harder to maintain
```

### Fluid Over Fixed

Use `clamp()` for typography to eliminate breakpoint jumps:

```tsx
// Fluid headline — scales smoothly
className="text-[clamp(2.5rem,6vw,5rem)]"

// Instead of stepped breakpoints
className="text-4xl md:text-5xl lg:text-6xl"  // Jumpy
```

### Content-Driven Breakpoints

Tailwind defaults work well for landing pages:
- `sm:` 640px — Large phones landscape
- `md:` 768px — Tablets
- `lg:` 1024px — Laptops
- `xl:` 1280px — Desktops
- `2xl:` 1536px — Large screens

---

## Hero Patterns

### Full-Screen Hero

```tsx
function Hero() {
  return (
    <section className="min-h-screen flex items-center justify-center px-6 py-20">
      <div className="max-w-4xl mx-auto text-center">
        {/* Content scales fluidly */}
        <h1 className="text-[clamp(2.5rem,8vw,6rem)] font-display font-black tracking-tight leading-[0.9]">
          Your headline here
        </h1>

        <p className="mt-6 text-lg md:text-xl text-ink-muted max-w-2xl mx-auto">
          Supporting text that explains the value proposition clearly.
        </p>

        {/* CTAs stack on mobile, inline on larger */}
        <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
          <button className="w-full sm:w-auto px-8 py-4 bg-brand text-white font-semibold rounded-full">
            Primary CTA
          </button>
          <button className="w-full sm:w-auto px-8 py-4 border border-edge text-ink font-medium rounded-full">
            Secondary CTA
          </button>
        </div>
      </div>
    </section>
  );
}
```

### Split Hero (Image + Content)

```tsx
function SplitHero() {
  return (
    <section className="min-h-screen flex items-center py-20 px-6">
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-20 items-center">
        {/* Content — full width on mobile, half on desktop */}
        <div className="text-center lg:text-left">
          <h1 className="text-[clamp(2.5rem,5vw,4rem)] font-display font-bold tracking-tight">
            Headline that commands attention
          </h1>
          <p className="mt-6 text-lg text-ink-muted">
            Supporting description here.
          </p>
          <div className="mt-8">
            <button className="px-8 py-4 bg-brand text-white font-semibold rounded-full">
              Get started
            </button>
          </div>
        </div>

        {/* Image — below on mobile, beside on desktop */}
        <div className="relative">
          <img
            src="/hero-image.png"
            alt="Product screenshot"
            className="w-full rounded-2xl shadow-2xl"
          />
        </div>
      </div>
    </section>
  );
}
```

---

## Section Patterns

### Standard Section

```tsx
function Section({ children }) {
  return (
    <section className="py-20 md:py-28 lg:py-32 px-6">
      <div className="max-w-7xl mx-auto">
        {children}
      </div>
    </section>
  );
}
```

### Narrow Content Section

```tsx
function NarrowSection({ children }) {
  return (
    <section className="py-20 md:py-28 lg:py-32 px-6">
      <div className="max-w-3xl mx-auto">
        {children}
      </div>
    </section>
  );
}
```

### Full-Bleed Section

```tsx
function FullBleedSection({ children, className }) {
  return (
    <section className={`py-20 md:py-28 lg:py-32 ${className}`}>
      <div className="max-w-7xl mx-auto px-6">
        {children}
      </div>
    </section>
  );
}

// Usage
<FullBleedSection className="bg-surface-alt">
  {/* Content */}
</FullBleedSection>
```

---

## Grid Patterns

### Feature Grid

```tsx
function FeatureGrid({ features }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 md:gap-10">
      {features.map((feature) => (
        <div key={feature.title} className="space-y-4">
          <div className="w-12 h-12 rounded-xl bg-brand/10 flex items-center justify-center">
            <feature.icon className="w-6 h-6 text-brand" />
          </div>
          <h3 className="text-xl font-semibold text-ink">{feature.title}</h3>
          <p className="text-ink-muted">{feature.description}</p>
        </div>
      ))}
    </div>
  );
}
```

### Alternating Content

```tsx
function AlternatingFeatures({ features }) {
  return (
    <div className="space-y-20 md:space-y-32">
      {features.map((feature, index) => (
        <div
          key={feature.title}
          className={`
            grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-20 items-center
            ${index % 2 === 1 ? 'lg:grid-flow-dense' : ''}
          `}
        >
          <div className={index % 2 === 1 ? 'lg:col-start-2' : ''}>
            <h3 className="text-2xl md:text-3xl font-bold text-ink mb-4">
              {feature.title}
            </h3>
            <p className="text-lg text-ink-muted">
              {feature.description}
            </p>
          </div>
          <div className={index % 2 === 1 ? 'lg:col-start-1' : ''}>
            <img src={feature.image} alt="" className="w-full rounded-2xl" />
          </div>
        </div>
      ))}
    </div>
  );
}
```

### Asymmetric Split

```tsx
// 60/40 split
<div className="grid grid-cols-1 lg:grid-cols-5 gap-12 items-center">
  <div className="lg:col-span-3">
    {/* Larger content area */}
  </div>
  <div className="lg:col-span-2">
    {/* Smaller content area */}
  </div>
</div>

// 70/30 split
<div className="grid grid-cols-1 lg:grid-cols-10 gap-12 items-center">
  <div className="lg:col-span-7">
    {/* Main content */}
  </div>
  <div className="lg:col-span-3">
    {/* Sidebar content */}
  </div>
</div>
```

---

## Navigation Patterns

### Simple Header

```tsx
function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="fixed top-0 inset-x-0 z-50 bg-white/80 backdrop-blur-md border-b border-edge">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        {/* Logo */}
        <a href="/" className="font-display font-bold text-xl">
          Logo
        </a>

        {/* Desktop nav */}
        <nav className="hidden md:flex items-center gap-8">
          <a href="#features" className="text-ink-muted hover:text-ink transition-colors">
            Features
          </a>
          <a href="#pricing" className="text-ink-muted hover:text-ink transition-colors">
            Pricing
          </a>
          <button className="px-5 py-2 bg-brand text-white font-medium rounded-full hover:bg-brand-dark transition-colors">
            Get started
          </button>
        </nav>

        {/* Mobile menu button */}
        <button
          className="md:hidden p-2 -mr-2"
          onClick={() => setMobileMenuOpen(true)}
        >
          <MenuIcon className="w-6 h-6" />
        </button>
      </div>

      {/* Mobile menu overlay */}
      {mobileMenuOpen && (
        <div className="fixed inset-0 z-50 bg-white md:hidden">
          <div className="p-6">
            <div className="flex items-center justify-between mb-8">
              <span className="font-display font-bold text-xl">Logo</span>
              <button onClick={() => setMobileMenuOpen(false)}>
                <XIcon className="w-6 h-6" />
              </button>
            </div>
            <nav className="space-y-6">
              <a href="#features" className="block text-2xl font-medium">Features</a>
              <a href="#pricing" className="block text-2xl font-medium">Pricing</a>
              <button className="w-full py-4 bg-brand text-white font-semibold rounded-full">
                Get started
              </button>
            </nav>
          </div>
        </div>
      )}
    </header>
  );
}
```

---

## Testimonial Patterns

### Card Grid

```tsx
function TestimonialGrid({ testimonials }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {testimonials.map((t) => (
        <blockquote
          key={t.author}
          className="bg-surface border border-edge rounded-2xl p-6"
        >
          <p className="text-ink mb-6">{t.quote}</p>
          <footer className="flex items-center gap-3">
            <img src={t.avatar} alt="" className="w-10 h-10 rounded-full" />
            <div>
              <div className="font-medium text-ink">{t.author}</div>
              <div className="text-sm text-ink-muted">{t.role}</div>
            </div>
          </footer>
        </blockquote>
      ))}
    </div>
  );
}
```

### Large Quote

```tsx
function LargeTestimonial({ quote, author, role, avatar }) {
  return (
    <blockquote className="max-w-4xl mx-auto text-center">
      <p className="text-2xl md:text-3xl lg:text-4xl font-medium text-ink leading-relaxed mb-8">
        "{quote}"
      </p>
      <footer className="flex items-center justify-center gap-4">
        <img src={avatar} alt="" className="w-14 h-14 rounded-full" />
        <div className="text-left">
          <div className="font-semibold text-ink">{author}</div>
          <div className="text-ink-muted">{role}</div>
        </div>
      </footer>
    </blockquote>
  );
}
```

---

## Footer Pattern

```tsx
function Footer() {
  return (
    <footer className="py-16 md:py-20 px-6 bg-surface-alt">
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-8 mb-12">
          {/* Logo column — full width on mobile */}
          <div className="col-span-2 md:col-span-4 lg:col-span-1 mb-4 lg:mb-0">
            <span className="font-display font-bold text-xl">Logo</span>
            <p className="mt-4 text-ink-muted text-sm max-w-xs">
              Short company description or tagline goes here.
            </p>
          </div>

          {/* Link columns */}
          <div>
            <h4 className="font-semibold text-ink mb-4">Product</h4>
            <ul className="space-y-3 text-sm text-ink-muted">
              <li><a href="#" className="hover:text-ink transition-colors">Features</a></li>
              <li><a href="#" className="hover:text-ink transition-colors">Pricing</a></li>
              <li><a href="#" className="hover:text-ink transition-colors">Changelog</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold text-ink mb-4">Company</h4>
            <ul className="space-y-3 text-sm text-ink-muted">
              <li><a href="#" className="hover:text-ink transition-colors">About</a></li>
              <li><a href="#" className="hover:text-ink transition-colors">Blog</a></li>
              <li><a href="#" className="hover:text-ink transition-colors">Careers</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold text-ink mb-4">Legal</h4>
            <ul className="space-y-3 text-sm text-ink-muted">
              <li><a href="#" className="hover:text-ink transition-colors">Privacy</a></li>
              <li><a href="#" className="hover:text-ink transition-colors">Terms</a></li>
            </ul>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="pt-8 border-t border-edge flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-ink-muted">
            © 2024 Company. All rights reserved.
          </p>
          <div className="flex items-center gap-4">
            <a href="#" className="text-ink-muted hover:text-ink transition-colors">
              <TwitterIcon className="w-5 h-5" />
            </a>
            <a href="#" className="text-ink-muted hover:text-ink transition-colors">
              <GitHubIcon className="w-5 h-5" />
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
```

---

## Touch Considerations

### Touch Targets

Minimum 44px for tappable elements:

```tsx
// Buttons — generous padding
className="px-6 py-4"  // At least 44px height

// Icon buttons — explicit size
className="w-11 h-11 flex items-center justify-center"

// Links in lists — generous spacing
className="py-3"  // Comfortable tap area
```

### Mobile-Specific Adjustments

```tsx
// Larger text on mobile for readability
className="text-base md:text-sm"

// More padding on mobile for touch
className="p-4 md:p-3"

// Stack buttons on mobile
className="flex flex-col sm:flex-row gap-4"
```

---

## Testing Checklist

1. **Resize browser** from 320px to 1920px
2. **Check breakpoint transitions** — no jarring jumps
3. **Test on real devices** — iOS Safari, Android Chrome
4. **Check touch targets** — minimum 44px
5. **Test horizontal scroll** — should never happen
6. **Verify text readability** — nothing smaller than 14px on mobile
