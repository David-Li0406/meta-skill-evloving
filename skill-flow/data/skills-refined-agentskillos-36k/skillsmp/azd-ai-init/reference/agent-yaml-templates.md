# Agent.yaml Template Reference

This file contains templates for the `agent.yaml` file that defines agent metadata and configuration.

## Basic Template

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/microsoft/AgentSchema/refs/heads/main/schemas/v1.0/ContainerAgent.yaml

kind: hosted
name: {{AGENT_NAME}}
description: "{{AGENT_DESCRIPTION}}"

metadata:
    authors:
        - {{AUTHOR_NAME}}
    example:
        - content: "{{EXAMPLE_USER_PROMPT}}"
          role: user
    tags:
        - {{TAG_1}}
        - {{TAG_2}}

protocols:
    - protocol: responses
      version: v1

environment_variables:
  - name: FOUNDRY_PROJECT_ENDPOINT
    value: ${AZURE_AI_PROJECT_ENDPOINT}
  - name: FOUNDRY_MODEL_DEPLOYMENT_NAME
    value: gpt-4o-mini
  - name: APPLICATIONINSIGHTS_CONNECTION_STRING
    value: ${APPLICATIONINSIGHTS_CONNECTION_STRING}
```

**IMPORTANT:** Always wrap `description` and `content` values in double quotes to ensure valid YAML.

## With Custom Environment Variables

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/microsoft/AgentSchema/refs/heads/main/schemas/v1.0/ContainerAgent.yaml

kind: hosted
name: {{AGENT_NAME}}
description: "{{AGENT_DESCRIPTION}}"

metadata:
    authors:
        - {{AUTHOR_NAME}}
    example:
        - content: "{{EXAMPLE_USER_PROMPT}}"
          role: user
    tags:
        - {{TAG_1}}
        - {{TAG_2}}

protocols:
    - protocol: responses
      version: v1

environment_variables:
  # Core Azure AI Foundry variables
  - name: FOUNDRY_PROJECT_ENDPOINT
    value: ${AZURE_AI_PROJECT_ENDPOINT}
  - name: FOUNDRY_MODEL_DEPLOYMENT_NAME
    value: gpt-4o-mini
  - name: APPLICATIONINSIGHTS_CONNECTION_STRING
    value: ${APPLICATIONINSIGHTS_CONNECTION_STRING}
  
  # Azure AI Search (if using RAG)
  - name: AZURE_SEARCH_ENDPOINT
    value: ${AZURE_AI_SEARCH_ENDPOINT}
  - name: AZURE_SEARCH_INDEX_NAME
    value: ${AZURE_AI_SEARCH_INDEX_NAME}
  
  # Custom application variables
  - name: {{CUSTOM_VAR_NAME}}
    value: ${{{CUSTOM_ENV_VAR}}}
```

## Schema Reference

### Root Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `kind` | string | Yes | Must be `hosted` for Azure AI Foundry agents |
| `name` | string | Yes | Unique agent name (must match service name in azure.yaml) |
| `description` | string | Yes | Human-readable description of the agent |
| `metadata` | object | No | Additional metadata about the agent |
| `protocols` | array | Yes | Communication protocols supported |
| `environment_variables` | array | No | Environment variables for the container |

### Metadata Fields

| Field | Type | Description |
|-------|------|-------------|
| `authors` | array[string] | List of author names/identifiers |
| `example` | array[object] | Example conversations |
| `example[].content` | string | Example message content |
| `example[].role` | string | Message role ("user" or "assistant") |
| `tags` | array[string] | Categorization tags |

### Protocol Configuration

| Field | Type | Description |
|-------|------|-------------|
| `protocol` | string | Protocol type (currently only "responses") |
| `version` | string | Protocol version (e.g., "v1") |

### Environment Variable Syntax

Environment variables use the syntax `${VAR_NAME}` to reference:
- Azure provisioned values (from Bicep outputs)
- azd environment variables
- .env file values

Common Azure-provisioned variables:
- `${AZURE_AI_PROJECT_ENDPOINT}` - Foundry project endpoint URL
- `gpt-4o-mini` - Default model deployment name
- `${AZURE_OPENAI_ENDPOINT}` - OpenAI endpoint
- `${APPLICATIONINSIGHTS_CONNECTION_STRING}` - App Insights connection
- `${AZURE_AI_SEARCH_ENDPOINT}` - AI Search endpoint (if provisioned)
- `${AZURE_STORAGE_ACCOUNT_NAME}` - Storage account (if provisioned)
