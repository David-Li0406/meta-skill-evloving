// ABOUTME: Detection utilities for npm package conflicts, Bun runtime, and plugin dependencies
// ABOUTME: Provides verification functions to ensure clean plugin installation and prevent npm/plugin conflicts

import { execSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { join } from 'node:path/posix';

export interface DetectionResult {
  detected: boolean;
  message?: string;
}

/**
 * Check if npm version of cc-track is globally installed
 * @param exec - Optional execSync function for testing
 * @returns Detection result with boolean and message
 */
export function detectNpmPackage(exec: typeof execSync = execSync): DetectionResult {
  try {
    // Use platform-appropriate command to find binary
    const isWindows = process.platform === 'win32';
    const findCommand = isWindows ? 'where cc-track' : 'which cc-track';
    const whichResult = exec(findCommand, {
      encoding: 'utf-8',
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    if (whichResult?.toString().trim()) {
      return {
        detected: true,
        message: `Found cc-track binary at: ${whichResult.toString().trim()}`,
      };
    }
  } catch {
    // Command failed, try npm list
  }

  try {
    // Check using npm list -g (works cross-platform)
    const npmResult = exec('npm list -g cc-track --depth=0', {
      encoding: 'utf-8',
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    if (npmResult?.toString().includes('cc-track@')) {
      return {
        detected: true,
        message: 'Found cc-track in global npm packages',
      };
    }
  } catch {
    // npm list failed, package not found
  }

  return { detected: false };
}

/**
 * Verify that Bun runtime is installed and accessible
 * @param exec - Optional execSync function for testing
 * @returns Detection result with boolean and message
 */
export function verifyBunInstalled(exec: typeof execSync = execSync): DetectionResult {
  try {
    const bunVersion = exec('bun --version', {
      encoding: 'utf-8',
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    if (bunVersion?.toString().trim()) {
      return {
        detected: true,
        message: `Bun v${bunVersion.toString().trim()} is installed`,
      };
    }
  } catch {
    return {
      detected: false,
      message: 'Bun runtime not found in PATH',
    };
  }

  return { detected: false, message: 'Bun check failed' };
}

/**
 * Verify that plugin dependencies are installed in the plugin directory
 * @param pluginRoot - Root directory of the plugin (${CLAUDE_PLUGIN_ROOT})
 * @param fs - Optional existsSync function for testing
 * @returns Detection result with boolean and message
 */
export function verifyPluginDependencies(pluginRoot: string, fs: typeof existsSync = existsSync): DetectionResult {
  const nodeModulesPath = join(pluginRoot, 'node_modules');

  if (!fs(nodeModulesPath)) {
    return {
      detected: false,
      message: `node_modules not found at ${nodeModulesPath}`,
    };
  }

  // Check for critical dependencies
  const criticalDeps = ['@anthropic-ai/claude-agent-sdk', 'ccusage'];
  const missingDeps: string[] = [];

  for (const dep of criticalDeps) {
    const depPath = join(nodeModulesPath, dep);
    if (!fs(depPath)) {
      missingDeps.push(dep);
    }
  }

  if (missingDeps.length > 0) {
    return {
      detected: false,
      message: `Missing dependencies: ${missingDeps.join(', ')}`,
    };
  }

  return {
    detected: true,
    message: 'All plugin dependencies are installed',
  };
}
