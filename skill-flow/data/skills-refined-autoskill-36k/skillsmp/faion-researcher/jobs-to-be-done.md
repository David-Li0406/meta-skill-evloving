---
id: jobs-to-be-done
name: "Jobs to Be Done (JTBD)"
domain: RES
skill: faion-researcher
category: "research"
---

# Jobs to Be Done (JTBD)

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Research |
| **Difficulty** | Intermediate |
| **Tags** | #research, #jtbd, #framework |
| **Domain Skill** | faion-researcher |
| **Agents** | faion-pain-point-researcher-agent |

---

## Problem

Product teams focus on features and demographics instead of underlying motivations. Issues:
- "What features should we add?" instead of "What job are we hired for?"
- Copying competitor features without understanding why they work
- Building for personas that don't capture motivation
- Missing the real competition (often non-obvious)

**The root cause:** Focusing on what customers say they want vs. what they're trying to accomplish.

---

## Framework

### What is Jobs to Be Done?

JTBD is a framework that focuses on the progress a customer is trying to make in a specific circumstance. Customers "hire" products to do a "job."

**Key insight:** People don't buy products, they hire them to make progress in their lives.

### The JTBD Formula

```
When [situation/trigger]
I want to [action/motivation]
So I can [outcome/expected result]
```

**Example:**
```
When I finish a client project
I want to send a professional invoice quickly
So I can get paid faster and move on to the next project
```

### Core JTBD Concepts

#### 1. The Job vs. The Solution

| Job (Stable) | Solution (Changes) |
|--------------|-------------------|
| Communicate with distant family | Letters → Phone → Email → Video call |
| Capture and organize thoughts | Paper → Typewriter → Word → Notion |
| Get from A to B quickly | Horse → Car → Uber → Autonomous vehicle |

**Jobs are stable over time. Solutions evolve.**

#### 2. Functional, Emotional, Social Jobs

| Type | Description | Example |
|------|-------------|---------|
| Functional | Get something done | "File my taxes correctly" |
| Emotional | Feel a certain way | "Feel in control of finances" |
| Social | How others perceive me | "Appear financially responsible" |

**Most jobs have all three components.**

#### 3. Hiring and Firing

**Customers hire products when:**
- Progress is needed
- Current solution is inadequate
- New solution promises better outcome

**Customers fire products when:**
- Job is done
- Better alternative exists
- Progress is no longer needed

#### 4. Forces of Progress

Four forces determine switching:

```
         PUSH              PULL
    [Current Pain] + [New Solution Appeal]
           ↓                    ↓
    ======== SWITCH LINE ========
           ↑                    ↑
    [Habit/Comfort] + [Anxiety of New]
        INERTIA            FEAR
```

**To get adoption:** Push + Pull > Habit + Fear

### JTBD Interview Method

#### Step 1: Find Recent Switchers

Interview people who recently:
- Bought your product
- Switched to a competitor
- Started using a category

**Why:** Fresh memory of decision process.

#### Step 2: Reconstruct the Timeline

Map their journey:

```
First Thought → Passive Looking → Active Looking → Decision → Consumption → Satisfaction
      ↓               ↓                ↓              ↓            ↓              ↓
   Trigger      Awareness        Evaluation      Purchase       Usage         Review
```

**Key questions:**
- "When did you first think you needed something different?"
- "What was happening in your life at that point?"
- "What did you try before this?"
- "What almost stopped you from switching?"

#### Step 3: Uncover the Job

Through the interview, identify:

| Element | Question |
|---------|----------|
| Situation | "What was going on when you started looking?" |
| Motivation | "What were you hoping to achieve?" |
| Outcome | "What does success look like?" |
| Constraints | "What limitations did you have?" |

### Job Mapping

For complex jobs, break down into stages:

| Stage | Job Steps | Pain Points |
|-------|-----------|-------------|
| Define | Determine what's needed | Unclear requirements |
| Locate | Find options | Information overload |
| Prepare | Get ready to use | Setup complexity |
| Confirm | Validate choice | Doubt, missing info |
| Execute | Do the core job | Friction, errors |
| Monitor | Check progress | Lack of feedback |
| Modify | Make adjustments | Limited flexibility |
| Conclude | Finish the job | Unclear completion |

---

## Templates

### Job Statement Template

