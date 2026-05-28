---
name: icp-creator
description: Creates comprehensive Ideal Customer Profile using an easy-to-answer questionnaire approach. Captures demographics, psychographics, pain points, aspirations, objections, and language patterns for precise audience targeting. Use when user wants to create an ICP, mentions "target audience", "customer profile", "who I'm writing for", or needs to document their ideal customer.
---

# ICP Creator

**Purpose:** Guide users through creating a comprehensive Ideal Customer Profile (ICP) using a structured, easy-to-answer questionnaire.

## When to Activate

Use this skill when:
- User wants to create an ICP or customer profile
- User mentions "target audience" or "ideal customer"
- User says "who should I write for?"
- User needs to document their customer persona
- User asks "create ICP" or "profile my audience"

## Core Principle

**ICPs go beyond demographics into psychology:**
- WHO they are (demographics)
- WHAT they feel (psychographics - fears, frustrations, aspirations)
- HOW they think (decision-making, objections, language)
- WHERE they are vs. where they want to be (transformation)

**Keep it practical:** Questions should be answerable from the user's experience, not requiring hours of research.

## Reference Materials

- `references/questionnaire.md` - Complete 19-question interview guide with examples and probes

## Workflow

### Step 1: Introduction

**Present this message:**

```
I'll help you create a comprehensive Ideal Customer Profile (ICP) for your audience. This will become the foundation for all targeted content.

This questionnaire takes about 15-20 minutes and focuses on what you already know about your customers from conversations, sales calls, and interactions.

Don't overthink it - your first instincts about your customers are usually right. You can always refine this later.

Ready? Let's start with the basics.
```

### Step 2: Conduct Interactive Interview

**Read the interview guide first:**
```
Read references/questionnaire.md
```

**Interview approach:**
- Conduct this as a **conversational interview**, not a form
- Ask **ONE question at a time**
- **Wait for response** before moving to next question
- **Probe for specifics** if answer is vague
- **Offer examples** if user seems stuck
- Be flexible - can skip, revisit, or ask follow-ups

**The 7 sections (19 questions total):**

| Section | Questions | Focus |
|---------|-----------|-------|
| 1. Profile Basics | Q1-Q2 | Name and description |
| 2. Demographics | Q3-Q5 | Roles, experience, business stage |
| 3. Psychographics | Q6-Q9 | Values, frustrations, fears, aspirations |
| 4. Current vs. Desired | Q10-Q12 | What they've tried, why it failed, vision |
| 5. Language | Q13-Q14 | How they describe problems, trigger words |
| 6. Objections | Q15-Q16 | Barriers and what convinces them |
| 7. Behavior | Q17-Q19 | Info consumption, timeline, investment |

**Follow the questionnaire guide for:**
- Exact question wording
- Examples to share
- Follow-up probes
- Clarification strategies

### Step 3: Generate ICP JSON

**After collecting all answers, generate:**

```json
{
  "_meta": {
    "title": "Ideal Customer Profile",
    "type": "icp",
    "updated_at": "[Today's date YYYY-MM-DD]"
  },
  "data": {
    "profile_overview": {
      "name": "[From Q1]",
      "tagline": "[From Q2]",
      "core_identity": "[Synthesized from answers]"
    },
    "demographics": {
      "professional_roles": ["[From Q3]"],
      "experience_level": "[From Q4]",
      "business_stage": ["[From Q5]"],
      "technical_comfort": "[Synthesized]"
    },
    "psychographics": {
      "values": ["[From Q6]"],
      "frustrations": ["[From Q7]"],
      "fears": ["[From Q8]"],
      "aspirations": ["[From Q9]"]
    },
    "current_state": {
      "what_theyve_tried": ["[From Q10]"],
      "why_it_hasnt_worked": ["[From Q11]"],
      "current_workflow_pain": ["[Synthesized from Q7 and Q11]"]
    },
    "desired_state": {
      "transformation_vision": "[From Q12]",
      "specific_outcomes": ["[Synthesized from Q9 and Q12]"],
      "identity_shift": "[From current to aspirational identity]",
      "competitive_advantage": "[Synthesized from aspirations]"
    },
    "behavioral_patterns": {
      "information_consumption": ["[From Q17]"],
      "decision_making": ["[From Q18 and Q19]"],
      "learning_preferences": ["[Synthesized]"]
    },
    "language_and_terminology": {
      "how_they_describe_their_problem": ["[From Q13]"],
      "resonant_phrases": ["[Synthesized]"],
      "trigger_words": ["[From Q14]"]
    },
    "objections_and_barriers": {
      "skepticism": ["[From Q15 - skeptical]"],
      "practical_concerns": ["[From Q15 - practical]"],
      "investment_hesitation": ["[From Q15 - investment]"]
    },
    "what_convinces_them": {
      "proof_types": ["[From Q16]"],
      "trust_builders": ["[Synthesized]"],
      "urgency_triggers": ["[Synthesized from fears]"]
    },
    "journey_stages": {
      "awareness": {
        "state": "[Synthesized]",
        "questions": ["[What they ask]"],
        "content_needs": "[What helps]"
      },
      "consideration": {
        "state": "[Synthesized]",
        "questions": ["[What they ask]"],
        "content_needs": "[What helps]"
      },
      "decision": {
        "state": "[Synthesized]",
        "questions": ["[What they ask]"],
        "content_needs": "[What helps]"
      }
    },
    "success_metrics": {
      "how_they_measure_success": ["[From aspirations]"],
      "timeline_expectations": "[From Q18]"
    },
    "buying_behavior": {
      "price_sensitivity": "[From Q19]",
      "decision_timeline": "[From Q18]",
      "research_depth": "[From Q17]",
      "commitment_level": "[Synthesized]"
    }
  }
}
```

### Step 4: Save the File

**Save to:** `/context/core/icp.json`

**Confirm success:**
```
✓ ICP Profile Created!

File saved: /context/core/icp.json

Your ICP captures:
- Profile: [Name from Q1]
- Target roles: [List 2-3 from Q3]
- Core frustrations: [List 2-3 from Q7]
- Key aspirations: [List 2-3 from Q9]
- Main objections: [List 2-3 from Q15]

This profile is now ready to use for targeted content creation.

Would you like me to:
1. Generate test content targeting this ICP?
2. Refine any specific sections?
```

## Quality Guidelines

### Synthesized Sections

Some fields require combining multiple answers:

| Field | Combine From |
|-------|--------------|
| Core Identity | Q1 + Q2 + overall essence |
| Current Workflow Pain | Q7 (frustrations) + Q11 (why failed) |
| Identity Shift | Current state → aspirational from Q12 + Q9 |
| Learning Preferences | Q4 (experience) + Q17 (consumption) |

### Be Specific, Not Generic

**Avoid:**
- "Entrepreneurs who want to grow"

**Aim for:**
- "Content strategists at growing brands frustrated with generic AI output who want to build proprietary systems maintaining their unique voice"

## Updating Existing ICP

If user wants to refine existing ICP:

1. Read current `/context/core/icp.json`
2. Ask what needs updating
3. Show current values for those sections
4. Get new answers
5. Update JSON
6. Update `updated_at` date

---

**Remember:** Great ICPs come from real customer conversations, not imagination. Encourage actual quotes, real objections, and true pain points.
