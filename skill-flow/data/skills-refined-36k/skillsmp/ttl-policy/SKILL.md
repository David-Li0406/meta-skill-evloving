---
name: ttl-policy
description: Manage Time-To-Live policies for framework content freshness
version: 1.0.0
---

# TTL Policy Skill

## Purpose

Manage Time-To-Live (TTL) policies for content consumed from the multi-agent-os framework. Ensures information freshness and triggers review cycles when content expires.

## When to Use

- When consuming content from framework
- When checking document freshness
- When syncing from upstream
- When reviewing stale content

## TTL by Content Type

| Type | TTL (days) | Rationale |
|------|------------|-----------|
| Protocol/Standard | 90 | Core protocols are stable |
| API Documentation | 60 | Interfaces change moderately |
| Configuration | 30 | Configs need frequent updates |
| Roadmap/Timeline | 14 | Time-sensitive |
| Security Policy | 90 | Security requires stability |
| Decision Record | 180 | Decisions are long-lived |
| Tutorial/Guide | 60 | Examples may need updates |
| Reference Data | 30 | Data freshness matters |

## Status States

```
🟢 FRESH    → now < expires - 7d    → Use normally
🟡 EXPIRING → expires-7d < now < expires → Alert, plan review
🔴 EXPIRED  → now >= expires        → Block usage, require refresh
```

## PROV Tag Format

Add provenance tracking to consumed content:

### Compact (1-line)
```html
<!-- PROV: https://github.com/ekson73/multi-agent-os/blob/main/protocols/hmp.md | v1.0 | sync:2026-01-07 | TTL:90d | exp:2026-04-07 -->
```

### Inline (Markdown-safe)
```markdown
[//]: # (PROV: https://github.com/ekson73/multi-agent-os/blob/main/protocols/hmp.md|v1.0|2026-01-07|TTL90|exp:2026-04-07)
```

### JSON
```json
{
  "_prov": "https://github.com/ekson73/multi-agent-os/blob/main/protocols/hmp.md|v1.0|2026-01-07|TTL90|exp:2026-04-07"
}
```

## PROV Fields

| Field | Format | Example |
|-------|--------|---------|
| `full-url` | GitHub URL | `https://github.com/.../file.md` |
| `version` | Semver | `v1.0` |
| `sync` | ISO date | `sync:2026-01-07` |
| `TTL` | Days | `TTL:90d` |
| `exp` | ISO date | `exp:2026-04-07` |

## Agent Actions by Status

| Status | Agent Action | Human Action |
|--------|--------------|--------------|
| 🟢 FRESH | Use normally | None needed |
| 🟡 EXPIRING | Warn human | Schedule review |
| 🔴 EXPIRED | Block, require refresh | Sync from upstream |

## Sync Protocol

When content is EXPIRED:
1. Check upstream for updates
2. Pull latest version
3. Update sync date
4. Recalculate expiration
5. Update PROV tag

---

*Skill based on TTL Policy v1.0 | multi-agent-os*
