# Token 预算管理

## 概述

Token 预算管理机制用于监控和控制 OHSpec 执行过程中的上下文消耗，防止因 Token 超限导致的会话中断或信息丢失。

## 三级预警机制

| 级别 | 阈值 | 状态 | 触发动作 |
|------|------|------|----------|
| 🟡 黄色 | 50% | 预警 | 归档旧 RFC，压缩 findings |
| 🟠 橙色 | 70% | 警告 | 只保留当前 RFC，创建检查点 |
| 🔴 红色 | 85% | 危险 | 最小上下文，建议新会话 |

## 各级别处理策略

### 🟡 黄色预警（50%）

触发条件：`token_usage.usage_ratio >= 0.50`

处理动作：
1. 归档旧 RFC 到 findings.json 的 `archived_rfcs` 字段
2. 压缩 findings 中的详细扫描结果（保留摘要，移除原始代码片段）
3. 移除冗余的代码片段引用

```yaml
# progress.json 更新
token_usage:
  alert_level: "yellow"
  alert_triggered_at: "2024-01-16T10:30:00Z"
  compression_actions:
    - action: "archive_old_rfcs"
      timestamp: "2024-01-16T10:30:01Z"
    - action: "compress_findings"
      timestamp: "2024-01-16T10:30:02Z"
```

### 🟠 橙色预警（70%）

触发条件：`token_usage.usage_ratio >= 0.70`

处理动作：
1. 只保留当前 RFC 相关上下文
2. 创建检查点（保存当前阶段和已完成的 RFC 章节）
3. 清理历史交互记录

```yaml
# progress.json 更新
token_usage:
  alert_level: "orange"
  checkpoint:
    created_at: "2024-01-16T10:30:00Z"
    phase: "design"
    rfc_sections_completed: ["§1", "§2", "§3"]
```

### 🔴 红色预警（85%）

触发条件：`token_usage.usage_ratio >= 0.85`

处理动作：
1. 切换到最小上下文模式（仅保留必要的执行状态）
2. 向用户发出警告，建议开启新会话
3. 保存完整状态到 progress.json，确保可恢复

```
⚠️ Token 使用率已达 85%，建议：
1. 使用 /ohspec resume RFC-xxx 在新会话中继续
2. 当前进度已保存，可安全切换会话
```

## 上下文压缩策略

### 优先保留内容

按优先级排序：
1. 当前阶段的 RFC 内容
2. 关键决策记录（decisions）
3. 未解决的约束和风险（constraints, risks）
4. 当前阶段的 findings

### 可压缩内容

按压缩优先级排序：
1. 历史代码扫描结果（保留文件路径，移除代码片段）
2. 已完成阶段的详细日志
3. 冗余的文件内容引用
4. 历史交互记录

## 调度员职责

调度员在每次阶段切换时必须：

1. 更新 `progress.json` 中的 `token_usage.current`
2. 计算 `usage_ratio = current / max`
3. 检查是否触发预警阈值
4. 执行对应级别的处理动作
5. 记录压缩操作到 `compression_actions`

## 与 Resume 模式集成

当触发红色预警后用户开启新会话：

1. 新会话调度员读取 `progress.json`
2. 从 `checkpoint` 恢复执行状态
3. 从 `token_usage.checkpoint.phase` 继续执行
4. 重置 `token_usage.current` 为 0

## 配置参考

```yaml
# config.yaml
token_budget:
  max_tokens: 200000
  thresholds:
    yellow: 0.50
    orange: 0.70
    red: 0.85
```
