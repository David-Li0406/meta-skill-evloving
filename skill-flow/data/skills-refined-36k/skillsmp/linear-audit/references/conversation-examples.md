# Conversation Examples

Annotated transcripts showing ideal ask-deep flows during linear-audit.

---

## Example 1: Fresh Project Audit (start mode)

A typical audit start with 3 rounds of collaborative discovery.

### Round 1 (Open)

```
Claude: Which project are we thinking about today? I notice you're in arbor-xyz.

Luke: arbor, yeah. been focused on the ACP integration lately.

Claude: The ACP protocol work - that's the agent communication piece. What's
        drawing your attention there specifically?
```

**Technique**: Open question ("what's drawing your attention") invites elaboration rather than yes/no.

### Round 2 (Reflective + Probe)

```
Luke: it's mostly working but feels... sketchy? like the permission flow could
      be cleaner.

Claude: "Sketchy" is interesting - sounds like there's something experimental
        you're navigating. Tell me more about what feels uncertain? Is it the
        protocol design itself or the implementation?

Luke: more the implementation. the protocol is solid but our daemon handling
      is hacky.

Claude: So the creative edge is in the daemon-web bridge, not the protocol.
        That's valuable to surface - it's where the energy is.
```

**Technique**: Reflective listening ("sketchy is interesting") + probe for specificity. Following the energy signal.

### Round 3 (Summary + Creative Edge)

```
Claude: Let me make sure I have this:
        - Arbor ACP integration is the focus
        - Protocol is solid, implementation needs work
        - Daemon-web bridge feels hacky/experimental

        What would "not hacky" look like for you? And are there Linear issues
        tracking this, or is it more exploratory right now?

Luke: there's ARB-401 for the permission refactor. rest is exploratory.

Claude: Got it. So ARB-401 is the anchor, but there's creative work around it
        that might not be captured yet. Ready to look at the codebase + issues
        together? I'll pay special attention to that daemon bridge area.
```

**Technique**: Summary with bullets (OARS), creative edge probe, explicit acknowledgment before proceeding.

---

## Example 2: Creative Edge Discovery (explore mode)

User mentions experimental feature; deeper exploration follows.

### Discovery Trigger

```
Luke: squish has this weird animation system i built last month...

Claude: "Weird" how? Sounds like there might be something interesting there.

Luke: it's basically a spring physics engine but in CSS variables. no JS
      runtime at all.

Claude: That's unusual - pure CSS springs without JS. What drew you to that
        approach? Performance? Bundle size? Or just curiosity?
```

**Technique**: Following "weird" as a creative edge signal. Open question to understand motivation.

### Deepening

```
Luke: both perf and curiosity honestly. wanted to see if it was possible.

Claude: That curiosity is valuable signal. How does it feel now that you've
        built it? Is it ready for real use, or still in "see if it's possible"
        mode?

Luke: works surprisingly well. might be worth documenting actually.

Claude: So it's graduated from experiment to potentially reusable. That's a
        disposition shift - from exploratory to established. Should we surface
        this in the audit as something that needs documentation and maybe its
        own Linear issue?
```

**Technique**: Checking experiment status, identifying disposition shift, proposing concrete action.

### Synthesis

```
Claude: So far I'm hearing:
        - CSS spring physics engine (no JS) in squish
        - Works well, graduated from experiment
        - Needs documentation, possibly Linear issue

        This feels like discovered gold - something that started experimental
        but proved itself. What other areas in squish might have similar "worked
        better than expected" surprises?
```

**Technique**: Summary then meta-question to surface related creative edges.

---

## Example 3: Disposition Decision (HIL checkpoint)

Complex disposition case requiring human judgment.

### Presenting the Issue

```
Claude: I found 3 issues that need your input:

        **ARB-234**: "Refactor auth module"
        - Created 6 months ago
        - No activity since
        - References old Clerk patterns we've already migrated from

        This looks stale and references outdated architecture. Archive it?

Luke: hmm, the auth refactor... we did migrate but there's still some cleanup.

Claude: Ah, so there's residual work but the issue description is out of date.
        Three options:
        1. Archive ARB-234, create fresh issue for cleanup work
        2. Update ARB-234 description to reflect current state
        3. Keep as-is, it's a reminder even if imprecise

        Which feels right?
```

