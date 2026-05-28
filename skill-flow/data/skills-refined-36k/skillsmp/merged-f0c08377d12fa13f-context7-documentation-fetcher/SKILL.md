---
name: context7-documentation-fetcher
description: Use this skill to fetch up-to-date library documentation via the Context7 API when working with external libraries or when specific API information is needed.
---

# Context7 Documentation Fetcher

Retrieve current library documentation via the Context7 API.

## Authentication

This skill requires a Context7 API key in `CONTEXT7_API_KEY`. Set it up using one of the following methods:

1. Export it in your shell profile (global):

   ```bash
   export CONTEXT7_API_KEY="your-context7-key"
   ```

2. Use a local `.env` file (per-repo):

   ```bash
   cp skills/context7/.env.example .env
   set -a; source .env; set +a
   ```

## Workflow

### 1. Search for the library

```bash
python3 ~/.config/opencode/skill/context7/scripts/context7.py search "<library-name>"
```

Returns library metadata including the `id` field needed for step 2.

### 2. Fetch documentation context

```bash
python3 ~/.config/opencode/skill/context7/scripts/context7.py context "<library-id>" "<query>"
```

Options:
- `--type txt|md` - Output format (default: txt)
- `--tokens N` - Limit response tokens

## Quick Reference

| Task | Command |
|------|---------|
| Find React docs | `search "react"` |
| Get React hooks info | `context "/facebook/react" "useEffect cleanup"` |
| Find Supabase | `search "supabase"` |
| Get Supabase auth | `context "/supabase/supabase" "authentication row level security"` |

## When to Use

- Before implementing any library-dependent feature.
- When unsure about current API signatures or library version-specific behavior.
- To verify best practices and patterns.
- Most importantly, when installing dependencies, libraries, or frameworks, always check the docs for the latest versions.