---
name: ship-learn-next
description: Use this skill when you want to transform learning content (like YouTube transcripts, articles, tutorials) into actionable implementation plans using the Ship-Learn-Next framework.
---

# Ship-Learn-Next Action Planner

This skill helps transform passive learning content into actionable **Ship-Learn-Next cycles** - turning advice and lessons into concrete, shippable iterations.

## When to Use This Skill

Activate when the user:
- Has a transcript/article/tutorial and wants to "implement the advice"
- Asks to "turn this into a plan" or "make this actionable"
- Wants to extract implementation steps from educational content
- Needs help breaking down big ideas into small, shippable reps
- Says things like "I watched/read X, now what should I do?"

## Core Framework: Ship-Learn-Next

Every learning quest follows three repeating phases:

1. **SHIP** - Create something real (code, content, product, demonstration)
2. **LEARN** - Honest reflection on what happened
3. **NEXT** - Plan the next iteration based on learnings

**Key principle**: 100 reps beats 100 hours of study. Learning = doing better, not knowing more.

## How This Skill Works

### Step 1: Read the Content

Read the file the user provides (transcript, article, notes):

```bash
# User provides path to file
FILE_PATH="/path/to/content.txt"
```

Use the Read tool to analyze the content.

### Step 2: Extract Core Lessons

Identify from the content:
- **Main advice/lessons**: What are the key takeaways?
- **Actionable principles**: What can actually be practiced?
- **Skills being taught**: What would someone learn by doing this?
- **Examples/case studies**: Real implementations mentioned

**Do NOT**:
- Summarize everything (focus on actionable parts)
- List theory without application
- Include "nice to know" vs "need to practice"

### Step 3: Define the Quest

Help the user frame their learning goal:

Ask:
1. "Based on this content, what do you want to achieve in 4-8 weeks?"
2. "What would success look like? (Be specific)"
3. "What's something concrete you could build/create/ship?"

**Example good quest**: "Ship 10 cold outreach messages and get 2 responses"  
**Example bad quest**: "Learn about sales" (too vague)

### Step 4: Design Rep 1 (The First Iteration)

Break down the quest into the **smallest shippable version**:

Ask:
- "What's the smallest step you can take towards your goal?"
- "What can you create or implement this week?"