import { beforeEach, describe, expect, mock, test } from 'bun:test';
import type { FileOps } from './claude-md';
import { ClaudeMdHelpers } from './claude-md';

describe('ClaudeMdHelpers', () => {
  beforeEach(() => {
    mock.restore();
  });

  function createMockFileOps(files: Record<string, string> = {}): FileOps {
    return {
      existsSync: mock((path: string) => path in files),
      readFileSync: mock((path: string) => {
        if (path in files) return files[path];
        throw new Error(`File not found: ${path}`);
      }),
      writeFileSync: mock((path: string, content: string) => {
        files[path] = content;
      }),
    };
  }

  describe('getClaudeMdPath', () => {
    test('returns correct path to CLAUDE.md', () => {
      const helpers = new ClaudeMdHelpers();
      expect(helpers.getClaudeMdPath('/project')).toBe('/project/CLAUDE.md');
    });
  });

  describe('getActiveTaskFile', () => {
    test('returns null when CLAUDE.md does not exist', () => {
      const fileOps = createMockFileOps({});
      const helpers = new ClaudeMdHelpers(fileOps);

      expect(helpers.getActiveTaskFile('/project')).toBeNull();
    });

    test('returns null when no active task reference found', () => {
      const fileOps = createMockFileOps({
        '/project/CLAUDE.md': '# Project\n\nNo task reference here',
      });
      const helpers = new ClaudeMdHelpers(fileOps);

      expect(helpers.getActiveTaskFile('/project')).toBeNull();
    });

    test('extracts task ID from spec pattern', () => {
      const fileOps = createMockFileOps({
        '/project/CLAUDE.md': '# Active Task\n@.cc-track/specs/100-feature-name/spec.md\n',
      });
      const helpers = new ClaudeMdHelpers(fileOps);

      expect(helpers.getActiveTaskFile('/project')).toBe('TASK_100');
    });

    test('handles multi-digit task IDs', () => {
      const fileOps = createMockFileOps({
        '/project/CLAUDE.md': '@.cc-track/specs/042-my-feature/spec.md',
      });
      const helpers = new ClaudeMdHelpers(fileOps);

      expect(helpers.getActiveTaskFile('/project')).toBe('TASK_042');
    });

    test('handles single-digit task IDs', () => {
      const fileOps = createMockFileOps({
        '/project/CLAUDE.md': '@.cc-track/specs/001-initial-setup/spec.md',
      });
      const helpers = new ClaudeMdHelpers(fileOps);

      expect(helpers.getActiveTaskFile('/project')).toBe('TASK_001');
    });
  });

  describe('getActiveTaskId', () => {
    test('returns null when no active task file', () => {
      const fileOps = createMockFileOps({});
      const helpers = new ClaudeMdHelpers(fileOps);

      expect(helpers.getActiveTaskId('/project')).toBeNull();
    });

    test('extracts task ID from spec pattern', () => {
      const fileOps = createMockFileOps({
        '/project/CLAUDE.md': '@.cc-track/specs/100-feature-name/spec.md',
      });
      const helpers = new ClaudeMdHelpers(fileOps);

      expect(helpers.getActiveTaskId('/project')).toBe('TASK_100');
    });

    test('extracts multi-digit task IDs', () => {
      const fileOps = createMockFileOps({
        '/project/CLAUDE.md': '@.cc-track/specs/042-my-awesome-feature/spec.md',
      });
      const helpers = new ClaudeMdHelpers(fileOps);

      expect(helpers.getActiveTaskId('/project')).toBe('TASK_042');
    });
  });
});
