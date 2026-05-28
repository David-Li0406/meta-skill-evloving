# azd-ai-init Skill

A Claude/Copilot skill that helps developers structure their AI agent code for deployment to Azure AI Foundry using the Azure Developer CLI (`azd ai`).

## The Problem This Solves

Deploying AI agents to Azure AI Foundry requires a specific project structure with multiple configuration files:

- **`azure.yaml`** - Project configuration with service definitions, model deployments, and scaling settings
- **`agent.yaml`** - Agent metadata, environment variables, and protocol definitions
- **`Dockerfile`** - Container configuration for the hosted agent
- **`infra/`** - Bicep templates for provisioning Azure resources (AI Services, Container Registry, etc.)

Getting this structure right is tedious and error-prone:
- The Bicep infrastructure is complex (~300+ lines across multiple files)
- Environment variables must be correctly mapped between files
- YAML formatting issues cause silent deployment failures
- The `azd ai` extension expects specific resource types (`Microsoft.CognitiveServices/accounts/projects`)

**This skill automates the entire scaffolding process**, letting you go from agent code to deployed Azure service with minimal friction.

## What This Skill Does

When you invoke this skill, Claude/Copilot will:

1. **Analyze your existing code** (if any) to understand your agent's structure
2. **Generate all required files** with correct configuration
3. **Copy working Bicep infrastructure** from the official template
4. **Validate YAML syntax** to prevent deployment failures
5. **Provide deployment instructions** for `azd up`

### Supported Scenarios

| Scenario | What the Skill Does |
|----------|---------------------|
| **Greenfield** (no code) | Scaffolds a complete working agent with sample tools |
| **Existing Python agent** | Wraps your code in the Azure AI Agent Framework pattern |
| **LangGraph/LangChain** | Adapts graph/chain logic to hosted agent format |
| **Semantic Kernel** | Converts plugins to tool functions |
| **AutoGen** | Restructures multi-agent patterns for Foundry |

## Quick Start

### 1. Install the Skill

**VS Code / GitHub Copilot:**
```
Place in .github/skills/azd-ai-init/ in your repository
```

**Claude Code:**
```bash
/skill add /path/to/skill-azd-ai-init
```

### 2. Invoke the Skill

Say any of these to Claude/Copilot:

**Scaffold/Create:**
- `"azd ai init"`
- `"scaffold agent"`
- `"create Foundry agent"`
- `"new azd ai project"`

**Convert/Migrate:**
- `"convert to azd ai"`
- `"convert my agent for Foundry"`
- `"migrate to azd ai"`
- `"migrate to Azure AI Foundry"`

**Update/Upgrade:**
- `"update for azd ai"`
- `"upgrade to azd ai"`
- `"update my agent for Foundry"`
- `"upgrade agent structure"`

**Fix/Troubleshoot:**
- `"fix azd ai deployment"`
- `"fix my Foundry agent"`
- `"troubleshoot azd deploy"`
- `"fix agent.yaml"`

### 3. Example Prompts

```
"Create a new agent for azd ai that can search the web and summarize results"

"I have a Python file with some tool functions - prepare it for Azure AI Foundry"

"Scaffold an azd ai project for my existing LangGraph workflow"

"What's the correct structure for deploying an agent with azd up?"
```

## Generated Project Structure

```
my-agent/
├── azure.yaml                 # Service config, model deployments, scaling
├── infra/                     # Azure infrastructure (Bicep)
│   ├── main.bicep
│   ├── main.parameters.json
│   ├── abbreviations.json
│   └── core/
│       └── ai/
│           └── ai-project.bicep
└── src/
    └── MyAgent/
        ├── agent.yaml         # Agent metadata & env vars
        ├── Dockerfile         # Container build
        ├── main.py            # Agent entry point
        └── requirements.txt   # Python dependencies
```

## Deployment Workflow

After scaffolding, deploy with three commands:

```bash
# Login to Azure
azd auth login

# Provision infrastructure + deploy agent
azd up
```

Or step-by-step:
```bash
azd provision    # Create Azure resources (~2 min)
azd deploy       # Deploy agent container (~2 min)
```

## Prerequisites

- [Azure Developer CLI (azd)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd) v1.21.3+
- Azure subscription with permissions to create resources
- The azd ai extension: `azd extension install azure.ai.agents`

## Key Features

### ✅ Correct Infrastructure
Uses the official `azd-ai-starter-basic` Bicep templates that create proper `Microsoft.CognitiveServices` resources (not ML workspaces).

### ✅ YAML Validation
Ensures all generated YAML files have proper quoting to prevent parsing errors.

### ✅ Environment Variable Mapping
Correctly maps Azure-provisioned values to agent runtime variables.

### ✅ Model Configuration
Sets up model deployments (GPT-4o, GPT-4o-mini) with appropriate SKUs and capacity.

### ✅ Container Configuration
Generates Dockerfiles with correct port exposure and startup commands.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `AZURE_AI_PROJECT_ID` error | Infrastructure must use CognitiveServices, not ML workspaces |
| Container probe failures | Check that agent listens on port 8088 |
| YAML parsing errors | Ensure strings with special characters are quoted |
| Model not found | Verify deployment name in `agent.yaml` matches `azure.yaml` |

## References

- [Azure Developer CLI Documentation](https://learn.microsoft.com/azure/developer/azure-developer-cli/)
- [azd ai agent extension source](https://github.com/Azure/azure-dev/tree/main/cli/azd/extensions/azure.ai.agents)
- [Azure AI Foundry Portal](https://ai.azure.com)
- [Official starter template](https://github.com/Azure-Samples/azd-ai-starter-basic)
- [Agent Framework samples](https://github.com/azure-ai-foundry/foundry-samples)

## License

Apache 2.0 - See [LICENSE](LICENSE) file.
