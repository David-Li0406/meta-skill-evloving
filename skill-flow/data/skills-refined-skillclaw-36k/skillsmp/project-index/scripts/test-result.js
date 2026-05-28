#!/usr/bin/env node
/**
 * Test Result - Vitest result extraction for AI consumption
 *
 * Design philosophy:
 * - Persist results locally, query with pagination
 * - Return rich, raw information - let AI decide how to classify/fix
 * - Stable error IDs for cross-session reference
 *
 * Usage:
 *   node test-result.js --save            # Run tests and save full results
 *   node test-result.js --cached          # Show cached summary
 *   node test-result.js --cached --errors # Show all cached errors
 *   node test-result.js --cached --offset=0 --limit=40   # Errors 1-40
 *   node test-result.js --cached --offset=40 --limit=40  # Errors 41-80
 *   node test-result.js --summary         # One-line summary
 *
 * Persisted format (.test-result.json):
 *   {
 *     "total": 240, "passed": 200, "failed": 40,
 *     "errors": [ { "id": 1, "file": "...", "message": "..." }, ... ]
 *   }
 *
 * Query returns:
 *   {
 *     "total": 240, "passed": 200, "failed": 40,
 *     "showing": "1-40 of 40 errors",
 *     "errors": [ ... ]
 *   }
 */

import { promises as fs } from 'fs';
import path from 'path';
import { spawn } from 'child_process';
import { parseArgs, readJsonSafe, writeJsonSafe } from './shared.js';

const RESULT_FILE = '.test-result.json';

/**
 * Extract location info from error message
 */
function extractLocation(message) {
  const match = message.match(/(?:at\s+)?([^\s:]+):(\d+)(?::(\d+))?/);
  if (match) {
    return {
      file: match[1],
      line: parseInt(match[2]),
      column: match[3] ? parseInt(match[3]) : undefined
    };
  }
  return {};
}

/**
 * Extract expected/received values from assertion error
 */
function extractAssertion(message) {
  const result = {};
  const expectedMatch = message.match(/Expected[:\s]+(.+?)(?=\n|Received|$)/is);
  const receivedMatch = message.match(/Received[:\s]+(.+?)(?=\n|$)/is);
  if (expectedMatch) result.expected = expectedMatch[1].trim().slice(0, 200);
  if (receivedMatch) result.received = receivedMatch[1].trim().slice(0, 200);
  const diffMatch = message.match(/(-\s+.+\n\+\s+.+)/s);
  if (diffMatch) result.diff = diffMatch[1].slice(0, 500);
  return result;
}

/**
 * Infer source file from test file path
 * tests/unit/foo/bar.test.js -> js/foo/bar.js or src/foo/bar.js
 */
