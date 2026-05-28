# Research Workflow - Agent Orchestration for Terraform Implementation

## Overview

This guide describes how to orchestrate parallel research agents to gather comprehensive information from Azure MCP and Terraform MCP before implementing infrastructure code.

## Parallel Agent Pattern

### Why Parallel Agents?

1. **Efficiency**: Azure and Terraform research can run simultaneously
2. **Comprehensive**: Each agent focuses on its domain expertise
3. **Quality**: Synthesis of multiple information sources ensures accuracy
4. **Consistency**: Standardized research process for all implementations

### Agent Execution Rules

**CRITICAL: Always launch agents in parallel, not sequentially**

✅ **Correct - Single message with multiple Task calls:**
```
I'm launching two research agents in parallel:

[Task tool: Azure MCP Research]
[Task tool: Terraform MCP Research]
```

❌ **Incorrect - Sequential execution:**
```
First launching Azure research...
[Wait for completion]
Now launching Terraform research...
```

## Agent 1: Azure Service Research

### Purpose
Query Azure MCP tools to gather service-specific documentation, best practices, and Terraform implementation patterns.

### Task Configuration

```
subagent_type: "general-purpose"
description: "Research Azure {service_name} documentation"
model: "sonnet" (default) or "haiku" (for simple queries)
```

### Prompt Template

```
Research Azure {service_name} using Azure MCP tools:

1. Service Documentation:
   - Use mcp__Azure__documentation('{service_name}')
   - Extract: Service overview, key features, configuration options

2. Terraform Best Practices:
   - Use mcp__Azure__azureterraformbestpractices('{service_name}')
   - Extract: Recommended Terraform patterns, common configurations, examples

3. Well-Architected Framework:
   - Use mcp__Azure__get_bestpractices('{service_name}')
   - Extract: Security requirements, reliability patterns, performance optimization

4. Synthesize findings:
   - Required configurations vs optional
   - Security best practices (network isolation, access control, encryption)
   - Common pitfalls and how to avoid them
   - Recommended naming conventions for Azure resources

Output format:
## Service Overview
[Key features and capabilities]

## Required Configuration
[Must-have settings]

## Security Best Practices
[Security requirements from Well-Architected Framework]

## Terraform Implementation Patterns
[Common patterns and examples]

## Recommendations
[Specific guidance for this service]
```

### Service Name Mapping

Common service names for Azure MCP:

| User Request | Azure MCP Service Name |
|--------------|------------------------|
| "Front Door" | "Front Door" |
| "App Service" | "App Service" |
| "Virtual Network", "VNet" | "Virtual Network" |
| "Storage Account" | "Storage Account" |
| "Key Vault" | "Key Vault" |
| "Application Gateway" | "Application Gateway" |
| "Azure SQL" | "SQL Database" |
| "Cosmos DB" | "Cosmos DB" |
| "AKS", "Kubernetes" | "Azure Kubernetes Service" |
| "Container Apps" | "Container Apps" |

## Agent 2: Terraform Provider Research

### Purpose
Query Terraform MCP tools to identify available resources, required arguments, and provider versions.

### Task Configuration

```
subagent_type: "general-purpose"
description: "Research Terraform provider details"
model: "sonnet" (default)
```

### Prompt Template

```
Research Terraform providers for {resource_description} using Terraform MCP tools:

1. azurerm Provider Details:
   - Use mcp__Terraform__get_provider_details('hashicorp', 'azurerm')
   - Search for relevant resource types matching: {resource_description}
   - List available data sources
   - Note provider configuration requirements

2. azapi Provider Details:
   - Use mcp__Terraform__get_provider_details('azure', 'azapi')
   - Check if preview features are available via azapi
   - Document API versions if using azapi

3. Provider Versions:
   - Use mcp__Terraform__get_latest_provider_version('hashicorp', 'azurerm')
   - Use mcp__Terraform__get_latest_provider_version('azure', 'azapi')
   - Document version constraints for terraform.tf

4. Resource Analysis:
   For each identified resource type:
   - List REQUIRED arguments (cannot be omitted)
   - List OPTIONAL arguments (with sensible defaults)
   - Identify nested blocks and their structure
   - Note any meta-arguments (count, for_each, depends_on)

Output format:
## Provider Versions
- azurerm: {version}
- azapi: {version}

## Identified Resources
### Resource: {resource_type}
**Required Arguments:**
- argument_name (type) - description

**Optional Arguments:**
- argument_name (type) - description [default: value]

**Nested Blocks:**
- block_name { ... }

## Available Data Sources
- data_source_name - use case

## Recommendations
- Which resources to use (azurerm vs azapi)
- Suggested argument values
- Common patterns for this resource type
```

### Resource Description Examples

| User Request | Resource Description for Agent |
|--------------|--------------------------------|
| "Create Azure Front Door with WAF" | "Azure Front Door with WAF policy and security configuration" |
| "Setup App Service with private endpoint" | "Azure App Service with private endpoint and VNet integration" |
| "Deploy Virtual Network with subnets" | "Azure Virtual Network with multiple subnets and service endpoints" |
| "Storage account with blob containers" | "Azure Storage Account with private blob containers and network rules" |

## Synthesis Phase

### After Both Agents Complete

Once both agents finish, synthesize their outputs:

1. **Cross-Validate Information**
   - Verify Azure best practices align with Terraform resource capabilities
   - Ensure security requirements can be implemented with available arguments

