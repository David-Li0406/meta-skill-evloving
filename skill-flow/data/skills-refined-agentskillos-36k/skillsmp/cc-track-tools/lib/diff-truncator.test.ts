import { describe, expect, test } from 'bun:test';
import { truncateGitDiff } from './diff-truncator';

describe('truncateGitDiff', () => {
  test('returns original diff when under size limit', () => {
    const diff = 'diff --git a/file.txt b/file.txt\n+added line\n-removed line';
    const result = truncateGitDiff(diff, 1000);

    expect(result.truncated).toBe(false);
    expect(result.diff).toBe(diff);
    expect(result.originalSize).toBe(diff.length);
    expect(result.filesOmitted).toBe(0);
  });

  test('truncates at file boundaries when multiple files', () => {
    const smallFile = `diff --git a/file1.txt b/file1.txt
+line 1`;
    const largeFile = `
diff --git a/file2.txt b/file2.txt
+${'long line '.repeat(50)}`;
    const diff = smallFile + largeFile;

    const result = truncateGitDiff(diff, smallFile.length + 150); // Include first file but not second

    expect(result.truncated).toBe(true);
    expect(result.diff).toContain('file1.txt');
    expect(result.diff).not.toContain('long line');
    expect(result.filesOmitted).toBe(1);
    expect(result.diff).toContain('omitted due to size limit');
  });

  test('truncates single large file', () => {
    const diff = `diff --git a/large.txt b/large.txt
+${'very long line '.repeat(100)}`;

    const result = truncateGitDiff(diff, 50);

    expect(result.truncated).toBe(true);
    expect(result.diff.length).toBeLessThan(diff.length);
    expect(result.diff).toContain('truncated due to size limit');
  });

  test('handles diff without file headers', () => {
    const diff = `+added line\n-removed line\n${'x'.repeat(1000)}`;
    const result = truncateGitDiff(diff, 100);

    expect(result.truncated).toBe(true);
    expect(result.diff).toContain('truncated due to size limit');
    expect(result.filesOmitted).toBe(0);
  });
});
