// ABOUTME: Tests for error message templates used in plugin setup and validation
// ABOUTME: Ensures clear, actionable error messages guide users through common issues

import { describe, expect, test } from 'bun:test';
import {
  getBunNotInstalledMessage,
  getMissingDependenciesMessage,
  getNpmPluginConflictMessage,
  getPluginRootNotSetMessage,
} from './error-messages';

describe('getNpmPluginConflictMessage', () => {
  test('returns message about npm/plugin conflict', () => {
    const message = getNpmPluginConflictMessage();

    expect(message).toContain('npm/plugin conflict detected');
    expect(message).toContain('npm package and plugin versions');
    expect(message).toContain('npm uninstall -g cc-track');
  });

  test('includes uninstall instructions', () => {
    const message = getNpmPluginConflictMessage();

    expect(message).toContain('npm uninstall');
    expect(message).toContain('restart Claude Code');
  });

  test('message is multiline', () => {
    const message = getNpmPluginConflictMessage();

    expect(message.split('\n').length).toBeGreaterThan(5);
  });
});

describe('getMissingDependenciesMessage', () => {
  test('returns message about missing dependencies', () => {
    const message = getMissingDependenciesMessage('/plugin/root');

    expect(message).toContain('Plugin dependencies not installed');
    expect(message).toContain('bun install');
  });

  test('includes plugin root path in instructions', () => {
    const pluginRoot = '/custom/path/to/plugin';
    const message = getMissingDependenciesMessage(pluginRoot);

    expect(message).toContain(pluginRoot);
    expect(message).toContain(`cd ${pluginRoot}`);
  });

  test('handles different plugin root paths', () => {
    const paths = [
      '/home/user/.claude/plugins/cc-track',
      '/Users/dev/plugins/cc-track',
      'C:\\Users\\Developer\\plugins\\cc-track',
    ];

    for (const path of paths) {
      const message = getMissingDependenciesMessage(path);
      expect(message).toContain(path);
    }
  });

  test('message is multiline with code block', () => {
    const message = getMissingDependenciesMessage('/plugin/root');

    expect(message.split('\n').length).toBeGreaterThan(5);
    expect(message).toContain('```bash');
  });
});

describe('getBunNotInstalledMessage', () => {
  test('returns message about Bun not installed', () => {
    const message = getBunNotInstalledMessage();

    expect(message).toContain('Bun runtime not found');
    expect(message).toContain('cc-track plugin requires Bun');
  });

  test('includes Bun installation instructions', () => {
    const message = getBunNotInstalledMessage();

    expect(message).toContain('curl -fsSL https://bun.sh/install');
    expect(message).toContain('https://bun.sh');
  });

  test('instructs to restart terminal', () => {
    const message = getBunNotInstalledMessage();

    expect(message).toContain('restart your terminal');
    expect(message).toContain('try again');
  });

  test('message is multiline with code block', () => {
    const message = getBunNotInstalledMessage();

    expect(message.split('\n').length).toBeGreaterThan(5);
    expect(message).toContain('```bash');
  });
});

describe('getPluginRootNotSetMessage', () => {
  test('returns message about plugin root not set', () => {
    const message = getPluginRootNotSetMessage();

    expect(message).toContain('Plugin root not found');
    // biome-ignore lint/suspicious/noTemplateCurlyInString: Testing for literal ${CLAUDE_PLUGIN_ROOT} text
    expect(message).toContain('${CLAUDE_PLUGIN_ROOT}');
    expect(message).toContain('environment variable');
  });

  test('explains what it means', () => {
    const message = getPluginRootNotSetMessage();

    expect(message).toContain('not running as a Claude Code plugin');
    expect(message).toContain('through Claude Code');
  });

  test('provides troubleshooting steps', () => {
    const message = getPluginRootNotSetMessage();

    expect(message).toContain('Make sure you:');
    expect(message).toContain('Claude Code plugin');
    expect(message).toContain('not via npm');
  });

  test('message is multiline', () => {
    const message = getPluginRootNotSetMessage();

    expect(message.split('\n').length).toBeGreaterThan(5);
  });
});

describe('all error messages', () => {
  test('start with warning emoji', () => {
    const messages = [
      getNpmPluginConflictMessage(),
      getMissingDependenciesMessage('/plugin'),
      getBunNotInstalledMessage(),
      getPluginRootNotSetMessage(),
    ];

    for (const message of messages) {
      expect(message.trimStart()).toMatch(/^⚠️/);
    }
  });

  test('are non-empty strings', () => {
    const messages = [
      getNpmPluginConflictMessage(),
      getMissingDependenciesMessage('/plugin'),
      getBunNotInstalledMessage(),
      getPluginRootNotSetMessage(),
    ];

    for (const message of messages) {
      expect(message.length).toBeGreaterThan(0);
      expect(message.trim().length).toBeGreaterThan(0);
    }
  });

  test('contain actionable next steps', () => {
    const messages = [
      getNpmPluginConflictMessage(),
      getMissingDependenciesMessage('/plugin'),
      getBunNotInstalledMessage(),
      getPluginRootNotSetMessage(),
    ];

    for (const message of messages) {
      // Should contain some action word
      const hasAction =
        message.includes('install') ||
        message.includes('uninstall') ||
        message.includes('run') ||
        message.includes('try');
      expect(hasAction).toBe(true);
    }
  });
});
