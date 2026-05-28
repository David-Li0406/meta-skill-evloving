---
id: feedback-management
name: "Feedback Management"
domain: PRD
skill: faion-product-manager
category: "product"
---

# Feedback Management

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Product |
| **Difficulty** | Beginner |
| **Tags** | #product, #feedback, #users |
| **Domain Skill** | faion-product-manager |
| **Agents** | faion-mlp-gap-finder-agent |

---

## Problem

Feedback is collected but not acted upon systematically. Issues:
- Feedback scattered across channels
- Loudest voices dominate decisions
- No way to measure feedback impact
- Users feel unheard

**The root cause:** No structured system for collecting, organizing, and acting on feedback.

---

## Framework

### What is Feedback Management?

Feedback management is the systematic collection, categorization, prioritization, and response to user input. It answers: "What are users telling us and what should we do about it?"

### Feedback Sources

| Source | Type | Volume | Quality |
|--------|------|--------|---------|
| Support tickets | Reactive | High | High (real issues) |
| In-app feedback | Prompted | Medium | Medium |
| App store reviews | Public | Medium | Mixed |
| Social media | Unsolicited | Variable | Variable |
| Sales calls | Prospects | Low | High |
| NPS surveys | Prompted | Medium | Medium |
| User interviews | Solicited | Low | Very High |
| Analytics | Behavioral | High | High (for patterns) |

### Feedback Processing Pipeline

```
COLLECT → CATEGORIZE → ANALYZE → PRIORITIZE → ACT → CLOSE LOOP
    ↓          ↓           ↓          ↓         ↓         ↓
 Sources    Taxonomy    Patterns    RICE     Build    Respond
```

### Feedback Categorization

#### By Type

| Type | Description | Example |
|------|-------------|---------|
| Bug | Something's broken | "Can't save settings" |
| Feature request | New capability | "Need PDF export" |
| Enhancement | Improve existing | "Make it faster" |
| Confusion | UX issue | "Where do I find X?" |
| Praise | Positive feedback | "Love this feature!" |
| Complaint | Negative sentiment | "Frustrated with..." |

#### By Topic

Create a taxonomy specific to your product:
- Onboarding
- Core feature A
- Core feature B
- Billing
- Integrations
- Performance
- etc.

### Feedback Management Process

#### Step 1: Centralize Collection

**Single source of truth:**
- Tool: ProductBoard, Canny, Notion, Linear
- Or: Spreadsheet/database

**Auto-import from:**
- Support tickets (tag with feedback)
- In-app widget
- Email alias (feedback@)
- Social monitoring

#### Step 2: Triage and Categorize

**For each piece of feedback:**
- Type (bug/request/enhancement)
- Topic (category)
- Source (where it came from)
- Segment (who said it)
- Sentiment (positive/neutral/negative)

#### Step 3: Aggregate and Analyze

**Regularly review:**
- Volume by category
- Trends over time
- Top requests by votes/mentions
- Correlation with segments

#### Step 4: Prioritize

**Connect to product process:**
- Link feedback to backlog items
- Use RICE or other prioritization
- Consider segment importance
- Factor in strategic goals

#### Step 5: Act

**For each decision:**
- Build it (add to roadmap)
- Won't do (document why)
- Need more info (research)
- Already planned (link to roadmap)

#### Step 6: Close the Loop

**Tell users what happened:**
- Email updates on shipped features
- "You asked, we delivered" posts
- Individual responses when possible
- Changelog/release notes

---

## Templates

### Feedback Log

```markdown
## Feedback Log: [Product]

### Recent Feedback

| Date | Source | User | Type | Topic | Verbatim | Status |
|------|--------|------|------|-------|----------|--------|
| [Date] | [Source] | [ID] | Request | [Topic] | "[Quote]" | Triaged |
| [Date] | [Source] | [ID] | Bug | [Topic] | "[Quote]" | Linked |

### By Category (This Month)

| Topic | Count | Top Request | Action |
|-------|-------|-------------|--------|
| [Topic 1] | [X] | [Request] | [Status] |
| [Topic 2] | [X] | [Request] | [Status] |

### Top Requests

| Request | Mentions | Segment | Priority | Status |
|---------|----------|---------|----------|--------|
| [Request 1] | [X] | [Who] | High | Planned Q2 |
| [Request 2] | [X] | [Who] | Medium | Researching |
| [Request 3] | [X] | [Who] | Low | Backlog |

### Trends
[Observations about patterns in feedback]
```

### Feedback Response Templates

```markdown
## Feedback Response: Shipped

**Subject:** You asked, we built: [Feature]

Hi [Name],

A few months ago, you requested [feature]. I'm excited to let you know it's now live!

[Brief description of what's new]

You can try it out by [instructions].

Thanks for helping us make [Product] better. Keep the feedback coming!

Best,
[Your name]

---

## Feedback Response: Not Planned

**Subject:** RE: Your request for [Feature]

Hi [Name],

Thanks for sharing your idea about [feature]. We really appreciate the thought!

After careful consideration, we've decided not to pursue this for now because [honest reason].

We're focusing on [what we're doing instead], which should help with [related benefit].

Your feedback is valuable, and we'll keep your suggestion in mind as we evolve.

Best,
[Your name]

---

## Feedback Response: More Info Needed

Hi [Name],

Thanks for the feedback on [topic]!

To better understand your needs, could you tell me more about:
- [Question 1]
- [Question 2]

This will help us prioritize improvements.

Best,
[Your name]
```

---

## Examples

### Example 1: Monthly Feedback Review

**Summary:**
- Total feedback: 150 items
- Top category: Integrations (40%)
- Top request: Slack integration (25 mentions)
- Emerging: Mobile app requests increasing

**Actions:**
- Slack integration: Added to Q2 roadmap
- Mobile: Need more research (scheduling interviews)
- Billing complaints: Fixed 3 bugs

**Close loop:**
- Email to 25 Slack requesters about roadmap addition

### Example 2: App Store Review Response Strategy

**1-2 star reviews:**
- Respond within 24 hours
- Apologize and offer help
- Move to direct support

**3-4 star reviews:**
- Thank and ask what would make it 5 stars
- Note feedback in log

**5 star reviews:**
- Thank and ask for referrals
- Feature in marketing

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Feedback in silos | Centralize in one tool |
| No categorization | Create taxonomy and tag everything |
| Building everything | Prioritize ruthlessly |
| Never responding | Always close the loop |
| Only loudest voices | Segment feedback by user type |
| Ignoring patterns | Regular analysis sessions |
| No link to roadmap | Connect feedback to backlog |

---

## Related Methodologies

- **user-interviews:** User Interviews
- **feature-discovery:** Feature Discovery
- **feature-prioritization-rice:** Feature Prioritization (RICE)
- **aarrr-pirate-metrics:** AARRR Pirate Metrics
- **user-research-methods:** User Research Methods

---

## Agent

**faion-mlp-gap-finder-agent** helps with feedback. Invoke with:
- "Categorize this feedback: [content]"
- "What are the patterns in [feedback list]?"
- "How should I respond to [feedback]?"
- "Prioritize these requests: [list]"

---

*Methodology | Product | Version 1.0*
