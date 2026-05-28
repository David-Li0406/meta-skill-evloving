---
name: twitter
description: X/Twitter via bird CLI. Use when user mentions Twitter, X, tweeting, posting, reading tweets, or wants to check their feed. Includes /twitter-digest for curated feed filtering. (user)
---

# Twitter

`bird` CLI for X/Twitter. Account: @odysseus0z

Runs from local `~/projects/bird` (personal branch). Update: `cd ~/projects/bird && git pull && npm run build`

## Quick Reference

```bash
bird tweet "text"              # post
bird reply <url> "text"        # reply
bird read <url>                # read tweet (full article body)
bird search "query" -n 10      # search
bird mentions -n 10            # mentions
bird bookmarks -n 10           # bookmarks
bird home -n 20                # home timeline
bird home --following -n 20    # following-only timeline
```

Run `bird --help` for full syntax.

---

## /twitter-digest

Curated feed that filters the home timeline, protecting attention from algorithmic engagement bait.

### Process

1. **Fetch**: `bird home -n 40`

2. **Filter each tweet** by:
   - Signal vs noise (insight vs engagement bait)
   - Relevance to user's interests
   - Quality of thought (original vs retweet farming)
   - Actionability (something to learn or do?)

3. **Present digest**:

```markdown
## Twitter Digest

### Worth Your Attention (N items)

**@username** — [why relevant]
> Tweet preview...
> [link]

---

### Skipped (N items)
<details>
<summary>Review what I filtered</summary>

- **@user**: "preview..." — *reason* [→ link]
- ...
</details>

---

### Feedback
Did I filter correctly?
- Anything I should have included?
- Anything I included that wasn't useful?
```

### Include
- Original insights
- Threads with depth
- Relevant news/updates
- Interesting people, interesting thoughts

### Skip
- Engagement bait ("hot takes...")
- Rage bait, dunking, drama
- Repetitive content
- Self-promotion without substance
- Vague motivational fluff

### Iteration
v1 uses AI judgment. As user provides feedback, patterns emerge → eventually capture in a personalization profile.
