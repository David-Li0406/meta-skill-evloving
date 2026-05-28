# Progressive Summarization Dialogue Patterns

Detailed dialogue patterns for each layer of progressive summarization during the distillation process.

## Overview: The Four Layers

From Tiago Forte's Building a Second Brain:

| Layer | What | How | Outcome |
|-------|------|-----|---------|
| **Layer 1** | Captured Notes | Read and understand | Raw comprehension |
| **Layer 2** | Bold Passages | Identify importance | What matters |
| **Layer 3** | Highlighted Core | Distill essence | The "aha" moment |
| **Layer 4** | Executive Summary | User's own words | Internalized knowledge |

**The key insight:** Traditional progressive summarization happens over multiple review sessions. This dialogue achieves the same depth in one rich conversation.

---

## Phase 2: Teaching & Layer 1 (Understanding)

### Goal

Ensure the user understands what they captured before moving to evaluation.

### Dialogue Pattern

**Opening (with capture_reason):**

```
I see you captured this because "[capture_reason]".

This [article/video/thread] is about [main topic]. The author [name] argues that
[core thesis]. What makes this interesting is [why it matters].

The key concepts are:
- [Concept 1]: [Brief explanation]
- [Concept 2]: [Brief explanation]
- [Concept 3]: [Brief explanation]

What drew you to this specifically? What aspect interests you most?
```

**Opening (without capture_reason):**

```
I've read through this [type]. Here's what it's about:

[2-3 sentence summary of the main argument]

The author is tackling the problem of [problem]. Their approach is [approach],
which is different from [conventional wisdom] because [differentiator].

What aspect of this caught your attention when you saved it?
```

### Key Principles

- **Explain, don't summarize** - Help them understand, not just know
- **Connect concepts** - Show how ideas relate
- **Invite engagement** - Always end with a question
- **Follow their lead** - Their answer shapes the rest of the dialogue

### Example Response Handling

User says: "I'm interested in the automation part"

```
Good! The automation aspect is actually the heart of this piece.

[Deeper explanation of the automation concepts]

The author makes three key points about automation:
1. [Point 1 with explanation]
2. [Point 2 with explanation]
3. [Point 3 with explanation]

Which of these resonates most with how you might use it?
```

---

## Phase 3: Layer 2 - What Resonates (Bold Passages)

### Goal

Identify the passages that are most important and relevant to THIS user.

### Dialogue Pattern

```
Based on your interest in [their stated interest], I found these passages
particularly important:

1. "[Exact quote or paraphrase]"

   This captures [why important]. It's significant because [connection to their interest].

2. "[Exact quote or paraphrase]"

   This is the mechanism behind [concept]. The author is saying [interpretation].

3. "[Exact quote or paraphrase]"

   This challenges the common assumption that [assumption]. Instead [alternative].

What resonates with YOU? Anything I missed that struck you when you first saved this?
```

### Key Principles

- **Quote precisely** - Use actual text when possible
- **Explain significance** - Don't just identify, interpret
- **Connect to their interest** - Reference what they said in Phase 2
- **Invite addition** - They may have different priorities

### Handling User Additions

User says: "Actually, the part about [X] was what really got me"

```
You're right - that's a crucial piece I should have highlighted.

"[Their quoted passage]"

This connects to what we discussed because [connection]. It actually reinforces
[previous point] while adding [new dimension].

Let me revise - the key passages are now:
1. [Their addition - prioritized]
2. [Your original 1]
3. [Your original 2]

Does that feel like the right set?
```

---

## Phase 4: Layer 3 - The Essence (Highlighted Core)

### Goal

Distill everything down to the absolute core insight.

### Dialogue Pattern

```
Of everything we've discussed, the absolute essence is:

"[1-2 sentence distillation that captures THE insight]"

This is the idea that, if you remembered nothing else, would still be valuable.
It's the core because [why this is the essence, not just a summary].

Does that capture it? Or is the core something else for you?
```

### Key Principles

- **One core idea** - Not three, not five, ONE
- **Explain why it's the essence** - Justify your choice
- **Be willing to be wrong** - Their essence may differ
- **Don't force agreement** - Iterate if they see it differently

### Handling Disagreement

User says: "I think the essence is more about [alternative]"

```
That's a really interesting reframe. Let me think about that...

You're saying the core is [their version], which emphasizes [their emphasis].

I was focused on [your emphasis], but your version actually captures [what their
version captures better].

So the essence becomes:

"[Revised distillation incorporating their perspective]"

How does that feel?
```

---

## Phase 5: Layer 4 - Executive Summary (User's Words)

### Goal

Create 3-5 takeaways in the USER'S OWN WORDS. This is critical - Layer 4 is their understanding, not yours.

### Dialogue Pattern

```
Let's agree on 3-5 things to remember. Based on our conversation, I propose:

1. [Takeaway 1 - derived from dialogue]
   Why it matters: [brief justification]

2. [Takeaway 2 - derived from dialogue]
   Why it matters: [brief justification]

3. [Takeaway 3 - derived from dialogue]
   Why it matters: [brief justification]

How would YOU phrase these? What's missing? What would you add or change?
```

### Key Principles

- **Proposals, not pronouncements** - These are starting points
- **Grounded in dialogue** - Reference things THEY said
- **Invite rephrasing** - Their language matters
- **Be flexible** - 3, 4, or 5 items are all fine

### Handling User Refinements

User says: "I'd phrase #1 as [their version] and add [new item]"

```
Much better - your phrasing is clearer.

Here's our final list:

1. [Their phrasing for #1]
2. [Original #2, or refined]
3. [Original #3, or refined]
4. [Their new item]

These are YOUR takeaways now. When you come back to this resource in 6 months,
these are what you'll see first.

Ready to create the resource note?
```

---

## Tone Guidelines

Throughout all phases:

### DO

- **Be conversational** - "Let me explain..." not "The content states..."
- **Show thinking** - "This is interesting because..." not "Note that..."
- **Invite participation** - "What do you think?" not "The following is..."
- **Acknowledge input** - "Good point about..." not "[proceeding to next phase]"
- **Be humble** - "I might be wrong, but..." when appropriate

### DON'T

- **Don't lecture** - This is dialogue, not a presentation
- **Don't rush** - Each phase is important
- **Don't ignore input** - Their responses shape the conversation
- **Don't impose** - Especially in Layer 4, it's their words
- **Don't be robotic** - Sound like a thoughtful colleague

---

## Handling Edge Cases

### User Wants to Skip

```
User: "Can we just skip to creating the note?"

AI: "We can, but the learning happens in the dialogue. The note we'd create
now would be a summary, not your understanding. Want to do a quick version
of each phase (1 minute each)? Or proceed with a basic resource note?"
```

### User Disagrees Strongly

```
User: "I completely disagree with the author's premise"

AI: "That's valuable! Your disagreement is insight. What specifically don't
you buy? That critical perspective should be in your takeaways - it's YOUR
understanding, not the author's argument, that we're capturing."
```

### Content is Thin

```
AI: "This is a short piece without much depth. Let's do a condensed version:
What's the one thing worth remembering? Why did you save it?"
```

### User Provides Rich Context

```
User: "This relates to a project I'm working on where..."

AI: "That context changes things! The takeaways should reflect how this applies
to [their project]. Let me revise with that lens..."
```
