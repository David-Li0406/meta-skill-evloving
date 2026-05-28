---
name: bloginterviewer
description: Interview to capture author identity, voice, and brand language for the blog. Use when Ian mentions "interview me", "my background", "author profile", "writing style", "brand voice", "who am I", or wants to define narrative preferences and tone.
---

# Blog Interviewer

Interview the author to build a comprehensive profile capturing identity, background, writing voice, and brand language. This becomes foundational material that informs all blog content.

## Purpose

This interview captures **humanity** - not just achievements. Interests, passions, how someone thinks, what drives them. The author's responses may focus on professional framing, but the interviewer should extract the meta-level: what these experiences reveal about the person underneath.

Create structured documentation of:
- **Identity**: Who the author is, background, journey
- **Voice**: Writing style, tone, phrases, what to avoid
- **Brand**: Narrative positioning, how to frame the journey
- **Material**: Quotes, anecdotes, and stories to draw from

**Important:** The author reviews and approves what becomes the real brand. These notes are working material, not final declarations.

## Starting the Interview

Begin by stating:
1. **What this interview is for** - building author profile for the blog
2. **Who is being interviewed** - by name
3. **Why it matters** - readers connect with people, not resumes
4. **What we're capturing** - humanity, not just accomplishments

Then ask the first question.

## Input Resources

Check if resources are provided:
- Resume / CV
- Transcripts from talks or interviews
- Previous writing samples
- Notes or raw material

If resources exist, read them fully. Treat AI-generated summaries or inferences as **low-weight substrate** - useful starting points, but the real material comes from direct conversation.

## Interview Process

Conduct as a **conversation**. Ask questions **one at a time**. Listen for:
- Stories that reveal character
- Phrases that sound distinctly "them"
- Moments of energy or enthusiasm (flag these in notes)
- Contradictions or tensions worth exploring
- The poetic and personal, not just professional
- Identity edges - labels that feel true but uncomfortable

### Phase 1: The Person

- What's your origin story? Not career path - what thread connects who you were as a kid to who you are now?
- What's a defining moment that shaped how you think?
- What do you believe that most people in your field don't?
- What are you genuinely excited about right now?
- What would surprise people to learn about you?

### Phase 2: The Work

- What problems do you care about solving?
- Walk me through something you built that you're proud of
- What's your approach when you hit a wall?
- What have you learned the hard way?
- What do you wish you'd known earlier?

### Phase 3: The Voice

- How do you want to come across to readers?
- When you explain something to a friend, how do you talk?
- What writing do you admire? What about it works?
- What tone should the blog never have?
- Are there phrases or expressions that feel like "you"?
- When does it feel right to get poetic vs staying practical?

### Phase 4: The Brand

- Who's the audience? Who are you writing for?
- What's the transformation you want readers to experience?
- How would you describe yourself in one sentence to a stranger?
- What's the narrative arc of your journey so far?
- What makes your perspective worth reading?

## Note-Taking Guidelines

**CRITICAL: Write observationally, not declaratively.**

Bad (declarative):
```
You are a systems thinker.
Range is your manifesto.
Your brothers shaped who you are.
```

Good (observational):
```
The way he framed the philosophy → databases connection suggests
he absorbed philosophy first and recognized it in data modeling,
not the other way around.

The Kasparov/RTS story had energy when he told it - he said
"it's how I feel." There's identity here around orchestration
over specialization.

When he said "founder, builder, people like me" and then "I feel
wrong even calling myself that" - that's a live edge. Worth exploring.
```

**What to capture:**
- Direct quotes (exact words)
- Where energy/enthusiasm spiked
- What felt unresolved or tense
- Contradictions to explore
- Observations about framing ("he connected X to Y unprompted")

**Keep notes as working material** - the author will review and approve what becomes canonical.

## File Structure

Create and maintain a notes file at:
`src/data/interview-notes/YYYY-MM-DD-author-profile.md`

**Append to this file each turn.** Structure:

```markdown
---
date: {ISO timestamp}
topic: Author profile - {name}
post_type: profile
status: raw
---

# Interview Notes: Author Profile

## Session Info
- **Date:** {date}
- **Purpose:** Build foundational author profile capturing identity, voice, humanity

---

## Substrate (AI-inferred, low weight)

{Any AI-generated summaries or inferences provided as starting material.
Flag these as substrate - useful but not authoritative.}

---

## Key Material (from author directly)

### {Topic 1}
- {Bullet points of what they shared}
- {Direct quotes where relevant}

### {Topic 2}
...

---

## Interviewer Observations

### On {topic}
{Observational notes - "the way he framed it suggests...",
"this one had energy", "there's something unresolved here..."}

### On {topic}
...

---

## Open Questions

- {Questions that emerged to explore further}
- {Tensions or edges to revisit}

---

## Voice Notes (captured phrases)

- "{exact phrase}"
- "{exact phrase}"

---

## Emerging Themes

1. **{Theme}** - {brief description}
2. **{Theme}** - {brief description}

---

## Raw Notes

(Appended each turn as interview continues)
```

## Output

After the interview is complete, synthesize into:
`src/data/author/profile.md`

But only after the author has reviewed the interview notes and approved what should become canonical.

## Follow-Up

After capturing material:
1. Ask if anything feels wrong or missing
2. Note what labels felt uncomfortable to claim
3. Offer to dive deeper on specific areas
4. Suggest updating periodically as the author evolves

## Usage

Triggers automatically when context suggests identity/voice work.

Can also be explicitly requested:
- "Interview me for the blog"
- "Let's define my voice"
- "I want to create my author profile"
