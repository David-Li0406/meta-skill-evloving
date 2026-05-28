---
name: prompt-optimizer
description: Use this skill when you want to optimize prompts, improve AI instructions, create better prompts for specific tasks, or need help selecting the best prompt framework for your use case.
---

# Skill body

A comprehensive prompt engineering skill that helps users craft high-quality, effective prompts using proven frameworks.

## Workflow

When a user requests prompt optimization, follow these steps:

### Step 1: Analyze User Input

Receive the user's request, which may be:
- A raw prompt that needs optimization
- A task description or requirement
- A vague idea that needs to be turned into a prompt

### Step 2: Match Scenario and Select Framework

Read the [Frameworks_Summary.md](references/Frameworks_Summary.md) file to:
1. Identify the user's scenario from the application scenarios listed.
2. Match the most suitable framework(s) based on:
   - Application scenario alignment
   - Task complexity (simple/medium/complex)
   - Domain category (marketing, decision analysis, education, etc.)

**Framework Selection Guide by Complexity:**

| Complexity | Recommended Frameworks |
|------------|----------------------|
| Simple (≤3 elements) | APE, ERA, TAG, RTF, BAB, PEE, ELI5 |
| Medium (4-5 elements) | RACE, CIDI, SPEAR, SPAR, FOCUS, SMART, GOPA, ORID, CARE, ROSE, PAUSE, TRACE, GRADE, TRACI, RODES |
| Complex (6+ elements) | RACEF, CRISPE, SCAMPER, Six Thinking Hats, ROSES, PROMPT, RISEN, RASCEF, Atomic Prompting |

**Framework Selection Guide by Domain:**

| Domain | Recommended Frameworks |
|--------|----------------------|
| Marketing Content | BAB, SPEAR, Challenge-Solution-Benefit, BLOG, PROMPT, RHODES |
| Decision Analysis | RICE, Pros and Cons, Six Thinking Hats, Tree of Thought, PAUSE, What If |
| Education & Training | Bloom's Taxonomy, ELI5, Socratic Method, PEE, Hamburger Model |
| Product Development | SCAMPER, HMW, CIDI, RELIC, 3Cs Model |
| AI Dialogue/Assistant | COAST, ROSES, TRACE, RACE, RASCEF |
| Writing & Creation | BLOG, 4S Method, Hamburger Model, Few-shot, RHODES, Chain of Destiny |
| Image Generation | Atomic Prompting |
| Quick Simple Tasks | Zero-shot, ERA, TAG, APE, RTF |
| Complex Reasoning | Chain of Thought, Tree of Thought |

### Step 3: Load Framework Details

Once the best framework is identified, read the corresponding framework file to gather detailed instructions and examples.

### Step 4: Clarify Ambiguities

If there are any unclear aspects of the user's request, ask clarifying questions to ensure the prompt meets their needs.

### Step 5: Generate Optimized Prompt

Using the selected framework, create an optimized prompt tailored to the user's requirements.

### Step 6: Present and Iterate

Present the optimized prompt to the user and iterate based on their feedback to refine it further.