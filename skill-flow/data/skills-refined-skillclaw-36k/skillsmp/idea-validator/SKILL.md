---
name: Idea Validator
description: Brutally honest pre-build reality check for app ideas. Evaluates market saturation, demand, feasibility, monetization, and interest factor to save you from building things nobody wants.
---

# Idea Validator Skill

## Purpose

Provides honest, rapid feedback on app ideas BEFORE you invest time building. Saves weeks of wasted effort by identifying fatal flaws early.

**Philosophy**: Better to hear "this has been done 100 times" now than after a month of development.

## When to Use

Use this skill BEFORE starting any new project to validate:
- Market opportunity and competition
- Real vs. stated demand
- Solo builder feasibility (2-4 week timeline)
- Monetization viability
- Genuine interest factor

## Evaluation Criteria

### 1. Market Analysis (20%)

**Questions**:
- Is this space crowded or wide open?
- Who are the major players?
- What makes this idea different?
- Are incumbents vulnerable or entrenched?

**Research Tools**:
- WebSearch for existing products
- Product Hunt, Indie Hackers for similar launches
- App stores for competitor analysis
- HN/Reddit discussions for market sentiment

✅ Pass: Clear differentiation or underserved niche
⚠️ Caution: Crowded but weak competitors
❌ Fail: Saturated market with strong incumbents

### 2. Demand Validation (25%)

**Questions**:
- Do people actually pay for this or just say they would?
- Are there active communities discussing this problem?
- Is this a "nice to have" or "must have"?
- Are people using workarounds/hacks currently?

**Evidence Sources**:
- Reddit threads with upvotes on problem discussions
- Twitter searches for pain points
- Existing paid solutions (proves willingness to pay)
- GitHub issues requesting this functionality

✅ Pass: Evidence of paying customers for similar solutions
⚠️ Caution: Strong interest but unclear payment intent
❌ Fail: Only theoretical demand, no market validation

### 3. Feasibility Assessment (20%)

**Questions**:
- Can a solo builder ship this in 2-4 weeks?
- What's the technical complexity?
- Are there infrastructure/scaling challenges?
- Do you need permissions/partnerships?

**Complexity Indicators**:
- Core feature count (<5 = good, >10 = risky)
- External API dependencies
- Real-time/scaling requirements
- Regulatory/compliance needs

✅ Pass: Clear MVP scope, proven tech stack
⚠️ Caution: Ambitious but achievable with scope cuts
❌ Fail: Requires team, complex infra, or >1 month

### 4. Monetization Viability (20%)

**Questions**:
- How would this make money?
- Are people paying for similar products?
- What's the realistic pricing range?
- Is the unit economics feasible?

**Revenue Model Check**:
- B2C SaaS: $5-50/month (needs volume)
- B2B SaaS: $50-500/month (needs fewer customers)
- One-time: $10-100 (needs continuous customer acquisition)
- Freemium: Requires viral growth

✅ Pass: Clear monetization with proven comparable pricing
⚠️ Caution: Monetization possible but unproven
❌ Fail: No clear path to revenue or unrealistic pricing

### 5. Interest Factor (15%)

**Questions**:
- Is this genuinely compelling or boring?
- Would you use this yourself daily?
- Does it solve a hair-on-fire problem?
- Is there a "wow" factor or is it commoditized?

**Gut Check**:
- Would you build this even if it made $0?
- Can you envision excited users?
- Is this a painkiller or vitamin?

✅ Pass: Exciting problem you're passionate about
⚠️ Caution: Interesting but not thrilling
❌ Fail: Boring, commoditized, or forced interest

## Scoring System

```
Total Score = Market (20%) + Demand (25%) + Feasibility (20%) + Monetization (20%) + Interest (15%)

90-100%: 🚀 Build it - Strong opportunity
70-89%:  🤔 Maybe - Needs refinement or validation
<70%:    ⛔ Skip it - Fatal flaws or too risky
```

## Output Format

```
🎯 VERDICT: [Build it | Maybe | Skip it]

WHY:
[2-3 brutally honest sentences explaining the verdict]

📊 SCORE BREAKDOWN:
Market: [score]/20 - [brief assessment]
Demand: [score]/25 - [evidence found]
Feasibility: [score]/20 - [timeline reality check]
Monetization: [score]/20 - [revenue path]
Interest: [score]/15 - [compelling factor]

TOTAL: [score]/100

🔍 SIMILAR PRODUCTS:
• [Product 1] - [what they do, pricing if known]
• [Product 2] - [what they do, pricing if known]
• [Product 3] - [what they do, pricing if known]

💡 WHAT WOULD MAKE THIS STRONGER:
• [Specific suggestion 1]
• [Specific suggestion 2]
• [Specific suggestion 3]

🚨 RED FLAGS (if any):
• [Critical concerns that could kill the project]
```

## Research Methodology

### Step 1: Market Research (5 min)
```bash
# Use WebSearch for:
- "[idea name] alternatives"
- "best [category] tools"
- "[problem] solutions"

# Check Product Hunt, Indie Hackers, Hacker News
```

