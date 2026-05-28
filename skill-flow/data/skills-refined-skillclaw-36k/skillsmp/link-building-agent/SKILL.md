---
name: link-building-agent
description: Strategic link acquisition through competitor analysis, broken link building, resource page outreach, and guest posting opportunities. Identifies link gaps, evaluates link quality, and automates prospecting. Use when building backlink profiles or improving domain authority.
---

# Link Building Agent

Strategische Backlink-Akquisition durch Analyse, Prospecting und Outreach.

## Quick Start

```
Input: Target Domain + Competitors + Link Goals
Output: Link Opportunities + Prioritized Prospects + Outreach Templates
```

## Link Building Methoden

| Methode | Aufwand | Qualität | Skalierbarkeit |
|---------|---------|----------|----------------|
| Guest Posting | Mittel | Hoch | Mittel |
| Broken Link Building | Niedrig | Mittel-Hoch | Hoch |
| Resource Page Outreach | Niedrig | Mittel | Hoch |
| Skyscraper Technique | Hoch | Sehr hoch | Niedrig |
| HARO/Expert Quotes | Mittel | Hoch | Mittel |
| Unlinked Mentions | Niedrig | Hoch | Mittel |
| Competitor Replication | Mittel | Variabel | Mittel |

Details: [LINK_BUILDING_METHODS.md](LINK_BUILDING_METHODS.md)

## Workflow

1. **Zieldefinition** → DA-Ziel, Link-Anzahl, Zeitrahmen
2. **Competitor Analysis** → Wer verlinkt auf Wettbewerber?
3. **Link Gap Analysis** → Welche Links fehlen dir?
4. **Prospecting** → Potenzielle Linkquellen finden
5. **Qualifizierung** → Links nach Wert bewerten
6. **Outreach** → Personalisierte Kontaktaufnahme
7. **Tracking** → Erfolge messen und dokumentieren

## Output Format

```json
{
  "campaign": {
    "target_domain": "example.com",
    "current_metrics": {
      "domain_authority": 45,
      "referring_domains": 234,
      "total_backlinks": 1892
    },
    "goals": {
      "target_da": 55,
      "new_links_needed": 50,
      "timeline": "6 months"
    }
  },
  "link_gap_analysis": {
    "competitors_analyzed": ["competitor1.com", "competitor2.com"],
    "common_referring_domains": 156,
    "unique_to_competitors": 89,
    "opportunities": [
      {
        "domain": "authority-site.com",
        "domain_authority": 72,
        "links_to_competitors": ["competitor1.com", "competitor2.com"],
        "link_type": "resource_page",
        "opportunity_score": 0.87,
        "contact_info": {
          "page": "https://authority-site.com/resources",
          "email": "editor@authority-site.com"
        }
      }
    ]
  },
  "prospects": {
    "guest_posting": [...],
    "broken_links": [...],
    "resource_pages": [...],
    "unlinked_mentions": [...]
  },
  "prioritized_actions": [
    {
      "priority": 1,
      "method": "broken_link",
      "target": "authority-site.com",
      "expected_value": "high",
      "effort": "low"
    }
  ]
}
```

## Link-Qualitäts-Bewertung

### Metriken

| Metrik | Gewichtung | Ideal |
|--------|------------|-------|
| Domain Authority (DA) | 25% | >50 |
| Relevanz | 30% | Thematisch passend |
| Traffic | 15% | >1000/Monat |
| Link-Platzierung | 15% | Im Content (nicht Footer) |
| DoFollow | 10% | Ja |
| Anchor Text | 5% | Natürlich, variiert |

### Scoring-Formel

```
Link Value Score =
  (DA × 0.25) +
  (Relevanz × 0.30) +
  (Traffic × 0.15) +
  (Platzierung × 0.15) +
  (DoFollow × 0.10) +
  (Anchor × 0.05)
```

### Qualitäts-Tiers

| Tier | Score | Beschreibung |
|------|-------|--------------|
| A | 0.8-1.0 | Premium Links, hoher Aufwand lohnt |
| B | 0.6-0.8 | Solide Links, Standard-Outreach |
| C | 0.4-0.6 | OK Links, nur wenn leicht zu bekommen |
| D | <0.4 | Vermeiden |

