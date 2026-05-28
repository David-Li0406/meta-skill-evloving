---
name: npm-publishing
description: Guidance for publishing npm packages with modern npm auth (trusted publishing/OIDC, granular tokens, 2FA) and release automation. Use when configuring GitHub Actions or other CI publish workflows, updating npm publish docs, or troubleshooting npm token/auth changes.
---

# Npm Publishing

## Overview

Use this skill to design or update npm publish workflows that align with the post-2025 token model (trusted publishing preferred, granular token fallback) and to keep release docs in sync with CI behavior.

## Workflow decision

1. Prefer trusted publishing (OIDC) when CI is GitHub Actions or GitLab shared runners.
2. Use granular tokens only when OIDC is not available (self-hosted runners, unsupported CI).
3. Keep interactive publish for bootstrap/emergency only.

## Trusted publishing workflow (OIDC)

- Configure npm trusted publisher for the repo + workflow filename.
- Ensure the workflow filename matches the trusted publisher setting exactly (e.g., `release.yaml` vs `release.yml`).
- Ensure workflow uses `permissions: id-token: write` and `contents: read`.
- Use npm CLI >= 11.5.1 in CI.
- Remove `NODE_AUTH_TOKEN`/`NPM_TOKEN` from publish steps so npm uses OIDC.
- Prefer `npm publish` with `NPM_CONFIG_PROVENANCE=true` or rely on npm defaults.
- Lock package settings to require 2FA and disallow tokens after OIDC is configured.

Refer to `references/npm-publishing-2025.md` for the full checklist and examples.

## Granular token fallback

- Create a write-enabled granular token scoped to the package only.
- Keep expiration short and rotate on a schedule.
- Use `NODE_AUTH_TOKEN` only for `npm publish` and avoid storing tokens in code or build outputs.
- If package settings disallow tokens, this path will not work.

Refer to `references/npm-publishing-2025.md` for fallback guidance.

## Repo updates to keep in sync

- `package.json`:
  - Add `publishConfig.access = "public"` for public scoped packages.
  - Add release scripts that tag + push (e.g., `release:patch`).
- `README.md`:
  - Document the tag-driven release flow.
  - Note trusted publishing setup steps and the tokenless publish policy.
- `.github/workflows/*.yml`:
  - Align permissions and npm version for OIDC.
  - Ensure publish job does not use secrets when OIDC is enabled.

## Validation steps

- Run `npm pack --dry-run` to verify published contents.
- Run `bun run build` (or repo build command) to confirm dist is fresh.
- Confirm `npm publish --dry-run` behaves as expected when run locally.

## Resources

### references/

- `references/npm-publishing-2025.md` for policy shifts, decision points, and workflow examples.
