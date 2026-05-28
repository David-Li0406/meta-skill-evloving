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

type CreateLoggerFn = (name: string) => Logger;

/** Create a console-based stub logger */
function createStubLogger(name: string, parentFields: Record<string, unknown> = {}): Logger {
  const format = (level: string, message: string, fields?: Record<string, unknown>) => {
    const allFields = { ...parentFields, ...fields };
    const fieldsStr = Object.keys(allFields).length > 0 ? ` ${JSON.stringify(allFields)}` : '';
    return `${level} - [${name}] ${message}${fieldsStr}`;
  };

  return {
    debug: (msg, fields) => console.debug(format('debug', msg, fields)),
    info: (msg, fields) => console.info(format('info', msg, fields)),
    warn: (msg, fields) => console.warn(format('warn', msg, fields)),
    error: (msg, fields) => console.error(format('error', msg, fields)),
    child: (fields) => createStubLogger(name, { ...parentFields, ...fields }),
    flush: async () => {},
  };
}

// Lazy-loaded lib-log module. Initialized on first createLogger() call.
// Uses lazy init instead of top-level await for browser build compatibility.
let libLog: { createLogger: CreateLoggerFn } | null = null;
let initPromise: Promise<void> | null = null;

async function ensureInit(): Promise<void> {
  if (libLog) return;
  if (initPromise) return initPromise;

  initPromise = (async () => {
    try {
      // Dynamic string concatenation prevents Rollup from statically analyzing this import
      const libLogModule = '@mdr/' + 'lib-log';
      libLog = await import(/* @vite-ignore */ libLogModule);
    } catch {
      // lib-log not available (CI or missing dep) - use console stub
      console.info('[lib-utils/browser] lib-log not available, using console-only logging');
      libLog = { createLogger: createStubLogger };
    }
  })();

  return initPromise;
}

// Eagerly start initialization (non-blocking)
ensureInit();

/**
 * Create a logger for browser environments.
 * Uses @mdr/lib-log if available (Axiom + console), otherwise console-only.
 *
 * @param name - Logger name (appears in log output, e.g., 'wsh:frontend')
 * @returns Logger instance with debug/info/warn/error/child/flush methods
 */
export function createLogger(name: string): Logger {
  // If lib-log loaded, use it. Otherwise use stub (init still pending or failed).
  if (libLog) {
    return libLog.createLogger(name);
  }
  // Fallback: return stub that will be used until async init completes
  // In practice, init is fast and this rarely executes
  return createStubLogger(name);
}
