# Component Patterns Reference

Detailed patterns for implementing Kenya Hara's "White" philosophy in UI components.

## Table of Contents
1. Layout Systems
2. Hero & Landing Patterns
3. Navigation Patterns
4. Typography Systems
5. Card & Container Patterns
6. Form Patterns
7. Interactive Elements
8. Animation Patterns

---

## 1. Layout Systems

### The Horizon Layout
Inspired by MUJI's famous Horizon campaign. Content occupies minimal space, surrounded by vast emptiness.

```
┌─────────────────────────────────────────┐
│                                         │
│                                         │
│                                         │
│            [Single Element]             │
│                                         │
│                                         │
│                                         │
└─────────────────────────────────────────┘
```

**CSS Pattern:**
```css
.horizon-layout {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 5vw;
}
```

### The Asymmetric Float
Elements positioned off-center, creating dynamic tension with surrounding space.

```
┌─────────────────────────────────────────┐
│                                         │
│    [Element]                            │
│                                         │
│                                         │
│                        [Element]        │
│                                         │
└─────────────────────────────────────────┘
```

### The Vertical Scroll
Long-form content with generous vertical spacing, each section a contemplative pause.

```css
.section {
  min-height: 80vh;
  padding: 15vh 10vw;
}

.section + .section {
  margin-top: 20vh;
}
```

---

## 2. Hero & Landing Patterns

### Muji Horizon Hero
Pure emptiness with centered typographic element.

```jsx
<section className="h-screen flex items-center justify-center bg-[#FAF9F7]">
  <div className="text-center">
    <h1 className="text-[#1A1A1A] text-lg tracking-[0.3em] font-light">
      品名
    </h1>
  </div>
</section>
```

### Single Image Hero
One powerful image floating in space, no overlays.

```jsx
<section className="min-h-screen p-[10vw] flex items-center justify-center">
  <img 
    src="..." 
    alt="..." 
    className="max-w-[60vw] max-h-[60vh] object-contain"
  />
</section>
```

### Typography-Only Hero
Words as the sole element, demanding attention through isolation.

```jsx
<section className="min-h-screen flex items-end p-16">
  <h1 className="text-6xl font-light leading-tight tracking-tight text-[#1A1A1A]">
    White is not<br />
    a color.
  </h1>
</section>
```

---

## 3. Navigation Patterns

### Whisper Navigation
Navigation that appears subtly, never demanding attention.

```jsx
<nav className="fixed top-0 left-0 right-0 p-8 flex justify-between items-center">
  <a href="/" className="text-sm tracking-widest text-[#4A4A4A] hover:text-[#1A1A1A] transition-colors duration-500">
    Home
  </a>
  <div className="flex gap-12">
    <a href="/works" className="text-sm tracking-widest text-[#4A4A4A] hover:text-[#1A1A1A] transition-colors duration-500">
      Works
    </a>
    <a href="/about" className="text-sm tracking-widest text-[#4A4A4A] hover:text-[#1A1A1A] transition-colors duration-500">
      About
    </a>
  </div>
</nav>
```

### Hidden Navigation
Revealed only on hover or scroll, preserving canvas purity.

```jsx
<nav className="fixed top-0 left-0 right-0 opacity-0 hover:opacity-100 transition-opacity duration-700">
  {/* Navigation content */}
</nav>
```

### Vertical Navigation
For long-form sites, a subtle vertical indicator.

```jsx
<nav className="fixed right-8 top-1/2 -translate-y-1/2 flex flex-col gap-4">
  {sections.map((section, i) => (
    <a 
      key={i}
      href={`#${section.id}`}
      className="w-px h-8 bg-[#8A8A8A] hover:bg-[#1A1A1A] transition-colors duration-500"
      aria-label={section.name}
    />
  ))}
</nav>
```

---

## 4. Typography Systems

### Heading Hierarchy

```css
/* Display - for hero moments */
.text-display {
  font-family: 'Cormorant', serif;
  font-size: clamp(2.5rem, 8vw, 6rem);
  font-weight: 300;
  line-height: 1.1;
  letter-spacing: -0.02em;
  color: var(--sumi);
}

/* Title - section headings */
.text-title {
  font-family: 'Karla', sans-serif;
  font-size: clamp(1.25rem, 3vw, 1.75rem);
  font-weight: 400;
  line-height: 1.3;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--usuzumi);
}

/* Body - readable prose */
.text-body {
  font-family: 'Karla', sans-serif;
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.8;
  letter-spacing: 0.02em;
  color: var(--usuzumi);
}

/* Caption - subtle annotations */
.text-caption {
  font-family: 'Karla', sans-serif;
  font-size: 0.75rem;
  font-weight: 400;
  line-height: 1.5;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--hai);
}
```

### Japanese Typography

```css
/* For Japanese text - generous line height is essential */
.text-jp {
  font-family: 'Noto Sans JP', sans-serif;
  font-weight: 300;
  line-height: 2;
  letter-spacing: 0.1em;
}

