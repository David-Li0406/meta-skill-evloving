# 可观测性规范

## 概述

OHSpec 可观测性机制用于追踪执行过程、收集性能指标和记录决策审计，支持问题诊断和流程优化。

## 追踪标识

### trace_id 规范

```
格式：ohspec-{rfc_id}-{timestamp}-{random}
示例：ohspec-RFC-001-20240116T103000-a1b2
```

- `rfc_id`：关联的 RFC 标识
- `timestamp`：ISO 8601 格式（精确到秒）
- `random`：4 位随机字符（防冲突）

### 生成时机

- 调度员启动新任务时生成
- Resume 模式继承原 trace_id，追加 `-r{n}` 后缀

## 阶段耗时追踪

### 指标定义

| 指标 | 说明 | 单位 |
|------|------|------|
| `phase_duration` | 阶段总耗时 | 秒 |
| `wait_time` | 等待用户输入时间 | 秒 |
| `active_time` | 实际执行时间 | 秒 |

### 记录格式

```json
{
  "phase": "analyze",
  "started_at": "2024-01-16T10:30:00Z",
  "completed_at": "2024-01-16T10:45:00Z",
  "duration_sec": 900,
  "wait_sec": 120,
  "active_sec": 780
}
```

## Token 消耗追踪

### 指标定义

| 指标 | 说明 |
|------|------|
| `input_tokens` | 输入 Token 数 |
| `output_tokens` | 输出 Token 数 |
| `total_tokens` | 总 Token 数 |
| `context_tokens` | 上下文占用 Token |

### 按阶段统计

```json
{
  "phase": "analyze",
  "tokens": {
    "input": 5000,
    "output": 2000,
    "total": 7000,
    "context": 15000
  }
}
```

## 工具调用统计

### 追踪内容

| 指标 | 说明 |
|------|------|
| `tool_name` | 工具名称 |
| `call_count` | 调用次数 |
| `success_count` | 成功次数 |
| `error_count` | 失败次数 |
| `total_duration_ms` | 总耗时（毫秒） |

### 记录格式

```json
{
  "tool_calls": [
    {
      "tool": "Read",
      "calls": 15,
      "success": 14,
      "errors": 1,
      "duration_ms": 450
    },
    {
      "tool": "Grep",
      "calls": 8,
      "success": 8,
      "errors": 0,
      "duration_ms": 320
    }
  ]
}
```

## 决策审计

### 审计事件类型

| 事件 | 说明 |
|------|------|
| `state_transition` | 状态转换 |
| `gate_check` | 质量门检查 |
| `user_decision` | 用户决策 |
| `auto_fix` | 自动修复 |
| `error_recovery` | 错误恢复 |

### 审计日志格式

```json
{
  "event": "state_transition",
  "timestamp": "2024-01-16T10:30:00Z",
  "trace_id": "ohspec-RFC-001-20240116T103000-a1b2",
  "from_state": "ANALYZING",
  "to_state": "DESIGNING",
  "trigger": "gate_passed",
  "actor": "dispatcher",
  "details": {
    "gate_score": 92,
    "auto_approved": true
  }
}
```

## 日志格式规范

### 结构化日志

```
[{timestamp}] [{level}] [{trace_id}] [{phase}] {message}
```

示例：
```
[2024-01-16T10:30:00Z] [INFO] [ohspec-RFC-001-...] [analyze] 开始需求分析
[2024-01-16T10:30:05Z] [DEBUG] [ohspec-RFC-001-...] [analyze] 扫描到 5 个相似实现
[2024-01-16T10:31:00Z] [WARN] [ohspec-RFC-001-...] [analyze] Token 使用率达 50%
```

### 日志级别

| 级别 | 用途 |
|------|------|
| `ERROR` | 执行失败、需要干预 |
| `WARN` | 预警、潜在问题 |
| `INFO` | 关键节点、状态变更 |
| `DEBUG` | 详细执行信息 |

## 指标收集规则

### 收集时机

1. **阶段开始**：记录 `started_at`，初始化阶段指标
2. **阶段结束**：记录 `completed_at`，计算耗时，汇总 Token
3. **状态转换**：记录审计事件
4. **错误发生**：记录错误详情和恢复动作

### 存储位置

- 实时指标：`progress.json` 的 `observability` 字段
- 历史审计：`progress.json` 的 `audit_log` 数组

## 性能基线

### 参考值

| 阶段 | 预期耗时 | Token 预算 |
|------|----------|------------|
| dispatcher | <30s | <2000 |
| analyze | 5-15min | <30000 |
| design | 5-15min | <30000 |
| precheck | <60s | <5000 |
| audit | 2-5min | <15000 |

### 异常检测

- 耗时超过预期 2 倍：记录 WARN
- Token 超过预算 1.5 倍：触发压缩策略
