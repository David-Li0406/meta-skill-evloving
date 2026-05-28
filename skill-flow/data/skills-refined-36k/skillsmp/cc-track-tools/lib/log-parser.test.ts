import { afterEach, beforeEach, describe, expect, mock, test } from 'bun:test';
import { Readable } from 'node:stream';
import { createMockLogger } from '../test-utils/command-mocks';
import { ClaudeLogParser, type FileOps, type SimplifiedEntry } from './log-parser';

// Helper to create mock file operations
function createMockFileOps(mockData: Record<string, string[]>): FileOps {
  return {
    createReadStream: mock((path: string) => {
      const lines = mockData[path] || [];
      return Readable.from(lines);
    }),
  };
}

// Test data
const createTestData = () => ({
  '/test/empty.jsonl': [],
  '/test/malformed.jsonl': ['not json\n', '{"valid": "json"}\n', 'also not json\n'],
  '/test/mixed.jsonl': [
    `${JSON.stringify({
      type: 'user',
      timestamp: '2025-01-09T10:00:00Z',
      uuid: 'user-1',
      message: { role: 'user', content: 'Hello Claude' },
    })}\n`,
    `${JSON.stringify({
      type: 'assistant',
      timestamp: '2025-01-09T10:00:05Z',
      uuid: 'assistant-1',
      message: {
        role: 'assistant',
        content: [{ type: 'text', text: 'Hello! How can I help you today?' }],
        model: 'claude-3-opus-20240229',
        usage: { input_tokens: 10, output_tokens: 20 },
      },
    })}\n`,
    `${JSON.stringify({
      type: 'assistant',
      timestamp: '2025-01-09T10:00:10Z',
      uuid: 'assistant-2',
      message: {
        role: 'assistant',
        content: [{ type: 'tool_use', name: 'Bash', id: 'tool-1', input: { command: 'ls -la' } }],
      },
    })}\n`,
    `${JSON.stringify({
      type: 'user',
      timestamp: '2025-01-09T10:00:15Z',
      uuid: 'user-2',
      toolUseResult: { stdout: 'file1.txt\nfile2.txt', stderr: '' },
    })}\n`,
    `${JSON.stringify({
      type: 'system',
      timestamp: '2025-01-09T10:00:20Z',
      uuid: 'system-1',
      subtype: 'compact_boundary',
      content: 'Conversation compacted',
    })}\n`,
    `${JSON.stringify({
      type: 'user',
      timestamp: '2025-01-09T10:00:25Z',
      uuid: 'user-3',
      toolUseResult: 'Error: Command not found',
    })}\n`,
  ],
  '/test/tools.jsonl': [
    `${JSON.stringify({
      type: 'assistant',
      timestamp: '2025-01-09T10:00:00Z',
      uuid: 'test-1',
      message: {
        role: 'assistant',
        content: [
          {
            type: 'tool_use',
            name: 'Read',
            input: { file_path: '/home/user/project/README.md' },
          },
        ],
      },
    })}\n`,
    `${JSON.stringify({
      type: 'assistant',
      timestamp: '2025-01-09T10:00:05Z',
      uuid: 'test-2',
      message: {
        role: 'assistant',
        content: [
          {
            type: 'tool_use',
            name: 'Grep',
            input: {
              pattern: 'function.*export.*async',
              path: '/src',
            },
          },
        ],
      },
    })}\n`,
    `${JSON.stringify({
      type: 'assistant',
      timestamp: '2025-01-09T10:00:10Z',
      uuid: 'test-3',
      message: {
        role: 'assistant',
        content: [
          {
            type: 'tool_use',
            name: 'WebSearch',
            input: {
              query: 'TypeScript best practices for error handling in async functions',
            },
          },
        ],
      },
    })}\n`,
  ],
});

