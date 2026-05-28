# npm Publishing 2025+ Reference

## Summary of auth changes

- Classic tokens are revoked and cannot be created or used.
- Only granular tokens exist; write-enabled tokens are short-lived (7-day default, 90-day max).
- 2FA is expected for publishing; session-based auth is used for `npm login`.
- WebAuthn/passkeys are the preferred 2FA method.

## Decision tree

1. Use trusted publishing (OIDC) if CI is GitHub Actions or GitLab shared runners.
2. Use granular tokens only when OIDC is not available.
3. Use interactive publish only for bootstrap or emergency fixes.

## Trusted publishing checklist (GitHub Actions)

### npm (one-time)

- Bootstrap the package with an interactive publish if it does not exist.
- Add a trusted publisher for repo + workflow filename.
- After OIDC works, set package policy to require 2FA and disallow tokens.

### GitHub Actions

- Set `permissions: id-token: write` in the publish job.
- Ensure npm CLI >= 11.5.1 (upgrade npm if needed).
- Remove `NODE_AUTH_TOKEN` and `NPM_TOKEN` from publish.
- Use `npm publish` and set `NPM_CONFIG_PROVENANCE=true` when desired.
- Confirm the workflow filename matches the trusted publisher config exactly and exists in `.github/workflows/`.

Example publish job skeleton:

```yaml
permissions:
  contents: read
  id-token: write

steps:
  - uses: actions/checkout@v4
  - uses: actions/setup-node@v5
    with:
      node-version: '22'
      registry-url: 'https://registry.npmjs.org'
  - run: npm install -g npm@11.5.1
  - run: npm ci
  - run: npm run build --if-present
  - run: npm test
  - env:
      NPM_CONFIG_PROVENANCE: 'true'
    run: npm publish
```

## Granular token fallback

- Create a write-enabled granular token scoped to the package.
- Keep expiration short and rotate regularly.
- Use `NODE_AUTH_TOKEN` only for `npm publish`.
- If package policy disallows tokens, publishing will fail.

Safe .npmrc pattern (no secret committed):

```ini
//registry.npmjs.org/:_authToken=${NODE_AUTH_TOKEN}
```

## Release flow (tag-driven)

- `npm version patch|minor|major`
- `git push --follow-tags`

## Documentation updates

- README: document tag-driven release + trusted publishing setup.
- package.json: set `publishConfig.access = "public"` for public scoped packages.
- CI: ensure no secrets are required for publish with OIDC.

## Safety notes

- Never bake tokens into build artifacts or dist outputs.
- Prefer OIDC over any long-lived credential.

## Operational gotchas

- Trusted publishing is strict about the workflow filename; a mismatch (e.g., `release.yml` vs `release.yaml`) causes `npm publish` to fail with `ENEEDAUTH`.
- If a publish job inherits `NODE_AUTH_TOKEN`/`NPM_TOKEN`, npm may attempt token auth instead of OIDC and fail when tokens are empty or expired.
