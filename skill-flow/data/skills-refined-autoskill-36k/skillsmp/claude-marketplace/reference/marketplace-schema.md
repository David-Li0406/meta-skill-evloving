# Marketplace Schema Reference

Complete technical reference for marketplace.json schema, fields, and validation rules.

## Complete JSON Schema

### Annotated Example

```json
{
  "name": "enterprise-marketplace",
  "owner": {
    "name": "Enterprise DevTools Team",
    "email": "devtools@enterprise.com",
    "url": "https://github.com/enterprise"
  },
  "metadata": {
    "description": "Enterprise development tools and workflows",
    "version": "3.2.0",
    "pluginRoot": "./packages/plugins"
  },
  "plugins": [
    {
      "name": "security-scanner",
      "source": "./security/scanner",
      "description": "Automated security vulnerability scanning",
      "version": "2.1.0",
      "author": {
        "name": "Security Team",
        "email": "security@enterprise.com"
      },
      "homepage": "https://docs.enterprise.com/plugins/security-scanner",
      "repository": "https://github.com/enterprise/security-scanner",
      "license": "MIT",
      "keywords": ["security", "scanner", "vulnerability"],
      "category": "security",
      "tags": ["audit", "compliance"],
      "commands": [
        "./commands/scan.md",
        "./commands/report.md"
      ],
      "agents": [
        "./agents/security-reviewer.md"
      ],
      "skills": "./skills/",
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [
              {
                "type": "command",
                "command": "${CLAUDE_PLUGIN_ROOT}/scripts/security-check.sh"
              }
            ]
          }
        ]
      },
      "mcpServers": {
        "security-db": {
          "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
          "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
        }
      },
      "strict": true
    },
    {
      "name": "deployment-tools",
      "source": {
        "source": "github",
        "repo": "enterprise/deploy-plugin"
      },
      "description": "Deployment automation and monitoring",
      "version": "1.5.0"
    },
    {
      "name": "external-formatter",
      "source": {
        "source": "url",
        "url": "https://gitlab.enterprise.com/tools/formatter.git"
      },
      "description": "Code formatting standards",
      "strict": false
    }
  ]
}
```

### Type Definitions

```typescript
interface Marketplace {
  name: string;                    // Required: marketplace identifier
  owner: Owner;                    // Required: maintainer information
  metadata?: MarketplaceMetadata;  // Optional: marketplace metadata
  plugins: PluginEntry[];          // Required: array of plugin entries
}

interface Owner {
  name: string;                    // Required: owner name
  email?: string;                  // Optional: contact email
  url?: string;                    // Optional: owner website/profile
}

interface MarketplaceMetadata {
  description?: string;            // Optional: marketplace description
  version?: string;                // Optional: marketplace version
  pluginRoot?: string;             // Optional: base path for relative sources
}

interface PluginEntry {
  // Required fields
  name: string;                    // Plugin identifier
  source: string | SourceObject;   // Plugin source location

  // Optional metadata
  description?: string;
  version?: string;
  author?: Author;
  homepage?: string;
  repository?: string;
  license?: string;
  keywords?: string[];
  category?: string;
  tags?: string[];

  // Component configuration
  commands?: string | string[];
  agents?: string | string[];
  skills?: string;
  hooks?: string | HooksConfig;
  mcpServers?: string | McpConfig;

  // Marketplace-specific
  strict?: boolean;                // Default: true
}

interface SourceObject {
  source: "github" | "url";
  repo?: string;                   // For GitHub sources
  url?: string;                    // For Git URL sources
}
```

## Required Fields

### Marketplace: name

**Type:** `string`

**Description:** Unique identifier for the marketplace. Used when installing plugins or referencing the marketplace.

**Rules:**
- Must be kebab-case (lowercase with hyphens)
- No spaces allowed
- Should be descriptive and unique
- Used in CLI commands: `/plugin install plugin-name@marketplace-name`

**Examples:**

```json
✅ Good
"name": "company-tools"
"name": "devops-automation"
"name": "enterprise-security"

❌ Bad
"name": "Company Tools"           // Spaces not allowed
"name": "companyTools"            // Not kebab-case
"name": "tools"                   // Too generic
```

