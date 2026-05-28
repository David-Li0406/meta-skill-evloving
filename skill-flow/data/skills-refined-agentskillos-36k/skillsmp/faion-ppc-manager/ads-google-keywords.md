---
id: google-keywords
name: "Google Ads Keyword Strategy"
domain: ADS
skill: faion-marketing-manager
category: "advertising"
---

# Google Ads Keyword Strategy

## Metadata

| Field | Value |
|-------|-------|
| **ID** | google-keywords |
| **Name** | Google Ads Keyword Strategy |
| **Category** | Ads API |
| **Difficulty** | Intermediate |
| **Agent** | faion-ads-agent |
| **Related** | google-campaign-setup, seo-fundamentals, paid-acquisition |

---

## Problem

You're targeting the wrong keywords. Broad keywords waste budget on irrelevant clicks. Too narrow and you miss opportunities. Understanding keyword match types and intent is crucial for profitable campaigns.

The right keyword strategy balances reach with relevance.

---

## Framework

Keyword strategy follows the intent-first approach:

```
RESEARCH  -> Find keywords your audience uses
QUALIFY   -> Match keywords to intent
ORGANIZE  -> Group by theme
MATCH     -> Choose appropriate match types
REFINE    -> Add negatives, optimize
```

### Step 1: Keyword Research

**Research sources:**

| Source | How to Use |
|--------|------------|
| Google Keyword Planner | Search volume, competition |
| Google Search | Autocomplete suggestions |
| Competitor ads | What they're bidding on |
| Your site search | What users look for |
| Customer language | How they describe problems |
| SEO tools | Ahrefs, SEMrush keyword data |

**Using Keyword Planner:**
1. Tools & Settings → Planning → Keyword Planner
2. "Discover new keywords"
3. Enter seed keywords or URL
4. Filter by volume, competition
5. Export relevant keywords

**Keyword types to find:**
- Product/service keywords
- Problem keywords
- Comparison keywords
- Alternative keywords
- Competitor keywords
- Long-tail variations

### Step 2: Understand Keyword Intent

**Intent categories:**

| Intent | Signals | Example |
|--------|---------|---------|
| **Navigational** | Brand names | "[company] login" |
| **Informational** | How, what, why | "how to manage projects" |
| **Commercial** | Best, top, compare | "best project management tool" |
| **Transactional** | Buy, pricing, trial | "project management software pricing" |

**Intent value hierarchy:**
```
High value: Transactional → Commercial → Informational → Navigational
```

**Focus budget on transactional and commercial first.**

### Step 3: Match Types

**Match type options:**

| Match Type | Syntax | Triggers |
|------------|--------|----------|
| **Broad** | keyword | Related searches, synonyms |
| **Phrase** | "keyword" | Searches containing phrase |
| **Exact** | [keyword] | Exactly or close variants |

**When to use each:**

| Match Type | Use Case | Risk |
|------------|----------|------|
| Broad | Discovery, high budget | Irrelevant traffic |
| Phrase | Balance reach/relevance | Some irrelevant |
| Exact | Proven keywords, tight control | Limited reach |

**Starting strategy:**
```
1. Start with phrase match
2. Add exact match for top performers
3. Use broad sparingly with tight negatives
```

### Step 4: Keyword Organization

**Ad group structure:**

| Approach | Description |
|----------|-------------|
| **SKAG** | Single Keyword Ad Groups (tight) |
| **Themed** | Related keywords grouped |
| **Funnel** | By intent stage |

**Themed approach (recommended):**
```
Ad Group: Project Management Tools
├── "project management software"
├── "project management tool"
├── "project management app"
├── [project management platform]
└── [team project management]

Ad Group: Task Management
├── "task management software"
├── "task tracking tool"
└── [task management app]
```

**Rules:**
- 10-20 keywords per ad group
- All keywords share same intent
- Ads match keyword theme
- Separate match types (optional)

### Step 5: Negative Keywords

**Negative keywords prevent wasted spend:**

| Type | Examples |
|------|----------|
| **Unqualified** | free, cheap, DIY |
| **Wrong intent** | jobs, careers, salary |
| **Wrong product** | unrelated products |
| **Competitors** | (if not targeting) |
| **Wrong audience** | students, hobbyists |

**Negative match types:**
- Negative broad: blocks if any word matches
- Negative phrase: blocks if phrase appears
- Negative exact: blocks exact match only

