# Test Patterns

Common patterns for testing scripts in this project.

## Pattern 1: CLI Tool Testing

Most scripts are command-line tools. Execute them with `execSync` and check output.

```javascript
import { describe, it } from 'node:test';
import assert from 'node:assert';
import { execSync } from 'node:child_process';
import { resolve } from 'node:path';

const projectRoot = resolve(import.meta.dirname, '../..');

function runScript(filePath) {
  try {
    const output = execSync(
      `node .claude/scripts/my-script.js "${filePath}"`,
      { cwd: projectRoot, encoding: 'utf-8', timeout: 30000 }
    );
    return { success: true, output, exitCode: 0 };
  } catch (error) {
    return {
      success: false,
      output: error.stdout || '',
      error: error.stderr || '',
      exitCode: error.status || 1
    };
  }
}

describe('my-script', () => {
  it('should process valid file', () => {
    const result = runScript('.claude/test/fixtures/valid/sample.html');
    assert.strictEqual(result.success, true);
  });

  it('should fail for invalid file', () => {
    const result = runScript('.claude/test/fixtures/invalid/broken.html');
    assert.strictEqual(result.success, false);
  });
});
```

## Pattern 2: JSON Output Parsing

Many tools output JSON. Parse it for structured assertions.

```javascript
function runWithJson(filePath) {
  try {
    const output = execSync(
      `npx tool "${filePath}" --reporter json`,
      { cwd: projectRoot, encoding: 'utf-8' }
    );
    const results = JSON.parse(output || '[]');
    return { success: true, results, errors: [] };
  } catch (error) {
    try {
      const results = JSON.parse(error.stdout || '[]');
      return { success: false, results, errors: results };
    } catch {
      return { success: false, results: [], errors: [error.message] };
    }
  }
}

it('should detect specific error', () => {
  const result = runWithJson('.claude/test/fixtures/invalid/missing-alt.html');
  assert.ok(result.errors.some(e => e.rule === 'alt-require'));
});
```

## Pattern 3: Async Fixture Setup

Create temporary test files during test execution.

```javascript
import { describe, it } from 'node:test';
import assert from 'node:assert';
import { writeFile, mkdir, rm } from 'node:fs/promises';
import { join } from 'node:path';

const testDir = join(import.meta.dirname, 'temp-fixtures');

describe('script with temp fixtures', () => {
  it('handles dynamically created files', async () => {
    // Setup
    await mkdir(testDir, { recursive: true });
    await writeFile(
      join(testDir, 'test.html'),
      '<!doctype html><html><head><title>Test</title></head><body></body></html>'
    );

    // Test
    const result = runScript(join(testDir, 'test.html'));
    assert.strictEqual(result.success, true);

    // Cleanup
    await rm(testDir, { recursive: true });
  });
});
```

## Pattern 4: Binary Data Generation

Generate test images or binary files programmatically.

```javascript
function createMinimalPNG() {
  // Minimal valid PNG (1x1 transparent pixel)
  return Buffer.from([
    0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, // PNG signature
    0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52, // IHDR chunk
    0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
    0x08, 0x06, 0x00, 0x00, 0x00, 0x1F, 0x15, 0xC4,
    0x89, 0x00, 0x00, 0x00, 0x0A, 0x49, 0x44, 0x41, // IDAT chunk
    0x54, 0x78, 0x9C, 0x63, 0x00, 0x01, 0x00, 0x00,
    0x05, 0x00, 0x01, 0x0D, 0x0A, 0x2D, 0xB4, 0x00,
    0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44, 0xAE, // IEND chunk
    0x42, 0x60, 0x82
  ]);
}

it('processes generated images', async () => {
  await writeFile(join(testDir, 'test.png'), createMinimalPNG());
  const result = runImageCheck(testDir);
  assert.strictEqual(result.exitCode, 0);
});
```

## Pattern 5: Configuration Validation

Test that configuration files are valid.

```javascript
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

function loadConfig(filename) {
  const configPath = resolve(projectRoot, filename);
  return JSON.parse(readFileSync(configPath, 'utf8'));
}

describe('Configuration', () => {
  it('has valid .htmlvalidate.json', () => {
    const config = loadConfig('.htmlvalidate.json');
    assert.ok(config.extends, 'Should have extends property');
    assert.ok(config.rules, 'Should have rules property');
  });
});
```

## Pattern 6: Regex Output Matching

Match output patterns with regular expressions.

```javascript
it('shows usage information', () => {
  const result = runScript('--help');
  assert.match(result.output, /Usage:/, 'Should show usage');
  assert.match(result.output, /Options:/, 'Should list options');
  assert.match(result.output, /--help/, 'Should document --help');
});

it('reports statistics', () => {
  const result = runScript('.claude/patterns/pages');
  assert.match(result.output, /\d+ files? checked/);
  assert.match(result.output, /\d+ errors?/);
});
```

## Pattern 7: Error Message Validation

Ensure error messages are informative.

```javascript
it('provides actionable error message', () => {
  const result = runScript('nonexistent-file.html');
  assert.strictEqual(result.success, false);
  assert.match(result.output, /not found|does not exist/i);
  assert.match(result.output, /nonexistent-file\.html/);
});
```

## Pattern 8: Environment Variable Testing

Test behavior with different environment settings.

```javascript
it('respects CI environment', () => {
  const result = execSync(
    'node .claude/scripts/my-script.js',
    {
      cwd: projectRoot,
      encoding: 'utf-8',
      env: { ...process.env, CI: 'true' }
    }
  );
  assert.match(result, /CI mode enabled/);
});
```

## Anti-Patterns to Avoid

| Anti-Pattern | Better Approach |
|--------------|-----------------|
| Hardcoded absolute paths | Use `import.meta.dirname` and `resolve()` |
| Skipping cleanup | Use `after()` hook for cleanup |
| Testing implementation details | Test public API and output |
| Fragile string matching | Use regex with `assert.match()` |
| No timeout on execSync | Always set `timeout` option |
