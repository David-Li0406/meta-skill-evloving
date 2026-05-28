---
name: article-writer
description: Create new log articles in nibzard.com style. Use when the user says "write an article", "create a blog post", "new log entry", or mentions wanting to write about a topic, experience, or idea. This skill captures the established voice: conversational, narrative-driven, technically deep yet accessible, with authentic personal perspective.
allowed-tools:
  - Write
  - Read
  - Bash
---

# Article Writer for nibzard.com Log

Create new log articles following the established writing voice and style. Articles are published at root-level URLs (e.g., `/vacuum`, `/api-first`).

## File Location

Create new articles in: `src/content/log/`

## Filename Format

Use **kebab-case** with short, unique names (1-2 words max) for clean URLs and OG image generation.

Examples: `vacuum.md`, `blink.md`, `theloop.md`, `agent-experience.md`

**Why short names matter:** They become URLs (`/vacuum`) and OG image filenames. Keep them punchy and memorable.

## Required Frontmatter Structure

```yaml
---
title: "Catchy, descriptive title in quotes"
description: "Brief summary (max 130 characters)"
tldr: "Even shorter summary in quotes (max 333 characters)"
date: YYYY-MM-DD
tags: [TAG1, TAG2, TAG3]  # Use ALL CAPS
draft: false
author: "Nikola Balić"
topics: [Topic 1, Topic 2, Topic 3]  # Detailed topics in sentence case
entities: [Entity 1, Entity 2]  # People, companies, tools mentioned
answers_questions:
  - Question 1 that the article answers?
  - Question 2 that the article answers?
  - Question 3 that the article answers?
---
```

**Critical frontmatter rules:**
- `title`: max 60 characters, use quotes
- `description`: max 130 characters, use quotes
- `tldr`: max 333 characters, use quotes
- `tags`: ALL CAPS (e.g., `[HUMAN, OPINION]`, `[AI, AGENTS, TOOLS]`)
- `topics` and `entities`: arrays for detailed categorization
- `answers_questions`: list 2-4 questions the article explicitly answers
- Always include `author: "Nikola Balić"`
- Use current date in YYYY-MM-DD format
- Set `draft: false` for published articles

## Writing Voice & Style

### Be Conversational & Direct

- Use "you" frequently to speak directly to the reader
- Write as if having a conversation with a smart colleague
- Maintain casual, approachable tone even with complex technical topics
- Avoid formal academic language - be accessible and engaging

**Example:**
> "The most experienced developers--those who've built systems from scratch, debugged the impossible, and shipped products that millions use—are often **the most skeptical** about AI coding tools."

### Use Narrative-Driven Structure

- Tell stories with journey formats: "Day 1, Day 2, Day 3" or "Part 1, Part 2, Part 3"
- Build suspense gradually through the article
- Weave personal experience and failures throughout
- Show evolution of thinking and learning over time

**Example from "The Agent is The Loop":**
> "There's a moment when a tool stops being a tool and becomes an agent. For most people, that moment with AI happens in a chat interface. You ask, it answers. You ask again, it answers again. But what if it could just... keep going?"

### Make Technical Topics Accessible

- Start with concrete examples and analogies
- Explain complex concepts intuitively before diving deep
- Use code examples naturally within explanations
- Bridge theory with practical implementation

### Be Authentic and Vulnerable

- Admit failures and what went wrong
- Share thought processes and uncertainties
- Show the messy reality of problem-solving
- Be humorous and self-aware when appropriate

**Example:**
> "I've seen many times how metrics can be deceiving, e.g.: a high signup rate means nothing if users aren't getting real value."

### Focus on Learning & Insights

- Emphasize what you learned, not just what you built
- Share meta-reflections on the process
- Discuss why approaches succeeded or failed
- Connect specific experiences to broader principles

## Content Patterns

### Start with Hook

- Begin with provocative observation or personal story
- Use effective blockquotes for key insights
- Create narrative tension that draws readers in

**Featured blockquote style:**
```markdown
<blockquote class="featured-quote primary">
    Senior engineers have to talk themselves into coding some things… but with AI, I just start writing a wishlist in the text box and send it off.
    <cite><a href="https://example.com">Source Name</a></cite>
</blockquote>
```

**Blockquote types:**
- `primary` - Main featured quotes
- `secondary` - Supporting quotes
- `accent` - Emphasis points
- `unattributed` - General insights

### Structure for Depth

- Go deep on technical details when warranted
- Include real code examples and implementation details
- Show multiple iterations and improvements
- End with actionable insights or reflections

