# Craft in Action

This shows how bold choices translate to real code using React + Tailwind + Framer Motion. Learn the thinking, not just the code.

---

## Example: Hero Section

A hero that commands attention, not just fills space.

### The Setup

```jsx
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: 'var(--brand)',
          dark: 'var(--brand-dark)',
        },
        surface: {
          DEFAULT: 'var(--surface)',
          alt: 'var(--surface-alt)',
        },
        ink: {
          DEFAULT: 'var(--ink)',
          muted: 'var(--ink-muted)',
        },
      },
      fontFamily: {
        display: ['var(--font-display)', 'sans-serif'],
        body: ['var(--font-body)', 'sans-serif'],
      },
    },
  },
}
```

```css
/* globals.css */
:root {
  --brand: #ff6b35;
  --brand-dark: #e55a2b;
  --surface: #ffffff;
  --surface-alt: #fafafa;
  --ink: #0f172a;
  --ink-muted: #64748b;
  --font-display: 'Clash Display', sans-serif;
  --font-body: 'Inter', sans-serif;
}
```

### The Component

```tsx
import { motion } from 'framer-motion';

function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center px-6 overflow-hidden">
      {/* Background texture — subtle grain */}
      <div
        className="absolute inset-0 opacity-[0.03]"
        style={{ backgroundImage: 'url(/noise.png)' }}
      />

      {/* Content */}
      <div className="relative max-w-4xl mx-auto text-center">
        {/* Eyebrow */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mb-6"
        >
          <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-brand/10 text-brand text-sm font-medium">
            <span className="w-2 h-2 rounded-full bg-brand animate-pulse" />
            Now in public beta
          </span>
        </motion.div>

        {/* Headline */}
        <motion.h1
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="text-[clamp(3rem,8vw,6rem)] font-display font-black tracking-tight leading-[0.9] text-ink mb-6"
        >
          Ship faster.
          <br />
          <span className="text-brand">Sleep better.</span>
        </motion.h1>

        {/* Subheadline */}
        <motion.p
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="text-xl md:text-2xl text-ink-muted max-w-2xl mx-auto mb-10"
        >
          The deployment platform that catches errors before your users do.
          Built for teams who ship daily.
        </motion.p>

        {/* CTAs */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="flex flex-col sm:flex-row items-center justify-center gap-4"
        >
          <button className="w-full sm:w-auto px-8 py-4 bg-brand hover:bg-brand-dark text-white font-semibold rounded-full transition-all duration-200 hover:scale-105 hover:shadow-lg">
            Start free trial
          </button>
          <button className="w-full sm:w-auto px-8 py-4 border border-edge text-ink font-medium rounded-full hover:bg-surface-alt transition-colors">
            Watch demo
          </button>
        </motion.div>

        {/* Social proof micro */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.5 }}
          className="mt-12 flex items-center justify-center gap-8 text-sm text-ink-muted"
        >
          <div className="flex -space-x-2">
            {[1,2,3,4,5].map((i) => (
              <div key={i} className="w-8 h-8 rounded-full bg-surface-alt border-2 border-white" />
            ))}
          </div>
          <span>Trusted by 2,000+ teams</span>
        </motion.div>
      </div>
    </section>
  );
}
```

### Why These Decisions

**Why `clamp()` for headline?** Fluid typography that scales from mobile (3rem) to desktop (6rem) without breakpoints. The headline stays dramatic at every size.

**Why `leading-[0.9]`?** Tight line height creates tension in headlines. The words feel compressed, urgent. Body text gets `leading-relaxed` for comfort.

**Why the eyebrow badge?** Creates entry point before the headline. The pulsing dot adds life without animation overload.

**Why `rounded-full` on CTAs?** Pill buttons feel friendly and clickable. They also stand out from rectangular content blocks.

**Why staggered animations?** Creates reveal hierarchy: eyebrow → headline → subhead → CTAs → proof. Each element earns attention.

---

## Example: Features Section (Anti-Grid)

Not a grid of icons. A sequence of reveals.

