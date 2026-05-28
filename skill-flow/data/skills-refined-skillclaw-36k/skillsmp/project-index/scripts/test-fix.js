#!/usr/bin/env node
/**
 * Test Fix - Automated test error fixing with BatchRunner
 *
 * Features:
 * - Reads errors from .test-result.json (created by test-result.js --save)
 * - Uses BatchRunner for proper concurrency pool execution
 * - LLM-based fix generation for each error
 * - Tracks fixes in TEST_FIX_HISTORY.md
 *
 * Usage:
 *   node test-fix.js [options]
 *
 * Options:
 *   --dry-run        Preview fixes without applying
 *   --concurrency=N  Parallel fix attempts (default 6)
 *   --offset=N       Start from error N (default 0)
 *   --limit=N        Process N errors (default 40)
 *   --resume         Resume from checkpoint
 *   --retry-failed   Retry only failed tasks
 *   --status         Show last result
 *   --help           Show help
 *
 * Workflow:
 *   1. node test-result.js --save     # Run tests, cache results
 *   2. node test-fix.js               # Fix first 40 errors
 *   3. node test-fix.js --offset=40   # Fix next 40
 */

import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { BatchRunner, runCodeagent } from './batch-llm-runner.js';
import {
  readJsonSafe,
  writeJsonSafe,
  parseArgs
} from './shared.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const RESULT_FILE = '.test-result.json';

const log = {
  info: (...args) => console.log('[test-fix]', ...args),
  warn: (...args) => console.warn('[test-fix]', ...args),
  error: (...args) => console.error('[test-fix]', ...args)
};

/**
 * Record fix to history
 * @param {object} item - Error item
 * @param {string} analysis - Fix analysis from LLM
 * @param {string} cwd - Working directory
 */
async function recordFix(item, analysis, cwd) {
  const historyFile = path.join(cwd, '.project-index', 'TEST_FIX_HISTORY.md');

  const entry = `
## ${new Date().toISOString().split('T')[0]} - ${item.testFile}

- **Test**: ${item.test}
- **Source**: ${item.sourceFile}
- **Analysis**: ${analysis?.slice(0, 200) || 'Fixed by codex'}
`;

  try {
    await fs.mkdir(path.dirname(historyFile), { recursive: true });
    const existing = await fs.readFile(historyFile, 'utf-8').catch(() => '# Test Fix History\n');
    await fs.writeFile(historyFile, existing + entry);
  } catch (e) {
    log.warn(`Failed to record fix history: ${e.message}`);
  }
}

/**
 * Load errors from cached test result
 * @param {string} cwd - Working directory
 * @param {number} offset - Start index
 * @param {number} limit - Number of errors to process
 * @returns {Promise<{errors: Array, total: number}>}
 */
async function loadCachedErrors(cwd, offset, limit) {
  const stateDir = path.join(cwd, '.project-index');
  const resultFile = path.join(stateDir, RESULT_FILE);
  const result = await readJsonSafe(resultFile, null);

  if (!result || !result.errors) {
    return { errors: [], total: 0, failed: 0 };
  }

  const errors = result.errors.slice(offset, offset + limit);
  return {
    errors,
    total: result.total,
    failed: result.failed,
    passed: result.passed,
    hasMore: offset + limit < result.errors.length
  };
}

/**
 * Main entry point - uses BatchRunner for concurrent fixing
 */
