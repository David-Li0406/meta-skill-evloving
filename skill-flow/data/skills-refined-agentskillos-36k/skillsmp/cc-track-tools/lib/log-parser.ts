import { createReadStream } from 'node:fs';
import { createLogger } from './logger';

// File system operations for dependency injection
export interface FileOps {
  createReadStream: typeof createReadStream;
}

const defaultFileOps: FileOps = {
  createReadStream,
};

// Complete type definition for JSONL log entries
export interface LogEntry {
  type: 'user' | 'assistant' | 'system' | 'summary';
  timestamp: string;
  uuid: string;
  parentUuid?: string | null;
  sessionId?: string;
  cwd?: string;
  version?: string;
  gitBranch?: string;
  userType?: string;
  isSidechain?: boolean;
  isCompactSummary?: boolean;
  isMeta?: boolean;
  isApiErrorMessage?: boolean;
  isVisibleInTranscriptOnly?: boolean;
  leafUuid?: string;
  logicalParentUuid?: string;
  requestId?: string;
  toolUseID?: string;
  toolUseResult?: unknown;
  level?: string;
  subtype?: string;
  content?: string;
  summary?: string;
  compactMetadata?: unknown;
  message?: {
    role: 'user' | 'assistant' | 'system';
    content?: unknown;
    id?: string;
    type?: string;
    model?: string;
    stop_reason?: string | null;
    stop_sequence?: string | null;
    usage?: {
      input_tokens?: number;
      cache_creation_input_tokens?: number;
      cache_read_input_tokens?: number;
      output_tokens?: number;
      service_tier?: string;
    };
  };
}

// Simplified entry for output
export interface SimplifiedEntry {
  timestamp: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  type?: 'message' | 'tool_use' | 'tool_result' | 'system_event';
  success?: boolean;
  metadata?: {
    model?: string;
    tokens?: { input: number; output: number };
    toolName?: string;
    sessionId?: string;
    uuid?: string;
  };
}

// Options for parsing
export interface ParseOptions {
  timeRange?: {
    start?: Date;
    end?: Date;
  };
  role?: 'user' | 'assistant' | 'system' | 'all';
  limit?: number;
  format?: 'json' | 'plaintext';
  includeTools?: boolean;
  simplifyResults?: boolean;
  outputFile?: string;
}

export class ClaudeLogParser {
  private filePath: string;
  private logger: ReturnType<typeof createLogger>;
  private entries: LogEntry[] = [];
  private fileOps: FileOps;

  constructor(filePath: string, fileOps?: FileOps, logger?: ReturnType<typeof createLogger>) {
    this.filePath = filePath;
    this.logger = logger || createLogger('log-parser');
    this.fileOps = fileOps || defaultFileOps;
  }

  /**
   * Parse the log file with the given options
   */
  async parse(options: ParseOptions = {}): Promise<SimplifiedEntry[] | string> {
    // Load all entries from file
    await this.loadEntries();

    // Apply filters
    let filtered = this.entries;

    if (options.timeRange) {
      filtered = this.filterByTimeRange(filtered, options.timeRange);
    }

    if (options.role && options.role !== 'all') {
      filtered = this.filterByRole(filtered, options.role);
    }

    // Simplify entries
    const simplified =
      options.simplifyResults !== false
        ? filtered.map((e) => this.simplifyEntry(e, options.includeTools ?? true))
        : filtered.map((e) => this.convertToSimplified(e));

    // Apply limit
    const limited = options.limit ? simplified.slice(0, options.limit) : simplified;

    // Format output
    if (options.format === 'json') {
      return limited;
    } else {
      return this.formatPlaintext(limited);
    }
  }

