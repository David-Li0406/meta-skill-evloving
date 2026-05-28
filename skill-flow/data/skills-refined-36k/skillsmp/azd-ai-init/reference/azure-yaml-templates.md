# Azure.yaml Template Reference

This file contains the template for the `azure.yaml` project configuration file required by `azd ai`.

## Minimal Template

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/Azure/azure-dev/main/schemas/v1.0/azure.yaml.json

requiredVersions:
    extensions:
        azure.ai.agents: '>=0.1.0-preview'

name: {{PROJECT_NAME}}

services:
    {{AGENT_NAME}}:
        project: src/{{AGENT_NAME}}
        host: azure.ai.agent
        language: docker
        docker:
            remoteBuild: true
        config:
            container:
                resources:
                    cpu: "1"
                    memory: 2Gi
                scale:
                    maxReplicas: 3
                    minReplicas: 1
            deployments:
                - model:
                    format: OpenAI
                    name: gpt-4o-mini
                    version: "2024-07-18"
                  name: gpt-4o-mini
                  sku:
                    capacity: 10
                    name: GlobalStandard

infra:
    provider: bicep
    path: ./infra
```

## With Multiple Models

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/Azure/azure-dev/main/schemas/v1.0/azure.yaml.json

requiredVersions:
    extensions:
        azure.ai.agents: '>=0.1.0-preview'

name: {{PROJECT_NAME}}

services:
    {{AGENT_NAME}}:
        project: src/{{AGENT_NAME}}
        host: azure.ai.agent
        language: docker
        docker:
            remoteBuild: true
        config:
            container:
                resources:
                    cpu: "2"
                    memory: 4Gi
                scale:
                    maxReplicas: 5
                    minReplicas: 1
            deployments:
                - model:
                    format: OpenAI
                    name: gpt-4o
                    version: "2024-08-06"
                  name: gpt-4o
                  sku:
                    capacity: 20
                    name: GlobalStandard
                - model:
                    format: OpenAI
                    name: gpt-4o-mini
                    version: "2024-07-18"
                  name: gpt-4o-mini
                  sku:
                    capacity: 50
                    name: GlobalStandard

infra:
    provider: bicep
    path: ./infra
```

## With Azure Resources/Connections

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/Azure/azure-dev/main/schemas/v1.0/azure.yaml.json

requiredVersions:
    extensions:
        azure.ai.agents: '>=0.1.0-preview'

name: {{PROJECT_NAME}}

services:
    {{AGENT_NAME}}:
        project: src/{{AGENT_NAME}}
        host: azure.ai.agent
        language: docker
        docker:
            remoteBuild: true
        config:
            container:
                resources:
                    cpu: "1"
                    memory: 2Gi
                scale:
                    maxReplicas: 3
                    minReplicas: 1
            deployments:
                - model:
                    format: OpenAI
                    name: gpt-4o-mini
                    version: "2024-07-18"
                  name: gpt-4o-mini
                  sku:
                    capacity: 10
                    name: GlobalStandard
            resources:
                - resource: search
                  connectionName: ai-search-connection
                - resource: storage
                  connectionName: storage-connection

infra:
    provider: bicep
    path: ./infra
```

## Schema Reference

### Service Configuration

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `project` | string | Yes | Path to agent source directory |
| `host` | string | Yes | Must be `azure.ai.agent` for hosted agents |
| `language` | string | Yes | `docker` for containerized agents |
| `docker.remoteBuild` | boolean | No | Build container in Azure (recommended) |
| `config.container.resources.cpu` | string | No | CPU allocation (e.g., "1", "0.5") |
| `config.container.resources.memory` | string | No | Memory allocation (e.g., "2Gi", "512Mi") |
| `config.container.scale.minReplicas` | integer | No | Minimum instances (default: 1) |
| `config.container.scale.maxReplicas` | integer | No | Maximum instances (default: 3) |
| `config.deployments` | array | Yes | Model deployments |
| `config.resources` | array | No | External Azure resource connections |

### Deployment Configuration

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Deployment name (referenced in code) |
| `model.format` | string | Yes | Provider format (e.g., "OpenAI") |
| `model.name` | string | Yes | Model identifier |
| `model.version` | string | Yes | Model version |
| `sku.name` | string | Yes | SKU tier ("GlobalStandard", "Standard") |
| `sku.capacity` | integer | Yes | TPM in thousands |

### Resource Types

| Resource | Connection Name Pattern | Description |
|----------|------------------------|-------------|
| `search` | `*-search-connection` | Azure AI Search |
| `storage` | `*-storage-connection` | Azure Blob Storage |
| `registry` | `acr-connection` | Azure Container Registry |
| `bing_grounding` | `bing-connection` | Bing Search API |
| `bing_custom_grounding` | `bing-custom-connection` | Bing Custom Search |
