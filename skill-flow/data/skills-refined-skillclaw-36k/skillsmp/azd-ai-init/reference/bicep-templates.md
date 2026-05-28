# Bicep Infrastructure Templates

This file contains Bicep templates for provisioning Azure AI Foundry resources.

## infra/main.bicep

```bicep
targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the environment that can be used as part of naming resource convention')
param environmentName string

@minLength(1)
@maxLength(90)
@description('Name of the resource group to use or create')
param resourceGroupName string = 'rg-${environmentName}'

@minLength(1)
@description('Primary location for all resources')
@allowed([
  'australiaeast'
  'brazilsouth'
  'canadacentral'
  'canadaeast'
  'eastus'
  'eastus2'
  'francecentral'
  'germanywestcentral'
  'italynorth'
  'japaneast'
  'koreacentral'
  'northcentralus'
  'norwayeast'
  'polandcentral'
  'southafricanorth'
  'southcentralus'
  'southeastasia'
  'southindia'
  'spaincentral'
  'swedencentral'
  'switzerlandnorth'
  'uaenorth'
  'uksouth'
  'westus'
  'westus2'
  'westus3'
])
param location string

@metadata({azd: {
  type: 'location'
  usageName: [
    'OpenAI.GlobalStandard.gpt-4o-mini,10'
  ]}
})
param aiDeploymentsLocation string

@description('Id of the user or app to assign application roles')
param principalId string

@description('Principal type of user or app')
param principalType string

@description('Optional. Name of an existing AI Services account within the resource group.')
param aiFoundryResourceName string = ''

@description('Optional. Name of the AI Foundry project.')
param aiFoundryProjectName string = 'ai-project-${environmentName}'

@description('List of model deployments')
param aiProjectDeploymentsJson string = '[]'

@description('List of connections')
param aiProjectConnectionsJson string = '[]'

@description('List of resources to create and connect to the AI project')
param aiProjectDependentResourcesJson string = '[]'

var aiProjectDeployments = json(aiProjectDeploymentsJson)
var aiProjectConnections = json(aiProjectConnectionsJson)
var aiProjectDependentResources = json(aiProjectDependentResourcesJson)

@description('Enable hosted agent deployment')
param enableHostedAgents bool

@description('Enable monitoring for the AI project')
param enableMonitoring bool = true

var tags = {
  'azd-env-name': environmentName
}

var hasAcr = contains(map(aiProjectDependentResources, r => r.resource), 'registry')
var dependentResources = (enableHostedAgents) && !hasAcr ? union(aiProjectDependentResources, [
  {
    resource: 'registry'
    connectionName: 'acr-connection'
  }
]) : aiProjectDependentResources

resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: resourceGroupName
  location: location
  tags: tags
}

module aiProject 'core/ai/ai-project.bicep' = {
  scope: rg
  name: 'ai-project'
  params: {
    tags: tags
    location: aiDeploymentsLocation
    aiFoundryProjectName: aiFoundryProjectName
    principalId: principalId
    principalType: principalType
    existingAiAccountName: aiFoundryResourceName
    deployments: aiProjectDeployments
    connections: aiProjectConnections
    additionalDependentResources: dependentResources
    enableMonitoring: enableMonitoring
    enableHostedAgents: enableHostedAgents
  }
}

// Outputs
output AZURE_RESOURCE_GROUP string = resourceGroupName
output AZURE_AI_ACCOUNT_NAME string = aiProject.outputs.aiServicesAccountName
output AZURE_AI_PROJECT_ID string = aiProject.outputs.projectId
output AZURE_AI_PROJECT_NAME string = aiProject.outputs.projectName

output AZURE_AI_PROJECT_ENDPOINT string = aiProject.outputs.AZURE_AI_PROJECT_ENDPOINT
output AZURE_OPENAI_ENDPOINT string = aiProject.outputs.AZURE_OPENAI_ENDPOINT
output APPLICATIONINSIGHTS_CONNECTION_STRING string = aiProject.outputs.APPLICATIONINSIGHTS_CONNECTION_STRING

output AZURE_AI_PROJECT_ACR_CONNECTION_NAME string = aiProject.outputs.dependentResources.registry.connectionName
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = aiProject.outputs.dependentResources.registry.loginServer

output BING_GROUNDING_CONNECTION_NAME string = aiProject.outputs.dependentResources.bing_grounding.connectionName
output BING_GROUNDING_RESOURCE_NAME string = aiProject.outputs.dependentResources.bing_grounding.name
output BING_GROUNDING_CONNECTION_ID string = aiProject.outputs.dependentResources.bing_grounding.connectionId

output BING_CUSTOM_GROUNDING_CONNECTION_NAME string = aiProject.outputs.dependentResources.bing_custom_grounding.connectionName
output BING_CUSTOM_GROUNDING_NAME string = aiProject.outputs.dependentResources.bing_custom_grounding.name
output BING_CUSTOM_GROUNDING_CONNECTION_ID string = aiProject.outputs.dependentResources.bing_custom_grounding.connectionId

output AZURE_AI_SEARCH_CONNECTION_NAME string = aiProject.outputs.dependentResources.search.connectionName
output AZURE_AI_SEARCH_SERVICE_NAME string = aiProject.outputs.dependentResources.search.serviceName

output AZURE_STORAGE_CONNECTION_NAME string = aiProject.outputs.dependentResources.storage.connectionName
output AZURE_STORAGE_ACCOUNT_NAME string = aiProject.outputs.dependentResources.storage.accountName
```

