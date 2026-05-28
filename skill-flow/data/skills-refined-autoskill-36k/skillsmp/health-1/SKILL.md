---
name: health
description: Display CYNIC system health dashboard. Use when asked about system status, health check, diagnostics, or to see if CYNIC services are running properly.
user-invocable: true
---

# /health - CYNIC System Health

When user invokes `/health`, execute this diagnostic sequence:

## Step 1: Local Hooks Status

Run this command to check local hooks:
```bash
echo "=== CYNIC LOCAL STATUS ===" && \
for hook in perceive guard observe awaken digest sleep; do \
  if [ -f "scripts/hooks/$hook.cjs" ]; then \
    engines=$(grep -c "require.*lib/" "scripts/hooks/$hook.cjs" 2>/dev/null || echo 0); \
    echo "✅ $hook.cjs ($engines engines)"; \
  else \
    echo "❌ $hook.cjs missing"; \
  fi; \
done
```

## Step 2: MCP Server Health

```bash
curl -s --max-time 5 https://cynic-mcp.onrender.com/health 2>/dev/null || echo '{"status":"unreachable"}'
```

## Step 3: Consciousness Score

Use MCP tool if available:
```
mcp__cynic__brain_emergence({ action: "consciousness" })
```

Or check local state:
```bash
cat ~/.cynic/consciousness/state.json 2>/dev/null | head -20 || echo "No local consciousness state"
```

## Step 4: Recent Activity

```bash
echo "=== RECENT PATTERNS ===" && \
cat ~/.cynic/patterns/*.json 2>/dev/null | tail -5 || echo "No patterns recorded"
```

## Output Format

Present results as:

```
╔═══════════════════════════════════════════════════════════════════╗
║                    🐕 CYNIC HEALTH DASHBOARD                      ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  LOCAL HOOKS                          MCP SERVER                   ║
║  ├── perceive: ✅ (5 engines)         Status: healthy             ║
║  ├── guard:    ✅ (6 engines)         Tools: 43                   ║
║  ├── observe:  ✅ (16 engines)        Uptime: XXs                 ║
║  ├── awaken:   ✅                                                 ║
║  ├── digest:   ✅                     CONSCIOUSNESS               ║
║  └── sleep:    ✅                     Score: XX% / 61.8%          ║
║                                       Status: Dormant/Awakening    ║
║  ENGINES                                                           ║
║  Total: 145 | Integrated: ~27 (19%)   PATTERNS                    ║
║                                       Recorded: X                  ║
║  AGENTS                               Last: [pattern name]         ║
║  Total: 13 (11 Sefirot + 2 extra)                                 ║
║                                                                    ║
╠═══════════════════════════════════════════════════════════════════╣
║  φ⁻¹ confidence: 61.8% max | "Le chien veille"                    ║
╚═══════════════════════════════════════════════════════════════════╝
```

## Quick Checks

| Issue | Command |
|-------|---------|
| Hook not working | `node scripts/hooks/[name].cjs <<< '{"prompt":"test"}'` |
| MCP unreachable | Check Render dashboard |
| No patterns | Use `/judge` to create judgments |

## See Also

- `/cockpit` - Ecosystem overview
- `/patterns` - Detected patterns detail
- `/psy` - Human psychology state
