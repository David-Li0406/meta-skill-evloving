---
name: feed-create
description: Scaffold new feed configs with templates, discovery, and validation. Triggers include "create feed", "new feed config", "add RSS feed", or when setting up content pipeline feeds. Agent-friendly YAML generation for the epub content pipeline.
---

# feed-create

scaffold new feed configs with templates, discovery, and validation. agent-friendly YAML generation for the epub content pipeline.

## when to use

| use | skip |
|-----|------|
| creating new feed config from scratch | editing existing feed YAML |
| discovering feed source from URL | manual YAML editing |
| selecting template (reddit-digest, rss-readability) | one-off conversions (use epub url) |
| validating feed config before save | debugging feed pipeline issues |

## modes

| mode | trigger | behavior |
|------|---------|----------|
| **conversational** | "create feed about X", "make me a feed" | ask questions, infer config |
| **template** | "use reddit-digest template", "technical weekly" | select preset, customize |
| **discovery** | "feed from URL", paste blog/RSS URL | detect source, generate config |

## decision tree: mode selection

```
What input does user provide?
├── URL (blog, RSS, Reddit, GitHub) → discovery mode
├── Topic/description ("soccer news", "AI weekly") → conversational mode
├── Template name ("reddit-digest", "rss-readability") → template mode
├── Existing feed ID to modify → error (use edit, not create)
└── No input → ask "what kind of feed?"
```

## decision tree: source type detection

```
Given URL, what source type?
├── URL matches reddit.com/r/* → reddit
├── URL contains /feed.xml, /rss, /atom → rss
├── URL matches github.com/*/*/issues → github
├── HTML page with <link rel="alternate" type="application/rss+xml"> → rss
├── Blog with archive page → rss (discover feed URL)
└── Unknown → fallback to generic URL scraper
```

## workflow: conversational mode

```
1. ask-deep to gather intent
   ├── "What content do you want?" (topic, sources)
   ├── "How often?" (daily, weekly)
   ├── "What style?" (narrative, technical, minimal)
   └── "Any special features?" (threads, code highlighting)

2. infer source type
   ├── topic keywords → search for RSS feeds
   ├── subreddit mention → reddit source
   ├── GitHub repo → github issues/PRs

3. select template
   ├── matches reddit patterns → reddit_digest
   ├── mentions code/tech → rss_readability + technical profile
   └── default → minimal with narrative style

4. generate config
   ├── fill required: id, source
   ├── add style profile
   ├── set select params (since, max_items)
   └── validate with zod schema

5. preview and confirm
   ├── show generated YAML
   ├── ask "looks good?"
   └── save or iterate
```

## workflow: template mode

```
1. list available templates
   ├── reddit_digest - subreddit digests with comments
   ├── rss_readability - blog/RSS with content extraction
   ├── technical_weekly - engineering feeds with syntax highlighting
   └── minimal - basic RSS subscription

2. prompt for customization
   ├── template has placeholders ({{subreddit}}, {{url}})
   ├── ask for values
   └── optional: style override

3. generate from template
   ├── load template YAML
   ├── substitute placeholders
   ├── validate schema
   └── preview

4. save
   ├── write to ~/.epub/feeds/{id}.yaml
   ├── update feed registry
   └── output: "Feed created: {id}"
```

## workflow: discovery mode

```
1. fetch URL
   ├── check for RSS autodiscovery
   ├── parse HTML for feed links
   └── detect source type (reddit, github, blog)

2. extract metadata
   ├── title, description
   ├── author (if blog)
   ├── update frequency (guess from archive)
   └── content type (technical, narrative)

3. generate config
   ├── choose template based on detected type
   ├── fill source config
   ├── infer style profile from content
   └── set defaults (since: 48h, max_items: 25)

4. validate and preview
   ├── zod schema validation
   ├── show YAML
   └── confirm or customize
```

## config generation

### minimal example

```yaml
version: 1
feeds:
  - id: hn
    sources:
      - https://hnrss.org/frontpage
```

### reddit digest