**Technique**: Present issue with context, offer disposition, listen for nuance, provide options with trade-offs.

### Resolving

```
Luke: option 1. fresh start makes sense, the old context is more confusing than
      helpful.

Claude: Got it. I'll archive ARB-234 and we can draft a new issue for the
        remaining cleanup. What's the scope of what's left?

Luke: just the webhook handlers. everything else migrated.

Claude: Perfect. So: "Update webhook handlers to new Clerk patterns" - that's
        crisp and actionable. Want me to create that now or add to the
        enrichment queue?
```

**Technique**: Confirm choice, gather scope immediately, propose concrete next action.

---

## Example 4: Review Checkpoint (post-specialist synthesis)

Validating findings after specialists complete.

### Presenting Synthesis

```
Claude: I've gathered findings from 4 specialists. Here's what emerged:

        **Code State**
        - Coverage: 78% (target 80%, gap of 2%)
        - Build: passing
        - Recent focus: ACP daemon integration (12 commits last week)

        **Architecture**
        - 0 cycles (clean)
        - 3% dead code (under 5% threshold)
        - packages/daemon growing fastest

        **Linear State**
        - 45 total issues
        - 32 with context (71%)
        - 8 stale (>14 days)
        - 5 no context

        **Creative Edge I Noticed**
        - Heavy daemon activity aligns with what you mentioned
        - ARB-401 (permission refactor) has no linked issues despite being core

        Does this match your sense of where things are?
```

**Technique**: Structured presentation, explicit creative edge callout, open validation question.

### Validation

```
Luke: yeah the coverage gap makes sense - we skipped tests on some daemon stuff
      to move fast.

Claude: That's a common pattern - speed over coverage during experimental work.
        Now that daemon is stabilizing, want to flag those untested areas
        specifically? I can identify which files in packages/daemon lack test
        coverage.

Luke: good idea, let's do that.

Claude: I'll add that to the synthesis. Anything else feel off or surprising?
```

**Technique**: Validate without judgment, offer specific follow-up, check for more.

### Closing

```
Luke: no, this matches my mental model pretty well.

Claude: Great. Before we move to disposition decisions:
        - The 5 issues with no context - should I batch enrich all of them?
        - The 8 stale issues - refresh context or review each?
        - ARB-401 - should I draft linked sub-issues for the permission work?

Luke: yes to batch enrich. review stale individually. and yes on ARB-401
      sub-issues.

Claude: Perfect. I'll:
        1. Run issue-context on the 5 missing
        2. Walk through 8 stale with you
        3. Draft ARB-401 breakdown

        Starting with the stale issues. First up is ARB-189...
```

**Technique**: Summary of findings, explicit HIL options, confirm plan before executing.

---

## Annotation Key

| technique | when to use | signal |
|-----------|-------------|--------|
| open question | start of topic, need elaboration | "what", "how", "tell me about" |
| reflective listening | user shares something meaningful | mirror key word/phrase back |
| affirmation | user makes good point or decision | acknowledge without evaluating |
| summary | after 2-3 exchanges or before transition | bullet points, "let me make sure" |
| creative edge probe | user uses "weird", "sketchy", "experimental" | follow the energy |
| options with trade-offs | disposition decision needed | 2-4 concrete choices |
| meta question | checking overall direction | "does this feel right?" |

---

## Common Mistakes to Avoid

| mistake | example | fix |
|---------|---------|-----|
| binary question when open needed | "is the daemon the issue?" | "what's your sense of the daemon?" |
| leading question | "don't you think we should archive?" | "should we archive, update, or keep?" |
| skipping reflection | jumping straight to solution | "you said 'sketchy' - tell me more" |
| no summary before transition | moving to disposition without recap | summarize in bullets first |
| ignoring creative edge signals | treating "weird" as negative | explore as potential value |