### Include Meta-Commentary

- Reference your own writing process when relevant
- Discuss how you collaborate with humans/AI
- Be transparent about what worked and what didn't
- Show the human side of technical work

## Common Topics That Work Well

**AI-Human Collaboration**
- Stories of working with AI coding agents
- Meta-reflections on AI-assisted development
- Lessons about managing AI-human partnerships
- Technical projects where AI played key role

**Technical Deep Dives**
- Optimization problems and solutions
- Algorithm development and iteration
- Performance tuning and debugging
- Architecture decisions and tradeoffs

**Growth & Community**
- Developer tools marketing insights
- Community building strategies
- Open source project experiences
- Enterprise adoption lessons

**Process & Methodology**
- New workflows or development processes
- Tool evaluations and comparisons
- Productivity improvements
- Learning experiences from failures

## Writing Process

When the user wants to write an article:

1. **Understand the core experience or insight**
   - Ask: "What's the real story here?"
   - Ask: "What did you learn that others might find valuable?"
   - Identify the "aha!" moment or key learning

2. **Plan narrative arc**
   - Beginning: Hook, setup, context
   - Middle: Journey, exploration, technical depth
   - End: Insights, broader lessons, actionable takeaways

3. **Draft in sections**
   - Start with the strongest material (often the middle)
   - Build outward to create narrative flow
   - Use markdown headers (`##`) to structure ideas

4. **Refine voice**
   - Check for "you" and direct address
   - Ensure conversational tone throughout
   - Add personal touches and vulnerability
   - Include specific details and examples

5. **Complete frontmatter**
   - Write compelling title and description
   - Craft tldr that captures essence
   - List relevant tags, topics, entities
   - Define questions the article answers

6. **Verify with build**
   - Run `npm run build` to check for errors
   - Fix any schema validation issues
   - Ensure image references work
   - Confirm markdown renders correctly

7. **Collaborative revision** (optional but common)
   - Share draft with user for feedback
   - Be open to edits: trimming fluff, clarifying phrasing, refining concepts
   - Iterate based on user input
   - Re-run build if changes are significant

8. **Commit and push**
   - Run build first: `npm run build` (generates OG image)
   - Stage the article and OG image: `git add src/content/log/filename.md public/og/filename.png`
   - Commit with descriptive message following repo conventions:
     ```
     add: Short article title

     One-line summary of what the article covers and why it matters.
     ```
   - Push to remote: `git push`

## Quality Guidelines

- **Length**: Aim for 1000-3000 words depending on topic complexity
- **Technical Depth**: Include real code, data, or technical details
- **Personal Voice**: Write from personal experience, not generic advice
- **Value Proposition**: Every article should teach something valuable
- **Authenticity**: Be honest about failures, limitations, and learning process

## CRITICAL: Always Test the Build

**MANDATORY STEP**: After completing any new article, you MUST run the build to ensure it doesn't break:

```bash
npm run build
```

This checks for:
- **Content schema validation** (title max 60 chars, description max 130 chars)
- **Image references** and missing assets
- **Build errors** from invalid markdown or frontmatter
- **Link validation** and internal references

**Never skip this step** - it prevents broken deployments and ensures content quality. If the build fails, fix the errors before considering the article complete.

## Article Types Reference

**Short & Focused (500-1000 words)**
- Single insight or observation
- Quick technical tip or pattern
- Reaction to news or announcement
- Example: "The Agent is The Loop"

**Medium (1000-2000 words)**
- Exploration of a single topic
- Technical deep dive with examples
- Experience-based lessons
- Example: "Why Senior Engineers Overlook Small AI Wins"

**Long-Form (2000+ words)**
- Comprehensive journey or narrative
- Multi-part exploration
- Year-in-review style retrospectives
- Example: "2025: The Year AI Became a Teammate"

## Examples of Good Style

Study these for reference:
- `vacuum.md` - Opinion piece with personal insights
- `agent-experience.md` - Technical deep dive
- `blink.md` - Market analysis with strong voice
- `theloop.md` - Short, focused insight
- `2025-year-in-review.md` - Long-form narrative
- `growth-value-flow.md` - Prescriptive advice from experience

## Final Reminders

The goal is to share valuable learning experiences with other developers. Your unique perspective, failures, and insights are what make the content valuable. Be authentic, be technical, and be generous with your knowledge.

**The best articles feel like learning from an experienced colleague who's been in the trenches and is willing to share both their successes and failures to help you grow.**
