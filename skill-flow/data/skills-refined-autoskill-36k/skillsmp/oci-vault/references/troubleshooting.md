# OCI Vault Troubleshooting Guide

Common issues and solutions when using OCI Vault with the MCP Server.

## Authentication & Configuration Errors

### "vault_id is required"

**Error Message**: 
```
vault_id is required. Either provide vault_id parameter or set OCI_VAULT_ID environment variable
```

**Cause**: The OCI_VAULT_ID environment variable is not set or not provided as a parameter.

**Solutions**:
1. Set the environment variable:
   ```bash
   export OCI_VAULT_ID=ocid1.vault.oc1.phx.xxxxxxxxxxxxx
   ```

2. Or provide it directly to the tool:
   ```
   Tell the agent: List secrets in vault ocid1.vault.oc1.phx.xxxxxxxxxxxxx
   ```

3. Verify it's set:
   ```bash
   echo $OCI_VAULT_ID
   ```

---

### "compartment_id is required"

**Error Message**: 
```
compartment_id is required. Either provide compartment_id parameter or set OCI_COMPARTMENT_ID environment variable
```

**Cause**: The OCI_COMPARTMENT_ID environment variable is not set.

**Solutions**:
1. Set the environment variable:
   ```bash
   export OCI_COMPARTMENT_ID=ocid1.compartment.oc1.xxxxxxxxxxxxx
   ```

2. Find your compartment ID:
   ```bash
   oci iam compartment list --output table
   ```

---

### "Import 'oci' could not be resolved"

**Error Message**: Python import error for OCI library.

**Cause**: OCI Python SDK not installed or virtual environment not activated.

**Solutions**:
1. Install OCI SDK:
   ```bash
   pip install oci
   ```

2. Verify installation:
   ```bash
   python -c "import oci; print(oci.__version__)"
   ```

3. Ensure virtual environment is activated if using one.

---

## Authentication Failures

### "Cannot authenticate with OCI"

**Error Message**: Authentication errors when connecting to OCI API.

**Cause**: OCI credentials are not properly configured or expired.

**Solutions**:
1. Verify OCI configuration exists:
   ```bash
   ls -la ~/.oci/config
   ```

2. Test authentication:
   ```bash
   oci identity user get --user-id ocid1.user.oc1.xxxxxxxxxxxxx
   ```

3. For session-based auth, validate session:
   ```bash
   oci session validate
   ```

4. For API key auth, verify key files exist:
   ```bash
   ls -la ~/.oci/oci_api_key.pem
   ```

5. Check OCI_CONFIG_PROFILE is set correctly:
   ```bash
   echo $OCI_CONFIG_PROFILE
   oci identity user get  # Should show current user
   ```

---

### "Permission denied" or "Access Denied"

**Error Message**: OCI API returns 403 or permission error.

**Cause**: User lacks required IAM permissions.

**Solutions**:
1. Check current user:
   ```bash
   oci iam user get --user-id <current-user-ocid>
   ```

2. Verify group membership:
   ```bash
   oci iam user list-groups --user-id <current-user-ocid>
   ```

3. Request permissions from compartment administrator:
   - Need: `manage_secrets` in the vault's compartment
   - Need: `read_secrets` for reading operations
   - Need: `delete_secrets` for deletion operations

4. Verify IAM policy is attached:
   ```bash
   oci iam policy list --compartment-id <compartment-ocid>
   ```

---

### "Invalid API key" or "Invalid token"

**Error Message**: Signature or token validation failed.

**Cause**: 
- API key is malformed or incorrect
- Security token file is missing or corrupted
- Key file permissions are incorrect

**Solutions**:
1. For API key authentication:
   ```bash
   # Check key file permissions (should be 600)
   ls -la ~/.oci/oci_api_key.pem
   
   # Fix permissions if needed
   chmod 600 ~/.oci/oci_api_key.pem
   ```

2. For session-based authentication:
   ```bash
   # Refresh token
   oci session authenticate --region=us-phoenix-1
   ```

3. Verify config file format:
   ```bash
   cat ~/.oci/config  # Check for correct profile
   ```

---

## Vault & Compartment Issues

### "Invalid vault ID"

**Error Message**: Vault OCID not found or invalid format.

**Cause**: Vault OCID is incorrect or vault doesn't exist in specified compartment.

**Solutions**:
1. List available vaults:
   ```bash
   oci vault vault list --compartment-id=$OCI_COMPARTMENT_ID
   ```

2. Verify vault OCID format (should start with `ocid1.vault.oc1.`)

