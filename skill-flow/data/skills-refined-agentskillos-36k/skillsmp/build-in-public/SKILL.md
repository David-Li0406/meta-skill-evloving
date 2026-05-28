---
name: build-in-public
description: "Use when sharing development progress publicly. Covers progress sharing, changelog writing, social media updates, community engagement, and milestone announcements."
---

# Build in Public

## Overview

Patterns for transparent development and effective public communication. Covers progress sharing, changelog writing, social media updates, community engagement, and milestone announcements. Build trust and audience while shipping.

## When to Use

- Building a product with public progress updates
- Maintaining a changelog
- Announcing releases and milestones
- Growing an audience through development journey
- Engaging with developer communities

## Quick Reference

| Update Type | Frequency | Platform |
|-------------|-----------|----------|
| **Ship Log** | Daily/Weekly | Twitter, Blog |
| **Changelog** | Per release | Website, GitHub |
| **Milestone** | Monthly | All platforms |
| **Deep Dive** | Monthly | Blog, Newsletter |
| **Retrospective** | Quarterly | Blog, Newsletter |

---

## Progress Sharing

### Daily Ship Log Format

```markdown
## Ship Log: [Date]

### Shipped Today
- [Feature/fix]: [Brief description]
- [Feature/fix]: [Brief description]

### In Progress
- [What I'm working on]

### Learnings
- [Insight or lesson]

### Tomorrow
- [Next priority]

---
#buildinpublic #[project]
```

### Weekly Update Format

```markdown
## Week [N] Update: [Project Name]

### Summary
[2-3 sentences on overall progress]

### Highlights
- [Achievement 1]
- [Achievement 2]
- [Achievement 3]

### Metrics
- Users: [X] (+Y%)
- Revenue: $[X] (+Y%)
- [Custom metric]: [Value]

### Challenges
- [Challenge faced and how resolved]

### Next Week
- [ ] [Goal 1]
- [ ] [Goal 2]
- [ ] [Goal 3]

### Screenshot/Demo
[Include visual progress when possible]
```

### Monthly Retrospective

```markdown
## Month [N] Retrospective: [Project Name]

### The Numbers
| Metric | Start | End | Change |
|--------|-------|-----|--------|
| Users | X | Y | +Z% |
| Revenue | $X | $Y | +Z% |
| Features | X | Y | +Z |

### What Shipped
1. **[Feature]**: [Impact description]
2. **[Feature]**: [Impact description]
3. **[Feature]**: [Impact description]

### What Worked
- [Strategy/approach that succeeded]
- [Decision that paid off]

### What Didn't Work
- [Approach that failed]
- [Lesson learned]

### Key Learnings
1. [Learning with context]
2. [Learning with context]

### Next Month Goals
- [ ] [Measurable goal]
- [ ] [Measurable goal]
- [ ] [Measurable goal]
```

---

## Changelog Writing

### Changelog Format (Keep a Changelog)

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New feature description

### Changed
- Existing functionality that changed

### Deprecated
- Features that will be removed

### Removed
- Features that were removed

### Fixed
- Bug fixes

### Security
- Security updates

## [1.0.0] - 2024-01-15

### Added
- Initial release with core features
- User authentication
- Dashboard
```

### Release Notes Template

```markdown
# [Project] v[X.Y.Z] Release Notes

**Release Date**: [Date]

## Highlights

[2-3 sentence summary of most important changes]

## New Features

### [Feature Name]
[Description with screenshot/gif if applicable]

**How to use:**
1. [Step 1]
2. [Step 2]

### [Feature Name]
[Description]

## Improvements

- **[Area]**: [What improved and why it matters]
- **[Area]**: [What improved and why it matters]

## Bug Fixes

