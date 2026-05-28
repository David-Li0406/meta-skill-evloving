---
name: oci-vault
description: Manage secrets in Oracle Cloud Infrastructure Vault via MCP. Provides 12 tools for complete secret lifecycle management including listing, searching, creating, updating, and deleting secrets. Compatible with any MCP-compatible client (Claude Desktop, Cursor, Cline, OpenCode, etc.). Use when working with OCI Vault credentials, API keys, or sensitive configuration data.
license: UPL-1.0
metadata:
  author: Oracle
  version: "1.0.0"
  compatibility: MCP-universal
  tags:
    - secrets
    - vault
    - oci
    - key-management
    - mcp-server
    - agent-agnostic
---

# OCI Vault MCP Server

Access and manage Oracle Cloud Infrastructure Vault secrets through the MCP (Model Context Protocol) server. This skill provides 12 tools for complete secret lifecycle management.

## Capabilities

This skill enables you to:

- **List and Search Secrets**: Find secrets by name or list all available secrets in your vault
- **Retrieve Secrets**: Get secret metadata, values, and complete version history
- **Create Secrets**: Store new secrets with proper naming and organization in OCI Vault
- **Update Secrets**: Create new versions of existing secrets and update metadata
- **Delete Secrets**: Schedule secrets for safe deletion (7-30 day retention period)
- **Configure Vault**: Set default vault and compartment IDs for your project
- **Manage Authentication**: Configure OCI CLI credentials and handle authentication
- **Apply Best Practices**: Implement security best practices for secret management

The skill leverages the OCI Vault MCP Server's 12 specialized tools to provide secure, auditable secret management across development, staging, and production environments.

## When to Use This Skill

Use this skill when you need to:

1. **Access secrets in OCI Vault** - Retrieve API keys, passwords, certificates, or other sensitive data
2. **Create new secrets** - Store new credentials, tokens, or sensitive configuration
3. **Manage secret versions** - Update secrets and maintain version history
4. **Configure vault access** - Set up default vault and compartment IDs for your operations
5. **Understand OCI Vault concepts** - Learn about secret lifecycle, versions, and metadata
6. **Debug authentication issues** - Troubleshoot OCI CLI connection problems
7. **Implement secure workflows** - Follow best practices for storing and accessing secrets

## Getting Started

Before your first operation, complete the **Setup Checklist** in `references/setup-checklist.md`:
- Verify OCI CLI authentication works
- Set environment variables (OCI_VAULT_ID, OCI_COMPARTMENT_ID)
- Test connectivity to your vault

For quick reference during operations, see `references/quick-reference.md` with common commands and error solutions.

## Available Tools

### Reading Secrets (No modifications)

- **list_secrets**: List all secrets in a vault
- **search_secrets**: Search for secrets by name (substring matching)
- **get_secret_metadata**: Get detailed metadata about a specific secret
- **list_secret_versions**: View all versions of a secret
- **get_secret_value**: Retrieve secret content for a specific version
- **get_secret**: Get complete secret information (metadata + versions)

### Managing Secrets (Modifications)

- **create_secret**: Create a new secret in the vault
- **update_secret**: Create a new version of an existing secret
- **update_secret_metadata**: Update secret description, tags, and metadata
- **delete_secret**: Schedule a secret for deletion (7-30 days retention period)

### Configuration

- **configure_vault**: Set default vault and compartment IDs
- **get_vault_config_tool**: Check current vault configuration

## Common Use Cases

### List All Secrets

Ask me to list all secrets in your configured vault:
```
List all secrets in the vault
```

I'll use `list_secrets` tool to retrieve and display all available secrets.

### Search for a Specific Secret

Find a secret by name pattern:
```
Search for secrets containing "api" or "database"
```

I'll use `search_secrets` to find matching secrets.

### Get Secret Details

Retrieve complete information about a secret:
```
Get full details for secret-id-12345
```

I'll use `get_secret` to retrieve metadata and version history.

### Create a New Secret

Store a new credential or API key:
```
Create a new secret named "my-api-key" with value "sk-xyz123"
```

I'll use `create_secret` with appropriate content type and metadata.

### Update Secret Version

Create a new version of an existing secret:
```
Update the secret "database-password" with new value "newpass123"
```

I'll use `update_secret` to create a new version while keeping the old one accessible.

### Update Secret Metadata

Add tags or description without creating a new version:
```
Update secret "my-secret" with description "Production API key" and tags environment=prod
```

