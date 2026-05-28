# 测试工具链详解

## 工具链架构

```
test-mapper.js     → 生成 .test-map.json (源码↔测试映射)
       ↓
test-status.js     → 分析覆盖状态 (untested/stale/covered)
       ↓
test-generator.js  → 批量生成缺失测试
       ↓
test-result.js     → 运行测试，缓存结果到 .test-result.json
       ↓
test-fix.js        → 并发修复测试错误 (读缓存，不跑测试)
```

## 脚本详解

| 脚本 | 职责 | 关键特性 |
|------|------|----------|
| **test-mapper.js** | 符号级 import 分析，生成源码→测试映射 | 追踪 index.js re-exports |
| **test-status.js** | 检查测试覆盖状态 | 支持 --json/--untested/--stale |
| **test-analyzer.js** | 检测测试质量问题 | 伪测试/弱断言/跳过的测试 |
| **test-generator.js** | LLM 批量生成测试 | 支持 --daemon 后台运行 |
| **test-result.js** | 运行 vitest 并缓存结果 | 支持按文件/ID 查询 |
| **test-fix.js** | LLM 并发修复测试错误 | 只读缓存，不跑测试 |
| **test-scaffold.js** | 生成测试骨架模板 | 输出 AI 友好的提示词 |
| **test-view.js** | 查看模块测试详情 | 读取 .test-map.json |
| **test-organizer.js** | 测试文件组织/迁移 | 检测放错位置的测试 |

## 测试修复工作流

**关键设计**: test-fix.js 使用 sandbox=read-only，禁止 codex 运行命令，只做代码分析。

```bash
# 1. 运行测试，缓存结果 (只跑一次)
node scripts/test-result.js --save

# 2. 查看错误摘要
node scripts/test-result.js --cached --summary

# 3. 按文件查询特定错误 (<100ms，不跑测试)
node scripts/test-result.js --cached --file=kernel
node scripts/test-result.js --cached --id=5

# 4. 并发修复 (默认跳过已完成的任务)
node scripts/test-fix.js --concurrency=25

# 5. 再次运行测试验证
node scripts/test-result.js --save
```

## test-result.js 查询接口

```bash
# 按文件名模糊查询
node scripts/test-result.js --cached --file=<关键词>

# 按错误 ID 查询
node scripts/test-result.js --cached --id=<ID>

# 分页获取错误列表
node scripts/test-result.js --cached --errors --offset=0 --limit=40
```

输出格式：
```json
{
  "query": "kernel",
  "found": 3,
  "errors": [
    {
      "id": 5,
      "testFile": "tests/unit/agents/core/kernel.test.js",
      "sourceFile": "js/agents/core/kernel.js",
      "test": "should emit events",
      "message": "Expected: 'agent:start' Received: 'agent.start'",
      "line": 42
    }
  ]
}
```

## test-fix.js 特性

- **自动跳过已完成**: 读取 `.test-fix-tasks.json` 过滤 completed 状态
- **sandbox 限制**: prompt 禁止运行 npm test/vitest
- **查询工具**: AI 可用 test-result.js --cached --file 获取更多上下文
- **断点续传**: 支持 --resume 从中断处继续
- **30 分钟超时**: 默认 1800000ms，适应 codex 后端响应时间

```bash
# 首次运行
node scripts/test-fix.js --concurrency=25

# 重试失败任务
node scripts/test-fix.js --retry-failed

# 强制全部重新处理
rm .project-index/.test-fix-tasks.json && node scripts/test-fix.js

# 限制处理数量
node scripts/test-fix.js --limit=20 --concurrency=10
```

## 关键实现细节

### 防止 codex 运行测试

问题：高并发时 codex 可能自动分解任务并运行 vitest 验证，导致 N 个 vitest 并发把系统卡死。

解决方案：
1. **prompt 约束** - 明确禁止运行任何命令
2. **结果缓存** - 测试结果预先保存到 `.test-result.json`
3. **查询接口** - AI 通过 `--cached --file` 获取上下文，<100ms 响应

prompt 中的关键约束：
```
## 约束
- 只分析代码，禁止运行任何命令 (npm test, vitest, node 等)
- 测试结果已缓存，无需验证修复

## 查询工具 (如需更多上下文)
- 按文件查询: node test-result.js --cached --file=<关键词>
- 按ID查询: node test-result.js --cached --id=<错误ID>
- 这些查询只读缓存 (<100ms)，不会运行测试
```

### 任务状态管理

状态文件位于 `.project-index/`:
- `.test-fix-tasks.json` - 任务状态 (pending/running/completed/failed)
- `.test-fix-progress.json` - 进度检查点 (用于断点续传)
- `.test-fix-result.json` - 最终结果汇总
- `.test-fix.log` - 执行日志

scan() 函数自动过滤已完成任务：
```javascript
const completedIds = new Set(
  prev.tasks.filter(t => t.status === 'completed').map(t => t.id)
);
return items.filter(item => !completedIds.has(item.id));
```

### Dashboard 集成

启动 Dashboard 监控任务进度：
```bash
node scripts/dashboard.js --open
# 访问 http://localhost:3008
```

Dashboard 实时读取 `.test-fix-tasks.json` 显示：
- 任务状态分布 (pending/running/completed/failed)
- 错误原因统计
- 重试操作入口
