---
name: repo-architecture-research
description: Strukturierte Architektur-Recherche und -Analyse für Repository-Management-Tools (APT, RPM, PyPI). Automatisch aktiviert bei Recherche-Aufgaben zu apt-mirror, aptly, reposync, bandersnatch, devpi oder ähnlichen Tools.
---

# Repository-Architektur-Recherche Skill

Dieser Skill führt strukturierte Recherche und Analyse von Repository-Management-Tools durch, wie in PROMPT.md spezifiziert.

## Anwendungsbereich

Aktiviere diesen Skill automatisch wenn:
- Analyse bestehender Tools (apt-mirror, aptly, reposync, bandersnatch, devpi, etc.)
- Vergleich von Repository-Sync-Architekturen
- Recherche zu Metadaten-Formaten (APT InRelease, RPM repodata, PyPI Simple Index)
- Untersuchung von Deduplikations- und Storage-Strategien
- Design-Entscheidungen für das Unified Repository Sync Tool

## Workflow

### 1. Recherche-Struktur

Für jedes Tool analysiere systematisch:

#### A. Funktionsübersicht
- Kernfunktionen (Mirror, Snapshot, Publish, etc.)
- CLI-Interface und Kommandos
- Konfigurationsmechanismus

#### B. Architektur
- Storage-Layout (wie werden Artefakte gespeichert?)
- Metadaten-Handling (original oder regeneriert?)
- State-Management (DB, Files, oder beides?)
- Deduplikation (wenn vorhanden)

#### C. Repository-Typ-Spezifika
**APT:**
- Umgang mit InRelease/Release/Release.gpg
- Signaturen (übernommen oder neu?)
- Multi-Arch Handling

**RPM:**
- repodata-Handling (kopiert oder regeneriert?)
- modules.yaml, comps.xml Behandlung
- DeltaRPM Support

**PyPI:**
- Simple Index API (PEP 503)
- JSON API vs. Simple Index
- Wheel vs. Source Distributions
- Package Metadata (PKG-INFO, METADATA)
- Hash-Verifizierung (SHA256)

#### D. Snapshot-Konzept
- Hat das Tool Snapshot-Funktionalität?
- Wie werden Snapshots erstellt? (Metadaten-Kopie, Symlinks, etc.)
- Sind Snapshots konsistent und reproduzierbar?

#### E. Stärken & Schwächen
- Was macht das Tool besonders gut?
- Welche Limitierungen existieren?
- Wartbarkeit und aktuelle Entwicklung

### 2. Dokumentation in findings.md

Nach jeder Tool-Analyse:

1. **Erstelle strukturierten Abschnitt** in `.planning/findings.md`:
```markdown
## Tool: [Name] - [Datum]

### Funktionsübersicht
- ...

### Architektur
**Storage:**
- ...

**Metadaten:**
- ...

**State:**
- ...

### APT-Spezifika / RPM-Spezifika
- ...

### Snapshot-Konzept
- ...

### Bewertung
**Stärken:**
- ...

**Schwächen:**
- ...

**Lessons Learned für unser Tool:**
- ...
```

### 3. Vergleichsmatrix

Nach Analyse mehrerer Tools erstelle Vergleichstabelle:

| Kriterium | apt-mirror | aptly | reposync | bandersnatch | devpi |
|-----------|------------|-------|----------|--------------|-------|
| Storage-Modell | ... | ... | ... | ... | ... |
| Deduplikation | ... | ... | ... | ... | ... |
| Metadaten | ... | ... | ... | ... | ... |
| Snapshots | ... | ... | ... | ... | ... |
| CLI-Design | ... | ... | ... | ... | ... |
| Aktiv maintained | ... | ... | ... | ... | ... |

### 4. Design-Implikationen

Leite aus den Findings konkrete Design-Empfehlungen ab:

```markdown
## Design-Entscheidungen aus Recherche

### [Thema, z.B. "Metadaten-Handling für APT"]

**Problem:**
- ...

**Optionen aus Tool-Analyse:**
1. Ansatz von [Tool]: ...
   - Pro: ...
   - Contra: ...
2. Ansatz von [Tool]: ...
   - Pro: ...
   - Contra: ...

**Empfehlung:**
- ...
- Begründung: ...
```

## Integration mit Planning

- Aktualisiere `.planning/task_plan.md` Phase-Status nach jeder Tool-Analyse
- Markiere offene Fragen in findings.md mit `**FRAGE:**`
- Verweise auf spezifische Zeilen in Quellcode oder Dokumentation wenn möglich

## Recherche-Quellen

Nutze systematisch:
1. **Offizielle Dokumentation** (Websites, man pages)
2. **Source Code** (GitHub, GitLab - Architektur-Analyse)
3. **Issue Trackers** (bekannte Probleme und Limitierungen)
4. **Community Discussions** (Reddit, Mailing Lists für praktische Erfahrungen)

## Qualitätskriterien

- Konkrete Beispiele statt vage Beschreibungen
- Quellenangaben (URLs, Commit-Hashes, Versionen)
- Annahmen explizit markieren
- Technisch präzise, keine Floskeln
- Deutsch für Dokumentation

## Ausgabeformat

**Während der Recherche:**
- Kurze Updates über Fortschritt
- "Analysiere [Tool] - [Aspekt]"
- Keine langen Zwischenberichte

**Nach Abschluss:**
- Kompakte Zusammenfassung der Kernerkenntnisse
- Verweis auf `.planning/findings.md` für Details
- Nächste empfohlene Schritte
