# Gatekeeper Mode

**Status**: Working examples in `apps/silverbullet/`, `apps/flatnotes/`, `apps/vdirsyncer-auth/`

Use `gatekeeper` mode when you need a login wall but don't need to pass identity to the backend. Users must authenticate, but the app doesn't receive any user info.

## How It Works

1. You declare `sso.mode = "gatekeeper"` in `fort.cluster.services`
2. fort.nix creates an `oauth2-proxy-<name>` service
3. oauth2-proxy requires OIDC login before proxying
4. Requests reach the backend without identity headers

## Use Cases

- Public-facing apps that should require login but don't use identity
- Simple access control without user-specific behavior
- "Members only" gates for content

## App Responsibilities

```nix
fort.cluster.services = [{
  name = "myapp";
  port = 8080;
  sso = {
    mode = "gatekeeper";
    groups = [ "members" ];  # Optional: restrict to specific groups
  };
}];
```

The app doesn't need any special configuration - it just receives normal HTTP requests after the user has authenticated at the oauth2-proxy level.

## Current Implementation

In `common/fort.nix`, gatekeeper mode uses the same oauth2-proxy setup as headers mode but the backend app simply ignores the injected headers.

A cleaner implementation might use different oauth2-proxy flags to avoid injecting headers at all, but the current approach works.

## Candidate Services

Services that might benefit from gatekeeper mode:
- Static file servers with "members only" content
- Simple dashboards without user-specific views
- Development/staging environments that need access control

## VPN Bypass (Split-Gatekeeper)

For services that should require login from the public internet but allow direct access from the VPN:

```nix
fort.cluster.services = [{
  name = "status";
  port = 8080;
  visibility = "public";  # Must be public or local for vpnBypass to be useful
  sso = {
    mode = "gatekeeper";
    vpnBypass = true;     # VPN requests skip auth entirely
  };
}];
```

**How it works:**
- Requests from the VPN (`$is_vpn = 1`) go directly to the backend
- Requests from the public internet go through oauth2-proxy

This is useful for monitoring dashboards, internal tools, or any service where VPN membership implies sufficient trust.

The `vpnBypass` option works with any SSO mode (`gatekeeper`, `headers`, `basicauth`), not just gatekeeper.

## TODO

- [ ] Consider whether to strip headers in gatekeeper mode

## See Also

- `common/fort.nix:182-190` - vpnBypass option definition
- `common/fort.nix:373-379` - nginx conditional routing