describe('ClaudeLogParser', () => {
  beforeEach(() => {
    mock.restore();
  });

  afterEach(() => {
    mock.restore();
  });

  test('parses empty log file', async () => {
    const testData = createTestData();
    const fileOps = createMockFileOps(testData);
    const logger = createMockLogger();
    const parser = new ClaudeLogParser('/test/empty.jsonl', fileOps, logger);
    const result = await parser.parse({ format: 'json' });

    expect(result).toEqual([]);
  });

  test('handles malformed lines gracefully', async () => {
    const testData = createTestData();
    const fileOps = createMockFileOps(testData);
    const logger = createMockLogger();
    const parser = new ClaudeLogParser('/test/malformed.jsonl', fileOps, logger);
    const result = await parser.parse({ format: 'json' });

    // Should only parse the valid JSON line
    expect(Array.isArray(result)).toBe(true);
  });

  test('parses and simplifies mixed entries', async () => {
    const testData = createTestData();
    const fileOps = createMockFileOps(testData);
    const logger = createMockLogger();
    const parser = new ClaudeLogParser('/test/mixed.jsonl', fileOps, logger);
    const result = (await parser.parse({ format: 'json' })) as SimplifiedEntry[];

    expect(result).toHaveLength(6);

    // Check user message
    expect(result[0]).toEqual({
      timestamp: '2025-01-09T10:00:00Z',
      role: 'user',
      content: 'Hello Claude',
      type: 'message',
      metadata: {
        sessionId: undefined,
        uuid: 'user-1',
      },
    });

    // Check assistant message with model info
    expect(result[1].role).toBe('assistant');
    expect(result[1].content).toBe('Hello! How can I help you today?');
    expect(result[1].metadata?.model).toBe('claude-3-opus-20240229');
    expect(result[1].metadata?.tokens).toEqual({ input: 10, output: 20 });

    // Check tool use
    expect(result[2].content).toContain('[Tool: Bash(cmd: "ls -la...")]');
    expect(result[2].type).toBe('tool_use');

    // Check successful tool result
    expect(result[3].content).toContain('[Result: success]');
    expect(result[3].content).toContain('file1.txt');
    expect(result[3].success).toBe(true);

    // Check system message
    expect(result[4].role).toBe('system');
    expect(result[4].content).toBe('=== Session Compacted ===');
    expect(result[4].type).toBe('system_event');

    // Check error tool result
    expect(result[5].content).toContain('[Result: failure]');
    expect(result[5].content).toContain('Error: Command not found');
    expect(result[5].success).toBe(false);
  });

  test('filters by role', async () => {
    const testData = createTestData();
    const fileOps = createMockFileOps(testData);
    const logger = createMockLogger();
    const parser = new ClaudeLogParser('/test/mixed.jsonl', fileOps, logger);
    const result = (await parser.parse({
      format: 'json',
      role: 'assistant',
    })) as SimplifiedEntry[];

    // Should only return assistant messages
    expect(result).toHaveLength(2);
    expect(result.every((e) => e.role === 'assistant')).toBe(true);
  });

  test('filters by time range', async () => {
    const testData = createTestData();
    const fileOps = createMockFileOps(testData);
    const logger = createMockLogger();
    const parser = new ClaudeLogParser('/test/mixed.jsonl', fileOps, logger);
    const result = (await parser.parse({
      format: 'json',
      timeRange: {
        start: new Date('2025-01-09T10:00:10Z'),
        end: new Date('2025-01-09T10:00:20Z'),
      },
    })) as SimplifiedEntry[];

    // Should return entries between 10:00:10 and 10:00:20
    expect(result).toHaveLength(3); // assistant-2, user-2, system-1
    expect(result[0].timestamp).toBe('2025-01-09T10:00:10Z');
    expect(result[2].timestamp).toBe('2025-01-09T10:00:20Z');
  });

  test('applies limit', async () => {
    const testData = createTestData();
    const fileOps = createMockFileOps(testData);
    const logger = createMockLogger();
    const parser = new ClaudeLogParser('/test/mixed.jsonl', fileOps, logger);
    const result = (await parser.parse({
      format: 'json',
      limit: 3,
    })) as SimplifiedEntry[];

    expect(result).toHaveLength(3);
  });

  test('excludes tools when requested', async () => {
    const testData = createTestData();
    const fileOps = createMockFileOps(testData);
    const logger = createMockLogger();
    const parser = new ClaudeLogParser('/test/mixed.jsonl', fileOps, logger);
    const result = (await parser.parse({
      format: 'json',
      includeTools: false,
    })) as SimplifiedEntry[];

    // Tool use should be marked as omitted
    expect(result[2].content).toBe('[Tool use omitted]');
    // Tool result should be marked as omitted
    expect(result[3].content).toBe('[Tool result omitted]');
    expect(result[5].content).toBe('[Tool result omitted]');
  });

  test('formats as plaintext', async () => {
    const testData = createTestData();
    const fileOps = createMockFileOps(testData);
    const logger = createMockLogger();
    const parser = new ClaudeLogParser('/test/mixed.jsonl', fileOps, logger);
    const result = (await parser.parse({
      format: 'plaintext',
      limit: 2,
    })) as string;

    expect(typeof result).toBe('string');
    expect(result).toContain('[01/09/2025, 10:00:00] User: Hello Claude');
    expect(result).toContain('[01/09/2025, 10:00:05] Assistant:');
    expect(result).toContain('Hello! How can I help you today?');
    expect(result).toContain('(Model: claude-3-opus-20240229)');
    expect(result).toContain('(Tokens: 10 in, 20 out)');
  });

  test('returns raw entries when simplifyResults is false', async () => {
    const testData = createTestData();
    const fileOps = createMockFileOps(testData);
    const logger = createMockLogger();
    const parser = new ClaudeLogParser('/test/mixed.jsonl', fileOps, logger);
    const result = (await parser.parse({
      format: 'json',
      simplifyResults: false,
      limit: 1,
    })) as SimplifiedEntry[];

    expect(result).toHaveLength(1);
    // Raw content should be JSON stringified
    expect(result[0].content).toBe('"Hello Claude"');
  });
});

describe('ClaudeLogParser - Tool Parameter Summarization', () => {
  test('summarizes various tool parameters', async () => {
    const testData = createTestData();
    const fileOps = createMockFileOps(testData);
    const logger = createMockLogger();
    const parser = new ClaudeLogParser('/test/tools.jsonl', fileOps, logger);
    const result = (await parser.parse({ format: 'json' })) as SimplifiedEntry[];

    expect(result).toHaveLength(3);
    expect(result[0].content).toBe('[Tool: Read(file: "/home/user/project/README.md")]');
    expect(result[1].content).toContain('[Tool: Grep(pattern: "function.*export.*as');
    expect(result[2].content).toContain('[Tool: WebSearch(query: "TypeScript best practices for');
  });
});
