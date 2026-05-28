---
name: hm-options
description: Search home-manager configuration options. Use when looking up home-manager options, checking available settings, or understanding option types and defaults.
argument-hint: [search-term]
allowed-tools: Bash, Grep, Read
---

# Home Manager Options Searcher

Search the home-manager options database cached at `~/.cache/hm-options/options.xhtml`.

## Cache Management

First, check if the cache exists and is fresh (less than 1 day old):

```bash
CACHE_FILE="$HOME/.cache/hm-options/options.xhtml"
CACHE_DIR="$HOME/.cache/hm-options"

if [[ ! -f "$CACHE_FILE" ]] || [[ $(find "$CACHE_FILE" -mtime +1 2>/dev/null) ]]; then
  mkdir -p "$CACHE_DIR"
  curl -sL "https://nix-community.github.io/home-manager/options.xhtml" -o "$CACHE_FILE"
  echo "Cache updated."
fi
```

## Search Task

Search for: **$ARGUMENTS**

1. Use Grep to search the XHTML file for option names matching the search term
2. Search patterns to try:
   - `class="option".*$ARGUMENTS` for option names
   - Case-insensitive search in descriptions
3. When matches are found, read the surrounding context to extract:
   - Option name (in `<code class="option">`)
   - Type (after `<em>Type:</em>`)
   - Default value (after `<em>Default:</em>`)
   - Description (in `<p>` after the option)
4. Format results clearly showing each option with its type, default, and description
5. If no exact match, try partial matches or suggest similar options

## Output Format

For each matching option, show:

```
## option.name.here

**Type:** <type>
**Default:** <default value>

<description>
```