async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.help) {
    console.log(`
Test Fix - Automated test error fixing with BatchRunner

Usage: node test-fix.js [options]

Options:
  --dry-run        Preview fixes without applying
  --concurrency=N  Parallel fix attempts (default 6)
  --offset=N       Start from error N (default 0)
  --limit=N        Process N errors (default 40)
  --resume         Resume from checkpoint
  --retry-failed   Retry only failed tasks
  --status         Show last result
  --help           Show this help

Workflow:
  1. node test-result.js --save     # Run tests, cache results
  2. node test-fix.js               # Fix first 40 errors
  3. node test-fix.js --offset=40   # Fix next 40
`);
    return;
  }

  const cwd = process.cwd();
  const dryRun = args['dry-run'] || false;
  const concurrency = parseInt(args.concurrency) || 6;
  const offset = parseInt(args.offset) || 0;
  const limit = parseInt(args.limit) || 40;

  // Status check
  if (args.status) {
    const runner = new BatchRunner({ name: 'test-fix', stateDir: cwd });
    const status = await runner.getStatus();
    console.log(JSON.stringify(status, null, 2));
    return;
  }

  // Load cached errors from test-result.js
  const cached = await loadCachedErrors(cwd, offset, limit);
  if (cached.errors.length === 0) {
    log.error('No cached errors. Run: node test-result.js --save');
    process.exit(1);
  }

  log.info(`Loaded ${cached.errors.length} errors (${offset + 1}-${offset + cached.errors.length} of ${cached.failed})`);

  // Create BatchRunner
  const runner = new BatchRunner({
    name: 'test-fix',
    concurrency,
    timeout: 1800000, // 30 minutes
    stateDir: cwd
  });

  // Define handlers for BatchRunner
  const handlers = {
    /**
     * Scan returns items to process (from cached errors)
     * Groups errors by testFile for efficient batch fixing
     */
    scan: async () => {
      // Load previous task states to filter completed
      const tasksFile = path.join(cwd, '.project-index', `.test-fix-tasks.json`);
      let completedIds = new Set();
      try {
        const prev = JSON.parse(await fs.readFile(tasksFile, 'utf-8'));
        if (prev.tasks) {
          completedIds = new Set(
            prev.tasks
              .filter(t => t.status === 'completed')
              .map(t => t.id)
          );
        }
      } catch { /* no previous state */ }

      // Group errors by testFile
      const fileGroups = new Map();
      for (const err of cached.errors) {
        const key = err.testFile;
        if (!fileGroups.has(key)) {
          fileGroups.set(key, {
            id: `file-${key.replace(/[^a-zA-Z0-9]/g, '-')}`,
            testFile: err.testFile,
            sourceFiles: new Set(),
            errors: []
          });
        }
        const group = fileGroups.get(key);
        if (err.sourceFile) group.sourceFiles.add(err.sourceFile);
        group.errors.push({
          test: err.test,
          message: err.message,
          line: err.line,
          expected: err.expected,
          received: err.received
        });
      }

      // Convert to array and filter completed
      const items = Array.from(fileGroups.values())
        .map(g => ({
          ...g,
          sourceFiles: Array.from(g.sourceFiles),
          errorCount: g.errors.length
        }))
        .filter(item => !completedIds.has(item.id));

      if (completedIds.size > 0) {
        log.info(`Skipped ${completedIds.size} already-fixed files`);
      }

      log.info(`Grouped ${cached.errors.length} errors into ${items.length} files`);
      return items;
    },

    /**
     * Build prompt for LLM - codex will directly modify files
     * Now handles multiple errors per file
     */
    buildPrompt: async (item) => {
      // Format all errors for this file
      const errorsSection = item.errors.map((err, i) => `
### 错误 ${i + 1}: ${err.test}
\`\`\`
${err.message?.slice(0, 1000) || 'No message'}
\`\`\`
${err.expected ? `- **Expected**: ${err.expected}` : ''}
${err.received ? `- **Received**: ${err.received}` : ''}`).join('\n');

      return `修复这个测试文件中的所有错误。

## 任务
修复测试文件中的 ${item.errorCount} 个错误。修复完成后，在最后一行输出结果状态。

## 测试文件
- **Test File**: ${item.testFile}
- **Related Source Files**: ${item.sourceFiles.join(', ') || 'N/A'}
- **Error Count**: ${item.errorCount}

## 错误列表
${errorsSection}

## 常见修复类型
1. **Import path 错误** - 计算正确的相对路径
2. **Event name 格式** - 冒号 vs 点: "foo:bar" vs "foo.bar"
3. **index.js 缺少 export** - 添加缺失的导出
4. **断言期望值错误** - 修正测试期望值或源码逻辑
5. **Mock 配置错误** - 修正 vi.mock/vi.spyOn 配置

## ⚠️ 禁止的反模式 (严格遵守)

### 1. 为测试通过而修改实现代码
❌ 测试期望 "tool:failed"，实现是 "tool.failed" → 修改实现代码
✅ 检查项目约定，修改测试断言匹配实际行为

**原则**: 测试验证现有行为，优先修改测试文件，不驱动实现变更。

### 2. 创建 Shim/桥接文件
❌ Import 路径不存在 → 创建 shim 文件 re-export 真实模块
✅ 修正测试的 import 路径指向实际模块位置

**原则**: 一个模块只有一个入口点，禁止创建重导出 shim。

### 3. 事件名/API 破坏性变更
❌ 在测试修复中顺便统一事件名格式
✅ 匹配现有行为，破坏性变更需独立 commit/PR

### 4. 动态添加 Polyfill/Wrapper
❌ 测试期望某方法 → 动态添加 prototype 方法
✅ 检查测试是否正确，如需新 API 在实现模块中正式添加

### 5. 重复 Emit 事件
❌ 为兼容新旧格式同时 emit 两种事件名
✅ 选择一种格式统一使用

## 执行步骤
1. 读取测试文件和相关源文件
2. 分析所有错误的根因（通常有共同原因）
3. **优先修改测试文件**，除非确认是实现 bug
4. 一次性修复所有问题

## 约束 (严格遵守，违反将导致系统崩溃)
- **绝对禁止** 运行任何测试命令: npm test, vitest, npx vitest, node, bun test 等
- **绝对禁止** 运行任何验证/检查命令，包括单个测试文件
- 只允许: 读取文件、修改文件、写入文件
- 测试结果已缓存，无需也不能验证修复
- 当前有多个并发任务，运行测试会导致系统内存耗尽

## 输出格式
修复完成后，在响应最后一行输出（必须是最后一行）：
- 成功: FIXED: <简短说明修复了什么>
- 失败: NOT_FIXABLE: <原因>`;
    },

    /**
     * Handle LLM result - check if codex fixed the file
     */
    handleResult: async (item, llmResult) => {
      if (!llmResult.success) {
        return { status: 'error', reason: llmResult.error };
      }

      const output = llmResult.output || '';

      // Check for FIXED or NOT_FIXABLE in output
      const fixedMatch = output.match(/FIXED:\s*(.+?)(?:\n|$)/i);
      const notFixableMatch = output.match(/NOT_FIXABLE:\s*(.+?)(?:\n|$)/i);

      if (fixedMatch) {
        const analysis = fixedMatch[1].trim();
        if (!dryRun) {
          await recordFix(item, analysis, cwd);
        }
        log.info(`  Fixed: ${analysis}`);
        return { status: 'fixed', analysis };
      }

      if (notFixableMatch) {
        const reason = notFixableMatch[1].trim();
        log.info(`  Not fixable: ${reason}`);
        return { status: 'skipped', reason };
      }

      // No clear status, check if output suggests completion
      if (output.includes('修改') || output.includes('fixed') || output.includes('修复')) {
        if (!dryRun) {
          await recordFix(item, 'Implicit fix detected', cwd);
        }
        return { status: 'fixed', analysis: 'Implicit fix detected from output' };
      }

      return { status: 'error', reason: 'No clear fix status in output' };
    }
  };

  // Run with BatchRunner
  const result = await runner.run(handlers, {
    resume: args.resume,
    retryFailed: args['retry-failed'],
    cwd
  });

  // Summary
  log.info(`\n=== Summary ===`);
  log.info(`Processed: ${result.processed}`);
  log.info(`By status: ${JSON.stringify(result.byStatus)}`);
  if (cached.hasMore) {
    log.info(`\nMore errors available. Run: node test-fix.js --offset=${offset + limit}`);
  }
}

main().catch(e => {
  console.error('Fatal error:', e);
  process.exit(1);
});
