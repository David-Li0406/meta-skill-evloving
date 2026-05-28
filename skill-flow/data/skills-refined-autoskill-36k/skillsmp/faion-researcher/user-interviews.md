---
id: user-interviews
name: "User Interviews"
domain: RES
skill: faion-researcher
category: "research"
---

# User Interviews

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Research |
| **Difficulty** | Beginner |
| **Tags** | #research, #interviews, #users |
| **Domain Skill** | faion-researcher |
| **Agents** | faion-persona-builder-agent |

---

## Problem

Founders skip user interviews or conduct them poorly. Common issues:
- Asking leading questions
- Pitching instead of listening
- Accepting "I would" instead of "I did"
- Not reaching enough people
- No systematic analysis of findings

**The root cause:** No framework for extracting honest, actionable insights.

---

## Framework

### What are User Interviews?

User interviews are structured conversations with target customers to understand their problems, behaviors, and needs. They answer: "What do people actually experience?"

### The Mom Test Principles

From Rob Fitzpatrick's "The Mom Test":

1. **Talk about their life, not your idea**
2. **Ask about specifics in the past, not generics about the future**
3. **Talk less, listen more**

**Good vs Bad Questions:**

| Bad (Hypothetical) | Good (Behavioral) |
|--------------------|-------------------|
| "Would you use this?" | "How do you solve this now?" |
| "Do you like this idea?" | "What did you try last time?" |
| "How much would you pay?" | "What have you paid for solutions?" |
| "Is this a problem?" | "Tell me about the last time..." |

### Interview Process

#### Step 1: Define Research Goals

**Template:**
```
We want to learn:
1. [Specific question about behavior]
2. [Specific question about pain points]
3. [Specific question about current solutions]

We'll know we're done when:
- [Criteria for enough interviews]
- [Pattern threshold]
```

#### Step 2: Recruit Participants

**Sources:**

| Source | How to Access | Response Rate |
|--------|---------------|---------------|
| LinkedIn | Cold DM | 5-10% |
| Twitter/X | Reply + DM | 10-20% |
| Reddit | Post in niche subs | Varies |
| Communities | Slack/Discord | 20-30% |
| Cold email | Find company emails | 2-5% |
| Referrals | Ask interviewees | 40%+ |

**Outreach template:**
```
Hi [Name],

I'm researching [topic] and noticed you [relevant context].
Would you spare 20 minutes to share your experience with [problem]?

No selling - just trying to understand the problem better.
Happy to share findings afterward or [offer incentive].

Best,
[Your name]
```

#### Step 3: Prepare Interview Script

**Structure (20-30 minutes):**

| Section | Duration | Purpose |
|---------|----------|---------|
| Warm-up | 2-3 min | Build rapport, explain format |
| Context | 3-5 min | Understand their situation |
| Problem exploration | 10-15 min | Dig into experiences |
| Solutions tried | 5 min | What they've used |
| Wrap-up | 2-3 min | Ask for referrals |

**Key question types:**

| Type | Example |
|------|---------|
| Open-ended | "Walk me through how you handle X" |
| Follow-up | "Tell me more about that" |
| Specific | "What happened last time?" |
| Quantifying | "How often does this occur?" |
| Emotional | "How did that make you feel?" |

#### Step 4: Conduct the Interview

**Do:**
- Record (with permission)
- Take brief notes on emotions/reactions
- Follow their lead, not your script
- Ask "why" 5 times to get to root
- Sit with silence - let them think

**Don't:**
- Pitch your solution
- Correct or argue
- Fill silences immediately
- Ask multiple questions at once
- Accept vague answers

#### Step 5: Analyze Findings

**After each interview:**
```markdown
## Interview: [Name]
**Date:** [X]
**Duration:** [X] min

### Key quotes
1. "[Quote]" - re: [topic]
2. "[Quote]" - re: [topic]

### Pain points identified
1. [Pain] - Severity: [1-5]
2. [Pain] - Severity: [1-5]

### Current solutions
- [What they use]
- [What they've tried]

### Surprising insights
- [Anything unexpected]

### Follow-up questions
- [What to ask in next interviews]
```

**Pattern analysis (after 5+ interviews):**

| Pattern | Frequency | Confidence |
|---------|-----------|------------|
| [Finding] | X of Y interviews | High/Medium/Low |

---

## Templates

### Interview Script Template

