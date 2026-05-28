/**
 * Unit tests for utility scripts
 *
 * Run with: npm test or node --test
 */

import { describe, it, beforeEach, afterEach, mock } from 'node:test';
import assert from 'node:assert';
import { existsSync, readFileSync, writeFileSync, mkdirSync, rmSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

// =============================================================================
// Test Helpers
// =============================================================================

const __dirname = dirname(fileURLToPath(import.meta.url));
const SCRIPTS_DIR = join(__dirname, '..');
const TEST_DIR = join(__dirname, 'temp-test-project');

function setupTestProject(files = {}) {
  // Create test directory
  mkdirSync(TEST_DIR, { recursive: true });

  // Create default package.json
  const defaultPkg = {
    name: 'test-project',
    version: '1.0.0',
    scripts: {},
  };

  writeFileSync(
    join(TEST_DIR, 'package.json'),
    JSON.stringify(files['package.json'] || defaultPkg, null, 2)
  );

  // Create other specified files
  for (const [path, content] of Object.entries(files)) {
    if (path === 'package.json') continue;

    const fullPath = join(TEST_DIR, path);
    const dir = join(fullPath, '..');
    mkdirSync(dir, { recursive: true });

    if (typeof content === 'object') {
      writeFileSync(fullPath, JSON.stringify(content, null, 2));
    } else {
      writeFileSync(fullPath, content || '');
    }
  }

  return TEST_DIR;
}

function cleanupTestProject() {
  try {
    rmSync(TEST_DIR, { recursive: true, force: true });
  } catch {
    // Ignore cleanup errors
  }
}

// =============================================================================
// audit-project.js Tests
// =============================================================================

describe('audit-project.js', () => {
  beforeEach(() => {
    cleanupTestProject();
  });

  afterEach(() => {
    cleanupTestProject();
  });

  it('should detect missing README.md', () => {
    const projectDir = setupTestProject({
      'package.json': { name: 'test', version: '1.0.0' },
    });

    const result = spawnSync('node', [join(SCRIPTS_DIR, 'audit-project.js'), '--json'], {
      cwd: projectDir,
      encoding: 'utf-8',
    });

    const output = JSON.parse(result.stdout);
    const processCategory = output.categories.find(c => c.name === 'Conformité Process');
    const readmeCheck = processCategory.checks.find(c => c.id === 'readme');

    assert.strictEqual(readmeCheck.passed, false);
  });

  it('should detect present README.md', () => {
    const projectDir = setupTestProject({
      'package.json': { name: 'test', version: '1.0.0' },
      'README.md': '# Test Project\n\nDescription here.\n',
    });

    const result = spawnSync('node', [join(SCRIPTS_DIR, 'audit-project.js'), '--json'], {
      cwd: projectDir,
      encoding: 'utf-8',
    });

    const output = JSON.parse(result.stdout);
    const processCategory = output.categories.find(c => c.name === 'Conformité Process');
    const readmeCheck = processCategory.checks.find(c => c.id === 'readme');

    assert.strictEqual(readmeCheck.passed, true);
  });

  it('should detect ESLint configuration', () => {
    const projectDir = setupTestProject({
      'package.json': { name: 'test', version: '1.0.0' },
      'eslint.config.js': 'export default [];',
    });

    const result = spawnSync('node', [join(SCRIPTS_DIR, 'audit-project.js'), '--json'], {
      cwd: projectDir,
      encoding: 'utf-8',
    });

    const output = JSON.parse(result.stdout);
    const qualityCategory = output.categories.find(c => c.name === 'Qualité du Code');
    const eslintCheck = qualityCategory.checks.find(c => c.id === 'eslint');

    assert.strictEqual(eslintCheck.passed, true);
  });

  it('should detect test script in package.json', () => {
    const projectDir = setupTestProject({
      'package.json': {
        name: 'test',
        version: '1.0.0',
        scripts: { test: 'vitest' },
      },
    });

    const result = spawnSync('node', [join(SCRIPTS_DIR, 'audit-project.js'), '--json'], {
      cwd: projectDir,
      encoding: 'utf-8',
    });

    const output = JSON.parse(result.stdout);
    const testingCategory = output.categories.find(c => c.name === 'Tests');
    const testScriptCheck = testingCategory.checks.find(c => c.id === 'test-script');

    assert.strictEqual(testScriptCheck.passed, true);
  });

  it('should calculate score correctly', () => {
    const projectDir = setupTestProject({
      'package.json': { name: 'test', version: '1.0.0' },
      'README.md': '# Test\n',
      '.gitignore': 'node_modules\n',
    });

    const result = spawnSync('node', [join(SCRIPTS_DIR, 'audit-project.js'), '--json'], {
      cwd: projectDir,
      encoding: 'utf-8',
    });

    const output = JSON.parse(result.stdout);

    assert.ok(output.score >= 0 && output.score <= 100);
    assert.ok(output.timestamp);
    assert.ok(Array.isArray(output.categories));
  });

  it('should skip deps audit with --no-deps', () => {
    const projectDir = setupTestProject({
      'package.json': { name: 'test', version: '1.0.0' },
    });

    const result = spawnSync('node', [join(SCRIPTS_DIR, 'audit-project.js'), '--json', '--no-deps'], {
      cwd: projectDir,
      encoding: 'utf-8',
    });

    const output = JSON.parse(result.stdout);

    assert.strictEqual(output.dependencies, null);
  });
});

// =============================================================================
// check-process.js Tests
// =============================================================================

describe('check-process.js', () => {
  beforeEach(() => {
    cleanupTestProject();
  });

  afterEach(() => {
    cleanupTestProject();
  });

  it('should fail when README.md is missing', () => {
    const projectDir = setupTestProject({
      'package.json': { name: 'test', version: '1.0.0' },
    });

    const result = spawnSync('node', [join(SCRIPTS_DIR, 'check-process.js')], {
      cwd: projectDir,
      encoding: 'utf-8',
    });

    assert.strictEqual(result.status, 1);
    assert.ok(result.stdout.includes('README.md'));
  });

  it('should pass when required files are present', () => {
    const projectDir = setupTestProject({
      'package.json': { name: 'test', version: '1.0.0' },
      'README.md': '# Test Project\n',
      '.gitignore': 'node_modules\n',
    });

    // Initialize git for the test
    spawnSync('git', ['init'], { cwd: projectDir });

    const result = spawnSync('node', [join(SCRIPTS_DIR, 'check-process.js')], {
      cwd: projectDir,
      encoding: 'utf-8',
    });

    assert.strictEqual(result.status, 0);
    assert.ok(result.stdout.includes('respecte le process'));
  });

  it('should detect missing package.json fields', () => {
    const projectDir = setupTestProject({
      'package.json': { name: 'test' }, // missing version
      'README.md': '# Test\n',
      '.gitignore': 'node_modules\n',
    });

    const result = spawnSync('node', [join(SCRIPTS_DIR, 'check-process.js')], {
      cwd: projectDir,
      encoding: 'utf-8',
    });

    // Should fail due to missing version
    assert.strictEqual(result.status, 1);
  });

  it('should detect ESLint alternatives', () => {
    const projectDir = setupTestProject({
      'package.json': { name: 'test', version: '1.0.0' },
      'README.md': '# Test\n',
      '.gitignore': 'node_modules\n',
      '.eslintrc.json': '{}', // Using alternative config
    });

    spawnSync('git', ['init'], { cwd: projectDir });

    const result = spawnSync('node', [join(SCRIPTS_DIR, 'check-process.js')], {
      cwd: projectDir,
      encoding: 'utf-8',
    });

    assert.ok(result.stdout.includes('ESLint'));
  });

  it('should detect git hooks', () => {
    const projectDir = setupTestProject({
      'package.json': { name: 'test', version: '1.0.0' },
      'README.md': '# Test\n',
      '.gitignore': 'node_modules\n',
      'lefthook.yml': 'pre-commit:\n  commands: {}\n',
    });

    spawnSync('git', ['init'], { cwd: projectDir });

    const result = spawnSync('node', [join(SCRIPTS_DIR, 'check-process.js')], {
      cwd: projectDir,
      encoding: 'utf-8',
    });

    assert.ok(result.stdout.includes('Git hooks configurés'));
    assert.ok(result.stdout.includes('Lefthook'));
  });

  it('should work in quiet mode', () => {
    const projectDir = setupTestProject({
      'package.json': { name: 'test', version: '1.0.0' },
      'README.md': '# Test\n',
      '.gitignore': 'node_modules\n',
    });

    spawnSync('git', ['init'], { cwd: projectDir });

    const result = spawnSync('node', [join(SCRIPTS_DIR, 'check-process.js'), '--quiet'], {
      cwd: projectDir,
      encoding: 'utf-8',
    });

    // Quiet mode should not show recommended files section
    assert.ok(!result.stdout.includes('Fichiers recommandés'));
  });
});

// =============================================================================
// Security Tests
// =============================================================================

describe('Security', () => {
  beforeEach(() => {
    cleanupTestProject();
  });

  afterEach(() => {
    cleanupTestProject();
  });

  it('should not be vulnerable to command injection in pattern check', () => {
    // This test ensures that the fix for command injection is working
    // The pattern contains shell metacharacters that would be dangerous
    // if passed directly to a shell

    const projectDir = setupTestProject({
      'package.json': { name: 'test', version: '1.0.0' },
      'README.md': '# Test\n',
    });

    // Initialize git
    spawnSync('git', ['init'], { cwd: projectDir });

    // Create a file with a dangerous name (simulating what could be in patterns)
    writeFileSync(join(projectDir, 'test;whoami'), 'test');

    const result = spawnSync('node', [join(SCRIPTS_DIR, 'audit-project.js'), '--json'], {
      cwd: projectDir,
      encoding: 'utf-8',
    });

    // The script should complete without executing the injected command
    assert.ok(result.status === 0 || result.status === null);
    assert.ok(!result.stderr?.includes('whoami'));
  });
});

// =============================================================================
// Helper Function Tests
// =============================================================================

describe('Helper Functions', () => {
  it('should correctly parse nested package.json values', () => {
    const projectDir = setupTestProject({
      'package.json': {
        name: 'test',
        version: '1.0.0',
        scripts: {
          test: 'vitest',
          lint: 'eslint .',
        },
      },
      'README.md': '# Test\n',
      '.gitignore': 'node_modules\n',
    });

    spawnSync('git', ['init'], { cwd: projectDir });

    const result = spawnSync('node', [join(SCRIPTS_DIR, 'check-process.js')], {
      cwd: projectDir,
      encoding: 'utf-8',
    });

    assert.ok(result.stdout.includes('Script de linting'));
    assert.ok(result.stdout.includes('Script de tests'));
  });
});
