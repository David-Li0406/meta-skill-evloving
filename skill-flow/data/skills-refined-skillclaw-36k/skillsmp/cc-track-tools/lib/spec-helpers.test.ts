import { beforeEach, describe, expect, mock, test } from 'bun:test';
import type { SpecFileOperations, SpecMetadata } from './spec-helpers';
import {
  createMetadata,
  createPlanFile,
  createProgressFile,
  createSpecDirectory,
  createSpecFile,
  createTasksFile,
  generateFeatureName,
  getActiveMetadata,
  getActiveSpecDirectory,
  getAllSpecDirectories,
  getNextTaskId,
  getSpecDirectory,
  readMetadata,
  readSpecFile,
  updateMetadata,
  writeSpecFile,
} from './spec-helpers';

describe('spec-helpers', () => {
  beforeEach(() => {
    mock.restore();
  });

  describe('getNextTaskId', () => {
    test('returns 001 when specs directory does not exist', () => {
      const fileOps: SpecFileOperations = {
        existsSync: mock(() => false),
        mkdirSync: mock(() => {}),
        readFileSync: mock(() => ''),
        writeFileSync: mock(() => {}),
      };
      const readDirs = mock(() => []);

      const result = getNextTaskId('/project', fileOps, readDirs);
      expect(result).toBe('001');
    });

    test('returns 001 when specs directory is empty', () => {
      const fileOps: SpecFileOperations = {
        existsSync: mock(() => true),
        mkdirSync: mock(() => {}),
        readFileSync: mock(() => ''),
        writeFileSync: mock(() => {}),
      };
      const readDirs = mock(() => []);

      const result = getNextTaskId('/project', fileOps, readDirs);
      expect(result).toBe('001');
    });

    test('returns next sequential ID when specs exist', () => {
      const fileOps: SpecFileOperations = {
        existsSync: mock(() => true),
        mkdirSync: mock(() => {}),
        readFileSync: mock(() => ''),
        writeFileSync: mock(() => {}),
      };
      const readDirs = mock(() => [
        { name: '001-feature-one', isDirectory: () => true },
        { name: '002-feature-two', isDirectory: () => true },
        { name: '005-feature-five', isDirectory: () => true },
      ]);

      const result = getNextTaskId('/project', fileOps, readDirs);
      expect(result).toBe('006');
    });

    test('ignores directories without numeric prefix', () => {
      const fileOps: SpecFileOperations = {
        existsSync: mock(() => true),
        mkdirSync: mock(() => {}),
        readFileSync: mock(() => ''),
        writeFileSync: mock(() => {}),
      };
      const readDirs = mock(() => [
        { name: '001-feature-one', isDirectory: () => true },
        { name: 'some-other-dir', isDirectory: () => true },
        { name: '002-feature-two', isDirectory: () => true },
      ]);

      const result = getNextTaskId('/project', fileOps, readDirs);
      expect(result).toBe('003');
    });
  });

  describe('createSpecDirectory', () => {
    test('creates specs directory if it does not exist', () => {
      const mkdirSyncCalls: string[] = [];
      const fileOps: SpecFileOperations = {
        existsSync: mock(() => false),
        mkdirSync: mock((path: string) => {
          mkdirSyncCalls.push(path);
        }),
        readFileSync: mock(() => ''),
        writeFileSync: mock(() => {}),
      };

      const result = createSpecDirectory('/project', '001', 'test-feature', fileOps);

      expect(result).toBe('/project/.cc-track/specs/001-test-feature');
      expect(mkdirSyncCalls).toContain('/project/.cc-track/specs');
      expect(mkdirSyncCalls).toContain('/project/.cc-track/specs/001-test-feature');
    });

    test('creates only spec directory if specs directory exists', () => {
      let existsSyncCallCount = 0;
      const mkdirSyncCalls: string[] = [];
      const fileOps: SpecFileOperations = {
        existsSync: mock(() => {
          existsSyncCallCount++;
          return existsSyncCallCount === 1; // First call (specs dir) exists, second (spec dir) doesn't
        }),
        mkdirSync: mock((path: string) => {
          mkdirSyncCalls.push(path);
        }),
        readFileSync: mock(() => ''),
        writeFileSync: mock(() => {}),
      };

      const result = createSpecDirectory('/project', '002', 'another-feature', fileOps);

      expect(result).toBe('/project/.cc-track/specs/002-another-feature');
      expect(mkdirSyncCalls).toHaveLength(1);
      expect(mkdirSyncCalls[0]).toBe('/project/.cc-track/specs/002-another-feature');
    });

    test('returns existing directory if already created', () => {
      const fileOps: SpecFileOperations = {
        existsSync: mock(() => true),
        mkdirSync: mock(() => {}),
        readFileSync: mock(() => ''),
        writeFileSync: mock(() => {}),
      };

      const result = createSpecDirectory('/project', '001', 'test', fileOps);
      expect(result).toBe('/project/.cc-track/specs/001-test');
    });
  });

  describe('createMetadata', () => {
    test('writes metadata as JSON to .metadata.json', () => {
      let writtenPath = '';
      let writtenContent = '';
      const fileOps: SpecFileOperations = {
        existsSync: mock(() => false),
        mkdirSync: mock(() => {}),
        readFileSync: mock(() => ''),
        writeFileSync: mock((path: string, content: string) => {
          writtenPath = path;
          writtenContent = content;
        }),
      };

      const metadata: SpecMetadata = {
        task_id: '001',
        feature_name: 'test-feature',
        branch: 'feature/test-001',
        status: 'in_progress',
        started: '2025-01-01T00:00:00Z',
      };

      createMetadata('/project/.cc-track/specs/001-test', metadata, fileOps);

      expect(writtenPath).toBe('/project/.cc-track/specs/001-test/.metadata.json');
      const parsed = JSON.parse(writtenContent);
      expect(parsed.task_id).toBe('001');
      expect(parsed.feature_name).toBe('test-feature');
      expect(parsed.status).toBe('in_progress');
    });

    test('includes optional github metadata', () => {
      let writtenContent = '';
      const fileOps: SpecFileOperations = {
        existsSync: mock(() => false),
        mkdirSync: mock(() => {}),
        readFileSync: mock(() => ''),
        writeFileSync: mock((_path: string, content: string) => {
          writtenContent = content;
        }),
      };

      const metadata: SpecMetadata = {
        task_id: '002',
        feature_name: 'github-feature',
        branch: 'feature/github-002',
        status: 'in_progress',
        started: '2025-01-01T00:00:00Z',
        github: {
          issue: 42,
          url: 'https://github.com/user/repo/issues/42',
        },
      };

      createMetadata('/spec', metadata, fileOps);

      const parsed = JSON.parse(writtenContent);
      expect(parsed.github.issue).toBe(42);
      expect(parsed.github.url).toBe('https://github.com/user/repo/issues/42');
    });
  });

  describe('readMetadata', () => {
    test('returns null if metadata file does not exist', () => {
      const fileOps: SpecFileOperations = {
        existsSync: mock(() => false),
        mkdirSync: mock(() => {}),
        readFileSync: mock(() => ''),
        writeFileSync: mock(() => {}),
      };

      const result = readMetadata('/project/.cc-track/specs/001-test', fileOps);
      expect(result).toBeNull();
    });

    test('reads and parses metadata JSON', () => {
      const metadata: SpecMetadata = {
        task_id: '001',
        feature_name: 'test',
        branch: 'feature/test-001',
        status: 'completed',
        started: '2025-01-01T00:00:00Z',
        completed: '2025-01-02T00:00:00Z',
      };

      const fileOps: SpecFileOperations = {
        existsSync: mock(() => true),
        mkdirSync: mock(() => {}),
        readFileSync: mock(() => JSON.stringify(metadata)),
        writeFileSync: mock((_path: string, _content: string) => {}),
      };

      const result = readMetadata('/spec', fileOps);
      expect(result).not.toBeNull();
      expect(result?.task_id).toBe('001');
      expect(result?.status).toBe('completed');
      expect(result?.completed).toBe('2025-01-02T00:00:00Z');
    });

    test('returns null on JSON parse error', () => {
      const fileOps: SpecFileOperations = {
        existsSync: mock(() => true),
        mkdirSync: mock(() => {}),
        readFileSync: mock(() => 'invalid json'),
        writeFileSync: mock(() => {}),
      };

      // Suppress expected error output during test
      const consoleErrorSpy = mock(() => {});
      const originalConsoleError = console.error;
      console.error = consoleErrorSpy;

      const result = readMetadata('/spec', fileOps);
      expect(result).toBeNull();

      // Verify error was logged
      expect(consoleErrorSpy).toHaveBeenCalledTimes(1);

      // Restore console.error
      console.error = originalConsoleError;
    });
  });

  describe('updateMetadata', () => {
    test('updates existing metadata with partial updates', () => {
      const originalMetadata: SpecMetadata = {
        task_id: '001',
        feature_name: 'test',
        branch: 'feature/test-001',
        status: 'in_progress',
        started: '2025-01-01T00:00:00Z',
      };

      let writtenContent = '';
      const fileOps: SpecFileOperations = {
        existsSync: mock(() => true),
        mkdirSync: mock(() => {}),
        readFileSync: mock(() => JSON.stringify(originalMetadata)),
        writeFileSync: mock((_path: string, content: string) => {
          writtenContent = content;
        }),
      };

      updateMetadata(
        '/spec',
        {
          status: 'completed',
          completed: '2025-01-05T00:00:00Z',
        },
        fileOps,
      );

      const updated = JSON.parse(writtenContent);
      expect(updated.status).toBe('completed');
      expect(updated.completed).toBe('2025-01-05T00:00:00Z');
      expect(updated.task_id).toBe('001'); // Unchanged
      expect(updated.branch).toBe('feature/test-001'); // Unchanged
    });

    test('throws error if metadata does not exist', () => {
      const fileOps: SpecFileOperations = {
        existsSync: mock(() => false),
        mkdirSync: mock(() => {}),
        readFileSync: mock(() => ''),
        writeFileSync: mock(() => {}),
      };

      expect(() => {
        updateMetadata('/spec', { status: 'completed' }, fileOps);
      }).toThrow('No metadata found');
    });
  });

  describe('getSpecDirectory', () => {
    test('returns null if specs directory does not exist', () => {
      const fileOps: SpecFileOperations = {
        existsSync: mock(() => false),
        mkdirSync: mock(() => {}),
        readFileSync: mock(() => ''),
        writeFileSync: mock(() => {}),
      };
      const readDirs = mock(() => []);

      const result = getSpecDirectory('/project', '001', fileOps, readDirs);
      expect(result).toBeNull();
    });

    test('returns null if no matching directory found', () => {
      const fileOps: SpecFileOperations = {
        existsSync: mock(() => true),
        mkdirSync: mock(() => {}),
        readFileSync: mock(() => ''),
        writeFileSync: mock(() => {}),
      };
      const readDirs = mock(() => [{ name: '002-other-feature', isDirectory: () => true }]);

      const result = getSpecDirectory('/project', '001', fileOps, readDirs);
      expect(result).toBeNull();
    });

    test('returns directory path for matching task ID', () => {
      const fileOps: SpecFileOperations = {
        existsSync: mock(() => true),
        mkdirSync: mock(() => {}),
        readFileSync: mock(() => ''),
        writeFileSync: mock(() => {}),
      };
      const readDirs = mock(() => [
        { name: '001-test-feature', isDirectory: () => true },
        { name: '002-other-feature', isDirectory: () => true },
      ]);

      const result = getSpecDirectory('/project', '001', fileOps, readDirs);
      expect(result).toBe('/project/.cc-track/specs/001-test-feature');
    });
  });

  describe('getActiveSpecDirectory', () => {
    test('returns null if CLAUDE.md does not exist', () => {
      const fileOps: SpecFileOperations = {
        existsSync: mock(() => false),
        mkdirSync: mock(() => {}),
        readFileSync: mock(() => ''),
        writeFileSync: mock(() => {}),
      };

      const result = getActiveSpecDirectory('/project', fileOps);
      expect(result).toBeNull();
    });

    test('returns null if no active task reference found', () => {
      const fileOps: SpecFileOperations = {
        existsSync: mock(() => true),
        mkdirSync: mock(() => {}),
        readFileSync: mock(() => '# Project\n\nNo active task here'),
        writeFileSync: mock(() => {}),
      };

      const result = getActiveSpecDirectory('/project', fileOps);
      expect(result).toBeNull();
    });

    test('extracts active spec directory from CLAUDE.md', () => {
      const claudeMdContent = `# Active Task
@.cc-track/specs/001-test-feature/spec.md

Some other content`;

      const fileOps: SpecFileOperations = {
        existsSync: mock(() => true),
        mkdirSync: mock(() => {}),
        readFileSync: mock(() => claudeMdContent),
        writeFileSync: mock(() => {}),
      };

      const result = getActiveSpecDirectory('/project', fileOps);
      expect(result).toBe('/project/.cc-track/specs/001-test-feature');
    });
  });

  describe('getActiveMetadata', () => {
    test('returns null if no active spec', () => {
      const fileOps: SpecFileOperations = {
        existsSync: mock(() => false),
        mkdirSync: mock(() => {}),
        readFileSync: mock(() => ''),
        writeFileSync: mock(() => {}),
      };

      const result = getActiveMetadata('/project', fileOps);
      expect(result).toBeNull();
    });

    test('returns metadata for active spec', () => {
      const metadata: SpecMetadata = {
        task_id: '001',
        feature_name: 'active-feature',
        branch: 'feature/active-001',
        status: 'in_progress',
        started: '2025-01-01T00:00:00Z',
      };

      let callCount = 0;
      const fileOps: SpecFileOperations = {
        existsSync: mock(() => true),
        mkdirSync: mock(() => {}),
        readFileSync: mock(() => {
          callCount++;
          if (callCount === 1) {
            return '@.cc-track/specs/001-active-feature/spec.md';
          }
          return JSON.stringify(metadata);
        }),
        writeFileSync: mock(() => {}),
      };

      const result = getActiveMetadata('/project', fileOps);
      expect(result).not.toBeNull();
      expect(result?.task_id).toBe('001');
      expect(result?.feature_name).toBe('active-feature');
    });
  });

  describe('file creation helpers', () => {
    test('createSpecFile writes to spec.md', () => {
      let writtenPath = '';
      let writtenContent = '';
      const fileOps: SpecFileOperations = {
        existsSync: mock(() => false),
        mkdirSync: mock(() => {}),
        readFileSync: mock(() => ''),
        writeFileSync: mock((path: string, content: string) => {
          writtenPath = path;
          writtenContent = content;
        }),
      };

      createSpecFile('/spec', 'spec content', fileOps);
      expect(writtenPath).toBe('/spec/spec.md');
      expect(writtenContent).toBe('spec content');
    });

    test('createPlanFile writes to plan.md', () => {
      let writtenPath = '';
      const fileOps: SpecFileOperations = {
        existsSync: mock(() => false),
        mkdirSync: mock(() => {}),
        readFileSync: mock(() => ''),
        writeFileSync: mock((path: string) => {
          writtenPath = path;
        }),
      };

      createPlanFile('/spec', 'plan content', fileOps);
      expect(writtenPath).toBe('/spec/plan.md');
    });

    test('createTasksFile writes to tasks.md', () => {
      let writtenPath = '';
      const fileOps: SpecFileOperations = {
        existsSync: mock(() => false),
        mkdirSync: mock(() => {}),
        readFileSync: mock(() => ''),
        writeFileSync: mock((path: string) => {
          writtenPath = path;
        }),
      };

      createTasksFile('/spec', 'tasks content', fileOps);
      expect(writtenPath).toBe('/spec/tasks.md');
    });

    test('createProgressFile writes to progress.md', () => {
      let writtenPath = '';
      const fileOps: SpecFileOperations = {
        existsSync: mock(() => false),
        mkdirSync: mock(() => {}),
        readFileSync: mock(() => ''),
        writeFileSync: mock((path: string) => {
          writtenPath = path;
        }),
      };

      createProgressFile('/spec', 'progress content', fileOps);
      expect(writtenPath).toBe('/spec/progress.md');
    });
  });

  describe('readSpecFile', () => {
    test('returns null if file does not exist', () => {
      const fileOps: SpecFileOperations = {
        existsSync: mock(() => false),
        mkdirSync: mock(() => {}),
        readFileSync: mock(() => ''),
        writeFileSync: mock(() => {}),
      };

      const result = readSpecFile('/spec', 'nonexistent.md', fileOps);
      expect(result).toBeNull();
    });

    test('reads and returns file content', () => {
      const fileOps: SpecFileOperations = {
        existsSync: mock(() => true),
        mkdirSync: mock(() => {}),
        readFileSync: mock(() => 'file content here'),
        writeFileSync: mock(() => {}),
      };

      const result = readSpecFile('/spec', 'test.md', fileOps);
      expect(result).toBe('file content here');
    });
  });

  describe('writeSpecFile', () => {
    test('writes content to specified file', () => {
      let writtenPath = '';
      let writtenContent = '';
      const fileOps: SpecFileOperations = {
        existsSync: mock(() => false),
        mkdirSync: mock(() => {}),
        readFileSync: mock(() => ''),
        writeFileSync: mock((path: string, content: string) => {
          writtenPath = path;
          writtenContent = content;
        }),
      };

      writeSpecFile('/spec', 'custom.md', 'custom content', fileOps);
      expect(writtenPath).toBe('/spec/custom.md');
      expect(writtenContent).toBe('custom content');
    });
  });

  describe('generateFeatureName', () => {
    test('converts title to lowercase slug', () => {
      expect(generateFeatureName('Add User Authentication')).toBe('add-user-authentication');
    });

    test('removes special characters', () => {
      expect(generateFeatureName('Fix Bug #123: API Error')).toBe('fix-bug-123-api-error');
    });

    test('collapses multiple hyphens', () => {
      expect(generateFeatureName('Fix    Multiple   Spaces')).toBe('fix-multiple-spaces');
    });

    test('removes leading and trailing hyphens', () => {
      expect(generateFeatureName('  Feature Name  ')).toBe('feature-name');
    });

    test('limits length to 50 characters', () => {
      const longTitle = 'This is a very long feature title that should be truncated to fifty characters maximum';
      const result = generateFeatureName(longTitle);
      expect(result.length).toBeLessThanOrEqual(50);
    });

    test('handles empty string', () => {
      expect(generateFeatureName('')).toBe('');
    });

    test('handles string with only special characters', () => {
      expect(generateFeatureName('!@#$%^&*()')).toBe('');
    });
  });

  describe('getAllSpecDirectories', () => {
    test('returns empty array if specs directory does not exist', () => {
      const fileOps: SpecFileOperations = {
        existsSync: mock(() => false),
        mkdirSync: mock(() => {}),
        readFileSync: mock(() => ''),
        writeFileSync: mock(() => {}),
      };
      const readDirs = mock(() => []);

      const result = getAllSpecDirectories('/project', fileOps, readDirs);
      expect(result).toEqual([]);
    });

    test('returns all spec directory paths', () => {
      const fileOps: SpecFileOperations = {
        existsSync: mock(() => true),
        mkdirSync: mock(() => {}),
        readFileSync: mock(() => ''),
        writeFileSync: mock(() => {}),
      };
      const readDirs = mock(() => [
        { name: '001-feature-one', isDirectory: () => true },
        { name: '002-feature-two', isDirectory: () => true },
        { name: 'file.txt', isDirectory: () => false },
      ]);

      const result = getAllSpecDirectories('/project', fileOps, readDirs);
      expect(result).toHaveLength(2);
      expect(result).toContain('/project/.cc-track/specs/001-feature-one');
      expect(result).toContain('/project/.cc-track/specs/002-feature-two');
    });
  });
});
