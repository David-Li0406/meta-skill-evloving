---
name: www-studio
description: Use this skill when building websites, landing pages, or UI components using reference bank patterns. Triggers include "build a site like X", "create landing page", "implement this design", or when referencing audited sites for implementation. Consumes www-audit output to build production-ready code.
---

# www-studio

build websites and UI components using extracted references. turns www-audit analysis into production code.

## philosophy

> "references inform, they don't dictate"

| principle | application |
|-----------|-------------|
| reference-driven | use audited patterns, don't reinvent |
| incremental building | page by page, component by component |
| verification gates | test, typecheck, build after each phase |
| pattern adaptation | match patterns to target stack, not 1:1 copy |

## when to use

| use | skip |
|-----|------|
| "build a site like X" | analyzing a site (use www-audit) |
| "create landing page" | pure API backend work |
| "implement this design" | bug fixes in existing UI |
| "match this reference" | content changes only |
| new marketing site | incremental feature work |

## companion skill: www-audit

`www-audit` extracts patterns. `www-studio` applies them.

```
www-audit (extract) → reference bank → www-studio (build)
```

| skill | purpose |
|-------|---------|
| www-audit | analyze external sites, extract patterns |
| www-studio | build sites using extracted references |

## modes

| mode | trigger | output |
|------|---------|--------|
| **full** | "build a site like X" | complete site scaffold |
| **page** | "create landing page", "build pricing page" | single page |
| **component** | "implement nav like X", "build hero section" | specific component |
| **theme** | "apply X's color scheme", "match typography" | design tokens only |

## decision tree: mode selection

```
What mode should I use?
├── User wants complete site?
│   └── mode: full
├── User wants specific page?
│   └── mode: page
├── User wants UI component?
│   └── mode: component
├── User wants styling only?
│   └── mode: theme
└── Default
    └── mode: page (safest starting point)
```

## decision tree: reference selection

```
Which references to use?
├── User explicitly names site ("like linear.app")?
│   └── load that reference
├── User describes style ("minimal", "dark mode", "saas")?
│   └── agents reference search by tags
├── Multiple references mentioned?
│   └── load all, merge patterns (first = primary)
├── No reference mentioned?
│   └── prompt: "any site you'd like me to reference?"
└── Reference not in bank?
    └── offer to run www-audit first
```

## workflow

### phase 1: context gathering

```bash
# load reference(s)
REF_NAME="${1:-}"
REF=$(agents reference show "$REF_NAME" --json -q)

# check if reference exists
if [ -z "$REF" ]; then
  echo "Reference '$REF_NAME' not found. Run www-audit first?"
  exit 1
fi

# extract key info
STACK=$(echo "$REF" | jq -r '.stack')
PATTERNS=$(echo "$REF" | jq -r '.patterns[]')

# load audit for full context
AUDIT=$(agents reference show "$REF_NAME" --audit)
```

### phase 2: target project analysis

understand the project we're building in:

```bash
# detect project type
if [ -f "convex.json" ]; then
  PROJECT_TYPE="convex-next"
elif [ -f "next.config.ts" ] || [ -f "next.config.js" ]; then
  PROJECT_TYPE="next"
elif [ -f "vite.config.ts" ]; then
  PROJECT_TYPE="vite"
else
  PROJECT_TYPE="unknown"
fi

# get existing structure
layer . --format=json -q > /tmp/project-structure.json
outline src/ -r --format=yaml > /tmp/project-outline.yaml
```

### phase 3: stack alignment

map reference patterns to target stack:

| reference uses | target has | adaptation |
|----------------|------------|------------|
| Tailwind | Tailwind | direct use |
| Tailwind | SASS | convert utilities to classes |
| SASS | Tailwind | extract tokens, use utilities |
| CSS Modules | Tailwind | convert to utilities |
| Framer Motion | CSS only | simplify to CSS transitions |

```typescript
// example: reference uses Tailwind tokens
// target is SASS - convert to variables
const tailwindToSass = {
  'bg-background': '$color-background',
  'text-foreground': '$color-foreground',
  'text-muted-foreground': '$color-muted',
};
```

### phase 4: design token setup

before building components, establish tokens:

```bash
# if reference has design system in AUDIT.md
# extract and create tokens file

# for Tailwind projects (tailwind.config.ts)
# for SASS projects (styles/_variables.scss)
# for CSS-in-JS (theme.ts)
```

**Token mapping from reference:**

| reference token | target implementation |
|-----------------|----------------------|
| `--background` | `colors.background` or `$background` |
| `--foreground` | `colors.foreground` or `$foreground` |
| `--primary` | `colors.primary` or `$primary` |
| `--muted` | `colors.muted` or `$muted` |
| `--border` | `colors.border` or `$border` |
| `--radius` | `borderRadius.DEFAULT` or `$radius` |

### phase 5: component building

build incrementally, one component at a time:

```
Order of implementation:
1. Layout shell (header, footer, container)
2. Typography components (headings, body, links)
3. Buttons and CTAs
4. Cards and containers
5. Forms and inputs
6. Navigation
7. Page-specific sections (hero, features, pricing)
```

**For each component:**

```bash
# 1. reference the screenshot
open ~/.agents/references/web/$REF_NAME/screenshots/component-nav.png

# 2. read pattern notes from AUDIT.md
grep -A 20 "### Navigation" ~/.agents/references/web/$REF_NAME/AUDIT.md

# 3. implement component
# Write tool → src/components/nav.tsx

# 4. verify
verify --format=summary
pnpm typecheck
```

### phase 6: page assembly

combine components into pages:

