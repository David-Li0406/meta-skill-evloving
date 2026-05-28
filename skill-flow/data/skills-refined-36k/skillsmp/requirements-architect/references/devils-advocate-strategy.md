# Devil's Advocate Strategy Framework

Use this framework to stress-test strategic decisions in PRDs. After every major choice, systematically argue the opposite position to surface weaknesses and blind spots.

---

## Core Principle

**Every strategic decision has trade-offs.** The devil's advocate reveals:
- Hidden assumptions you haven't validated
- Risks you're unconsciously accepting
- Alternative paths you dismissed too quickly
- Second-order effects you haven't considered

---

## How to Use This Framework

### Step 1: State the Decision
Clearly articulate the choice being made:
- "We will focus on [X] instead of [Y]"
- "We will build [approach A] rather than [approach B]"
- "We will target [segment] first"

### Step 2: Argue the Opposite
Forcefully make the case for the path not taken:
- Present the strongest evidence for the alternative
- Identify what would need to be true for the alternative to be better
- Surface risks in the chosen path
- Highlight benefits you're sacrificing

### Step 3: Evaluate and Decide
After hearing the counter-argument:
- Reaffirm decision with better rationale
- Adjust decision based on valid points
- Identify mitigations for surfaced risks
- Document the trade-offs explicitly

---

## Common Strategic Decisions to Challenge

### 1. Target Market / Segment Choice

**Decision Format**: "We will focus on [Segment A] instead of [Segment B]"

**Devil's Advocate Questions**:
- What if Segment B has higher willingness to pay?
- What if Segment A is more price-sensitive than we think?
- Are we choosing Segment A because it's easier or because it's better?
- What if a competitor owns Segment A and we can't differentiate?
- What's the market size difference, really?

**Challenge Template**:
> "You've chosen to focus on [Segment A], but let me argue for [Segment B]:
> - [Segment B] represents $X larger TAM
> - [Segment B] has demonstrated willingness to pay X% more
> - Our competitors are weaker with [Segment B]
> - [Segment B]'s problems are more acute, suggesting faster adoption
> Why shouldn't we focus there instead?"

---

### 2. Build vs Buy vs Partner

**Decision Format**: "We will build this in-house rather than [buy/partner]"

**Devil's Advocate Questions**:
- What's the true total cost including opportunity cost?
- How long until a build matches buy quality?
- What core competencies are we developing vs distracting from?
- What happens if the vendor improves faster than we can build?
- Are we underestimating integration complexity?

**Challenge Template**:
> "You've decided to build this in-house, but consider the buy option:
> - [Vendor X] already has this at 80% of needed functionality
> - Integration would take 2-4 weeks vs 6 months to build
> - Your engineering team could focus on [core differentiator] instead
> - The vendor's roadmap includes features you'd need to build anyway
> What's the real reason we're not buying?"

---

### 3. Feature Scope / MVP Definition

**Decision Format**: "We will include [these features] and exclude [those features]"

**Devil's Advocate Questions**:
- Is this MVP actually enough to validate the hypothesis?
- Are we cutting too much and risking the value proposition?
- Are we including features that aren't really necessary?
- What if the "nice-to-have" feature is actually the differentiator?
- Are we just doing what's easiest rather than what's right?

**Challenge Template**:
> "Your MVP scope excludes [Feature X], but let me argue for including it:
> - Every competitor has [Feature X] as table stakes
> - User research showed [Feature X] was the #2 requested capability
> - Without [Feature X], users may not see enough value to adopt
> - The delta effort is only [Y weeks] more
> Is your MVP too minimal to prove anything?"

---

### 4. Technology / Architecture Choice

**Decision Format**: "We will use [Technology A] instead of [Technology B]"

**Devil's Advocate Questions**:
- Are we choosing based on team familiarity rather than fitness?
- What if we're optimizing for today's scale, not tomorrow's?
- What's the hiring market for this technology?
- What happens if this technology loses community support?
- Are we avoiding the right choice because it's harder?

