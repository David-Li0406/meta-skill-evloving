---
name: use-the-best-tool
description: Use this skill when choosing CLI tools, a tool seems slow, or when "best tool", "which tool", or "tool alternatives" are mentioned.
---

# Use the Best Tool

Select optimal CLI tools → graceful fallback → research when needed.

<when_to_use>

- Choosing which tool for file search, content search, JSON processing
- Tool taking unexpectedly long for task size
- User expresses frustration with current tool
- Task could be done more elegantly
- Need to verify tool availability before recommending

NOT for: tasks where tool choice is predetermined, simple one-line commands

</when_to_use>

<detection>

Run detection script before selecting tools:

```bash
bun /Users/mg/Developer/outfitter/agents/baselayer/skills/use-the-best-tool/scripts/index.ts
```

Parse output to determine:
- Available modern tools
- Missing tools that could enhance workflow
- System context (OS, package managers)

Cache results per session — no need to re-run unless tool availability changes.

</detection>

<selection>

Map task to best available tool:

| Task | Preferred | Fallback | Legacy | Notes |
|------|-----------|----------|--------|-------|
| Find files by name | `fd` | - | `find` | fd: faster, better defaults |
| Search file contents | `rg` | - | `grep` | rg: respects .gitignore, faster |
| AST-aware code search | `sg` | `rg` | `grep` | sg: structure-aware queries |
| Process JSON | `jq` | - | `python`/`node` | jq: domain-specific language |
| View file with syntax | `bat` | - | `cat` | bat: syntax highlighting, git diff |
| List directory | `eza` | - | `ls` | eza: modern output, icons |
| View git diff | `delta` | - | `git diff` | delta: side-by-side, syntax highlighting |
| Navigate directories | `zoxide` | - | `cd` | zoxide: frecency-based jumping |
| Fuzzy select | `fzf` | - | - | fzf: interactive filtering |
| HTTP requests | `httpie` | - | `curl` | httpie: human-friendly syntax |

Selection algorithm:
1. Check detection results for preferred tool
2. If available → use with optimal flags
3. If unavailable → check fallback column
4. If no fallback → use legacy with best-effort flags
5. Note gap if preferred tool would significantly improve workflow

</selection>

<fallback>

When preferred tool unavailable:

**Minor improvement** (preferred 10–30% better):
- Use next best option silently
- Don't interrupt workflow

**Significant improvement** (preferred 2x+ better):
- Use fallback
- Surface suggestion: `◇ Alte

</fallback>