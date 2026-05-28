# OIDC Mode

**Status**: Working, has examples

Use `oidc` mode when the service supports OpenID Connect natively. The control plane (`oidc-register` capability) automatically provisions credentials in pocket-id and delivers them to the target host.

## How It Works

1. You declare `sso.mode = "oidc"` in `fort.cluster.services`
2. `common/fort.nix` auto-generates a `fort.host.needs.oidc-register.<service>` declaration
3. The consumer contacts the pocket-id host via the control plane
4. The `oidc-register` capability creates/returns OIDC client credentials
5. The consumer handler writes credentials to `/var/lib/fort-auth/<service-name>/`:
   - `client-id` - the OIDC client ID
   - `client-secret` - the OIDC client secret
6. The service specified in `sso.restart` is restarted

## App Responsibilities

```nix
# 1. Declare exposure with restart target
fort.cluster.services = [{
  name = "myapp";
  port = 8080;
  visibility = "public";  # or vpn, local
  sso = {
    mode = "oidc";
    restart = "myapp.service";  # Service to restart after creds delivered
  };
}];

# 2. Create tmpfiles for credential directory
systemd.tmpfiles.rules = [
  "d /var/lib/fort-auth/myapp 0700 myapp myapp -"
  "f /var/lib/fort-auth/myapp/client-id 0600 myapp myapp -"
  "f /var/lib/fort-auth/myapp/client-secret 0600 myapp myapp -"
];

# 3. Configure the app to use pocket-id OIDC endpoints
# (see example below for credential injection pattern)
```

## Pocket ID OIDC Endpoints

```
Issuer URL:    https://id.${domain}
Auth URL:      https://id.${domain}/authorize
Token URL:     https://id.${domain}/api/oidc/token
Userinfo URL:  https://id.${domain}/api/oidc/userinfo
```

## Working Example: Outline

From `apps/outline/default.nix`:

```nix
{ rootManifest, ... }:
{ pkgs, ... }:
let
  domain = rootManifest.fortConfig.settings.domain;

  # Wrap the binary to inject credentials at runtime
  wrappedOutline = pkgs.symlinkJoin {
    name = "outline-wrapped";
    paths = [ pkgs.outline ];
    buildInputs = [ pkgs.makeWrapper ];
    postBuild = ''
      wrapProgram $out/bin/outline-server \
        --run 'export OIDC_CLIENT_ID=$(cat /var/lib/fort-auth/outline/client-id)' \
        --run 'export OIDC_CLIENT_SECRET=$(cat /var/lib/fort-auth/outline/client-secret)'
    '';
  };
in
{
  systemd.tmpfiles.rules = [
    "d /var/lib/fort-auth/outline 0755 outline outline -"
    "f /var/lib/fort-auth/outline/client-id 0600 outline outline -"
    "f /var/lib/fort-auth/outline/client-secret 0600 outline outline -"
  ];

  services.outline = {
    enable = true;
    package = wrappedOutline;
    port = 4654;
    publicUrl = "https://outline.${domain}";
    oidcAuthentication = {
      authUrl = "https://id.${domain}/authorize";
      tokenUrl = "https://id.${domain}/api/oidc/token";
      userinfoUrl = "https://id.${domain}/api/oidc/userinfo";
      scopes = [ "openid" "email" "profile" ];
      usernameClaim = "preferred_username";
      displayName = "Pocket ID";

      # Placeholder - overridden at runtime by wrapper
      clientId = "outline";
      clientSecretFile = "/var/lib/fort-auth/outline/client-secret";
    };
  };

  fort.cluster.services = [{
    name = "outline";
    port = 4654;
    visibility = "public";
    sso = {
      mode = "oidc";
      restart = "outline.service";
    };
  }];
}
```

## Credential Injection Patterns

### Pattern 1: wrapProgram (environment variables)

Best when the app reads credentials from environment variables:

```nix
wrappedApp = pkgs.symlinkJoin {
  name = "app-wrapped";
  paths = [ pkgs.myapp ];
  buildInputs = [ pkgs.makeWrapper ];
  postBuild = ''
    wrapProgram $out/bin/myapp \
      --run 'export CLIENT_ID=$(cat /var/lib/fort-auth/myapp/client-id)' \
      --run 'export CLIENT_SECRET=$(cat /var/lib/fort-auth/myapp/client-secret)'
  '';
};
```

### Pattern 2: clientSecretFile (if supported)

Best when the NixOS module supports file-based secrets:

```nix
services.myapp.oidc = {
  clientId = "myapp";  # Will be wrong until first sync, but required
  clientSecretFile = "/var/lib/fort-auth/myapp/client-secret";
};
```

### Pattern 3: ExecStartPre script

For services that need secrets in config files:

```nix
systemd.services.myapp.serviceConfig.ExecStartPre = pkgs.writeShellScript "inject-oidc" ''
  CLIENT_ID=$(cat /var/lib/fort-auth/myapp/client-id)
  CLIENT_SECRET=$(cat /var/lib/fort-auth/myapp/client-secret)
  sed -i "s/CLIENT_ID_PLACEHOLDER/$CLIENT_ID/" /var/lib/myapp/config.json
  sed -i "s/CLIENT_SECRET_PLACEHOLDER/$CLIENT_SECRET/" /var/lib/myapp/config.json
'';
```

## Initial Deployment Timing

On first deployment, credentials don't exist yet:

1. Service starts with dummy/placeholder credentials
2. Control plane consumer triggers (on deploy or via retry timer)
3. Real credentials are delivered
4. Service is restarted with valid credentials

The control plane retry interval is configurable via `nag` (default 15m for OIDC). Credentials should arrive shortly after deployment.

## See Also

- `apps/outline/default.nix` - Full OIDC example
- `apps/forgejo/default.nix` - OIDC with custom setup service
- `apps/pocket-id/default.nix` - The `oidc-register` capability provider
- `common/fort.nix` - Auto-generation of OIDC needs from service declarations
