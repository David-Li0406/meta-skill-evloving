# Creative Portfolio Template

A starting point for portfolio sites that showcase creative or technical work. Includes optional Three.js integration for immersive experiences.

---

## When to Use

- Developer/designer portfolios
- Creative agency showcases
- Freelancer personal sites
- Artist/photographer portfolios
- 3D artist showcases

---

## Example Data Notice

> **This template includes realistic example data** to make the first iteration viewable. Look for `// -- EXAMPLE DATA --` comments marking data you should replace with your own content.

## Structure

```
1. Hero — Name, role, signature visual
2. Selected Work — Project showcases (2-4 featured)
3. About — Brief bio, skills, approach
4. Contact — CTA, social links
5. Footer — Minimal
```

---

## Direction Prompts

Before using this template, answer:

1. **What's your signature?** The one visual element that makes this unmistakably yours.
2. **What work do you want?** The projects on display should attract similar work.
3. **What's the vibe?** Technical precision? Creative chaos? Minimal elegance?
4. **Do you need 3D?** Only if it showcases your work or fits your brand — not as decoration.

---

## Stack Options

### Standard Stack
```
React + Tailwind CSS + Framer Motion
```
Good for: Most portfolios, content-focused, fast loading

### Enhanced Stack (with Three.js)
```
React + Tailwind CSS + Framer Motion + React Three Fiber
```
Good for: 3D artists, creative technologists, immersive brands

**Only include Three.js if:**
- You're showcasing 3D work
- Your brand is explicitly technical/cutting-edge
- You can provide mobile fallbacks

---

## Section Blueprints

### 1. Hero

**Standard Hero:**
```tsx
<section className="min-h-screen flex items-center px-6 md:px-12 lg:px-24">
  <div className="max-w-4xl">
    {/* Optional eyebrow */}
    <span className="text-sm font-mono text-brand uppercase tracking-widest mb-4 block">
      {/* -- EXAMPLE DATA -- */}
      Creative Developer
      {/* -- END EXAMPLE DATA -- */}
    </span>

    <h1 className="text-[clamp(3rem,8vw,6rem)] font-display font-bold tracking-tight leading-[0.9]">
      {/* -- EXAMPLE DATA -- */}
      Alex Rivera
      {/* -- END EXAMPLE DATA -- */}
    </h1>

    <p className="mt-6 text-xl text-ink-muted max-w-xl">
      {/* -- EXAMPLE DATA -- */}
      I design and build digital experiences that blend craft with code.
      {/* -- END EXAMPLE DATA -- */}
    </p>

    <div className="mt-8 flex gap-4">
      <a href="#work" className="btn-primary">View Work</a>
      <a href="#contact" className="btn-secondary">Get in Touch</a>
    </div>
  </div>
</section>
```

**Hero with Three.js Background:**
```tsx
<section className="relative min-h-screen flex items-center px-6 md:px-12 lg:px-24">
  {/* 3D Background */}
  <div className="absolute inset-0 -z-10">
    <Suspense fallback={<div className="bg-void" />}>
      <Canvas camera={{ position: [0, 0, 5] }}>
        <HeroScene />
      </Canvas>
    </Suspense>
  </div>

  {/* Content */}
  <div className="relative max-w-4xl">
    {/* Same content as above */}
  </div>
</section>
```

**Hero Scene Options:**
- Floating geometry (see `references/threejs-patterns.md`)
- Particle field
- Mouse-following element
- Custom shader background

### 2. Selected Work

**Projects Data:**
```tsx
// -- EXAMPLE DATA --
const projects = [
  {
    id: 1,
    title: 'Meridian',
    category: 'Brand Identity',
    year: '2024',
    image: '/projects/meridian.jpg',
    description: 'Visual identity for a sustainable fashion label',
  },
  {
    id: 2,
    title: 'Pulse',
    category: 'Web Application',
    year: '2024',
    image: '/projects/pulse.jpg',
    description: 'Real-time analytics dashboard for e-commerce',
  },
  {
    id: 3,
    title: 'Terraform',
    category: 'Interactive',
    year: '2023',
    image: '/projects/terraform.jpg',
    description: 'WebGL terrain visualization experiment',
  },
  {
    id: 4,
    title: 'Sonnet',
    category: 'Mobile App',
    year: '2023',
    image: '/projects/sonnet.jpg',
    description: 'Poetry writing and sharing app',
  },
];
// -- END EXAMPLE DATA --
```

