# SaaS Product Launch Template

A starting point for SaaS product launches. Adapt to your brand — don't use as-is.

---

## When to Use

- New SaaS product launch
- Feature announcement pages
- Beta/waitlist landing pages
- Product-led growth landing pages

## Structure

```
1. Hero — The promise
2. Social Proof Strip — Quick credibility
3. Problem/Pain — Why this matters
4. Solution — How it works (3 key features)
5. Deep Dive — One feature showcase
6. Testimonials — Proof it works
7. Pricing (optional) — Clear tiers
8. Final CTA — The close
9. Footer
```

---

## Brand Direction Prompts

Before using this template, answer:

1. **Who lands here?** Developer? Marketer? Founder? Their skepticism shapes the tone.
2. **What's the ONE action?** Sign up? Book demo? Join waitlist?
3. **What emotion?** Urgency? Relief? Excitement? Curiosity?
4. **What makes it memorable?** The signature element.

---

## Section Blueprints

### 1. Hero

```tsx
<section className="min-h-screen flex items-center justify-center px-6">
  <div className="max-w-4xl mx-auto text-center">
    {/* Eyebrow — optional status badge */}
    <div className="mb-6">
      <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-brand/10 text-brand text-sm font-medium">
        <span className="w-2 h-2 rounded-full bg-brand animate-pulse" />
        Now in public beta
      </span>
    </div>

    {/* Headline — bold, specific */}
    <h1 className="text-[clamp(2.5rem,8vw,5rem)] font-display font-black tracking-tight leading-[0.9] text-ink mb-6">
      [Specific outcome]
      <br />
      <span className="text-brand">[in less time/effort]</span>
    </h1>

    {/* Subheadline — expand on promise */}
    <p className="text-xl md:text-2xl text-ink-muted max-w-2xl mx-auto mb-10">
      [One sentence that explains what this does and who it's for]
    </p>

    {/* CTAs */}
    <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
      <button className="w-full sm:w-auto px-8 py-4 bg-brand text-white font-semibold rounded-full">
        [Primary action verb]
      </button>
      <button className="w-full sm:w-auto px-8 py-4 border border-edge text-ink font-medium rounded-full">
        [Secondary — watch demo, learn more]
      </button>
    </div>

    {/* Micro social proof */}
    <div className="mt-12 flex items-center justify-center gap-4 text-sm text-ink-muted">
      <div className="flex -space-x-2">
        {/* Avatar stack */}
      </div>
      <span>Trusted by X+ [relevant noun]</span>
    </div>
  </div>
</section>
```

**Customize:**
- Headline should state the specific outcome, not generic "better/faster"
- Use a number in social proof (specificity builds trust)

### 2. Social Proof Strip

```tsx
<section className="py-12 border-y border-edge">
  <div className="max-w-7xl mx-auto px-6">
    <p className="text-center text-sm text-ink-muted mb-8">
      Trusted by teams at
    </p>
    <div className="flex items-center justify-center gap-12 opacity-60">
      {/* 4-6 logos, grayscale */}
    </div>
  </div>
</section>
```

**Customize:**
- Choose logos your target audience recognizes
- Fewer, relevant logos > many random logos

### 3. Problem/Pain Section

```tsx
<section className="py-20 md:py-28">
  <div className="max-w-3xl mx-auto px-6 text-center">
    <h2 className="text-[clamp(1.75rem,4vw,2.5rem)] font-display font-bold text-ink mb-6">
      [Pain point as a question or statement]
    </h2>
    <p className="text-lg text-ink-muted leading-relaxed">
      [Describe the problem your audience faces. Be specific. Show you understand.]
    </p>
  </div>
</section>
```

**Customize:**
- Speak to a specific pain, not generic "it's hard to..."
- Use language your audience uses

### 4. Solution — Key Features

```tsx
<section className="py-20 md:py-28 bg-surface-alt">
  <div className="max-w-7xl mx-auto px-6">
    <div className="max-w-3xl mb-16">
      <h2 className="text-[clamp(2rem,5vw,3rem)] font-display font-bold text-ink mb-4">
        [How we solve it]
      </h2>
      <p className="text-lg text-ink-muted">
        [Brief explanation of approach]
      </p>
    </div>

    {/* 3 features — alternating layout */}
    <div className="space-y-20">
      {features.map((feature, i) => (
        <div className={`grid grid-cols-1 lg:grid-cols-2 gap-12 items-center ${i % 2 === 1 ? 'lg:grid-flow-dense' : ''}`}>
          <div className={i % 2 === 1 ? 'lg:col-start-2' : ''}>
            <h3 className="text-2xl font-bold text-ink mb-4">{feature.title}</h3>
            <p className="text-ink-muted">{feature.description}</p>
          </div>
          <div className={i % 2 === 1 ? 'lg:col-start-1' : ''}>
            {/* Screenshot or illustration */}
          </div>
        </div>
      ))}
    </div>
  </div>
</section>
```

