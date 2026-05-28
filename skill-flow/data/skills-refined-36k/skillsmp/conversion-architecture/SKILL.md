---
name: conversion-architecture
description: |
  Frameworks and principles for designing website architecture that converts. Covers page hierarchy, user flow design, conversion goal setting, and awareness-based structure.
  
  USE THIS SKILL WHEN:
  - Designing site structure or information architecture
  - Mapping user flows to pages
  - Setting page-level conversion goals
  - Deciding what pages a site needs
  - Planning navigation and hierarchy
  - User mentions "sitemap", "site structure", "IA", "information architecture"
  
  PROVIDES: Frameworks, templates, and decision guides for conversion-focused site architecture
allowed-tools: Read, Grep, Glob
---

# Conversion Architecture Skill

## Overview

Site architecture isn't about organizing content—it's about orchestrating conversion. Every page exists to move a visitor closer to becoming a customer. This skill provides the frameworks for designing structures that convert.

## Core Principle: Architecture IS Strategy

A sitemap is not a navigation menu. It's a conversion plan that answers:
- What pages does each audience need?
- In what order should they experience them?
- What's the ONE job of each page?
- How do we minimize friction to conversion?

---

## Framework 1: The Page Purpose Hierarchy

Every page must fit one of these roles:

```
PAGE PURPOSE HIERARCHY

┌─────────────────────────────────────────────────────────────┐
│ TIER 1: CONVERSION PAGES                                     │
│ Purpose: Direct conversion action                            │
│ Examples: Product pages, pricing, signup, contact            │
│ Goal: Convert visitor to lead/customer                       │
│ Rule: Maximum 1 click from homepage                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ TIER 2: PERSUASION PAGES                                     │
│ Purpose: Build trust, handle objections                      │
│ Examples: Case studies, testimonials, about, how it works    │
│ Goal: Move visitor from skeptical to convinced               │
│ Rule: Maximum 2 clicks from homepage                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ TIER 3: EDUCATION PAGES                                      │
│ Purpose: Attract and nurture                                 │
│ Examples: Blog, resources, guides, FAQ                       │
│ Goal: Move visitor from unaware to problem/solution-aware    │
│ Rule: Must have clear path to Tier 1 or 2                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ TIER 4: UTILITY PAGES                                        │
│ Purpose: Support and legal                                   │
│ Examples: Privacy, terms, sitemap, 404                       │
│ Goal: Required functionality, not conversion                 │
│ Rule: Accessible but not prominent                          │
└─────────────────────────────────────────────────────────────┘
```

**Decision Rule:** If a page doesn't fit a tier, question whether it should exist.

---

## Framework 2: Awareness-Based Architecture

Different awareness levels need different pages and paths:

### Unaware Visitors
*Don't know they have a problem*

**Need:**
- Educational content that reveals the problem
- Blog posts, guides, social content
- Soft entry points, no sales pressure

**Page Types:**
- Blog articles
- Educational resources
- Quizzes ("Is [problem] affecting you?")
- Industry reports

**Path:** Education → Problem awareness → Solution awareness

---

### Problem-Aware Visitors
*Know the problem, don't know solutions exist*

**Need:**
- Problem validation ("You're not alone")
- Introduction to solution category
- Hope that solutions exist

**Page Types:**
- Problem-focused landing pages
- "How to solve [problem]" guides
- Comparison of approaches
- Success stories (before/after)

**Path:** Problem pages → Solution introduction → Product

---

### Solution-Aware Visitors
*Know solutions exist, comparing options*

**Need:**
- Differentiation (why you vs. alternatives)
- Proof that your approach works
- Clear explanation of your method

**Page Types:**
- Comparison pages
- "Our approach" / methodology pages
- Case studies
- Founder story / "why we built this"

**Path:** Differentiation → Proof → Product

---

### Product-Aware Visitors
*Know your product, not yet convinced*

**Need:**
- Objection handling
- Social proof and validation
- Details and specifics
- Risk reduction

**Page Types:**
- Detailed product/service pages
- Pricing with value justification
- Reviews and testimonials
- FAQ / objection handling
- Demo or trial

**Path:** Product details → Objection handling → Convert

