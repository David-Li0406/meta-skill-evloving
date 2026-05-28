Most people complain that AI writes too generic.

Then they keep using it the exact same way and expect different results.

I was doing this too. Tweaking prompts, adding examples, getting output that still felt off. The problem wasn't the model. It was me expecting it to learn preferences I'd never actually documented.

So I built a system that learns from every edit I make to AI-generated drafts.

To be clear: this isn't about automating publishing. It's about making drafts better starting points. I still review and refine everything before it goes out and that part stays human. The goal is spending less time editing, not zero time.

**How it works:**

Generate a draft → edit and publish → capture the final → analyze what changed → apply learnings to the next draft.

The system categorizes edits into patterns: structural changes, tone adjustments, word choices, content additions, format preferences.

When a pattern shows up 3+ times, it becomes a high-confidence rule that's auto-applied to future drafts.

📊 **What it's learning:**

After analyzing my first published post, it noticed I:

- Added emoji section headers (🔧, 📦, 🎯)

- Made punchy sentences into standalone paragraphs

- Removed all suggested hashtags

- Added personal accountability stories

- Softened aggressive language

These aren't things I would have articulated in a prompt. But they showed up consistently in my edits.

🧠 **The research foundation:**

This approach draws from recent papers (CIPHER, PLUME) showing that learning from user edits beats fine-tuning for personalization. Instead of retraining models, you extract interpretable preference descriptions and add them to prompts.

The part I care about most: my preferences live in markdown files I can review and edit manually. No black box. No vendor lock-in. I own the system.

**Why it matters:**

Generic AI output isn't a model problem. It's a feedback loop problem. The model can't learn what you never teach it.

This system closes that loop automatically.

---

How are you capturing your editing patterns (if at all)?

What's one consistent change you make to AI drafts that you haven't turned into a rule yet?
