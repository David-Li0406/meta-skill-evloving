# Headers Mode

**Status**: Working, has examples

Use `headers` mode when the service can consume identity from HTTP headers. fort.nix sets up oauth2-proxy to inject `X-Auth-*` headers after authentication.

## How It Works

1. You declare `sso.mode = "headers"` in `fort.cluster.services`
2. fort.nix creates an `oauth2-proxy-<name>` systemd service
3. nginx proxies to oauth2-proxy's unix socket instead of directly to the app
4. oauth2-proxy handles OIDC auth with pocket-id
5. Authenticated requests get `X-Auth-*` headers injected

## Headers Injected

oauth2-proxy injects these headers (with `--pass-user-headers`):

| Header | Contents |
|--------|----------|
| `X-Forwarded-User` | Username |
| `X-Forwarded-Email` | Email address |
| `X-Forwarded-Preferred-Username` | Preferred username |
| `X-Forwarded-Groups` | Comma-separated group list |

## App Responsibilities

```nix
# 1. Declare exposure
fort.cluster.services = [{
  name = "myapp";
  port = 8080;
  sso = {
    mode = "headers";
    groups = [ "users" ];  # Optional: restrict access
  };
}];

# 2. Configure app to trust proxy headers
# (app-specific - see example below)
```

## Working Example: Grafana

From `apps/fort-observability/default.nix`:

```nix
{ rootManifest, ... }:
{ config, pkgs, ... }:
let
  domain = rootManifest.fortConfig.settings.domain;
in
{
  services.grafana = {
    enable = true;
    settings = {
      server = {
        http_port = 3000;
        http_addr = "0.0.0.0";
      };

      # Enable proxy authentication
      "auth.proxy" = {
        enabled = true;
        header_name = "X-Forwarded-User";  # Read user from this header
      };
    };
  };

  fort.cluster.services = [{
    name = "monitor";
    port = 3000;
    sso.mode = "headers";
  }];
}
```

## What fort.nix Does

When you use `sso.mode = "headers"`, fort.nix (`common/fort.nix:141-200`) creates:

1. **oauth2-proxy service** (`oauth2-proxy-<name>`):
   - Listens on unix socket `/run/fort-auth/<name>.sock`
   - Proxies to your app at `http://127.0.0.1:<port>`
   - Configured for pocket-id OIDC
   - Auto-generates cookie secret if missing

2. **nginx location**:
   - Proxies to the oauth2-proxy socket instead of directly to your app
   - WebSocket support included

3. **State directories**:
   - `/var/lib/fort-auth/<name>/` for credentials
   - `/run/fort-auth/<name>/` for runtime socket

## Credential Provisioning

service-registry provisions OIDC credentials for headers mode too:

- Creates pocket-id client named after the service FQDN
- Delivers credentials to `/var/lib/fort-auth/<name>/`
- Restarts `oauth2-proxy-<name>` (default) or custom `sso.restart` target

## Group Restrictions (Planned)

The schema supports group-based access control:

```nix
sso = {
  mode = "headers";
  groups = [ "admins" "developers" ];
};
```

**Note**: This is **not yet functional**. See `fort-040` for tracking. When implemented, it will pass `--allowed-group` flags to oauth2-proxy.

## Common App Configurations

### Grafana
```nix
"auth.proxy" = {
  enabled = true;
  header_name = "X-Forwarded-User";
};
```

### Generic Header Trust
Many apps have a "trust proxy headers" or "reverse proxy auth" option. Look for:
- `REMOTE_USER` or `X-Forwarded-User` header config
- "Proxy authentication" or "Header authentication" settings
- "Trust X-Forwarded-*" options

## See Also

- `apps/fort-observability/default.nix` - Grafana with headers auth
- `common/fort.nix:141-200` - oauth2-proxy service definition