### Step 2: Demand Evidence (5 min)
```bash
# Search Reddit, Twitter, forums for:
- Pain point discussions
- Feature requests
- Workaround mentions
- Competitor complaints
```

### Step 3: Competitor Analysis (5 min)
```bash
# For each competitor found:
- Pricing model
- User reviews (what they love/hate)
- Feature gaps
- Last update date (active or abandoned?)
```

### Step 4: Monetization Check (3 min)
```bash
# Research:
- Comparable pricing in the space
- Average customer LTV estimates
- Payment willingness indicators
```

### Step 5: Reality Check (2 min)
```bash
# Honest assessment:
- Can I ship MVP in 2-4 weeks?
- Would I pay for this?
- Am I excited or just chasing trends?
```

## Examples

### Example 1: Strong Idea
```
🎯 VERDICT: 🚀 Build it

WHY:
Developer-focused screenshot annotation tool with code syntax highlighting is underserved.
Existing tools are generic or overpriced ($15-30/mo). Clear demand from dev Twitter with
people hacking together ImageMagick scripts. You can ship MVP in 2 weeks with your stack.

📊 SCORE BREAKDOWN:
Market: 16/20 - Niche but growing, weak competition
Demand: 22/25 - Active dev complaints, proven workarounds
Feasibility: 18/20 - Straightforward with existing libs
Monetization: 17/20 - $8-12/mo SaaS or $29 one-time viable
Interest: 13/15 - Solves your own pain point

TOTAL: 86/100

🔍 SIMILAR PRODUCTS:
• CleanShot X - $29 one-time, Mac only, not dev-focused
• Markup Hero - $8/mo, generic annotations, no code highlighting
• Annotate.com - Enterprise focus, $25/user/mo, overkill

💡 WHAT WOULD MAKE THIS STRONGER:
• Focus on developer-specific features (syntax highlighting, code themes)
• Launch with CLI + web app for dev workflow integration
• Price at $9/mo or $39 lifetime to undercut competitors

🚨 RED FLAGS: None major. Risk is market size - may be too niche for scaling.
```

### Example 2: Maybe Idea
```
🎯 VERDICT: 🤔 Maybe

WHY:
AI-powered meal planning is saturated but most solutions are complex and expensive.
Simpler, cheaper option could work but requires nutrition API partnerships and
content generation that might exceed 4-week timeline. Validate with landing page first.

📊 SCORE BREAKDOWN:
Market: 12/20 - Very crowded, need strong differentiation
Demand: 20/25 - Clear demand but high competition
Feasibility: 12/20 - Doable but tight for solo 4-week sprint
Monetization: 16/20 - Proven $10-20/mo pricing
Interest: 10/15 - Useful but not passionate about it

TOTAL: 70/100

🔍 SIMILAR PRODUCTS:
• Eat This Much - $9/mo, complex interface
• PlateJoy - $12/mo, heavily marketed
• Mealime - Freemium, strong mobile presence

💡 WHAT WOULD MAKE THIS STRONGER:
• Focus on single niche (keto, budget meals, meal prep)
• Start with curated recipes, add AI later
• Partner with grocery delivery APIs for unique value

🚨 RED FLAGS: Market is crowded. Need exceptional execution to stand out.
```

### Example 3: Skip Idea
```
🎯 VERDICT: ⛔ Skip it

WHY:
Social network for book lovers is a graveyard of failed startups. Goodreads dominates
despite poor UX because of network effects. Building a better Goodreads requires massive
scale to be useful, impossible for solo builder. Monetization unclear.

📊 SCORE BREAKDOWN:
Market: 5/20 - Dominated by Goodreads, Amazon backing
Demand: 15/25 - People want better but won't switch without users
Feasibility: 8/20 - Social features need scale, chicken-egg problem
Monetization: 6/20 - No proven revenue model for book social networks
Interest: 9/15 - Personally interesting but rationally flawed

TOTAL: 43/100

🔍 SIMILAR PRODUCTS:
• Goodreads - Free, 90M users, Amazon-owned
• StoryGraph - Bootstrapped alternative, struggling for traction
• Literal Club - VC-backed, limited success
• The Storygraph - Better UX but growth challenges

💡 WHAT WOULD MAKE THIS STRONGER:
• Pivot to niche: Technical book clubs, indie author platform
• Focus on features Goodreads can't/won't do
• Build for existing community rather than starting from zero

🚨 RED FLAGS:
• Network effect moat is insurmountable
• No monetization path without scale
• Requires years, not weeks, to gain traction
• History of well-funded failures in this space
```

## ROI

**Time Investment**: 20-30 minutes of research
**Potential Savings**: 2-4 weeks of wasted development time
**Success Rate**: Helps filter out 60-80% of ideas with fatal flaws

## Integration with Confidence Check

This skill complements the Confidence Check skill:
- **Idea Validator**: Use BEFORE deciding to build (strategic validation)
- **Confidence Check**: Use BEFORE implementing features (tactical validation)

Both prevent wrong-direction work but at different stages of the development lifecycle.
