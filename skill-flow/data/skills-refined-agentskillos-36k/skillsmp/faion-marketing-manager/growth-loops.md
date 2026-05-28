---
id: growth-loops
name: "Growth Loops"
domain: GRO
skill: faion-marketing-manager
category: "growth"
---

# Growth Loops

## Metadata

| Field | Value |
|-------|-------|
| **ID** | growth-loops |
| **Name** | Growth Loops |
| **Category** | Growth |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | viral-coefficient, product-led-growth, retention-loops |

---

## Problem

Traditional marketing funnels are linear: you spend money to acquire users, they use the product, some convert. The problem is that output does not feed back into input. You must keep spending to keep growing.

Growth loops are different. They are self-reinforcing systems where output from one cycle becomes input for the next. This creates compounding growth instead of linear growth.

---

## Framework

### What is a Growth Loop?

A growth loop is a closed system where:
1. An action generates an output
2. That output can be reinvested as input
3. This creates a compounding cycle

```
     ┌──────────────────────────────────────┐
     │                                      │
     ▼                                      │
  [INPUT] → [ACTION] → [OUTPUT] → [REINVESTMENT]
     │
     └── New cycle starts with more input
```

### Growth Loop vs Funnel

```
FUNNEL (Linear)                    GROWTH LOOP (Circular)
─────────────────                  ────────────────────────
  Acquisition                            ┌───────────┐
       ↓                                 │           │
  Activation                             ▼           │
       ↓                            [New User]       │
  Retention              →                ↓           │
       ↓                            [Uses Product]    │
  Revenue                                 ↓           │
       ↓                            [Creates Value]   │
  Referral                                ↓           │
       ↓                            [Shares/Invites]  │
     END                                  │           │
                                         └───────────┘
```

### Types of Growth Loops

#### 1. Viral Loops

Users invite other users directly.

```
User signs up → Uses product → Invites friends → Friends sign up → ...
```

**Examples:**
- Dropbox: "Get 500MB for each friend who joins"
- WhatsApp: Works better with friends
- Calendly: Scheduling link sent to others

**Key Metric:** Viral coefficient (K-factor)

#### 2. Content Loops

Users create content that attracts new users.

```
User creates content → Content indexed/shared → New user discovers → Signs up → Creates content → ...
```

**Examples:**
- Pinterest: Users create boards that appear in Google
- Quora: Questions/answers rank in search
- YouTube: Videos attract viewers who become creators

**Key Metric:** Content created per user, SEO traffic

#### 3. Paid Loops

Revenue funds acquisition that generates more revenue.

```
User pays → Revenue → Reinvest in ads → New user acquired → User pays → ...
```

**Examples:**
- E-commerce: Each sale funds more ads
- SaaS: Subscription revenue funds growth marketing

**Key Metric:** LTV:CAC ratio (must be > 3:1)

#### 4. Network Effect Loops

Product becomes more valuable as more users join.

```
User joins → Product value increases → Attracts more users → User joins → ...
```

**Examples:**
- LinkedIn: More professionals = more value
- Uber: More drivers = shorter wait times = more riders
- Airbnb: More hosts = more options = more travelers

**Key Metric:** Network density, engagement per user

#### 5. Supply-Side Loops

Suppliers/creators attract demand.

```
Creator joins → Creates supply → Attracts consumers → Revenue → More creators join → ...
```

**Examples:**
- Substack: Writers bring their audience
- Shopify: Stores bring their customers
- App Store: Developers attract users

**Key Metric:** Creator acquisition, creator retention

---

## Templates

### Growth Loop Design Template

```markdown
# Growth Loop: [Name]

## Loop Type
[Viral / Content / Paid / Network Effect / Supply-Side]

## Loop Diagram
```
[Step 1] → [Step 2] → [Step 3] → [Step 4]
    ↑                              │
    └──────────────────────────────┘
```

## Steps
1. **[Input]:** What starts the loop?
2. **[Action]:** What does the user do?
3. **[Output]:** What result is produced?
4. **[Reinvestment]:** How does output become new input?

## Key Metrics
| Metric | Current | Target |
|--------|---------|--------|
| Cycle time | | |
| Conversion at each step | | |
| Output per cycle | | |

## Bottleneck
[Which step has lowest conversion?]

## Optimization Plan
1.
2.
3.
```

### Loop Mapping Canvas

```
┌─────────────────────────────────────────────────────────┐
│                    GROWTH LOOP CANVAS                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  TRIGGER              ACTION              OUTPUT        │
│  ┌──────────┐        ┌──────────┐        ┌──────────┐  │
│  │          │   →    │          │   →    │          │  │
│  │          │        │          │        │          │  │
│  └──────────┘        └──────────┘        └──────────┘  │
│        ↑                                      │         │
│        │                                      │         │
│        │         REINVESTMENT                 │         │
│        │         ┌──────────┐                 │         │
│        └─────────│          │←────────────────┘         │
│                  │          │                           │
│                  └──────────┘                           │
│                                                         │
│  METRICS:                                               │
│  ├─ Cycle Time: _____ days                              │
│  ├─ Step 1→2 Conversion: _____ %                        │
│  ├─ Step 2→3 Conversion: _____ %                        │
│  └─ Step 3→1 Conversion: _____ %                        │
│                                                         │
│  BOTTLENECK: _____________________                      │
└─────────────────────────────────────────────────────────┘
```