---

### Most-Aware Visitors
*Ready to buy, need the right offer*

**Need:**
- Clear, frictionless purchase path
- Compelling offer
- Urgency (if appropriate)
- Easy next step

**Page Types:**
- Streamlined checkout
- Pricing page
- Special offers
- "Get started" pages

**Path:** Direct to conversion

---

## Framework 3: The One-Job Rule

Every page should have ONE primary job. If you can't state it in one sentence, the page is trying to do too much.

### Page Job Statement Template

```
This page's job is to [ACTION] [AUDIENCE] by [METHOD].
```

**Examples:**

| Page | Job Statement |
|------|---------------|
| Homepage | Convert product-aware visitors by orienting them and routing to relevant path |
| Pricing | Convert ready-to-buy visitors by making decision easy and reducing friction |
| Case Study | Move skeptical visitors to convinced by proving results with specific evidence |
| Blog Post | Move unaware visitors to problem-aware by educating about the problem |
| About | Build trust with evaluating visitors by humanizing the brand |

### When a Page Has Multiple Jobs

If a page needs to serve multiple purposes:

1. **Prioritize:** Make ONE job primary, others secondary
2. **Segment:** Can you split into multiple pages?
3. **Progressive Disclosure:** Reveal secondary content as user scrolls/clicks
4. **Path Splitting:** Route different visitors to different pages

---

## Framework 4: User Flow Design

A user flow maps the path from entry to conversion.

### Flow Components

```
ENTRY POINT → PAGE 1 → PAGE 2 → ... → CONVERSION
     ↓           ↓         ↓              ↓
[How they    [What they  [What they   [Action
 arrive]      think]      do next]     taken]
```

### Flow Design Template

```markdown
## Flow: [Name]

**Target Audience:** [ICP segment]
**Entry Point:** [How they arrive - search, ad, referral, etc.]
**Target Conversion:** [What action we want]

### Steps

1. **[Page Name]**
   - User thinks: "[Their mental state]"
   - User needs: [Information/proof/reassurance]
   - They click: [CTA or link]

2. **[Page Name]**
   - User thinks: "[Their mental state]"
   - User needs: [Information/proof/reassurance]
   - They click: [CTA or link]

3. **[Conversion Page]**
   - User thinks: "[Their mental state]"
   - User needs: [Final reassurance]
   - They convert: [Action]

### Friction Points
- [Where might they drop off?]
- [What might make them hesitate?]

### Mitigation
- [How we address friction point 1]
- [How we address friction point 2]

### Alternate Paths
- If not ready: [Nurture path - email signup, resource download]
- If wrong fit: [Exit path - redirect to right place]
```

### Common Flow Patterns

**The Direct Path (Most Aware)**
```
Homepage → Pricing → Signup
```

**The Trust-Building Path (Product Aware)**
```
Homepage → Product Page → Case Study → Pricing → Signup
```

**The Education Path (Problem Aware)**
```
Blog Post → Related Resource → Product Overview → Demo Request
```

**The Comparison Path (Solution Aware)**
```
Comparison Page → Our Approach → Case Study → Contact
```

---

## Framework 5: Navigation Architecture

Navigation is wayfinding, not a sitemap dump.

### Primary Navigation Rules

1. **Maximum 7 items** (5-6 preferred)
2. **Conversion pages always accessible** (Pricing, Contact, CTA)
3. **User language, not company jargon**
4. **Most important = leftmost** (except CTA which goes right)
5. **Dropdown menus only when necessary**

### Navigation Hierarchy

```
PRIMARY NAV
├── High-traffic pages
├── Key persuasion pages  
├── Conversion entry points
└── CTA button (rightmost)

SECONDARY NAV (header utility)
├── Login
├── Search
└── Support/Help

FOOTER NAV
├── All primary nav items
├── Legal/utility pages
├── Secondary content
└── Social links
```

### Mobile Navigation Considerations

- Hamburger menu acceptable, but CTA should remain visible
- Most common actions = fewest taps
- Search should be easily accessible
- Consider bottom navigation for apps/PWAs

---

## Framework 6: Page Hierarchy Principles

How you organize pages signals importance.