**Grid Layout:**
```tsx
<section id="work" className="py-24 md:py-32 px-6 md:px-12 lg:px-24">
  <div className="max-w-7xl mx-auto">
    <h2 className="text-3xl md:text-4xl font-display font-bold mb-12">
      Selected Work
    </h2>

    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
      {projects.map((project) => (
        <ProjectCard key={project.id} project={project} />
      ))}
    </div>
  </div>
</section>
```

**Project Card:**
```tsx
function ProjectCard({ project }) {
  return (
    <article className="group">
      {/* Image/Preview */}
      <div className="aspect-[4/3] rounded-xl overflow-hidden bg-surface mb-4">
        <img
          src={project.image}
          alt={project.title}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
        />
      </div>

      {/* Info */}
      <div className="flex items-start justify-between">
        <div>
          <h3 className="text-xl font-semibold group-hover:text-brand transition-colors">
            {project.title}
          </h3>
          <p className="text-ink-muted mt-1">{project.category}</p>
        </div>
        <span className="text-sm text-ink-muted">{project.year}</span>
      </div>
    </article>
  );
}
```

**With 3D Preview (for 3D work):**
```tsx
function Project3DCard({ project }) {
  const [hovered, setHovered] = useState(false);

  return (
    <article
      className="group"
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      <div className="aspect-[4/3] rounded-xl overflow-hidden bg-charcoal">
        {hovered ? (
          <Canvas>
            <Suspense fallback={null}>
              <ProjectModel url={project.modelUrl} />
              <OrbitControls enableZoom={false} autoRotate />
            </Suspense>
          </Canvas>
        ) : (
          <img src={project.thumbnail} alt={project.title} />
        )}
      </div>
      {/* Same info section */}
    </article>
  );
}
```

### 3. About

**Skills Data:**
```tsx
// -- EXAMPLE DATA --
const skills = [
  'React',
  'TypeScript',
  'Three.js',
  'Figma',
  'Framer Motion',
  'Node.js',
  'Tailwind CSS',
  'WebGL',
];
// -- END EXAMPLE DATA --
```

```tsx
<section id="about" className="py-24 md:py-32 px-6 md:px-12 lg:px-24 bg-surface-alt">
  <div className="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-12">
    {/* Photo or avatar */}
    <div className="md:col-span-1">
      <div className="aspect-square rounded-xl overflow-hidden">
        <img src="/avatar.jpg" alt="Alex Rivera" className="w-full h-full object-cover" />
      </div>
    </div>

    {/* Bio */}
    <div className="md:col-span-2 space-y-6">
      <h2 className="text-3xl font-display font-bold">About</h2>

      <p className="text-lg text-ink-muted leading-relaxed">
        {/* -- EXAMPLE DATA -- */}
        I'm a creative developer based in Portland, crafting interfaces that feel as good as they look.
        I bridge the gap between design and engineering, turning ambitious concepts into polished products.
        {/* -- END EXAMPLE DATA -- */}
      </p>

      <p className="text-ink-muted leading-relaxed">
        {/* -- EXAMPLE DATA -- */}
        Previously at Stripe and Vercel, now working independently with startups and studios who care
        about the details. When I'm not coding, I'm usually hiking the Pacific Northwest or
        experimenting with generative art.
        {/* -- END EXAMPLE DATA -- */}
      </p>

      {/* Skills/tools */}
      <div className="pt-4">
        <h3 className="text-sm font-mono text-ink-muted uppercase tracking-wide mb-3">
          Tools & Technologies
        </h3>
        <div className="flex flex-wrap gap-2">
          {skills.map((skill) => (
            <span
              key={skill}
              className="px-3 py-1 text-sm bg-surface border border-edge rounded-full"
            >
              {skill}
            </span>
          ))}
        </div>
      </div>
    </div>
  </div>
</section>
```

### 4. Contact

