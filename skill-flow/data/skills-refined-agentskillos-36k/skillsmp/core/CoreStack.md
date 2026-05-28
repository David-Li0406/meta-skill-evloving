# Core Stack Preferences

Technical preferences for code generation and tooling.

Generated: 2026-01-09

---

## Language Preferences

| Priority | Language | Use Case |
|----------|----------|----------|
| 1 | Go | Backend services, CLI tools, performance-critical code |
| 2 | TypeScript | Frontend, scripting, when JS ecosystem required |
| 3 | Nix | System configuration, package management |

---

## Package Managers

| Language | Manager | Never Use |
|----------|---------|-----------|
| JavaScript/TypeScript | bun | npm, yarn, pnpm |
| Python | uv | pip, pip3 |
| Go | go mod | - |

---

## Runtime

| Purpose | Tool |
|---------|------|
| JavaScript Runtime | Bun |
| Backend Services | Go |
| System Config | NixOS/home-manager |

---

## Markup Preferences

| Format | Use | Never Use |
|--------|-----|-----------|
| Markdown | All content, docs, notes | HTML for basic content |
| YAML | Configuration, frontmatter | - |
| JSON | API responses, data | - |
| Nix | System/package config | - |

---

## Code Style

- Prefer explicit over clever
- No unnecessary abstractions
- Comments only where logic isn't self-evident
- Error messages should be actionable
- NixOS: prefer declarative over imperative when possible
