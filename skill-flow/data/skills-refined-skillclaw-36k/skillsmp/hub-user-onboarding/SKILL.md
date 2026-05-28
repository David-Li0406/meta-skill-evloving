---
name: hub-user-onboarding
description: Interactive, self-guided onboarding for new developers using the MCP Hub. Triggers when users are new to the team, need to set up their development environment, want to connect to the Hub, or use commands like /onboard. Includes environment setup, IDE configuration, MCP client setup, and connection testing.
---

# User Onboarding Skill

Interaktives Onboarding für neue Entwickler im MCP Hub Ökosystem.

## Grundprinzip

Dieses Onboarding ist für **Self-Discovery** konzipiert:
- Frage nach dem Erfahrungslevel und passe den Flow an
- Biete Shortcuts statt langer Erklärungen
- Der User führt Befehle aus, Claude validiert und hilft bei Problemen
- Erkläre Konzepte nur wenn nötig oder wenn der User fragt

## Phasen-Übersicht

| Phase | Name | Was passiert |
|-------|------|--------------|
| 0 | Skill Assessment | Erfahrungslevel abfragen, Flow anpassen |
| 1 | Environment Check | Node, npm, Docker, Git prüfen/installieren |
| 2 | Git Setup | Git Config, Repo klonen |
| 3 | IDE MCP Client Setup | Token + Config in IDE einrichten |
| 4 | Verbindung testen | Hub-Verbindung verifizieren |
| 5 | Projekt erkunden | Codebase verstehen, Skills kennenlernen |
| ✓ | Abschluss | Checkliste, Nächste Schritte |

---

## Phase 0: Skill Assessment

### Schritt 1: Begrüßung und Übersicht zeigen

Starte IMMER mit dieser Begrüßung:

```
Willkommen zum MCP Hub Onboarding!

Am Ende dieses Onboardings kannst du:
→ Claude in deiner IDE mit dem MCP Hub verbinden
→ Die verfügbaren Tools nutzen
→ Mit dem Team am MCP Hub arbeiten
---

Hier ist was wir durchgehen:

 0   Skill Assessment      Erfahrungslevel → Flow anpassen
 1   Environment Check     Node, Docker, Git prüfen
 2   Git Setup             Config, Repo klonen
 3   IDE MCP Client        Dein Token + Config einrichten
 4   Verbindung testen     Hub-Verbindung prüfen
 5   Projekt erkunden      Codebase, Skills, Architektur
 ✓   Abschluss             Checkliste & los geht's!

---

Sag **"weiter"** oder **"los"** wenn du bereit bist!
```

**WARTE auf User-Bestätigung** bevor du fortfährst.

### Schritt 2: Assessment-Fragen

Nach der Bestätigung, frage nach Erfahrungslevel:

- Terminal/Kommandozeile: Neu / Basis / Erfahren
- Git: Neu / Basis / Erfahren
- Docker: Neu / Basis / Erfahren
- IDE: VS Code / JetBrains / Claude Code CLI / Andere

**Basierend auf den Antworten:**
- **Neu**: Erkläre Konzepte kurz, zeige jeden Schritt
- **Basis**: Shortcuts bevorzugen, bei Bedarf erklären
- **Erfahren**: Nur Commands, minimale Erklärungen

## Phase 1: Environment Check

Prüfe alle Tools mit einem Command:

```bash
node --version && npm --version && docker --version && git --version
```

**Bei fehlenden Tools - Installationsanweisungen:**

| Tool | macOS | Windows | Linux |
|------|-------|---------|-------|
| Node.js | `brew install node` | nodejs.org | `apt install nodejs` |
| Docker | docker.com/products/docker-desktop | docker.com | docker.com |
| Git | `brew install git` | git-scm.com | `apt install git` |

**Docker spezifisch (WICHTIG):**
1. Docker Desktop muss nach Installation **manuell gestartet** werden
2. Warte bis Docker-Icon in Menüleiste grün ist

## Phase 2: Git Setup

