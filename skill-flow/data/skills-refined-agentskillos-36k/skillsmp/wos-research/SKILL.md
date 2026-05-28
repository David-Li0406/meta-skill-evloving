---
name: wos-research
description: Researches Whiteout Survival game data from verified tiered sources. Use when looking up building costs, troop stats, hero info, chief gear, war academy, or any game mechanics. Automatically selects the best source based on topic and applies confidence levels.
allowed-tools: WebFetch(domain:www.whiteoutsurvival.wiki), WebFetch(domain:whiteoutsurvival.fandom.com), WebFetch(domain:whiteoutsurvival.app), WebFetch(domain:whiteoutdata.com), WebFetch(domain:www.quackulator.com), WebFetch(domain:onechilledgamer.com), WebFetch(domain:www.allclash.com), WebFetch(domain:www.bluestacks.com), WebFetch(domain:lootbar.gg), WebFetch(domain:www.ajackof.com), WebSearch, Read, Write, Glob
---

# WoS Research - Tiered Source Registry

## Design Principle
Use official/structured sources for mechanics & costs, community tools for tables/calculators, content creators only for meta (explicitly labeled).

## Research Rules (MUST FOLLOW)

1. **Mechanics > Meta**: If Wiki contradicts community guide, Wiki wins
2. **Tables > Advice**: If a calculator table exists, use it instead of prose
3. **Meta must be labeled**: Community/meta claims must have `claim_type: meta` and `confidence_cap: C`
4. **Cost data requires a table**: Never guess costs from text descriptions

## Source Tiers

### Tier 1 - Highest Trust (trust: 1.0)
Use for mechanics, rules, skill descriptions, system definitions.

| Source | URL | Use For | Do NOT Use For |
|--------|-----|---------|----------------|
| **WoS Wiki** | www.whiteoutsurvival.wiki | Mechanics, skills, unlock conditions, static tables | "Best" advice without meta label |
| **Official Help/Patch Notes** | In-game | Rules, limits, rally mechanics, skill stacking | Cost tables |

**Wiki wins over all other sources if conflict exists.**

### Tier 2 - Structured Calculators (trust: 0.85-0.9)
Use for cost tables and structured data.

| Source | URL | Use For | Do NOT Use For |
|--------|-----|---------|----------------|
| **whiteoutsurvival.app** | whiteoutsurvival.app | Building costs, FC levels (30-1 to FC10-0), prerequisites, War Academy | PvP advice, hero tiers |
| **Whiteout Data** | whiteoutdata.com | Building costs L1-L30, prerequisites | FC levels, strategy |
| **Quackulator** | www.quackulator.com | Chief gear costs, cost validation | Skill mechanics |
| **OneChilledGamer** | onechilledgamer.com | Troop training/promotion costs, event points | Strategy without meta label |

### Tier 3 - Community Meta (trust: 0.6)
**ALWAYS tag output as `claim_type: meta` and cap confidence at C.**

| Source | URL | Use For | Do NOT Use For |
|--------|-----|---------|----------------|
| **All Clash** | www.allclash.com | Hero tier lists, strategy guides | Mechanics, costs, exact percentages |
| **BlueStacks Guides** | www.bluestacks.com | Beginner guides, general strategy | Authoritative mechanics |
| **LootBar** | lootbar.gg | Event guides, hero analysis | Cost data |
| **A Jack Of** | www.ajackof.com | Hero analysis, guides | Exact costs |

### Tier 4 - Early Detection Only (trust: 0.4)
**Never emit without at least one stronger source.**

- Reddit/Discord/Facebook - Use only for early patch detection, edge cases

## Topic → Best Source Mapping

| Topic | Best Source | Endpoint |
|-------|-------------|----------|
| Building costs (L1-L30) | whiteoutdata.com | /{building}/ |
| Building costs (FC levels) | whiteoutsurvival.app | /buildings/{building}/ |
| War Academy costs | whiteoutsurvival.app | /buildings/war-academy/ |
| Chief Gear costs | quackulator.com | /chiefgear.php |
| Troop training/promotion | onechilledgamer.com | /whiteout-survival-troop-cost-calculator/ |
| Hero mechanics/skills | www.whiteoutsurvival.wiki | /heroes/{hero}/ |
| Hero tier lists | www.allclash.com | (label as meta!) |
| Rally mechanics | www.whiteoutsurvival.wiki | /advanced-guide-to-hero-rallies-buff/ |
| Server timeline | www.whiteoutsurvival.wiki | /events/server-timeline-server-age/ |

## Local Data - Check FIRST

Before fetching external sources, check if data already exists:

