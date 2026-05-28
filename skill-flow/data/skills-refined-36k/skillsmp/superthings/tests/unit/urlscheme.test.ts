import { describe, it, expect, jest, beforeEach } from '@jest/globals';

// Mock child_process.exec to prevent real execution
const mockExec = jest.fn<(cmd: string, opts: unknown, callback: (error: Error | null, result: { stdout: string; stderr: string }) => void) => void>();

jest.unstable_mockModule('child_process', () => ({
  exec: mockExec
}));

// Dynamic import after mocking
const { executeThingsURL, executeThingsJSON } = await import('../../src/lib/urlscheme.js');

describe('executeThingsURL', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    // Default: exec succeeds
    mockExec.mockImplementation((cmd, opts, callback) => {
      if (typeof opts === 'function') {
        opts(null, { stdout: '', stderr: '' });
      } else {
        callback(null, { stdout: '', stderr: '' });
      }
    });
  });

  // Helper to extract URL from exec call
  function getLastURL(): string {
    const call = mockExec.mock.calls[mockExec.mock.calls.length - 1];
    const cmd = call[0] as string;
    const match = cmd.match(/open "(.+?)"/);
    return match ? match[1] : '';
  }

  describe('URL construction', () => {
    it('should handle arrays with special handling', async () => {
      const params = {
        tags: ['work', 'urgent'],
        checklist_items: ['Item 1', 'Item 2'],
        todos: ['Todo 1', 'Todo 2'],
        filter: ['tag1', 'tag2']
      };

      await executeThingsURL('add', params);
      const url = getLastURL();

      expect(url).toContain('tags=work%2Curgent');
      expect(url).toContain('checklist-items=Item%201%0AItem%202');
      expect(url).toContain('to-dos=Todo%201%0ATodo%202');
      expect(url).toContain('filter=tag1%2Ctag2');
    });

    it('should skip empty arrays', async () => {
      await executeThingsURL('add', {
        title: 'Test',
        tags: []
      });
      const url = getLastURL();

      expect(url).toContain('title=Test');
      expect(url).not.toContain('tags=');
    });

    it('should handle boolean values', async () => {
      await executeThingsURL('add', {
        completed: true,
        canceled: false
      });
      const url = getLastURL();

      expect(url).toContain('completed=true');
      expect(url).toContain('canceled=false');
    });

    it('should convert snake_case to kebab-case', async () => {
      await executeThingsURL('add', {
        list_id: 'project-123',
        area_id: 'area-456',
        some_other_field: 'value'
      });
      const url = getLastURL();

      expect(url).toContain('list-id=project-123');
      expect(url).toContain('area-id=area-456');
      expect(url).toContain('some-other-field=value');
    });

    it('should skip null and undefined values', async () => {
      await executeThingsURL('add', {
        title: 'Test',
        notes: undefined,
        when: null,
        deadline: ''
      });
      const url = getLastURL();

      expect(url).toContain('title=Test');
      expect(url).toContain('deadline=');
      expect(url).not.toContain('notes=');
      expect(url).not.toContain('when=');
    });

    it('should properly encode special characters', async () => {
      await executeThingsURL('add', {
        title: 'Test & Task',
        notes: 'Line 1\nLine 2',
        tags: ['tag with spaces', 'tag/slash']
      });
      const url = getLastURL();

      expect(url).toContain('title=Test%20%26%20Task');
      expect(url).toContain('notes=Line%201%0ALine%202');
      expect(url).toContain('tags=tag%20with%20spaces%2Ctag%2Fslash');
    });

    it('should sanitize control characters', async () => {
      await executeThingsURL('add', {
        title: 'Test\x00Task\x1FClean'
      });
      const url = getLastURL();

      expect(url).toContain('title=TestTaskClean');
      expect(url).not.toContain('\x00');
      expect(url).not.toContain('\x1F');
    });
  });

  describe('error handling', () => {
    it('should throw on execution failure', async () => {
      mockExec.mockImplementation((cmd, opts, callback) => {
        if (typeof opts === 'function') {
          opts(new Error('exec failed'), { stdout: '', stderr: '' });
        } else {
          callback(new Error('exec failed'), { stdout: '', stderr: '' });
        }
      });

      await expect(executeThingsURL('add', { title: 'Test' }))
        .rejects.toMatchObject({ code: 'URL_EXECUTION_FAILED' });
    });
  });

  describe('authentication', () => {
    const originalEnv = process.env;

    beforeEach(() => {
      process.env = { ...originalEnv };
    });

    afterEach(() => {
      process.env = originalEnv;
    });

    it('should not require auth token for json commands without update operations', async () => {
      delete process.env.THINGS_AUTH_TOKEN;

      // Mock exec to fail so we can verify no auth error is thrown
      mockExec.mockImplementation((cmd, opts, callback) => {
        if (typeof opts === 'function') {
          opts(new Error('exec failed'), { stdout: '', stderr: '' });
        } else {
          callback(new Error('exec failed'), { stdout: '', stderr: '' });
        }
      });

      try {
        await executeThingsJSON([{ type: 'to-do', attributes: { title: 'test' } }]);
      } catch (error: any) {
        expect(error.code).toBe('JSON_EXECUTION_FAILED');
        expect(error.message).not.toContain('THINGS_AUTH_TOKEN');
      }
    });

    it('should not require auth token for other commands', async () => {
      delete process.env.THINGS_AUTH_TOKEN;

      mockExec.mockImplementation((cmd, opts, callback) => {
        if (typeof opts === 'function') {
          opts(new Error('exec failed'), { stdout: '', stderr: '' });
        } else {
          callback(new Error('exec failed'), { stdout: '', stderr: '' });
        }
      });

      try {
        await executeThingsURL('add', { title: 'Test' });
      } catch (error: any) {
        expect(error.code).toBe('URL_EXECUTION_FAILED');
        expect(error.message).not.toContain('THINGS_AUTH_TOKEN');
      }
    });
  });
});
