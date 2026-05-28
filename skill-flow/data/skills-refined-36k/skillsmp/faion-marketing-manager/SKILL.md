---
name: faion-marketing-manager
description: "Marketing Manager role: GTM strategy, landing pages, copywriting, SEO/SEM, GEO/AEO, content marketing, social media, email campaigns, ads (Google, Meta), analytics, A/B testing, conversion optimization. 86 methodologies."
user-invocable: false
allowed-tools: Read, Write, Edit, Task, WebSearch, AskUserQuestion, TodoWrite, Glob
---

# Marketing Domain Skill

**Communication: User's language. Content: target audience language.**

## Purpose

Orchestrates all marketing activities from go-to-market strategy to growth experiments. Covers GTM planning, landing pages, content marketing, SEO, paid ads, email marketing, social media, and growth hacking.

## Merged From

| Original Skill | Content |
|----------------|---------|
| faion-gtm-manifest | GTM Manifest from research data |
| faion-landing-page | High-converting landing pages |

---

## Agents

| Agent | Purpose | Modes/Skills |
|-------|---------|--------------|
| faion-landing-agent | Landing page orchestrator | analyze, copy, design |
| faion-content-agent | Content marketing, SEO | faion-analytics-skill |
| faion-email-agent | Email marketing campaigns | - |
| faion-social-agent | Social media marketing | - |
| faion-growth-agent | Growth hacking, experiments | faion-analytics-skill |
| faion-ads-agent | Paid advertising | faion-meta-ads-skill, faion-google-ads-skill |

**Landing Agent Mode Mapping:**
| Mode | Replaces | Purpose |
|------|----------|---------|
| analyze | faion-landing-agent (mode: analyze) | Conversion audit, A/B tests |
| copy | faion-landing-agent (mode: copy) | AIDA/PAS copy, headlines |
| design | faion-landing-agent (mode: design) | HTML/Tailwind, mobile-first |

---

## References

| Reference | Content | Lines |
|-----------|---------|-------|
| [ref-methodologies-detail.md](ref-methodologies-detail.md) | Detailed methodology frameworks (72) | ~1200 |
| [ref-seo.md](ref-seo.md) | Technical SEO, AEO, Core Web Vitals | ~560 |
| [ref-google-ads.md](ref-google-ads.md) | Search, Display, Performance Max | ~1470 |
| [ref-meta-ads.md](ref-meta-ads.md) | Facebook, Instagram ads | ~1100 |
| [ref-image-generation.md](ref-image-generation.md) | DALL-E, Midjourney, Flux | ~1300 |
| [ref-video-generation.md](ref-video-generation.md) | Sora, Runway, Pika | ~860 |
| [ref-audio-production.md](ref-audio-production.md) | TTS, voice cloning, podcasts | ~1300 |
| [ref-analytics.md](ref-analytics.md) | Mixpanel, PostHog, GA4 | ~1470 |

**Total:** ~9,500 lines of reference material

---

## Decision Trees

### Main Decision Tree: What Marketing Goal?

```
START: What is your marketing goal?
│
├── LAUNCH PRODUCT → GTM Strategy Category
│   ├── New product? → gtm-strategy, launch-plan
│   ├── Define ICP? → icp-definition, value-proposition-design
│   ├── Pricing? → pricing-strategy
│   └── Sales model? → sales-model-selection
│
├── ACQUIRE USERS → Acquisition Category
│   ├── Budget available?
│   │   ├── YES → Paid Advertising
│   │   │   ├── B2B? → LinkedIn Ads, Google Search
│   │   │   ├── B2C? → Meta Ads, TikTok
│   │   │   └── Local? → Google Local, Meta
│   │   └── NO → Organic Channels
│   │       ├── Long-term? → SEO, Content Marketing
│   │       ├── Short-term? → Social Media, Community
│   │       └── Viral potential? → Referral Programs
│   └── Channel selection → channel-strategy
│
├── CONVERT VISITORS → Conversion Category
│   ├── Landing page? → Landing Page methodologies
│   │   ├── Copy needed? → aida-framework, pas-framework
│   │   ├── Design needed? → above-the-fold-design, mobile-first-design
│   │   └── Optimization? → ab-testing-framework, heat-map-analysis
│   ├── Email capture? → welcome-sequence, lead-nurture
│   └── Low conversion? → cta-optimization, form-optimization
│
├── RETAIN USERS → Retention Category
│   ├── Email marketing → Email Marketing methodologies
│   │   ├── New subscribers? → welcome-sequence
│   │   ├── Inactive users? → re-engagement-campaigns
│   │   └── Engagement low? → email-segmentation
│   ├── Community → community-building, social-listening
│   └── Product-led? → retention-loops, activation-rate
│
├── GROW REVENUE → Growth Category
│   ├── Referrals? → referral-program-design, viral-coefficient
│   ├── Upsell? → customer-lifecycle-marketing
│   ├── Experiments? → growth-experiment-framework, ab-testing-framework
│   └── Track metrics? → aarrr-funnel-analysis, north-star-metric
│
└── ANALYZE PERFORMANCE → Analytics Category
    ├── Attribution? → attribution-modeling
    ├── Funnel leaks? → funnel-optimization, cohort-analysis
    └── Reporting? → marketing-analytics-stack, paid-media-reporting
```