- Fixed [bug description] (#issue)
- Fixed [bug description] (#issue)

## Breaking Changes

- **[Change]**: [Migration guide]

## Upgrade Guide

```bash
npm install [package]@latest
```

[Additional upgrade steps if needed]

## Acknowledgments

Thanks to [contributors] for their contributions!
```

### User-Friendly Changelog

```markdown
## What's New in [Project] - [Month Year]

Hey [user type]!

Here's what we've been building for you:

### [Emoji] [Feature Name]
[Plain language description of benefit]

### [Emoji] [Improvement]
[Plain language description of benefit]

### Bug Squashing
- [Fixed issue in plain terms]
- [Fixed issue in plain terms]

---

Questions? Reply to this email or [contact method].

Happy [using/building/shipping]!
[Your name]
```

---

## Social Media Updates

### Twitter/X Templates

**Ship Update (Short)**
```
Just shipped: [Feature] in [Project]

[1 sentence benefit]

[Screenshot/GIF]

#buildinpublic
```

**Progress Thread**
```
[Project] Week [N] Thread

Here's what I shipped this week:

1/[N]
```

**Milestone Announcement**
```
[Emoji] Milestone: [Achievement]!

[Project] just hit [metric].

Here's how we got here:

[Thread or brief story]

Thank you to everyone using [product]!
```

**Lesson Learned**
```
Lesson from building [Project]:

[Insight in 1-2 sentences]

Context: [Brief story]

The fix: [What I did differently]

#buildinpublic
```

**Asking for Feedback**
```
Building: [Feature]

I'm torn between:
A) [Option A]
B) [Option B]

Which would you prefer and why?

[Screenshot of both options]
```

### LinkedIn Template

```markdown
[Emoji] [Milestone/Achievement] at [Project]

[2-3 paragraphs telling the story]

Key learnings:
- [Learning 1]
- [Learning 2]
- [Learning 3]

If you're interested in [topic], I'm sharing the journey at [link].

#buildinpublic #[relevant hashtags]
```

### Content Calendar Template

| Day | Content Type | Topic |
|-----|--------------|-------|
| Mon | Ship update | Weekend progress |
| Tue | Insight/Lesson | Technical learning |
| Wed | Engagement | Ask question |
| Thu | Behind scenes | Process/tool |
| Fri | Weekly summary | Week highlights |
| Sat | - | Rest |
| Sun | Plan sharing | Next week goals |

---

## Community Engagement

### Announcement Posts

**Product Hunt Launch**
```markdown
# [Product Name] - [Tagline]

Hey Product Hunt!

I'm [Name], and I've been building [Product] for [time period].

## The Problem
[2-3 sentences on the problem]

## The Solution
[What your product does]

## Key Features
- [Feature 1]: [Benefit]
- [Feature 2]: [Benefit]
- [Feature 3]: [Benefit]

## Pricing
[Simple pricing explanation]

## Special for PH
[Any launch offer]

Would love your feedback!
```

**Hacker News Launch**
```markdown
Show HN: [Product Name] - [Concise description]

[1 paragraph on what it is and why you built it]

Tech stack: [Brief stack overview]

Would love feedback, especially on [specific aspect].

[Link]
```

**Reddit Post**
```markdown
[Descriptive title with context]

Hey r/[subreddit],

