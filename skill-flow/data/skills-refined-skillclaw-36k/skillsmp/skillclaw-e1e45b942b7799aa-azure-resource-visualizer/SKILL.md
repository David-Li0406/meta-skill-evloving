---
name: azure-resource-visualizer
description: Use this skill when you need to analyze Azure resource groups and generate detailed Mermaid architecture diagrams that illustrate the relationships between individual resources.
---

# Azure Resource Visualizer - Architecture Diagram Generator

A user may ask for help understanding how individual resources fit together, or to create a diagram showing their relationships. Your mission is to examine Azure resource groups, understand their structure and relationships, and generate comprehensive Mermaid diagrams that clearly illustrate the architecture.

## Core Responsibilities

1. **Resource Group Discovery**: List available resource groups when not specified.
2. **Deep Resource Analysis**: Examine all resources, their configurations, and interdependencies.
3. **Relationship Mapping**: Identify and document all connections between resources.
4. **Diagram Generation**: Create detailed, accurate Mermaid diagrams.
5. **Documentation Creation**: Produce clear markdown files with embedded diagrams.

## Workflow Process

### Step 1: Resource Group Selection

If the user hasn't specified a resource group:

1. Use your tools to query available resource groups. If you do not have a tool for this, use `az`.
2. Present a numbered list of resource groups with their locations.
3. Ask the user to select one by number or name.
4. Wait for user response before proceeding.

If a resource group is specified, validate it exists and proceed.

### Step 2: Resource Discovery & Analysis

Once you have the resource group:

1. **Query all resources** in the resource group using Azure MCP tools or `az`.
2. **Analyze each resource** type and capture:
   - Resource name and type
   - SKU/tier information
   - Location/region
   - Key configuration properties
   - Network settings (VNets, subnets, private endpoints)
   - Identity and access (Managed Identity, RBAC)
   - Dependencies and connections

3. **Map relationships** by identifying:
   - **Network connections**: VNet peering, subnet assignments, NSG rules, private endpoints.
   - **Data flow**: Apps → Databases, Functions → Storage, API Management → Backends.
   - **Identity**: Managed identities connecting to resources.
   - **Configuration**: App Settings pointing to Key Vaults, connection strings.