**Challenge Template**:
> "You've chosen [Tech A], but consider [Tech B]:
> - [Tech B] handles [specific requirement] natively
> - [Tech B] has stronger enterprise adoption
> - The performance characteristics of [Tech B] match our future needs better
> - Three of your most-wanted hires are expert in [Tech B]
> Are you choosing [Tech A] because it's familiar, not because it's right?"

---

### 5. Pricing / Monetization Strategy

**Decision Format**: "We will price at [X] using [model Y]"

**Devil's Advocate Questions**:
- What if you're leaving money on the table?
- What if this price signals low quality?
- What if a different pricing model aligns incentives better?
- What if your target segment can't afford this?
- What's the LTV:CAC at this price point?

**Challenge Template**:
> "Your $X/month price point seems low. Consider higher pricing:
> - Competitor [Y] charges 3x with similar value proposition
> - Your unit economics require X customers to break even at this price
> - Low price may signal low quality to enterprise buyers
> - You have no price anchoring allowing for discounts
> Are you underpricing because you're afraid of rejection?"

---

### 6. Timeline / Phasing Decision

**Decision Format**: "We will ship Phase 1 in [X timeframe]"

**Devil's Advocate Questions**:
- Is this timeline realistic given historical velocity?
- What's not included in this estimate?
- What if a faster timeline captures market opportunity?
- What if a longer timeline produces significantly better quality?
- Are you padding or are you too aggressive?

**Challenge Template**:
> "Your 3-month timeline seems aggressive. Consider the risks:
> - Similar projects historically took 4-5 months
> - You haven't accounted for [X dependency]
> - Quality at this pace may create tech debt costing more later
> - User research findings may require mid-project pivots
> What's the cost of being 6 weeks late vs shipping something half-baked?"

---

### 7. Go-to-Market Strategy

**Decision Format**: "We will launch via [channel/approach]"

**Devil's Advocate Questions**:
- What if this channel is saturated?
- What if a different channel reaches buyers faster?
- Are we conflating what's comfortable with what's effective?
- What if our competitors have this channel locked down?
- What's the customer acquisition cost through this channel?

**Challenge Template**:
> "Your PLG motion assumes self-serve adoption, but consider sales-led:
> - Enterprise deals have 10x the ACV
> - Your current users are predominantly from direct outreach
> - Self-serve requires significant product investment you haven't scoped
> - Sales-led gives you direct customer feedback during the sale
> Are you avoiding sales because you're not comfortable with it?"

---

## Red Flags to Watch For

When doing devil's advocate, these responses suggest weak reasoning:

| Response | Translation | Action |
|----------|-------------|--------|
| "Everyone knows X" | Unvalidated assumption | Demand evidence |
| "We've always done Y" | Habit, not strategy | Challenge directly |
| "There's no time to evaluate Z" | Avoiding difficult analysis | Make time |
| "The team wants A" | Preference, not rationale | Ask "why want?" |
| "It's too hard to do B" | Risk aversion | Evaluate trade-offs |
| "Competitors do X" | Copying, not thinking | Ask "should we?" |

---

## Output Format

After each devil's advocate challenge, document:

```markdown
## Decision: [Statement of decision]

### Original Rationale
[Why this was the initial choice]

### Devil's Advocate Challenge
[Strongest argument for the alternative]

### Counter-Arguments Considered
1. [Point raised]
2. [Point raised]

### Final Decision
[Reaffirm / Adjust / Reconsider]

### Trade-offs Accepted
- We accept [risk/downside] in exchange for [benefit]

### Mitigations Added
- [Action to address valid concerns]
```

---

## When to Skip Devil's Advocate

Not every decision needs formal challenge:
- **Reversible decisions** with low cost of being wrong
- **Clear data** pointing to one option overwhelmingly
- **Table stakes** features that are non-negotiable
- **Constrained choices** where alternatives don't exist

Focus devil's advocate energy on:
- **High-stakes** irreversible decisions
- **Strategic bets** with significant resource commitment  
- **Decisions under uncertainty** where data is limited
- **Decisions with strong emotional pull** (founder bias)