**Build negative list:**
1. Review Search Terms report weekly
2. Add irrelevant searches as negatives
3. Create shared negative lists
4. Apply across campaigns

### Step 6: Ongoing Optimization

**Weekly keyword tasks:**

| Task | How |
|------|-----|
| Review Search Terms | Find new negatives, keyword ideas |
| Check Quality Scores | Improve low QS keywords |
| Adjust bids | Based on performance |
| Add new keywords | From Search Terms insights |
| Pause poor performers | High cost, no conversions |

**Quality Score factors:**
- Expected CTR
- Ad relevance
- Landing page experience

**Improve Quality Score:**
- Use keyword in ad copy
- Match landing page to keyword
- Improve CTR through better ads
- Create tighter ad groups

---

## Templates

### Keyword Research Spreadsheet

```markdown
| Keyword | Match Type | Volume | Competition | Intent | Priority |
|---------|------------|--------|-------------|--------|----------|
| [word]  | Phrase     | 5,000  | Medium      | Trans  | High     |
| [word]  | Exact      | 1,000  | Low         | Comm   | High     |
| [word]  | Phrase     | 10,000 | High        | Info   | Medium   |
```

### Ad Group Plan

```markdown
## Ad Group: [Theme]

### Keywords (Phrase Match)
- "keyword 1"
- "keyword 2"
- "keyword 3"

### Keywords (Exact Match)
- [keyword 1]
- [high performer]

### Negative Keywords
- free
- [irrelevant term]

### Expected Volume
- Monthly searches: X,XXX
- Est. clicks: XXX
```

### Negative Keyword List

```markdown
## Shared Negative List: [Name]

### Unqualified
- free
- cheap
- discount (if not offering)

### Wrong Intent
- jobs
- careers
- how to make
- tutorial
- template (if not offering)

### Wrong Audience
- student
- beginner
- DIY

### Competitors (if not targeting)
- [competitor name]
```

---

## Examples

### Example 1: SaaS Product

**Keyword strategy:**
```
High Intent (Exact):
[project management software for teams]
[best project management tool]
[project management software pricing]

Medium Intent (Phrase):
"project management software"
"team collaboration tool"
"task management app"

Long-tail (Phrase):
"project management for remote teams"
"agile project management software"

Competitor (Exact):
[asana alternative]
[monday.com vs]
```

### Example 2: E-commerce

**Keyword strategy:**
```
Product Keywords:
[buy running shoes online]
"men's running shoes"
[nike running shoes]

Category Keywords:
"athletic shoes"
"workout sneakers"

Competitor:
[adidas alternative]

Negatives:
- free
- used
- repair
- jobs
```

---

## Implementation Checklist

### Research Phase
- [ ] Use Keyword Planner
- [ ] Analyze competitors
- [ ] Check search autocomplete
- [ ] Review customer language

### Organization Phase
- [ ] Group by theme
- [ ] Assign match types
- [ ] Create ad groups
- [ ] Build negative lists

### Launch Phase
- [ ] Start with phrase match
- [ ] Set initial bids
- [ ] Apply negative lists
- [ ] Monitor first week

### Optimization Phase
- [ ] Weekly Search Terms review
- [ ] Add negatives continuously
- [ ] Promote winners to exact
- [ ] Pause non-performers

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| All broad match | Wasted spend | Use phrase/exact |
| No negatives | Irrelevant clicks | Add weekly |
| Too many keywords | Diluted budget | 10-20 per group |
| Ignoring Search Terms | Missing insights | Review weekly |
| Mixing intents | Poor ad relevance | Separate by intent |
| Set and forget | Declining performance | Optimize weekly |

---

## Keyword Performance Benchmarks

| Metric | Poor | Average | Good |
|--------|------|---------|------|
| Quality Score | <5 | 5-6 | 7+ |
| CTR | <2% | 3-4% | 5%+ |
| Conversion rate | <2% | 3-5% | 7%+ |
| Impression share | <50% | 60-70% | 80%+ |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Research | Google Keyword Planner |
| Competitive | SpyFu, SEMrush |
| Analysis | Google Ads Editor |
| Tracking | Search Terms Report |
| Expansion | Keyword Tool.io |

---

## Related Methodologies

- **google-campaign-setup:** Google Campaign Setup
- **google-creative:** Google Creative
- **seo-fundamentals:** SEO Fundamentals (keyword overlap)
- **paid-acquisition:** Paid Acquisition Overview

---

*Methodology: google-keywords | Ads API | faion-ads-agent*