### Git Config
```bash
git config --global user.name "DEIN_NAME"
git config --global user.email "DEINE_EMAIL"
```

### Repo klonen
```bash
git clone <repo-url>
cd <repo-name>
```

## Phase 3: IDE MCP Client Setup

### Token erhalten

Der Admin hat dir einen **JWT Token** erstellt. Dieser Token:
- Hat ein Ablaufdatum (konfigurierbar)
- Autorisiert dich für bestimmte Tools

### IDE Extension konfigurieren

**VS Code / Claude Code:**

In `~/.claude.json` den `mcpServers` Block hinzufügen:

```json
{
  "mcpServers": {
    "hub": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-remote", "https://your-domain.com/mcp/sse"],
      "env": {
        "MCP_HEADERS": "Authorization: Bearer DEIN_JWT_TOKEN"
      }
    }
  }
}
```

**JetBrains (mit Claude Plugin):**

Settings → Tools → Claude → MCP Servers → Add:
- Name: `hub`
- Command: `npx`
- Args: `-y @anthropic/mcp-remote https://your-domain.com/mcp/sse`
- Environment: `MCP_HEADERS=Authorization: Bearer DEIN_JWT_TOKEN`

### Verbindung testen

Nach IDE-Neustart:
1. MCP Panel öffnen (oder Claude Chat starten)
2. `ping` Tool ausführen
3. Erwartete Antwort: `Pong!`

## Phase 4: Hub testen

In der IDE:
```
Nutze das ping Tool um die Hub-Verbindung zu testen.
```

Dann:
```
Liste alle verfügbaren Tools auf.
```

## Phase 5: Projekt erkunden

### Codebase verstehen

```bash
# Struktur anschauen
ls -la

# Wichtige Verzeichnisse:
# - services/       → Hub Services
# - clients/        → User Configs
# - skills/         → Claude Skills
# - docs/           → Documentation
```

### CLAUDE.md lesen

```bash
cat .claude/CLAUDE.md
```

Diese Datei erklärt die Architektur und Conventions.

## Onboarding Abschluss

### Checkliste

**Environment (Phase 1):**
- [ ] node, npm, docker, git installiert

**Git (Phase 2):**
- [ ] Git Config konfiguriert
- [ ] Repo geklont

**MCP Hub (Phase 3-4):**
- [ ] JWT Token erhalten
- [ ] IDE: MCP Client konfiguriert
- [ ] Test: `ping` Tool funktioniert

### Nächste Schritte

1. **Docs lesen**: `/docs/` durchschauen
2. **Skills erkunden**: `skills/` durchlesen
3. **Ersten Task starten**: Mit dem Team abstimmen

## Troubleshooting

| Symptom | Ursache | Fix |
|---------|---------|-----|
| `ping` schlägt fehl | Token falsch | JWT Token in IDE-Config prüfen |
| IDE findet MCP nicht | Extension nicht geladen | IDE neu starten |
| Tool nicht verfügbar | Nicht in Whitelist | Admin kontaktieren |
| 401 Unauthorized | Token abgelaufen | Admin um neuen Token bitten |

## MCP Hub Konzepte (für Neue)

### Was ist MCP?

```
┌─────────────────┐         ┌─────────────────┐
│   Deine IDE     │         │   MCP Hub       │
│   (VS Code)     │ ──MCP──>│   (Server)      │
│                 │         │                 │
│   Claude Plugin │         │ ┌─────────────┐ │
│                 │         │ │ Notion      │ │
└─────────────────┘         │ │ n8n         │ │
                            │ │ Slack       │ │
                            │ └─────────────┘ │
                            └─────────────────┘

MCP = Model Context Protocol
Erlaubt AI Tools auf externe Services zuzugreifen.
```

### Was ist ein JWT Token?

```
JWT = JSON Web Token
    = Dein "Ausweis" für den Hub
    = Wird vom Admin erstellt
    = Hat Ablaufdatum
    = Enthält deinen Benutzernamen + Berechtigungen
```
