# Growth Loops Framework

## Purpose

Design and optimize sustainable growth mechanics. One-time campaigns fade; loops compound forever.

---

## What is a Growth Loop?

A growth loop is a self-reinforcing cycle where the output of one cycle becomes the input of the next.

```
[Input] → [Action] → [Output] → [Input]...
```

### Loop vs Funnel

| Funnel | Loop |
|--------|------|
| Linear | Circular |
| Decays over time | Compounds over time |
| Requires constant input | Self-sustaining |
| "Pour users in top" | "Users create more users" |

---

## Types of Growth Loops

### 1. Viral Loop

**How it works:**
Users invite other users directly.

```
User signs up
    ↓
Uses product, gets value
    ↓
Invites friends/colleagues
    ↓
Friends sign up
    ↓
[Repeat]
```

**Key metric:** Viral coefficient (K-factor)
- K < 1: Not viral (need other acquisition)
- K = 1: Stable (each user brings 1 new user)
- K > 1: Viral growth (exponential)

**Examples:**
- Dropbox: Get free storage for referrals
- Calendly: Every meeting = exposure
- Slack: Invite teammates to collaborate

**How to build:**
1. Product must be worth sharing
2. Sharing must be natural (not forced)
3. Incentive alignment (both parties benefit)
4. Low friction to invite

### 2. Content Loop

**How it works:**
Users create content that attracts new users.

```
User signs up
    ↓
Creates content on platform
    ↓
Content gets indexed/shared
    ↓
New users discover content
    ↓
New users sign up
    ↓
[Repeat]
```

**Key metric:** Content velocity, SEO traffic

**Examples:**
- Notion: Templates shared publicly
- Figma: Designs embedded and shared
- Medium: Articles rank in Google

**How to build:**
1. Make creating content easy
2. Make content shareable/embeddable
3. SEO optimize user content
4. Public by default (or incentivize)

### 3. Paid Loop

**How it works:**
Revenue funds acquisition that generates more revenue.

```
Acquire user (paid)
    ↓
User pays for product
    ↓
Revenue funds more ads
    ↓
Acquire more users
    ↓
[Repeat]
```

**Key metric:** CAC/LTV ratio (should be < 1:3)

**Examples:**
- Most e-commerce
- Direct response SaaS
- Performance marketing

**How to build:**
1. Know your unit economics
2. LTV > 3x CAC
3. Short payback period
4. Scalable ad channels

### 4. Sales Loop

**How it works:**
Revenue funds sales team that generates more revenue.

```
Sales closes customer
    ↓
Customer pays
    ↓
Revenue funds more sales
    ↓
More customers closed
    ↓
[Repeat]
```

**Key metric:** Sales efficiency, magic number

**Not recommended for solo builders** - requires team.

### 5. Product Loop

**How it works:**
Product usage creates more value/data that improves the product.

```
User uses product
    ↓
Creates data/network value
    ↓
Product improves for everyone
    ↓
More users want to join
    ↓
[Repeat]
```

**Examples:**
- Waze: More users = better traffic data
- Yelp: More reviews = more useful
- LinkedIn: More connections = more value

**Hard for solo builders** - requires network effects.

---

## Flywheel Model

A flywheel is multiple loops connected together.

### Example: Content SaaS Flywheel

```
         ┌──────────────────┐
         │   User Content   │
         └────────┬─────────┘
                  │
                  ▼
         ┌──────────────────┐
         │   SEO Traffic    │
         └────────┬─────────┘
                  │
                  ▼
         ┌──────────────────┐
         │   New Sign-ups   │
         └────────┬─────────┘
                  │
                  ▼
         ┌──────────────────┐
         │   More Content   │───┐
         └──────────────────┘   │
                  ▲             │
                  └─────────────┘
```

---

## Solo Builder Loop Recommendations

### Best Loops for Solo

| Loop Type | Feasibility | Why |
|-----------|-------------|-----|
| Content loop | High | You control content, SEO is free |
| Viral loop (organic) | Medium | Depends on product fit |
| Paid loop | Low | Requires capital, optimization |
| Sales loop | Very Low | Requires team |

### Recommended Approach

**Primary:** Content loop (long-term)
- Create valuable content
- SEO optimization
- Social sharing

**Secondary:** Organic viral (if product fits)
- Make product shareable
- Incentivize referrals
- Word of mouth

---

## Measuring Loops

### Viral Coefficient (K-factor)

```
K = (Invites per user) × (Conversion rate of invites)
```

**Example:**
- Average user sends 5 invites
- 20% of invites convert
- K = 5 × 0.2 = 1.0

### Content Loop Metrics

| Metric | What it Measures |
|--------|------------------|
| Content created/day | Loop input |
| SEO impressions | Content reach |
| Organic sign-ups | Loop output |
| Creator retention | Loop sustainability |

### Loop Health Check

| Question | Good | Bad |
|----------|------|-----|
| Is the loop running? | New users from loop source | No loop activity |
| Is it accelerating? | Metrics improving | Metrics flat/declining |
| Is it sustainable? | Low friction, natural | Requires constant effort |

---

## Building Your Loop

### Step 1: Identify Loop Potential

```
What does your product naturally create?
├── Content → Content loop
├── Connections → Viral loop
├── Data → Product loop
└── Revenue → Paid/Sales loop
```

### Step 2: Remove Friction

| Stage | Friction to Remove |
|-------|---------------------|
| Input | Make action easy |
| Action | Reduce steps |
| Output | Auto-share/distribute |
| Re-input | Make discovery easy |

### Step 3: Add Amplifiers

| Amplifier | How |
|-----------|-----|
| Incentives | Reward loop participation |
| Visibility | Make outputs discoverable |
| Triggers | Prompt loop actions |
| Social proof | Show loop success |

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Forcing virality | Users won't share junk | Make product worth sharing |
| Incentive only | No genuine value | Ensure real benefit |
| Too much friction | Loop breaks | Reduce steps |
| No measurement | Can't optimize | Track loop metrics |
| Wrong loop | Doesn't fit product | Choose appropriate loop |

---

## Output Format

```markdown
## Growth Loop Analysis

### Primary Loop
**Type:** {Content / Viral / Paid / Product}

**Mechanics:**
{User action} → {Creates output} → {Attracts input} → {New user}

**Current Metrics:**
- K-factor: {X}
- Loop cycle time: {days/weeks}
- Loop efficiency: {%}

### Loop Diagram
{Draw the specific loop}

### Optimizations
1. {Optimization to improve loop}
2. {Optimization}
3. {Optimization}

### Health Status
- Loop running: {Yes/No}
- Accelerating: {Yes/No}
- Sustainable: {Yes/No}
```