### Decision Tree: Channel Selection

```
What audience are you targeting?
│
├── B2B DECISION MAKERS
│   ├── Enterprise (>1000 employees)
│   │   ├── Primary: LinkedIn Ads, Google Search
│   │   ├── Secondary: Content Marketing, Webinars
│   │   └── Methodologies: linkedin-content-strategy, google-ads-structure
│   └── SMB (<1000 employees)
│       ├── Primary: Google Search, Meta Ads
│       ├── Secondary: Email, Content
│       └── Methodologies: email-marketing, content-pillar-strategy
│
├── B2C CONSUMERS
│   ├── Age 18-34
│   │   ├── Primary: TikTok, Instagram, YouTube
│   │   ├── Secondary: Influencer Marketing
│   │   └── Methodologies: tiktok-marketing, instagram-organic-growth
│   └── Age 35+
│       ├── Primary: Facebook, Google, Email
│       ├── Secondary: YouTube
│       └── Methodologies: meta-ads-structure, email-automation-flows
│
├── DEVELOPERS/TECHNICAL
│   ├── Primary: Twitter/X, Reddit, Hacker News
│   ├── Secondary: Dev.to, GitHub, Content
│   └── Methodologies: twitter-x-growth, hacker-news-launch, reddit-marketing
│
└── LOCAL/REGIONAL
    ├── Primary: Google Local, Meta Local
    ├── Secondary: Community, Partnerships
    └── Methodologies: google-ads-structure, community-building
```

### Decision Tree: Content Type Selection

```
What content goal?
│
├── AWARENESS (Top of Funnel)
│   ├── SEO play? → Pillar pages, blog posts
│   ├── Social reach? → Short videos, infographics
│   ├── Authority? → Thought leadership, podcasts
│   └── Methodologies: content-pillar-strategy, video-content-strategy
│
├── CONSIDERATION (Middle of Funnel)
│   ├── Comparison content → vs competitors, alternatives
│   ├── How-to guides → Tutorials, walkthroughs
│   ├── Case studies → Customer stories, results
│   └── Methodologies: blog-post-template, long-form-content-structure
│
├── DECISION (Bottom of Funnel)
│   ├── Product demos → Video, interactive
│   ├── Testimonials → Video, written
│   ├── Free trials → Landing pages
│   └── Methodologies: landing-page-checklist, social-proof-strategy
│
└── RETENTION (Post-Purchase)
    ├── Onboarding → Email sequences, guides
    ├── Education → Webinars, courses
    ├── Community → Forums, groups
    └── Methodologies: welcome-sequence, customer-lifecycle-marketing
```

### Decision Tree: Landing Page Optimization

