import { describe, expect, test } from 'bun:test';
import { BiomeParser, ESLintParser, GenericParser, getLintParser } from './lint-parsers';

describe('BiomeParser', () => {
  const parser = new BiomeParser();

  test('parses diagnostic count from output', () => {
    const output = `
Found 5 diagnostics.
src/file.ts:10:5 lint/style/noVar Variable should use const
    `;
    const result = parser.parseOutput(output);
    expect(result.issueCount).toBe(5);
  });

  test('extracts errors for specific file', () => {
    const output = `
src/test.ts:10:5 lint/style/noVar Use const instead
src/other.ts:20:3 lint/style/noUnusedVariables Unused variable
src/test.ts:15:8 lint/correctness/noUnusedImports Unused import
    `;
    const result = parser.parseOutput(output, 'src/test.ts');
    expect(result.errors).toHaveLength(2);
    expect(result.errors[0]).toBe('Line 10: Use const instead');
    expect(result.errors[1]).toBe('Line 15: Unused import');
  });

  test('limits errors to 20 items', () => {
    const lines = Array.from({ length: 30 }, (_, i) => `src/file.ts:${i + 1}:5 lint/style/rule Error ${i + 1}`);
    const output = lines.join('\n');
    const result = parser.parseOutput(output);
    expect(result.errors).toHaveLength(21); // 20 errors + "... and more"
    expect(result.errors[20]).toBe('... and more');
  });

  test('parses verbose format with box characters', () => {
    const output = `
test.ts:1:1 lint/suspicious/noVar  FIXABLE  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  × Use let or const instead of var.

  > 1 │ var x = 1;
      │ ^^^^^^^^^
    2 │ debugger;
    3 │

test.ts:1:5 lint/correctness/noUnusedVariables  FIXABLE  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  × This variable x is unused.

  > 1 │ var x = 1;
      │     ^
    2 │ debugger;
    3 │

Checked 1 file in 2ms. No fixes applied.
Found 2 errors.
    `;
    const result = parser.parseOutput(output, 'test.ts');
    expect(result.errors).toHaveLength(2);
    expect(result.errors[0]).toBe('Line 1: Use let or const instead of var.');
    expect(result.errors[1]).toBe('Line 1: This variable x is unused.');
    expect(result.issueCount).toBe(2);
  });

  test('parses verbose format with ! symbol', () => {
    const output = `
src/file.ts:10:5 lint/style/useTemplate  FIXABLE  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ! Template literals are preferred over string concatenation.

    8 │ const name = 'World';
  > 10 │ const greeting = 'Hello ' + name;
       │                  ^^^^^^^^^^^^^^^^
   11 │

Checked 1 file in 1ms. No fixes applied.
Found 1 error.
    `;
    const result = parser.parseOutput(output, 'src/file.ts');
    expect(result.errors).toHaveLength(1);
    expect(result.errors[0]).toBe('Line 10: Template literals are preferred over string concatenation.');
  });

  test('handles Windows absolute paths', () => {
    const output = `
src\\test.ts:5:1 lint/suspicious/noDebugger  FIXABLE  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  × This is an unexpected use of the debugger statement.

  > 5 │ debugger;
      │ ^^^^^^^^^

Checked 1 file in 2ms. No fixes applied.
Found 1 error.
    `;
    // Test with Windows-style absolute path
    const result = parser.parseOutput(output, 'C:\\projects\\repo\\src\\test.ts');
    expect(result.errors).toHaveLength(1);
    expect(result.errors[0]).toBe('Line 5: This is an unexpected use of the debugger statement.');
  });

  test('handles Windows absolute paths in Biome output', () => {
    // Biome on Windows may output absolute paths with drive letters
    const output = `
C:\\projects\\repo\\src\\test.ts:5:1 lint/suspicious/noDebugger  FIXABLE  ━━━━━━━━━━━━━━━━━━━━━━━━

  × This is an unexpected use of the debugger statement.

  > 5 │ debugger;
      │ ^^^^^^^^^

Checked 1 file in 2ms. No fixes applied.
Found 1 error.
    `;
    const result = parser.parseOutput(output, 'C:\\projects\\repo\\src\\test.ts');
    expect(result.errors).toHaveLength(1);
    expect(result.errors[0]).toBe('Line 5: This is an unexpected use of the debugger statement.');
  });

  test('prevents filename collision (test.ts vs latest.ts)', () => {
    const output = `
src/test.ts:10:1 lint/suspicious/noVar  FIXABLE  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  × Use let or const instead of var.

  > 10 │ var x = 1;
       │ ^^^^^^^^^^

src/latest.ts:20:1 lint/suspicious/noVar  FIXABLE  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  × Use let or const instead of var.

  > 20 │ var y = 2;
       │ ^^^^^^^^^^

Checked 2 files in 3ms. No fixes applied.
Found 2 errors.
    `;
    // Should only get error from test.ts, not latest.ts
    const result = parser.parseOutput(output, 'src/test.ts');
    expect(result.errors).toHaveLength(1);
    expect(result.errors[0]).toBe('Line 10: Use let or const instead of var.');
  });

  test('strips ANSI color codes from filenames', () => {
    // Biome may output filenames with ANSI color codes when running in a terminal
    const output = `
\u001b[36msrc/test.ts\u001b[0m:5:1 lint/suspicious/noDebugger  FIXABLE  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  × This is an unexpected use of the debugger statement.

  > 5 │ debugger;
      │ ^^^^^^^^^

Checked 1 file in 2ms. No fixes applied.
Found 1 error.
    `;
    const result = parser.parseOutput(output, 'src/test.ts');
    expect(result.errors).toHaveLength(1);
    expect(result.errors[0]).toBe('Line 5: This is an unexpected use of the debugger statement.');
  });

  test('strips ANSI color codes from error message lines', () => {
    // Biome adds color codes to error symbols when running in a TTY
    const output = `
src/test.ts:5:1 lint/suspicious/noDebugger  FIXABLE  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  \u001b[31m×\u001b[0m This is an unexpected use of the debugger statement.

  > 5 │ debugger;
      │ ^^^^^^^^^

Checked 1 file in 2ms. No fixes applied.
Found 1 error.
    `;
    const result = parser.parseOutput(output, 'src/test.ts');
    expect(result.errors).toHaveLength(1);
    expect(result.errors[0]).toBe('Line 5: This is an unexpected use of the debugger statement.');
  });

  test('returns auto-fix command', () => {
    expect(parser.getAutoFixCommand('bunx biome check')).toBe('bunx biome check --write');
    expect(parser.getAutoFixCommand('bunx biome check --write')).toBe('bunx biome check --write');
  });
});

