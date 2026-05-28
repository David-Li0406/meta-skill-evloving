---
name: seo-landing
description: Create landing page specifications with designer-ready wireframes and conversion-focused copywriting. Use when users mention "landing page", ask for help with marketing copy, want to improve an existing page, or explicitly invoke /marketer. Supports both new page creation and analysis/improvement of existing pages.
---

# Landing Page Spec Creator

Create designer-ready landing page specifications with structured wireframes, SEO-aware copy, and implementation guidance.

## Workflow

### 1. Determine Mode

- **New page**: User wants to create a landing page from scratch
- **Improve existing**: User has an existing page (URL or pasted content) to analyze and improve

For existing pages, fetch the URL or accept pasted content, then produce a full replacement spec.

### 2. Discovery (New Pages)

Run structured discovery using AskUserQuestion in small batches (2-3 questions). Push for clarity on vague answers - do not proceed with ambiguity.

**Batch 1 - Core Offering**

- What product/service is this page for?
- Who is the primary target audience?
- What transformation or outcome does the customer achieve?

**Batch 2 - Competitive Context**

- What alternatives exist? Why choose this over them?
- What's the primary objection or hesitation buyers have?
- What proof points exist (testimonials, stats, logos, case studies)?

**Batch 3 - Page Goals**

- What's the single primary action visitors should take?
- What happens after they take that action?
- Any secondary actions to support?

**Batch 4 - Constraints**

- Any brand voice guidelines or tone requirements?
- Required elements (specific features, compliance text, etc.)?
- Known SEO keywords to incorporate?

### 3. Discovery (Existing Pages)

For improvement requests:

- Fetch URL using WebFetch or accept pasted content
- Identify current structure, messaging, and CTA
- Note what's working and what's weak
- Run abbreviated discovery to fill gaps

### 4. Generate Spec

Write spec to `SPEC.md` in project root. Structure:

```markdown
# [Product/Page Name] Landing Page Spec

## Overview

- **Primary Goal**: [Single CTA]
- **Target Audience**: [Who]
- **Core Value Prop**: [One sentence]

## SEO

- **Meta Title**: [60 chars max]
- **Meta Description**: [155 chars max]
- **Primary Keywords**: [2-3 terms]

## Page Structure

### Hero Section

**Purpose**: Capture attention, communicate core value, drive primary CTA
**Above the fold**: Yes

- **Headline**: [Benefit-focused, 6-12 words]
- **Subheadline**: [Expand on headline, address who it's for]
- **Primary CTA**: [Button text + destination]
- **Supporting Visual**: [Description of hero image/video concept]
- **Layout Notes**: [Visual hierarchy guidance]

### [Section Name]

**Purpose**: [Why this section exists]
**Above the fold**: [Yes/No]

- **Section Header**: [Text]
- **Body Content**: [Full copy]
- **Visual Elements**: [What imagery/icons support this]
- **Layout Notes**: [Guidance for designer]

[Continue for each section...]

## Implementation Notes

- **Above-the-fold priorities**: [What must be visible without scrolling]
- **Mobile considerations**: [Key adaptations for mobile]
- **Visual hierarchy**: [What draws the eye first, second, third]
```

## Section Types

Use these section patterns as building blocks. Not all pages need all sections.

**Hero**: Opening section with headline, value prop, primary CTA. Always first.

**Problem/Pain**: Articulate the frustration or challenge the visitor faces. Use their language.

**Solution/How It Works**: Explain what the product does and how it delivers the outcome. 3 steps max if using a process format.

**Benefits**: Outcome-focused (not feature-focused). What changes for the customer?

**Features**: Specific capabilities. Only include if benefits alone aren't concrete enough.

**Social Proof**: Testimonials, logos, stats, case studies. Specificity beats quantity.

**Objection Handling**: Address top 1-2 hesitations directly. FAQ format works well.

**Final CTA**: Restate value prop, repeat primary action. Often mirrors hero messaging.

## Copy Principles

**Headlines**: Lead with outcome, not feature. "Get X" beats "We offer Y".

**Specificity**: Numbers and details beat vague claims. "47% faster" beats "much faster".

**Voice**: Match audience sophistication. B2B enterprise ≠ consumer app.

**Length**: Say what needs saying, then stop. Every word earns its place.

**CTAs**: Action verb + outcome hint. "Start Free Trial" beats "Submit".

## Output

Write complete spec to `SPEC.md` in project root with all section copy, layout notes, mobile considerations, and SEO elements. After writing, summarize what was created and highlight any assumptions made.