  /**
   * Load all entries from the JSONL file
   */
  private async loadEntries(): Promise<void> {
    return new Promise((resolve, reject) => {
      const stream = this.fileOps.createReadStream(this.filePath) as unknown as NodeJS.ReadableStream & {
        setEncoding?: (enc: string) => void;
      };

      try {
        // Ensure we receive strings
        if (typeof stream.setEncoding === 'function') {
          stream.setEncoding('utf8');
        }
      } catch {
        // Non-fatal; continue without forcing encoding
      }

      let buffer = '';

      const processLines = (data?: string) => {
        if (data) buffer += data;
        let idx = buffer.indexOf('\n');
        while (idx !== -1) {
          const rawLine = buffer.slice(0, idx);
          buffer = buffer.slice(idx + 1);
          const line = rawLine.replace(/\r$/, '');
          if (line.length > 0) {
            try {
              const entry = JSON.parse(line) as LogEntry;
              this.entries.push(entry);
            } catch (e) {
              // Skip malformed lines
              this.logger.debug('Skipping malformed line', { error: e });
            }
          }
          idx = buffer.indexOf('\n');
        }
      };

      stream.on('data', (chunk: unknown) => {
        // chunk can be string or Buffer depending on producer
        const data =
          typeof chunk === 'string' ? chunk : Buffer.isBuffer(chunk) ? chunk.toString('utf8') : String(chunk ?? '');
        processLines(data);
      });

      stream.on('end', () => {
        // Process any remaining data without trailing newline
        if (buffer.length > 0) {
          processLines('\n');
        }
        this.logger.info(`Loaded ${this.entries.length} entries from log file`);
        resolve();
      });

      stream.on('error', (error: unknown) => {
        this.logger.error('Error reading log file', { error: (error as Error)?.message ?? String(error) });
        reject(error);
      });
    });
  }

  /**
   * Filter entries by time range
   */
  private filterByTimeRange(entries: LogEntry[], range: { start?: Date; end?: Date }): LogEntry[] {
    return entries.filter((entry) => {
      const timestamp = new Date(entry.timestamp);
      if (range.start && timestamp < range.start) return false;
      if (range.end && timestamp > range.end) return false;
      return true;
    });
  }

  /**
   * Filter entries by role
   */
  private filterByRole(entries: LogEntry[], role: 'user' | 'assistant' | 'system'): LogEntry[] {
    return entries.filter((entry) => {
      if (entry.type === role) return true;
      if (entry.message?.role === role) return true;
      return false;
    });
  }

  /**
   * Convert entry to simplified format without simplification
   */
  private convertToSimplified(entry: LogEntry): SimplifiedEntry {
    const roleRaw = entry.type;
    const role: 'user' | 'assistant' | 'system' =
      roleRaw === 'user' || roleRaw === 'assistant' || roleRaw === 'system' ? roleRaw : 'system';

    return {
      timestamp: entry.timestamp,
      role,
      content: JSON.stringify(entry.message?.content || entry.content || entry.summary || ''),
      type: 'message',
      metadata: {
        sessionId: entry.sessionId,
        uuid: entry.uuid,
        model: entry.message?.model,
      },
    };
  }

  /**
   * Simplify a log entry to extract the essential information
   */
  private simplifyEntry(entry: LogEntry, includeTools: boolean): SimplifiedEntry {
    const roleRaw = entry.type;
    const role: 'user' | 'assistant' | 'system' =
      roleRaw === 'user' || roleRaw === 'assistant' || roleRaw === 'system' ? roleRaw : 'system';

    // Handle system messages
    if (role === 'system') {
      return this.simplifySystemEntry(entry);
    }

    // Handle tool results
    if (entry.toolUseResult) {
      if (!includeTools) {
        // Skip tool results if not including tools
        return {
          timestamp: entry.timestamp,
          role: 'system',
          content: '[Tool result omitted]',
          type: 'tool_result',
        };
      }
      return this.simplifyToolResult(entry);
    }

    // Handle regular messages
    if (entry.message) {
      return this.simplifyMessage(entry, includeTools);
    }

    // Fallback for other types
    return {
      timestamp: entry.timestamp,
      role,
      content: entry.content || entry.summary || '[No content]',
      type: 'message',
      metadata: {
        sessionId: entry.sessionId,
        uuid: entry.uuid,
      },
    };
  }

  /**
   * Simplify system entries
   */
  private simplifySystemEntry(entry: LogEntry): SimplifiedEntry {
    let content = entry.content || '';

    if (entry.subtype === 'compact_boundary') {
      content = '=== Session Compacted ===';
    } else if (entry.subtype === 'informational') {
      // Extract first line or key info
      content = content.split('\n')[0] || 'System message';
    }

    return {
      timestamp: entry.timestamp,
      role: 'system',
      content,
      type: 'system_event',
      metadata: {
        sessionId: entry.sessionId,
        uuid: entry.uuid,
      },
    };
  }

