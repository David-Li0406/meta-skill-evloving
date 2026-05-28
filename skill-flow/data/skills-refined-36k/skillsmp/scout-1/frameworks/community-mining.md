# Community Mining Framework

## Purpose

Extract real signals from where users actually talk. Answer: "Do people actually want this?"

**Philosophy:** User research at scale through public conversations. Real quotes > assumptions.

---

## Signal Sources

### Primary Sources

| Source | Best For | Signal Quality |
|--------|----------|----------------|
| **Reddit** | Honest discussions, complaints, recommendations | High |
| **Twitter/X** | Real-time sentiment, viral problems | Medium-High |
| **Hacker News** | Tech-savvy users, startup discussions | High for tech |
| **YouTube Comments** | Tutorial demand, feature requests | Medium |
| **Indie Hackers** | Builder perspective, validation stories | High for B2B |
| **Product Hunt** | Early adopter feedback, launch reactions | Medium |
| **Discord/Slack** | Niche community deep dives | High but hard to access |

### Secondary Sources

| Source | Best For |
|--------|----------|
| Quora | Question patterns, pain points |
| Stack Overflow | Technical pain points |
| Facebook Groups | Consumer niches |
| LinkedIn | B2B professional problems |
| Niche Forums | Vertical-specific insights |

---

## Reddit Mining

### Finding Relevant Subreddits

**Search patterns:**
```
site:reddit.com/r/ "{topic}"
"{topic} subreddit"
"reddit {target audience}"
```

**Common subreddits by audience:**

| Audience | Subreddits |
|----------|------------|
| Entrepreneurs | r/entrepreneur, r/smallbusiness, r/startups |
| Developers | r/programming, r/webdev, r/SaaS |
| Designers | r/design, r/userexperience, r/web_design |
| Creators | r/NewTubers, r/podcasting, r/content_marketing |
| Productivity | r/productivity, r/getdisciplined |
| Finance | r/personalfinance, r/financialindependence |

### Reddit Search Queries

```
# Finding pain points
site:reddit.com "{problem} help"
site:reddit.com "{problem} frustrated"
site:reddit.com "I wish there was"
site:reddit.com "anyone know a tool"

# Finding existing solutions discussion
site:reddit.com "what do you use for {problem}"
site:reddit.com "{competitor} alternative"
site:reddit.com "{competitor}" (flair:question OR flair:help)

# Finding willingness to pay
site:reddit.com "worth paying for {solution type}"
site:reddit.com "would pay for {feature}"
site:reddit.com "{product type} pricing"
```

### What to Extract from Reddit

| Signal Type | What to Look For | Example |
|-------------|------------------|---------|
| **Pain intensity** | Emotional language, frustration | "I'm SO frustrated with..." |
| **Frequency** | How often the problem occurs | "Every single day I have to..." |
| **Current solutions** | What they're using now | "Right now I'm using X but..." |
| **Willingness to pay** | Budget discussions | "I'd gladly pay $X for..." |
| **Feature requests** | What they wish existed | "If only it could..." |
| **Deal breakers** | Why they won't switch | "I'd switch but..." |

---

## Twitter/X Mining

### Search Operators

```
# Pain points
"{problem}" (frustrated OR annoying OR hate)
"I wish {product type}" -filter:links
"{competitor} sucks" OR "{competitor} terrible"

# Feature requests
"{product type}" "should have"
"why doesn't {competitor}"

# Alternatives seeking
"looking for" "{product type}" -filter:links
"alternative to {competitor}"

# Purchase intent
"just bought" OR "just subscribed" "{product type}"
"worth it" "{product type}"
```

### Twitter Signal Quality

**High quality signals:**
- Organic complaints (not prompted)
- Threads with engagement
- Replies expressing agreement
- Quote tweets adding context

**Low quality signals:**
- Marketing/promotion tweets
- Single tweets with no engagement
- Obvious affiliate links
- Outrage bait

---

## YouTube Comment Mining

### Finding Relevant Videos

```
# Tutorial videos (high intent)
"{topic} tutorial"
"how to {solve problem}"
"{product type} for beginners"

# Review videos (sentiment)
"{competitor} review"
"{competitor} vs {competitor}"
"best {product type} 2024"

# Problem-focused
"{problem} solution"
"{problem} fix"
```

### What to Extract from Comments

| Comment Type | What It Signals |
|--------------|-----------------|
| "How do I..." | Unmet need, educational opportunity |
| "I use X instead" | Alternative solutions |
| "This doesn't work for..." | Gap in current solutions |
| "I paid for..." | Willingness to pay |
| "Please make a video about..." | Demand for topics |
| Engagement metrics | View counts show interest level |

