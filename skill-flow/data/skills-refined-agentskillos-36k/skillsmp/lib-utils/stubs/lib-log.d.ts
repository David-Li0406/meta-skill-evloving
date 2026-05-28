/**
 * Type stub for @mdr/lib-log
 * Used when optional dependency is not installed (GitHub Actions typecheck)
 */
declare module '@mdr/lib-log' {
  interface Logger {
    debug(message: string, fields?: Record<string, unknown>): void;
    info(message: string, fields?: Record<string, unknown>): void;
    warn(message: string, fields?: Record<string, unknown>): void;
    error(message: string, fields?: Record<string, unknown>): void;
    child(fields: Record<string, unknown>): Logger;
    flush(): Promise<void>;
  }

  export function createLogger(name: string): Logger;
}
