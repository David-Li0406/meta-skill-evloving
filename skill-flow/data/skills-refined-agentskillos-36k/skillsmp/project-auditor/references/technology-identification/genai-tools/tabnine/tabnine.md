# Tabnine

**Category**: genai-tools
**Description**: AI code completion tool
**Homepage**: https://tabnine.com

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

No specific npm packages - Tabnine is an IDE extension.

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Tabnine usage*

- `.tabnine` - Tabnine configuration
- `tabnine.toml` - Tabnine TOML configuration

### Code Patterns

**Pattern**: `tabnine\.com|TABNINE_`
- Tabnine URLs and environment
- Example: `TABNINE_API_KEY`

**Pattern**: `"TabNine\.tabnine"|tabnine\.enabled`
- VS Code extension settings
- Example: `"TabNine.tabnine.enable": true`

### IDE Extension Patterns

**Pattern**: `"TabNine\.tabnine-vscode"`
- VS Code extension ID
- Example: `extensions.recommendations: ["TabNine.tabnine-vscode"]`

**Pattern**: `tabnine-vim|tabnine-nvim`
- Vim/Neovim plugin
- Example: `Plug 'codota/tabnine-nvim'`

**Pattern**: `com\.tabnine`
- JetBrains plugin ID

---

## Environment Variables

- `TABNINE_API_KEY` - Tabnine API key
- `TABNINE_TOKEN` - Authentication token

## Detection Notes

- One of the first AI code completion tools
- Supports local and cloud models
- Team and Enterprise versions
- Supports most popular IDEs

---

## Secrets Detection

### API Keys

#### Tabnine API Key
**Pattern**: `(?:tabnine|TABNINE).*(?:api[_-]?key|API[_-]?KEY|token|TOKEN)\s*[=:]\s*['"]?([a-zA-Z0-9_-]{30,})['"]?`
**Severity**: high
**Description**: Tabnine API key or token
**Example**: `TABNINE_API_KEY=abc123...`
