<!-- TIER: 2 | QUICK REFERENCE -->
<!-- Read after: SKILL.md (entry point) -->
<!-- Purpose: Complete CLI reference for Agentforce agents -->

# CLI Guide

Complete reference for Salesforce CLI commands used with Agentforce agents.

> ⚠️ **Note**: These commands are in beta. Use `--help` to verify current flags.

---

## Command Quick Reference

| Command | Purpose | Stage |
|---------|---------|-------|
| `sf agent validate authoring-bundle` | Validate Agent Script syntax | Authoring |
| `sf agent publish authoring-bundle` | Publish authoring bundle | Authoring |
| `sf agent preview` | Preview agent behavior | Testing |
| `sf agent activate` | Activate published agent | Deployment |
| `sf agent deactivate` | Deactivate agent for changes | Deployment |
| `sf project retrieve start --metadata Agent:Name` | Sync agent from org | Sync |
| `sf project deploy start --metadata Agent:Name` | Deploy agent to org | Sync |

---

## Authoring Commands

### sf agent validate authoring-bundle

Validates Agent Script syntax before publishing.

```bash
sf agent validate authoring-bundle [flags]
```

| Flag | Description | Required |
|------|-------------|----------|
| `-n, --api-name` | API name of authoring bundle | No (prompts if omitted) |
| `-o, --target-org` | Org username or alias | No (uses default) |
| `--api-version` | Override API version | No |

> ⚠️ **No `--source-dir` flag!** The command finds bundles in your DX project automatically.

```bash
# Validate specific bundle
sf agent validate authoring-bundle --api-name Customer_Support_Agent --target-org myorg
```

**Common Errors:**

| Error | Cause | Solution |
|-------|-------|----------|
| `SyntaxError: Unexpected token` | Invalid syntax | Check indentation, colons, quotes |
| `type integer is not supported` | Using `integer` type | Use `number` instead |
| `Unexpected '<'` | Using `list<type>` | Use `list[type]` (square brackets) |

---

### sf agent publish authoring-bundle

Publishes the authoring bundle to create or update the agent.

```bash
sf agent publish authoring-bundle [flags]
```

| Flag | Description | Required |
|------|-------------|----------|
| `-n, --api-name` | API name of authoring bundle | No (prompts if omitted) |
| `-o, --target-org` | Org username or alias | No (uses default) |

> ⚠️ **No `--source-dir`, `--async`, or `--wait` flags!**

```bash
# Publish specific bundle
sf agent publish authoring-bundle --api-name Customer_Support_Agent --target-org myorg
```

**Creates/Updates:**
- `Bot` - Top-level chatbot
- `BotVersion` - Version configuration
- `AiAuthoringBundle` - Agent Script metadata
- `GenAiPlugin` - Topics
- `GenAiFunction` - Actions

---

## Testing Commands

### sf agent preview

Preview agent behavior before production deployment.

```bash
sf agent preview [flags]
```

| Flag | Description | Required |
|------|-------------|----------|
| `--api-name` | Agent API name | No |
| `--target-org` | Org username or alias | No |
| `--use-live-actions` | Enable live mode (real Apex/Flows) | No |
| `--client-app` | Connected app name | For live mode |
| `--output-dir` | Save transcript/response files | No |
| `--apex-debug` | Generate Apex debug logs | No |
| `--authoring-bundle` | Specify authoring bundle | No |

```bash
# Simulated mode (default)
sf agent preview --api-name Customer_Support_Agent --target-org myorg

# Live mode with connected app
sf agent preview --api-name Customer_Support_Agent --use-live-actions --client-app MyAgentApp --target-org myorg

# With debug output
sf agent preview --api-name Customer_Support_Agent --output-dir ./logs --apex-debug --target-org myorg
```

#### Preview Modes

| Mode | Description | Use When |
|------|-------------|----------|
| **Simulated** (default) | LLM simulates action responses | Apex/Flows not ready, testing logic |
| **Live** | Uses actual Apex/Flows | Integration testing with real data |

---

### Connected App Setup (Required for Live Preview)

#### Step 1: Create Connected App

1. **Setup → App Manager → New Connected App**
2. Configure:

| Setting | Value |
|---------|-------|
| Connected App Name | `AgentPreviewApp` |
| Enable OAuth Settings | ✅ Checked |
| Callback URL | `http://localhost:1717/OauthRedirect` |
| OAuth Scopes | `Manage user data via Web browsers (web)` |

3. Save and wait for activation

#### Step 2: Link to CLI User

```bash
sf org login web \
  --client-app AgentPreviewApp \
  --client-id YOUR_CONSUMER_KEY \
  --scopes web
```

#### Step 3: Run Live Preview

```bash
sf agent preview --api-name My_Agent --use-live-actions --client-app AgentPreviewApp --target-org myorg
```

---

### Preview Output Files

When using `--output-dir`:

