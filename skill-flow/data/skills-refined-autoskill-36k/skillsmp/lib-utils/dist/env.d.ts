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
/**
 * Initialize environment from .env.template using 1Password CLI.
 * Safe to use in CI environments where lib-1password may not be installed.
 *
 * @param projectRoot - Directory containing .env.template and .env
 * @param skipIfEnvVars - Skip injection if ALL these env vars are already set
 * @param log - Logger with info/error methods (defaults to console)
 * @returns { parsed: Record<string, string> } - The loaded/skipped env vars
 */
export declare function initEnv(projectRoot: string, skipIfEnvVars?: string[], log?: Log): DotenvConfigOutput;
export {};