/* Traditional Japanese feel */
.text-jp-traditional {
  font-family: 'Shippori Mincho', serif;
  font-weight: 400;
  line-height: 2.2;
}
```

---

## 5. Card & Container Patterns

### Borderless Card
Content floats without explicit boundaries.

```jsx
<article className="p-8">
  <img src="..." alt="..." className="w-full mb-8" />
  <h3 className="text-sm tracking-widest text-[#4A4A4A] mb-4">Title</h3>
  <p className="text-sm text-[#8A8A8A] leading-relaxed">Description</p>
</article>
```

### Single-Line Card
Subtle bottom border as the only definition.

```jsx
<article className="py-8 border-b border-[#F0EFED]">
  <h3 className="text-base text-[#1A1A1A] mb-2">Title</h3>
  <p className="text-sm text-[#8A8A8A]">Description</p>
</article>
```

### Hover-Reveal Card
Additional information emerges on interaction.

```jsx
<article className="group p-8">
  <img src="..." alt="..." className="w-full mb-8" />
  <h3 className="text-sm tracking-widest text-[#4A4A4A]">Title</h3>
  <p className="text-sm text-[#8A8A8A] leading-relaxed opacity-0 group-hover:opacity-100 transition-opacity duration-500 mt-4">
    Description revealed on hover
  </p>
</article>
```

---

## 6. Form Patterns

### Minimal Input
Bottom border only, focusing attention on content.

```jsx
<div className="relative">
  <input 
    type="text"
    className="w-full py-4 bg-transparent border-b border-[#F0EFED] focus:border-[#1A1A1A] outline-none transition-colors duration-500 text-[#1A1A1A]"
    placeholder="Enter text"
  />
</div>
```

### Floating Label Input

```jsx
<div className="relative pt-6">
  <input 
    type="text"
    id="name"
    className="peer w-full py-2 bg-transparent border-b border-[#F0EFED] focus:border-[#1A1A1A] outline-none transition-colors duration-500 text-[#1A1A1A]"
    placeholder=" "
  />
  <label 
    htmlFor="name"
    className="absolute top-0 left-0 text-xs tracking-widest text-[#8A8A8A] peer-placeholder-shown:text-base peer-placeholder-shown:top-8 peer-focus:top-0 peer-focus:text-xs transition-all duration-300"
  >
    Name
  </label>
</div>
```

### Textarea with Breath

```jsx
<textarea 
  className="w-full min-h-[200px] p-6 bg-[#FAF9F7] border-none outline-none resize-none text-[#1A1A1A] leading-relaxed placeholder:text-[#8A8A8A]"
  placeholder="Share your thoughts..."
/>
```

---

## 7. Interactive Elements

### Text Button
No background, just text that transforms.

```jsx
<button className="text-sm tracking-widest text-[#4A4A4A] hover:text-[#1A1A1A] transition-colors duration-500">
  Learn more
</button>
```

### Outline Button
Minimal border, no fill.

```jsx
<button className="px-8 py-3 border border-[#1A1A1A] text-sm tracking-widest text-[#1A1A1A] hover:bg-[#1A1A1A] hover:text-white transition-all duration-500">
  Submit
</button>
```

### Icon Button
Icon alone, no decoration.

```jsx
<button className="p-4 text-[#4A4A4A] hover:text-[#1A1A1A] transition-colors duration-500">
  <svg className="w-5 h-5" /* icon */ />
</button>
```

### Link with Underline Reveal

```jsx
<a href="#" className="relative text-[#1A1A1A] group">
  <span>Discover</span>
  <span className="absolute bottom-0 left-0 w-0 h-px bg-[#1A1A1A] group-hover:w-full transition-all duration-500" />
</a>
```

---

## 8. Animation Patterns

### Fade Emerge
Content fades and rises gently into view.

```jsx
<div 
  className="opacity-0 translate-y-5 animate-emerge"
  style={{ animationDelay: '200ms' }}
>
  Content
</div>

// In CSS
@keyframes emerge {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-emerge {
  animation: emerge 800ms cubic-bezier(0.23, 1, 0.32, 1) forwards;
}
```

### Staggered Reveal
Multiple elements appear in sequence.

```jsx
{items.map((item, i) => (
  <div 
    key={i}
    className="opacity-0 translate-y-5 animate-emerge"
    style={{ animationDelay: `${200 + i * 100}ms` }}
  >
    {item}
  </div>
))}
```

### Scroll-Triggered Fade

```jsx
// Using Intersection Observer
const [isVisible, setIsVisible] = useState(false);
const ref = useRef();

useEffect(() => {
  const observer = new IntersectionObserver(
    ([entry]) => setIsVisible(entry.isIntersecting),
    { threshold: 0.1 }
  );
  if (ref.current) observer.observe(ref.current);
  return () => observer.disconnect();
}, []);

<div 
  ref={ref}
  className={`transition-all duration-1000 ${
    isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
  }`}
>
  Content
</div>
```

### Breath Animation
Subtle pulsing that suggests life.

```css
@keyframes breathe {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}

.animate-breathe {
  animation: breathe 4s ease-in-out infinite;
}
```
