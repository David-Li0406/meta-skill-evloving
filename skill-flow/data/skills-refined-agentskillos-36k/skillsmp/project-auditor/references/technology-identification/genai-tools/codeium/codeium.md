# Codeium

**Category**: genai-tools
**Description**: Free AI-powered code completion and chat
**Homepage**: https://codeium.com

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

No specific npm packages - Codeium is an IDE extension.

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Codeium usage*

- `.codeiumrc` - Codeium configuration
- `.codeiumignore` - Files to ignore

### Code Patterns

**Pattern**: `codeium\.com|CODEIUM_`
- Codeium URLs and environment
- Example: `CODEIUM_API_KEY`

**Pattern**: `"Codeium\.codeium"|codeium\.enabled`
- VS Code extension settings
- Example: `"Codeium.codeium.enable": true`

### IDE Extension Patterns

**Pattern**: `"Codeium\.codeium"`
- VS Code extension ID
- Example: `extensions.recommendations: ["Codeium.codeium"]`

**Pattern**: `codeium\.vim|codeium-vim`
- Vim plugin
- Example: `Plug 'Exafunction/codeium.vim'`

**Pattern**: `com\.codeium`
- JetBrains plugin ID

---

## Environment Variables

- `CODEIUM_API_KEY` - Codeium API key
- `CODEIUM_TOKEN` - Authentication token

## Detection Notes

- Free alternative to GitHub Copilot
- Supports VS Code, JetBrains, Vim/Neovim
- Enterprise version for teams
- Chat and autocomplete features

---

## Secrets Detection

### API Keys

#### Codeium API Key
**Pattern**: `(?:codeium|CODEIUM).*(?:api[_-]?key|API[_-]?KEY|token|TOKEN)\s*[=:]\s*['"]?([a-zA-Z0-9_-]{30,})['"]?`
**Severity**: high
**Description**: Codeium API key or token
**Example**: `CODEIUM_API_KEY=abc123...`
