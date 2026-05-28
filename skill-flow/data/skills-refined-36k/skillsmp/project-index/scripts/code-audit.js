#!/usr/bin/env node
/**
 * Code Audit - Security and quality audit for subdirectories
 *
 * Usage:
 *   node code-audit.js [--all | path1 path2 ...]
 *   node code-audit.js --status
 *   node code-audit.js --resume
 */

import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { BatchRunner } from './batch-llm-runner.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const IGNORE_DIRS = new Set([
  'node_modules', '.git', 'dist', 'build', '.next', '__pycache__',
  'venv', '.venv', 'target', 'vendor', '.cache', 'coverage'
]);

const CODE_EXTENSIONS = new Set([
  '.js', '.ts', '.jsx', '.tsx', '.mjs', '.cjs',
  '.py', '.go', '.rs', '.java', '.rb', '.php'
]);

const LARGE_THRESHOLD = { files: 5, lines: 200 };

const TEST_FILE_MARKERS = ['.test.', '.spec.'];

async function exists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

function isTestFile(fileName) {
  return TEST_FILE_MARKERS.some(marker => fileName.includes(marker));
}

/**
 * Find directories with code files
 */
async function findCodeDirs(dir, rootPath, maxDepth = 3, depth = 0) {
  const results = [];
  if (depth > maxDepth) return results;

  try {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    let hasCode = false;

    for (const entry of entries) {
      if (entry.isFile()) {
        const ext = path.extname(entry.name).toLowerCase();
        if (CODE_EXTENSIONS.has(ext)) hasCode = true;
      }
    }

    if (hasCode) {
      results.push(dir);
    }

    for (const entry of entries) {
      if (entry.isDirectory() && !IGNORE_DIRS.has(entry.name)) {
        const subResults = await findCodeDirs(
          path.join(dir, entry.name),
          rootPath,
          maxDepth,
          depth + 1
        );
        results.push(...subResults);
      }
    }
  } catch {}

  return results;
}

/**
 * Get code file count and line count for a directory (non-recursive)
 */
async function getDirStats(dir) {
  let fileCount = 0;
  let lineCount = 0;
  let entries = [];

  try {
    entries = await fs.readdir(dir, { withFileTypes: true });
  } catch {
    return { fileCount, lineCount };
  }

  for (const entry of entries) {
    if (!entry.isFile()) continue;
    const ext = path.extname(entry.name).toLowerCase();
    if (!CODE_EXTENSIONS.has(ext)) continue;
    if (isTestFile(entry.name)) continue;

    fileCount++;
    try {
      const filePath = path.join(dir, entry.name);
      const fileContent = await fs.readFile(filePath, 'utf-8');
      lineCount += fileContent.split('\n').length;
    } catch {}
  }

  return { fileCount, lineCount };
}

/**
 * Find unaudited small subdirectories (direct children only)
 */
async function findUnauditedSmallSubdirs(parentDir) {
  const results = [];
  let entries = [];

  try {
    entries = await fs.readdir(parentDir, { withFileTypes: true });
  } catch {
    return results;
  }

  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    if (IGNORE_DIRS.has(entry.name) || entry.name.startsWith('.')) continue;

    const fullPath = path.join(parentDir, entry.name);
    const hasAudit = await exists(path.join(fullPath, 'AUDIT.md'));
    if (hasAudit) continue;

    const stats = await getDirStats(fullPath);
    if (stats.fileCount < LARGE_THRESHOLD.files && stats.lineCount < LARGE_THRESHOLD.lines) {
      results.push({
        path: path.relative(parentDir, fullPath),
        fullPath,
        fileCount: stats.fileCount,
        lineCount: stats.lineCount
      });
    }
  }

  return results;
}

/**
 * Read code files from a directory (limited)
 */