describe('ESLintParser', () => {
  const parser = new ESLintParser();

  test('parses problem count from summary', () => {
    const output = `
/src/file.ts
  10:5  error  Unexpected var  no-var

✖ 3 problems (2 errors, 1 warning)
    `;
    const result = parser.parseOutput(output);
    expect(result.issueCount).toBe(3);
  });

  test('parses stylish format output', () => {
    const output = `
/src/test.ts
  10:5  error    Unexpected var         no-var
  15:8  warning  Unused variable 'x'    no-unused-vars
    `;
    const result = parser.parseOutput(output);
    // When no specific file is given, it includes the file path
    expect(result.errors).toContain('/src/test.ts:10 - Unexpected var');
    expect(result.errors).toContain("/src/test.ts:15 - Unused variable 'x'");
  });

  test('parses compact format output', () => {
    const output = `
/src/test.ts:10:5: Unexpected var [no-var]
/src/test.ts:15:8: Unused variable 'x' [no-unused-vars]
/src/other.ts:20:3: Missing semicolon [semi]
    `;
    const result = parser.parseOutput(output, '/src/test.ts');
    expect(result.errors).toHaveLength(2);
    expect(result.errors[0]).toBe('Line 10: Unexpected var');
    expect(result.errors[1]).toBe("Line 15: Unused variable 'x'");
  });

  test('handles file headers correctly', () => {
    const output = `
/src/components/Button.tsx
  5:10  error  Component should be exported  react/no-unused-vars

/src/utils/helper.js
  10:5  warning  Unexpected console statement  no-console
    `;
    const result = parser.parseOutput(output);
    expect(result.errors).toContain('/src/components/Button.tsx:5 - Component should be exported');
    expect(result.errors).toContain('/src/utils/helper.js:10 - Unexpected console statement');
  });

  test('returns auto-fix command', () => {
    expect(parser.getAutoFixCommand('npx eslint')).toBe('npx eslint --fix');
    expect(parser.getAutoFixCommand('npx eslint --fix')).toBe('npx eslint --fix');
  });
});

describe('GenericParser', () => {
  const parser = new GenericParser();

  test('extracts lines with error or warning keywords', () => {
    const output = `
Checking files...
Error: Invalid syntax at line 10
Warning: Deprecated function at line 15
Line 20: Type mismatch
Done with 3 issues
    `;
    const result = parser.parseOutput(output);
    expect(result.errors).toContain('Error: Invalid syntax at line 10');
    expect(result.errors).toContain('Warning: Deprecated function at line 15');
    expect(result.errors).toContain('Line 20: Type mismatch');
    expect(result.errors).not.toContain('Checking files...');
    expect(result.errors).not.toContain('Done with 3 issues');
  });

  test('filters by file path when provided', () => {
    const output = `
src/test.ts: Error on line 10
src/other.ts: Error on line 20
src/test.ts: Warning on line 15
    `;
    const result = parser.parseOutput(output, 'src/test.ts');
    expect(result.errors).toHaveLength(2);
    expect(result.errors[0]).toBe('src/test.ts: Error on line 10');
    expect(result.errors[1]).toBe('src/test.ts: Warning on line 15');
  });

  test('extracts issue count from common patterns', () => {
    const output = `
Some linter output
Found 8 errors in the code
    `;
    const result = parser.parseOutput(output);
    expect(result.issueCount).toBe(8);
  });

  test('returns undefined for auto-fix command', () => {
    expect(parser.getAutoFixCommand('some-linter')).toBeUndefined();
  });
});

describe('getLintParser', () => {
  test('returns BiomeParser for biome tool', () => {
    const parser = getLintParser('biome');
    expect(parser).toBeInstanceOf(BiomeParser);
  });

  test('returns ESLintParser for eslint tool', () => {
    const parser = getLintParser('eslint');
    expect(parser).toBeInstanceOf(ESLintParser);
  });

  test('returns GenericParser for unknown tools', () => {
    const parser = getLintParser('unknown-linter');
    expect(parser).toBeInstanceOf(GenericParser);
  });

  test('is case-insensitive', () => {
    expect(getLintParser('BIOME')).toBeInstanceOf(BiomeParser);
    expect(getLintParser('ESLint')).toBeInstanceOf(ESLintParser);
  });
});
