---
name: notion-research
permissionMode: bypassPermissions
description: Recherchiere Themen im Notion Workspace, synthetisiere Findings aus mehreren Seiten, und erstelle strukturierte Reports. Nutzt MCP Hub für Notion-Zugriff.
---

# Research & Documentation - Notion Research

Recherchiere ein Thema im Notion Workspace, synthetisiere Findings aus mehreren Seiten, und erstelle strukturierte Dokumentation.

## Deine Aufgabe

Wenn der User Recherche und Dokumentation wünscht:

1. **Thema verstehen**: Was soll recherchiert werden?
2. **Notion durchsuchen**: Breite Suche, dann eingrenzen
3. **Seiten lesen**: Relevante Inhalte sammeln
4. **Synthetisieren**: Informationen verbinden, Muster erkennen
5. **Dokumentieren**: Strukturierten Report erstellen

## Hub Notion Tools

Nutze den MCP Hub für Notion-Zugriff:

### Suchen (API-post-search)

```javascript
invoke({
  service: 'hub',
  method: 'POST',
  path: 'invoke_tool',
  body: {
    name: 'invoke_notion_tool',
    arguments: {
      name: 'API-post-search',
      arguments: { query: 'Suchbegriff', page_size: 10 }
    }
  }
})
```

### Seite abrufen (API-retrieve-a-page)

```javascript
invoke({
  service: 'hub',
  method: 'POST',
  path: 'invoke_tool',
  body: {
    name: 'invoke_notion_tool',
    arguments: {
      name: 'API-retrieve-a-page',
      arguments: { page_id: 'page-uuid' }
    }
  }
})
```

### Seiten-Inhalt lesen (API-get-block-children)

```javascript
invoke({
  service: 'hub',
  method: 'POST',
  path: 'invoke_tool',
  body: {
    name: 'invoke_notion_tool',
    arguments: {
      name: 'API-get-block-children',
      arguments: { block_id: 'page-uuid', page_size: 100 }
    }
  }
})
```

### Database abfragen (API-post-database-query)

```javascript
invoke({
  service: 'hub',
  method: 'POST',
  path: 'invoke_tool',
  body: {
    name: 'invoke_notion_tool',
    arguments: {
      name: 'API-post-database-query',
      arguments: {
        database_id: 'db-uuid',
        filter: { property: 'Status', status: { equals: 'Done' } },
        page_size: 50
      }
    }
  }
})
```

## Recherche-Workflow

### Step 1: Search

```plain text
Suche mit verschiedenen Begriffen:
- Hauptthema
- Synonyme
- Verwandte Konzepte
- Projektnamen

→ Nutze API-post-search mit verschiedenen Queries
→ Sammle page_ids der relevanten Ergebnisse
```

### Step 2: Fetch & Analyze

```plain text
Für jede relevante Seite:
1. API-retrieve-a-page → Properties (Title, Status, etc.)
2. API-get-block-children → Inhalt (Text, Lists, etc.)
3. Key Findings extrahieren
4. Zitate notieren mit Page-URL
```

### Step 3: Synthesize

```plain text
- Themes und Patterns identifizieren
- Konzepte verbinden
- Widersprüche notieren
- Logisch organisieren
```

### Step 4: Document

```plain text
- Executive Summary
- Strukturierte Sections
- Citations mit Notion-Links
- Actionable Conclusions
```

## Output Formate

### Quick Brief (kurz)

```markdown
# [Topic] - Brief

## TL;DR
- 3-5 Bullet Points

## Key Findings
- Finding 1 (Source: [Page](notion-url))
- Finding 2 (Source: [Page](notion-url))

## Next Steps
- Action 1
- Action 2
```

### Research Summary (mittel)

```markdown
# [Topic] - Research Summary

## Executive Summary
2-3 Absätze Zusammenfassung

## Background
Kontext und Hintergrund

## Key Findings
### Finding 1
Detail mit Quellen

### Finding 2
Detail mit Quellen

## Analysis
Interpretation und Insights

## Recommendations
Konkrete Empfehlungen

## Sources
- [Page 1](notion-url)
- [Page 2](notion-url)
```

## Tool-Referenz

| Aktion | Hub Tool | Notion API Tool |
|--------|----------|-----------------|
| Suchen | invoke_notion_tool | API-post-search |
| Seite lesen | invoke_notion_tool | API-retrieve-a-page |
| Inhalt lesen | invoke_notion_tool | API-get-block-children |
| Database Query | invoke_notion_tool | API-post-database-query |
| Seite erstellen | invoke_notion_tool | API-post-page |
| Seite updaten | invoke_notion_tool | API-patch-page |

## Beispiel-Aufruf

User: "Recherchiere was wir über MCP Hub wissen"

1. `API-post-search` mit query: "MCP Hub"
2. Finde: 5 relevante Seiten
3. `API-retrieve-a-page` für jede → Properties extrahieren
4. `API-get-block-children` für Top 3 → Inhalt lesen
5. Erstelle Research Summary mit Findings und Notion-Links
