# 脚本参考

所有脚本位于 `scripts/` 目录。

## 核心脚本

### scan.js

扫描项目结构，检测模块和技术栈。

```bash
node scripts/scan.js [path]
```

### generate.js

生成 CLAUDE.md 层次结构。

```bash
# 生成指定层
node scripts/generate.js --layer 1|2|3 [--module path]

# 自动生成所有层
node scripts/generate.js --auto [--dry-run]

# 批量任务发现
node scripts/generate.js --batch --scan <path> [--json]

# 生成提示词上下文
node scripts/generate.js --prompt-context --module <path>
```

### update.js

基于 git diff 增量更新。

```bash
node scripts/update.js [--diff HEAD~1]
```

### hook.js

Hook 管理器。

```bash
# 项目初始化
node scripts/hook.js init [--global]

# 安装/卸载
node scripts/hook.js install <hook>
node scripts/hook.js uninstall <hook>

# 开关
node scripts/hook.js toggle <hook> on|off

# 状态
node scripts/hook.js status
node scripts/hook.js list
```

可用 Hooks: `post-commit`, `stale-notify`

## 状态检查

### check-stale.js

检测过期的 CLAUDE.md。

```bash
node scripts/check-stale.js [--json] [--stale-only]
node scripts/check-stale.js --touch <path1> <path2>
node scripts/check-stale.js --touch-all
```

### audit-status.js

检查 AUDIT.md 覆盖和新鲜度。

```bash
node scripts/audit-status.js [path] [--json|--never|--stale|--summary]
```

状态: `never` | `stale` | `fresh` | `clean`

### test-status.js

基于 import 分析检查测试覆盖。

```bash
node scripts/test-status.js [path] [--json|--untested|--stale|--imports|--summary]
```

状态: `untested` | `stale` | `covered`

### test-analyzer.js

检测测试质量问题。

```bash
node scripts/test-analyzer.js [path] [--json|--summary|--fix]
```

问题类型: `pseudo` | `weak` | `skipped` | `commented` | `empty` | `flaky`

## 后台任务

### update-bg.js

后台更新 CLAUDE.md（LLM 判断是否需要）。

```bash
node scripts/update-bg.js [--concurrency=N] [--resume]
node scripts/update-bg.js --status|--log
```

### module-analyzer.js

统一的文档和审计批量处理工具。

**用法**:
```bash
node scripts/module-analyzer.js [options] [path]
```

**模式选择（互斥）**:

| 参数 | 说明 |
|------|------|
| `--stale` | 只处理过期模块（默认） |
| `--missing` | 只处理缺失文档/审计的目录 |
| `--all` | 过期 + 缺失 |
| `--force` | 强制刷新所有大目录 |
| `--reindex` | `--force` 别名 |

**功能开关**:

| 参数 | 说明 |
|------|------|
| `--no-doc` | 跳过 CLAUDE.md 更新 |
| `--no-audit` | 跳过 AUDIT.md 更新 |
| `--no-kanban` | 跳过 Kanban 任务创建 |

**执行控制**:

| 参数 | 说明 |
|------|------|
| `--dry-run` | 预览模式（不调用 LLM） |
| `--concurrency=N` | 并发数（默认 6） |
| `--resume` | 从中断处继续 |
| `--retry-failed` | 只重试失败任务（不清空状态） |
| `--daemon` | 后台运行 |
| `--status` | 查看上次结果 |
| `--help` | 显示帮助 |

**路径参数**:
- `[path]` - 可选子目录（如 `js/agents`）

**常用组合**:

```bash
# 日常维护（更新过期模块）
node scripts/module-analyzer.js

# 补全缺失的 CLAUDE.md
node scripts/module-analyzer.js --missing --no-audit

# 补全缺失的 AUDIT.md
node scripts/module-analyzer.js --missing --no-doc

# 全量处理（过期 + 缺失）
node scripts/module-analyzer.js --all

# 预览将处理的目录
node scripts/module-analyzer.js --all --dry-run

# 强制刷新所有模块
node scripts/module-analyzer.js --force

# 指定目录 + 高并发
node scripts/module-analyzer.js --all --concurrency=12 js/agents/core
```

### code-audit.js

批量执行代码审计，生成 AUDIT.md。

```bash
node scripts/code-audit.js [--all | path1 path2 ...]
node scripts/code-audit.js --status
node scripts/code-audit.js --resume
```

- 只扫描大目录
- 自动注入小子目录上下文
- `LARGE_THRESHOLD = { files: 5, lines: 200 }`

### test-generator.js

批量生成测试文件。

**用法**:
```bash
node scripts/test-generator.js [options] [path]
```

**模式选择**:

| 参数 | 说明 |
|------|------|
| `--untested` | 为未测试文件生成测试（默认） |
| `--stale` | 重新生成过期测试 |
| `--all` | 未测试 + 过期 |

**执行控制**:

| 参数 | 说明 |
|------|------|
| `--dry-run` | 预览模式 |
| `--concurrency=N` | 并发数（默认 3） |
| `--resume` | 从中断处继续 |
| `--retry-failed` | 只重试失败任务 |
| `--daemon` | 后台运行 |
| `--status` | 查看上次结果 |

**常用组合**:

```bash
# 为所有未测试文件生成测试
node scripts/test-generator.js

# 预览将处理的文件
node scripts/test-generator.js --dry-run

# 指定目录
node scripts/test-generator.js js/agents/core

# 后台运行高并发
node scripts/test-generator.js --daemon --concurrency=5

# 重试失败的任务
node scripts/test-generator.js --retry-failed
```

### stale-notify.js

SessionStart Hook，通知过期模块。

```bash
node scripts/stale-notify.js
node scripts/stale-notify.js --enable|--disable|--status|--reset
```

## 工具脚本

### audit-archive.js

归档已修复的问题。

```bash
node scripts/audit-archive.js <path> --show
node scripts/audit-archive.js <path> 1 3 5
node scripts/audit-archive.js <path> --all|--history
```

### dashboard.js

启动 Web UI 仪表盘。

```bash
node scripts/dashboard.js [--port N] [--open]
```

### batch-llm-runner.js

通用批量 LLM 任务框架（库）。

```javascript
import { BatchRunner, runCodeagent } from './batch-llm-runner.js';

const runner = new BatchRunner({
  name: 'my-task',
  concurrency: 8,
  timeout: 120000
});

await runner.run({
  scan: async (cwd) => [...items],
  buildPrompt: (item) => '...',
  handleResult: async (item, result) => ({ status: '...' })
});
```