## infra/main.parameters.json

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "environmentName": {
      "value": "${AZURE_ENV_NAME}"
    },
    "location": {
      "value": "${AZURE_LOCATION}"
    },
    "aiDeploymentsLocation": {
      "value": "${AZURE_AI_DEPLOYMENTS_LOCATION}"
    },
    "principalId": {
      "value": "${AZURE_PRINCIPAL_ID}"
    },
    "principalType": {
      "value": "${AZURE_PRINCIPAL_TYPE}"
    },
    "aiProjectDeploymentsJson": {
      "value": "${AI_PROJECT_DEPLOYMENTS}"
    },
    "aiProjectConnectionsJson": {
      "value": "${AI_PROJECT_CONNECTIONS}"
    },
    "aiProjectDependentResourcesJson": {
      "value": "${AI_PROJECT_DEPENDENT_RESOURCES}"
    },
    "enableHostedAgents": {
      "value": "${ENABLE_HOSTED_AGENTS=true}"
    }
  }
}
```

## Simplified main.bicep (Without ai-project module)

If you need a standalone template without the external module:

```bicep
targetScope = 'subscription'

@minLength(1)
@maxLength(64)
param environmentName string

param location string
param principalId string
param principalType string = 'User'

var resourceGroupName = 'rg-${environmentName}'
var aiServicesName = 'ai-${environmentName}'
var aiProjectName = 'ai-project-${environmentName}'
var logAnalyticsName = 'log-${environmentName}'
var appInsightsName = 'appi-${environmentName}'
var acrName = replace('acr${environmentName}', '-', '')

var tags = { 'azd-env-name': environmentName }

resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: resourceGroupName
  location: location
  tags: tags
}

module logAnalytics 'core/monitor/loganalytics.bicep' = {
  scope: rg
  name: 'loganalytics'
  params: {
    name: logAnalyticsName
    location: location
    tags: tags
  }
}

module appInsights 'core/monitor/applicationinsights.bicep' = {
  scope: rg
  name: 'appinsights'
  params: {
    name: appInsightsName
    location: location
    tags: tags
    logAnalyticsWorkspaceId: logAnalytics.outputs.id
  }
}

module containerRegistry 'core/host/container-registry.bicep' = {
  scope: rg
  name: 'container-registry'
  params: {
    name: acrName
    location: location
    tags: tags
  }
}

// Output environment variables for agent
output AZURE_RESOURCE_GROUP string = resourceGroupName
output APPLICATIONINSIGHTS_CONNECTION_STRING string = appInsights.outputs.connectionString
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = containerRegistry.outputs.loginServer
```

## Supported Locations

The following Azure regions support the AI Foundry Responses API:

| Region | Location Code |
|--------|---------------|
| Australia East | `australiaeast` |
| Brazil South | `brazilsouth` |
| Canada Central | `canadacentral` |
| Canada East | `canadaeast` |
| East US | `eastus` |
| East US 2 | `eastus2` |
| France Central | `francecentral` |
| Germany West Central | `germanywestcentral` |
| Italy North | `italynorth` |
| Japan East | `japaneast` |
| Korea Central | `koreacentral` |
| North Central US | `northcentralus` |
| Norway East | `norwayeast` |
| Poland Central | `polandcentral` |
| South Africa North | `southafricanorth` |
| South Central US | `southcentralus` |
| Southeast Asia | `southeastasia` |
| South India | `southindia` |
| Spain Central | `spaincentral` |
| Sweden Central | `swedencentral` |
| Switzerland North | `switzerlandnorth` |
| UAE North | `uaenorth` |
| UK South | `uksouth` |
| West US | `westus` |
| West US 2 | `westus2` |
| West US 3 | `westus3` |

## Key Resource Types

| Resource | Bicep Type | Description |
|----------|------------|-------------|
| AI Services Account | `Microsoft.CognitiveServices/accounts` | Foundry hub/account |
| AI Project | `Microsoft.MachineLearningServices/workspaces` | Foundry project |
| Container Registry | `Microsoft.ContainerRegistry/registries` | For agent containers |
| Log Analytics | `Microsoft.OperationalInsights/workspaces` | Logging |
| Application Insights | `Microsoft.Insights/components` | Monitoring |
| Storage Account | `Microsoft.Storage/storageAccounts` | Data storage |
| AI Search | `Microsoft.Search/searchServices` | Vector search |