```markdown
## Interview Script: [Research Topic]

### Goals
Learn about:
1. [Goal 1]
2. [Goal 2]
3. [Goal 3]

### Warm-up (2 min)
"Thanks for chatting with me. I'm researching [topic] and trying to understand how people handle [problem]. This is not a sales call - I'm just learning. Mind if I record? I'll keep it confidential."

"First, tell me a bit about your role/situation."

### Context Questions (3 min)
1. "What does a typical day/week look like for you?"
2. "What are your main priorities right now?"
3. "Where does [topic] fit into your work?"

### Problem Exploration (12 min)
4. "Walk me through the last time you dealt with [problem]."
5. "What happened?" [Let them tell story]
6. "How did you handle it?"
7. "What was the hardest part?"
8. "How often does this come up?"
9. "What happens if you don't solve this?"

### Solutions & Alternatives (5 min)
10. "What have you tried to solve this?"
11. "How did that work out?"
12. "What do you use now?"
13. "What do you like/dislike about current solution?"
14. "What would the ideal solution look like?"

### Wrap-up (3 min)
15. "Is there anything I should have asked but didn't?"
16. "Do you know 2-3 other people who face similar challenges?"
17. "Can I follow up if I have more questions?"

"Thanks so much - this was really helpful."

### Post-Interview Notes
[Complete immediately after]
```

### Interview Synthesis Template

```markdown
## Interview Synthesis: [Research Topic]

### Summary
- **Interviews conducted:** [X]
- **Date range:** [X to X]
- **Target profile:** [Who]

### Top Findings

#### Finding 1: [Title]
**Frequency:** X of Y interviews
**Evidence:**
- "[Quote 1]"
- "[Quote 2]"
**Implication:** [What this means]

#### Finding 2: [Title]
...

### Pain Point Ranking

| Pain Point | Frequency | Severity | Opportunity |
|------------|-----------|----------|-------------|
| [Pain 1] | X/Y | High | [Y/N] |
| [Pain 2] | X/Y | Medium | [Y/N] |

### Current Solutions Used

| Solution | Users | Satisfaction |
|----------|-------|--------------|
| [Tool/process] | X/Y | High/Med/Low |

### Unexpected Insights
1. [Insight]
2. [Insight]

### Questions Resolved
- [Question]: [Answer based on research]

### Open Questions
- [Still need to learn]

### Recommendations
1. [Action to take]
2. [Action to take]
```

---

## Examples

### Example 1: Interviewing Freelance Designers

**Goal:** Understand project management pain points

**Sample script questions:**
- "Walk me through your last client project from start to finish"
- "Where did things get complicated?"
- "How do you track what's done and what's pending?"
- "What happens when scope changes?"

**Findings (from 12 interviews):**
- 10/12 use spreadsheets or Notion (not PM tools)
- Main pain: scope creep without payment increase
- Average 3 hours/week lost to "project admin"
- Would pay $10-20/month for simple solution

### Example 2: Interviewing SaaS Founders

**Goal:** Understand analytics needs

**Sample script questions:**
- "How do you know if your product is doing well?"
- "Walk me through the last time you checked metrics"
- "What decisions have you made based on data?"
- "What data do you wish you had?"

**Findings (from 8 interviews):**
- 6/8 use Mixpanel/Amplitude but check monthly at most
- Main pain: "Too many dashboards, no clear signal"
- Want: "One number that tells me health"
- Existing tools feel "enterprise-y"

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Asking "Would you use...?" | Ask "How do you handle this now?" |
| Pitching your solution | Save ideas for the end or not at all |
| Only positive feedback | Actively seek pain and negatives |
| Leading questions | Start open-ended, let them lead |
| Too few interviews | Minimum 10 for patterns |
| No recording | Always record (with consent) |
| Not asking for referrals | End every interview with referral ask |
| Immediate synthesis | Let patterns emerge over interviews |

---

## Related Methodologies

- **problem-validation:** Problem Validation
- **pain-point-research:** Pain Point Research
- **persona-building:** Persona Building
- **jobs-to-be-done:** Jobs to Be Done
- **user-research-methods:** User Research Methods

---

## Agent

**faion-persona-builder-agent** helps with user interviews. Invoke with:
- "Create interview script for [audience]"
- "Analyze these interview notes: [data]"
- "What patterns do you see in [findings]?"
- "How many interviews do I need for [topic]?"

---

*Methodology | Research | Version 1.0*
