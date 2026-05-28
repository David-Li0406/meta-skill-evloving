---
name: review-coaching-guide
description: Generate a coaching guide from code review feedback to help tech leads conduct effective review discussions. Use when the user wants to discuss review items with authors, create discussion questions, or prepare for 1:1 code review sessions.
---

# Review Coaching Guide

Transform structured code review feedback into a coaching conversation guide that helps reviewers:
- Understand author's decision-making process
- Guide authors to discover issues through questions
- Teach the reasoning behind suggestions

## Prerequisites

One of these files must exist:
- `.claude/code-review.md` (preferred - comprehensive review)
- `.claude/reviewer-feedback.md` (alternative - processed reviewer notes)

## Workflow

### Step 1: Read Review Input

1. Check for `.claude/code-review.md` first
2. If not found, check `.claude/reviewer-feedback.md`
3. If neither exists, display error:
   ```
   Error: No review feedback found.

   Run one of these first:
   - `/code-review` to generate AI code review
   - `/process-reviewer-feedback` to process your manual notes
   ```

### Step 2: Generate Coaching Guide

For each review item, generate a coaching section with:

#### A. What Author Did Well (Lead With This)
Acknowledge positives before discussing issues:
- What the author got right in this area
- Working aspects of their implementation
- Good instincts or patterns they followed
- Foundation they built that we're improving on

#### B. Understanding Questions (Ask Second)
Questions to understand author's thinking before suggesting changes:
- "What led you to this approach?"
- "What alternatives did you consider?"
- "What constraints were you working with?"

#### C. Discovery Questions (Socratic Method)
Questions that guide author to discover the issue themselves:
- Lead author toward the problem without stating it directly
- Build on their domain knowledge
- Help them see edge cases or implications

#### D. Teaching Points (If Needed)
When direct teaching is appropriate:
- Explain the "why" behind the suggestion
- Connect to broader principles (SOLID, DRY, etc.)
- Share relevant project conventions

#### E. Discussion Prompts
Open-ended questions for deeper exploration:
- Trade-offs to consider together
- Alternative approaches to evaluate
- Future implications to discuss

### Step 3: Structure Output

Write to `.claude/coaching-guide.md`:

```markdown
# Code Review Coaching Guide

**Review Source:** <code-review.md or reviewer-feedback.md>
**Generated:** <date>
**Purpose:** Discussion guide for 1:1 review session with author

---

## How to Use This Guide

1. **Acknowledge first** - Start each item with "What Author Did Well"
2. **Understand their thinking** - Ask the "Understanding Questions"
3. **Guide discovery** - Use "Discovery Questions" to help author see issues
4. **Teach when needed** - Use "Teaching Points" only if discovery doesn't work
5. **Explore together** - End with "Discussion Prompts" for collaborative learning

---

## Review Items

### [Priority] Item #N: <title>

**File:** `<file:line>`
**Issue Summary:** <brief description>

#### What Author Did Well
> Acknowledge before discussing the issue

- <what they got right in this area>
- <working aspects of their implementation>
- <good instincts or foundation they built>

#### Understanding Questions
> Ask these to understand author's perspective

- <question about their approach>
- <question about constraints they faced>
- <question about alternatives considered>

#### Discovery Questions
> Guide author to discover the issue themselves

- <leading question 1>
- <leading question 2>
- <question about edge cases>
- <question about implications>

#### Teaching Points
> Use if discovery approach doesn't reveal the issue

**Core Concept:** <principle or pattern being applied>

**Why This Matters:**
- <reason 1>
- <reason 2>

**Project Convention:** <relevant project standard if applicable>

#### Discussion Prompts
> For collaborative exploration

- <trade-off to discuss>
- <alternative approach to consider>
- <follow-up learning opportunity>

---

[Repeat for each review item]
```

### Step 4: Prioritize Items

Order items in the guide by teaching value:
1. **Blocking items** - These are learning priorities
2. **Pattern issues** - Issues that repeat across codebase teach broader lessons
3. **Architectural concerns** - These build understanding of system design
4. **Nits** - Lower priority, but can teach conventions

### Step 5: Add Session Planning Section

At the end of the guide, add:

```markdown
---

## Session Planning

### Estimated Discussion Time
- Blocking items: ~<N> minutes each
- Important items: ~<N> minutes each
- Nits: ~<N> minutes total (can batch)

### Suggested Session Structure

1. **Opening (2 min)**
   - Acknowledge good aspects of the PR
   - Set collaborative tone

2. **Core Discussion (<N> min)**
   - Focus on blocking/important items
   - Use discovery approach first

3. **Quick Wins (<N> min)**
   - Cover nits briefly
   - Author can self-fix most

4. **Wrap-up (3 min)**
   - Summarize key learnings
   - Agree on action items
   - Offer follow-up support

### Positive Observations
> Start the session by acknowledging these

- <good practice observed in PR>
- <improvement from previous work>
- <clever solution worth highlighting>
```

## Question Generation Patterns

### For Validation Issues
**Understanding:** "What validation does this need in production?"
**Discovery:** "What happens if a user submits X without selecting Y?"
**Teaching:** "Form objects validate user input at the boundary..."

### For Missing Edge Cases
**Understanding:** "What edge cases did you consider?"
**Discovery:** "What if this collection is empty? What if it's already processed?"
**Teaching:** "Defensive programming helps us handle unexpected states..."

### For Convention Violations
**Understanding:** "How did you decide on this approach?"
**Discovery:** "Have you seen how X is handled in <similar file>?"
**Teaching:** "Our project convention for this is... because..."

### For Architectural Concerns
**Understanding:** "How does this fit with the existing architecture?"
**Discovery:** "What happens when another module needs this data?"
**Teaching:** "Single responsibility principle suggests... so that..."

### For Performance Issues
**Understanding:** "What's the expected data volume here?"
**Discovery:** "What happens when this list grows to 1000 items?"
**Teaching:** "N+1 queries compound because... We use eager loading to..."

## Identifying Positives

For each review item, find something genuine to acknowledge:

### For Validation Issues
- "You set up the form property correctly"
- "The happy path works as expected"
- "You understood the business requirement"

### For Missing Edge Cases
- "The main flow is solid"
- "You handled the common cases well"
- "The foundation is there to build on"

### For Convention Violations
- "The code works and solves the problem"
- "You followed the pattern you saw elsewhere"
- "This approach is consistent with existing code"

### For Architectural Concerns
- "You got the feature working end-to-end"
- "The separation of concerns is close"
- "You used existing patterns as reference"

### For Test Issues
- "You wrote tests - that's the right instinct"
- "The test structure follows conventions"
- "You identified the scenarios that need coverage"

**Key principle:** Every issue exists because the author tried something. Acknowledge the effort and working parts before discussing improvements.

## Tone Guidelines

- **Curious, not accusatory:** "I'm curious about..." not "Why didn't you..."
- **Collaborative:** "Let's think through..." not "You should have..."
- **Growth-focused:** "This is a great learning opportunity" not "This is wrong"
- **Specific:** Reference actual code, not abstract principles

## Output

After generating, display:

```
Generated `.claude/coaching-guide.md`

Summary:
- <N> blocking items (estimated <N> min discussion each)
- <N> important items
- <N> nits

Suggested session length: <N> minutes

Tips for the session:
1. Start by acknowledging what the author did well
2. Use discovery questions before revealing issues
3. Focus on the "why" not just the "what to fix"
```