## Competitor Analysis

### Workflow

```
1. Top 5 Konkurrenten identifizieren
2. Backlink-Profile exportieren (Ahrefs/SEMrush)
3. Gemeinsame Linkquellen finden
4. Einzigartige Linkquellen pro Konkurrent
5. Link-Typ-Verteilung analysieren
6. Replizierbare Strategien identifizieren
```

### Was analysieren?

```
Pro Konkurrent:
- Referring Domains (Anzahl + Top 10)
- Link-Velocity (neue Links/Monat)
- Anchor Text Distribution
- DoFollow vs NoFollow Ratio
- Link-Typen (Guest Post, Resource, Mention, etc.)
- Top Content (was bekommt Links?)
```

Details: [COMPETITOR_ANALYSIS.md](COMPETITOR_ANALYSIS.md)

## Prospecting-Methoden

### 1. Google Search Operators

```
Gastbeiträge finden:
"[niche]" + "gastbeitrag"
"[niche]" + "Gastartikel einreichen"
"[niche]" + "schreiben Sie für uns"
inurl:gastautor [niche]

Resource Pages finden:
"[topic]" + "ressourcen"
"[topic]" + "nützliche links"
"[topic]" + "empfohlene websites"
inurl:links [topic]

Broken Links finden:
"[topic]" + "links" + site:edu
"[topic]" + "ressourcen" + intitle:links
```

### 2. Ahrefs/SEMrush Queries

```
Content Explorer:
- Topic + referring domains > 100
- Filter: One link per domain
- Sort: Domain Rating

Link Intersect:
- Input: 3 Konkurrenten
- Show: Links zu 2+ Konkurrenten
- Exclude: Already linking to you
```

### 3. Unlinked Mentions

```
Google Alerts:
- "[brand name]"
- "[product name]"
- "[ceo name]"

BrandMentions/Mention.com:
- Monitor brand mentions
- Filter: No link present
- Outreach to convert
```

## Outreach-Integration

### Mit press-outreach-bot

```
Für hochwertige Links (DA>60):
→ Nutze press-outreach-bot für personalisierte Pitches

Für Bulk-Outreach (DA 30-60):
→ Nutze Templates mit leichter Personalisierung
```

### Templates pro Methode

Details: [OUTREACH_TEMPLATES.md](OUTREACH_TEMPLATES.md)

## Tools-Integration

### Ahrefs API

```typescript
// Backlink-Daten abrufen
const getBacklinks = async (domain: string) => {
  const response = await ahrefs.backlinks({
    target: domain,
    mode: 'domain',
    limit: 1000
  });
  return response.backlinks;
};
```

### SEMrush API

```typescript
// Link Gap Analysis
const linkGap = async (myDomain: string, competitors: string[]) => {
  const response = await semrush.backlinks.gap({
    targets: [myDomain, ...competitors]
  });
  return response.results;
};
```

## Tracking & Reporting

### KPIs

| Metrik | Ziel | Messung |
|--------|------|---------|
| Neue Referring Domains | +10/Monat | Ahrefs |
| Avg. Link DA | >40 | Ahrefs |
| Link Velocity | Steigend | Ahrefs |
| Outreach Response Rate | >20% | Email Tool |
| Link Conversion Rate | >10% | Manuell |

### Reporting Template

```
Wöchentlicher Report:
- Outreach gesendet: XX
- Antworten erhalten: XX
- Links gesichert: XX
- Pending: XX
- Link-Wert (geschätzt): XX

Monatlicher Report:
- Neue Referring Domains: +XX
- DA-Veränderung: XX → XX
- Top Links gewonnen: [Liste]
- Erfolgreiche Methoden: [Ranking]
```

## Checkliste

- [ ] Competitor Backlinks analysiert?
- [ ] Link Gap identifiziert?
- [ ] Prospects qualifiziert (Tier A/B)?
- [ ] Outreach personalisiert?
- [ ] Tracking-Sheet eingerichtet?
- [ ] Follow-Up-Sequenz geplant?
- [ ] Spam-Links vermieden?
- [ ] Anchor Text variiert?
