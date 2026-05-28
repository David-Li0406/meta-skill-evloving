---
name: audit-fix
description: 审计问题修复技能。读取模块的 AUDIT.md，逐个修复安全/质量问题，修复后归档到 AUDIT_HISTORY.md。严格约束只修改 AUDIT.md 列出的文件。
---

# audit-fix (审计修复)

修复 AUDIT.md 中记录的安全和代码质量问题，保持修改范围最小化。

## 触发方式

```bash
/audit-fix <module-path>                    # 修复指定模块
/audit-fix <module-path> --issues 1,3,5     # 只修复指定 issue
/audit-fix <module-path> --dry-run          # 预览修复计划
/audit-fix --batch <severity>               # 批量修复指定级别 (critical/high/medium/low)
```

## 核心约束

⚠️ **严格限制**: 只能修改 AUDIT.md 列出的文件和行号
❌ **禁止**: 扩展修改范围、重构其他代码、添加新功能、"顺便"优化
✅ **允许**: 新增必要的工具函数文件（如 path-utils.js）

## 工作流程

### Phase 1: 读取审计报告

```bash
# 检查 AUDIT.md 存在
cat <module-path>/AUDIT.md

# 或使用脚本查看
node ~/.claude/skills/project-index/scripts/audit-archive.js <module-path> --show
```

解析内容：
- Severity 级别
- Issues 列表（每个有 File:Line, Description, Suggestion）

### Phase 2: 逐个修复

对每个 issue：

1. **读取目标文件** - 定位到指定行号
2. **理解问题** - 根据 Description 理解风险
3. **应用修复** - 按 Suggestion 实现，保持最小改动
4. **立即归档** - 修复后立即归档该 issue

```bash
# 归档单个 issue
node ~/.claude/skills/project-index/scripts/audit-archive.js <module-path> <issue-id>
```

### Phase 3: 清理与提交

1. **提交代码** - 只提交修改的源文件（AUDIT.md 被 gitignore）
2. **更新 CLAUDE.md**:
   - 功能有变化（如新增参数、改变默认行为）→ 修改 CLAUDE.md 内容
   - 功能无变化（纯 bug 修复）→ 只需 `touch CLAUDE.md` 更新时间戳

```bash
# 提交格式
git commit -m "fix(<module>): resolve N security audit issues

- issue1: <brief description>
- issue2: <brief description>
...

BREAKING: <if any breaking changes>"
```

## 常见问题类型及修复模式

### 1. path-traversal (路径穿越)
```javascript
// Before
const absPath = p.startsWith('/') ? p : `${workDir}/${p}`;

// After
import path from 'path';
const resolved = path.resolve(workDir, p);
if (!resolved.startsWith(workDir + path.sep)) {
  throw new Error('Path traversal detected');
}
```

### 2. silent-catch (静默捕获)
```javascript
// Before
} catch { /* ignore */ }

// After
} catch (err) {
  return { error: err.message, available: false };
}
```

### 3. permission-bypass (权限绕过)
```javascript
// Before
const defaultHandler = async () => 'allow-once';

// After
const defaultHandler = async () => 'deny';
```

### 4. browser-compat (浏览器兼容)
```javascript
// Before
workDir = process.cwd()

// After - 要求显式传入
if (!workDir) {
  throw new Error('workDir is required');
}
```

### 5. jsdoc (文档缺失)
```javascript
// Before
export function foo(x, y) { ... }

// After
/**
 * Brief description
 * @param {string} x - Description
 * @param {number} y - Description
 * @returns {boolean} Description
 */
export function foo(x, y) { ... }
```

### 6. event-naming (事件命名)
```javascript
// Before
emit('agent.step.completed', data);

// After
emit('agent:stepCompleted', data);
```

### 7. timeout-not-enforced (超时未强制)
```javascript
// Before
const proc = spawn(cmd, args);

// After
const proc = spawn(cmd, args);
const timer = setTimeout(() => proc.kill('SIGTERM'), timeoutMs);
proc.on('exit', () => clearTimeout(timer));
```

## 批量执行

### 方式 1: 直接并行 (无 Kanban)

使用 Task 工具并行修复多个模块：

```javascript
// Claude 会话中执行（建议 6-8 并发）
const modules = ['js/agents/core', 'js/agents/runtime', ...];
// 7 个 Task 工具并行调用，每个 run_in_background: true
```

### 方式 2: 先导入 Kanban 再批量

```bash
# 1. 导入审计任务到 Kanban
node ~/.claude/skills/audit-fix/import-to-kanban.js

# 或只导入 CRITICAL
node ~/.claude/skills/audit-fix/import-to-kanban.js --severity=critical

# 预览模式
node ~/.claude/skills/audit-fix/import-to-kanban.js --dry-run

# 2. 查看导入的任务
node ~/.claude/skills/kanban/kanban-cli.js list --status=todo

# 3. 批量执行
/kanban-batch --priority=0
```

### 检查后台任务进度

```bash
# 查看所有后台任务
ls /tmp/claude/*/tasks/*.output

# 查看单个任务输出
tail -50 /tmp/claude/-mnt-f-pb-paper-burner/tasks/<agent-id>.output

# 检查审计修复状态
node ~/.claude/skills/project-index/scripts/audit-status.js
```

## Kanban 集成

审计修复可与 Code Kanban 结合，提供任务追踪和隔离开发环境。

### 方式 1: CLI 创建任务

```bash
CLI="$HOME/.claude/skills/kanban/kanban-cli.js"

# 创建审计任务
node "$CLI" add "[AUDIT] js/agents/core/sandbox/system (7 issues)" \
  --priority=0 \
  --tags=type/audit,severity/critical \
  --description="修复 AUDIT.md 中的 7 个安全问题"

# 查看待办
node "$CLI" list --status=todo
```

### 方式 2: 使用 kanban-implement

```bash
# 认领任务并在独立 worktree 中修复
/kanban-implement <task-id>
```

Worktree 隔离的好处：
- 并行修复多个模块互不干扰
- 修复失败可直接丢弃分支
- 便于 code review

### 方式 3: 批量编排 (kanban-batch)

```bash
# 把所有 CRITICAL 审计问题导入 Kanban 后
/kanban-batch --priority=0
```

自动分析依赖关系，并行执行无依赖的任务。

### 任务状态更新

```bash
# 开始任务
node "$CLI" start <id>

# 完成任务
node "$CLI" done <id>
```

### 推荐工作流

```
1. audit-status.js 检查问题分布
   ↓
2. CLI 创建 Kanban 任务 (P0=CRITICAL, P1=HIGH...)
   ↓
3. /kanban-batch 或手动 /kanban-implement
   ↓
4. 每个模块修复后：
   - audit-archive.js 归档
   - git commit
   - node "$CLI" done <id>
```

## 验证清单

修复完成后检查：

- [ ] 所有 issues 已归档 (`--show` 返回 Issues: 0)
- [ ] 代码已提交（不含 AUDIT.md）
- [ ] CLAUDE.md 时间戳已更新
- [ ] 无引入新的 lint/type 错误
- [ ] Breaking changes 已在 commit message 说明

## 依赖

- `~/.claude/skills/project-index/scripts/audit-archive.js` - 归档脚本
- `~/.claude/skills/project-index/scripts/audit-status.js` - 状态检查

## 参考

- `/project-index` - 索引管理
- `/js-agents-entropy-scan` - 生成审计报告
