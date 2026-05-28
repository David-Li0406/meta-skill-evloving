---
id: competitive-positioning
name: "Competitive Positioning"
domain: PRD
skill: faion-product-manager
category: "product"
---

# Competitive Positioning

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Product |
| **Difficulty** | Intermediate |
| **Tags** | #product, #positioning, #competition |
| **Domain Skill** | faion-product-manager |
| **Agents** | faion-competitor-analyzer-agent |

---

## Problem

Products struggle to stand out in crowded markets. Issues:
- "We're like X but better" (no differentiation)
- Competing on features (race to bottom)
- Positioning that doesn't resonate
- No clear reason to choose you

**The root cause:** No framework for carving out and communicating a unique market position.

---

## Framework

### What is Competitive Positioning?

Competitive positioning is defining how your product is uniquely valuable compared to alternatives. It answers: "Why should customers choose us?"

### Positioning Components

**April Dunford's model:**

| Component | Question | Example |
|-----------|----------|---------|
| Competitive alternatives | What would they do if we didn't exist? | Spreadsheets, competitor X |
| Unique attributes | What do we have that others don't? | Real-time collaboration |
| Value | What does that attribute enable? | Save 5 hours/week |
| Target customer | Who cares most about that value? | Remote teams |
| Market category | What type of product is this? | Team project management |

### Positioning Strategies

#### 1. Head-to-Head

**When:** You're better on established criteria
**Risk:** Feature wars
**Example:** "Faster than [competitor]"

#### 2. Differentiation

**When:** You serve a specific need others ignore
**Risk:** Niche too small
**Example:** "CRM built for solo consultants"

#### 3. Niche Dominance

**When:** You own a specific segment
**Risk:** Growth ceiling
**Example:** "The design tool for iOS developers"

#### 4. Category Creation

**When:** You're truly new
**Risk:** Market education required
**Example:** "AI-powered writing assistant" (new category)

### Positioning Development Process

#### Step 1: Analyze Alternatives

**List everything:**
- Direct competitors (same category)
- Indirect competitors (different solution, same problem)
- Status quo (do nothing)

**For each:** What's their positioning? Strengths? Weaknesses?

#### Step 2: Identify Your Unique Attributes

**What can you truthfully claim:**
- Features only you have
- Approach only you take
- Expertise only you possess
- Experience you've created

**Test:** Can competitors claim this too?

#### Step 3: Translate to Customer Value

**For each attribute:**
- So what? (first level benefit)
- So what? (deeper benefit)
- So what? (ultimate outcome)

**Example:**
- Attribute: Real-time sync
- So what: Team always sees latest version
- So what: No version confusion
- So what: Ship faster with fewer mistakes

#### Step 4: Identify Best-Fit Customers

**Who values this most:**
- Segment characteristics
- Problems they face
- Why your value matters specifically to them

#### Step 5: Define Market Category

**Options:**
- Existing category (easier to explain)
- Subcategory (more specific)
- New category (highest differentiation, hardest)

#### Step 6: Craft Positioning Statement

**Template:**
```
For [target customer]
Who [need/situation]
[Product name] is [market category]
That [key benefit]
Unlike [alternatives]
We [unique differentiator]
```

---

## Templates

### Positioning Canvas

```markdown
## Positioning Canvas: [Product]

### Competitive Alternatives
What would customers do if we didn't exist?
1. [Alternative 1] - [Their positioning]
2. [Alternative 2] - [Their positioning]
3. [Status quo] - [What they do today]

### Our Unique Attributes
| Attribute | Competitors Have? | Defensible? |
|-----------|-------------------|-------------|
| [Attribute 1] | No | Yes |
| [Attribute 2] | Partially | Yes |

### Value Translation
| Attribute | Feature Benefit | Business Benefit | Outcome |
|-----------|-----------------|------------------|---------|
| [Attr 1] | [Benefit] | [Benefit] | [Outcome] |

### Best-Fit Customer
**Profile:** [Description]
**Key characteristics:**
- [Characteristic 1]
- [Characteristic 2]

**Why they care:** [Why our value matters to them]

### Market Category
**Category:** [Name]
**Type:** [Existing/Subcategory/New]
**Rationale:** [Why this framing]

### Positioning Statement

For [target customer]
Who [need/situation]
[Product name] is [market category]
That [key benefit]
Unlike [alternatives]
We [unique differentiator]

### Proof Points
1. [Evidence of claim]
2. [Evidence of claim]
3. [Evidence of claim]
```

### Competitive Positioning Map

```markdown
## Positioning Map: [Market]

### Dimensions
- **X-axis:** [Dimension 1, e.g., Price]
- **Y-axis:** [Dimension 2, e.g., Ease of use]

### Map

```
    Easy to Use
        ↑
        |
    [Us]        [Comp A]
        |
   ─────┼─────────────────→ High Price
        |
    [Comp B]    [Comp C]
        |
        ↓
    Complex
```

### Our Position
**Quadrant:** [Description]
**Rationale:** [Why we're here]

### Opportunities
- [Gap in the market]
- [Underserved position]

### Threats
- [Competitor moving toward us]
- [New entrant risk]
```

---

## Examples

### Example 1: Project Management Tool

**Alternatives:**
- Asana, Monday (feature-rich, complex)
- Trello (simple but limited)
- Spreadsheets (free but painful)

**Unique attributes:**
- Designed for solo creators
- No team features (simpler)
- Built-in time tracking

**Value:** Get organized in 5 minutes, not 5 hours

**Best-fit:** Solo freelancers who are overwhelmed by big tools

**Position statement:**
```
For solo freelancers
Who need to track projects without complexity
SoloBoard is a personal project manager
That gets you organized in 5 minutes
Unlike Asana and Monday
We deliberately have no team features
```

### Example 2: Email Marketing Platform

**Alternatives:**
- Mailchimp (all-in-one, expensive at scale)
- ConvertKit (creator-focused)
- Substack (newsletter-native)

**Unique attributes:**
- Flat pricing (no per-subscriber fees)
- Focused on <10K subscribers
- Integrated with Ghost/WordPress

**Value:** Grow without pricing anxiety

**Best-fit:** Indie writers/bloggers building audience

**Position statement:**
```
For indie writers growing their newsletter
Who worry about costs as they scale
WriterMail is email marketing
That stays affordable forever
Unlike Mailchimp and ConvertKit
We charge flat fees, not per-subscriber
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| "Better" positioning | Find what's different, not better |
| Feature-focused | Translate to customer value |
| Too broad | Focus on best-fit customers |
| Ignoring alternatives | Always position against something |
| Static positioning | Revisit as market changes |
| No proof points | Back claims with evidence |
| Category confusion | Be clear about what you are |

---

## Related Methodologies

- **competitor-analysis:** Competitor Analysis
- **value-proposition-design:** Value Proposition Design
- **gtm-strategy:** GTM Strategy
- **landing-page-design:** Landing Page Design
- **content-marketing:** Content Marketing

---

## Agent

**faion-competitor-analyzer-agent** helps with positioning. Invoke with:
- "Help me position [product] against [competitors]"
- "What's our differentiation from [competitor]?"
- "Create a positioning map for [market]"
- "Review my positioning statement: [statement]"

---

*Methodology | Product | Version 1.0*