2. **Identify Gaps**
   - Missing required configurations
   - Preview features requiring azapi
   - Additional resources needed (e.g., resource groups, networking)

3. **Create Implementation Plan**
   - File structure (which .tf files needed)
   - Resource dependencies (creation order)
   - Variable requirements
   - Output values to expose

### Synthesis Template

```markdown
## Implementation Summary

### Azure Requirements (from Azure MCP)
- [Key security/compliance requirements]
- [Network isolation requirements]
- [Required Azure resource dependencies]

### Terraform Resources (from Terraform MCP)
- azurerm resources: [list]
- azapi resources: [list if needed]
- Data sources: [list]

### Implementation Approach
1. [Resource Group creation]
2. [Network resources if needed]
3. [Primary resources]
4. [Supporting resources]

### Variables Needed
- [variable_name] (type) - description

### Outputs to Expose
- [output_name] - what it provides

### Security Considerations
- [Specific security configurations based on Well-Architected Framework]
```

## Example: Front Door with WAF

### User Request
"Create Azure Front Door with WAF policy for my web application"

### Agent 1: Azure Research

```
Task(
  subagent_type="general-purpose",
  description="Research Azure Front Door documentation",
  prompt="""Research Azure Front Door using Azure MCP tools:

1. Use mcp__Azure__documentation('Front Door')
2. Use mcp__Azure__azureterraformbestpractices('Front Door')
3. Use mcp__Azure__get_bestpractices('Front Door')

Focus on:
- WAF configuration requirements
- Security best practices
- Origin configuration patterns
- Custom domain setup
"""
)
```

### Agent 2: Terraform Research

```
Task(
  subagent_type="general-purpose",
  description="Research Terraform Front Door resources",
  prompt="""Research Terraform providers for Azure Front Door with WAF using Terraform MCP tools:

1. Use mcp__Terraform__get_provider_details('hashicorp', 'azurerm')
   - Find: azurerm_cdn_frontdoor_* resources
   - Find: azurerm_cdn_frontdoor_firewall_policy resource

2. Use mcp__Terraform__get_latest_provider_version('hashicorp', 'azurerm')

3. Document for each resource:
   - Required arguments
   - Security-related optional arguments
   - Nested blocks structure

Focus on:
- azurerm_cdn_frontdoor_profile
- azurerm_cdn_frontdoor_endpoint
- azurerm_cdn_frontdoor_origin_group
- azurerm_cdn_frontdoor_origin
- azurerm_cdn_frontdoor_firewall_policy
- azurerm_cdn_frontdoor_security_policy
"""
)
```

### Expected Synthesis

After both agents complete:

```markdown
## Implementation Plan

### Resources Required (from Terraform MCP)
1. azurerm_resource_group
2. azurerm_cdn_frontdoor_profile (sku: Premium for WAF)
3. azurerm_cdn_frontdoor_endpoint
4. azurerm_cdn_frontdoor_origin_group (with health probes)
5. azurerm_cdn_frontdoor_origin (pointing to web app)
6. azurerm_cdn_frontdoor_firewall_policy (WAF rules)
7. azurerm_cdn_frontdoor_security_policy (associate WAF to endpoint)

### Security Requirements (from Azure MCP)
- Use Premium SKU for WAF functionality
- Enable managed rule sets: DefaultRuleSet 2.1 + BotManagerRuleSet 1.0
- Set WAF mode to "Prevention"
- Configure health probes on origins
- Use HTTPS for origin connections

### Variables Needed
- project_name (string)
- environment (string)
- location (string)
- origin_host_name (string)
- waf_mode (string) [default: "Prevention"]

### File Structure
- terraform.tf (provider versions)
- providers.tf (azurerm provider)
- variables.tf (input variables)
- main.tf (resource group)
- frontdoor.tf (Front Door resources)
- outputs.tf (Front Door endpoint URL)
```

## Best Practices

### Agent Prompts

**DO:**
- ✅ Be specific about which MCP tools to use
- ✅ Request structured output format
- ✅ Ask for synthesis and recommendations
- ✅ Focus on security and best practices
- ✅ Request both required and optional configurations

**DON'T:**
- ❌ Ask agents to implement code (research only)
- ❌ Use vague service names
- ❌ Skip synthesis step
- ❌ Forget to request latest versions

### Parallel Execution

**DO:**
- ✅ Launch both agents in single message
- ✅ Use appropriate model (sonnet for complex, haiku for simple)
- ✅ Provide clear task descriptions
- ✅ Wait for both to complete before synthesizing

**DON'T:**
- ❌ Launch agents sequentially
- ❌ Start implementation before research completes
- ❌ Skip one agent to save time
- ❌ Use unclear agent descriptions

### Error Handling

If an agent fails or returns incomplete information:

1. **Azure MCP Issues:**
   - Try alternative service name
   - Check if service is spelled correctly
   - Fall back to general Azure best practices

2. **Terraform MCP Issues:**
   - Verify provider namespace (hashicorp vs azure)
   - Check if resource type exists
   - Search provider registry manually as fallback

3. **Re-launch with Refined Prompts:**
   - Make prompt more specific
   - Focus on subset of information
   - Use different agent type if needed

## Integration with Main Workflow

This research phase is **Step 1** in the Terraform Code workflow:

```
Step 1: Research (THIS DOCUMENT) → Parallel agents gather info
Step 2: Structure Files → Create .tf files based on research
Step 3: Implement Resources → Write code following research findings
Step 4: Validate → Run terraform fmt/validate + style checks
```

Always complete research before moving to implementation.
