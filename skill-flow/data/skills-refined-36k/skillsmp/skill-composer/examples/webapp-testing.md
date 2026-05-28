# Example: Web Application Testing

**Source**: https://github.com/anthropics/skills/tree/main/webapp-testing
**Pattern**: Concise skill with helper scripts and decision tree
**Use case**: Testing local web applications with automated browser interaction

## Complete SKILL.md (96 lines)

This skill is notably **concise** compared to other official skills.

### Key Sections

**Helper Scripts Section** (Upfront):
```markdown
**Always run scripts with `--help` first** to see usage. DO NOT read the
source until you try running the script first and find that a customized
solution is absolutely necessary. These scripts can be very large and thus
pollute your context window.
```

**Decision Tree** (ASCII diagram):
```
User task → Is it static HTML?
    ├─ Yes → Read HTML file directly to identify selectors
    │         ├─ Success → Write Playwright script using selectors
    │         └─ Fails/Incomplete → Treat as dynamic (below)
    │
    └─ No (dynamic webapp) → Is the server already running?
        ├─ No → Run: python scripts/with_server.py --help
        │        Then use the helper + write simplified Playwright script
        │
        └─ Yes → Reconnaissance-then-action:
            1. Navigate and wait for networkidle
            2. Take screenshot or inspect DOM
            3. Identify selectors from rendered state
            4. Execute actions with discovered selectors
```

**Example: Using with_server.py**:
```bash
# Single server
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py

# Multiple servers (backend + frontend)
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

**Reconnaissance-Then-Action Pattern**:
1. Inspect rendered DOM (screenshot or page.content())
2. Identify selectors from inspection results
3. Execute actions using discovered selectors

**Common Pitfall**:
```markdown
❌ **Don't** inspect the DOM before waiting for `networkidle` on dynamic apps
✅ **Do** wait for `page.wait_for_load_state('networkidle')` before inspection
```

**Best Practices**:
- **Use bundled scripts as black boxes**
- Use `--help` to see usage, then invoke directly
- Always close the browser when done
- Always use `headless=True` for automation

**Reference Files**:
- examples/element_discovery.py
- examples/static_html_automation.py
- examples/console_logging.py

## Analysis

**What makes this work**:

1. **Extreme conciseness**: Only 96 lines total
2. **Helper script emphasis**: "DO NOT read source" - use --help first
3. **Decision tree upfront**: Visual ASCII diagram guides approach
4. **Progressive disclosure**: Brief SKILL.md, examples in separate directory
5. **Black box principle**: Scripts exist to be called, not ingested

## Unique Features

**Black Box Philosophy**:
"DO NOT read the source until you try running the script first and find that a customized solution is absolutely necessary."

Explicitly warns about context window pollution from large helper scripts.

**Decision Tree Diagram**:
ASCII-art decision tree showing three paths based on application type.

**Multi-Server Support**:
Can test applications requiring multiple services (backend API + frontend dev server).

**Reconnaissance Pattern**:
Inspect-first approach prevents brittle selectors. Discover what's actually rendered before writing automation.

**Always Headless**:
Explicitly requires `headless=True` for chromium launch in automation scripts.

## Pattern Type

**Helper script pattern** with:
- Concise SKILL.md (96 lines)
- External helper scripts (with_server.py)
- Examples directory
- Decision tree for complexity

## Key Takeaways

1. **Conciseness is valuable** - 96 lines vs 300+ for other skills
2. **Helper scripts as black boxes** - Don't pollute context by reading source
3. **--help first philosophy** - Scripts self-document their usage
4. **Decision trees guide approach** - ASCII diagram shows three paths
5. **Reconnaissance prevents brittleness** - Inspect before automating
6. **Progressive disclosure works** - Brief skill, detailed examples elsewhere
7. **Multi-server lifecycle management** - Helper script handles complexity
