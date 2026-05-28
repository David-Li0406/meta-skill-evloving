---
name: workspace-integrity
description: How to verify that everything in this workspace is still good and stable.
---

1. `pnpm` package installation, build, linting and tests pass from the root directory
2. `dotnet` package installation, build and tests pass from the root directory
3. `aspire run` starts all resources as healthy
4. `markdownlint-cli2 --config .config/.markdownlint-cli2.jsonc docs/**/*.md README.md` passes
