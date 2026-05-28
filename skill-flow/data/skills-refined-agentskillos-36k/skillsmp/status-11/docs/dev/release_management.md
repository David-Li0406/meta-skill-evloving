# Release Management

This document will eventually describe the full release process for WAIF.

For now, it provides an initial recommended process that matches the current repository and CLI behavior.

## Goals

- Ship changes without breaking `main`.
- Make it easy to answer: “What version is running?” and “What changed?”
- Keep releases reproducible and verifiable.

## Definitions

- **Release artifact**: A built distribution intended for users (e.g., npm package / published tarball). It will not include `.git/`.
- **Working tree**: A developer checkout with `.git/` present.

## Version Number Management

### `waif --version`

The CLI prints a version string and exits without running other application logic.

- **Release mode**: prints `v<package.json version>` (example: `v1.2.3`).
- **Dev mode**: prints a development stamp: `v0.0.0-dev+YYYYMMDDTHHMMSS.<short-commit>`.
  - The `<short-commit>` suffix is included when a git repo is available.

The logic lives in `src/lib/version.ts` and is consumed by `src/index.ts`.

### Strategy

- The source of truth for release semver is `package.json`.
- Tags are used to indicate official releases.
- A working tree that is **not** exactly at the tag `v<package.json version>` is considered “unreleased” and will emit the dev stamp.

### Release requirements

- Bump `package.json` to the desired semver.
- Create an annotated git tag matching `v<package.json version>`.
- Ensure the release artifact reliably contains `package.json` with that version.

### Notes for deterministic testing

The CLI currently selects version output based solely on tags / `.git` presence (see “Current `waif --version` behavior” above).

A future testability hook under consideration is a `WAIF_VERSION_MODE` environment variable that would force behavior:

- `WAIF_VERSION_MODE=release` would force `v<package.json version>`.
- `WAIF_VERSION_MODE=dev` would force `v0.0.0-dev+...`.
- `WAIF_VERSION_MODE=auto` (default) would select based on tag / `.git` presence.

This environment variable is **not yet implemented** in the current CLI; setting it has no effect today.
## Proposed Release Process (Initial)

This is a minimal process intended to work well with the current repo conventions.

### 1) Prepare the release on a topic branch

- Create a branch like `release/vX.Y.Z`.
- Update `package.json` version.
- Update `CHANGELOG.md` (user-facing summary).
- Run quality gates:
  - `npm run build`
  - `npm test`

### 2) Open a PR

- Open a PR into `main`.
- Ensure CI or local checks pass.
- Get review and approval.

### 3) Merge to `main`

- Merge the PR.
- Pull `main` locally.

### 4) Tag the release

- Create a tag on the merge commit:
  - `git tag -a vX.Y.Z -m "WAIF vX.Y.Z"`
  - `git push origin vX.Y.Z`

The tag name must match `v<package.json version>` for `waif --version` to emit the release semver in `auto` mode.

### 5) Build and publish the release artifact

This repository is currently set up to build to `dist/` via TypeScript.

- `npm run build`
- Publish (exact mechanism TBD):
  - npm publish
  - GitHub Releases upload
  - or attach artifact to the tag

### 6) Post-release checks

- Install/use the released artifact and verify:
  - `waif --version` prints `vX.Y.Z`
  - core commands still function (`waif --help`, `waif next`, etc.)

## Open Questions / Follow-ups

- Decide whether releases are published to npm, GitHub Releases, or both.
- Decide whether to generate release notes automatically from `CHANGELOG.md`.
- Decide whether to enforce version/tag correctness in CI (recommended).
