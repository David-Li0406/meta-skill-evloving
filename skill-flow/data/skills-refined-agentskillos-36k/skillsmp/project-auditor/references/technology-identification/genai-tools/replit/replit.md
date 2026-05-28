# Replit

**Category**: genai-tools
**Description**: Cloud-based IDE with AI coding assistant
**Homepage**: https://replit.com

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Replit packages*

- `@replit/database` - Replit Database client
- `@replit/object-storage` - Replit Object Storage
- `@replit/extensions` - Replit Extensions SDK
- `@replit/river` - Replit River RPC

#### PYPI
*Replit Python packages*

- `replit` - Replit Python SDK
- `replit-db` - Replit Database client

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Replit usage*

- `.replit` - Replit configuration
- `replit.nix` - Nix configuration for Replit
- `.replit.toml` - TOML configuration
- `.breakpoints` - Debugger breakpoints

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`

**Pattern**: `from\s+['"]@replit/database['"]`
- Replit Database import
- Example: `import Database from '@replit/database';`

#### Python
Extensions: `.py`

**Pattern**: `^from\s+replit\s+import`
- Replit Python import
- Example: `from replit import db`

**Pattern**: `^import\s+replit`
- Replit Python import
- Example: `import replit`

### Code Patterns

**Pattern**: `replit\.com|repl\.co|repl\.it`
- Replit URLs
- Example: `https://replit.com/@user/project`

**Pattern**: `REPLIT_|REPL_`
- Replit environment variables
- Example: `REPLIT_DB_URL`

**Pattern**: `replit\.db|Database\(\)|db\[`
- Replit Database usage
- Example: `db["key"] = "value"`

---

## Environment Variables

- `REPLIT_DB_URL` - Replit Database URL
- `REPL_ID` - Repl identifier
- `REPL_OWNER` - Repl owner username
- `REPL_SLUG` - Repl slug/name
- `REPLIT_DEPLOYMENT` - Deployment mode flag
- `REPLIT_DEV_DOMAIN` - Development domain
- `REPLIT_CLUSTER` - Cluster identifier

## Detection Notes

- .replit file configures run commands and languages
- replit.nix for Nix package management
- Replit Database is a key-value store
- Ghostwriter is the AI coding assistant
- Deployments have specific environment variables

---

## Secrets Detection

### Tokens

#### Replit Token
**Pattern**: `(?:replit|REPLIT|REPL).*(?:token|TOKEN)\s*[=:]\s*['"]?([a-zA-Z0-9_-]{30,})['"]?`
**Severity**: high
**Description**: Replit API or auth token
**Example**: `REPLIT_TOKEN=abc123...`

#### Replit Database URL
**Pattern**: `REPLIT_DB_URL\s*[=:]\s*['"]?(https://[^\s'"]+)['"]?`
**Severity**: medium
**Description**: Replit Database URL (contains credentials)
**Example**: `REPLIT_DB_URL=https://kv.replit.com/v0/...`

---

## TIER 3: Configuration Extraction

### Run Command Extraction

**Pattern**: `run\s*=\s*['"]([^'"]+)['"]`
- Run command from .replit file
- Extracts: `run_command`
- Example: `run = "python main.py"`

### Language Extraction

**Pattern**: `language\s*=\s*['"]([^'"]+)['"]`
- Language from .replit file
- Extracts: `language`
- Example: `language = "python3"`
