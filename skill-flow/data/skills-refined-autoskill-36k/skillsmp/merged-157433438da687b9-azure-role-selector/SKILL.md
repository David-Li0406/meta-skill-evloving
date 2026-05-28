---
name: azure-role-selector
description: Use this skill when you need guidance on assigning the least privilege role to an identity based on desired permissions.
---

To assign a role to an identity with the least privilege access, follow these steps:

1. Use the `Azure MCP/documentation` tool to find the minimal role definition that matches the desired permissions.
2. If no built-in role matches the desired permissions, use the `Azure MCP/extension_cli_generate` tool to create a custom role definition with the specified permissions.
3. Generate the CLI commands needed to assign that role to the identity using the `Azure MCP/extension_cli_generate` tool.
4. Provide a Bicep code snippet for adding the role assignment using the `Azure MCP/bicepschema` and `Azure MCP/get_bestpractices` tools.

Ensure that the role assignment adheres to the principle of least privilege.