### Marketplace: owner

**Type:** `object`

**Description:** Information about the marketplace maintainer.

**Required subfields:**
- `name` (string): Maintainer name or team name

**Optional subfields:**
- `email` (string): Contact email
- `url` (string): Website, GitHub profile, or documentation URL

**Examples:**

```json
✅ Minimal
{
  "owner": {
    "name": "DevTools Team"
  }
}

✅ Complete
{
  "owner": {
    "name": "Enterprise Development Team",
    "email": "devtools@enterprise.com",
    "url": "https://github.com/enterprise"
  }
}
```

### Marketplace: plugins

**Type:** `array`

**Description:** Array of plugin entries available in this marketplace.

**Rules:**
- Must be an array (can be empty)
- Each entry must be a valid PluginEntry object
- Each plugin must have unique `name` within marketplace

**Examples:**

```json
✅ Valid
{
  "plugins": []
}

{
  "plugins": [
    {
      "name": "plugin-one",
      "source": "./plugins/one"
    },
    {
      "name": "plugin-two",
      "source": {
        "source": "github",
        "repo": "org/plugin-two"
      }
    }
  ]
}
```

## Optional Metadata Fields

### metadata.description

**Type:** `string`

**Description:** Brief description of the marketplace purpose and contents.

**Use cases:**
- Explain marketplace focus (e.g., "Security tools", "Frontend development")
- Describe target audience
- Provide context for plugin discovery

**Example:**

```json
{
  "metadata": {
    "description": "Enterprise development tools for secure, compliant software delivery"
  }
}
```

### metadata.version

**Type:** `string`

**Description:** Semantic version of the marketplace catalog.

**Use cases:**
- Track marketplace changes over time
- Coordinate updates across teams
- Document breaking changes in marketplace structure

**Recommended format:** Semantic versioning (MAJOR.MINOR.PATCH)

**Example:**

```json
{
  "metadata": {
    "version": "3.0.0"
  }
}
```

### metadata.pluginRoot

**Type:** `string`

**Description:** Base path for resolving relative plugin sources. Prepended to all relative `source` paths.

**Rules:**
- Must be relative path starting with `./`
- Applied only to string-type sources (not SourceObject)
- Useful for monorepo structures

**Example:**

```json
{
  "metadata": {
    "pluginRoot": "./packages/plugins"
  },
  "plugins": [
    {
      "name": "tool-a",
      "source": "./tool-a"
    },
    {
      "name": "tool-b",
      "source": "./tool-b"
    }
  ]
}
```

**Result:**
- `tool-a` resolves to `./packages/plugins/tool-a`
- `tool-b` resolves to `./packages/plugins/tool-b`

## Plugin Entry Schema

### Required: name

**Type:** `string`

**Description:** Unique plugin identifier within the marketplace.

**Rules:**
- Must be kebab-case (lowercase with hyphens)
- No spaces allowed
- Must be unique within marketplace
- Used for installation: `/plugin install plugin-name@marketplace-name`

**Examples:**

```json
✅ Good
"name": "code-formatter"
"name": "security-scanner"
"name": "deployment-tools"

❌ Bad
"name": "Code Formatter"          // Spaces not allowed
"name": "codeFormatter"           // Not kebab-case
```

### Required: source

**Type:** `string | object`

**Description:** Location where the plugin can be fetched.

**String format (relative path):**

```json
{
  "name": "local-plugin",
  "source": "./plugins/my-plugin"
}
```

**Object format (GitHub):**

```json
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo"
  }
}
```

**Object format (Git URL):**

```json
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git"
  }
}
```

### Optional: Standard Metadata

**description** (string): Brief plugin description shown in plugin lists

```json
{
  "description": "Automatic code formatting with team standards"
}
```

**version** (string): Plugin version (semantic versioning recommended)

```json
{
  "version": "2.1.0"
}
```

**author** (object): Plugin author information

