/**
 * Logger wrapper for lib-log.
 *
 * lib-log is an optional dependency that may not be installed in CI.
 * This wrapper provides graceful degradation:
 * - Development: full Axiom logging via lib-log
 * - CI: console-based stub logger
 * - Missing dep outside CI: fatal error (forces proper setup)
 */
interface Logger {
    debug(message: string, fields?: Record<string, unknown>): void;
    info(message: string, fields?: Record<string, unknown>): void;
    warn(message: string, fields?: Record<string, unknown>): void;
    error(message: string, fields?: Record<string, unknown>): void;
    child(fields: Record<string, unknown>): Logger;
    flush(): Promise<void>;
}
/**
 * Create a logger that uses @mdr/lib-log if available, otherwise falls back to a stub.
 * Safe to use in CI environments where lib-log may not be installed.
 *
 * @param name - Logger name (appears in log output)
 * @returns Logger instance with debug/info/warn/error/child/flush methods
 */
export declare function createLogger(name: string): Logger;
/**
 * Flush all pending logs and reset the shared Axiom client.
 * Call in test teardown to allow clean process exit.
 */
export declare function shutdown(): Promise<void>;
export {};
