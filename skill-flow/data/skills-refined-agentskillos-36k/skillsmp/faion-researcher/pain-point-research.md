---
id: pain-point-research
name: "Pain Point Research"
domain: RES
skill: faion-researcher
category: "research"
---

# Pain Point Research

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Research |
| **Difficulty** | Beginner |
| **Tags** | #research, #pain-points, #discovery |
| **Domain Skill** | faion-researcher |
| **Agents** | faion-pain-point-researcher-agent |

---

## Problem

Finding pain points manually is time-consuming and hit-or-miss. Entrepreneurs often:
- Look in the wrong places
- Misinterpret complaints as problems
- Miss hidden pain points beneath surface issues
- Don't categorize or prioritize findings

**The root cause:** No systematic approach to discovering and organizing pain points.

---

## Framework

### What is Pain Point Research?

Pain point research is the systematic discovery and categorization of problems that cause frustration, waste time, or cost money for a specific audience.

### The Pain Point Discovery Framework

#### Step 1: Define Your Research Scope

**Template:**
```
Audience: [Specific group]
Context: [Situation/workflow]
Domain: [Industry/area]
Goal: Find [X] pain points in [Y] hours
```

**Example:**
- Audience: Freelance web developers
- Context: Client project management
- Domain: Remote services
- Goal: Find 20 pain points in 4 hours

#### Step 2: Mine Pain Point Sources

**Tier 1: Direct Complaints (Highest Signal)**

| Source | How to Search | What to Find |
|--------|---------------|--------------|
| Reddit | r/[niche] + sort by top/controversial | "I hate when...", "Frustrated with..." |
| Twitter/X | "[topic] sucks" OR "[topic] frustrating" | Rants, complaints |
| Product Hunt | Read negative reviews | Feature gaps, UX issues |
| G2/Capterra | 1-3 star reviews | Why people left/hate product |
| App Store | Filter by recent 1-2 stars | Specific grievances |

**Tier 2: Questions (Problem Indicators)**

| Source | How to Search | What to Find |
|--------|---------------|--------------|
| Quora | "[topic] how to" | What people can't figure out |
| Stack Overflow | [tag] + closed as duplicate | Recurring issues |
| Subreddit wikis | FAQ sections | Most asked questions |
| Google "People Also Ask" | Search [topic] | Common confusions |

**Tier 3: Forums & Communities**

| Source | How to Access | What to Find |
|--------|---------------|--------------|
| Slack groups | Join niche communities | Daily struggles |
| Discord servers | Search for [niche] discord | Real-time problems |
| Facebook groups | Search and join | Lengthy complaint posts |
| Indie Hackers | Browse discussions | Founder problems |

**Tier 4: Jobs & Gigs**

| Source | How to Search | What to Find |
|--------|---------------|--------------|
| Upwork | Browse job posts | What people outsource |
| Fiverr | Popular gigs | Repetitive needs |
| LinkedIn Jobs | "looking for someone to" | Manual work needs |

#### Step 3: Categorize Pain Points

**Pain Point Categories:**

| Category | Description | Example |
|----------|-------------|---------|
| Time Waste | Takes too long to do X | "Spend 2 hours updating reports" |
| Money Loss | Costs more than it should | "Paying $200/mo for features I don't use" |
| Complexity | Too hard to understand | "Can't figure out the settings" |
| Integration | Tools don't work together | "Have to copy-paste between apps" |
| Reliability | Doesn't work consistently | "It crashes every other day" |
| Support | Can't get help | "No response from support in 3 days" |
| Process | Workflow is broken | "Need 5 approvals for simple change" |
| Learning | Hard to get started | "Took 2 weeks to set up" |

#### Step 4: Score Pain Points

**Pain Intensity Matrix:**

| Factor | Weight | 1 | 3 | 5 |
|--------|--------|---|---|---|
| Frequency | 30% | Rarely | Weekly | Daily |
| Severity | 25% | Annoying | Painful | Blocking |
| Reach | 20% | Few people | Many | Everyone |
| Spend | 15% | $0 spent | Some | Significant |
| Alternatives | 10% | Many exist | Few | None |

**Score = (Freq×0.3) + (Sev×0.25) + (Reach×0.2) + (Spend×0.15) + (Alt×0.1)**

**Priority:**
- Score > 4: Critical pain - high priority
- Score 3-4: Significant pain - worth solving
- Score 2-3: Moderate pain - could be feature
- Score < 2: Minor pain - deprioritize

#### Step 5: Extract Root Causes

