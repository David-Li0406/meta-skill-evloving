---
name: planning-with-files
description: Verwaltet komplexe, mehrstufige Projekte durch persistentes Tracking in Markdown-Dateien (task_plan.md, findings.md, progress.md). Automatisch aktiviert bei komplexen Architektur-, Recherche- oder Implementierungsaufgaben.
---

# Planning with Files Skill

Dieser Skill implementiert den "Planning with Files" Workflow für komplexe, mehrstufige Aufgaben. Das Dateisystem wird als persistenter Arbeitsspeicher verwendet.

## Philosophie

**"Markdown ist mein Arbeitsspeicher auf der Festplatte"**

- Komplexe Aufgaben werden in Phasen aufgeteilt
- Jede Recherche, Entscheidung und Erkenntnis wird dokumentiert
- Vor wichtigen Aktionen wird der Plan re-gelesen
- Kein "Goal Drift" durch kontinuierliches Tracking

## Drei zentrale Dateien

### 1. `.planning/task_plan.md` - Phasen & Fortschritt
**Zweck:** High-level Roadmap des gesamten Projekts

**Struktur:**
```markdown
# Task Plan: [Projektname]

**Status:** [Phase] - [Fortschritt]
**Letzte Aktualisierung:** [Datum + Uhrzeit]

## Übersicht
[1-2 Sätze: Was ist das Gesamtziel?]

## Phasen

### Phase 1: [Name] - [Status: 🔄 In Arbeit / ✅ Fertig / ⏸️ Wartend]
**Ziel:** [Was soll erreicht werden?]
**Status:** [Detaillierter Status]

Aufgaben:
- [x] Abgeschlossene Aufgabe
- [ ] Offene Aufgabe
- [ ] Weitere Aufgabe

**Nächster Schritt:** [Was kommt als nächstes?]

---

### Phase 2: [Name] - [Status]
...

## Offene Fragen
- **FRAGE:** [Frage an User]
- **FRAGE:** [Weitere Frage]

## Entscheidungslog
- **[Datum]** [Kurze Entscheidung und Begründung]
```

### 2. `.planning/findings.md` - Recherche & Entscheidungen
**Zweck:** Detaillierte technische Erkenntnisse und Design-Entscheidungen

**Struktur:**
```markdown
# Findings: [Projektname]

## Recherche-Ergebnisse

### [Tool/Technologie] - [Datum]
[Detaillierte Analyse, siehe repo-architecture-research Skill]

### [Weiteres Thema] - [Datum]
...

## Design-Entscheidungen

### [Thema, z.B. "Storage-Architektur"] - [Datum]
**Problem:**
- ...

**Optionen:**
1. [Option A]: ...
2. [Option B]: ...

**Entscheidung:** [Option X]
**Begründung:**
- ...

**Implikationen:**
- ...

## Code-Snippets & Beispiele
[Relevante Code-Beispiele, Konfigurationen, etc.]

## Referenzen
- [URL] - [Beschreibung]
- [Dokument] - [Beschreibung]
```

### 3. `.planning/progress.md` - Session-Log
**Zweck:** Chronologisches Log aller Sessions und Ergebnisse

**Struktur:**
```markdown
# Progress Log: [Projektname]

## Session [Datum] [Uhrzeit]

**Dauer:** [Start - Ende]
**Phase:** [Aktuelle Phase]
**Ziel:** [Was sollte erreicht werden?]

### Durchgeführte Aktionen
- [Aktion 1]
- [Aktion 2]
- ...

### Ergebnisse
- [Ergebnis 1]
- [Ergebnis 2]

### Tests / Validierung
- [Test 1]: [Ergebnis]
- [Test 2]: [Ergebnis]

### Erkenntnisse
- [Erkenntnis 1]
- ...

### Blockiert / Probleme
- [Problem 1]
- [Problem 2]

### Nächste Session
- [ ] [Aufgabe für nächste Session]
- [ ] [Weitere Aufgabe]

---

## Session [Vorheriges Datum] [Uhrzeit]
...
```

## Workflow

### Bei Session-Start
1. **Prüfe ob `.planning/` existiert**
   - Falls nein: Initialisiere mit Template-Dateien
2. **Lese `task_plan.md`**
   - Verstehe aktuellen Phase-Status
   - Identifiziere nächste Aufgaben
