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

// Type matches lib-log's createLogger signature
type CreateLoggerFn = (name: string) => Logger;

/** Create a console-based stub logger for CI environments */
function createStubLogger(name: string, parentFields: Record<string, unknown> = {}): Logger {
  const format = (level: string, message: string, fields?: Record<string, unknown>) => {
    const allFields = { ...parentFields, ...fields };
    const fieldsStr = Object.keys(allFields).length > 0 ? ` ${JSON.stringify(allFields)}` : '';
    return `${level} - [${name}] ${message}${fieldsStr}`;
  };

  return {
    debug: (msg, fields) => console.log(format('debug', msg, fields)),
    info: (msg, fields) => console.log(format('info', msg, fields)),
    warn: (msg, fields) => console.warn(format('warn', msg, fields)),
    error: (msg, fields) => console.error(format('error', msg, fields)),
    child: (fields) => createStubLogger(name, { ...parentFields, ...fields }),
    flush: async () => {},
  };
}

// Try to load lib-log at module init. Will be either:
// - The real lib-log module (normal case)
// - A stub creator function (CI case)
// - Never assigned (non-CI failure → process.exit before reaching here)
let libLog: { createLogger: CreateLoggerFn; shutdown?: () => Promise<void> };
try {
  libLog = await import('@mdr/lib-log');
} catch {
  const caller = process.argv[1] || 'unknown';
  if (process.env.CI) {
    // CI: lib-log not needed, use console-based stub
    console.log(`[lib-utils] lib-log not available, using stub (caller: ${caller})`);
    libLog = { createLogger: createStubLogger };
  } else {
    // Development: lib-log is required, fail loudly
    console.error(
      `[lib-utils] FATAL: lib-log not available.\n` +
        `Add to optionalDependencies:\n` +
        `  "@mdr/lib-log": "file:../lib-log"\n` +
        `Then run: bun install\n` +
        `(caller: ${caller})`
    );
    process.exit(1);
  }
}

/**
 * Create a logger that uses @mdr/lib-log if available, otherwise falls back to a stub.
 * Safe to use in CI environments where lib-log may not be installed.
 *
 * @param name - Logger name (appears in log output)
 * @returns Logger instance with debug/info/warn/error/child/flush methods
 */
export function createLogger(name: string): Logger {
  return libLog.createLogger(name);
}

/**
 * Flush all pending logs and reset the shared Axiom client.
 * Call in test teardown to allow clean process exit.
 */
export async function shutdown(): Promise<void> {
  if (libLog.shutdown) {
    await libLog.shutdown();
  }
}
