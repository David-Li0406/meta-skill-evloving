import { appendFileSync, existsSync, mkdirSync, readdirSync, statSync, unlinkSync } from 'node:fs';
import { homedir, platform } from 'node:os';
import { join } from 'node:path/posix';
import { getLoggingConfig } from './config';

export enum LogLevel {
  ERROR = 0,
  WARN = 1,
  INFO = 2,
  DEBUG = 3,
  TRACE = 4,
}

export interface LogEntry {
  timestamp: string;
  level: string;
  source: string;
  message: string;
  context?: Record<string, unknown>;
  error?: string;
  stack?: string;
}

export interface LogConfig {
  enabled: boolean;
  level: keyof typeof LogLevel;
  retentionDays: number;
  prettyPrint: boolean;
}

// File system operations abstracted for testing
export interface FileSystemOps {
  existsSync: typeof existsSync;
  mkdirSync: typeof mkdirSync;
  appendFileSync: typeof appendFileSync;
  readdirSync: typeof readdirSync;
  statSync: typeof statSync;
  unlinkSync: typeof unlinkSync;
}

const defaultFs: FileSystemOps = {
  existsSync,
  mkdirSync,
  appendFileSync,
  readdirSync,
  statSync,
  unlinkSync,
};

export class Logger {
  private source: string;
  private logDir: string;
  private config: LogConfig;
  private levelValue: number;
  private fs: FileSystemOps;

  constructor(source: string, logDir?: string, config?: LogConfig, fs?: FileSystemOps) {
    this.source = source;
    this.fs = fs || defaultFs;
    this.logDir = logDir || this.findLogDir();
    this.config = config || this.getLogConfig();
    this.levelValue = LogLevel[this.config.level] ?? LogLevel.INFO;

    // Ensure log directory exists
    if (this.config.enabled && !this.fs.existsSync(this.logDir)) {
      this.fs.mkdirSync(this.logDir, { recursive: true });
    }

    // Clean up old logs on initialization
    if (this.config.enabled) {
      this.cleanOldLogs();
    }
  }

  private findLogDir(): string {
    // Get logging config to check for configured directory
    const loggingConfig = getLoggingConfig();

    if (loggingConfig.directory) {
      // Expand tilde to home directory
      return this.expandPath(loggingConfig.directory);
    }

    // Use platform-specific default directory
    return this.getDefaultLogDir();
  }

  private expandPath(path: string): string {
    if (path.startsWith('~')) {
      return join(homedir(), path.slice(1));
    }
    // Expand environment variables (basic support for $HOME)
    return path.replace(/\$HOME/g, homedir());
  }

  private getDefaultLogDir(): string {
    const home = homedir();
    const plat = platform();

    switch (plat) {
      case 'darwin':
        // macOS: ~/Library/Logs/cc-track/
        return join(home, 'Library', 'Logs', 'cc-track');

      case 'win32': {
        // Windows: %LOCALAPPDATA%\cc-track\logs\
        const localAppData = process.env.LOCALAPPDATA || join(home, 'AppData', 'Local');
        return join(localAppData, 'cc-track', 'logs');
      }

      default: {
        // Linux/WSL/Others: Follow XDG Base Directory spec
        const xdgDataHome = process.env.XDG_DATA_HOME || join(home, '.local', 'share');
        return join(xdgDataHome, 'cc-track', 'logs');
      }
    }
  }

  private getLogConfig(): LogConfig {
    // Get logging config from the centralized config system
    const loggingConfig = getLoggingConfig();

    // Convert to LogConfig format used internally
    return {
      enabled: loggingConfig.enabled,
      level: loggingConfig.level,
      retentionDays: loggingConfig.retentionDays,
      prettyPrint: loggingConfig.prettyPrint,
    };
  }

  private cleanOldLogs(): void {
    try {
      const files = this.fs.readdirSync(this.logDir);
      const now = Date.now();
      const retentionMs = this.config.retentionDays * 24 * 60 * 60 * 1000;

      for (const file of files) {
        if (file.endsWith('.jsonl')) {
          const filePath = join(this.logDir, file);
          const stats = this.fs.statSync(filePath);

          if (now - stats.mtimeMs > retentionMs) {
            this.fs.unlinkSync(filePath);
          }
        }
      }
    } catch (_error) {
      // Ignore cleanup errors
    }
  }

  getLogFileName(date?: Date): string {
    const dateStr = (date || new Date()).toISOString().split('T')[0];
    return join(this.logDir, `${dateStr}.jsonl`);
  }

  private writeLog(level: LogLevel, levelName: string, message: string, context?: Record<string, unknown>): void {
    if (!this.config.enabled || level > this.levelValue) {
      return;
    }

    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level: levelName,
      source: this.source,
      message,
    };

    if (context) {
      // Extract error info if present
      if (context.error instanceof Error) {
        entry.error = context.error.message;
        entry.stack = context.error.stack;
        // Remove error from context to avoid circular reference
        const { error: _error, ...restContext } = context;
        if (Object.keys(restContext).length > 0) {
          entry.context = restContext;
        }
      } else {
        entry.context = context;
      }
    }

    try {
      const logFile = this.getLogFileName();
      const logLine = `${JSON.stringify(entry)}\n`;
      this.fs.appendFileSync(logFile, logLine);

      // NEVER output to console - hooks must only return values, not print
      // All logging goes to files only
    } catch (_error) {
      // Fail silently - logging should never break the application
    }
  }

  error(message: string, context?: Record<string, unknown>): void {
    this.writeLog(LogLevel.ERROR, 'ERROR', message, context);
  }

  warn(message: string, context?: Record<string, unknown>): void {
    this.writeLog(LogLevel.WARN, 'WARN', message, context);
  }

  info(message: string, context?: Record<string, unknown>): void {
    this.writeLog(LogLevel.INFO, 'INFO', message, context);
  }

  debug(message: string, context?: Record<string, unknown>): void {
    this.writeLog(LogLevel.DEBUG, 'DEBUG', message, context);
  }

  trace(message: string, context?: Record<string, unknown>): void {
    this.writeLog(LogLevel.TRACE, 'TRACE', message, context);
  }

  // Convenience method for logging errors with stack traces
  exception(message: string, error: Error, context?: Record<string, unknown>): void {
    this.error(message, { ...context, error });
  }
}

// Factory function to create logger instances
export function createLogger(source: string, logDir?: string, config?: LogConfig, fs?: FileSystemOps): Logger {
  return new Logger(source, logDir, config, fs);
}
