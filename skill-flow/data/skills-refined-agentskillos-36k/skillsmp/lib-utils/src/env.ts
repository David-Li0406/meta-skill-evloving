/**
 * Environment initialization wrapper for lib-1password.
 *
 * lib-1password is an optional dependency that may not be installed in CI.
 * This wrapper provides graceful degradation:
 * - Development: delegates to lib-1password for 1Password injection
 * - CI: returns empty stub (no secrets needed in CI)
 * - Missing dep outside CI: fatal error (forces proper setup)
 */

import type { DotenvConfigOutput } from 'dotenv';

/** Logger interface - console and lib-log Logger both satisfy this */
interface Log {
  info(msg: string, ...args: unknown[]): void;
  error(msg: string, ...args: unknown[]): void;
}

// Type matches lib-1password's initEnv signature
type InitEnvFn = (root: string, skip: string[], log: Log) => DotenvConfigOutput;

// Try to load lib-1password at module init. Will be either:
// - The real lib-1password module (normal case)
// - A stub that returns empty parsed object (CI case)
// - Never assigned (non-CI failure → process.exit before reaching here)
let lib1p: { initEnv: InitEnvFn };
try {
  lib1p = await import('@mdr/lib-1password');
} catch {
  const caller = process.argv[1] || 'unknown';
  if (process.env.CI) {
    // CI: lib-1password not needed, use stub that returns empty result
    console.log(`[lib-utils] lib-1password not available, using stub (caller: ${caller})`);
    lib1p = { initEnv: () => ({ parsed: {} }) };
  } else {
    // Development: lib-1password is required, fail loudly
    console.error(
      `[lib-utils] FATAL: lib-1password not available.\n` +
        `Add to optionalDependencies:\n` +
        `  "@mdr/lib-1password": "file:../lib-1password"\n` +
        `Then run: bun install\n` +
        `(caller: ${caller})`
    );
    process.exit(1);
  }
}

/**
 * Initialize environment from .env.template using 1Password CLI.
 * Safe to use in CI environments where lib-1password may not be installed.
 *
 * @param projectRoot - Directory containing .env.template and .env
 * @param skipIfEnvVars - Skip injection if ALL these env vars are already set
 * @param log - Logger with info/error methods (defaults to console)
 * @returns { parsed: Record<string, string> } - The loaded/skipped env vars
 */
export function initEnv(projectRoot: string, skipIfEnvVars: string[] = [], log: Log = console): DotenvConfigOutput {
  return lib1p.initEnv(projectRoot, skipIfEnvVars, log);
}