For top pain points, dig deeper:

**5 Whys Analysis:**
```
Pain: "I spend 3 hours/week on expense reports"
Why 1: Reports are manual
Why 2: System doesn't auto-import receipts
Why 3: No OCR integration
Why 4: IT won't approve new tools
Why 5: Process for new tools takes 6 months
Root: Organizational friction in tool adoption
```

**Jobs to be Done:**
```
When [situation]
I want to [action]
So I can [outcome]
```

---

## Templates

### Pain Point Research Log

```markdown
## Pain Point Research: [Audience]

### Research Scope
- **Audience:** [X]
- **Context:** [X]
- **Time spent:** [X] hours
- **Sources checked:** [X]

### Pain Points Found

#### PP-001: [Name]
- **Source:** [Where found]
- **Category:** [Time/Money/Complexity/etc.]
- **Quote:** "[Exact quote]"
- **Frequency:** [1-5]
- **Severity:** [1-5]
- **Reach:** [1-5]
- **Score:** [X]
- **Root cause:** [Analysis]

#### PP-002: [Name]
...

### Summary by Category

| Category | Count | Avg Score |
|----------|-------|-----------|
| Time Waste | X | X |
| Money Loss | X | X |
...

### Top 5 Pain Points (Prioritized)

1. [PP-X]: Score X - [Brief]
2. [PP-X]: Score X - [Brief]
3. [PP-X]: Score X - [Brief]
4. [PP-X]: Score X - [Brief]
5. [PP-X]: Score X - [Brief]

### Opportunities Identified
1. [Opportunity from PP-X]
2. [Opportunity from PP-X]

### Next Steps
- [ ] Validate PP-001 with interviews
- [ ] Research solutions for PP-002
```

### Reddit Mining Template

```markdown
## Reddit Research: r/[subreddit]

### Posts Analyzed
- **Date range:** [X]
- **Posts reviewed:** [X]
- **Relevant posts:** [X]

### Pain Points Extracted

| Post Title | Upvotes | Pain Point | Category |
|------------|---------|------------|----------|
| "[Title]" | X | [Pain] | [Cat] |
| "[Title]" | X | [Pain] | [Cat] |

### Notable Quotes
1. "[Quote]" - [Link]
2. "[Quote]" - [Link]

### Patterns Noticed
- [Pattern 1]
- [Pattern 2]
```

---

## Examples

### Example 1: Pain Points for Email Marketers

**Research scope:** Solo marketers managing newsletters

**Top findings:**

| Pain | Source | Category | Score |
|------|--------|----------|-------|
| Deliverability issues | r/emailmarketing | Reliability | 4.5 |
| Can't segment properly | G2 reviews | Complexity | 4.2 |
| Analytics confusing | Twitter rants | Complexity | 3.8 |
| Template editing clunky | App reviews | Process | 3.5 |
| Pricing spikes with growth | Reddit | Money | 4.0 |

**Root cause:** Tools built for big teams, not solopreneurs.

**Opportunity:** Simple email tool optimized for <10K subscribers.

### Example 2: Pain Points for Online Course Creators

**Research scope:** First-time course creators

**Top findings:**

| Pain | Source | Category | Score |
|------|--------|----------|-------|
| Video editing takes forever | Indie Hackers | Time Waste | 4.6 |
| Platform fees too high | Reddit | Money | 4.3 |
| Don't know what to teach | Quora | Learning | 3.9 |
| Students don't complete | Twitter | Process | 4.1 |
| Marketing is overwhelming | Facebook groups | Complexity | 4.0 |

**Root cause:** Creators are content experts, not tech/marketing experts.

**Opportunity:** Done-for-you course launch service.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Surface-level research | Dig into comments, not just posts |
| Only one source | Use 3+ source types |
| Not quantifying | Always estimate frequency/severity |
| Ignoring context | Note who is complaining |
| Confirmation bias | Document ALL pain points, not just expected |
| No categorization | Categorize to see patterns |

---

## Related Methodologies

- **idea-generation:** Idea Generation
- **problem-validation:** Problem Validation
- **competitor-analysis:** Competitor Analysis
- **user-interviews:** User Interviews
- **jobs-to-be-done:** Jobs to Be Done

---

## Agent

**faion-pain-point-researcher-agent** helps discover pain points. Invoke with:
- "Find pain points for [audience]"
- "Research pain points on Reddit for [topic]"
- "Score these pain points: [list]"
- "What are the top pain points in [industry]?"

---

*Methodology | Research | Version 1.0*
