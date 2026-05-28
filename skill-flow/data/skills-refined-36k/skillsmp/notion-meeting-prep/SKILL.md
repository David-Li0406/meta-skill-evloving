---
name: notion-meeting-prep
permissionMode: bypassPermissions
description: Bereite Meetings vor durch Kontext-Sammlung aus Notion, Anreicherung mit Recherche, und Erstellung von Pre-Reads (intern) sowie Agendas (extern). Unterstützt Decision Meetings, Status Updates, Brainstorming und Customer Meetings.
---

# Meeting Intelligence - Notion Meeting Prep

Bereite ein Meeting vor, indem du Kontext aus Notion sammelst, mit Recherche anreicherst, und strukturierte Meeting-Dokumente erstellst.

## Deine Aufgabe

Wenn der User ein Meeting vorbereiten möchte:

1. **Kontext sammeln**: Frage nach Meeting-Details (Thema, Teilnehmer, Zweck, Datum)
2. **Notion durchsuchen**: Nutze die Notion API um relevante Seiten zu finden
3. **Inhalte analysieren**: Lies die relevanten Seiten und extrahiere Key Points
4. **Anreichern**: Füge relevantes Wissen hinzu (Best Practices, Frameworks, Kontext)
5. **Pre-Read erstellen**: Internes Dokument mit vollem Kontext für das Team
6. **Agenda erstellen**: Externes Meeting-Dokument für alle Teilnehmer

## Meeting-Typen

- **Decision Meeting**: Optionen, Pros/Cons, Empfehlung, Entscheidung
- **Status Update**: Fortschritt, Blocker, Next Steps
- **Brainstorming**: Constraints, Ideen-Sammlung, Priorisierung
- **Customer Meeting**: Professionell, fokussiert, externe Agenda

## Pre-Read Struktur (intern)

```markdown
# [Meeting Topic] - Pre-Read (Internal)

## Meeting Overview
- Datum, Zeit, Teilnehmer, Zweck

## Background Context
- Worum geht es (2-3 Sätze)
- Warum ist es wichtig
- Links zu relevanten Notion-Seiten

## Current Status
- Wo stehen wir
- Letzte Updates
- Key Metrics

## Context & Insights
- Industry Context / Best Practices
- Relevante Überlegungen

## Key Discussion Points
- Themen die besprochen werden müssen
- Offene Fragen
- Entscheidungen die getroffen werden müssen

## What We Need from This Meeting
- Erwartete Outcomes
- Entscheidungen
- Next Steps
```

## Agenda Struktur (extern)

```markdown
# [Meeting Topic] - Agenda

## Meeting Details
- Datum, Zeit, Teilnehmer

## Objective
- Klares Meeting-Ziel (1-2 Sätze)

## Agenda Items
1. Topic 1 (10 min)
2. Topic 2 (20 min)
3. Topic 3 (15 min)

## Discussion Topics
- Key Items
- Questions to answer

## Decisions Needed
- Decision points

## Action Items
- (Während Meeting ausfüllen)

## Related Resources
- Links zu relevanten Seiten
- Link zum Pre-Read
```

## MCP Hub Notion Tools

### Suchen (API-post-search)
```javascript
mcp__t0-hub__invoke({
  service: 'hub',
  method: 'POST',
  path: 'invoke_tool',
  body: {
    name: 'invoke_notion_tool',
    arguments: {
      name: 'API-post-search',
      arguments: { query: 'Meeting Thema oder Projekt', page_size: 10 }
    }
  }
})
```

### Seite abrufen (API-retrieve-a-page)
```javascript
mcp__t0-hub__invoke({
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
mcp__t0-hub__invoke({
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

### Meeting-Dokument erstellen (API-post-page)
```javascript
mcp__t0-hub__invoke({
  service: 'hub',
  method: 'POST',
  path: 'invoke_tool',
  body: {
    name: 'invoke_notion_tool',
    arguments: {
      name: 'API-post-page',
      arguments: {
        parent: { page_id: '{MEETINGS_FOLDER_ID}' },
        properties: { title: [{ text: { content: 'Meeting: [Thema] - Pre-Read' } }] },
        children: [/* Agenda/Pre-Read Inhalt als Blocks */]
      }
    }
  }
})
```

## Tool-Referenz

| Aktion | Hub Tool | Notion API Tool |
|--------|----------|-----------------|
| Suchen | invoke_notion_tool | API-post-search |
| Seite lesen | invoke_notion_tool | API-retrieve-a-page |
| Inhalt lesen | invoke_notion_tool | API-get-block-children |
| Meeting-Doc erstellen | invoke_notion_tool | API-post-page |
| Content hinzufügen | invoke_notion_tool | API-patch-block-children |

## Beispiel-Aufruf

User: "Bereite das Sprint Planning für morgen vor"

1. Suche nach: "Sprint", "Planning", "Backlog", aktuelles Projekt
2. Finde: Sprint Backlog, letzte Retro, offene Tasks
3. Erstelle Pre-Read mit: Status, offene Items, Velocity, Kapazität
4. Erstelle Agenda mit: Review, Planning Poker, Commitments

## Configuration

**Required**: Set `{MEETINGS_FOLDER_ID}` in your environment or replace in skill with your Notion page ID where meeting documents should be created.