```tsx
<section id="contact" className="py-24 md:py-32 px-6 md:px-12 lg:px-24">
  <div className="max-w-2xl mx-auto text-center">
    <h2 className="text-3xl md:text-4xl font-display font-bold mb-6">
      Let's Work Together
    </h2>

    <p className="text-xl text-ink-muted mb-8">
      {/* -- EXAMPLE DATA -- */}
      Currently taking on new projects for Q2 2024. I work best with teams who
      value craft and aren't afraid to push boundaries.
      {/* -- END EXAMPLE DATA -- */}
    </p>

    <a
      {/* -- EXAMPLE DATA -- */}
      href="mailto:hello@alexrivera.dev"
      {/* -- END EXAMPLE DATA -- */}
      className="inline-flex items-center gap-2 px-8 py-4 bg-brand text-white font-semibold rounded-full hover:bg-brand-dark transition-colors"
    >
      Get in Touch
      <ArrowRight className="w-5 h-5" />
    </a>

    {/* Social links */}
    <div className="mt-12 flex items-center justify-center gap-6">
      <a href="#" className="text-ink-muted hover:text-brand transition-colors">
        <Twitter className="w-5 h-5" />
      </a>
      <a href="#" className="text-ink-muted hover:text-brand transition-colors">
        <GitHub className="w-5 h-5" />
      </a>
      <a href="#" className="text-ink-muted hover:text-brand transition-colors">
        <LinkedIn className="w-5 h-5" />
      </a>
    </div>
  </div>
</section>
```

---

## Three.js Integration Points

If the user opts in to Three.js, these are the natural integration points:

| Section | 3D Option | Fallback |
|---------|-----------|----------|
| Hero | Background scene, particles, floating geometry | Static gradient or image |
| Work | 3D model previews on hover | Static thumbnails |
| About | Animated avatar or scene | Static photo |
| 404 | Interactive lost-in-space scene | Simple text |

**Always provide fallbacks** — See `references/threejs-patterns.md` for WebGL detection.

---

## Color Direction Options

### Dark Technical (Developer)
```css
--brand: #00ff88;
--surface: #0a0a0a;
--ink: #fafafa;
--ink-muted: #888888;
```

### Warm Creative (Designer)
```css
--brand: #ff6b35;
--surface: #fffbf5;
--ink: #1a1a1a;
--ink-muted: #666666;
```

### Minimal Mono (Photographer)
```css
--brand: #000000;
--surface: #ffffff;
--ink: #000000;
--ink-muted: #888888;
```

### Cyberpunk (3D Artist)
```css
--brand: #ff00ff;
--surface: #0d0d0d;
--ink: #ffffff;
--accent: #00ffff;
```

---

## Signature Ideas

The portfolio needs ONE memorable element. Options:

- **Custom cursor** that transforms on interactive elements
- **Magnetic buttons** that follow the mouse
- **Page transitions** with distinctive animation
- **3D hero scene** that responds to scroll/mouse
- **Typography treatment** unique to your name
- **Loading sequence** that sets the tone
- **Hover reveals** on project cards

Pick one. Commit to it. Echo it subtly throughout.

---

## Anti-Patterns

- **Too many projects** — 3-6 featured, not a complete archive
- **Generic bio** — "Passionate creative" means nothing
- **No personality** — Your portfolio IS your brand
- **3D for decoration** — Only if it serves the work
- **Slow loading** — Performance is part of the experience
- **No clear CTA** — What do you want visitors to do?

---

## Next Steps

1. Answer the direction prompts
2. Choose your stack (standard or with Three.js)
3. Define your signature element
4. Build hero → work → about → contact
5. Run the craft checks before launching
6. Offer to save patterns to `.launchpad/system.md`

This template is a starting point. Your portfolio should be unrecognizable as a template.

---

## Customization Checklist

Replace the example data with your own content:

- [ ] **Hero** — Your name, title, and tagline
- [ ] **Projects** — Your 3-6 best projects with images
- [ ] **Skills** — Your actual tools and technologies
- [ ] **About** — Your bio, background, and photo
- [ ] **Contact** — Your email and social links
- [ ] **Colors** — Choose a palette that fits your brand
- [ ] **Signature** — Pick one memorable element and commit to it
