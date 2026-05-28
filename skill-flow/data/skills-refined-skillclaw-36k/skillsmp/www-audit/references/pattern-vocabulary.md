# UI Pattern Vocabulary

Consistent naming for extracted patterns. Use these terms in audit reports for www-studio consumption.

## Layout Patterns

| Pattern | Description | Example Sites |
|---------|-------------|---------------|
| **sticky-nav** | Navigation fixed to top on scroll | most SaaS sites |
| **hero-split** | Hero with text left, visual right | landing pages |
| **hero-centered** | Centered hero with CTA | minimal sites |
| **bento-grid** | Asymmetric feature grid | Apple, Linear |
| **alternating-sections** | Left-right alternating content | product pages |
| **sidebar-layout** | Fixed sidebar, scrolling content | docs, dashboards |
| **footer-grid** | Multi-column footer with links | most sites |
| **footer-minimal** | Single line footer | minimal sites |
| **faq-driven** | FAQ as primary content structure | internet.dev |

## Navigation Patterns

| Pattern | Description |
|---------|-------------|
| **topbar-nav** | Horizontal nav in header |
| **hamburger-mobile** | Collapsed nav on mobile |
| **mega-menu** | Dropdown with rich content |
| **command-palette** | Cmd+K search interface |
| **breadcrumb** | Hierarchical path navigation |
| **tab-nav** | Horizontal tabs for sections |
| **sidebar-nav** | Vertical navigation list |

## Component Patterns

### Buttons

| Pattern | Description |
|---------|-------------|
| **btn-primary** | Main CTA, filled |
| **btn-secondary** | Secondary action, outlined |
| **btn-ghost** | Minimal, text-only |
| **btn-icon** | Icon-only button |
| **btn-gradient** | Gradient background |

### Cards

| Pattern | Description |
|---------|-------------|
| **card-feature** | Icon + title + description |
| **card-testimonial** | Quote + avatar + name |
| **card-pricing** | Tier + price + features |
| **card-blog** | Image + title + excerpt |
| **card-product** | Image + details + CTA |

### Forms

| Pattern | Description |
|---------|-------------|
| **input-floating** | Label floats on focus |
| **input-inline** | Label to the left |
| **input-stacked** | Label above input |
| **validation-inline** | Error below input |
| **validation-toast** | Error as notification |

### Feedback

| Pattern | Description |
|---------|-------------|
| **toast-bottom** | Notifications bottom-right |
| **toast-top** | Notifications top-center |
| **modal-centered** | Centered dialog |
| **modal-drawer** | Slide-in from side |
| **skeleton-loading** | Placeholder shapes while loading |
| **progress-bar** | Linear progress indicator |
| **spinner** | Circular loading indicator |

### Lists

| Pattern | Description |
|---------|-------------|
| **list-simple** | Basic unordered list |
| **list-icon** | Icon prefix per item |
| **list-description** | Title + description per item |
| **accordion** | Expandable sections |
| **details-summary** | Native HTML expand/collapse |

## Content Patterns

| Pattern | Description |
|---------|-------------|
| **faq-accordion** | Q&A with expand/collapse |
| **feature-grid** | Icons/titles in grid |
| **testimonial-carousel** | Rotating quotes |
| **logo-wall** | Client/partner logos |
| **stats-row** | Key metrics inline |
| **comparison-table** | Feature comparison |
| **changelog** | Version history list |

## Typography Patterns

| Pattern | Description |
|---------|-------------|
| **typography-first** | Large text, minimal images |
| **display-serif** | Serif for headings |
| **display-sans** | Sans-serif for headings |
| **mono-accents** | Monospace for code/technical |
| **gradient-text** | Gradient fill on headings |

## Visual Patterns

| Pattern | Description |
|---------|-------------|
| **dark-mode** | Dark theme support |
| **light-mode** | Light theme only |
| **glassmorphism** | Frosted glass effect |
| **neumorphism** | Soft shadows, embossed |
| **minimal-chrome** | Very little UI decoration |
| **border-subtle** | Light borders for separation |
| **shadow-elevation** | Shadows for depth |

## Animation Patterns

| Pattern | Description |
|---------|-------------|
| **fade-in** | Elements fade on enter |
| **slide-up** | Elements slide up on scroll |
| **stagger** | Sequential animation delays |
| **parallax** | Depth on scroll |
| **hover-lift** | Element rises on hover |
| **hover-glow** | Glow effect on hover |
| **micro-interactions** | Small feedback animations |

## Responsive Patterns

| Pattern | Breakpoints |
|---------|-------------|
| **mobile-first** | 640, 768, 1024, 1280 |
| **desktop-first** | reverse of above |
| **fluid-typography** | clamp() for font sizes |
| **container-queries** | Component-level responsive |

## Color Patterns

| Pattern | Description |
|---------|-------------|
| **monochrome** | Single hue + neutrals |
| **complementary** | Two opposite hues |
| **analogous** | Adjacent hues |
| **accent-minimal** | Mostly neutral + one accent |
| **vibrant** | High saturation colors |
| **muted** | Low saturation, soft |

## Reference Sites by Pattern

| Site | Key Patterns |
|------|--------------|
| **linear.app** | bento-grid, command-palette, dark-mode, micro-interactions |
| **stripe.com** | gradient-text, alternating-sections, comparison-table |
| **vercel.com** | minimal-chrome, typography-first, dark-mode |
| **notion.so** | sidebar-layout, command-palette, block-based |
| **figma.com** | bento-grid, feature-grid, gradient-text |
| **internet.dev** | faq-driven, typography-first, minimal-chrome, footer-grid |
| **sacred.computer** | terminal-aesthetic, monospace, minimal-chrome |

## Using in www-studio

When building, reference patterns by name:

```
"Build a landing page with:
- hero-centered
- feature-grid (3 columns)
- testimonial-carousel
- faq-accordion
- footer-grid

Reference internet.dev for the faq-driven pattern.
Reference linear.app for the bento-grid pattern."
```