---

## Examples

### Example 1: SaaS Content Loop

**Product:** Project management tool

**Loop:**
```
User creates project → Project has public page →
Page ranks in Google → New visitor finds it →
Visitor signs up → Creates own project → ...
```

**Metrics:**
- 15% of users create public projects
- Each public project gets 50 visits/month
- 3% of visitors sign up
- Cycle compounds monthly

**Calculation:**
```
Start: 1,000 users
15% create public projects = 150 projects
150 x 50 visits = 7,500 new visitors
7,500 x 3% signup = 225 new users

Month 2: 1,225 users → 184 projects → 9,200 visits → 276 new users
...
```

### Example 2: Marketplace Viral Loop

**Product:** Freelance platform

**Loop:**
```
Freelancer joins → Creates profile → Gets hired →
Delivers work → Client is happy → Client refers colleagues →
More clients join → More freelancers needed → ...
```

**Metrics:**
| Step | Conversion |
|------|------------|
| Freelancer joins | 100% |
| Gets first job | 40% |
| Client satisfied | 85% |
| Client refers | 15% |
| Referral signs up | 25% |

**K-factor:** 0.40 x 0.85 x 0.15 x 0.25 = 0.013

(Not viral, but contributes to growth)

### Example 3: Paid Acquisition Loop

**Product:** E-commerce subscription box

**Loop:**
```
Customer buys ($50) →
Profit margin (30% = $15) →
Reinvest 50% in ads ($7.50) →
CPA is $5 → Acquire 1.5 new customers →
1.5 x $50 = $75 revenue → ...
```

**Requirements for sustainable paid loop:**
- LTV > CAC
- Positive unit economics
- Ability to scale ad spend

---

## Implementation Checklist

### Phase 1: Identify (Week 1)
- [ ] List all ways users currently bring in other users
- [ ] Map existing acquisition channels
- [ ] Identify natural "sharing moments" in product
- [ ] Find what content users create
- [ ] Calculate current K-factor

### Phase 2: Design (Week 2)
- [ ] Choose primary loop type
- [ ] Map all steps in the loop
- [ ] Identify conversion at each step
- [ ] Find the bottleneck
- [ ] Design experiments to improve bottleneck

### Phase 3: Instrument (Week 3)
- [ ] Set up tracking for each step
- [ ] Create dashboard
- [ ] Set baseline metrics
- [ ] Define targets

### Phase 4: Optimize (Ongoing)
- [ ] Run experiments on bottleneck
- [ ] Measure cycle time
- [ ] Track compounding effect
- [ ] Add new loops as product matures

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Ignoring loop quality | Viral but low-quality users | Measure activation of loop-acquired users |
| Too many loops | Diluted effort | Focus on ONE loop until it works |
| Not measuring cycle time | Can't optimize speed | Track days from input to output |
| Forcing unnatural sharing | Feels spammy, hurts brand | Find genuine sharing moments |
| Optimizing wrong step | Bottleneck elsewhere | Always fix lowest-conversion step |

---

## Loop Efficiency Calculator

```
INPUTS:
─────────────────────────────────────
Initial users:           [A] = ____
Step 1→2 conversion:     [B] = _____%
Step 2→3 conversion:     [C] = _____%
Step 3→1 conversion:     [D] = _____%
Cycle time (days):       [T] = _____

CALCULATIONS:
─────────────────────────────────────
Loop efficiency = B × C × D = _____

If efficiency < 1.0: Loop decays (needs external input)
If efficiency = 1.0: Loop maintains (no growth)
If efficiency > 1.0: Loop compounds (viral growth)

After 12 months:
Users = A × (efficiency ^ (365/T)) = _____
```

---

## Growth Loop Stack

Most successful products have multiple loops:

```
Primary Loop:   [Your main growth driver]
         ↓
Secondary Loop: [Backup/complementary]
         ↓
Paid Loop:      [For predictable scaling]
```

**Example - Slack:**
1. **Primary:** Viral (teams invite team members)
2. **Secondary:** Content (integrations attract searches)
3. **Paid:** Enterprise sales (revenue funds outbound)

---

## Related Methodologies

- **viral-coefficient:** Viral Coefficient (deep dive into viral loops)
- **product-led-growth:** Product-Led Growth (PLG as a loop)
- **retention-loops:** Retention Loops (engagement-based loops)

---

*Methodology: growth-loops | Growth | faion-growth-agent*