3. **Bestätige Ziel** mit User falls unklar

### Während der Arbeit
1. **2-Action Rule für Recherche:**
   - Nach jeweils 2 WebFetch/Read/Grep-Operationen:
   - Aktualisiere `findings.md` mit neuen Erkenntnissen

2. **Vor wichtigen Tool-Calls:**
   - Lese relevanten Abschnitt aus `task_plan.md`
   - Verifiziere dass Aktion zum Plan passt

3. **Nach Phasen-Abschluss:**
   - Markiere Phase in `task_plan.md` als ✅ Fertig
   - Füge Eintrag in Entscheidungslog hinzu
   - Starte nächste Phase

### Bei Session-Ende
1. **Erstelle Session-Eintrag** in `progress.md`
   - Was wurde gemacht?
   - Was sind die Ergebnisse?
   - Was ist für nächstes Mal geplant?

2. **Aktualisiere `task_plan.md`**
   - Aktuellen Status markieren
   - "Letzte Aktualisierung" Timestamp

3. **Prüfe Vollständigkeit:**
   - Sind alle Phasen abgeschlossen?
   - Gibt es offene Fragen?

## Automatisierung durch Hooks

Dieser Skill wird unterstützt durch Hooks (siehe `.claude/settings.json`):

- **SessionStart:** Initialisiert `.planning/` falls nicht vorhanden
- **PreToolUse:** Liest `task_plan.md` vor Edit/Write/Task
- **PostToolUse:** Trigger für findings.md Update nach Research
- **Stop:** Erstellt Session-Log in progress.md

## Phasen-Struktur für Chantal-Projekt

Typischer Phasenplan für dieses Projekt:

```
Phase 1: Recherche & Tool-Analyse (3-7 Tage)
├─ Analyse: apt-mirror, aptly
├─ Analyse: reposync, DNF
├─ Analyse: bandersnatch, devpi (PyPI)
├─ Vergleichsmatrix
└─ Lessons Learned

Phase 2: Anforderungs-Konsolidierung (1-2 Tage)
├─ Must/Should/Nice-Kategorisierung
├─ Explizite Nicht-Ziele
└─ Rückfragen-Runde mit User

Phase 3: Architektur-Design (3-5 Tage)
├─ Komponenten-Übersicht
├─ Storage-Layout
├─ Plugin-Interfaces
├─ State-Management-Konzept
└─ Sync/Snapshot-Workflows

Phase 4: Implementierungsplan (1-2 Tage)
├─ MVP-Scope Definition
├─ Iterationsplan
├─ Risiko-Analyse
└─ Teststrategie

Phase 5: Implementation (iterativ)
├─ Core-Framework
├─ APT-Plugin
├─ RPM-Plugin
└─ CLI & Konfiguration
```

## Best Practices

### DO:
- Aktualisiere Dateien kontinuierlich (nicht erst am Ende)
- Nutze konkrete Timestamps für Nachvollziehbarkeit
- Markiere Annahmen explizit: `**ANNAHME:**`
- Stelle offene Fragen explizit: `**FRAGE:**`
- Verweise auf Quellen (URLs, Commits, Dokumente)

### DON'T:
- Warte nicht bis zum Ende mit Dokumentation
- Vergiss nicht task_plan.md vor wichtigen Entscheidungen zu lesen
- Lasse keine "Goal Drift" zu - prüfe regelmäßig den Plan
- Erstelle keine riesigen Monolith-Einträge (besser: kontinuierlich kleine Updates)

## Qualitätskriterien

- **Nachvollziehbarkeit:** Jemand Neues kann aus den Dateien den Projektstatus verstehen
- **Aktualität:** Status-Informationen sind aktuell (< 1 Tag alt)
- **Vollständigkeit:** Alle wichtigen Entscheidungen sind dokumentiert
- **Präzision:** Technisch korrekt, keine vagen Aussagen
- **Deutsch:** Alle Dokumentation auf Deutsch (Code-Kommentare können Englisch sein)

## Integration mit anderen Skills

- **repo-architecture-research:** Schreibt direkt in `findings.md`
- **TodoWrite Tool:** Ergänzt (nicht ersetzt) die Planning-Dateien
  - TodoWrite: Kurzfristige Task-Tracking innerhalb einer Session
  - Planning Files: Langfristige Projekt-Übersicht über Sessions hinweg
