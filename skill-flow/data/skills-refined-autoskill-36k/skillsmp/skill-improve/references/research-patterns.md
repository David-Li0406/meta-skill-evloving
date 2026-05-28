# research patterns

how to find and extract primary sources for skill improvement.

## source hierarchy

| tier | source type | trust level | example |
|------|-------------|-------------|---------|
| 1 | source code | highest | github.com/author/repo/src/index.tsx |
| 2 | official docs | high | docs.library.com/api |
| 3 | author content | medium-high | blog posts by library author |
| 4 | tutorials | medium | official getting started guides |
| 5 | community | low | stack overflow, random blogs |

**always prefer tier 1-2 sources for concrete values.**

## research workflow

### step 1: identify the domain

```
What is the skill about?
└── Library? → Find npm package, read source
└── Framework? → Find official docs
└── Pattern? → Find canonical implementation
└── Tool? → Find CLI help, man pages, source
```

### step 2: gather sources

```bash
# for a library skill
npm view $PACKAGE repository.url
mcp__Ref__ref_search_documentation "$PACKAGE documentation"
WebFetch "https://raw.githubusercontent.com/$AUTHOR/$REPO/main/src/index.tsx"
```

### step 3: extract and document

for each source:
1. note the URL/path
2. extract concrete values
3. note any decision logic
4. capture anti-patterns mentioned

### step 4: cross-reference

- do values match between source and docs?
- are there version differences?
- what do tests expect?

### step 5: stop condition

stop when you have:
- 5+ concrete values with sources
- 1+ decision tree worth of logic
- 3+ anti-patterns with fixes
- references that are 50+ lines each

## source log template

```
| source | type | version/date | notes | values extracted |
|--------|------|--------------|-------|------------------|
| https://github.com/org/repo/blob/main/src/core.ts | code | commit abc123 | defaults table | duration=200, easing=out |
| https://docs.lib.com/api | docs | 2025-02-01 | props list | max=3, timeout=4000 |
```

## citation format

use a consistent citation in the skill:

```
| constant | value | source |
|----------|-------|--------|
| GAP | 14px | sonner/src/index.tsx:10 |
| TOAST_WIDTH | 356px | https://sonner.emilkowal.ski/getting-started |
```

## finding source code

### for npm packages

```bash
# find repo URL
npm view package-name repository.url

# common patterns
https://github.com/author/package-name
https://github.com/org/package-name
```

### reading source via WebFetch

```bash
# raw githubusercontent for direct file access
WebFetch "https://raw.githubusercontent.com/author/repo/main/src/index.tsx"

# for specific files, check package.json "main" or "exports"
```

### repo-local research

when the skill is about an internal tool or repo:

```bash
# scan for defaults and config
rg -n "default|defaults|const .*=" .

# find decision logic
rg -n "if .*\(|switch\(" .

# find config objects
rg -n "config|options|settings" .
```

## extracting concrete values

### timing/duration

look for:
- `duration`, `delay`, `timeout` variables
- millisecond values in animations
- transition properties in CSS/styled-components

document as:
```
| constant | value | source |
|----------|-------|--------|
| ANIMATION_DURATION | 200ms | src/animation.ts:15 |
```

### thresholds

look for:
- `threshold`, `min`, `max` variables
- conditional checks with numbers
- configuration limits

document as:
```
| threshold | value | purpose |
|-----------|-------|---------|
| SWIPE_THRESHOLD | 45px | minimum swipe distance to dismiss |
```

### configuration defaults

look for:
- `defaultProps`, `defaults`, `config` objects
- function parameter defaults
- context provider initial values

document as:
```
| option | default | range |
|--------|---------|-------|
| duration | 300 | 100-500 |
| easing | 'ease-out' | css easing |
```

## extracting decision logic

look for:
- branching conditions tied to user actions
- thresholds that change behavior
- feature flags or mode toggles

document as a decision tree with:
- condition
- action taken
- default path

## anti-pattern discovery

where to look:
- issue trackers and bug reports
- tests that encode expected failures
- README sections named "gotchas" or "caveats"
- code comments warning about pitfalls

capture as:
```
| pattern | problem | fix | source |
|---------|---------|-----|--------|
| useEffect without deps | rerender loop | add deps array | src/hooks.tsx:12 |
```

## using Ref MCP

### searching documentation

```bash
# search for library docs
mcp__Ref__ref_search_documentation "framer motion animation 2025"

# search for API patterns
mcp__Ref__ref_search_documentation "radix ui dialog accessibility"

# search for best practices
mcp__Ref__ref_search_documentation "react 19 server components patterns"
```

### reading specific pages

```bash
# read search result URL
mcp__Ref__ref_read_url "https://docs.example.com/api/animation"

# read github source
mcp__Ref__ref_read_url "https://github.com/author/repo/blob/main/src/core.ts"
```

## example: researching sonner (toast library)

```bash
# 1. find repo
npm view sonner repository.url
# -> https://github.com/emilkowalski/sonner

# 2. read main source
WebFetch "https://raw.githubusercontent.com/emilkowalski/sonner/main/src/index.tsx"

# extracted:
# - GAP = 14 (line 10)
# - TOAST_WIDTH = 356 (line 11)
# - VISIBLE_TOASTS_AMOUNT = 3 (line 13)
# - SWIPE_THRESHOLD = 45 (line 18)
# - TIME_BEFORE_UNMOUNT = 200 (line 19)

# 3. read docs
mcp__Ref__ref_search_documentation "sonner toast react"
mcp__Ref__ref_read_url "https://sonner.emilkowal.ski/getting-started"

# 4. document in skill
| constant | value | source |
|----------|-------|--------|
| GAP | 14px | sonner/src/index.tsx:10 |
| TOAST_WIDTH | 356px | sonner/src/index.tsx:11 |
| SWIPE_THRESHOLD | 45px | sonner/src/index.tsx:18 |
```

## common research targets

| skill type | research target |
|------------|-----------------|
| animation | framer-motion source, CSS spec |
| UI components | radix-ui source, WAI-ARIA spec |
| state management | library source, React docs |
| testing | vitest/jest source, testing-library |
| CLI tools | --help output, man pages, source |

## failure signals

- only tier 4-5 sources available
- no constants or defaults found
- values differ across sources without explanation
- references are thin or stubby

when you see these, pause and ask for more context or deeper sources.