  /**
   * Simplify tool results
   */
  private simplifyToolResult(entry: LogEntry): SimplifiedEntry {
    const result = entry.toolUseResult;
    let content = '';
    let success = true;

    if (typeof result === 'string') {
      content = result.substring(0, 200);
      success = !result.toLowerCase().includes('error');
    } else if (Array.isArray(result) && result[0]?.type === 'text') {
      content = result[0].text?.substring(0, 200) || '[Tool result]';
    } else if (typeof result === 'object' && result !== null) {
      const res = result as { stdout?: string; stderr?: string; output?: string };
      if (res.stdout || res.stderr || res.output) {
        content = (res.stdout || res.stderr || res.output || '').substring(0, 200);
        success = !res.stderr && !content.toLowerCase().includes('error');
      } else {
        content = JSON.stringify(result).substring(0, 200);
      }
    }

    return {
      timestamp: entry.timestamp,
      role: 'system',
      content: `[Result: ${success ? 'success' : 'failure'}] ${content}`,
      type: 'tool_result',
      success,
      metadata: {
        sessionId: entry.sessionId,
        uuid: entry.uuid,
      },
    };
  }

  /**
   * Simplify regular messages
   */
  private simplifyMessage(entry: LogEntry, includeTools: boolean): SimplifiedEntry {
    const message = entry.message || { role: 'unknown' as const, content: '' };
    let content = '';
    let type: 'message' | 'tool_use' = 'message';

    // Extract content based on type
    if (typeof message.content === 'string') {
      content = message.content;
    } else if (Array.isArray(message.content)) {
      const parts: string[] = [];

      for (const item of message.content) {
        if (item.type === 'text' && item.text) {
          parts.push(item.text);
        } else if (item.type === 'tool_use' && item.name) {
          if (!includeTools) {
            parts.push('[Tool use omitted]');
          } else {
            type = 'tool_use';
            const params = item.input ? this.summarizeToolParams(item.input) : '';
            parts.push(`[Tool: ${item.name}(${params})]`);
          }
        }
      }

      content = parts.join(' ');
    } else {
      content = '[Complex content]';
    }

    return {
      timestamp: entry.timestamp,
      role: message.role as 'user' | 'assistant',
      content,
      type,
      metadata: {
        model: 'model' in message ? message.model : undefined,
        tokens:
          'usage' in message && message.usage
            ? {
                input:
                  (message.usage.input_tokens || 0) +
                  (message.usage.cache_creation_input_tokens || 0) +
                  (message.usage.cache_read_input_tokens || 0),
                output: message.usage.output_tokens || 0,
              }
            : undefined,
        sessionId: entry.sessionId,
        uuid: entry.uuid,
      },
    };
  }

  /**
   * Summarize tool parameters for display
   */
  private summarizeToolParams(input: unknown): string {
    if (typeof input === 'string') return input.substring(0, 50);

    if (typeof input === 'object' && input !== null) {
      const params: string[] = [];

      // Extract key parameters
      const obj = input as Record<string, unknown>;
      if (obj.command && typeof obj.command === 'string') params.push(`cmd: "${obj.command.substring(0, 30)}..."`);
      if (obj.file_path && typeof obj.file_path === 'string') params.push(`file: "${obj.file_path}"`);
      if (obj.pattern && typeof obj.pattern === 'string') params.push(`pattern: "${obj.pattern.substring(0, 20)}..."`);
      if (obj.query && typeof obj.query === 'string') params.push(`query: "${obj.query.substring(0, 30)}..."`);

      return params.join(', ');
    }

    return '';
  }

  /**
   * Format entries as plaintext
   */
  private formatPlaintext(entries: SimplifiedEntry[]): string {
    const lines: string[] = [];

    for (const entry of entries) {
      const timestamp = new Date(entry.timestamp).toLocaleString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false,
      });

      const roleSafe = (entry.role || 'system') as 'user' | 'assistant' | 'system';
      const role = roleSafe.charAt(0).toUpperCase() + roleSafe.slice(1);
      const prefix = `[${timestamp}] ${role}:`;

      // Format content with proper indentation for multi-line
      const contentLines = entry.content.split('\n');
      if (contentLines.length === 1) {
        lines.push(`${prefix} ${entry.content}`);
      } else {
        lines.push(`${prefix}`);
        for (const line of contentLines) {
          lines.push(`  ${line}`);
        }
      }

      // Add metadata if relevant
      if (entry.metadata?.model) {
        lines.push(`  (Model: ${entry.metadata.model})`);
      }
      if (entry.metadata?.tokens) {
        lines.push(`  (Tokens: ${entry.metadata.tokens.input} in, ${entry.metadata.tokens.output} out)`);
      }
    }

    return lines.join('\n');
  }
}