I'll use `update_secret_metadata` to update descriptive information.

### Delete a Secret

Schedule a secret for deletion:
```
Delete secret-id-12345 with 30-day retention
```

I'll use `delete_secret` with appropriate retention period.

## Configuration Required

Before using this skill effectively, ensure:

1. **OCI CLI Authentication**: Set up `oci session authenticate` or API key authentication
2. **Environment Variables**:
   - `OCI_CONFIG_PROFILE`: Your OCI CLI profile name
   - `OCI_VAULT_ID`: OCID of your vault (e.g., `ocid1.vault.oc1.phx...`)
   - `OCI_COMPARTMENT_ID`: OCID of your compartment

3. **IAM Permissions**: Your OCI user has appropriate permissions:
   - `MANAGE_VAULTS`
   - `READ_SECRETS`
   - `CREATE_SECRETS`
   - `UPDATE_SECRETS`
   - `DELETE_SECRETS`

## Important Concepts

### Secret Versions

OCI Vault maintains all previous versions of a secret. When you update a secret using `update_secret`, the new content becomes the current version while previous versions remain accessible.

### Deletion Retention

When you delete a secret, it's not immediately removed. Instead, it's scheduled for deletion with a retention period of 7-30 days. During this period, you can cancel the deletion.

### Content Types

Secrets support different content types:
- `application/octet-stream` (default)
- `text/plain`
- `application/json`
- `application/pkcs8`

### Compartments and Vaults

- **Compartment**: Logical grouping of OCI resources for organization and access control
- **Vault**: Container for secrets within a compartment
- Multiple vaults can exist in the same compartment

## Best Practices

1. **Use Descriptive Names**: Name secrets clearly to indicate their purpose (e.g., `prod-db-password`, `slack-webhook-token`)

2. **Tag Secrets**: Use tags to organize secrets by environment, team, or application

3. **Version Control**: Keep version history clean. Don't create unnecessary versions.

4. **Access Control**: Use IAM policies to restrict who can access specific secrets

5. **Rotation**: Implement secret rotation policies. Update secrets periodically.

6. **Audit Logging**: Enable audit logging to track who accessed which secrets and when

7. **Least Privilege**: Grant minimum necessary permissions to users and applications

8. **Never Share Credentials**: Don't expose secret values in logs, error messages, or documentation

9. **Use Appropriate Retention**: When deleting secrets, use reasonable retention periods (7-30 days)

10. **Compartmentalization**: Use separate vaults/compartments for different environments (prod, staging, dev)

## Troubleshooting

Encountering issues? Refer to `references/troubleshooting.md` for solutions to:

- Authentication and configuration errors
- Authentication failures and permission issues
- Vault and compartment configuration problems
- Secret operation errors
- Performance issues
- MCP Server connection problems
- Security concerns

Each issue includes the error message, likely cause, and step-by-step solutions.

## Learning More

- Read the [OCI Vault documentation](https://docs.oracle.com/en-us/iaas/Content/KeyManagement/Concepts/keyoverview.htm)
- Explore the [OCI CLI Vault commands](https://docs.oracle.com/en-us/iaas/tools/oci-cli/latest/oci_cli_docs/commandscompute/)
- Review the [FastMCP documentation](https://github.com/jferrettiboke/fastmcp)
- Check the project [README](../../../README.md) for setup instructions

## Examples

### Example 1: Search and Retrieve a Secret

```
Search for my database password and show me all versions
```

I would:
1. Use `search_secrets` to find secrets containing "database" or "password"
2. Use `get_secret` on the matching secret ID
3. Display metadata and version history

### Example 2: Create and Tag a New Secret

```
Create a new secret named "github-token" with value "ghp_abc123xyz" and tag it as production
```

I would:
1. Use `create_secret` to create the secret
2. Use `update_secret_metadata` to add tags
3. Confirm successful creation

### Example 3: Update a Secret

```
Update the secret "api-key" with a new value
```

I would:
1. Retrieve the current secret using `get_secret_metadata`
2. Use `update_secret` to create a new version
3. Confirm the update and show version information

### Example 4: Manage Secret Lifecycle

```
I want to retire the old password secret. Show me how many versions it has and schedule it for deletion.
```

I would:
1. Use `list_secret_versions` to show all versions
2. Use `delete_secret` with appropriate retention period
3. Confirm the deletion schedule

## Related Skills

- **git-release**: For managing versioned releases
- **docker**: For containerized deployments of secret consumers
- **authentication**: For general authentication concepts