```typescript
// example: landing page structure from reference
// reference pattern: hero → features → social-proof → cta → footer

export default function LandingPage() {
  return (
    <>
      <Header />
      <main>
        <HeroSection />
        <FeaturesSection />
        <TestimonialsSection />
        <CTASection />
      </main>
      <Footer />
    </>
  );
}
```

### phase 7: verification

after each major phase:

```bash
# type check
pnpm typecheck

# tests (if applicable)
verify --format=summary

# build
pnpm build

# visual check (if dev server running)
agent-browser open http://localhost:3000
agent-browser screenshot /tmp/build-check.png
```

## reference loading

### single reference

```bash
# load reference context for prompts
REF_CONTEXT=$(agents reference show linear-app --prompt)

# includes:
# - URL, domain, type
# - Stack info
# - Patterns list
# - Notes
# - Gist resources (if available)
```

### multiple references

```bash
# merge multiple references
PRIMARY=$(agents reference show linear-app --prompt)
SECONDARY=$(agents reference show stripe-com --prompt)

# use primary for structure, secondary for specific patterns
```

### reference screenshots

```bash
# list available screenshots
ls ~/.agents/references/web/$REF_NAME/screenshots/

# reference specific component
open ~/.agents/references/web/$REF_NAME/screenshots/component-hero.png

# use Read tool to view in context
# Read tool can display images
```

## pattern adaptation

### navigation

| reference pattern | implementation |
|-------------------|----------------|
| sticky-nav | `position: sticky; top: 0` |
| transparent-nav | `bg-transparent` on hero, solid on scroll |
| hamburger-mobile | responsive nav with mobile drawer |
| pill-nav | rounded-full links with active state |

### hero sections

| reference pattern | implementation |
|-------------------|----------------|
| centered-hero | flex col items-center text-center |
| split-hero | grid cols-2, text left, visual right |
| video-hero | background video with overlay |
| gradient-hero | gradient background or text gradient |

### component patterns

| reference pattern | implementation |
|-------------------|----------------|
| card-shadow | shadow-sm/md/lg based on reference |
| card-border | border with radius |
| card-glass | backdrop-blur with semi-transparent bg |
| button-solid | filled primary color |
| button-outline | border only, transparent bg |
| button-ghost | no border, text only |

## integration with loop

www-studio works well within loop for sustained building:

```
loop context:
- trajectory: build marketing site
- reference: async-app
- current phase: component building
- completed: tokens, layout
- next: hero section
```

```bash
# loop can call www-studio for focused work
# "implement hero section using async-app reference"
```

## verification gates

| gate | command | required |
|------|---------|----------|
| typecheck | `pnpm typecheck` | yes |
| lint | `pnpm lint` | yes |
| build | `pnpm build` | yes |
| test | `verify --format=summary` | if tests exist |
| visual | `agent-browser screenshot` | recommended |

## output contract

for skill composition, return structured JSON:

```json
{
  "mode": "full | page | component | theme",
  "status": "success | partial | blocked",
  "reference": "async-app",
  "target_project": "arbor-xyz",
  "artifacts": [
    {
      "type": "component",
      "path": "src/components/hero.tsx",
      "source_pattern": "centered-hero"
    },
    {
      "type": "tokens",
      "path": "tailwind.config.ts",
      "tokens_added": ["colors", "spacing"]
    }
  ],
  "verification": {
    "typecheck": "pass",
    "build": "pass",
    "tests": "pass"
  },
  "next_steps": ["implement features section", "add animations"],
  "confidence": 8,
  "summary": "Built hero section using async-app centered-hero pattern. Added gradient text and pill CTA button."
}
```

## concrete values

| metric | value | source |
|--------|-------|--------|
| component order | layout → typography → buttons → cards → forms → nav | UX layer cake |
| verification after | every major component | prevent drift |
| max components per phase | 3-5 | cognitive load |
| screenshot check frequency | after each page | visual regression |

## anti-patterns

| pattern | problem | fix |
|---------|---------|-----|
| copy-paste from reference | doesn't adapt to stack | translate patterns |
| building without reference | reinventing solved problems | always load reference context |
| skipping verification | errors compound | verify after each component |
| all components at once | hard to debug | incremental building |
| ignoring screenshots | miss visual details | always reference screenshots |
| no token setup first | inconsistent styling | establish tokens before components |

## example invocations

```
User: "build a landing page like async.app"
→ mode: page
→ load async-app reference
→ extract patterns: centered-hero, integration-grid, pill-buttons
→ implement: hero, features, integrations, CTA
→ verify: typecheck, build, visual check

User: "implement nav like linear.app"
→ mode: component
→ load linear-app reference
→ pattern: sticky-nav, command-palette trigger
→ implement: responsive nav with scroll behavior
→ verify: typecheck, visual check

User: "apply stripe's color scheme to my site"
→ mode: theme
→ load stripe-com reference
→ extract: color tokens, gradients
→ implement: update tailwind.config.ts
→ verify: build
```

## tool commands

| tool | command | purpose |
|------|---------|---------|
| agents reference | `show --prompt` | load reference context |
| agents reference | `show --audit` | get full audit |
| agents reference | `list --tags X` | find references |
| layer | `.` | understand project structure |
| outline | `src/ -r` | understand existing code |
| verify | `--format=summary` | run tests |
| agent-browser | `screenshot` | visual verification |

## trails integration

persist build sessions:

```bash
trails trail record --agent claude --action completed \
  --task "www-studio: built $COMPONENT using $REF_NAME" \
  --confidence $CONFIDENCE \
  --json -q
```

## references

- `~/.agents/references/` - reference bank
- `~/.agents/rules/references.md` - reference bank docs
- `~/.claude/skills/www-audit/SKILL.md` - extraction skill
- `~/.claude/skills/loop/SKILL.md` - sustained work integration
