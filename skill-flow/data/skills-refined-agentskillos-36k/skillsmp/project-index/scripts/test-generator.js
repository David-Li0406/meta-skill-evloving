#!/usr/bin/env node
/**
 * Test Generator - Batch test file generation using LLM
 *
 * Scans source files, identifies missing/stale tests, and generates
 * test files via codeagent-wrapper. Progress tracked in Dashboard.
 *
 * Usage:
 *   node test-generator.js [options] [path]
 *
 * Modes:
 *   --untested       Generate tests for untested files (default)
 *   --stale          Regenerate stale tests
 *   --all            Both untested and stale
 *
 * Execution:
 *   --dry-run        Preview only
 *   --concurrency=N  Override concurrency (default 3)
 *   --resume         Resume from checkpoint
 *   --daemon         Run in background
 *   --status         Show last result
 *   --help           Show help
 */

import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { execSync, spawn } from 'child_process';
import { BatchRunner } from './batch-llm-runner.js';
import { loadConfig, parseArgs, shouldProcess, readFileSafe } from './shared.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const CODE_EXTENSIONS = new Set(['.js', '.mjs', '.cjs', '.ts', '.tsx']);
const IGNORE_DIRS = new Set([
  'node_modules', '.git', 'dist', 'build', 'coverage', 'tests', '__tests__'
]);

/**
 * Get test status from test-status.js
 * @param {string} cwd
 * @param {string} filter - 'untested' | 'stale' | null (all)
 * @returns {Promise<Array<{path: string, status: string, testFiles?: string[]}>>}
 */
async function getTestStatus(cwd, filter = null) {
  try {
    const script = path.join(__dirname, 'test-status.js');
    let args = '--json';
    if (filter === 'untested') args += ' --untested';
    else if (filter === 'stale') args += ' --stale';

    const result = execSync(`node "${script}" ${args}`, {
      encoding: 'utf-8',
      cwd,
      timeout: 120000
    });
    const data = JSON.parse(result);
    return data.files || [];
  } catch (e) {
    console.error('Failed to get test status:', e.message);
    return [];
  }
}

/**
 * Read source file content (head portion for prompt)
 * @param {string} filePath
 * @param {number} maxLines
 * @returns {Promise<string>}
 */
async function readSourceFile(filePath, maxLines = 100) {
  try {
    const content = await fs.readFile(filePath, 'utf-8');
    const lines = content.split('\n');
    return lines.slice(0, maxLines).join('\n');
  } catch {
    return '';
  }
}

/**
 * Extract exports from source file
 * @param {string} content
 * @returns {string[]}
 */
function extractExports(content) {
  const exports = [];

  // Named exports: export function X, export const X, export class X
  const namedRegex = /export\s+(function|const|let|var|class|async\s+function)\s+(\w+)/g;
  let match;
  while ((match = namedRegex.exec(content)) !== null) {
    exports.push(match[2]);
  }

  // Re-exports: export { X, Y } from
  const reexportRegex = /export\s*\{\s*([^}]+)\s*\}/g;
  while ((match = reexportRegex.exec(content)) !== null) {
    const symbols = match[1].split(',').map(s => {
      const asMatch = s.trim().match(/(\w+)\s+as\s+(\w+)/);
      return asMatch ? asMatch[2] : s.trim();
    }).filter(Boolean);
    exports.push(...symbols);
  }

  // Default export
  if (/export\s+default/.test(content)) {
    exports.push('default');
  }

  return [...new Set(exports)];
}

/**
 * Calculate relative import path from test to source
 * @param {string} sourcePath - e.g. js/agents/core/kernel.js
 * @param {string} testPath - e.g. tests/unit/agents/core/kernel.test.js
 * @returns {string}
 */
