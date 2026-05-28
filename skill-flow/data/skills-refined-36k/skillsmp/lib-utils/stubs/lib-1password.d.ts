/**
 * Type stub for @mdr/lib-1password
 * Used when optional dependency is not installed (GitHub Actions typecheck)
 */
declare module '@mdr/lib-1password' {
  import type { DotenvConfigOutput } from 'dotenv';

  interface Log {
    info(msg: string, ...args: unknown[]): void;
    error(msg: string, ...args: unknown[]): void;
  }

  export function initEnv(
    root: string,
    skip?: string[],
    log?: Log
  ): DotenvConfigOutput;
}