3. Ensure vault is in correct compartment

---

### "Cannot find vault in compartment"

**Error Message**: Vault exists but not in the specified compartment.

**Cause**: Vault is in a different compartment than specified.

**Solutions**:
1. List all vaults in root compartment:
   ```bash
   oci vault vault list --compartment-id=ocid1.compartment.oc1.xxxxxxxxxxxxx
   ```

2. Find correct compartment ID:
   ```bash
   oci iam compartment list --output table
   ```

3. Update OCI_COMPARTMENT_ID to correct value

---

## Secret Operations

### "Secret not found"

**Error Message**: The specified secret ID doesn't exist.

**Cause**: 
- Secret ID is incorrect
- Secret was deleted
- Secret is in different vault/compartment

**Solutions**:
1. List secrets to find correct ID:
   ```bash
   oci vault secret list --vault-id=$OCI_VAULT_ID
   ```

2. Search by name:
   ```bash
   oci vault secret list --vault-id=$OCI_VAULT_ID --search-by-name=<name-pattern>
   ```

3. Verify vault ID is correct:
   ```bash
   echo $OCI_VAULT_ID
   ```

---

### "Cannot create secret: name already exists"

**Error Message**: A secret with that name already exists in the vault.

**Cause**: You're trying to create a secret with a name that's already in use.

**Solutions**:
1. Use a unique name:
   ```
   Create secret "my-api-key-v2" instead
   ```

2. Or update the existing secret:
   ```
   Update the existing secret with new version
   ```

3. Or delete the old one first (requires 7-30 day retention period):
   ```
   Schedule secret for deletion
   ```

---

### "Secret is scheduled for deletion"

**Error Message**: Cannot modify a secret that's scheduled for deletion.

**Cause**: Secret is in pending deletion state.

**Solutions**:
1. Cancel deletion (requires specific API call):
   ```bash
   oci vault secret cancel-deletion --secret-id=<secret-id>
   ```

2. Wait for deletion to complete (if you want to reuse the name)

3. Create new secret with different name

---

## Performance Issues

### "Operation is slow"

**Cause**: Large number of secrets in vault or network latency.

**Solutions**:
1. Use `limit` parameter to reduce result set:
   ```
   List 100 secrets in vault
   ```

2. Use `search_secrets` instead of `list_secrets` to filter

3. Check network connectivity to OCI:
   ```bash
   ping oss.oraclecloud.com
   ```

4. Consider pagination if vault has many secrets

---

### "Timeout when listing secrets"

**Cause**: Vault has too many secrets and operation is taking too long.

**Solutions**:
1. Use pagination with limit:
   ```
   List 50 secrets first
   ```

2. Use search instead:
   ```
   Search for secrets containing specific pattern
   ```

3. Contact OCI support if vault is very large

---

## MCP Server Issues

### "MCP Server not responding"

**Error Message**: Cannot connect to OCI Vault MCP Server.

**Cause**: 
- Server not running
- Server crashed
- Connection timeout

**Solutions**:
1. Check if server is running:
   ```bash
   ps aux | grep oci-vault-mcp
   ```

2. Restart the server:
   ```bash
   killall oci-vault-mcp
   # Restart OpenCode or manually start server
   ```

3. Check server logs for errors:
   ```bash
   FASTMCP_LOG_LEVEL=DEBUG uvx oracle.oci-vault-mcp-server
   ```

---

### "Tool not found" error

**Cause**: MCP Server tools not registered properly.

**Solutions**:
1. Verify tools are available:
   ```bash
   Ask agent: What tools are available?
   ```

2. Restart OpenCode to reload MCP servers

3. Check opencode.json configuration for oci-vault MCP entry

---

## Security Concerns

### "Should I be concerned about secret exposure?"

**Best Practice**: All secrets should be:
- Transmitted over HTTPS/TLS
- Never logged or printed to console
- Access should be audited
- Regularly rotated
- Restricted by IAM policy

Verify audit logging is enabled:
```bash
oci audit event list --compartment-id=$OCI_COMPARTMENT_ID
```

---

## Getting Help

If you're still experiencing issues:

1. **Check OCI documentation**: https://docs.oracle.com/en-us/iaas/Content/KeyManagement/Concepts/keyoverview.htm

2. **Check OCI CLI help**: `oci vault --help`

3. **Enable debug logging**:
   ```bash
   export FASTMCP_LOG_LEVEL=DEBUG
   export OCI_CLI_DEBUG=true
   ```

4. **Contact OCI Support**: Through your OCI account

5. **Open an issue**: In the project repository
