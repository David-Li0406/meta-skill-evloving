import { beforeEach, describe, expect, mock, spyOn, test } from 'bun:test';
import * as os from 'node:os';
import * as configModule from './config';
import type { FileSystemOps, LogConfig, LogEntry } from './logger';
import { createLogger, Logger } from './logger';

describe('Logger', () => {
  let mockFs: FileSystemOps;
  let appendedLines: string[] = [];
  let createdDirs: string[] = [];

  beforeEach(() => {
    appendedLines = [];
    createdDirs = [];

    mockFs = {
      existsSync: mock((_path: string) => false),
      mkdirSync: mock((path: string, _options?: { recursive?: boolean }) => {
        createdDirs.push(path);
      }),
      appendFileSync: mock((_path: string, data: string) => {
        appendedLines.push(data);
      }),
      readdirSync: mock(() => []),
      statSync: mock(() => ({ mtimeMs: Date.now() })),
      unlinkSync: mock(() => {}),
    };
  });

  describe('constructor', () => {
    test("creates log directory if it doesn't exist", () => {
      const config: LogConfig = {
        enabled: true,
        level: 'INFO',
        retentionDays: 7,
        prettyPrint: false,
      };

      new Logger('test', '/tmp/logs', config, mockFs);

      expect(createdDirs).toContain('/tmp/logs');
    });

    test("doesn't create directory when logging disabled", () => {
      const config: LogConfig = {
        enabled: false,
        level: 'INFO',
        retentionDays: 7,
        prettyPrint: false,
      };

      new Logger('test', '/tmp/logs', config, mockFs);

      expect(createdDirs).toHaveLength(0);
    });
  });

  describe('log levels', () => {
    test('respects log level filtering', () => {
      const config: LogConfig = {
        enabled: true,
        level: 'WARN',
        retentionDays: 7,
        prettyPrint: false,
      };

      const logger = new Logger('test', '/tmp/logs', config, mockFs);

      logger.debug('debug message');
      logger.info('info message');
      logger.warn('warn message');
      logger.error('error message');

      // Only WARN and ERROR should be logged
      expect(appendedLines).toHaveLength(2);
      expect(appendedLines[0]).toContain('warn message');
      expect(appendedLines[1]).toContain('error message');
    });

    test('logs all levels when set to TRACE', () => {
      const config: LogConfig = {
        enabled: true,
        level: 'TRACE',
        retentionDays: 7,
        prettyPrint: false,
      };

      const logger = new Logger('test', '/tmp/logs', config, mockFs);

      logger.error('error');
      logger.warn('warn');
      logger.info('info');
      logger.debug('debug');
      logger.trace('trace');

      expect(appendedLines).toHaveLength(5);
    });
  });

  describe('log entry format', () => {
    test('creates proper log entry structure', () => {
      const config: LogConfig = {
        enabled: true,
        level: 'INFO',
        retentionDays: 7,
        prettyPrint: false,
      };

      const logger = new Logger('test-source', '/tmp/logs', config, mockFs);
      logger.info('test message', { key: 'value' });

      expect(appendedLines).toHaveLength(1);
      const entry: LogEntry = JSON.parse(appendedLines[0].trim());

      expect(entry.level).toBe('INFO');
      expect(entry.source).toBe('test-source');
      expect(entry.message).toBe('test message');
      expect(entry.context).toEqual({ key: 'value' });
      expect(entry.timestamp).toBeDefined();
    });

    test('handles error objects properly', () => {
      const config: LogConfig = {
        enabled: true,
        level: 'ERROR',
        retentionDays: 7,
        prettyPrint: false,
      };

      const logger = new Logger('test', '/tmp/logs', config, mockFs);
      const error = new Error('test error');
      logger.exception('Something went wrong', error);

      expect(appendedLines).toHaveLength(1);
      const entry: LogEntry = JSON.parse(appendedLines[0].trim());

      expect(entry.error).toBe('test error');
      expect(entry.stack).toBeDefined();
    });
  });

  describe('getLogFileName', () => {
    test('generates correct log file name', () => {
      const config: LogConfig = {
        enabled: true,
        level: 'INFO',
        retentionDays: 7,
        prettyPrint: false,
      };

      const logger = new Logger('test', '/tmp/logs', config, mockFs);
      const testDate = new Date('2025-01-15T12:00:00Z');
      const fileName = logger.getLogFileName(testDate);

      expect(fileName).toBe('/tmp/logs/2025-01-15.jsonl');
    });
  });

  describe('log cleanup', () => {
    test('removes old log files on initialization', () => {
      const oldFileTime = Date.now() - 8 * 24 * 60 * 60 * 1000; // 8 days old
      const newFileTime = Date.now() - 1 * 24 * 60 * 60 * 1000; // 1 day old

      const mockFsWithFiles: FileSystemOps = {
        ...mockFs,
        readdirSync: mock(() => ['2025-01-01.jsonl', '2025-01-10.jsonl']),
        statSync: mock((path: string) => ({
          mtimeMs: path.includes('2025-01-01') ? oldFileTime : newFileTime,
        })),
      };

      const config: LogConfig = {
        enabled: true,
        level: 'INFO',
        retentionDays: 7,
        prettyPrint: false,
      };

      const unlinkedFiles: string[] = [];
      mockFsWithFiles.unlinkSync = mock((path: string) => {
        unlinkedFiles.push(path);
      });

      new Logger('test', '/tmp/logs', config, mockFsWithFiles);

      // Only the old file should be deleted
      expect(unlinkedFiles).toHaveLength(1);
      expect(unlinkedFiles[0]).toContain('2025-01-01.jsonl');
    });
  });

  describe('createLogger factory', () => {
    test('creates logger instance', () => {
      const config: LogConfig = {
        enabled: true,
        level: 'INFO',
        retentionDays: 7,
        prettyPrint: false,
      };

      const logger = createLogger('test', '/tmp/logs', config, mockFs);

      expect(logger).toBeInstanceOf(Logger);

      logger.info('test');
      expect(appendedLines).toHaveLength(1);
    });
  });

  describe('disabled logging', () => {
    test("doesn't write logs when disabled", () => {
      const config: LogConfig = {
        enabled: false,
        level: 'INFO',
        retentionDays: 7,
        prettyPrint: false,
      };

      const logger = new Logger('test', '/tmp/logs', config, mockFs);

      logger.info('test message');
      logger.error('error message');

      expect(appendedLines).toHaveLength(0);
    });
  });

  describe('platform-specific log directories', () => {
    test('uses configured directory when provided', () => {
      const mockGetLoggingConfig = spyOn(configModule, 'getLoggingConfig');
      mockGetLoggingConfig.mockReturnValue({
        enabled: true,
        level: 'INFO',
        retentionDays: 7,
        prettyPrint: false,
        directory: '/custom/log/path',
      });

      const logger = new Logger('test', undefined, undefined, mockFs);
      const fileName = logger.getLogFileName();

      expect(fileName).toContain('/custom/log/path');
      mockGetLoggingConfig.mockRestore();
    });

    test('expands tilde in configured path', () => {
      const mockGetLoggingConfig = spyOn(configModule, 'getLoggingConfig');
      const mockHomedir = spyOn(os, 'homedir');
      mockHomedir.mockReturnValue('/home/testuser');

      mockGetLoggingConfig.mockReturnValue({
        enabled: true,
        level: 'INFO',
        retentionDays: 7,
        prettyPrint: false,
        directory: '~/.local/share/cc-track/logs',
      });

      const logger = new Logger('test', undefined, undefined, mockFs);
      const fileName = logger.getLogFileName();

      expect(fileName).toContain('/home/testuser/.local/share/cc-track/logs');

      mockGetLoggingConfig.mockRestore();
      mockHomedir.mockRestore();
    });

    test('uses Linux default when platform is linux', () => {
      const mockGetLoggingConfig = spyOn(configModule, 'getLoggingConfig');
      const mockPlatform = spyOn(os, 'platform');
      const mockHomedir = spyOn(os, 'homedir');

      mockGetLoggingConfig.mockReturnValue({
        enabled: true,
        level: 'INFO',
        retentionDays: 7,
        prettyPrint: false,
      });
      mockPlatform.mockReturnValue('linux');
      mockHomedir.mockReturnValue('/home/testuser');

      const logger = new Logger('test', undefined, undefined, mockFs);
      const fileName = logger.getLogFileName();

      expect(fileName).toContain('/home/testuser/.local/share/cc-track/logs');

      mockGetLoggingConfig.mockRestore();
      mockPlatform.mockRestore();
      mockHomedir.mockRestore();
    });

    test('uses macOS default when platform is darwin', () => {
      const mockGetLoggingConfig = spyOn(configModule, 'getLoggingConfig');
      const mockPlatform = spyOn(os, 'platform');
      const mockHomedir = spyOn(os, 'homedir');

      mockGetLoggingConfig.mockReturnValue({
        enabled: true,
        level: 'INFO',
        retentionDays: 7,
        prettyPrint: false,
      });
      mockPlatform.mockReturnValue('darwin');
      mockHomedir.mockReturnValue('/Users/testuser');

      const logger = new Logger('test', undefined, undefined, mockFs);
      const fileName = logger.getLogFileName();

      expect(fileName).toContain('/Users/testuser/Library/Logs/cc-track');

      mockGetLoggingConfig.mockRestore();
      mockPlatform.mockRestore();
      mockHomedir.mockRestore();
    });

    test('uses Windows default when platform is win32', () => {
      const mockGetLoggingConfig = spyOn(configModule, 'getLoggingConfig');
      const mockPlatform = spyOn(os, 'platform');
      const mockHomedir = spyOn(os, 'homedir');

      mockGetLoggingConfig.mockReturnValue({
        enabled: true,
        level: 'INFO',
        retentionDays: 7,
        prettyPrint: false,
      });
      mockPlatform.mockReturnValue('win32');
      mockHomedir.mockReturnValue('C:\\Users\\testuser');
      process.env.LOCALAPPDATA = 'C:\\Users\\testuser\\AppData\\Local';

      const logger = new Logger('test', undefined, undefined, mockFs);
      const fileName = logger.getLogFileName();

      expect(fileName).toContain('cc-track');

      delete process.env.LOCALAPPDATA;
      mockGetLoggingConfig.mockRestore();
      mockPlatform.mockRestore();
      mockHomedir.mockRestore();
    });
  });
});
