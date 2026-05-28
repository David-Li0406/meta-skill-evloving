---
id: elicitation-techniques
name: "Elicitation Techniques"
domain: BA
skill: faion-business-analyst
category: "business-analysis"
---

# Elicitation Techniques

## Metadata
- **Category:** BA Framework / Elicitation and Collaboration
- **Difficulty:** Intermediate
- **Tags:** #methodology #babok #elicitation #requirements #business-analysis
- **Agent:** faion-ba-agent

---

## Problem

Stakeholders cannot articulate what they need. You ask questions but get vague answers. Different stakeholders give contradictory information. Critical requirements are discovered late. The written requirements do not match what stakeholders actually want.

Without proper elicitation:
- Incomplete requirements
- Misunderstood needs
- Late discoveries
- Rework and delays

---

## Framework

### What is Elicitation?

Elicitation is the process of drawing out information from stakeholders about their needs, wants, and constraints. It is not just asking questions - it is using techniques to uncover stated and unstated requirements.

### Elicitation Techniques Overview

| Technique | Best For | Stakeholders |
|-----------|----------|--------------|
| **Interviews** | Deep understanding | Individuals |
| **Workshops** | Consensus, complex topics | Groups |
| **Focus Groups** | User perspectives | Similar users |
| **Observation** | Process understanding | Users at work |
| **Surveys** | Broad input | Many people |
| **Document Analysis** | Existing state | Documents |
| **Prototyping** | Validating ideas | Users, designers |
| **Brainstorming** | Generating ideas | Groups |

---

## Technique Details

### 1. Interviews

**Purpose:** Gather detailed information from individuals.

**When to use:**
- Need deep understanding
- Topic is sensitive
- Stakeholder has unique knowledge

**Preparation:**
1. Define interview objectives
2. Prepare questions (open and closed)
3. Schedule with stakeholder
4. Review relevant background

**Conducting the interview:**
- Start with rapport building
- Use open-ended questions to explore
- Use closed questions to confirm
- Listen actively
- Take notes or record (with permission)

**Question types:**

| Type | Purpose | Example |
|------|---------|---------|
| **Open** | Explore | "Tell me about your process" |
| **Closed** | Confirm | "Do you use this daily?" |
| **Probing** | Dig deeper | "Why is that important?" |
| **Clarifying** | Ensure understanding | "So you mean...?" |

### 2. Workshops

**Purpose:** Bring stakeholders together to collaborate.

**When to use:**
- Need consensus
- Multiple perspectives required
- Complex topic to explore

**Workshop planning:**
1. Define clear objectives
2. Identify participants
3. Create agenda
4. Prepare materials
5. Arrange logistics

**Facilitation tips:**
- Set ground rules
- Manage participation (all voices heard)
- Park off-topic items
- Document decisions
- Summarize and confirm

### 3. Observation

**Purpose:** See how work is actually done.

**Types:**

| Type | Description | Best For |
|------|-------------|----------|
| **Passive** | Watch without interaction | Unbiased view |
| **Active** | Ask questions while observing | Understanding why |
| **Participant** | Join in the work | Deep understanding |

**What to observe:**
- Steps performed
- Tools used
- Time taken
- Exceptions and workarounds
- Pain points

### 4. Document Analysis

**Purpose:** Extract requirements from existing materials.

**Documents to review:**
- Current system documentation
- Process manuals
- Business rules
- Reports and forms
- Regulations and standards
- Previous project documents

**Analysis approach:**
1. Identify relevant documents
2. Review for requirements
3. Note gaps and questions
4. Validate with stakeholders

### 5. Surveys/Questionnaires

**Purpose:** Gather input from many stakeholders.

**When to use:**
- Large stakeholder group
- Need quantitative data
- Geographically distributed

**Question design:**
- Keep questions clear and concise
- Mix question types (multiple choice, rating, open)
- Avoid leading questions
- Test before distributing

### 6. Prototyping

**Purpose:** Validate understanding through tangible examples.

**Types:**