```yaml
version: 1
templates:
  reddit_digest:
    select: { since: 24h, max_items: 20 }
    digest: { include_comments: top_3, group_by: flair }

feeds:
  - id: reddit-{{subreddit}}-digest
    extends: [reddit_digest]
    source: { type: reddit, subreddit: {{subreddit}} }
```

### technical blog

```yaml
version: 1
feeds:
  - id: {{slug}}
    source: {{rss_url}}
    style:
      profile: technical
      features: { syntax_highlighting: auto }
    select: { since: 7d, max_items: 40 }
```

## validation gates

```
Before saving:
├── zod schema validation PASS → continue
├── id is unique (check ~/.epub/feeds/) → continue
├── source URL reachable → continue
├── style profile exists (if specified) → continue
└── Any fail → show error, offer fixes
```

## tool integration

| tool | command | purpose |
|------|---------|---------|
| epub | `epub feed validate {yaml}` | schema validation |
| agents | `agents reference show {ref}` | load template reference |
| WebFetch | fetch URL for discovery | detect source type |
| ask-deep | conversational mode | gather intent |

### epub CLI integration

```bash
# Validate generated config
epub feed validate ~/.epub/feeds/new-feed.yaml

# Test fetch without saving
epub feed test new-feed.yaml --dry-run

# List available templates
epub feed templates
```

### agents integration

```bash
# Load template from reference bank
agents reference show reddit-digest --format yaml

# Save generated config as reference
agents reference save --type feed --name custom-digest
```

### ask-deep integration

```bash
# Conversational intake
# ask-deep runs in explore mode to gather:
# - content topic/sources
# - frequency (daily/weekly)
# - style preferences
# - special features
```

## file structure

```
~/.epub/feeds/
├── reddit-soccer-digest.yaml
├── engineering-weekly.yaml
└── custom/
    └── personal-blogs.yaml

~/.claude/skills/feed-create/
├── SKILL.md
├── references/
│   ├── templates.md          # available templates
│   ├── source-detection.md   # URL → source type rules
│   ├── config-patterns.md    # common config recipes
│   └── validation.md         # schema + gates
├── scripts/
│   ├── discover-feed.sh      # URL → feed metadata
│   ├── validate-config.sh    # zod schema check
│   └── list-templates.sh     # show available templates
└── assets/
    └── templates/
        ├── reddit-digest.yaml
        ├── rss-readability.yaml
        ├── technical-weekly.yaml
        └── minimal.yaml
```

## scripts

### discover-feed.sh

```bash
#!/bin/bash
# Discover feed metadata from URL
URL="$1"
curl -sL "$URL" | rg '<link.*alternate.*rss' | head -1
```

### validate-config.sh

```bash
#!/bin/bash
# Validate feed config with zod schema
YAML_FILE="$1"
cd ~/Developer/utils/epub
bun run -e "
import { validateFeedConfig } from './schemas/schema.ts';
import { readFileSync } from 'fs';
import { parse } from 'yaml';
const yaml = readFileSync('$YAML_FILE', 'utf8');
const data = parse(yaml);
const result = validateFeedConfig(data);
if (!result.success) {
  console.error(result.error.issues);
  process.exit(1);
}
console.log('✓ Valid feed config');
"
```

## anti-patterns

| pattern | problem | fix |
|---------|---------|-----|
| no validation before save | invalid YAML saved | always run validate-config.sh |
| duplicate IDs | feed conflicts | check ~/.epub/feeds/ for existing |
| missing required fields | schema fail | use templates with all required |
| unreachable source URL | feed will fail | test fetch before saving |
| no style profile | falls back to defaults | infer from content or ask |
| hard-coded templates in code | update friction | load from assets/templates/ |

## references

- [references/templates.md](references/templates.md) - available templates with examples
- [references/source-detection.md](references/source-detection.md) - URL → source type detection rules
- [references/config-patterns.md](references/config-patterns.md) - common config recipes and shortcuts
- [references/validation.md](references/validation.md) - zod schema validation and error handling

## next steps

after creating feed:
1. test fetch: `epub feed test {id} --dry-run`
2. run first sync: `epub feed sync {id}`
3. verify output: `epub library list --source feed:{id}`
4. add to device: `epub device sync --feeds`