**transcript.json** - Conversation record:
```json
{
  "messages": [
    {"role": "user", "content": "What is my order status?"},
    {"role": "assistant", "content": "I'd be happy to help..."}
  ]
}
```

**responses.json** - Full API messages with internal details

---

### Preview Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| "No active agents found" | Agent not activated | Run `sf agent activate` first |
| "Connected app not found" | Not linked to CLI user | Run `sf org login web --client-app` |
| "default_agent_user not found" | Invalid user in config | Update config block |
| Preview hangs | Action timeout | Use `--apex-debug`, check limits |
| Actions not executing | Not deployed | Deploy Apex/Flows first |

---

## Deployment Commands

### sf agent activate

Activates a published agent.

```bash
sf agent activate --api-name My_Agent --target-org myorg
```

**Requirements:**
- Agent must be published first
- Apex classes and Flows deployed
- `default_agent_user` must be valid org user

---

### sf agent deactivate

Deactivates an agent (required before making changes).

```bash
sf agent deactivate --api-name My_Agent --target-org myorg
```

**Required before:**
- Adding/removing topics
- Modifying action configurations
- Changing system instructions
- Updating variable definitions

---

## Management Commands

### sf org open (with Agent)

Opens agent in Agentforce Builder.

```bash
sf org open --source-file force-app/main/default/aiAuthoringBundles/My_Agent/My_Agent.agent --target-org myorg

# Or navigate to Agentforce Studio
sf org open --path /lightning/setup/AgentStudio/home --target-org myorg
```

---

## Sync Commands

### Retrieve Agent from Org

```bash
sf project retrieve start --metadata Agent:Customer_Support_Agent --target-org myorg
```

**Retrieves:**
- Bot, BotVersion, GenAiPlannerBundle
- GenAiPlugin (topics), GenAiFunction (actions)
- Supporting Apex/Flows (if in same package)

---

### Deploy Agent to Org

```bash
sf project deploy start --metadata Agent:Customer_Support_Agent --target-org myorg
```

**Does NOT deploy Apex or Flows** - deploy separately first.

---

## Common Workflows

### New Agent Development

```bash
# 1. Validate syntax
sf agent validate authoring-bundle --api-name My_Agent --target-org myorg

# 2. Deploy dependencies FIRST
sf project deploy start --source-dir force-app/main/default/classes --target-org myorg
sf project deploy start --source-dir force-app/main/default/flows --target-org myorg

# 3. Publish agent
sf agent publish authoring-bundle --api-name My_Agent --target-org myorg

# 4. Preview (simulated)
sf agent preview --api-name My_Agent --target-org myorg

# 5. Activate
sf agent activate --api-name My_Agent --target-org myorg

# 6. Preview (live mode)
sf agent preview --api-name My_Agent --use-live-actions --client-app MyApp --target-org myorg
```

---

### Modifying Existing Agent

```bash
# 1. Deactivate
sf agent deactivate --api-name My_Agent --target-org myorg

# 2. Edit Agent Script file

# 3. Validate
sf agent validate authoring-bundle --api-name My_Agent --target-org myorg

# 4. Re-publish
sf agent publish authoring-bundle --api-name My_Agent --target-org myorg

# 5. Test
sf agent preview --api-name My_Agent --target-org myorg

# 6. Re-activate
sf agent activate --api-name My_Agent --target-org myorg
```

---

### Syncing Between Orgs

```bash
# 1. Retrieve from source
sf project retrieve start --metadata Agent:My_Agent --target-org source-org

# 2. Deploy dependencies to target
sf project deploy start --source-dir force-app/main/default/classes --target-org target-org
sf project deploy start --source-dir force-app/main/default/flows --target-org target-org

# 3. Deploy agent metadata
sf project deploy start --metadata Agent:My_Agent --target-org target-org

# 4. Activate
sf agent activate --api-name My_Agent --target-org target-org
```

---

## Agent Metadata Types

| Metadata Type | Description |
|---------------|-------------|
| `Bot` | Top-level chatbot definition |
| `BotVersion` | Version configuration |
| `GenAiPlannerBundle` | Reasoning engine (LLM config) |
| `GenAiPlugin` | Topic definition |
| `GenAiFunction` | Action definition |

```bash
# Retrieve specific metadata types
sf project retrieve start --metadata Bot:Customer_Support_Agent --target-org myorg
sf project retrieve start --metadata GenAiPlugin --target-org myorg
```

---

## Preview Limitations

| Limitation | Details |
|------------|---------|
| Escalation testing | Not supported - test via actual endpoint |
| Connection endpoints | Preview doesn't strictly adhere to config |
| Script changes | Require validation and preview restart |
| Active agent required | Agent must be active for preview |

---

## Related Documentation

- [Agent Script Reference](agent-script-reference.md) - Complete syntax guide
- [Actions Reference](actions-reference.md) - Action configuration
- [Patterns & Practices](patterns-and-practices.md) - Best practices
