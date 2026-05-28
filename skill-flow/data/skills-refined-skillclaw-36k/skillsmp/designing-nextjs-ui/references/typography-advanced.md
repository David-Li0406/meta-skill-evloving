# Advanced Typography Techniques

Professional typography patterns for creating visual hierarchy and emphasis.

## Font Loading with Next.js

### Using Google Fonts (Recommended)

```tsx
import { Inter, Playfair_Display, Fira_Code } from 'next/font/google'

// Primary font (body text)
const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

// Display font (headings)
const playfair = Playfair_Display({
  subsets: ['latin'],
  variable: '--font-playfair',
  display: 'swap',
  weight: ['400', '700', '900'],
})

// Monospace font (code)
const firaCode = Fira_Code({
  subsets: ['latin'],
  variable: '--font-fira-code',
  display: 'swap',
})

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${inter.variable} ${playfair.variable} ${firaCode.variable}`}>
      <body className="font-sans antialiased">{children}</body>
    </html>
  )
}
```

Then configure in `tailwind.config.ts`:

```ts
export default {
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font-inter)', 'sans-serif'],
        display: ['var(--font-playfair)', 'serif'],
        mono: ['var(--font-fira-code)', 'monospace'],
      },
    },
  },
}
```

### Distinctive Font Recommendations

**Avoid generic fonts like Inter, Roboto, Arial, system fonts for important projects.**

**Display/Heading Fonts:**
- `Playfair Display` - Elegant serif, high contrast
- `Bebas Neue` - Bold, condensed, impactful
- `Space Grotesk` - Modern geometric sans
- `Abril Fatface` - High contrast display serif
- `Cinzel` - Classical elegance
- `Righteous` - Bold retro vibes

**Body Text Fonts:**
- `Source Sans Pro` - Clean, professional
- `Lora` - Readable serif with personality
- `Work Sans` - Versatile sans-serif
- `Merriweather` - Readable serif for longer content
- `DM Sans` - Modern, geometric
- `Manrope` - Rounded, friendly

**Monospace/Code Fonts:**
- `Fira Code` - Ligatures for code
- `JetBrains Mono` - Coding-specific design
- `Source Code Pro` - Clean monospace

## Text Hierarchy System

### Size Scale

```tsx
// Massive headlines (hero sections)
<h1 className="text-6xl md:text-7xl lg:text-8xl font-extrabold">
  Hero Headline
</h1>

// Large headings (section titles)
<h2 className="text-4xl md:text-5xl font-bold">
  Section Title
</h2>

// Medium headings (subsections)
<h3 className="text-2xl md:text-3xl font-semibold">
  Subsection
</h3>

// Small headings (cards, components)
<h4 className="text-xl font-semibold">
  Component Title
</h4>

// Body text
<p className="text-base leading-7">
  Body content with comfortable line height
</p>

// Small text (captions, metadata)
<span className="text-sm text-gray-600">
  Supporting information
</span>

// Extra small (labels, tags)
<span className="text-xs uppercase tracking-wider text-gray-500">
  Label
</span>
```

## Making Words Stand Out

### 1. Gradient Text (Eye-Catching)

```tsx
// Pink to violet gradient
<h1 className="text-5xl font-extrabold">
  <span className="bg-gradient-to-r from-pink-500 to-violet-500 bg-clip-text text-transparent">
    Stand Out Text
  </span>
</h1>

// Multi-color gradient
<span className="bg-gradient-to-r from-yellow-400 via-red-500 to-pink-500 bg-clip-text text-transparent">
  Vibrant Gradient
</span>

// Subtle elegant gradient
<span className="bg-gradient-to-r from-gray-700 to-gray-900 bg-clip-text text-transparent dark:from-gray-100 dark:to-gray-300">
  Elegant Gradient
</span>

// Animated gradient (requires custom CSS)
<span className="animate-gradient bg-gradient-to-r from-purple-400 via-pink-500 to-red-500 bg-clip-text text-transparent">
  Animated Gradient
