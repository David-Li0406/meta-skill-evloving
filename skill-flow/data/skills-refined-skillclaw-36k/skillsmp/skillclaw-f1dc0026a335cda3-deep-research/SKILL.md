---
name: deep-research
description: Use this skill when you need to conduct thorough research on a topic using Gemini CLI, ensuring efficient use of resources and comprehensive output.
---

# Skill body

Conduct deep research on any topic using Gemini CLI via a spawned sub-agent. This approach utilizes your Google AI subscription instead of Claude tokens, making it ideal for extensive research tasks.

## How It Works

**When the user says "Research: [topic]" or requests deep research:**

### Step 1: Clarifying Questions (Always)

Before initiating any research, ask 2-5 quick questions to focus the work:

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

### Step 2: Spawn Research Agent

Once you have context, use `sessions_spawn` to run the research:

```
sessions_spawn(
  task: "Research: [FULL TOPIC WITH CONTEXT]"
)
```

Use Gemini CLI to research this topic. Run:

```
gemini --yolo "[RESEARCH PROMPT]"
```

The research prompt should cover:
1. Overview & Core Concepts - what is this, terminology, why it matters
2. Current State - latest developments, major players
3. Technical Deep Dive - how it works, mechanisms, key techniques
4. Practical Applications - real-world use cases, tools available
5. Challenges & Open Problems - technical, ethical, barriers
6. Future Outlook - trends, predictions, emerging areas
7. Resources - key papers, researchers, communities, courses

Save the output to: `~/clawd/research/[slug]/research.md`

Be thorough (aim for 500+ lines). Include specific examples and citations.

### Step 3: Notify Completion

When research is complete:
1. Send a wake event to notify the main agent immediately:
   ```
   cron(action: 'wake', text: '🔬 Research complete: [TOPIC]. Key findings: [2-3 bullet points]. Full report: ~/clawd/research/[slug]/research.md', mode: 'now')
   ```
2. When asked to produce an announce message, reply accordingly.