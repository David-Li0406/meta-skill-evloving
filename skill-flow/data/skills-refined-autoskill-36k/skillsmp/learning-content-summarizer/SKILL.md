---
name: learning-content-summarizer
description: Summarizes technical/AI/data content from URLs, YouTube videos, or how-to guides into actionable step-by-step learning instructions. Use when given a video, article, or tutorial URL to convert into a learnable guide.
---

# Learning Content Summarizer

Transforms technical content (videos, articles, tutorials) into optimized step-by-step learning guides for rapid skill adoption.

## Capabilities

- Extract key concepts from YouTube videos, articles, and documentation
- Create structured, actionable step-by-step instructions
- Capture screenshots at critical moments for visual reference
- Identify prerequisites and dependencies
- Highlight common pitfalls and pro tips
- Generate practice exercises for reinforcement

## Workflow

### 1. Content Ingestion

When given a URL:
1. Use `read_web_page` to fetch the content
2. For YouTube videos, extract video ID and use transcript if available
3. Identify the content type: tutorial, explanation, demo, or reference

### 2. Content Analysis

Extract and organize:
- **Goal**: What will you be able to do after completing this?
- **Prerequisites**: Required knowledge, tools, accounts, or setup
- **Key concepts**: Core ideas explained simply (ELI5 where helpful)
- **Time estimate**: Realistic time to complete hands-on

### 3. Step-by-Step Guide Generation

Create instructions following this structure:

```markdown
# [Topic Title]

## 🎯 Goal
One-sentence outcome statement.

## ⚙️ Prerequisites
- [ ] Tool/software installed
- [ ] Account created
- [ ] Prior knowledge required

## ⏱️ Time Estimate
~X minutes/hours

## 📋 Steps

### Step 1: [Action Title]
**What**: Brief description
**Why**: Reason this step matters
**How**:
1. Specific action
2. Specific action
3. Verify: Expected result

> 💡 **Tip**: Pro tip or shortcut

> ⚠️ **Watch out**: Common mistake to avoid

### Step 2: [Action Title]
...

## ✅ Verification
How to confirm you've succeeded.

## 🔗 Next Steps
What to learn next for deeper understanding.

## 📚 Resources
- Original source link
- Related documentation
- Community/support links
```

### 4. Screenshots and Visuals

When processing video content or when visuals are critical:
1. Note timestamps where key UI/visuals appear
2. Describe what the screenshot should capture
3. If user provides screenshots, use `look_at` to analyze and reference them

For web content:
1. Identify diagrams or UI elements worth capturing
2. Describe or link to relevant visual assets

## Output Guidelines

- **Be actionable**: Every step should be something the user can DO
- **Be specific**: Include exact commands, button names, menu paths
- **Be sequential**: Order matters—dependencies first
- **Be concise**: Cut fluff, keep only what helps learning
- **Be practical**: Focus on "how" over "why" (unless understanding is crucial)

## Example Usage

User provides: "Summarize this video: https://youtube.com/watch?v=..."

Response structure:
1. Acknowledge the content type
2. Fetch/analyze the content
3. Generate the structured guide
4. Offer to save as a markdown file in the repo

## Integration with Learn In Public

When appropriate, offer to:
- Save the guide to `weeks/YYYY/week-XX/` as a detailed post
- Link it from the weekly README
- Tag with appropriate category (💻 AI, Data & Programming)