</span>
```

Add to your CSS:

```css
@keyframes gradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.animate-gradient {
  background-size: 200% auto;
  animation: gradient 3s ease infinite;
}
```

### 2. Color Emphasis

```tsx
// Inline color emphasis
<p className="text-gray-700">
  This is normal text with{' '}
  <span className="font-semibold text-violet-600">highlighted words</span>
  {' '}that stand out.
</p>

// Background highlight
<p className="text-gray-900">
  Important information{' '}
  <span className="bg-yellow-200 px-1 font-medium">highlighted like a marker</span>
  {' '}for emphasis.
</p>

// Accent underline
<span className="border-b-2 border-violet-500 font-semibold">
  Underlined emphasis
</span>

// Combination emphasis
<span className="bg-violet-100 px-2 py-1 rounded font-semibold text-violet-700">
  Pill highlight
</span>
```

### 3. Weight & Style Contrast

```tsx
// Weight contrast within sentence
<p className="text-lg">
  This is <strong className="font-bold text-gray-900">important</strong> information
  {' '}mixed with <em className="font-medium italic">emphasized</em> content.
</p>

// Progressive weight scale
<div className="space-y-2">
  <p className="font-light text-gray-600">Light weight for subtle text</p>
  <p className="font-normal text-gray-700">Normal weight for body</p>
  <p className="font-medium text-gray-800">Medium weight for emphasis</p>
  <p className="font-semibold text-gray-900">Semibold for strong emphasis</p>
  <p className="font-bold text-gray-900">Bold for maximum emphasis</p>
</div>
```

### 4. Size Contrast

```tsx
// Mixed sizes in same line
<h2 className="text-4xl font-bold">
  Big Title{' '}
  <span className="text-xl font-normal text-gray-600">with small subtitle</span>
</h2>

// Number/stat emphasis
<div className="text-center">
  <div className="text-6xl font-extrabold text-violet-600">
    99%
  </div>
  <div className="text-sm text-gray-600 uppercase tracking-wide">
    Customer Satisfaction
  </div>
</div>
```

### 5. Letter Spacing & Transform

```tsx
// Wide tracking for labels
<span className="text-xs uppercase tracking-widest font-semibold text-gray-500">
  New Feature
</span>

// Tight tracking for impact
<h1 className="text-6xl font-black tracking-tighter">
  IMPACT
</h1>

// Normal tracking
<p className="tracking-normal">
  Default spacing
</p>

// Loose tracking
<p className="tracking-wide">
  Slightly loose
</p>

// Extra loose
<p className="tracking-widest">
  Very loose
</p>
```

### 6. Text Shadows & Effects

```tsx
// Drop shadow for depth
<h1 className="text-5xl font-bold text-white drop-shadow-lg">
  Text with Shadow
</h1>

// Multiple shadows for glow
<h1 className="text-4xl font-bold text-violet-500" style={{
  textShadow: '0 0 20px rgba(139, 92, 246, 0.5), 0 0 40px rgba(139, 92, 246, 0.3)'
}}>
  Glowing Text
</h1>

// Hard shadow for retro effect
<h1 className="text-5xl font-black text-violet-600" style={{
  textShadow: '4px 4px 0 rgba(0, 0, 0, 0.1)'
}}>
  Retro Shadow
</h1>
```

## Line Height for Readability

```tsx
// Tight line height for headings
<h1 className="text-6xl font-bold leading-tight">
  Multi-line
  Heading
</h1>

// Snug for subheadings
<h2 className="text-3xl font-semibold leading-snug">
  Comfortable
  Subheading
</h2>

// Normal for short text
<p className="text-lg leading-normal">
  Short paragraph text
</p>

// Relaxed for body text (recommended)
<p className="text-base leading-relaxed">
  Longer body text that needs comfortable reading space.
</p>

// Loose for extra readability
<p className="text-base leading-loose">
  Maximum readability for important content.