```
What's the conversion problem?
│
├── LOW TRAFFIC → Not a landing page problem
│   └── Go to: Acquisition Decision Tree
│
├── HIGH BOUNCE RATE (>70%)
│   ├── Check: Page speed → page-speed-optimization
│   ├── Check: Message match → landing-page-ad-alignment
│   ├── Check: Above fold → above-the-fold-design
│   └── Check: Mobile → mobile-first-design
│
├── LOW CLICK-THROUGH
│   ├── CTA not visible? → cta-optimization
│   ├── Copy weak? → aida-framework, pas-framework
│   ├── No urgency? → CTA copy formulas
│   └── Too many options? → Single CTA focus
│
├── FORM ABANDONMENT
│   ├── Too many fields? → form-optimization
│   ├── Trust issues? → social-proof-strategy
│   ├── Unclear value? → value-proposition-design
│   └── Technical issues? → Inline validation
│
└── NOT SURE
    ├── Run heat maps → heat-map-analysis
    ├── A/B test → ab-testing-framework
    └── User testing → Direct feedback
```

### Decision Tree: Email Strategy

```
What email need?
│
├── NEW SUBSCRIBER
│   └── welcome-sequence (5 emails over 7 days)
│
├── LEAD NURTURING
│   ├── Short sales cycle (<7 days) → 3-email sequence
│   ├── Long sales cycle (>30 days) → nurture-sequence (5+ weeks)
│   └── Methodology: nurture-sequence, email-segmentation
│
├── INACTIVE USER
│   ├── 30 days inactive → re-engagement-campaigns
│   ├── 90+ days → Last chance + unsubscribe
│   └── Methodology: re-engagement-campaigns
│
├── CUSTOMER
│   ├── Onboarding → Product education series
│   ├── Upsell → Feature highlight emails
│   ├── Advocacy → Referral requests
│   └── Methodology: transactional-email-optimization
│
└── NEWSLETTER
    ├── Frequency: Weekly or bi-weekly
    ├── Format: 80% value, 20% promo
    └── Methodology: newsletter-strategy
```

---

## Methodology Categories (86 total)

### Category: GTM Strategy (12)

**When to use:** Launching new product, entering new market, pivoting positioning.

| Methodology | Problem | Agent |
|-------------|---------|-------|
| executive-summary | No GTM overview | faion-content-agent |
| market-context-analysis | GTM not grounded | faion-market-researcher-agent |
| icp-definition | Target unclear | faion-persona-builder-agent |
| value-proposition-design | Unclear differentiation | faion-content-agent |
| positioning-statement | Inconsistent positioning | faion-content-agent |
| messaging-framework | Inconsistent messaging | faion-landing-agent (copy) |
| pricing-strategy | Pricing misaligned | faion-pricing-researcher-agent |
| sales-model-selection | Wrong sales approach | faion-growth-agent |
| channel-strategy | Scattered efforts | faion-growth-agent |
| launch-plan | Uncoordinated launch | faion-growth-agent |
| success-metrics-definition | No success criteria | faion-growth-agent |
| risk-mitigation | Unidentified risks | faion-growth-agent |

### Category: Landing Page (12)

**When to use:** Creating/optimizing landing pages, improving conversion rates.

| Methodology | Problem | Agent |
|-------------|---------|-------|
| aida-framework | Copy doesn't convert | faion-landing-agent (copy) |
| pas-framework | Not addressing pain | faion-landing-agent (copy) |
| above-the-fold-design | No clear value prop | faion-landing-agent (design) |
| social-proof-strategy | No credibility | faion-landing-agent (design) |
| cta-optimization | Low CTR | faion-landing-agent (analyze) |
| mobile-first-design | Desktop-only | faion-landing-agent (design) |
| form-optimization | Form abandonment | faion-landing-agent (analyze) |
| page-speed-optimization | Slow load | faion-landing-agent (design) |
| conversion-rate-benchmarks | No baseline | faion-landing-agent (analyze) |
| ab-testing-framework | No systematic testing | faion-landing-agent (analyze) |
| heat-map-analysis | Unknown behavior | faion-landing-agent (analyze) |
| landing-page-checklist | Missing elements | faion-landing-agent (analyze) |

### Category: Email Marketing (12)

**When to use:** Lead nurturing, customer retention, newsletter strategy.