```json
{
  "author": {
    "name": "DevTools Team",
    "email": "devtools@company.com",
    "url": "https://github.com/devtools"
  }
}
```

**homepage** (string): Plugin documentation or homepage URL

```json
{
  "homepage": "https://docs.company.com/plugins/formatter"
}
```

**repository** (string): Source code repository URL

```json
{
  "repository": "https://github.com/company/formatter-plugin"
}
```

**license** (string): SPDX license identifier

```json
{
  "license": "MIT"
}
```

Common licenses: `MIT`, `Apache-2.0`, `GPL-3.0`, `BSD-3-Clause`, `ISC`

**keywords** (array of strings): Tags for plugin discovery

```json
{
  "keywords": ["formatting", "code-style", "linting"]
}
```

**category** (string): Plugin category for organization

```json
{
  "category": "development"
}
```

Common categories: `development`, `productivity`, `security`, `deployment`, `testing`, `documentation`

**tags** (array of strings): Additional searchability tags

```json
{
  "tags": ["automation", "ci-cd", "devops"]
}
```

### Optional: Component Configuration

Override default component locations. Custom paths supplement (not replace) default directories.

**commands** (string | array): Custom command file or directory paths

```json
{
  "commands": "./custom/commands/deploy.md"
}

{
  "commands": [
    "./commands/core/",
    "./commands/experimental/preview.md"
  ]
}
```

**agents** (string | array): Custom agent file paths

```json
{
  "agents": "./custom/agents/"
}

{
  "agents": [
    "./agents/security-reviewer.md",
    "./agents/compliance-checker.md"
  ]
}
```

**skills** (string): Custom skills directory path

```json
{
  "skills": "./custom-skills/"
}
```

**hooks** (string | object): Hook configuration path or inline config

```json
{
  "hooks": "./config/hooks.json"
}

{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
          }
        ]
      }
    ]
  }
}
```

**mcpServers** (string | object): MCP server config path or inline config

```json
{
  "mcpServers": "./mcp-config.json"
}

{
  "mcpServers": {
    "plugin-db": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    }
  }
}
```

### Optional: strict

**Type:** `boolean`

**Default:** `true`

**Description:** Controls whether plugin.json manifest is required in plugin directory.

**`strict: true` (default):**
- Plugin must include `.claude-plugin/plugin.json`
- Marketplace fields supplement plugin.json values
- Plugin.json takes precedence for conflicting fields
- Recommended for production plugins

**`strict: false`:**
- Plugin.json is optional
- If missing, marketplace entry serves as complete manifest
- Useful for simple plugins, rapid prototyping, or inline-only configurations

**Examples:**

```json
✅ Production plugin (strict: true)
{
  "name": "enterprise-tools",
  "source": {
    "source": "github",
    "repo": "company/enterprise-plugin"
  },
  "description": "Enterprise workflow tools",
  "strict": true
}

✅ Simple plugin (strict: false)
{
  "name": "quick-command",
  "source": "./plugins/quick",
  "description": "Simple utility command",
  "commands": "./quick.md",
  "strict": false
}
```

## Source Type Specifications

### Relative Paths

**Format:** String starting with `./`

**Behavior:**
- Resolved relative to marketplace repository root
- If `metadata.pluginRoot` is set, prepended to source path
- Plugin directory must contain plugin files at resolved path

**Examples:**

```json
{
  "name": "local-plugin",
  "source": "./plugins/my-plugin"
}

{
  "name": "nested-plugin",
  "source": "./packages/tools/formatter"
}
```

**With pluginRoot:**

```json
{
  "metadata": {
    "pluginRoot": "./packages"
  },
  "plugins": [
    {
      "name": "tool",
      "source": "./tool"
    }
  ]
}
```

Resolves to: `./packages/tool`

### GitHub Repositories

**Format:** Object with `source: "github"` and `repo` field

**Fields:**
- `source` (required): Must be `"github"`
- `repo` (required): Format `"owner/repository"`

**Behavior:**
- Fetches plugin from GitHub repository
- Uses default branch (typically `main` or `master`)
- Repository must be public or user must have access

