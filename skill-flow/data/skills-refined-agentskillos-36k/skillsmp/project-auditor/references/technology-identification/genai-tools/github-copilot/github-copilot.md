# GitHub Copilot

**Category**: genai-tools
**Description**: AI-powered code completion and generation tool
**Homepage**: https://github.com/features/copilot

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*GitHub Copilot related packages*

- `@github/copilot-language-server` - Copilot language server
- `@github/copilot-cli` - Copilot CLI

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate GitHub Copilot usage*

- `.github/copilot.yml` - Copilot configuration
- `.copilotignore` - Files to ignore for Copilot
- `.vscode/settings.json` - VS Code settings with Copilot config

### Code Patterns

**Pattern**: `github\.copilot\.|"github.copilot`
- VS Code Copilot settings
- Example: `"github.copilot.enable": true`

**Pattern**: `copilot\.enable|copilot\.advanced`
- Copilot configuration keys
- Example: `copilot.enable.* = true`

**Pattern**: `GITHUB_COPILOT_|GH_COPILOT_`
- Copilot environment variables
- Example: `GITHUB_COPILOT_TOKEN`

**Pattern**: `copilot-proxy|copilot-internal`
- Copilot proxy/internal URLs
- Example: `copilot-proxy.githubusercontent.com`

### IDE Extension Patterns

**Pattern**: `"GitHub.copilot"|"github.copilot"`
- VS Code extension ID
- Example: `extensions.recommendations: ["GitHub.copilot"]`

**Pattern**: `copilot\.vim|copilot-vim`
- Vim/Neovim plugin
- Example: `Plug 'github/copilot.vim'`

**Pattern**: `com\.github\.copilot`
- JetBrains plugin ID

---

## Environment Variables

- `GITHUB_COPILOT_TOKEN` - Copilot authentication token
- `GH_COPILOT_TOKEN` - Alternative token variable
- `COPILOT_AGENT_VERBOSE` - Enable verbose logging

## Detection Notes

- Primarily detected via IDE configuration
- .copilotignore similar to .gitignore syntax
- Copilot Chat is a separate feature
- Enterprise version has additional configuration

---

## Secrets Detection

### Tokens

#### GitHub Copilot Token
**Pattern**: `(?:copilot|COPILOT).*(?:token|TOKEN)\s*[=:]\s*['"]?([a-zA-Z0-9_-]{30,})['"]?`
**Severity**: high
**Description**: GitHub Copilot authentication token
**Example**: `GITHUB_COPILOT_TOKEN=abc123...`

---

## TIER 3: Configuration Extraction

### Enabled Languages Extraction

**Pattern**: `"github\.copilot\.enable"\s*:\s*\{([^}]+)\}`
- Copilot enabled languages from VS Code settings
- Extracts: `language_config`
- Example: `"github.copilot.enable": {"*": true, "markdown": false}`
