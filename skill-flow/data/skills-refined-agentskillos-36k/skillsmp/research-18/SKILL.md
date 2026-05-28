---
name: research
description: Deep research via Gemini CLI — runs in background sub-agent.
---

# Research Skill

Conduct deep research on any topic using Gemini CLI via a spawned sub-agent.

## How It Works

**When user says "Research: [topic]" or asks for deep research:**

### Step 1: Clarifying Questions (Always)

Before running any research, ask 2-5 quick questions to focus the work:

**Start with the goal:**
> "Before I dive in - what's your goal here? Are you learning about this topic, making a decision, writing something, or just curious?"

**Then adapt based on their answer:**

If learning/curious:
- "Any specific aspect you're most interested in?"
- "How technical should I go? (High-level overview vs deep technical detail)"

If decision-making:
- "What decision are you trying to make?"
- "Any specific criteria or constraints I should focus on?"

If writing/creating:
- "What's the output? (Blog post, report, presentation?)"
- "Who's the audience?"

**Keep it natural — 2-5 questions max.** Don't interrogate.

### Step 2: Conduct Research Using Sub-Agents

Conduct research using sub-agent(s) (if available) using web search or any other relevant tools available at your disposal. 
Research must include:

1. Overview & Core Concepts - what is this, terminology, why it matters
2. Current State - latest developments, major players
3. Technical Deep Dive - how it works, mechanisms, key techniques
4. Practical Applications - real-world use cases, tools available
5. Challenges & Open Problems - technical, ethical, barriers
6. Future Outlook - trends, predictions, emerging areas
7. Resources - key papers, researchers, communities, courses

Save the output to: `C:\Users\Sarfraz\OneDrive\Documents\AI-Generated-Researches\<slug>\research.md`

Be thorough (aim for 500+ lines). Include specific examples and citations.

## Tips

- Research typically takes 3-10 minutes depending on complexity
- Check `C:\Users\Sarfraz\OneDrive\Documents\AI-Generated-Researches` for all past research
