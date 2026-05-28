---
name: dify-plugin
description: Build Dify plugins (Tool, Trigger, Extension, Model, Datasource, Agent Strategy). Use when integrating external APIs, adding webhooks, implementing model providers, connecting data sources, or creating custom agent reasoning strategies. Supports Python SDK with YAML configurations.
---

# Dify Plugin Development

## Key Reference Repositories

Sync with `./scripts/sync_repos.sh` (default: `~/playground/dify-repo/`):

| Repository | Purpose |
|------------|---------|
| **dify-official-plugins** | Official plugin examples - study real implementations |
| **dify-plugin-daemon** | Plugin runtime & CLI - understand how plugins are executed |
| **dify** | Dify core - understand plugin invocation and workflow integration |

## Quick Decision: Which Plugin Type?

```
User wants to...
├─ "Add capability to workflow/agent" ───────► Tool (API calls, logic, file processing)
├─ "Start workflow when webhook received" ───► Trigger
├─ "Expose HTTP endpoint (OAuth, webhook)" ──► Extension
├─ "Add new LLM/Embedding/TTS provider" ─────► Model
├─ "Import docs from cloud storage" ─────────► Datasource
└─ "Custom agent loop (ReAct, CoT)" ─────────► Agent Strategy
```

## Plugin Types

| Type | Purpose | Reference | Example in official-plugins |
|------|---------|-----------|----------------------------|
| **Tool** | Add capabilities: API calls, logic operations, file processing | [tool-plugin.md](references/tool-plugin.md) | `tools/wikipedia`, `tools/github` |
| **Trigger** | Start workflows from webhooks | [trigger-plugin.md](references/trigger-plugin.md) | `triggers/github_trigger` |
| **Extension** | Custom HTTP endpoints | [extension-plugin.md](references/extension-plugin.md) | `extensions/slack_bot` |
| **Model** | Add AI model providers | [model-plugin.md](references/model-plugin.md) | `models/openai`, `models/anthropic` |
| **Datasource** | Connect external storage | [datasource-plugin.md](references/datasource-plugin.md) | `datasources/github` |
| **Agent Strategy** | Custom agent reasoning | [agent-strategy-plugin.md](references/agent-strategy-plugin.md) | `agent-strategies/cot_agent` |

## Development Workflow

### Phase 1: Understand Requirements
1. Determine plugin type using decision tree above
2. If integrating external API, read their API documentation first
3. Find similar plugin in `dify-official-plugins` as reference

### Phase 2: Initialize Project
```bash
# Create plugin scaffold
dify plugin init
# Follow prompts: choose category, set name, configure permissions

# Setup Python environment
cd my-plugin
uv init --no-readme
uv add dify_plugin
```

### Phase 3: Implement
1. Read the corresponding type reference (e.g., [tool-plugin.md](references/tool-plugin.md))
2. Edit `manifest.yaml` - see [MANIFEST_REFERENCE.md](references/MANIFEST_REFERENCE.md) for field rules
3. Create `provider/*.yaml` - credentials schema
4. Implement `provider/*.py` - credential validation
5. Create tool/event definitions and implementations

### Phase 4: Test & Debug

**Important**: Before debugging, Claude should automatically fetch the debug key using saved credentials. If credentials don't exist, prompt the user once and save to `.credential`.

```bash
# Get debug key (auto-loads from .credential, or prompts first time)
python scripts/get_debug_key.py

# Output directly to plugin's .env file
python scripts/get_debug_key.py --output-env > .env

# Run plugin in debug mode (auto-kills previous process)
./scripts/debug.sh

# Or use directly (won't auto-kill previous process)
uv run python -m main
```

**Credential workflow:**
- First time: Script prompts for Dify host, email, password → saves to `.credential`
- Subsequent runs: Automatically uses saved credentials
- `.credential` is gitignored (contains sensitive login info)

See [debugging.md](references/debugging.md) for detailed debugging guide.

### Phase 5: Package & Deploy
```bash
dify plugin package ./my-plugin
```

## When Stuck: Where to Look

| Problem | Solution |
|---------|----------|
| manifest.yaml validation error | [MANIFEST_REFERENCE.md](references/MANIFEST_REFERENCE.md) |
| How to structure YAML files | Type reference + `dify-official-plugins` examples |
| Python interface/method signature | `dify-plugin-daemon` source code |
| Runtime behavior, hooks | [PLUGIN_ARCHITECTURE.md](references/PLUGIN_ARCHITECTURE.md) |
| Error handling patterns | [best-practices.md](references/best-practices.md) |
| Working examples | [plugins_reference.md](references/plugins_reference.md) |

### Troubleshooting with Reference Repositories

When documentation is insufficient, sync the reference repos (see [preparation.md](references/preparation.md#reference-repositories-optional)):

```bash
./scripts/sync_repos.sh
```

**When to consult each repository:**

| Repository | When to Use |
|------------|-------------|
| **dify-plugin-daemon** | Plugin runtime issues, understanding how plugins are loaded/executed, SDK interface definitions, debugging connection problems |
| **dify** | Understanding how Dify invokes plugins, how plugins integrate with workflows, node execution context, API request/response flow |
| **dify-official-plugins** | Implementation patterns, YAML structure examples, real-world credential handling |

## Core Structure

```
my-plugin/
├── manifest.yaml          # Plugin metadata (see MANIFEST_REFERENCE.md)
├── main.py               # Entry: plugin = Plugin(DifyPluginEnv())
├── pyproject.toml        # Dependencies (uv)
├── provider/
│   ├── provider.yaml     # Credentials + config
│   └── provider.py       # Validation logic
├── tools/                # Tool plugins
│   ├── tool.yaml
│   └── tool.py
└── _assets/
    └── icon.svg
```

**Important**: For complete manifest.yaml field rules, validation constraints, and examples, see [MANIFEST_REFERENCE.md](references/MANIFEST_REFERENCE.md).

## Valid Tags

Only 19 tags accepted: `search`, `image`, `videos`, `weather`, `finance`, `design`, `travel`, `social`, `news`, `medical`, `productivity`, `education`, `business`, `entertainment`, `utilities`, `agent`, `rag`, `trigger`, `other`

## Best Practices

See [best-practices.md](references/best-practices.md) for detailed guidelines including execution status mechanics.

## References

### Core References
- [MANIFEST_REFERENCE.md](references/MANIFEST_REFERENCE.md) - **Complete manifest.yaml reference** (field rules, validation, examples)
- [PLUGIN_ARCHITECTURE.md](references/PLUGIN_ARCHITECTURE.md) - **Plugin architecture deep dive** (lifecycle, hooks, runtime, directory structures)

### Plugin Type References
- [tool-plugin.md](references/tool-plugin.md) - Tool plugin details
- [trigger-plugin.md](references/trigger-plugin.md) - Trigger plugin details
- [model-plugin.md](references/model-plugin.md) - Model plugin details
- [extension-plugin.md](references/extension-plugin.md) - Extension plugin details
- [datasource-plugin.md](references/datasource-plugin.md) - Datasource plugin details
- [agent-strategy-plugin.md](references/agent-strategy-plugin.md) - Agent Strategy plugin details

### Additional References
- [best-practices.md](references/best-practices.md) - **Development best practices** (error handling, execution status, common pitfalls)
- [yaml-schemas.md](references/yaml-schemas.md) - Common YAML patterns
- [plugins_reference.md](references/plugins_reference.md) - Official plugin examples
- [debugging.md](references/debugging.md) - Debugging techniques
