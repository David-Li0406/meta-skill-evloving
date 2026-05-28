# BasicAuth Mode

**Status**: Defined in fort.nix, no working examples yet

Use `basicauth` mode when the service only supports HTTP Basic Authentication. oauth2-proxy translates OIDC identity into Basic Auth credentials.

## How It Works

1. You declare `sso.mode = "basicauth"` in `fort.cluster.services`
2. fort.nix creates an `oauth2-proxy-<name>` service (same as headers mode)
3. oauth2-proxy authenticates via OIDC with pocket-id
4. Authenticated requests get Basic Auth header injected

## App Responsibilities

```nix
# 1. Declare exposure
fort.cluster.services = [{
  name = "myapp";
  port = 8080;
  sso = {
    mode = "basicauth";
    groups = [ "users" ];  # Optional
  };
}];

# 2. Configure app to accept Basic Auth
# The username will be the OIDC username
# Password handling depends on oauth2-proxy config
```

## Current Implementation

In `common/fort.nix`, basicauth mode uses the same oauth2-proxy setup as headers mode. The `--pass-user-headers` flag is set, which includes Basic Auth passthrough.

**Note**: This mode may need additional oauth2-proxy flags for proper Basic Auth translation. If you're implementing this, check oauth2-proxy docs for:
- `--pass-basic-auth`
- `--basic-auth-password`
- `--set-basic-auth`

## Candidate Services

Services that might benefit from basicauth mode:
- Legacy apps with only Basic Auth support
- Simple HTTP services without header parsing
- APIs that expect Basic Auth credentials

## TODO

- [ ] Add a working example to the codebase
- [ ] Verify oauth2-proxy flags for proper Basic Auth translation
- [ ] Document password handling (static vs derived)

## See Also

- `common/fort.nix:141-200` - oauth2-proxy service definition
- oauth2-proxy docs: https://oauth2-proxy.github.io/oauth2-proxy/