```tsx
import { motion } from 'framer-motion';

const features = [
  {
    title: "Catch errors in staging",
    description: "AI-powered error detection flags issues before they reach production. No more 3am pages.",
    visual: "/feature-1.png",
  },
  {
    title: "One-click rollbacks",
    description: "Something breaks? Roll back to any previous deploy in seconds. Not minutes. Seconds.",
    visual: "/feature-2.png",
  },
  {
    title: "Built for teams",
    description: "Branch previews, PR comments, Slack alerts. Your whole team stays in sync.",
    visual: "/feature-3.png",
  },
];

function Features() {
  return (
    <section className="py-24 md:py-32 lg:py-40">
      <div className="max-w-7xl mx-auto px-6">
        {/* Section header */}
        <div className="max-w-3xl mb-20">
          <h2 className="text-[clamp(2rem,5vw,3.5rem)] font-display font-bold tracking-tight text-ink mb-6">
            Everything you need.
            <br />
            <span className="text-ink-muted">Nothing you don't.</span>
          </h2>
        </div>

        {/* Features — alternating layout */}
        <div className="space-y-24 md:space-y-32">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-100px" }}
              transition={{ duration: 0.6 }}
              className={`
                grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-20 items-center
                ${index % 2 === 1 ? 'lg:grid-flow-dense' : ''}
              `}
            >
              {/* Content */}
              <div className={index % 2 === 1 ? 'lg:col-start-2' : ''}>
                <h3 className="text-2xl md:text-3xl font-display font-bold text-ink mb-4">
                  {feature.title}
                </h3>
                <p className="text-lg text-ink-muted leading-relaxed">
                  {feature.description}
                </p>
              </div>

              {/* Visual */}
              <div className={`
                relative rounded-2xl overflow-hidden bg-surface-alt
                ${index % 2 === 1 ? 'lg:col-start-1' : ''}
              `}>
                <img
                  src={feature.visual}
                  alt={feature.title}
                  className="w-full"
                />
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
```

### Why These Decisions

**Why alternating layouts?** Breaks monotony. Left-right-left creates rhythm. A grid of three identical cards is forgettable.

**Why `lg:grid-flow-dense`?** Lets us control which side the image appears on at large screens while keeping markup order for mobile.

**Why no icons?** Icons are generic. Screenshots/visuals of actual product features are specific. Show, don't icon.

**Why separate animations per feature?** Each feature reveals as you scroll to it. Creates a journey, not a dump of information.

---

## Example: Social Proof Section

Not a logo wall. Context and credibility.

```tsx
import { motion } from 'framer-motion';

const testimonials = [
  {
    quote: "We went from weekly deploys to daily. The error catching alone paid for itself in the first month.",
    author: "Sarah Chen",
    role: "CTO at Raycast",
    avatar: "/avatars/sarah.jpg",
  },
  {
    quote: "Finally, a tool that doesn't require a PhD to configure. My team was productive in minutes.",
    author: "Marcus Johnson",
    role: "Lead Engineer at Linear",
    avatar: "/avatars/marcus.jpg",
  },
];

const logos = ['stripe', 'notion', 'figma', 'linear', 'raycast'];

function SocialProof() {
  return (
    <section className="py-24 md:py-32 bg-surface-alt">
      <div className="max-w-7xl mx-auto px-6">
        {/* Logo strip — understated */}
        <div className="flex items-center justify-center gap-12 mb-20 opacity-60">
          {logos.map((logo) => (
            <img
              key={logo}
              src={`/logos/${logo}.svg`}
              alt={logo}
              className="h-6 md:h-8 grayscale"
            />
          ))}
        </div>

        {/* Testimonials — large, impactful */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 md:gap-12">
          {testimonials.map((testimonial, index) => (
            <motion.blockquote
              key={testimonial.author}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              className="relative"
            >
              {/* Quote mark */}
              <span className="absolute -top-4 -left-2 text-6xl text-brand/20 font-serif">
                "
              </span>

              <p className="text-xl md:text-2xl text-ink leading-relaxed mb-6 relative">
                {testimonial.quote}
              </p>

              <footer className="flex items-center gap-4">
                <img
                  src={testimonial.avatar}
                  alt={testimonial.author}
                  className="w-12 h-12 rounded-full"
                />
                <div>
                  <div className="font-semibold text-ink">{testimonial.author}</div>
                  <div className="text-sm text-ink-muted">{testimonial.role}</div>
                </div>
              </footer>
            </motion.blockquote>
          ))}
        </div>
      </div>
    </section>
  );
}
```