function inferSourceFile(testFile) {
  // Common patterns: tests/unit/X -> js/X or src/X
  let source = testFile
    .replace(/^tests\/(unit|integration)\//, '')
    .replace(/\.test\.(js|ts|mjs)$/, '.js')
    .replace(/\.spec\.(js|ts|mjs)$/, '.js');

  // Try common prefixes
  const prefixes = ['js/', 'src/', 'lib/', ''];
  for (const prefix of prefixes) {
    // Return the most likely path (caller should verify)
    if (prefix) return prefix + source;
  }
  return source;
}

/**
 * Parse error into structured format with stable ID
 */
function parseError(testResult, filePath, cwd, id) {
  const message = testResult.failureMessages?.join('\n') || '';
  const location = extractLocation(message);
  const assertion = extractAssertion(message);
  const testFile = path.relative(cwd, filePath);

  return {
    id,
    testFile,
    sourceFile: inferSourceFile(testFile),  // 推断的源文件路径
    test: testResult.fullName || testResult.title,
    ancestors: testResult.ancestorTitles || [],
    message: message.slice(0, 2000),
    ...location,
    ...assertion
  };
}

/**
 * Run vitest and collect ALL errors (no limit during collection)
 */
async function runVitest(testPath, cwd) {
  return new Promise((resolve) => {
    const args = ['vitest', 'run', '--reporter=json'];
    if (testPath) args.push(testPath);

    const startTime = Date.now();
    const child = spawn('npx', args, {
      cwd,
      stdio: ['pipe', 'pipe', 'pipe'],
      shell: process.platform === 'win32'
    });

    let stdout = '';
    let stderr = '';

    child.stdout.on('data', (data) => { stdout += data.toString(); });
    child.stderr.on('data', (data) => { stderr += data.toString(); });

    child.on('close', () => {
      const duration = Date.now() - startTime;

      try {
        const jsonMatch = stdout.match(/\{[\s\S]*"testResults"[\s\S]*\}/);
        if (jsonMatch) {
          const result = JSON.parse(jsonMatch[0]);
          const errors = [];
          let errorId = 1;

          for (const file of result.testResults || []) {
            for (const test of file.assertionResults || []) {
              if (test.status === 'failed') {
                errors.push(parseError(test, file.name, cwd, errorId++));
              }
            }
          }

          resolve({
            total: result.numTotalTests || 0,
            passed: result.numPassedTests || 0,
            failed: result.numFailedTests || 0,
            skipped: result.numPendingTests || 0,
            duration,
            timestamp: new Date().toISOString(),
            errors  // ALL errors with stable IDs
          });
          return;
        }
      } catch (e) {
        // Fall through
      }

      // Fallback
      const output = stderr + stdout;
      const failedMatch = output.match(/(\d+) failed/);
      const passedMatch = output.match(/(\d+) passed/);
      const skippedMatch = output.match(/(\d+) skipped/);

      resolve({
        total: (passedMatch ? parseInt(passedMatch[1]) : 0) +
               (failedMatch ? parseInt(failedMatch[1]) : 0) +
               (skippedMatch ? parseInt(skippedMatch[1]) : 0),
        passed: passedMatch ? parseInt(passedMatch[1]) : 0,
        failed: failedMatch ? parseInt(failedMatch[1]) : 0,
        skipped: skippedMatch ? parseInt(skippedMatch[1]) : 0,
        duration,
        timestamp: new Date().toISOString(),
        errors: [],
        rawOutput: output.slice(0, 3000),
        parseMode: 'text-fallback'
      });
    });
  });
}

/**
 * Format one-line summary
 */
function formatSummary(result) {
  const status = result.failed > 0 ? 'FAIL' : 'PASS';
  const emoji = result.failed > 0 ? '❌' : '✅';
  return `${emoji} ${status}: ${result.passed}/${result.total} passed, ${result.failed} failed (${result.errors?.length || 0} error details)`;
}

async function main() {
  const args = parseArgs(process.argv.slice(2), {
    cached: false,
    summary: false,
    errors: false,
    save: false,
    help: false,
    file: null,      // 按文件名查询
    id: null,        // 按错误 ID 查询
    offset: '0',
    limit: '40'
  });

  if (args.help) {
    console.log(`
Test Result - Vitest result extraction for AI

Usage: node test-result.js [options] [path]

Options:
  --save           Run tests and save full results to cache
  --cached         Use cached results (required for queries)
  --summary        One-line summary
  --errors         Show errors with testFile, sourceFile, message
  --file=X         Query errors by file path (supports partial match)
  --id=N           Query single error by ID
  --offset=N       Start from error N (0-indexed, default 0)
  --limit=N        Return N errors (default 40, AI can fix concurrently)
  --help           Show this help

Examples:
  node test-result.js --save                    # Run and save
  node test-result.js --cached --errors         # Get 40 errors, fix concurrently
  node test-result.js --cached --errors --offset=40  # Next 40
  node test-result.js --cached --file=kernel    # Find errors in *kernel* files
  node test-result.js --cached --id=5           # Get error #5 details

Output per error:
  { id, testFile, sourceFile, test, message, line, expected, received }

AI receives 40 errors, fixes them concurrently (each error = different file).
`);
    return;
  }

  const cwd = process.cwd();
  const testPath = args._?.[0] || '';
  const stateDir = path.join(cwd, '.project-index');
  const resultFile = path.join(stateDir, RESULT_FILE);
  const offset = parseInt(args.offset) || 0;
  const limit = parseInt(args.limit) || 40;

  // --save: run tests and persist
  if (args.save) {
    console.error('Running vitest...');
    const result = await runVitest(testPath, cwd);
    await fs.mkdir(stateDir, { recursive: true });
    await writeJsonSafe(resultFile, result);
    console.error(`Saved: ${result.failed} failed, ${result.errors.length} error details`);
    console.log(formatSummary(result));
    return;
  }

  // All other modes require cached data
  const result = await readJsonSafe(resultFile, null);
  if (!result) {
    console.error('No cached result. Run with --save first.');
    process.exit(1);
  }

  if (args.summary) {
    console.log(formatSummary(result));
    return;
  }

  // --file: 按文件名模糊查询
  if (args.file) {
    const pattern = args.file.toLowerCase();
    const matched = (result.errors || []).filter(e =>
      e.testFile?.toLowerCase().includes(pattern) ||
      e.sourceFile?.toLowerCase().includes(pattern)
    );
    console.log(JSON.stringify({
      query: args.file,
      found: matched.length,
      errors: matched
    }, null, 2));
    return;
  }

  // --id: 按错误 ID 查询
  if (args.id) {
    const id = parseInt(args.id);
    const error = (result.errors || []).find(e => e.id === id);
    if (error) {
      console.log(JSON.stringify(error, null, 2));
    } else {
      console.log(JSON.stringify({ error: `Error #${id} not found` }));
    }
    return;
  }

  if (args.errors) {
    const allErrors = result.errors || [];
    const sliced = allErrors.slice(offset, offset + limit);
    const endIndex = Math.min(offset + limit, allErrors.length);

    console.log(JSON.stringify({
      total: result.total,
      passed: result.passed,
      failed: result.failed,
      timestamp: result.timestamp,
      showing: `${offset + 1}-${endIndex} of ${allErrors.length} errors`,
      hasMore: endIndex < allErrors.length,
      nextOffset: endIndex < allErrors.length ? endIndex : null,
      concurrency: sliced.length,  // AI 可以并发处理这些
      errors: sliced
    }, null, 2));
    return;
  }

  // Default: show summary without error details
  console.log(JSON.stringify({
    total: result.total,
    passed: result.passed,
    failed: result.failed,
    skipped: result.skipped,
    duration: result.duration,
    timestamp: result.timestamp,
    errorCount: result.errors?.length || 0,
    hint: 'Use --errors to get error list, AI can fix concurrently'
  }, null, 2));
}

main().catch(e => {
  console.error('Error:', e.message);
  process.exit(1);
});
