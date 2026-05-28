---
name: jikime-marketing-copywriting
description: Conversion copywriting specialist for writing compelling marketing copy including headlines, CTAs, landing pages, and product descriptions.
version: 1.0.0
tags: ["marketing", "copywriting", "content", "headlines", "cta"]
triggers:
  keywords: ["write copy", "copywriting", "headline", "CTA", "rewrite", "marketing copy", "카피라이팅", "헤드라인", "문구"]
  phases: ["plan", "run"]
  agents: ["frontend", "documenter"]
  languages: []
# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~6000
user-invocable: true
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
  - TodoWrite
---

# Conversion Copywriting

## Quick Reference (30 seconds)

Conversion Copywriting Specialist - Write marketing copy that is clear, compelling, and drives action.

Core Principles:
- **Clarity > Cleverness**: If choosing between clear and creative, choose clear
- **Benefits > Features**: Connect features to customer outcomes
- **Specificity > Vagueness**: "Save 4 hours weekly" beats "Save time"
- **Customer Language**: Mirror how they describe their problems

Key Capabilities:
- Headline formula library (10+ patterns)
- Page structure frameworks
- CTA optimization guidelines
- Voice and tone adaptation

---

## Implementation Guide (5 minutes)

### Pre-Writing Context Gathering

Before writing, gather:

| Category | Questions |
|----------|-----------|
| **Page Purpose** | What type? What's the ONE primary action? |
| **Audience** | Who? What problem? What objections? |
| **Product** | What's different? Key transformation? |
| **Context** | Traffic source? Prior messaging exposure? |

### Core Writing Principles

```
┌─────────────────────────────────────────────────────────────────┐
│  WRITING STYLE HIERARCHY                                        │
│                                                                 │
│  1. Simple > Complex      ("Use" not "Utilize")                │
│  2. Specific > Vague      (Numbers, timeframes, details)       │
│  3. Active > Passive      ("We generate" not "Reports are...")  │
│  4. Confident > Qualified (Remove "almost," "very," "really")   │
│  5. Show > Tell           (Describe outcome, not "instantly")   │
│  6. Honest > Sensational  (Never fabricate claims)             │
└─────────────────────────────────────────────────────────────────┘
```

### Headline Formula Library

| Pattern | Template | Example |
|---------|----------|---------|
| **Outcome + Pain** | `{Achieve X} without {Pain Y}` | "Understand user behavior without drowning in numbers" |
| **The Opposite Way** | `The {opposite} way to {outcome}` | "The easiest way to turn passion into income" |
| **Never Again** | `Never {unpleasant event} again` | "Never miss a sales opportunity again" |
| **For Audience** | `{Product type} for {audience}` | "Advanced analytics for Shopify e-commerce" |
| **For + Purpose** | `{Product} for {audience} to {purpose}` | "An online whiteboard for teams to ideate together" |
| **No Need** | `You don't have to {skill} to {outcome}` | "You don't have to be an SEO pro to rank higher" |
| **How Possible** | `{Outcome} by {how product helps}` | "Generate more leads by seeing who visits your site" |
| **Direct Benefit** | `{Key benefit of product}` | "Sound clear in online meetings" |
| **Pain Question** | `{Question about main pain}?` | "Hate returning stuff to Amazon?" |
| **Transform** | `Turn {input} into {outcome}` | "Turn hard-earned sales into repeat customers" |

### Page Structure Framework

```
┌─────────────────────────────────────────────────────────────────┐
│  ABOVE THE FOLD                                                 │
│  ├── Headline (core value proposition)                         │
│  ├── Subheadline (expands, adds specificity)                   │
│  ├── Primary CTA (action + value)                              │
│  └── Supporting Visual (reinforce, not distract)               │
├─────────────────────────────────────────────────────────────────┤
│  SOCIAL PROOF BAR                                               │
│  └── Logos / Key metric / Short testimonial / Star rating      │
├─────────────────────────────────────────────────────────────────┤
│  PROBLEM SECTION                                                │
│  └── Articulate pain better than they can                      │
├─────────────────────────────────────────────────────────────────┤
│  SOLUTION/BENEFITS (3-5 max)                                    │
│  └── Headline + Explanation + Proof point                      │
├─────────────────────────────────────────────────────────────────┤
│  HOW IT WORKS (3-4 steps)                                       │
│  └── Step + Outcome format                                     │
├─────────────────────────────────────────────────────────────────┤
│  DETAILED SOCIAL PROOF                                          │
│  └── Full testimonials with results, names, photos             │
├─────────────────────────────────────────────────────────────────┤
│  OBJECTION HANDLING                                             │
│  └── FAQ / Comparison / Guarantee                              │
├─────────────────────────────────────────────────────────────────┤
│  FINAL CTA                                                      │
│  └── Recap value + CTA + Risk reversal                         │
└─────────────────────────────────────────────────────────────────┘
```