| Type | Fidelity | Purpose |
|------|----------|---------|
| **Paper** | Low | Quick concept validation |
| **Wireframe** | Low-Medium | Layout and flow |
| **Mockup** | Medium-High | Visual design |
| **Working** | High | Functional validation |

---

## Templates

### Interview Guide Template

```markdown
# Interview Guide: [Topic]

**Interviewee:** [Name]
**Role:** [Role]
**Date:** [Date]
**Duration:** [Time]
**Interviewer:** [Name]

## Objectives
- [Objective 1]
- [Objective 2]

## Background Questions
1. [Question about role and experience]
2. [Question about current process]

## Main Questions
1. [Open question about topic]
   - Follow-up: [Probing question]
2. [Question about challenges]
3. [Question about desired outcomes]
4. [Question about constraints]

## Closing Questions
1. What else should I know about [topic]?
2. Who else should I speak with?
3. What documents should I review?

## Notes
[Space for interview notes]

## Action Items
- [Follow-up needed]
```

### Workshop Agenda Template

```markdown
# Workshop Agenda: [Topic]

**Date:** [Date]
**Time:** [Start] - [End]
**Location:** [Room/Virtual]
**Facilitator:** [Name]
**Note-taker:** [Name]

## Objectives
- [Objective 1]
- [Objective 2]

## Participants
- [Name, Role]
- [Name, Role]

## Agenda

| Time | Duration | Topic | Activity | Owner |
|------|----------|-------|----------|-------|
| 9:00 | 10 min | Welcome, objectives | Presentation | Facilitator |
| 9:10 | 30 min | [Topic 1] | [Activity] | [Name] |
| 9:40 | 45 min | [Topic 2] | [Activity] | [Name] |
| 10:25 | 10 min | Break | | |
| 10:35 | 40 min | [Topic 3] | [Activity] | [Name] |
| 11:15 | 15 min | Summary, next steps | Discussion | Facilitator |

## Materials Needed
- [ ] [Material 1]
- [ ] [Material 2]

## Pre-work for Participants
- [What to prepare]

## Output/Deliverables
- [Expected outputs]
```

---

## Examples

### Example 1: Requirements Discovery Interview

**Stakeholder:** Customer Service Manager

**Questions asked:**
1. "Walk me through a typical customer inquiry" (Process understanding)
2. "What are the most common issues your team faces?" (Pain points)
3. "What information do you wish you had access to?" (Needs)
4. "How do you measure success?" (Metrics)
5. "What would ideal look like?" (Vision)

**Insights gathered:**
- Average call takes 12 minutes (7 minutes searching for info)
- 3 different systems checked per call
- No visibility into order status
- Customer satisfaction dropping

### Example 2: Process Mapping Workshop

**Objective:** Map current order fulfillment process

**Participants:** Order entry, Warehouse, Shipping, Customer Service

**Activities:**
1. Each team presents their steps (15 min each)
2. Group maps end-to-end flow (45 min)
3. Identify handoff points and issues (20 min)
4. Prioritize pain points (15 min)

**Output:**
- Current state process map
- List of 12 pain points
- Top 3 priorities for improvement

---

## Common Mistakes

1. **Leading questions** - Suggesting the answer
2. **Not listening** - Waiting to ask next question
3. **Assuming knowledge** - Not validating understanding
4. **Too many techniques** - Overwhelming stakeholders
5. **No preparation** - Wasting stakeholder time

---

## Technique Selection Guide

| Situation | Recommended Technique |
|-----------|----------------------|
| Understand current process | Observation + Interview |
| Gather broad input | Survey + Focus group |
| Build consensus | Workshop |
| Validate design | Prototyping |
| Understand documentation | Document analysis |
| Generate ideas | Brainstorming workshop |
| Deep dive with expert | Interview |

---

## Next Steps

After elicitation:
1. Consolidate and organize findings
2. Validate understanding with stakeholders
3. Identify gaps and conflicts
4. Plan additional elicitation if needed
5. Connect to Requirements Documentation methodology

---

## References

- BA Framework Guide v3 - Elicitation and Collaboration
- BA industry Elicitation Techniques Guide
