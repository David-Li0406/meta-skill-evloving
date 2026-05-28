#!/usr/bin/env node
/**
 * 批量导入审计任务到 Kanban
 *
 * Usage:
 *   node import-to-kanban.js                    # 导入所有审计模块
 *   node import-to-kanban.js --severity=critical # 只导入 CRITICAL
 *   node import-to-kanban.js --dry-run          # 预览不执行
 */

import { execSync } from 'child_process';
import { existsSync, readFileSync } from 'fs';
import path from 'path';

const KANBAN_CLI = process.env.HOME + '/.claude/skills/kanban/kanban-cli.js';
const AUDIT_STATUS = process.env.HOME + '/.claude/skills/project-index/scripts/audit-status.js';

// 解析参数
const args = process.argv.slice(2);
const dryRun = args.includes('--dry-run');
const severityFilter = args.find(a => a.startsWith('--severity='))?.split('=')[1];

// 优先级映射
const SEVERITY_TO_PRIORITY = {
  critical: 0,
  high: 1,
  medium: 2,
  low: 3,
};

async function main() {
  console.log('正在获取审计状态...\n');

  // 运行 audit-status 获取 JSON 输出
  let statusOutput;
  try {
    statusOutput = execSync(`node "${AUDIT_STATUS}" --json`, {
      encoding: 'utf-8',
      cwd: process.cwd(),
    });
  } catch (err) {
    console.error('无法获取审计状态:', err.message);
    process.exit(1);
  }

  const status = JSON.parse(statusOutput);
  const modules = [];

  // 按严重程度收集模块
  for (const [severity, items] of Object.entries(status.bySeverity || {})) {
    if (severityFilter && severity.toLowerCase() !== severityFilter.toLowerCase()) {
      continue;
    }

    for (const item of items) {
      modules.push({
        path: item.path,
        severity: severity.toLowerCase(),
        issues: item.issues,
        priority: SEVERITY_TO_PRIORITY[severity.toLowerCase()] ?? 2,
      });
    }
  }

  if (modules.length === 0) {
    console.log('没有找到需要导入的审计模块');
    return;
  }

  console.log(`找到 ${modules.length} 个模块待导入:\n`);

  // 按优先级排序
  modules.sort((a, b) => a.priority - b.priority);

  for (const mod of modules) {
    const title = `[AUDIT] ${mod.path} (${mod.issues} issues)`;
    const tags = `type/audit,severity/${mod.severity}`;
    const desc = `修复 ${mod.path}/AUDIT.md 中的 ${mod.issues} 个问题`;

    console.log(`  [P${mod.priority}] ${title}`);

    if (!dryRun) {
      try {
        execSync(
          `node "${KANBAN_CLI}" add "${title}" --priority=${mod.priority} --tags=${tags} --description="${desc}"`,
          { encoding: 'utf-8', stdio: 'pipe' }
        );
      } catch (err) {
        console.error(`    ❌ 创建失败: ${err.message}`);
      }
    }
  }

  console.log(`\n${dryRun ? '[DRY RUN] ' : ''}共 ${modules.length} 个任务`);

  if (dryRun) {
    console.log('\n使用不带 --dry-run 参数执行实际导入');
  } else {
    console.log('\n使用 `node ~/.claude/skills/kanban/kanban-cli.js list --status=todo` 查看');
  }
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
