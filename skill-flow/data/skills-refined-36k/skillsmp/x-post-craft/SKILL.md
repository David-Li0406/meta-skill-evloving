---
name: x-post-craft
description: Create viral X/Twitter posts based on the official X algorithm (Phoenix/Grok). Generates and improves posts optimized for maximum engagement. Use when (1) creating X posts for products, services, or information, (2) improving existing post drafts, (3) designing thread structures for long content.
---

# X Post Craft - Algorithm-Driven Post Creation

Create high-engagement X/Twitter posts based on insights from X's public algorithm (Phoenix/Grok scoring system).

> **Reference**: This skill is based on insights from [x-algorithm](https://github.com/xai-org/x-algorithm) - X's open-source recommendation algorithm.

## Algorithm Fundamentals

### Scoring Signals (by importance)

X's algorithm predicts engagement probabilities and weights them into a final score:

| Positive Signal | Description | Weight |
|----------------|-------------|--------|
| `dwell_time` | Time spent reading | Very High |
| `favorite` | Like | High |
| `retweet` | Repost | High |
| `reply` | Reply | High |
| `quote` | Quote post | High |
| `share` / `share_via_dm` / `copy_link` | Share actions | Medium-High |
| `follow_author` | Follow | Medium |
| `profile_click` | Profile visit | Medium |
| `vqv` | Video quality view (30s+) | Video only |

| Negative Signal | Description | Impact |
|----------------|-------------|--------|
| `not_interested` | Not interested | Negative |
| `block_author` | Block | Strong Negative |
| `mute_author` | Mute | Strong Negative |
| `report` | Report | Strong Negative |

### Author Diversity Penalty

Same author's consecutive posts get score decay.
→ **Quality over quantity** - one great post beats multiple mediocre ones

### In-Network vs Out-of-Network

Reaching non-followers requires higher scores.
→ **Universal value** spreads better than niche content

---

## Workflow

### Step 1: Information Gathering (via AskUserQuestion)

Collect from user:

```
Required:
- Topic (service/feature/news/insight)
- Core message (one sentence)
- Target audience

Optional:
- Tone (expert/casual/provocative/educational)
- Format (single/thread/quote RT)
- Visual assets (image/video)
- Target language for output
```

### Step 2: Analysis & Design

From collected info:

1. **Hook Design**: What stops the scroll in first 1-2 lines
2. **Value Proposition**: Why worth reading
3. **Action Trigger**: Which engagement to optimize for
4. **Risk Avoidance**: Prevent negative signals

### Step 3: Generate Variations

Minimum 3 patterns:

| Pattern | Characteristic |
|---------|---------------|
| A: Classic | Clear value, easy to read |
| B: Hook-Heavy | Strong opening, curiosity gap |
| C: Discussion-Starter | Strong opinion, invites replies |

### Step 4: Algorithm Explanation

For each variation:
- Why this structure increases score
- Which signals it targets
- Potential risks and mitigations

### Step 5: Feedback Loop

Collect user preference, refine final version

---

## Generation Rules

### Structure Template

```
[HOOK] 1-2 lines to stop the scroll
  ↓
[BODY] Deliver value
  ↓
[CTA] Call to action (optional)
```

### Hook Patterns

| Pattern | Example | Goal |
|---------|---------|------|
| Number Impact | "5 things I learned after 10 years in tech" | Specificity builds trust |
| Contrarian | "Everything you know about X is wrong" | Triggers discussion |
| Empathy | "Struggling with X? Here's what worked" | Target identification |
| Conclusion First | "Bottom line: You should do X" | Clarity |
| Story | "Yesterday something happened that changed my view" | Curiosity |

### Character Guidelines

| Format | Recommended Length | Reason |
|--------|-------------------|--------|
| Single (short) | 100-140 chars | Easy to RT |
| Single (medium) | 200-280 chars | Value + completion |
| Thread post 1 | ~140 chars | Hook focus |
| Thread post 2+ | 200-280 chars | Expand content |

### Visual Asset Recommendations

| Asset Type | Algorithm Effect |
|------------|-----------------|
| Infographic | dwell_time+, share+ |
| Screenshot | Credibility, specificity |
| Video (30s+) | vqv_score activation |
| Image carousel | photo_expand+ |

---

## Thread Design

### Structure Template

```
1/N [HOOK] Why read this + "Thread below"
2/N [CONTEXT] Background or problem setup
3 to N-2/N [CORE] Main content (1 point per post)
N-1/N [SUMMARY] Key takeaways
N/N [CTA] Follow/RT/comment request
```

### Thread Hook Examples

- "X things you need to know about [topic] (thread)"
- "I researched [topic] and found something surprising. Here's what I learned 👇"
- "After X years in [industry], here's what I wish I knew (long, so thread)"

---

## Edit Mode

For improving existing drafts:

### Analysis Criteria

1. **Hook Strength**: Does line 1 stop the scroll?
2. **Value Clarity**: Is the benefit obvious?
3. **Dwell Factor**: Elements that make people read longer?
4. **Action Trigger**: Clear what to do next?
5. **Risk Check**: Any negative signal triggers?

### Improvement Format

```
[ORIGINAL ANALYSIS]
- Strengths: ...
- Areas to improve: ...

[IMPROVED VERSION]
(improved post text)

[CHANGES EXPLAINED]
- Hook: [why changed]
- Body: [why changed]
- Algorithm view: [which signals improved]
```

---

## Avoid (Negative Signal Prevention)

- Excessive provocation/aggressive tone (triggers block/mute)
- Obvious clickbait (triggers not_interested)
- Hashtag spam
- False/exaggerated claims
- Personal attacks

---

## Output Format

### For New Generation

```markdown
## 📝 Post Variations

### A: Classic
```
(post text)
```
**Algorithm Analysis**: [why this structure scores well]
**Target Signals**: favorite, retweet, dwell_time
**Characters**: XXX

### B: Hook-Heavy
...

### C: Discussion-Starter
...

---

## 🎨 Visual Suggestions

### Image Option 1: [title]
- Content: [description]
- Expected effect: dwell_time+, share+
- Creation difficulty: Low/Medium/High

---

## 📊 Recommendation

**Most effective**: Variation [A/B/C]
**Reason**: [selection rationale]
```

### For Thread Generation

```markdown
## 🧵 Thread Structure

### 1/5 (Hook)
```
(hook post)
```

### 2/5 (Context)
```
(context post)
```

...

---

## 📊 Thread Design Breakdown

| Post | Role | Target Signals |
|------|------|---------------|
| 1/5 | Hook | click, dwell |
| 2/5 | Context | dwell_time |
| ... | ... | ... |
```

---

## Interactive Questions Template

Use AskUserQuestion to collect:

### Basic Info

```
Q1: What are you posting about?
- Product/service announcement
- News/trend commentary
- Knowledge/how-to sharing
- Personal experience/learning
- Other

Q2: Core message in one sentence
(free input)

Q3: Target audience?
- Industry peers/experts
- General users/consumers
- Specific community
- As broad as possible
```

### Style

```
Q4: What tone fits best?
- Expert/authoritative
- Friendly/approachable
- Educational/explanatory
- Provocative/debate-starting
- Humorous/light

Q5: Format?
- Single post (short)
- Single post (detailed)
- Thread
- Quote RT comment
```

### Options

```
Q6: Visual assets?
- Yes (will provide)
- No (suggest some)
- Undecided

Q7: Priority?
- Virality (RT focus)
- Credibility/expertise
- Discussion/comments
- Follower growth

Q8: Output language?
- English
- Japanese
- Other (specify)
```

---

## Language Support

**Skill documentation**: English
**Output language**: User-specified (default: match user's input language)

When generating posts:
- Adapt hook patterns to target language conventions
- Consider character limits (Japanese ~140 chars = ~70 words in English)
- Use culturally appropriate expressions and references