function getRelativeImport(sourcePath, testPath) {
  const testDir = path.dirname(testPath);
  const sourceDir = path.dirname(sourcePath);

  // Calculate depth from tests/unit/X to js/X
  const testParts = testDir.split('/');
  const sourceParts = sourceDir.split('/');

  // tests/unit/agents/core -> 4 parts
  // need to go up 4 levels then into js/agents/core
  const ups = '../'.repeat(testParts.length);
  return ups + sourcePath;
}

/**
 * Convert source path to expected test path
 * @param {string} sourcePath
 * @returns {string}
 */
function sourceToTestPath(sourcePath) {
  // js/agents/core/kernel.js -> tests/unit/agents/core/kernel.test.js
  const withoutJs = sourcePath.replace(/^js\//, '');
  const parsed = path.parse(withoutJs);
  return path.join('tests/unit', parsed.dir, `${parsed.name}.test.js`);
}

function printHelp() {
  console.log(`Usage:
  node test-generator.js [options] [path]

Modes:
  --untested       Generate tests for untested files (default)
  --stale          Regenerate stale tests
  --all            Both untested and stale

Execution:
  --dry-run        Preview only
  --concurrency=N  Override concurrency (default 3)
  --resume         Resume from checkpoint
  --retry-failed   Retry failed tasks only
  --daemon         Run in background
  --status         Show last result
  --help           Show help

Examples:
  node test-generator.js js/agents/core --dry-run
  node test-generator.js --untested --concurrency=2
`);
}

async function main() {
  const rawArgs = process.argv.slice(2);
  const cwd = process.cwd();

  if (rawArgs.includes('--help') || rawArgs.includes('-h')) {
    printHelp();
    return;
  }

  const args = parseArgs(rawArgs, {
    dryRun: false,
    resume: false,
    retryFailed: false,
    status: false,
    daemon: false,
    untested: false,
    stale: false,
    all: false
  });

  if (args.status) {
    const resultPath = path.join(cwd, '.project-index', '.test-generator-result.json');
    try {
      const result = await fs.readFile(resultPath, 'utf-8');
      console.log(result);
    } catch {
      console.log('No result found.');
    }
    return;
  }

  // Daemon mode
  if (args.daemon) {
    const scriptPath = fileURLToPath(import.meta.url);
    const childArgs = rawArgs.filter(arg => !arg.startsWith('--daemon'));

    const child = spawn(process.execPath, [scriptPath, ...childArgs], {
      cwd,
      detached: true,
      stdio: 'ignore'
    });
    child.unref();

    console.log(`test-generator started in background (pid: ${child.pid})`);
    console.log(`Check progress: node "${scriptPath}" --status`);
    return;
  }

  // Determine mode
  let filter = null;
  if (args.all) filter = null;
  else if (args.stale) filter = 'stale';
  else filter = 'untested';  // default

  // Path filter
  const pathFilter = args._?.[0] || null;

  // Load config
  const config = await loadConfig(cwd);
  let concurrency = 3;  // Lower default for test generation (more expensive)
  if (args.concurrency !== undefined) {
    concurrency = parseInt(args.concurrency, 10) || 3;
  }

  // Get files needing tests
  console.log(`Mode: ${filter || 'all'}`);
  console.log(`Scanning for files needing tests...`);

  let files = await getTestStatus(cwd, filter);

  // Apply path filter
  if (pathFilter) {
    files = files.filter(f => f.path.startsWith(pathFilter));
    console.log(`Scope: ${pathFilter}`);
  }

  // Apply config include/ignore
  files = files.filter(f => shouldProcess(f.path, config));

  // Sort by path depth (deeper first for better context)
  files.sort((a, b) => {
    const depthA = a.path.split('/').length;
    const depthB = b.path.split('/').length;
    return depthB - depthA;
  });

  if (args.dryRun) {
    console.log(`\nDry run: ${files.length} files need tests`);
    for (const f of files.slice(0, 30)) {
      const testPath = sourceToTestPath(f.path);
      console.log(`- ${f.path} → ${testPath}`);
    }
    if (files.length > 30) {
      console.log(`... and ${files.length - 30} more`);
    }
    return;
  }

  if (files.length === 0 && !args.resume) {
    console.log('No files need tests.');
    return;
  }

  console.log(`Files to process: ${files.length}`);
  console.log(`Concurrency: ${concurrency}`);

  // Load testing config for prompt
  const testingConfig = config.testing || {};
  const conventions = config.conventions || {};

  const runner = new BatchRunner({
    name: 'test-generator',
    concurrency,
    timeout: config.timeout || 300000,  // 5 min per file
    stateDir: cwd,
    silent: true
  });

  await runner.run({
    scan: async () => files.map(f => ({
      id: f.path,
      sourcePath: f.path,
      fullSourcePath: path.join(cwd, f.path),
      testPath: sourceToTestPath(f.path),
      fullTestPath: path.join(cwd, sourceToTestPath(f.path)),
      status: f.status,
      testingConfig,
      conventions
    })),

    buildPrompt: async function (item) {
      const sourceContent = await readSourceFile(item.fullSourcePath, 150);
      const exports = extractExports(sourceContent);
      const importPath = getRelativeImport(item.sourcePath, item.testPath);

      // Check if there's an existing test to update
      let existingTest = '';
      if (item.status === 'stale') {
        existingTest = await readFileSafe(item.fullTestPath, 100) || '';
      }

      const testRequirements = item.testingConfig.antiPatterns
        ? `\n避免以下反模式:\n${item.testingConfig.antiPatterns.map(p => `- ${p}`).join('\n')}`
        : '';

      const boundaryConditions = item.testingConfig.boundaryConditions
        ? `\n必须测试的边界条件:\n${item.testingConfig.boundaryConditions.map(c => `- ${c}`).join('\n')}`
        : '';

      return `你是一个测试工程师。请为以下源文件生成完整的单元测试。

## 源文件
路径: ${item.sourcePath}
导出符号: ${exports.join(', ') || '(请从代码分析)'}

\`\`\`javascript
${sourceContent}
\`\`\`

## 测试文件
路径: ${item.testPath}
导入路径: ${importPath}

${existingTest ? `## 现有测试 (需要更新)\n\`\`\`javascript\n${existingTest}\n\`\`\`\n` : ''}

## 要求
- 使用 vitest 框架 (import { describe, it, expect, vi, beforeEach } from 'vitest')
- 每个导出函数/类单独 describe 块
- 包含正常路径、边界条件、错误处理测试
- 使用 vi.mock() 模拟外部依赖
- 测试应该是独立的，不依赖执行顺序
${testRequirements}
${boundaryConditions}

## 输出格式
只输出完整的测试文件代码，不要其他解释。代码必须以 \`\`\`javascript 开始，以 \`\`\` 结束。`;
    },

    handleResult: async function (item, result) {
      // Extract code from LLM response
      const codeMatch = result.match(/```(?:javascript|js)?\n([\s\S]*?)```/);
      if (!codeMatch) {
        return {
          success: false,
          error: 'No code block found in response',
          item
        };
      }

      const testCode = codeMatch[1].trim();

      // Validate it looks like a test file
      if (!testCode.includes('describe') || !testCode.includes('it(')) {
        return {
          success: false,
          error: 'Generated code does not appear to be a valid test file',
          item
        };
      }

      // Ensure test directory exists
      const testDir = path.dirname(item.fullTestPath);
      await fs.mkdir(testDir, { recursive: true });

      // Write test file
      await fs.writeFile(item.fullTestPath, testCode, 'utf-8');

      return {
        success: true,
        testPath: item.testPath,
        sourcePath: item.sourcePath,
        lines: testCode.split('\n').length
      };
    }
  }, {
    resume: args.resume,
    retryFailed: args.retryFailed,
    cwd
  });

  console.log('\nTest generation complete.');
  console.log(`Check results: node "${fileURLToPath(import.meta.url)}" --status`);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
