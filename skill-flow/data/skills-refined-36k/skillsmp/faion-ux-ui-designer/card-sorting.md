---
id: card-sorting
name: "Card Sorting"
domain: UX
skill: faion-ux-ui-designer
category: "ux-design"
---

# Card Sorting

## Metadata
- **Category:** UX / Research Methods
- **Difficulty:** Beginner
- **Tags:** #methodology #ux #research #information-architecture #card-sorting
- **Agent:** faion-ux-researcher-agent

---

## Problem

You do not know how users think about your content. Navigation categories make sense to you but not to users. Users cannot find information because it is organized by internal logic. Menu structures mirror org charts instead of user mental models.

Without card sorting:
- Navigation does not match user expectations
- Users cannot find content
- High search usage (navigation failure)
- Frustrated users

---

## Framework

### What is Card Sorting?

Card sorting asks users to organize topics into categories that make sense to them. It reveals how users naturally group information and what labels they expect.

### Card Sorting Types

| Type | Description | When to Use |
|------|-------------|-------------|
| **Open** | Users create categories | Early exploration |
| **Closed** | Users sort into predefined categories | Validate structure |
| **Hybrid** | Predefined + user can add | Refine existing IA |

---

## Process

### Step 1: Define Goals

```
What do you want to learn?
- How do users group our content?
- What labels make sense to users?
- Does our navigation match mental models?
```

### Step 2: Prepare Cards

**Card selection:**
- 30-60 items typical
- Real content labels
- Avoid jargon
- Representative of full content

### Step 3: Choose Format

| Format | Pros | Cons |
|--------|------|------|
| **In-person** | Rich discussion, follow-up | Time, logistics |
| **Remote** | Scale, convenience | Less insight |
| **Physical** | Tangible, natural | Limited scale |
| **Digital** | Easy analysis, scalable | Less engagement |

### Step 4: Recruit Participants

- 15-20 participants for open sort
- 30+ for closed sort (statistical)
- Match target users
- Mix of experience levels

### Step 5: Conduct Sessions

**Open sort instructions:**
```
"Please organize these cards into groups that make sense
to you. You can create as many groups as you need.
When done, give each group a name."
```

**Closed sort instructions:**
```
"Please place each card into one of these categories.
If a card doesn't fit anywhere, put it in 'Doesn't Fit'."
```

### Step 6: Analyze Results

**Metrics:**
- Agreement rate (how often items grouped together)
- Category similarity
- Standardization (consistency across participants)

---

## Templates

### Card Sort Plan Template

```markdown
# Card Sort Plan: [Project]

**Date:** [Date]
**Researcher:** [Name]

## Objectives
What questions will this answer?
1. [Question 1]
2. [Question 2]

## Method
- **Type:** Open / Closed / Hybrid
- **Format:** In-person / Remote
- **Tool:** [Tool name]
- **Duration:** [X] minutes

## Participants
- **Number:** [X] participants
- **Profile:** [Target user description]
- **Recruitment:** [How recruited]

## Cards

| # | Card Label | Notes |
|---|------------|-------|
| 1 | [Label] | [If needed] |
| 2 | [Label] | |
| ... | | |

## Categories (Closed Sort Only)
- [Category 1]
- [Category 2]
- [Category 3]

## Analysis Plan
- [How you will analyze results]

## Timeline
- Prep: [Date]
- Sessions: [Dates]
- Analysis: [Date]
- Report: [Date]
```

### Card Sort Results Template

```markdown
# Card Sort Results: [Project]

**Date:** [Date]
**Participants:** [N]
**Type:** [Open/Closed]

## Summary
[High-level findings]

## Category Structure (Open Sort)

### User-Created Categories

| Category Name | Frequency | Cards Included |
|---------------|-----------|----------------|
| [Name] | [X participants] | [Cards] |

### Agreement Matrix
[Show which cards were grouped together]

## Placement Results (Closed Sort)

| Card | Category 1 | Category 2 | Category 3 |
|------|------------|------------|------------|
| [Card] | [X%] | [Y%] | [Z%] |

## Key Insights

### Strong Agreements
- [Cards that were consistently grouped]

### Disagreements
- [Cards with no clear home]

### Surprising Findings
- [Unexpected groupings]

## Recommendations

### Navigation Structure
[Recommended categories based on results]

### Labels
[Recommended terminology]

### Further Research
[Areas needing more investigation]
```

---

## Examples

### Open Sort Example

**Content:** E-commerce product categories

**Results:**
- 15 of 20 users grouped "Laptops" and "Desktops" together
- Users called this category "Computers" (not "Computing Devices")
- "Tablets" split: 8 users with computers, 7 with phones

**Insight:** Create "Computers" category, test tablet placement.

### Closed Sort Example

**Categories:** Electronics, Home, Clothing

**Results:**
| Item | Electronics | Home | Clothing |
|------|-------------|------|----------|
| Smart Watch | 85% | 5% | 10% |
| Fitness Tracker | 70% | 10% | 20% |
| Heated Blanket | 40% | 55% | 5% |

**Insight:** Heated blanket category unclear - needs investigation.

---

## Analysis Metrics

### Similarity Matrix

Shows how often pairs of cards were grouped together:

```
High similarity (>70%): Definitely group together
Medium (40-70%): Consider grouping
Low (<40%): Keep separate
```

### Standardization

How consistent were categories across participants?

```
High: Most users created similar categories
Low: Each user had unique approach
```

### Best Merge Method

Algorithmic approach to find optimal groupings based on actual user data.

---

## Common Mistakes

1. **Too many cards** - Over 60 causes fatigue
2. **Jargon on cards** - Use user language
3. **Too few participants** - Need 15+ for patterns
4. **Ignoring outliers** - Unusual groupings may reveal insights
5. **Not asking why** - Follow up on interesting groupings

---

## Remote Card Sorting Tools

| Tool | Features | Best For |
|------|----------|----------|
| **Optimal Workshop** | Full-featured, analysis | Comprehensive studies |
| **UserZoom** | Enterprise integration | Large organizations |
| **Maze** | Modern, quick setup | Fast studies |
| **UXtweak** | Budget-friendly | Smaller teams |

---

## Tree Testing Connection

After card sorting, validate with tree testing:

```
Card Sort → Proposed Structure → Tree Test → Refined Structure
```

Tree testing validates if users can find items in your proposed navigation.

---

## Checklist

- [ ] Clear research questions defined
- [ ] Cards represent real content
- [ ] Cards written in user language
- [ ] 30-60 cards (not too many)
- [ ] Right number of participants
- [ ] Instructions are clear
- [ ] Analysis plan ready
- [ ] Results connect to IA decisions
- [ ] Follow-up research planned if needed

---

## References

- UX research community: Card Sorting
- Information Architecture: For the Web and Beyond
- Optimal Workshop Resources