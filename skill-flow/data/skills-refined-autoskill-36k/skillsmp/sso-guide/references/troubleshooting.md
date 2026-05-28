# SSO Troubleshooting

Common issues and debugging steps for SSO integration.

## Credential Delivery Issues

### Symptoms
- Service fails to authenticate
- "Invalid client" errors
- Credentials file empty or contains placeholder

### Debugging

1. **Check if service-registry has run**:
   ```bash
   ssh root@<forge-host> "journalctl -u fort-service-registry -n 50"
   ```

2. **Check credentials were delivered**:
   ```bash
   ssh root@<app-host> "cat /var/lib/fort-auth/<service>/client-id"
   ssh root@<app-host> "cat /var/lib/fort-auth/<service>/client-secret"
   ```

3. **Verify pocket-id client exists**:
   ```bash
   # On forge host, or via API
   curl -H "X-API-KEY: $(cat /var/lib/pocket-id/service-key)" \
     https://id.<domain>/api/oidc/clients
   ```

4. **Force service-registry to run**:
   ```bash
   ssh root@<forge-host> "systemctl start fort-service-registry"
   ```

### Common Causes

- **First deployment**: Credentials don't exist yet. Wait up to 10 minutes for service-registry.
- **SSH issues**: service-registry can't reach the host. Check tailscale connectivity.
- **Missing tmpfiles**: `/var/lib/fort-auth/<service>/` doesn't exist. Add tmpfiles rules.

## OIDC Callback Issues

### Symptoms
- Redirect loop after login
- "Callback URL mismatch" errors
- Login succeeds but app rejects token

### Debugging

1. **Check callback URL in pocket-id**:
   - Client should be named after the service FQDN (e.g., `outline.example.com`)
   - Callback URLs should include the app's expected paths

2. **Verify app's configured redirect URI**:
   - Must match what pocket-id expects
   - Usually `https://<service>.<domain>/callback` or similar

### Common Causes

- **Wrong issuer URL**: Use `https://id.${domain}`, not `https://id.${domain}/`
- **Missing scopes**: Ensure `openid email profile` are requested
- **HTTPS mismatch**: Callback must use HTTPS if app is behind HTTPS proxy

## oauth2-proxy Issues

### Symptoms
- 502 Bad Gateway
- "Upstream connection refused"
- oauth2-proxy service failing

### Debugging

1. **Check oauth2-proxy service**:
   ```bash
   ssh root@<host> "systemctl status oauth2-proxy-<service>"
   ssh root@<host> "journalctl -u oauth2-proxy-<service> -n 50"
   ```

2. **Check socket exists**:
   ```bash
   ssh root@<host> "ls -la /run/fort-auth/<service>.sock"
   ```

3. **Check app is listening**:
   ```bash
   ssh root@<host> "ss -tlnp | grep <port>"
   ```

### Common Causes

- **App not running**: oauth2-proxy can't reach upstream
- **Wrong port**: `fort.cluster.services` port doesn't match app
- **Permission issues**: nginx can't read the socket

## Groups Claim Issues

**Note**: Group-based access control is **not yet functional**. The `sso.groups` option exists in the schema but isn't wired up. See `fort-040` for tracking.

When this is implemented, common issues might include:
- oauth2-proxy not receiving groups claim from pocket-id
- Groups scope not requested
- LDAP group sync issues

## Header Injection Issues

### Symptoms
- App doesn't see `X-Forwarded-User`
- User shows as anonymous despite login
- Headers present but app ignores them

### Debugging

1. **Verify headers are being set**:
   Add a debug endpoint or check app logs for incoming headers.

2. **Check app trusts the headers**:
   - App must be configured to read from proxy headers
   - May need to whitelist the proxy IP

### Common Causes

- **App config**: Proxy auth not enabled
- **Wrong header name**: App expects `REMOTE_USER` but gets `X-Forwarded-User`
- **Multiple proxies**: Headers stripped by intermediate proxy

## General Tips

1. **Check the flow order**:
   - service-registry runs on forge (drhorrible)
   - Provisions pocket-id clients
   - SSHs credentials to target hosts
   - Restarts specified service

2. **Timing matters**:
   - service-registry runs every 10 minutes
   - First deploy will have placeholder creds until sync

3. **Logs to check**:
   - `fort-service-registry` on forge host
   - `oauth2-proxy-<service>` on app host
   - `nginx` on app host
   - The app's own logs

4. **When in doubt**:
   - Force service-registry run
   - Restart oauth2-proxy
   - Restart the app
   - Check pocket-id admin UI