```markdown
## Job Statement: [Product/Feature]

### Core Job
When [situation with emotional context]
I want to [action/motivation]
So I can [functional + emotional outcome]

### Functional Dimension
- Goal: [Specific outcome]
- Metrics: [How success is measured]

### Emotional Dimension
- Desired feeling: [How they want to feel]
- Avoided feeling: [What they want to avoid]

### Social Dimension
- Desired perception: [How they want to be seen]
- Status signal: [What success signals]

### Key Circumstances
- When: [Specific trigger moments]
- Where: [Context/environment]
- Why now: [What changed]

### Competitors (Same Job)
- Direct: [Obvious competitors]
- Indirect: [Non-obvious - doing nothing, workarounds]
- Internal: [Habits, existing processes]
```

### JTBD Interview Template

```markdown
## JTBD Interview: [Person]

### Context
- **Product purchased:** [X]
- **Date of purchase:** [X]
- **Previous solution:** [X]

### Timeline Questions

**First thought:**
"Tell me about when you first started thinking about [category]."
Notes: [X]

**Situation:**
"What was going on in your life/work at that time?"
Notes: [X]

**Passive looking:**
"What did you first look at? How did you hear about options?"
Notes: [X]

**Active looking:**
"When did you start seriously evaluating? What criteria mattered?"
Notes: [X]

**The switch:**
"Walk me through the moment you decided to switch."
Notes: [X]

### Forces Analysis

**Push (Pain with old way):**
- [What was broken]
- "[Quote]"

**Pull (Attraction to new):**
- [What seemed better]
- "[Quote]"

**Habit (Comfort with old):**
- [What they'd miss]
- "[Quote]"

**Fear (Anxiety about new):**
- [What worried them]
- "[Quote]"

### Job Statement (Draft)
When [situation]
I want to [action]
So I can [outcome]
```

### Job Map Template

```markdown
## Job Map: [Core Job]

### Stage 1: Define
**Customer goals:**
- [What they're trying to figure out]

**Current pain:**
- [Where it breaks down]

**Opportunity:**
- [How to help]

### Stage 2: Locate
**Customer goals:**
- [What they're trying to find]

**Current pain:**
- [Where it breaks down]

**Opportunity:**
- [How to help]

### Stage 3: Prepare
[Continue for all 8 stages...]

### Priority Stages
Based on pain severity:
1. [Stage X] - Highest pain
2. [Stage Y] - Medium pain
3. [Stage Z] - Lower pain
```

---

## Examples

### Example 1: Milkshake Job

**Classic JTBD case from Clayton Christensen:**

**Situation:** Commuters buying milkshakes at 7am

**Surface understanding:** They want breakfast

**JTBD understanding:**
```
When I have a long, boring commute
I want something to do with my hand and that lasts 20 minutes
So I can make the drive less boring and arrive less hungry
```

**Competitors:** Not other milkshakes, but donuts, bananas, bagels, podcasts

**Implication:** Make milkshake thicker (lasts longer), add chunks (interesting)

### Example 2: CRM Software

**Surface understanding:** "We need to manage contacts"

**JTBD understanding:**
```
When I'm trying to close more deals
I want to know where each prospect is and what to do next
So I can hit my quota and not let opportunities slip
```

**Forces for switching to new CRM:**
- Push: Old CRM is clunky, loses data
- Pull: New one has automation, mobile app
- Habit: Team knows old system
- Fear: Migration might lose contacts

### Example 3: Online Course

**Surface:** "I want to learn Python"

**JTBD:**
```
When I'm stuck in a dead-end job
I want to gain a skill that's in demand
So I can switch careers and earn more money
```

**Real competition:** Not other Python courses, but also:
- Bootcamps
- Getting an MBA
- Networking for promotions
- Starting a business

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Asking "what features?" | Ask "what are you trying to accomplish?" |
| Focusing on demographics | Focus on circumstances and motivations |
| Ignoring emotional job | Always capture functional + emotional |
| Narrow competitor view | Consider all ways to get the job done |
| Static job definition | Jobs have context and change |
| Skipping forces analysis | Understand why people do/don't switch |

---

## Related Methodologies

- **problem-validation:** Problem Validation
- **persona-building:** Persona Building
- **user-interviews:** User Interviews
- **user-story-mapping:** User Story Mapping
- **user-journey-mapping:** User Journey Mapping

---

## Agent

**faion-pain-point-researcher-agent** helps with JTBD analysis. Invoke with:
- "What's the job for [product/feature]?"
- "Create a job statement for [audience]"
- "Map the job for [process]"
- "Analyze switching forces for [product]"

---

*Methodology | Research | Version 1.0*