### Depth = Importance (Inverse)

```
/ (Homepage)              ← Most important
/products/                ← Very important  
/products/category/       ← Important
/products/category/item/  ← Specific but findable
/blog/2024/post-slug/     ← Discoverable via search
```

### URL Structure Best Practices

| Pattern | Good For | Example |
|---------|----------|---------|
| `/page-name` | Core pages | `/pricing`, `/about` |
| `/category/page` | Organized sections | `/products/skincare` |
| `/type/slug` | Content | `/blog/post-title` |
| `/tool/action` | Apps | `/app/dashboard` |

### Avoid

- Deep nesting (`/a/b/c/d/e/page`)
- IDs in URLs (`/products/12345`)
- Dates in non-time-sensitive URLs
- Duplicate content at multiple URLs

---

## Framework 7: Conversion Points Placement

Where and how often to present conversion opportunities.

### The Rhythm of CTAs

```
PAGE STRUCTURE WITH CTA RHYTHM

┌─────────────────────────────────────────┐
│ HERO                                     │
│ Primary value prop + Primary CTA         │  ← First CTA
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│ SECTION 1                                │
│ Supporting content (no CTA yet)          │  ← Build value first
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│ SECTION 2                                │
│ Proof/benefits + Contextual CTA          │  ← Second CTA (earned)
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│ SECTION 3                                │
│ Deeper content                           │  ← More value
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│ SECTION 4                                │
│ Social proof + CTA                       │  ← Third CTA (after proof)
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│ FINAL SECTION                            │
│ Clear CTA with urgency/offer             │  ← Final CTA (strong)
└─────────────────────────────────────────┘
```

### CTA Placement Rules

1. **Always above the fold** — Don't make them scroll to take action
2. **After proof** — CTA following testimonials/results converts better
3. **Repeated but not annoying** — 3-4 CTAs per long page is fine
4. **Varied language** — Don't repeat identical CTA text
5. **Secondary option available** — For those not ready for primary action

---

## Decision Guide: What Pages Do You Need?

### Required for Every Site

| Page | Why Required |
|------|--------------|
| Homepage | Orientation, routing, trust building |
| About | Trust building, human connection |
| Contact | Lead capture, accessibility |
| Privacy Policy | Legal requirement |

### Required for Most Sites

| Page | Why Usually Needed |
|------|-------------------|
| Product/Service pages | Explain and sell offering |
| Pricing | Reduce friction, handle objections |
| Testimonials/Results | Social proof for conversion |

### Conditional Pages

| Page | Include If... |
|------|---------------|
| Case Studies | B2B, high-consideration purchase |
| Blog | SEO strategy, thought leadership |
| FAQ | Common objections exist |
| Comparison | Competitors are well-known |
| Demo/Trial | Product is complex |
| Careers | Actively hiring |
| Press | Newsworthy company |
| Partners | Partner ecosystem matters |

### Question Every Other Page

For any page not listed above, ask:
1. What job does this page do?
2. Which ICP segment needs it?
3. What happens if we don't have it?
4. Can this content live elsewhere?

---

## Common Architecture Mistakes

### Mistake 1: Org-Chart Structure
**Wrong:** Pages mirror internal departments
**Right:** Pages mirror user needs and questions

### Mistake 2: Everything in Primary Nav
**Wrong:** 12 items in main navigation
**Right:** 5-7 items covering key paths

### Mistake 3: Burying Conversion
**Wrong:** "Contact" hidden in footer only
**Right:** CTA visible on every page

### Mistake 4: One-Size-Fits-All
**Wrong:** Same path for all visitors
**Right:** Different paths for different awareness levels

### Mistake 5: Feature-Organized Products
**Wrong:** `/features/reporting`, `/features/automation`
**Right:** `/solutions/sales-teams`, `/solutions/marketing`

### Mistake 6: Dead-End Pages
**Wrong:** Blog posts with no next step
**Right:** Every page leads somewhere

---

## References

For additional frameworks and examples, see:
- `references/sitemap-templates.md` - Example sitemaps by business type
- `references/page-types-guide.md` - Detailed guide to common page types
- `references/flow-examples.md` - Sample user flow documentation