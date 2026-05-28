# Safety Protocols for Artifact Cleanup

In 2026, where monorepos and complex build pipelines are standard, "blind deletion" can lead to significant downtime or loss of local-only configuration. Follow these protocols to ensure a safe janitorial process.

## 1. The 3-Step Verification Rule

Before executing a destructive command like `rm -rf`, you MUST follow these steps:

1.  **Discovery**: Identify exactly what is being deleted and why. Is it a build artifact (`.next`) or a dependency (`node_modules`)?
2.  **Sizing**: Run a dry run or use `du -sh` to understand the impact. Deleting a 10GB `node_modules` folder takes time and affects system performance.
3.  **Confirmation**: Always seek explicit user confirmation unless the `--force` flag is used in a known safe environment (like a CI cleanup script).

## 2. Protected Files (The "Do Not Touch" List)

Never delete the following files during a standard janitorial pass:

-   `.env` and `.env.local`: Contain sensitive secrets and local configuration.
-   `.git/`: Deleting this destroys the repository's history and state.
-   `*.db`, `*.sqlite`: Local development databases.
-   `package.json`, `bun.lock`, `pnpm-lock.yaml`: Dependency definitions.

## 3. Handling Monorepos

In workspaces (Bun/pnpm), artifacts are often scattered across multiple packages.

-   **Root Cleanup**: Some artifacts live in the root `node_modules`.
-   **Package Cleanup**: Each package has its own `dist`, `.next`, or `node_modules`.
-   **Strategy**: Use the `scripts/deep-clean.sh` which traverses the entire tree, or use package manager commands like `pnpm -r exec rm -rf node_modules`.

## 4. Post-Cleanup Recovery

Always assume the environment is "broken" after a deep clean.

-   **Reinstall**: Run `bun install` or `pnpm install`.
-   **Rebuild**: Run `bun run build`.
-   **Check**: Verify the dev server starts correctly with `bun dev`.

## 5. Automation Safety

When using the `deep-clean.sh` script in an automated fashion:

-   Always use `--dry-run` first in logs to see what was targeted.
-   Log the amount of space reclaimed for audit purposes.
-   Ensure no critical processes are running that might be using those files (e.g., a running Next.js dev server).

---
*Updated: January 22, 2026 - 16:45*
