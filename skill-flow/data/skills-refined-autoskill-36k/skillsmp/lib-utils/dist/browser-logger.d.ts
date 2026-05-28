/**
 * Browser-compatible logger wrapper for lib-log.
 *
 * lib-log is an optional dependency that provides Axiom cloud logging.
 * This wrapper provides graceful degradation for browsers:
 * - With lib-log: full Axiom logging (lib-log handles browser token via __WSH_CONFIG__)
 * - Without lib-log: console-only fallback (CI environments)
 *
 * Unlike the Node logger.ts, this module:
 * - Uses no Node.js APIs (no process.env, process.argv, process.exit)
 * - Uses lazy initialization (no top-level await for browser compatibility)
 * - Never exits fatally (browsers can't exit)
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
 * Create a logger for browser environments.
 * Uses @mdr/lib-log if available (Axiom + console), otherwise console-only.
 *
 * @param name - Logger name (appears in log output, e.g., 'wsh:frontend')
 * @returns Logger instance with debug/info/warn/error/child/flush methods
 */
export declare function createLogger(name: string): Logger;
export {};
