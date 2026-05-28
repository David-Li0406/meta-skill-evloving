---
name: x07-package
description: Use this skill when managing X07 project dependencies and lockfiles for reproducible builds, including adding dependencies, generating lockfiles, and publishing packages.
---

# Skill body

This skill documents the single canonical workflow for dependency management in X07 using the built-in package manager (`x07 pkg ...`).

## When to use

Use this skill when:
- adding/updating dependencies,
- generating/verifying lockfiles,
- publishing a package to an index/registry.

## Canonical commands

- Add a dependency entry to `x07.json` and sync the lockfile:
  - `x07 pkg add <name>@<version> --sync`

- Generate or update a project lockfile:
  - `x07 pkg lock --project x07.json`

- Verify a lockfile is up to date (CI mode):
  - `x07 pkg lock --project x07.json --check`

- Pack a package directory deterministically:
  - `x07 pkg pack --package <dir> --out <out.tar.gz>`

- Login (store credentials for an index):
  - `x07 pkg login --index <url> --token <token>`

- Publish:
  - `x07 pkg publish --package <dir> --index <url>`

## Notes

- The lockfile path is controlled by `x07.json` (`lockfile`) and defaults to `x07.lock.json`.
- When fetching is required, `x07 pkg lock` defaults to the official registry index; override with `--index <url>`.
- Official packages may declare required helper packages via `meta.requires_packages`. When present, `x07 pkg lock` will add and fetch these transitive dependencies automatically (and update `x07.json`).
- If dependencies are already present on disk, `x07 pkg lock` can run without `--index` using `--offline`.

See also: https://x07lang.org/docs/packages/publishing-by-example/