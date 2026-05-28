# Writing Samples

Reference these posts when drafting content. Study the voice, structure, and what makes each effective.

---

## Sample 1: Product Launch (Personal Site)

**Type:** Announcement with personality
**Why it works:** Hooks with the struggle ("after years of..."), shows personality through design choices, lists concrete things, ends with engagement question.

```
I finally shipped my personal site.

After years of "I should really build a portfolio," adamslaker.dev is live.

But I didn't want another generic developer page with a hero section and a contact form.

So I built something that actually reflects how I think:

A terminal-inspired interface. Lime green on dark zinc. The kind of aesthetic that makes you feel like you're hacking into something (you're not, I promise).

What you'll find:

→ Projects like Ephemeris (real-time ISS tracking) and my work as a maintainer on Auto-Claude, an autonomous multi-agent coding framework

→ Consulting offerings for teams navigating AI strategy, looking for technical speaking, or needing fractional CTO support

→ A "Character Sheet" section — because outside of work, I'm a NICA mountain biking coach, a D&D player, and someone who has strong opinions about Cole Wehrle board games

→ A technical blog (coming soon) where I'll write about agentic AI patterns, LLM architectures, and the infrastructure that makes it all work

Built with Astro, React, TypeScript, Tailwind, and deployed on Cloudflare Workers (Workers because then I can manage DNS in code, which I prefer to a dashboard).

Did I build it using AI? Hell yeah (go check out DesignOS by Brian Casel it's an amazing way to design your UI and data model)

Did I let the AI do the thinking for me? Hell no! This is my design, and my website.

The stack matters less than the fact that it's finally done.

Check it out: adamslaker.dev

What's one thing you've been putting off shipping?
```

**Patterns to copy:**
- Opens with the win, not preamble
- "But I didn't want..." pivot shows intentionality
- "(you're not, I promise)" is the dad-joke aside
- Arrow bullets for scannable lists
- "Hell yeah / Hell no" contrast is blunt and memorable
- Ends with genuine question, not performative CTA

---

## Sample 2: Technical Deep Dive (Parallel Research)

**Type:** Educational/Tutorial
**Why it works:** Opens with the insight, uses visual separators for scannability, concrete code-like examples, delivers a framework you can use immediately.

```
Sequential research gives you one answer. Parallel research gives you five, then lets you pick the best.

Post five built /solve-problem. It chains /research → /synthesize → /write-plan into one workflow.

The bottleneck? Research explores solutions one at a time.

For architecture decisions, technical tradeoffs, or integration strategies, you want multiple perspectives before committing.

Here's how to upgrade the /research command with parallel subagents that let your main agent judge.

━━━━━━━━

🔍 The single-perspective trap:

/solve-problem "add real-time notifications"

The /research command explores sequentially:
→ Polling → tradeoffs → websockets → tradeoffs → continues until timeout

You get findings. No comparison, no consensus. 5x slower because each approach adds time.

One researcher, one lens, one recommendation.

━━━━━━━━

🤝 The parallel alternative:

Spawn N subagents (you control the number), each exploring a different solution:
→ Agent 1: polling
→ Agent 2: websockets
→ Agent 3: server-sent events
→ Agent 4: webhook patterns
→ Agent 5: pub/sub architecture

Each runs in parallel, explores deeply, writes findings to its own file.

They report back to your main agent, which judges and recommends the strongest.

Parallel solution exploration with LLM-as-judge.

━━━━━━━━

⚙️ The mechanics:

Your /research command becomes an orchestrator:

1. Spawn N subagents with specific instructions per solution
2. Each explores its assigned approach, writes findings
3. All subagents report back
4. Main agent evaluates all approaches
5. Pass winner to /synthesize

Each subagent runs in an isolated context window. No bleed, no interference.

Configuration in .claude/agents/ as Markdown files. Your main agent handles evaluation.

━━━━━━━━

🎁 The payoff:

/solve-problem "notifications" --deep

You get:
→ Five solutions explored in parallel
→ Comparative evaluation against criteria
→ Evidence-based recommendation

Cost: roughly one Opus call (five Sonnet subagents, main agent judges)
Quality: Opus-level insight with comparative analysis
Speed: 5x faster than sequential

Compound automation with orchestrated intelligence.

━━━━━━━━

🔄 When to use:

**Fast path**: Straightforward problems. One researcher, quick findings.

**Deep path**: Complex decisions needing comparison. Multiple researchers, judge selects strongest.

Add --deep flag to /solve-problem. The orchestrator decides which mode.

━━━━━━━━

This is the architecture shift from post six: orchestrator-worker pattern at the workflow level.

Your main command delegates to parallel workers. Each explores a different solution. The orchestrator evaluates and selects.

You're not just automating steps. You're orchestrating comparison.

━━━━━━━━

Next up: Subagent configuration and evaluation flow. You'll see how the main agent scores approaches and selects the winner.
```

**Patterns to copy:**
- Opens with the insight, not the setup
- Uses horizontal rules for visual breathing room
- Emoji headers for quick scanning
- Code/command examples make it concrete
- "The payoff" section delivers the deliverable
- Numbered lists for sequential processes
- Teases what's next (series structure)

---

## Sample 3: Personal Journey + Series Announcement

**Type:** Reflection with value proposition
**Why it works:** Vulnerable opening about doubt, specific turning point, calls out common mistakes, announces series with clear promise.

