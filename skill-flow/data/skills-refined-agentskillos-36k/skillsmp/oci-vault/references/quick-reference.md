# OCI Vault Quick Reference

Fast reference for common OCI Vault operations with the MCP Server.

## Quick Setup

```bash
# 1. Find your vault and compartment IDs
oci vault vault list --compartment-id=<comp-id>
oci iam compartment list

# 2. Set environment variables
export OCI_CONFIG_PROFILE=default
export OCI_VAULT_ID=ocid1.vault.oc1.phx.xxxxx
export OCI_COMPARTMENT_ID=ocid1.compartment.oc1.xxxxx

# 3. Test connectivity
# Ask agent: List all secrets in my vault
```

## Common Commands

### List Operations

```
List all secrets
→ Use: list_secrets tool

Search for secrets named "api"
→ Use: search_secrets with name pattern

Get full details of secret <id>
→ Use: get_secret to see metadata + versions

Show versions of secret <id>
→ Use: list_secret_versions
```

### Create Operations

```
Create new secret "my-key" with value "xyz"
→ Use: create_secret with name and value

Update secret <id> with new value
→ Use: update_secret (creates new version)

Add tags to secret <id>
→ Use: update_secret_metadata with tags
```

### Delete Operations

```
Delete secret <id>
→ Use: delete_secret (schedules for deletion)

Specify 7-30 day retention period
→ Use: delete_secret with time_of_deletion_in_days
```

### Configuration

```
Configure default vault/compartment
→ Use: configure_vault

Check current configuration
→ Use: get_vault_config_tool
```

## Secret Naming Convention

Recommended naming pattern: `<environment>-<service>-<secret-type>`

Examples:
- `prod-database-password`
- `staging-api-key-stripe`
- `dev-jwt-secret`
- `prod-ssl-certificate`

## Security Checklist

- [ ] Never commit secrets to git
- [ ] Use environment variables for vault configuration
- [ ] Enable audit logging on vault access
- [ ] Implement secret rotation (e.g., quarterly)
- [ ] Use IAM policies for access control
- [ ] Monitor secret access patterns
- [ ] Keep OCI CLI updated

## Lifecycle of a Secret

1. **Create**: `create_secret` - Initial creation
2. **Active**: Secret is available for use
3. **Update**: `update_secret` - Create new version, previous versions accessible
4. **Schedule Deletion**: `delete_secret` - Marked for deletion
5. **Pending Deletion**: Waiting period (7-30 days)
6. **Deleted**: Permanently removed

## Tools at a Glance

| Tool | Purpose | Creates Version? |
|------|---------|-----------------|
| `list_secrets` | List all secrets | No |
| `search_secrets` | Find by name | No |
| `get_secret_metadata` | Get metadata only | No |
| `list_secret_versions` | See all versions | No |
| `get_secret_value` | Get secret content | No |
| `get_secret` | Complete info | No |
| `create_secret` | Create new secret | Yes (v1) |
| `update_secret` | New version | Yes |
| `update_secret_metadata` | Update metadata | No |
| `delete_secret` | Schedule deletion | No |
| `configure_vault` | Set defaults | N/A |
| `get_vault_config_tool` | Check config | N/A |

## Environment Variables

```bash
# Required
OCI_CONFIG_PROFILE      # OCI CLI profile name
OCI_VAULT_ID           # Vault OCID
OCI_COMPARTMENT_ID     # Compartment OCID

# Optional
FASTMCP_LOG_LEVEL      # DEBUG, INFO, ERROR
OCI_CLI_DEBUG          # true for debug mode
```

## Error Resolution

| Error | Likely Cause | Fix |
|-------|------------|-----|
| `vault_id is required` | Missing env var | `export OCI_VAULT_ID=...` |
| `Permission denied` | No IAM permission | Ask admin for `manage_secrets` |
| `Secret not found` | Wrong ID | Use `list_secrets` to find |
| `Name already exists` | Duplicate name | Use unique name or update existing |
| `Cannot authenticate` | Bad credentials | Run `oci session authenticate` |

## Useful Commands

```bash
# Verify OCI CLI works
oci identity user get --user-id $(oci iam user list | jq -r '.data[0].id')

# Validate session
oci session validate

# List all vaults in compartment
oci vault vault list --compartment-id=$OCI_COMPARTMENT_ID

# Test vault access
oci vault secret list --vault-id=$OCI_VAULT_ID --limit=1

# Enable debug logging
FASTMCP_LOG_LEVEL=DEBUG uvx oracle.oci-vault-mcp-server
```

## Tips & Tricks

1. **Batch Operations**: Ask agent to manage multiple secrets in one conversation
2. **Version Control**: Always verify new version was created after updates
3. **Search First**: Use `search_secrets` before using IDs you're unsure about
4. **Limit Results**: Use `limit` parameter for large vaults to avoid timeouts
5. **Tag Organization**: Use tags to organize by team, environment, or application
6. **Rotation Calendar**: Schedule quarterly secret rotation reviews
7. **Audit Review**: Regularly check audit logs for unauthorized access attempts

## Related Resources

- OCI Vault Documentation: https://docs.oracle.com/en-us/iaas/Content/KeyManagement/Concepts/keyoverview.htm
- OCI CLI Reference: https://docs.oracle.com/en-us/iaas/tools/oci-cli/
- IAM Best Practices: https://docs.oracle.com/en-us/iaas/Content/Identity/Concepts/iam-security.htm
- FastMCP Documentation: https://github.com/jferrettiboke/fastmcp