```
data/upgrades/buildings.edges.json      - Building L1-L30 (261 edges, 9 buildings)
data/upgrades/buildings.fc.edges.json   - Building FC levels (313 edges, 7 buildings)
data/upgrades/chief_gear.steps.json     - Chief gear costs (83 edges)
data/upgrades/war_academy.steps.json    - War Academy costs (45 edges)
data/upgrades/troops.train.edges.json   - Troop training (90 edges)
data/upgrades/troops.promote.edges.json - Troop promotion (75 edges)
data/research_sources.json              - Full source registry with all endpoints
data/heroes.json                        - Hero data
data/WOS_REFERENCE.md                   - Reference document
```

## Confidence Grades

| Grade | Meaning | When to Use |
|-------|---------|-------------|
| **A** | Direct table row from Tier 1-2 source | Calculator output, wiki table |
| **B** | Derived/calculated from Tier 1-2 source | Computed totals, cross-referenced |
| **C** | Meta/community consensus | Tier 3 sources (max for meta) |
| **D** | Unverified/single social source | Tier 4 only, needs verification |

## Output Format

For factual data:
```json
{
  "topic": "building_costs",
  "source_id": "whiteoutsurvival_app",
  "source_url": "https://whiteoutsurvival.app/buildings/furnace/",
  "claim_type": "fact",
  "confidence": "A",
  "data": { ... }
}
```

For meta claims:
```json
{
  "topic": "best_rally_heroes",
  "source_id": "allclash",
  "source_url": "https://www.allclash.com/whiteout-survival-best-heroes-tier-list/",
  "claim_type": "meta",
  "confidence": "C",
  "note": "Community consensus, may vary by server meta"
}
```

## Research Workflow

1. **Identify topic** - What type of data is needed?
2. **Check local data first** - Read from data/ if it exists
3. **Select best source** - Use Topic → Source mapping
4. **Fetch and extract** - WebFetch with specific prompt
5. **Apply confidence** - Based on source tier
6. **Label meta claims** - If Tier 3+, must label as meta
7. **ALWAYS WRITE TO FILES** - Save findings to appropriate data files (see below)
8. **Cite sources** - Always include URL and access date

## CRITICAL: Persisting Research Results

**Research is USELESS if not saved to files.** After gathering data, you MUST:

### File Destinations by Topic

| Topic | Write To | Format |
|-------|----------|--------|
| Hero skills/descriptions | `data/heroes.json` | Add `_desc` suffix fields |
| Hero mechanics | `data/heroes.json` + `data/WOS_REFERENCE.md` | JSON + markdown |
| Building costs | `data/upgrades/buildings.*.json` | Edge graph JSON |
| Chief gear | `data/chief_gear.json` | Structured JSON |
| Pets | `data/raw/pets.research.json` | Research JSON |
| Charms | `data/raw/chief_charms.research.json` | Research JSON |
| Research tree | `data/guides/research_priorities.json` | Guide JSON |
| Daybreak Island | `data/raw/daybreak_island.research.json` | Research JSON |
| Shop items | `data/shops.json` (create if missing) | Structured JSON |
| Chest types | `data/chests.json` (create if missing) | Structured JSON |
| General mechanics | `data/WOS_REFERENCE.md` | Markdown section |
| New system research | `data/raw/{system}.research.json` | Research JSON |

### Write Procedure

1. **Read existing file first** (required before editing)
2. **Merge new data** with existing (don't overwrite good data)
3. **Add metadata**: `retrieved_at`, `sources` array with URLs
4. **Validate JSON** before writing
5. **Update RESEARCH_QUESTIONS.md** - Mark items complete, add notes

### Research JSON Template

```json
{
  "system": "topic_name",
  "retrieved_at": "2026-01-10T00:00:00Z",
  "sources": [
    {"source_id": "SRC_NAME", "url": "https://...", "confidence": "A"}
  ],
  "data_completeness": "complete|partial",
  "overview": { ... },
  "details": { ... }
}
```

**If you complete research but don't write to files, the research is LOST.**

## Disallowed Sources (REFUSE TO USE)

- AI-generated blogs without citations
- SEO spam sites
- Tier lists with no data backing
- Unsourced Google Docs / screenshots

If user provides these, request a better source.

## Example Usage

**User**: "What are the costs for Furnace FC1-0 to FC5-0?"

1. Check local: `Read data/upgrades/buildings.fc.edges.json`
2. If not found: `WebFetch whiteoutsurvival.app/buildings/furnace/`
3. Extract FC level costs from table
4. Report with `confidence: A, source_id: whiteoutsurvival_app`

**User**: "Who are the best rally leaders?"

1. Fetch from allclash.com hero tier list
2. **MUST label**: `claim_type: meta, confidence: C`
3. Note: "Community consensus, individual results vary"