```
I was unsure about using Claude Code at first.

I genuinely like coding, and using an AI agent full time felt irresponsible. Like giving up something I loved. For months, I treated it like better autocomplete.

Then I realized: I wasn't limited by what to build. I was limited by how fast I could build it.

Once I shifted from "I love implementation" to "I love creation," everything changed. Eight months in, I can work on multiple projects simultaneously. The tool doesn't replace the work I enjoy. It removes what kept me from shipping.

But here's what I keep seeing:

Some people are using Claude Code but barely scratching the surface. They're stuck in reactive mode, going back and forth with the agent on every little thing. They haven't built the skill to pause, observe, and automate. So they're rebuilding the same sequences every time.

Others still think GitHub Copilot or Cursor are the ceiling for AI-assisted development.

Both groups are leaving a lot on the table.

Let me show you what's possible.

A few months ago, I asked Claude Code to fix a bug. It fixed it, then flagged two related pieces of code that were "flaky" and could cause a race condition, without me even asking.

That's not deterministic instruction-following. That's agency.

Some people worry that relying on a non-deterministic system to write code is irresponsible. But we already rely on non-deterministic systems to write code every day. They're called other human beings.

Claude Code forces you to be explicit about your processes. Define your practices, template workflows, build guardrails.

To be clear: this isn't vibe coding. This is engineering. Context engineering.

You're using engineering know-how to constrain Claude Code within boundaries you define. The goal: output code that's the same quality or better than what you'd write by hand.

Claude Code isn't just autocomplete. It's an agentic coding assistant that can:

- Write across multiple files in a single session
- Understand feature-level requirements
- Manage context across your project
- Execute custom workflows

The shift is from file-level automation to feature-level automation. You stop stitching components together and start reviewing, refining, and making architectural decisions.

📍 What's coming:

Over the next few weeks, I'll write posts covering Claude Code from the ground up, starting with the basics and building to advanced techniques. Just getting started? I'll walk you through what it is and why it matters. Already using it? I hope to share techniques you haven't seen yet.

This series covers custom slash commands, subagents, skills, plugins, and MCP servers, with concrete, daily-use examples you can implement immediately.

If you're curious about what Claude Code can actually do, or you're already using it and want to push further, follow along.
```

**Patterns to copy:**
- Opens with doubt, not certainty
- "Then I realized:" is the pivot moment
- "But here's what I keep seeing:" transitions to teaching
- Concrete anecdote (the race condition story)
- "To be clear:" reframes potential objections
- Bullet list of capabilities as deliverable
- Series announcement with clear audience targeting

---

## Sample 4: Vulnerable Personal Post

**Type:** Personal reflection
**Why it works:** Authentic about anxiety and imposter syndrome, acknowledges both sides of an issue, makes a public commitment, invites community.

```
Starting to post on social media can be daunting.

It doesn't have to be, though.

I am historically someone who has been a "lurker" on social media, but never a contributor.

Some of this has been due to my principles:
- We have decided not to share pictures of our daughter until she is old enough to decide that she wants pictures of herself on the internet.
- When I use social media, it inevitably becomes a huge drain on productivity due to the built-in "race to the bottom of the brain stem" design of the interfaces. In addition, we are becoming more aware of how much of a psychological burden it is to the world at large in its current form.

The rest has been due mostly to anxiety:
- Even after 10 years as a software developer, I have imposter syndrome. I still have trouble convincing myself that anyone would care to hear what I have to say.
- Since I don't post that often, it is hard for me to get started posting. This creates a negative feedback loop that keeps me away from it altogether.

Though there can be many downsides to social media, I am also one who believes very strongly that technology, when used properly, can help us become better humans.

For example, the community aspect of social media can't be ignored. The ability to hop onto a laptop in my office in Wisconsin and immediately interface with folks from all over the world is, for lack of a better term, magic.

Though I have been a member for 13 years now, it wasn't until recent months that I have realized that LinkedIn is a place where the community tolerates less toxicity and is instead more focused on positivity and progress.

This is a platform that I can get behind.

This post may or may not be relevant to your current situation. Regardless, I personally need it in order to publicly pledge to actively participate more. Today marks the start of a new chapter in my professional journey. I'm making a commitment to myself and my network to actively share my knowledge and experience. By documenting what I've learned, I hope to provide value to others while also pushing myself to continue growing.

The only way we can become better humans through technology is if those of us who believe in this future take a larger part in it.

I would like to say a big thank you to Jasmin Alić and Chris Do for their fantastic two-part series on how to build a LinkedIn presence. Your strategies have really helped lower the barrier to entry for me, and gave me the tools needed to combat my personal imposter syndrome.

If you still have that tiny little imposter syndrome gremlin sitting on your shoulder like I do, how have you been dealing with it? Any tips or tricks you can share with me or anyone else who's trying to conquer their own anxiety?
```

**Patterns to copy:**
- Opens with the relatable struggle
- Lists specific reasons (principles vs anxiety)
- "race to the bottom of the brain stem" is a vivid phrase
- Acknowledges both sides before taking a position
- "This is a platform that I can get behind" is the firm stance
- Public commitment creates accountability
- Thanks specific people (generosity)
- Ends with genuine question seeking help

---

## Quick Reference: What Makes These Work

| Element | How Adam Does It |
|---------|------------------|
| **Opening** | Start with the point or struggle, never "I'm excited to..." |
| **Pivot** | "But here's the thing..." or "Then I realized..." |
| **Humor** | Parenthetical asides, self-deprecating, never at others' expense |
| **Lists** | Arrow bullets (→) for options, numbers for sequences |
| **Specificity** | Real numbers, real tools, real anecdotes |
| **Closing** | Genuine question or clear next step |
| **Stance** | Strong opinion stated directly, invites disagreement |
