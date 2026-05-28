---
name: codebase-search
description: Advanced codebase search using Mantic for finding files, understanding context, and analyzing code impact. Use this skill when searching for code, files, or understanding code relationships.
---

# Codebase Search with Mantic

You have access to Mantic via the terminal with enhanced search features.

---

## Basic Search

```bash
mantic "your query here"
```

---

## Advanced Features

**Zero-Query Mode (Context Detection):**
```bash
mantic ""  # Shows modified files, suggestions, impact
```

**Context Carryover (Session Mode):**
```bash
mantic "query" --session "session-name"
```

**Output Formats:**
```bash
mantic "query" --json        # Full metadata
mantic "query" --files       # Paths only
mantic "query" --markdown    # Pretty output
```

**Impact Analysis:**
```bash
mantic "query" --impact  # Shows blast radius
```

**File Type Filters:**
```bash
mantic "query" --code     # Code files only
mantic "query" --test     # Test files only
mantic "query" --config   # Config files only
```

---

## Search Quality Features

- **CamelCase detection**: "ScriptController" finds script_controller.h
- **Exact filename matching**: "download_manager.cc" returns exact file first
- **Path sequence**: "blink renderer core dom" matches directory structure
- **Word boundaries**: "script" won't match "javascript"
- **Directory boosting**: "gpu" prioritizes files in gpu/ directories

---

## Best Practices

**Do NOT use grep/find blindly. Use Mantic first.**

Mantic provides intelligent search with context awareness, making it superior to traditional grep/find commands for code exploration.