### CTA Copy Guidelines

**CTA Strength Scale:**

| Level | Examples | Issue |
|-------|----------|-------|
| ❌ Weak | Submit, Sign Up, Click Here | No value communicated |
| ⚠️ Medium | Get Started, Learn More | Vague action |
| ✅ Strong | Start Free Trial, Get My Report | Value + ownership |
| ⭐ Best | See Pricing for My Team, Create My First Project | Specific + personal |

**CTA Formula:**
```
[Action Verb] + [What They Get] + [Qualifier]

Examples:
- "Start My Free Trial"
- "Get the Complete Checklist"
- "See Pricing for Teams"
- "Download the 2024 Guide"
```

### Landing Page Section Variety

**Weak Structure (Feature-Heavy):**
```
Hero → Feature 1 → Feature 2 → Feature 3 → CTA
```

**Strong Structure (Varied):**
```
Hero → Social Proof Bar → Problem Section → How It Works →
Key Benefits (2-3) → Testimonial → Use Cases → Comparison →
Case Study Snippet → FAQ → Final CTA + Guarantee
```

**Section Types to Mix:**

| Section | Purpose |
|---------|---------|
| How It Works | Reduce perceived complexity |
| Comparison | Show advantage over alternatives |
| Founder Story | Create emotional connection |
| Use Cases | Help visitors self-identify |
| Personas | "Built for marketers" |
| Stats | "10,000+ customers" |
| Demo/Video | Show product in action |
| Integrations | "Works with your stack" |
| Guarantee | Reduce risk |

---

## Page-Specific Guidance

### Homepage Copy

| Challenge | Solution |
|-----------|----------|
| Multiple audiences | Lead with broadest value prop |
| Different intents | Clear paths for each visitor type |
| Not too generic | Specific enough to resonate |

### Landing Page Copy

| Requirement | Implementation |
|-------------|----------------|
| Message match | Headline = Ad copy |
| Single focus | One CTA, remove nav |
| Complete story | All info on one page |

### Pricing Page Copy

| Element | Copy Approach |
|---------|--------------|
| Tier names | Descriptive, not creative |
| Feature lists | Benefits, not just features |
| Recommended plan | "Most popular" or "Best for..." |
| "Which plan?" anxiety | Use case descriptions |

### Feature Page Copy

| Section | Copy Focus |
|---------|------------|
| Hero | Feature → Benefit → Outcome |
| Use cases | "Perfect for when you need to..." |
| Differentiation | "Unlike [competitor], we..." |

---

## Voice and Tone Framework

### Formality Spectrum

| Level | Characteristics | Example |
|-------|-----------------|---------|
| **Casual** | Conversational, contractions, humor | "Let's fix that mess" |
| **Professional** | Friendly but polished | "We'll help you organize" |
| **Formal** | Enterprise, no contractions | "We provide organizational solutions" |

### Brand Personality Dimensions

| Dimension | Slider |
|-----------|--------|
| Playful ←→ Serious | Match audience expectations |
| Bold ←→ Understated | Reflect brand confidence |
| Technical ←→ Accessible | Match audience expertise |

### Consistency Rules

- Headlines: Can be bolder
- Body copy: Must be clearer
- CTAs: Always action-oriented
- Maintain voice throughout

---

## Output Format

When writing copy, provide:

```markdown
## Page Copy

### Headline
[Primary headline]

### Subheadline
[Supporting subheadline]

### Primary CTA
[Button copy]

### [Section Name]
[Section copy]

---

## Annotations
- **[Element]**: [Why this choice works]

## Alternatives
**Headline Options:**
- Option A: [copy] — [rationale]
- Option B: [copy] — [rationale]
- Option C: [copy] — [rationale]

**CTA Options:**
- Option A: [copy] — [rationale]
- Option B: [copy] — [rationale]

## Meta Content
- **Page Title**: [SEO-optimized title]
- **Meta Description**: [150-160 chars]
```

---

## Quality Checklist

```
Copy Quality Validation:
- [ ] Value proposition clear in headline
- [ ] Benefits, not just features
- [ ] Specific numbers and timeframes where possible
- [ ] No jargon (or jargon audience uses)
- [ ] Active voice throughout
- [ ] CTA communicates value
- [ ] Social proof supports claims
- [ ] Objections addressed
- [ ] One idea per section
- [ ] Scans well (heading hierarchy)
```

---

## Works Well With

Skills:
- `jikime-marketing-page-cro` - For page structure optimization
- `jikime-marketing-psychology` - For persuasion principles
- `jikime-marketing-ab-test` - For testing copy variations

---

Version: 1.0.0
Last Updated: 2026-01-25
Attribution: Enhanced from marketingskills by Corey Haines (MIT License)
