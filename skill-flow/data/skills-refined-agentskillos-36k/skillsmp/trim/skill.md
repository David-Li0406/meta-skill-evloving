---
name: trim
description: Trim large tool outputs to free context space
---

To free context space, run:

```bash
./work --trim
```

This will:
1. Sync current session to episodic-memory (preserve full content)
2. Find tool outputs over 500 characters (configurable in .work.toml)
3. Truncate them, keeping first 500 chars + reference to original
4. Create new session file with trim metadata
5. Output resume command for the trimmed session

**Typical savings:** 30-50% on first trim.

**After trimming:**
- Run `claude --resume <session-id>` with the ID shown
- If you need full content of a truncated result, re-run the tool or search episodic-memory

**If trimming doesn't free meaningful space (<10% saved), use `/rollover` instead.**

**Configuration** (`.work.toml`):
```toml
[context]
trim_threshold_chars = 500           # Characters to keep before truncating
trim_target_tools = ["Read", "Bash", "Grep", "Glob"]  # Tools to trim
```