</p>
```

**Line height scale:**
- `leading-none` (1) - Very tight
- `leading-tight` (1.25) - Headlines
- `leading-snug` (1.375) - Subheadings
- `leading-normal` (1.5) - Default
- `leading-relaxed` (1.625) - Body text
- `leading-loose` (2) - Very comfortable

## Complete Typography Example

```tsx
export function BlogPost() {
  return (
    <article className="max-w-3xl mx-auto px-4 py-12">
      {/* Category badge */}
      <span className="inline-block mb-4 text-xs uppercase tracking-widest font-semibold text-violet-600 bg-violet-50 px-3 py-1 rounded-full">
        Tutorial
      </span>

      {/* Main headline with gradient */}
      <h1 className="text-5xl md:text-6xl font-extrabold leading-tight mb-6">
        <span className="bg-gradient-to-r from-violet-600 to-pink-600 bg-clip-text text-transparent">
          Master Typography
        </span>
        {' '}in Modern Web Design
      </h1>

      {/* Subtitle */}
      <p className="text-xl text-gray-600 leading-relaxed mb-8">
        Learn how to create <span className="font-semibold text-gray-900">beautiful, readable interfaces</span>
        {' '}with professional typography techniques.
      </p>

      {/* Metadata */}
      <div className="flex items-center gap-4 mb-12 pb-8 border-b">
        <img
          src="/avatar.jpg"
          alt="Author"
          className="size-12 rounded-full"
        />
        <div>
          <div className="font-semibold text-gray-900">Jane Doe</div>
          <div className="text-sm text-gray-600">
            Published on <time>January 17, 2026</time> · 8 min read
          </div>
        </div>
      </div>

      {/* Body content */}
      <div className="prose prose-lg">
        <p className="text-lg leading-relaxed text-gray-700 mb-6">
          Typography is the foundation of great design. Every element on your page
          communicates through text, and{' '}
          <strong className="font-semibold text-gray-900">how that text looks</strong>
          {' '}can make or break the user experience.
        </p>

        <h2 className="text-3xl font-bold text-gray-900 mt-12 mb-4">
          The Hierarchy Principle
        </h2>

        <p className="text-lg leading-relaxed text-gray-700 mb-6">
          Visual hierarchy guides your readers through content. Use size, weight,
          and color to create{' '}
          <span className="bg-yellow-100 px-1 font-medium">clear distinction</span>
          {' '}between elements.
        </p>

        {/* Callout box */}
        <div className="my-8 p-6 bg-violet-50 border-l-4 border-violet-500 rounded-r-lg">
          <p className="text-base leading-relaxed text-violet-900">
            <strong className="font-bold">Pro Tip:</strong> Limit your design to 2-3 fonts maximum.
            One for headings, one for body, and optionally one for code or special elements.
          </p>
        </div>
      </div>
    </article>
  )
}
```

## Responsive Typography

```tsx
// Scale smoothly across breakpoints
<h1 className="
  text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl
  font-extrabold leading-tight
">
  Responsive Headline
</h1>

// Adjust line height with size
<p className="
  text-base sm:text-lg md:text-xl
  leading-relaxed sm:leading-relaxed md:leading-loose
">
  Responsive body text
</p>

// Using clamp() for fluid typography (requires custom CSS)
<h1 className="fluid-heading">
  Fluid Headline
</h1>
```

Add to your CSS:

```css
.fluid-heading {
  font-size: clamp(2rem, 5vw, 4rem);
  line-height: 1.2;
}
```

## Dark Mode Typography

```tsx
// Adjust contrast for dark mode
<h1 className="text-gray-900 dark:text-white">
  Headline
</h1>

<p className="text-gray-700 dark:text-gray-300">
  Body text with proper contrast
</p>

// Gradient text in dark mode
<span className="
  bg-gradient-to-r from-violet-600 to-pink-600
  dark:from-violet-400 dark:to-pink-400
  bg-clip-text text-transparent
">
  Adaptive gradient
</span>

// Muted text
<span className="text-gray-600 dark:text-gray-400">
  Secondary information
</span>
```

## Accessibility Considerations

```tsx
// Minimum contrast ratios (WCAG AA)
// Normal text: 4.5:1
// Large text (18px+ or 14px+ bold): 3:1

// Good contrast
<p className="text-gray-900 dark:text-white">
  Readable text
</p>

// Use semantic HTML
<article>
  <h1>Main Title</h1>
  <p><strong>Important:</strong> Use semantic tags</p>
  <em>Emphasized text</em>
</article>

// Screen reader friendly
<span className="sr-only">Additional context for screen readers</span>
```