---

## Indie Hackers / Hacker News Mining

### Indie Hackers

```
# On the forum
site:indiehackers.com "{topic}"
site:indiehackers.com "built" "{product type}"
site:indiehackers.com "revenue" "{product type}"

# Validation stories
site:indiehackers.com "validation" "{topic}"
site:indiehackers.com "launched" "{topic}"
```

**What to look for:**
- Successful products in adjacent spaces
- Failed products (learn from mistakes)
- Revenue numbers (market viability)
- User acquisition strategies that worked

### Hacker News

```
# Discussions
site:news.ycombinator.com "{topic}"
site:news.ycombinator.com "Ask HN" "{topic}"
site:news.ycombinator.com "Show HN" "{product type}"

# Launch reactions
site:news.ycombinator.com "{competitor}"
```

**HN-specific signals:**
- "I would pay for this" comments
- Extensive feature discussions
- Technical feasibility debates
- Skepticism worth addressing

---

## Signal Scoring

### Pain Intensity Scale

| Level | Signals | Meaning |
|-------|---------|---------|
| **5 - Hair on fire** | "I NEED this", "take my money", active searching | Strong demand, urgent problem |
| **4 - Significant** | Detailed complaints, workaround sharing | Real problem, will pay |
| **3 - Notable** | Discussions exist, some frustration | Problem exists, validate WTP |
| **2 - Minor** | Occasional mentions, mild annoyance | Nice-to-have, low priority |
| **1 - Theoretical** | Only hypothetical discussions | Problem may not be real |

### Frequency Assessment

| Signal | Indicates |
|--------|-----------|
| Daily mentions across platforms | Hot topic, real demand |
| Weekly discussions | Active problem space |
| Monthly threads | Recurring but not urgent |
| Rare mentions | Niche or non-problem |

### Willingness to Pay Signals

**Strong WTP signals:**
- Explicit "I would pay $X"
- Currently paying for alternatives
- Time/money spent on workarounds
- Business impact discussions

**Weak WTP signals:**
- "That would be nice"
- Free solution expectations
- Only students/hobbyists discussing
- Complaints without switching behavior

---

## Quote Collection

### Quote Template

```markdown
### Quote: {Brief Description}

**Source:** {Platform} - {Subreddit/Account/Video}
**Date:** {When posted}
**Context:** {What triggered this comment}

> "{Exact quote}"

**Engagement:** {Upvotes/likes/replies}

**Signal Type:** {Pain/Request/WTP/Alternative}
**Intensity:** {1-5}

**Insight:** {What this tells us}
```

### Organizing Quotes

Group quotes by:
1. **Pain points** - What problems are mentioned
2. **Solutions** - What alternatives are used
3. **Features** - What capabilities are requested
4. **Objections** - Why people don't switch
5. **WTP** - Price sensitivity signals

---

## Output Format

```markdown
## Community Signals

### Summary

| Metric | Value |
|--------|-------|
| Sources searched | {N platforms} |
| Relevant discussions | {N posts/threads} |
| Pain intensity (avg) | {X}/5 |
| WTP signals | {Strong/Medium/Weak} |

### Pain Points

**1. {Pain Point}** (Intensity: {X}/5)

> "{Quote 1}" - Reddit r/{subreddit}

> "{Quote 2}" - Twitter @{handle}

**Frequency:** {How often mentioned}
**Current workarounds:** {What people do now}

**2. {Pain Point}** (Intensity: {X}/5)
{Same format}

### Feature Requests

| Request | Mentions | Platforms |
|---------|----------|-----------|
| {Feature} | {N} | Reddit, Twitter |
| {Feature} | {N} | HN, IndieHackers |

### Willingness to Pay

**Evidence:**
> "{Quote about paying}" - {Source}

**Price points mentioned:** ${X} - ${Y}
**Comparison to alternatives:** {How they price}

### Alternative Solutions Mentioned

| Alternative | Sentiment | Complaints |
|-------------|-----------|------------|
| {Product} | Mixed | "{main complaint}" |
| {Product} | Negative | "{main complaint}" |

### Key Insights

1. {Insight 1}
2. {Insight 2}
3. {Insight 3}

### Red Flags

{Any signals suggesting this might not work}
```

---

## Red Flags

- Can't find discussions anywhere (problem doesn't exist)
- All mentions are self-promotional (no organic interest)
- Only theoretical "would be nice" comments (low priority problem)
- Strong "just use X" consensus (solved problem)
- Discussions are old, no recent activity (dated problem)
- Only enterprise/big company discussions (not solo-builder friendly)
