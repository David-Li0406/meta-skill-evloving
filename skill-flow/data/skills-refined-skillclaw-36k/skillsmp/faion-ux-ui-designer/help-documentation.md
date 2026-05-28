---
id: help-documentation
name: "Help and Documentation"
domain: UX
skill: faion-ux-ui-designer
category: "ux-design"
---

# Help and Documentation

## Metadata
- **Category:** UX / Usability Heuristic #10
- **Difficulty:** Beginner
- **Tags:** #methodology #ux #heuristics #nielsen-norman #help
- **Agent:** faion-usability-agent

---

## Problem

Users get stuck and cannot find help. Documentation exists but is hard to find. Help content is outdated or too technical. Users must leave the interface to find answers. Help does not address what users actually struggle with.

Without effective help:
- Users give up
- Increased support costs
- Frustrated customers
- Poor adoption

---

## The Heuristic

**Usability Heuristic #10:** Even though it is better if the system can be used without documentation, it may be necessary to provide help and documentation. Any such information should be easy to search, focused on the user's task, list concrete steps to be carried out, and not be too large.

---

## Framework

### Help Hierarchy

```
1. Interface design (no help needed - best)
2. Inline help (contextual hints)
3. Tooltips (hover information)
4. Guided tours (onboarding)
5. FAQs (common questions)
6. Documentation (detailed reference)
7. Support (human assistance - last resort)
```

### Help Principles

1. **Contextual** - Help where the user needs it
2. **Task-focused** - Organized by user goals
3. **Searchable** - Easy to find answers
4. **Concise** - Brief and to the point
5. **Current** - Kept up to date

---

## Implementation Patterns

### Inline Help

**Field hints:**
```
Label: Password
Hint: Use 8+ characters with letters and numbers
[Password field]
```

**Placeholder text:**
```
[Search products, categories, or brands]
```

### Tooltips

**Icon tooltips:**
```
[?] hover → "This setting controls notification frequency"
```

**Feature explanation:**
```
[i] hover → Brief explanation of feature
```

### Contextual Help Panels

**Sidebar help:**
```
Page-specific help in collapsible sidebar
Shows relevant information for current task
```

### Guided Tours

**Onboarding tour:**
```
Step 1: "This is your dashboard"
Step 2: "Click here to create new project"
Step 3: "Invite team members here"
[Skip] [Next]
```

### Knowledge Base

**Searchable documentation:**
```
Search: "how to reset password"
Results: Password reset instructions
Categories: Account, Security, Getting Started
```

### FAQs

**Common questions:**
```
Q: How do I change my email address?
A: Go to Settings → Account → Email → [Change Email]
```

---

## Templates

### Help Content Template

```markdown
# How to [Task Name]

**Difficulty:** Beginner / Intermediate / Advanced
**Time required:** X minutes
**Prerequisites:** [What user needs before starting]

## Overview
[Brief description of what this guide covers]

## Steps

### Step 1: [Action]
[Detailed instruction]
[Screenshot if helpful]

### Step 2: [Action]
[Detailed instruction]

### Step 3: [Action]
[Detailed instruction]

## Result
[What user should see when complete]

## Troubleshooting

**Problem:** [Common issue]
**Solution:** [How to fix]

## Related Topics
- [Link to related help article]
- [Link to related help article]
```

### Help Audit Template

```markdown
# Help Audit: [Product/Feature]

**Date:** [Date]
**Reviewer:** [Name]

## Help Availability

| Location | Help Available? | Type | Quality |
|----------|-----------------|------|---------|
| [Page/Feature] | Y/N | [Type] | [Rating] |

## Common User Questions

| Question | Answer Available? | Findable? | Notes |
|----------|-------------------|-----------|-------|
| [Question] | Y/N | Y/N | [Notes] |

## Help Content Quality

| Content | Current? | Accurate? | Clear? | Task-focused? |
|---------|----------|-----------|--------|---------------|
| [Content] | Y/N | Y/N | Y/N | Y/N |

## Gaps Identified

| Gap | Impact | Recommendation |
|-----|--------|----------------|
| [Gap] | H/M/L | [Fix] |

## Priority Improvements

1. [Top priority]
2. [Second priority]
3. [Third priority]
```

---

## Examples

### Good Examples

**Notion:**
- Contextual ? icon on each feature
- Searchable help center
- Video tutorials
- Template gallery (learning by example)

**Stripe:**
- Comprehensive documentation
- Code examples
- Interactive API explorer
- Contextual tooltips in dashboard

**Slack:**
- Slackbot answers questions
- Keyboard shortcut guide (?/)
- Getting started checklist
- Searchable help center

### Bad Examples

**Hidden help:**
```
Help buried in footer
No contextual assistance
Users must search entire site
```

**Outdated documentation:**
```
Screenshots from old version
Features that no longer exist
Broken links
```

**Technical overload:**
```
Documentation assumes expertise
No beginner content
Jargon without explanation
```

---

## Types of Help Content

### Onboarding

| Type | When | Purpose |
|------|------|---------|
| Welcome tour | First login | Introduce key features |
| Empty states | New sections | Explain what goes here |
| Progress checklist | Early use | Guide setup completion |

### In-Context

| Type | When | Purpose |
|------|------|---------|
| Tooltips | Hover | Explain specific elements |
| Inline hints | Always visible | Guide input |
| ? icons | On demand | Detailed explanation |

### Reference

| Type | When | Purpose |
|------|------|---------|
| FAQs | Common questions | Quick answers |
| How-tos | Task guidance | Step-by-step |
| Reference docs | Deep details | Complete information |

### Support

| Type | When | Purpose |
|------|------|---------|
| Search | Self-service | Find answers |
| Chat | Need assistance | Human help |
| Email | Complex issues | Detailed support |

---

## Common Mistakes

1. **No help exists** - Users left completely alone
2. **Help is hidden** - Cannot find the help
3. **Help is outdated** - Documentation not maintained
4. **Help is too long** - Overwhelming amount of content
5. **Help is technical** - Written for experts, not users

---

## Measuring Help Effectiveness

| Metric | What to Measure |
|--------|-----------------|
| Help searches | What users look for |
| Search success | Do users find answers? |
| Support tickets | Questions that help should answer |
| Feature adoption | Does help increase usage? |
| Time to proficiency | Learning speed with help |

---

## Accessibility Requirements

- Help content is screen reader accessible
- Help navigation is keyboard accessible
- Videos have captions
- Text is readable (contrast, size)
- Help works on mobile

---

## Checklist

- [ ] Help is accessible from anywhere in app
- [ ] Search functionality works well
- [ ] Contextual help is available
- [ ] Content is task-focused
- [ ] Documentation is current
- [ ] Help is written in plain language
- [ ] Steps are concrete and specific
- [ ] Related topics are linked
- [ ] Onboarding helps new users
- [ ] Support options are available

---

## References

- UX research community: 10 Usability Heuristics
- Don't Make Me Think by Steve Krug
- Content Strategy for Help