| Methodology | Problem | Agent |
|-------------|---------|-------|
| welcome-sequence | Poor first impression | faion-email-agent |
| nurture-sequence | Leads going cold | faion-email-agent |
| email-copywriting-formula | Low open/click rates | faion-email-agent |
| subject-line-formulas | Emails not opened | faion-email-agent |
| email-segmentation | Generic messaging | faion-email-agent |
| email-automation-flows | Manual work | faion-email-agent |
| newsletter-strategy | Inconsistent comm | faion-email-agent |
| email-deliverability | Going to spam | faion-email-agent |
| email-ab-testing | No optimization | faion-email-agent |
| email-metrics-benchmarks | Unknown performance | faion-email-agent |
| re-engagement-campaigns | Inactive subscribers | faion-email-agent |
| transactional-email-optimization | Underutilized | faion-email-agent |

### Category: Growth & Operations (6)

**When to use:** Scaling, experimentation, lifecycle marketing.

| Methodology | Problem | Agent |
|-------------|---------|-------|
| aarrr-funnel-analysis | Unknown leaks | faion-growth-agent |
| growth-experiment-framework | Random efforts | faion-growth-agent |
| referral-program-design | No organic growth | faion-growth-agent |
| customer-lifecycle-marketing | Same messaging | faion-growth-agent |
| competitive-intelligence | Unaware of competitors | faion-market-researcher-agent |
| marketing-analytics-stack | No data infrastructure | faion-analytics-skill |

---

## Workflows

### Workflow 1: GTM Manifest Creation

```
Read product research → AskUserQuestion (sales model, timeline) → Generate 12 sections → Combine into gtm-manifest-full.md
```

**Prerequisites:** Completed research in `product_docs/`:
- market-research.md
- competitive-analysis.md
- user-personas.md
- pricing-research.md

**Output:**
```
product_docs/gtm-manifest/
├── 01-executive-summary.md
├── 02-market-context.md
├── 03-icp.md
├── 04-value-proposition.md
├── 05-positioning.md
├── 06-messaging-framework.md
├── 07-pricing-packaging.md
├── 08-sales-model.md
├── 09-marketing-channels.md
├── 10-launch-plan.md
├── 11-success-metrics.md
├── 12-risks-mitigations.md
└── gtm-manifest-full.md
```

### Workflow 2: Landing Page Creation

```
Discovery → Copy (AIDA/PAS) → Design → Implementation → Analysis
```

### Workflow 3: Content Marketing

```
Keyword Research → Content Plan → Creation → Optimization → Distribution
```

### Workflow 4: Growth Experiments

```
Hypothesis → Experiment Design → Run → Analyze → Learn → Iterate
```

---

## Quick Reference

### Copy Frameworks

| Framework | When to Use |
|-----------|-------------|
| AIDA | General conversion copy |
| PAS | Aware audience with known pain |
| BAB | Transformation stories |
| FAB | Feature-focused products |

### Key Metrics by Stage

| Funnel Stage | Primary Metric | Target |
|--------------|----------------|--------|
| Awareness | Impressions, Reach | - |
| Acquisition | CAC, CPC | Industry avg |
| Activation | Activation Rate | 40%+ |
| Retention | Churn, DAU/MAU | <5% churn |
| Revenue | LTV, ARPU | LTV:CAC > 3:1 |
| Referral | Viral coefficient | K > 0.5 |

### Platform Quick Guide

| Platform | Best For | Budget Min |
|----------|----------|------------|
| Google Search | High intent | $30/day |
| Meta (FB/IG) | Awareness, retargeting | $20/day |
| LinkedIn | B2B | $50/day |
| TikTok | Gen Z, viral | $20/day |
| Twitter/X | Tech, developers | $10/day |

---

## Technical Skills Used

| Skill | Purpose |
|-------|---------|
| faion-meta-ads-skill | Meta Ads API |
| faion-google-ads-skill | Google Ads API |
| faion-analytics-skill | GA4, Plausible |

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| faion-researcher | Provides market data for marketing |
| faion-product-manager | Provides product positioning |
| faion-seo-skill | SEO optimization |

---

> **Note:** Full methodology details available in [methodologies-detail.md](references/methodologies-detail.md) and `methodologies/` folder.

---

*Domain Skill v1.1 - Marketing*
*86 Methodologies | 6 Agents*
*Merged from: faion-gtm-manifest, faion-landing-page*
