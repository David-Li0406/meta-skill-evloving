---
name: autonomous-longtask
permissionMode: bypassPermissions
description: Guide für lange, autonome Entwicklungsaufgaben mit Claude Code. Optimierte Patterns für Multi-Session-Tasks, Sub-Agents, Parallelisierung und Loop-Closing.
---

# Autonomous Long-Task Development

Dieses Skill optimiert Claude Code für lange, autonome Entwicklungsaufgaben - von mehrstündigen Feature-Implementierungen bis zu Multi-Session-Refactorings.

## Wann diesen Skill nutzen

- **Komplexe Features**: Implementierungen die mehrere Dateien/Services betreffen
- **Multi-Step Workflows**: Tasks mit 5+ abhängigen Schritten
- **Long-Running Tasks**: Aufgaben die >30 Min dauern
- **Multi-Session Tasks**: Arbeit die über Context-Grenzen hinausgeht

---

## Core Principles

### 1. Loop Closing (Test-Driven)

**Jede Code-Änderung muss einen Feedback-Loop schließen:**

```
1. Test schreiben (was soll passieren)
2. Code implementieren
3. Test ausführen → Loop geschlossen
4. Refactor falls nötig
5. Test erneut → Sicherheit
```

**Anti-Pattern (Open Loop):**
```
"Implementiere Feature X"
→ Code geschrieben, keine Verifikation
→ Bugs später entdeckt
```

**Best Practice (Closed Loop):**
```
"Implementiere Feature X mit E2E Test.
Führe den Test nach Implementation aus."
→ Sofortige Verifikation
```

### 2. Incremental Progress mit Checkpoints

**Niemals alles auf einmal:**

```
❌ Versuchen das komplette Feature zu "one-shotten"
   → Context läuft aus mitten in der Implementierung
   → Nächste Session erbt Chaos

✓ Kleine, getestete Inkremente
   → Jedes Inkrement funktioniert standalone
   → Klare Übergabe zwischen Sessions
```

**Checkpoint-Pattern:**
- Committe nach jedem funktionierenden Inkrement
- Dokumentiere State in `STATUS.md` oder `claude-progress.txt`

### 3. Context-Window Management

**Claude Opus 4 kann 200K Tokens, aber:**

- Sub-Agents haben eigene Context Windows (isoliert)
- Lange Sessions fragmentieren den Context
- `claude-progress.txt` für Session-Handoffs nutzen

---

## Sub-Agents für Parallelisierung

### Verfügbare Agent-Typen

| Agent | Zweck | Tools |
|-------|-------|-------|
| `general-purpose` | Komplexe Multi-Step Tasks | Alle |
| `Explore` | Codebase-Exploration, Pattern-Search | Glob, Grep, Read, Bash |
| `Plan` | Implementation Planning | Glob, Grep, Read |

### Wann Sub-Agents nutzen

**DO:**
- Unbekannte Codebase-Teile erkunden
- Patterns über viele Dateien suchen
- Unabhängige Tasks parallelisieren (max 10 parallel)

**DON'T:**
- Spezifische bekannte Datei lesen → Read direkt
- In 2-3 Dateien suchen → Read direkt
- Klassen-Definition finden → Glob direkt

### Parallel Workflow Pattern

```
"Implementiere Stripe Integration parallel:

Sub-Agent 1 (Backend): API Endpoint erstellen
Sub-Agent 2 (Frontend): Payment Form Component
Sub-Agent 3 (Tests): Integration Tests schreiben

Starte alle drei parallel mit Task tool.
Warte auf Completion, dann integrieren."
```

---

## Multi-Session Task Patterns

### Session Handoff mit claude-progress.txt

**Am Ende jeder Session:**

```markdown
## Session 2025-12-06 14:30

### Completed
- UserService refactored to dependency injection
- All controller endpoints updated
- Unit tests passing (23/23)

### Current State
- Branch: refactor/user-service
- Last commit: abc123
- Tests: ✓ Passing

### Blockers
- None

### Next Session
1. Frontend updates for new API structure
2. Integration tests
3. Documentation
```

---

## Template Prompts

### Long-Running Feature Implementation

```
"Implementiere [FEATURE] mit vollständiger Loop-Closing.

Requirements:
- [Req 1]
- [Req 2]

Approach (track mit TodoWrite):
1. [Step 1] → Test schreiben + implementieren
2. [Step 2] → Test schreiben + implementieren
...

Constraints:
- Jedes Inkrement muss testbar sein
- Committe nach jedem funktionierenden Schritt
- Dokumentiere in STATUS.md falls komplex

Token-Budget: Nutze volle 200K, stoppe NICHT früh.
Bei Context-Grenze: STATUS.md für Handoff updaten.
Parallelisiere unabhängige Tasks mit Sub-Agents."
```

### Multi-Session Refactoring

```
"Refactoring Part [N] von [TOTAL].

Previous Sessions:
- Siehe claude-progress.txt
- Git log für bisherige Änderungen

This Session Goals:
- [Goal 1]
- [Goal 2]

Am Ende dieser Session:
- claude-progress.txt updaten
- Alle Tests müssen grün sein
- Klare Next Steps dokumentieren

Falls Context knapp wird:
- Sauber abschließen (keine halben Implementierungen)
- Handoff-Dokument schreiben
- Nächste Session kann nahtlos weitermachen"
```

---

## Autonomy Levels

### High Autonomy (Default für Long Tasks)

```
"Implementiere Feature X.
Triff alle Implementierungsentscheidungen selbst basierend auf Best Practices.
Stoppe NICHT wegen Token-Budget.
Erstelle Tests und Docs während du arbeitest."
```

### Guided Autonomy (Bei kritischen Entscheidungen)

```
"Implementiere Feature X.
Frage mich VOR Entscheidungen zu:
- Datenbankschema-Änderungen
- Externe API Auswahl
- Breaking Changes

Bei allem anderen: Mach selbstständig weiter."
```

---

## Common Failure Modes

| Problem | Lösung |
|---------|--------|
| Claude stoppt zu früh | "Stoppe NICHT wegen Token-Budget" explizit sagen |
| Zu viele Rückfragen | Mehr Kontext upfront, Autonomy Level setzen |
| Code-Style passt nicht | "Folge Pattern in [FILE]" referenzieren |
| Task zu komplex | In Inkremente brechen, TodoWrite nutzen |
| Context läuft aus | claude-progress.txt + saubere Commits |
| One-shotting fails | Explizit inkrementelles Vorgehen fordern |

---

## Testing Strategy für Long Tasks

### Test Pyramid

```
          /\
         /E2E\ ← Playwright (kritische Flows)
        /-----\
       / API   \ ← Integration Tests
      /---------\
     /   Unit    \ ← Schnellstes Feedback
    /--------------\
```

---

## Quick Reference

```
START:
1. TodoWrite mit Task-Breakdown erstellen
2. Autonomy Level definieren
3. Loop-Closing Pattern etablieren

WÄHREND:
- Jedes Inkrement testen
- Nach funktionierenden Steps committen
- Sub-Agents für parallele Arbeit

ENDE / HANDOFF:
- claude-progress.txt updaten
- Tests grün
- Klare Next Steps
```
