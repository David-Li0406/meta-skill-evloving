# OCI Vault Setup Checklist

Complete this checklist before using OCI Vault with the MCP Server.

## Prerequisites

- [ ] OCI account with appropriate IAM permissions
- [ ] OCI CLI installed (`oci --version`)
- [ ] OCI Vault created in your compartment
- [ ] API key or session token for authentication

## Authentication Setup

- [ ] Set up OCI CLI authentication
  - [ ] Run `oci session authenticate` OR
  - [ ] Set up API key authentication with `~/.oci/config`
- [ ] Verify authentication works: `oci identity user get --user-id <ocid>`
- [ ] Session is valid: `oci session validate`
- [ ] Choose appropriate profile to use

## Environment Configuration

- [ ] Find your vault OCID
  - [ ] Run: `oci vault vault list --compartment-id=<compartment-ocid>`
  - [ ] Record vault OCID
- [ ] Find your compartment OCID
  - [ ] Run: `oci iam compartment list`
  - [ ] Record compartment OCID
- [ ] Set environment variables:
  ```bash
  export OCI_CONFIG_PROFILE=<profile-name>
  export OCI_VAULT_ID=<vault-ocid>
  export OCI_COMPARTMENT_ID=<compartment-ocid>
  ```
- [ ] Verify environment variables are set:
  ```bash
  echo $OCI_VAULT_ID $OCI_COMPARTMENT_ID
  ```

## IAM Permissions

- [ ] Verify your user/group has required permissions:
  - [ ] `manage_vaults` - to list and configure vaults
  - [ ] `manage_secrets` - to create and update secrets
  - [ ] `read_secrets` - to retrieve secret values
  - [ ] `delete_secrets` - to delete secrets
- [ ] Contact your compartment administrator if permissions are missing

## OCI Vault Server Setup

- [ ] Install or verify OCI Vault MCP Server is available
- [ ] Server can access OCI configuration: `~/.oci/config`
- [ ] Server has correct profile configured in `OCI_CONFIG_PROFILE`

## Connectivity Test

- [ ] Test list_secrets: Check that you can list secrets (empty or populated)
- [ ] Test search_secrets: Search for a known secret
- [ ] Test create_secret: Create a test secret
- [ ] Test update_secret: Update the test secret with a new version
- [ ] Test delete_secret: Schedule the test secret for deletion

## Ready for Production

- [ ] All connectivity tests pass
- [ ] Team is trained on secret naming conventions
- [ ] Secret rotation policy is established
- [ ] Audit logging is enabled in OCI
- [ ] Backup and disaster recovery procedures are documented
- [ ] Secret access is properly audited and monitored