[Genuine intro - why you're posting here]

**The Problem**: [Context they'll relate to]

**What I Built**: [Brief description]

**Key Features**:
- [Feature relevant to this community]
- [Feature relevant to this community]

**Looking For**: [Specific feedback request]

[Link - follow subreddit rules]

Happy to answer any questions!
```

### Engagement Best Practices

```markdown
## Engagement Guidelines

### DO
- [ ] Respond to every comment
- [ ] Ask follow-up questions
- [ ] Thank people genuinely
- [ ] Share credit with helpers
- [ ] Engage with others' content
- [ ] Be consistent in posting
- [ ] Show vulnerability/struggles
- [ ] Celebrate others' wins

### DON'T
- [ ] Only post about yourself
- [ ] Ignore negative feedback
- [ ] Delete critical comments
- [ ] Use engagement bait
- [ ] Spam communities
- [ ] Fake metrics or progress
- [ ] Overpromise features
- [ ] Ghost after launching
```

---

## Milestone Announcements

### Types of Milestones

| Milestone | Example | Celebration Level |
|-----------|---------|-------------------|
| **User milestones** | 100, 1K, 10K users | High |
| **Revenue milestones** | First $, $1K MRR | High |
| **Feature milestones** | V1, major release | Medium |
| **Personal milestones** | 1 year building | Medium |
| **Technical milestones** | 99.9% uptime | Low-Medium |

### Milestone Post Template

```markdown
## [Emoji] [Project] just hit [Milestone]!

[1-2 sentences of genuine excitement]

### The Journey
[Brief timeline of how you got here]

- [Date]: [Event]
- [Date]: [Event]
- [Date]: Today!

### What Made This Possible
1. [Factor 1]
2. [Factor 2]
3. [Factor 3]

### Learnings
[Most valuable insight from reaching this milestone]

### What's Next
[Your focus going forward]

### Thank You
[Genuine thanks to users/community/supporters]

---

If you're curious about [project]: [Link]

#buildinpublic #milestone
```

### Revenue Milestone (Transparent)

```markdown
## [Project] hit $[X] MRR - Here's everything

[Brief intro on why sharing]

### The Numbers (All of them)
- **MRR**: $[X]
- **Customers**: [Y]
- **ARPU**: $[Z]
- **Churn**: [A]%
- **Runway**: [B] months

### Revenue Breakdown
[Chart or table if possible]

### How We Got Here
[Timeline with key decisions]

### What Didn't Work
[Honest failures]

### What Worked
[Successful strategies]

### Expenses
[Real costs breakdown]

### Net
$[Actual profit/loss]

---

AMA in the comments!
```

---

## Content Templates

### Dev Log Blog Post

```markdown
# Dev Log #[N]: [Title]

*[Date]*

## This Week's Focus
[What I planned to work on]

## What Actually Happened
[Reality vs plan]

## Technical Deep Dive
[One interesting technical challenge]

### The Problem
[What I was trying to solve]

### Approaches Tried
1. [Approach 1]: [Result]
2. [Approach 2]: [Result]

### The Solution
```code
[Relevant code snippet]
```

### Why This Works
[Explanation]

## Metrics Update
| Metric | Last Week | This Week |
|--------|-----------|-----------|
| [Metric] | [Value] | [Value] |

## Next Week
- [ ] [Priority 1]
- [ ] [Priority 2]

## Random Thought
[Something interesting that came up]
```

### Newsletter Template

```markdown
Subject: [Project] Update: [Catchy Summary]

Hey [First Name],

[Personal opening - 1-2 sentences]

## What's New

### [Feature/Update 1]
[Brief description with screenshot]

### [Feature/Update 2]
[Brief description]

## Behind the Scenes
[One interesting story from development]

## Numbers
[Key metrics if sharing publicly]

## What's Coming
[Preview of next updates]

## One Ask
[Specific request - feedback, share, etc.]

---

Thanks for following along!

[Your name]

P.S. [Fun fact or teaser]
```

---

## Consistency Framework

### Building in Public Pledge

```markdown
## My Build in Public Commitment

I commit to:
- [ ] Share progress [frequency]
- [ ] Be honest about failures
- [ ] Respond to feedback
- [ ] Share real numbers
- [ ] Help others building

I will NOT:
- [ ] Fake metrics
- [ ] Hide struggles
- [ ] Spam communities
- [ ] Abandon consistency
```

### Metrics to Track

```markdown
## Build in Public Metrics

### Engagement
- Followers: [X]
- Avg. engagement rate: [Y]%
- Newsletter subscribers: [Z]

### Impact
- Referral signups: [X]
- Community mentions: [Y]
- Press/features: [Z]

### Consistency
- Posts this month: [X]
- Streak: [Y] days
- Response rate: [Z]%
```

---

## Red Flags - STOP

**Never:**
- Fake metrics or progress
- Overpromise timelines
- Ignore negative feedback
- Abandon community after launch
- Spam same content everywhere
- Be inconsistent without explanation

**Always:**
- Be authentic about struggles
- Give credit to helpers
- Respond to comments
- Share real numbers
- Stay consistent
- Celebrate others' wins

---

## Integration

**Related skills:** idea-to-product, analytics, seo-content-generation
**Platforms:** Twitter/X, LinkedIn, Product Hunt, Hacker News, Dev.to