**Customize:**
- Show actual product screenshots, not generic illustrations
- Each feature should solve a specific part of the problem

### 5. Deep Dive — Feature Showcase

```tsx
<section className="py-20 md:py-28">
  <div className="max-w-7xl mx-auto px-6">
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
      <div>
        <span className="text-sm font-medium text-brand uppercase tracking-wide">
          [Feature category]
        </span>
        <h2 className="mt-4 text-[clamp(2rem,4vw,3rem)] font-display font-bold text-ink mb-6">
          [Headline for the main feature]
        </h2>
        <p className="text-lg text-ink-muted mb-8">
          [Detailed explanation of how this feature works and why it matters]
        </p>
        <ul className="space-y-4">
          {/* Benefit list with checkmarks */}
        </ul>
      </div>
      <div>
        {/* Large product visual — could be interactive */}
      </div>
    </div>
  </div>
</section>
```

**Customize:**
- Pick your strongest differentiator
- Show the feature in action, not just describe it

### 6. Testimonials

```tsx
<section className="py-20 md:py-28 bg-surface-alt">
  <div className="max-w-7xl mx-auto px-6">
    <h2 className="text-center text-[clamp(1.75rem,4vw,2.5rem)] font-display font-bold text-ink mb-12">
      What our customers say
    </h2>

    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {/* Testimonial cards */}
    </div>
  </div>
</section>
```

**Customize:**
- Use real names, real companies, real photos
- Include specific results when possible ("saved 10 hours/week")

### 7. Pricing (Optional)

```tsx
<section className="py-20 md:py-28">
  <div className="max-w-5xl mx-auto px-6">
    <div className="text-center mb-12">
      <h2 className="text-[clamp(2rem,5vw,3rem)] font-display font-bold text-ink mb-4">
        Simple, transparent pricing
      </h2>
      <p className="text-lg text-ink-muted">
        [One line about pricing philosophy]
      </p>
    </div>

    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
      {/* Pricing cards — highlight recommended tier */}
    </div>
  </div>
</section>
```

**Customize:**
- Highlight the tier you want most people to choose
- Include what's in each tier, not just features

### 8. Final CTA

```tsx
<section className="py-24 md:py-32">
  <div className="max-w-4xl mx-auto px-6 text-center">
    <h2 className="text-[clamp(2rem,5vw,3.5rem)] font-display font-black text-ink mb-6">
      [Restate the main promise]
    </h2>
    <p className="text-xl text-ink-muted mb-10 max-w-2xl mx-auto">
      [Final persuasion — why act now]
    </p>
    <button className="px-10 py-5 bg-brand text-white text-lg font-semibold rounded-full">
      [Primary action — same as hero]
    </button>
    <div className="mt-8 flex items-center justify-center gap-6 text-sm text-ink-muted">
      {/* Trust signals: No CC required, Free trial, Cancel anytime */}
    </div>
  </div>
</section>
```

---

## Common Customizations

### For Developer Tools
- Add code snippets in features
- Show terminal/CLI examples
- Use monospace accents
- Darker color palette acceptable

### For Marketing/Sales Tools
- Emphasize ROI and metrics
- Show dashboards and reports
- Include case study snippets
- Brighter, more energetic palette

### For Productivity Tools
- Focus on time saved
- Show before/after workflows
- Include integrations section
- Clean, calming palette

---

## Anti-Patterns to Avoid

Even with this template, watch for:

- **Generic headlines** — "The best way to..." → Be specific
- **Vague benefits** — "Save time" → "Cut deployment time by 80%"
- **Stock visuals** — Use real product screenshots
- **Competing CTAs** — One primary action per section
- **Missing signature** — Add something memorable

---

## Next Steps

1. Answer the brand direction prompts
2. Fill in the section blueprints with your content
3. Identify your signature element
4. Run the craft checks before launching

This template is a starting point. The goal is to make it unrecognizable as a template.