### Why These Decisions

**Why grayscale logos?** Color logos compete for attention. Grayscale says "these companies trust us" without visual noise.

**Why large quote text?** Testimonials should be readable at a glance. Small text buried in cards gets skipped.

**Why real names and roles?** Specificity builds trust. "CTO at Raycast" is credible. "Happy customer" is not.

**Why the decorative quote mark?** Creates visual interest without adding content. The subtle brand color ties it back.

---

## Example: CTA Section (Final)

The close. Make it count.

```tsx
import { motion } from 'framer-motion';

function FinalCTA() {
  return (
    <section className="py-24 md:py-32 lg:py-40">
      <div className="max-w-4xl mx-auto px-6 text-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="text-[clamp(2.5rem,6vw,4.5rem)] font-display font-black tracking-tight text-ink mb-6">
            Ready to ship
            <br />
            <span className="text-brand">with confidence?</span>
          </h2>

          <p className="text-xl text-ink-muted mb-10 max-w-2xl mx-auto">
            Join 2,000+ teams who deploy without fear. Start your free trial today — no credit card required.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <button className="w-full sm:w-auto px-10 py-5 bg-brand hover:bg-brand-dark text-white text-lg font-semibold rounded-full transition-all duration-200 hover:scale-105 hover:shadow-xl">
              Start free trial
            </button>
            <button className="w-full sm:w-auto px-8 py-5 text-ink font-medium hover:text-brand transition-colors">
              Talk to sales →
            </button>
          </div>

          {/* Trust signals */}
          <div className="mt-12 flex flex-wrap items-center justify-center gap-6 text-sm text-ink-muted">
            <span className="flex items-center gap-2">
              <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
              14-day free trial
            </span>
            <span className="flex items-center gap-2">
              <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
              No credit card
            </span>
            <span className="flex items-center gap-2">
              <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
              Cancel anytime
            </span>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
```

### Why These Decisions

**Why larger button than hero?** Final CTA is the close. Make it unmissable. The larger size signals "this is important."

**Why trust signals?** Removes friction objections. "No credit card" answers "what's the catch?"

**Why "→" on secondary?** The arrow suggests continuation without competing with the primary CTA.

---

## Animation Patterns

### Stagger Container

```tsx
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};

function StaggeredList({ items }) {
  return (
    <motion.ul
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {items.map((item) => (
        <motion.li key={item.id} variants={itemVariants}>
          {item.content}
        </motion.li>
      ))}
    </motion.ul>
  );
}
```

### Scroll Progress

```tsx
import { useScroll, useTransform, motion } from 'framer-motion';

function ParallaxImage({ src }) {
  const { scrollYProgress } = useScroll();
  const y = useTransform(scrollYProgress, [0, 1], [0, -100]);

  return (
    <motion.img
      src={src}
      style={{ y }}
      className="w-full"
    />
  );
}
```

### Magnetic Button

```tsx
import { motion, useMotionValue, useSpring } from 'framer-motion';

function MagneticButton({ children }) {
  const x = useMotionValue(0);
  const y = useMotionValue(0);

  const springX = useSpring(x, { stiffness: 300, damping: 20 });
  const springY = useSpring(y, { stiffness: 300, damping: 20 });

  const handleMouse = (e: React.MouseEvent) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    x.set((e.clientX - centerX) * 0.2);
    y.set((e.clientY - centerY) * 0.2);
  };

  const handleLeave = () => {
    x.set(0);
    y.set(0);
  };

  return (
    <motion.button
      style={{ x: springX, y: springY }}
      onMouseMove={handleMouse}
      onMouseLeave={handleLeave}
      className="px-8 py-4 bg-brand text-white font-semibold rounded-full"
    >
      {children}
    </motion.button>
  );
}
```

---

## The Craft Check

Apply these to your output:

1. **Blur test:** Step back. Is hierarchy clear? Anything jarring?
2. **Swap test:** Replace your choices with defaults. Does it feel different?
3. **Scroll test:** Is there a reason to keep scrolling?
4. **Generic test:** Remove the brand. Could this be anyone's page?

If any fails, iterate before showing.
