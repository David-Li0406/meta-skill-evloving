// ABOUTME: Tests for npm package detection, Bun verification, and plugin dependency checking
// ABOUTME: Ensures clean plugin installation by detecting conflicts and missing requirements

import { describe, expect, mock, test } from 'bun:test';
import { detectNpmPackage, verifyBunInstalled, verifyPluginDependencies } from './detection';

describe('detectNpmPackage', () => {
  // Helper to check for platform-appropriate find command
  const isFindCommand = (cmd: string) => cmd === 'which cc-track' || cmd === 'where cc-track';

  test('detects npm package via which/where command', () => {
    const mockExec = mock((cmd: string) => {
      if (isFindCommand(cmd)) {
        return '/usr/local/bin/cc-track\n';
      }
      return '';
    });

    const result = detectNpmPackage(mockExec);

    expect(result.detected).toBe(true);
    expect(result.message).toContain('/usr/local/bin/cc-track');
  });

  test('detects npm package via npm list', () => {
    const mockExec = mock((cmd: string) => {
      if (isFindCommand(cmd)) {
        throw new Error('not found');
      }
      if (cmd === 'npm list -g cc-track --depth=0') {
        return 'cc-track@2.10.0\n';
      }
      return '';
    });

    const result = detectNpmPackage(mockExec);

    expect(result.detected).toBe(true);
    expect(result.message).toContain('global npm packages');
  });

  test('returns not detected when neither which/where nor npm list find package', () => {
    const mockExec = mock(() => {
      throw new Error('not found');
    });

    const result = detectNpmPackage(mockExec);

    expect(result.detected).toBe(false);
    expect(result.message).toBeUndefined();
  });

  test('handles which/where command returning empty string', () => {
    const mockExec = mock((cmd: string) => {
      if (isFindCommand(cmd)) {
        return '';
      }
      if (cmd === 'npm list -g cc-track --depth=0') {
        throw new Error('not found');
      }
      return '';
    });

    const result = detectNpmPackage(mockExec);

    expect(result.detected).toBe(false);
  });

  test('handles npm list not containing cc-track', () => {
    const mockExec = mock((cmd: string) => {
      if (isFindCommand(cmd)) {
        throw new Error('not found');
      }
      if (cmd === 'npm list -g cc-track --depth=0') {
        return 'other-package@1.0.0\n';
      }
      return '';
    });

    const result = detectNpmPackage(mockExec);

    expect(result.detected).toBe(false);
  });
});

describe('verifyBunInstalled', () => {
  test('detects Bun when installed', () => {
    const mockExec = mock((cmd: string) => {
      if (cmd === 'bun --version') {
        return '1.0.15\n';
      }
      return '';
    });

    const result = verifyBunInstalled(mockExec);

    expect(result.detected).toBe(true);
    expect(result.message).toContain('Bun v1.0.15');
  });

  test('returns not detected when Bun not installed', () => {
    const mockExec = mock(() => {
      throw new Error('command not found: bun');
    });

    const result = verifyBunInstalled(mockExec);

    expect(result.detected).toBe(false);
    expect(result.message).toContain('not found in PATH');
  });

  test('handles empty version string', () => {
    const mockExec = mock((cmd: string) => {
      if (cmd === 'bun --version') {
        return '';
      }
      return '';
    });

    const result = verifyBunInstalled(mockExec);

    expect(result.detected).toBe(false);
    expect(result.message).toBe('Bun check failed');
  });

  test('trims whitespace from version', () => {
    const mockExec = mock((cmd: string) => {
      if (cmd === 'bun --version') {
        return '  1.0.20  \n';
      }
      return '';
    });

    const result = verifyBunInstalled(mockExec);

    expect(result.detected).toBe(true);
    expect(result.message).toContain('Bun v1.0.20');
  });
});

describe('verifyPluginDependencies', () => {
  test('detects all dependencies when present', () => {
    const mockFs = mock((path: string) => {
      return path.includes('node_modules');
    });

    const result = verifyPluginDependencies('/plugin/root', mockFs);

    expect(result.detected).toBe(true);
    expect(result.message).toContain('All plugin dependencies are installed');
  });

  test('detects missing node_modules directory', () => {
    const mockFs = mock((path: string) => {
      return !path.includes('node_modules');
    });

    const result = verifyPluginDependencies('/plugin/root', mockFs);

    expect(result.detected).toBe(false);
    expect(result.message).toContain('node_modules not found');
    expect(result.message).toContain('/plugin/root/node_modules');
  });

  test('detects missing @anthropic-ai/claude-agent-sdk', () => {
    const mockFs = mock((path: string) => {
      if (path.endsWith('node_modules')) {
        return true;
      }
      if (path.includes('claude-agent-sdk')) {
        return false;
      }
      return true;
    });

    const result = verifyPluginDependencies('/plugin/root', mockFs);

    expect(result.detected).toBe(false);
    expect(result.message).toContain('Missing dependencies');
    expect(result.message).toContain('@anthropic-ai/claude-agent-sdk');
  });

  test('detects missing ccusage', () => {
    const mockFs = mock((path: string) => {
      if (path.endsWith('node_modules')) {
        return true;
      }
      if (path.includes('ccusage')) {
        return false;
      }
      return true;
    });

    const result = verifyPluginDependencies('/plugin/root', mockFs);

    expect(result.detected).toBe(false);
    expect(result.message).toContain('Missing dependencies');
    expect(result.message).toContain('ccusage');
  });

  test('detects multiple missing dependencies', () => {
    const mockFs = mock((path: string) => {
      if (path.endsWith('node_modules')) {
        return true;
      }
      // Both dependencies missing
      return false;
    });

    const result = verifyPluginDependencies('/plugin/root', mockFs);

    expect(result.detected).toBe(false);
    expect(result.message).toContain('Missing dependencies');
    expect(result.message).toContain('@anthropic-ai/claude-agent-sdk');
    expect(result.message).toContain('ccusage');
  });

  test('handles different plugin root paths', () => {
    const mockFs = mock((path: string) => {
      return path.includes('node_modules');
    });

    const result = verifyPluginDependencies('/custom/path/to/plugin', mockFs);

    expect(result.detected).toBe(true);
    // Verify it checked the correct path
    expect(mockFs).toHaveBeenCalledWith('/custom/path/to/plugin/node_modules');
  });
});