async function readCodeFiles(dir, maxFiles = 5, maxLines = 50) {
  let content = '';
  let count = 0;
  let entries = [];

  try {
    entries = await fs.readdir(dir, { withFileTypes: true });
  } catch {
    return content;
  }

  for (const entry of entries) {
    if (count >= maxFiles) break;
    if (!entry.isFile()) continue;

    const ext = path.extname(entry.name).toLowerCase();
    if (!CODE_EXTENSIONS.has(ext)) continue;

    const filePath = path.join(dir, entry.name);
    try {
      const fileContent = await fs.readFile(filePath, 'utf-8');
      const lines = fileContent.split('\n').slice(0, maxLines);

      content += `\n--- ${entry.name} ---\n${lines.join('\n')}\n`;
      count++;
    } catch {}
  }

  return content;
}

async function main() {
  const args = process.argv.slice(2);
  const cwd = process.cwd();

  if (args.includes('--status')) {
    try {
      const result = await fs.readFile(
        path.join(__dirname, '.code-audit-result.json'),
        'utf-8'
      );
      console.log(result);
    } catch {
      console.log('No audit result found.');
    }
    return;
  }

  const runner = new BatchRunner({
    name: 'code-audit',
    concurrency: 8,
    timeout: 120000,
    stateDir: __dirname
  });

  await runner.run({
    scan: async (cwd) => {
      const dirs = await findCodeDirs(cwd, cwd);
      const largeDirs = [];

      for (const dir of dirs) {
        const stats = await getDirStats(dir);
        if (stats.fileCount >= LARGE_THRESHOLD.files || stats.lineCount >= LARGE_THRESHOLD.lines) {
          largeDirs.push({
            id: path.relative(cwd, dir) || '.',
            path: dir
          });
        }
      }

      return largeDirs;
    },

    buildPrompt: async (item) => {
      const codeContent = await readCodeFiles(item.path, 8, 100);
      const smallDirs = await findUnauditedSmallSubdirs(item.path);

      let subdirContext = '';
      if (smallDirs.length > 0) {
        subdirContext = `\n\n## 未独立审计的小子目录\n以下子目录因规模较小未生成独立 AUDIT.md，请一并审查：\n`;
        for (const d of smallDirs) {
          subdirContext += `- ${d.path} (${d.fileCount} 文件, ${d.lineCount} 行)\n`;
          const subCode = await readCodeFiles(d.fullPath, 3, 30);
          if (subCode) subdirContext += subCode + '\n';
        }
      }

      return `你是一个代码安全审计专家。请审查以下代码目录，检查：
1. 安全漏洞（注入、XSS、敏感信息泄露等）
2. 代码质量问题（错误处理、资源泄漏等）
3. 最佳实践违反

目录: ${item.id}

${codeContent}
${subdirContext}

请以 JSON 格式返回：
{
  "severity": "low|medium|high|critical",
  "issues": [{"type": "...", "description": "...", "file": "...", "line": "..."}],
  "summary": "简要总结"
}`;
    },

    handleResult: async (item, result) => {
      if (!result.success) {
        return { status: 'llm_error', reason: result.error, sessionId: result.sessionId };
      }

      // Try to parse JSON from output
      const jsonMatch = result.output.match(/\{[\s\S]*"severity"[\s\S]*\}/);
      if (jsonMatch) {
        try {
          const audit = JSON.parse(jsonMatch[0]);

          // Write audit result to file
          const auditFile = path.join(item.path, 'AUDIT.md');
          const content = `# Code Audit - ${item.id}

Generated: ${new Date().toISOString()}

## Severity: ${audit.severity}

## Summary
${audit.summary}

## Issues
${audit.issues?.map(i => `- **${i.type}** (${i.file}:${i.line || '?'}): ${i.description}`).join('\n') || 'None found'}
`;
          await fs.writeFile(auditFile, content);

          return {
            status: audit.severity === 'critical' ? 'critical' : 'audited',
            severity: audit.severity,
            issueCount: audit.issues?.length || 0
          };
        } catch {
          return { status: 'parse_error', sessionId: result.sessionId };
        }
      }

      return { status: 'unclear', sessionId: result.sessionId };
    }
  }, {
    resume: args.includes('--resume'),
    cwd
  });
}

main().catch(console.error);
