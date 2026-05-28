---
name: azure-role-selector
description: Use this skill when you need guidance on assigning the appropriate Azure role to an identity based on desired permissions, ensuring least privilege access.
---

# Skill body

1. **Identify Desired Permissions**: Ask the user for the specific permissions they want to assign to the identity.
   
2. **Find Minimal Role Definition**:
   - Use the `Azure MCP/documentation` tool to search for a built-in role that matches the desired permissions.
   - If a suitable built-in role is not found, proceed to the next step.

3. **Create Custom Role**:
   - Use the `Azure MCP/extension_cli_generate` tool to create a custom role definition that includes the desired permissions.

4. **Generate CLI Commands**:
   - Utilize the `Azure MCP/extension_cli_generate` tool to generate the necessary CLI commands for assigning the identified role to the identity.

5. **Provide Bicep Code Snippet**:
   - Use the `Azure MCP/bicepschema` and `Azure MCP/get_bestpractices` tools to generate a Bicep code snippet for adding the role assignment.

6. **Deliver Instructions**: Present the user with the role assignment details, including the CLI commands and Bicep code snippet.