**Examples:**

```json
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "anthropics/claude-plugin-example"
  }
}

{
  "name": "org-plugin",
  "source": {
    "source": "github",
    "repo": "company/internal-tools"
  }
}
```

**Private repositories:**
- User must have GitHub authentication configured
- Repository access must be granted to user's GitHub account

### Git URLs

**Format:** Object with `source: "url"` and `url` field

**Fields:**
- `source` (required): Must be `"url"`
- `url` (required): Full Git repository URL

**Supported protocols:**
- HTTPS: `https://gitlab.com/team/plugin.git`
- SSH: `git@gitlab.com:team/plugin.git`
- Other Git hosting services (GitLab, Bitbucket, self-hosted)

**Examples:**

```json
{
  "name": "gitlab-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/company/plugins.git"
  }
}

{
  "name": "private-repo",
  "source": {
    "source": "url",
    "url": "git@github.enterprise.com:team/plugin.git"
  }
}

{
  "name": "bitbucket-plugin",
  "source": {
    "source": "url",
    "url": "https://bitbucket.org/team/plugin.git"
  }
}
```

**Authentication:**
- HTTPS URLs may require credentials
- SSH URLs use SSH key authentication
- Private repositories require appropriate access configuration

### Local Paths (Development)

**Format:** Relative path string for local development

**Use cases:**
- Testing plugins before distribution
- Monorepo development
- Local plugin collections

**Example directory structure:**

```
my-marketplace/
├── .claude-plugin/
│   └── marketplace.json
└── plugins/
    ├── formatter/
    ├── linter/
    └── deployer/
```

**marketplace.json:**

```json
{
  "name": "local-dev",
  "owner": {...},
  "plugins": [
    {
      "name": "formatter",
      "source": "./plugins/formatter"
    },
    {
      "name": "linter",
      "source": "./plugins/linter"
    },
    {
      "name": "deployer",
      "source": "./plugins/deployer"
    }
  ]
}
```

### Direct Marketplace URLs

**Format:** String with direct URL to marketplace.json file

**Use cases:**
- Hosting marketplace.json on CDN
- Dynamic marketplace generation
- Serverless marketplace hosting

**Example:**

```json
{
  "name": "remote-marketplace",
  "source": "https://cdn.company.com/marketplaces/tools.json"
}
```

**Requirements:**
- URL must return valid marketplace.json content
- Must be accessible via HTTPS
- Content-Type should be application/json

## Validation Rules

### Schema Validation

Run `claude plugin validate .` to check:

1. **JSON syntax:** Valid JSON format
2. **Required fields:** name, owner, plugins present
3. **Field types:** Correct types for all fields
4. **Field constraints:** Valid values (kebab-case names, etc.)
5. **Source formats:** Valid source objects
6. **Path formats:** Relative paths start with `./`

### Common Validation Errors

**Missing required fields:**

```json
❌ Error: Missing owner
{
  "name": "marketplace"
}

✅ Fixed
{
  "name": "marketplace",
  "owner": {
    "name": "Team"
  },
  "plugins": []
}
```

**Invalid name format:**

```json
❌ Error: name contains spaces
{
  "name": "My Marketplace"
}

✅ Fixed
{
  "name": "my-marketplace"
}
```

**Invalid source format:**

```json
❌ Error: Missing repo field
{
  "name": "plugin",
  "source": {
    "source": "github"
  }
}

✅ Fixed
{
  "name": "plugin",
  "source": {
    "source": "github",
    "repo": "owner/repo"
  }
}
```

**Invalid path format:**

```json
❌ Error: Absolute path not allowed
{
  "name": "plugin",
  "source": "/absolute/path"
}

✅ Fixed
{
  "name": "plugin",
  "source": "./relative/path"
}
```

## See Also

- [SKILL.md](../SKILL.md) - Main marketplace management guide
- [plugin-management.md](plugin-management.md) - Plugin entry patterns
- [team-distribution.md](team-distribution.md) - Team distribution setup
- [troubleshooting.md](troubleshooting.md) - Debugging and error resolution
