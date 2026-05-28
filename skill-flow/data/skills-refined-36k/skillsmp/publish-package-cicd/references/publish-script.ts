#!/usr/bin/env bun

/**
 * Custom publish script for monorepos with workspace:* dependencies
 * 
 * Problem:
 * - `npm publish` doesn't resolve workspace:* protocol (fails with "invalid version")
 * - `bunx changeset publish` doesn't resolve workspace:* either
 * - `bun publish` resolves workspace:* but doesn't support npm OIDC (requires npm login)
 * 
 * Solution:
 * 1. `bun pm pack` - Creates tarball with workspace:* resolved to actual versions (e.g., 0.1.0)
 * 2. `npm publish <tarball>` - Publishes tarball with OIDC Trusted Publisher support
 * 
 * Why this works:
 * - bun pm pack reads lockfile and resolves workspace:* to concrete versions
 * - npm publish supports OIDC (auto-detects CI env, no manual token needed)
 * - Tarballs bypass npm's package.json validation (workspace:* already resolved)
 * 
 * Critical gotcha:
 * - Lockfile MUST be synced before packing (run `bun install` in CI)
 * - If lockfile is stale, you'll pack old versions
 * 
 * Usage:
 * 1. Add to root package.json scripts:
 *    "ci:publish": "bun run scripts/publish.ts"
 * 2. Configure Changesets action to use this script:
 *    publish: bun run ci:publish
 * 3. Ensure CI runs `bun install` before publish step
 */

import { $ } from "bun";
import { resolve } from "node:path";
import { readdir, unlink } from "node:fs/promises";

// List of packages to publish (relative to repo root)
// Adjust to match your monorepo structure
const PACKAGES = [
  "packages/swarm-mail",
  "packages/opencode-swarm-plugin",
];

/**
 * Get published version from npm registry
 * Returns null if package not yet published
 */
async function getPublishedVersion(name: string): Promise<string | null> {
  try {
    const output = await $`npm view ${name} version`.quiet().text();
    return output.trim();
  } catch {
    // Package not found in registry (first publish)
    return null;
  }
}

/**
 * Get local version from package.json
 */
async function getLocalVersion(pkgPath: string) {
  const pkgJsonPath = resolve(pkgPath, "package.json");
  const pkg = await Bun.file(pkgJsonPath).json();
  return {
    name: pkg.name,
    version: pkg.version,
  };
}

/**
 * Publish a single package
 * Skip if local version matches npm registry version
 */
async function publishPackage(pkgPath: string) {
  const { name, version } = await getLocalVersion(pkgPath);
  const npmVersion = await getPublishedVersion(name);

  // Skip if already published
  if (npmVersion === version) {
    console.log(`[SKIP] ${name}@${version} - already published`);
    return;
  }

  console.log(`[PUBLISH] ${name}@${version} (npm: ${npmVersion ?? "not published"})`);

  // Step 1: Create tarball with workspace:* resolved
  // This reads bun.lock and replaces workspace:* with actual versions
  await $`bun pm pack`.cwd(pkgPath).quiet();

  // Step 2: Find generated tarball
  const files = await readdir(pkgPath);
  const tarball = files.find((f) => f.endsWith(".tgz"));
  if (!tarball) {
    throw new Error(`No tarball found in ${pkgPath} after bun pm pack`);
  }

  // Step 3: Publish tarball to npm
  // npm CLI 11.5.1+ auto-detects OIDC environment (no NPM_TOKEN needed)
  // For classic tokens, ensure NPM_TOKEN is set in .npmrc
  await $`npm publish ${resolve(pkgPath, tarball)} --access public`.quiet();

  // Step 4: Cleanup tarball
  await unlink(resolve(pkgPath, tarball));

  console.log(`[SUCCESS] ${name}@${version} published`);
}

/**
 * Main entry point
 * Publishes all packages that have version bumps
 */
async function main() {
  console.log("Starting publish process...\n");

  for (const pkgPath of PACKAGES) {
    try {
      await publishPackage(pkgPath);
    } catch (error) {
      console.error(`[ERROR] Failed to publish ${pkgPath}:`, error);
      process.exit(1);
    }
  }

  console.log("\n✅ All packages published successfully");
}

main();

/**
 * Integration with Changesets workflow:
 * 
 * 1. Developer creates changeset:
 *    $ bunx changeset
 *    or manually create .changeset/my-change.md
 * 
 * 2. Push to main → Changesets action creates PR:
 *    - Runs `bun run ci:version` (bumps versions in package.json)
 *    - Creates "chore: release packages" PR
 * 
 * 3. Merge PR → Changesets action publishes:
 *    - Runs `bun run ci:publish` (THIS SCRIPT)
 *    - Each package: bun pm pack → npm publish <tarball>
 *    - Tarballs have workspace:* resolved to concrete versions
 * 
 * Common issues:
 * - "workspace:* is not a valid version": Using npm publish directly (use this script)
 * - "Version 0.1.0 already published": Forgot to bump version (run changeset version)
 * - "OIDC auth failed": Verify Trusted Publisher config + id-token: write permission
 * - "Cannot find module X": CLI deps must be in dependencies, not devDependencies
 * 
 * Tracking:
 * - Bun native npm OIDC support: https://github.com/oven-sh/bun/issues/15601
 * - When resolved, can replace this with: bun publish --provenance
 */
