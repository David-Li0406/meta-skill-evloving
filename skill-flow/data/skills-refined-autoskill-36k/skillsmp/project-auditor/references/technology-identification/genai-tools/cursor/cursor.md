# Cursor

**Category**: genai-tools
**Description**: AI-first code editor built on VS Code
**Homepage**: https://cursor.sh

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

No specific npm packages - Cursor is an IDE, not a library.

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Cursor usage*

- `.cursorrules` - Cursor AI instructions file
- `.cursorignore` - Files to ignore for Cursor AI
- `.cursor/` - Cursor configuration directory

### Code Patterns

**Pattern**: `\.cursorrules|\.cursorignore`
- Cursor configuration files
- Example: `.cursorrules`

**Pattern**: `cursor\.sh|CURSOR_`
- Cursor URLs and environment
- Example: `CURSOR_API_KEY`

**Pattern**: `cursor-api|cursor\.so`
- Cursor API references
- Example: `api.cursor.sh`

### Project Structure

**Pattern**: `\.cursor/settings\.json|\.cursor/mcp\.json`
- Cursor settings directory
- Example: `.cursor/settings.json`

---

## Environment Variables

- `CURSOR_API_KEY` - Cursor API key (if applicable)
- `CURSOR_BACKGROUND_KEY` - Background processing key

## Detection Notes

- Cursor is a fork of VS Code with AI features
- .cursorrules provides project-specific AI context
- .cursorignore prevents files from AI analysis
- Uses Claude and GPT models for code generation

---

## Secrets Detection

### API Keys

#### Cursor API Key
**Pattern**: `(?:cursor|CURSOR).*(?:api[_-]?key|API[_-]?KEY)\s*[=:]\s*['"]?([a-zA-Z0-9_-]{30,})['"]?`
**Severity**: high
**Description**: Cursor API key
**Example**: `CURSOR_API_KEY=abc123...`

---

## TIER 3: Configuration Extraction

### Rules File Detection

**Pattern**: `\.cursorrules`
- Cursor rules file presence indicates Cursor usage
- Context: Project root
