import { beforeEach, describe, expect, mock, test } from 'bun:test';
import {
  clearConfigCache,
  getConfig,
  getConfigPath,
  getGitHubConfig,
  isGitHubIntegrationEnabled,
  isHookEnabled,
} from './config';

describe('config', () => {
  beforeEach(() => {
    mock.restore();
    clearConfigCache();
  });

  describe('getConfigPath', () => {
    test('returns config path in .claude directory', () => {
      // This is testing the actual implementation without mocks
      // since the path construction is deterministic
      const path = getConfigPath('/home/test/project');
      expect(path).toContain('/.cc-track/track.config.json');
    });
  });

  describe('getConfig', () => {
    test('returns config with expected structure', () => {
      const config = getConfig();
      expect(config).toHaveProperty('hooks');
      expect(config).toHaveProperty('features');
    });

    test('has default hooks configured', () => {
      const config = getConfig();
      expect(config.hooks).toHaveProperty('capture_plan');
      expect(config.hooks).toHaveProperty('pre_compact');
      expect(config.hooks).toHaveProperty('stop_review');
      expect(config.hooks).toHaveProperty('edit_validation');
    });

    test('has default features configured', () => {
      const config = getConfig();
      expect(config.features).toHaveProperty('statusline');
      expect(config.features).toHaveProperty('git_branching');
      expect(config.features).toHaveProperty('api_timer');
      expect(config.features).toHaveProperty('github_integration');
    });
  });

  describe('isHookEnabled', () => {
    test('returns expected values for default hooks', () => {
      // Test with a non-existent config path to force default values
      const nonExistentPath = '/tmp/nonexistent/config.json';
      // Deprecated hooks are disabled by default
      expect(isHookEnabled('capture_plan', nonExistentPath)).toBe(false);
      expect(isHookEnabled('pre_compact', nonExistentPath)).toBe(false);
      expect(isHookEnabled('stop_review', nonExistentPath)).toBe(false);
      expect(isHookEnabled('edit_validation', nonExistentPath)).toBe(false); // Disabled by default
      expect(isHookEnabled('pre_tool_validation', nonExistentPath)).toBe(true); // Enabled by default
    });

    test('returns expected values for features with defaults', () => {
      const nonExistentPath = '/tmp/nonexistent/config.json';
      expect(isHookEnabled('statusline', nonExistentPath)).toBe(true);
      expect(isHookEnabled('git_branching', nonExistentPath)).toBe(false); // Disabled by default
    });

    test('returns true for unknown hook (default behavior)', () => {
      const nonExistentPath = '/tmp/nonexistent/config.json';
      expect(isHookEnabled('unknown_hook', nonExistentPath)).toBe(true);
    });
  });

  describe('getGitHubConfig', () => {
    test('returns GitHub config structure from defaults', () => {
      const nonExistentPath = '/tmp/nonexistent/config.json';
      const config = getGitHubConfig(nonExistentPath);
      // With default config, GitHub integration exists but is disabled
      expect(config).not.toBeNull();
      expect(config?.enabled).toBe(false);
      expect(config?.description).toContain('GitHub');
    });
  });

  describe('isGitHubIntegrationEnabled', () => {
    test('returns false by default', () => {
      const nonExistentPath = '/tmp/nonexistent/config.json';
      expect(isGitHubIntegrationEnabled(nonExistentPath)).toBe(false);
    });
  });
});
