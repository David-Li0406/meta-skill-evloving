---
name: internal-linker
description: Analyzes article content and existing site structure to suggest and insert relevant internal links. Considers semantic relevance, anchor text optimization, and link equity distribution. Prevents orphan pages and creates topic clusters. Use after writing content or when optimizing internal link structure.
---

# Internal Linker

Intelligente interne Verlinkung basierend auf Content-Analyse und Seitenstruktur.

## Quick Start

```
Input: Artikel-Content + Bestehende Artikel-Datenbank
Output: Link-Vorschläge mit Anchor-Text + optimierter Content
```

## Workflow

1. **Artikel-Inventar laden** → Alle bestehenden URLs + Titles + Topics
2. **Neuen Content analysieren** → Themen, Keywords, Entities extrahieren
3. **Semantische Matches finden** → [SEMANTIC_ANALYSIS.md](SEMANTIC_ANALYSIS.md)
4. **Link-Stellen identifizieren** → Natürliche Ankerpunkte im Text
5. **Anchor-Text optimieren** → [ANCHOR_TEXT_STRATEGIES.md](ANCHOR_TEXT_STRATEGIES.md)
6. **Link-Struktur validieren** → Keine Orphan Pages, ausgewogene Verteilung
7. **Links einfügen** → Mit optimiertem Anchor-Text

## Output Format

```json
{
  "article_id": "uuid",
  "internal_links": {
    "outbound": [
      {
        "target_url": "/artikel-xyz",
        "target_title": "Zielartikel Titel",
        "anchor_text": "optimierter Anchor Text",
        "position": {
          "paragraph": 3,
          "context": "...Text vor [LINK] Text nach..."
        },
        "relevance_score": 0.85,
        "reason": "Thematisch verwandt: beide über Content Marketing"
      }
    ],
    "inbound_suggestions": [
      {
        "source_url": "/anderer-artikel",
        "source_title": "Quell-Artikel Titel",
        "suggested_anchor": "Anchor für Link hierher",
        "reason": "Erwähnt [Thema], sollte hierher verlinken"
      }
    ]
  },
  "orphan_page_warnings": [],
  "link_equity_analysis": {
    "pages_linking_here": 5,
    "pages_this_links_to": 8,
    "status": "balanced"
  }
}
```

## Link-Typen

| Typ | Beschreibung | Priorität |
|-----|--------------|-----------|
| Contextual | Im Fließtext, thematisch relevant | Hoch |
| Related | "Weitere Artikel" Section | Mittel |
| Navigation | Kategorien, Tags | Niedrig |
| CTA | "Mehr erfahren" Links | Mittel |

## Relevanz-Kriterien

Links werden vorgeschlagen basierend auf:

1. **Thematische Übereinstimmung** (40%)
   - Gleiche/ähnliche Hauptkeywords
   - Überlappende Topics

2. **Semantische Nähe** (30%)
   - Entity-Matching (Personen, Produkte, Konzepte)
   - LSI-Keywords

3. **User Intent Match** (20%)
   - Gleiche Suchintention
   - Logische Weiterführung

4. **Link-Struktur** (10%)
   - Seite braucht mehr Links (Orphan Prevention)
   - Wichtige Seite verdient mehr Links

## Anchor-Text Regeln

### DO ✅
- Beschreibend und natürlich
- Keyword-relevant aber nicht stuffed
- Variiert (nicht immer gleicher Anchor)
- Im Kontext sinnvoll

### DON'T ❌
- "Hier klicken"
- "Mehr erfahren" (als einziger Anchor)
- Exact-Match-Keyword-Stuffing
- Zu lange Anchors (>5 Wörter)

Details: [ANCHOR_TEXT_STRATEGIES.md](ANCHOR_TEXT_STRATEGIES.md)

## Orphan Page Prevention

Jede Seite sollte:
- Mind. 3 interne Links erhalten
- Mind. 3 interne Links ausgeben
- Innerhalb von 3 Klicks von Homepage erreichbar sein

## Integration

### Mit Supabase
```typescript
// Alle Artikel laden
const { data: articles } = await supabase
  .from('articles')
  .select('id, title, slug, content, seo_keywords')
  .eq('status', 'published');

// An Internal Linker übergeben
const linkSuggestions = await internalLinker.analyze(newArticle, articles);
```

### Output anwenden
```typescript
// Links in Content einfügen
const linkedContent = internalLinker.applyLinks(
  article.content,
  linkSuggestions.outbound
);
```

## Checkliste

- [ ] Alle bestehenden Artikel geladen?
- [ ] Mind. 3 ausgehende Links pro Artikel?
- [ ] Anchor-Texte variiert?
- [ ] Keine Orphan Pages entstanden?
- [ ] Links thematisch sinnvoll?
- [ ] Link-Verteilung ausgewogen?
