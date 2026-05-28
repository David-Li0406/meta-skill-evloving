# dispatcher 阶段 - 需求调度和成本估算

## 概述

**目标**：分析用户需求，评估复杂度，估算成本，决策执行路径

**执行者**：Dispatcher 子代理

**输入**：用户需求原文

**输出**：复杂度评估、专家组合、执行模式、成本估算、**基线扫描结果（scan-of-record）**

---

## 执行流程

### 基线扫描（scan-of-record）

Dispatcher 必须完成一次“可审计的基线扫描”，作为后续阶段的唯一事实来源：
- 写入 `findings.confirmed.key_files`（≥3 且覆盖入口/配置/依赖或测试/可观测）
- 写入 `findings.confirmed.facts`（≥3，项目事实提炼：配置/存储/权限/错误码/线程模型/可观测等，每条附证据锚点）
- 写入相似实现/关键证据锚点（repo@rev:path#Lline）
- 明确扫描范围与工具（来自 ASSESS：tooling + strategy）
- **仅一次 repo-wide 搜索**：基线阶段最多一次全仓搜索（文件列表 + 关键词统计）；后续 analyze/design 仅在“证据缺口”时定向补扫

> 后续 analyze/design 默认不再做全量扫描，仅在发现“证据缺口”时触发补扫。

### 性能与可观测（强制，避免“搜索 10 分钟黑盒”）

在 Codex 兼容回退或任何“全仓搜索”时，必须记录每一次搜索的：
- pattern/命令
- 扫描 ROOT（显式路径）
- 耗时（秒）
- 命中文件数（或 0）

推荐用 `time` 或 `date` 计时，并把记录追加到：
- `progress.json.observability.tool_calls[]`
- 同步更新 `progress.json.tooling.metrics.total_searches/total_time_sec/avg_time_sec`

硬规则（避免跑飞）：
- 单次 repo-wide 搜索若 > 5s：立刻停止扩大搜索，改为缩小范围（限定目录/文件类型/更精确关键词）
- key_files/facts 达标后必须早停（禁止“顺便多读几个文件”）
- **全仓扫描是搜索级别**：禁止全量 Read；只读关键文件与少量候选文件

### 兼容模式（Task 不可用）

当 Task 子代理不可用（如 Codex 环境）时，允许编排器执行最小化扫描回退：
- 使用已选搜索工具（rg/ag/grep）进行关键词预过滤
- 收集**候选**关键文件锚点并标注角色（入口/配置/依赖/测试/可观测等）
- 提炼 ≥3 条项目事实（配置/存储/权限/错误码/线程模型/可观测等），每条附证据锚点并写入 `findings.confirmed.facts`
- 先展示候选锚点与覆盖面给用户确认（必要时仅需选择保留/剔除）
- 不得基于假设填充接口/设置键名
- 记录到 progress.json 的 `audit_log` 与 `tooling`
- **第一分钟必须产出基线**：在开始深度 Read/设计推演前，必须先把 `findings.confirmed.key_files`（≥3，覆盖面达标）与 `findings.confirmed.facts`（≥3，每条有证据锚点）落盘；否则就算后续中断也会留下“可恢复状态”
- **早停**：一旦 key_files/facts 达标，立即停止 repo-wide 搜索，进入澄清/设计；后续只允许“缺口触发”的定向补扫

> 若覆盖面仍不足，优先让用户选择“补扫模块/扩展范围”，仅在最后才请求人工锚点；否则停在 DRAFT。

### 步骤 1：初步代码扫描

使用 Grep/Glob 快速扫描代码库，理解项目结构。

### 步骤 2：需求分析

分析用户需求，提取：
- 意图（intent）
- 范围（scope）
- 复杂度（complexity）
- 路由信号（signals）

### 步骤 2.5：竞品分析判断

识别是否需要竞品分析（适用于操作系统类项目）：

```python
needs_competitive = (
    "API" in requirement or "api" in requirement or
    "接口" in requirement or "interface" in requirement or
    "性能" in requirement or "performance" in requirement or
    "架构" in requirement or "architecture" in requirement or
    "安全" in requirement or "security" in requirement or
    "设计模式" in requirement or "design pattern" in requirement
)

if needs_competitive:
    metadata["needs_competitive_analysis"] = True
    # 默认分析 Android 和 iOS/macOS 平台
    metadata["competitive_platforms"] = ["android", "ios-macos"]
```

写入 progress.json：
```json
{
  "needs_competitive_analysis": true,
  "competitive_platforms": ["android", "ios-macos"]
}
```

### 步骤 3：成本估算（新增）

基于 ASSESS 阶段的规模评估，计算预期成本。

#### 成本估算公式

```
总成本 = 代码扫描成本 + Persona 加载成本 + RFC 生成成本 + 用户交互成本

其中：
- 代码扫描成本 = 文件数 × 平均行数 × 4 (tokens)
- Persona 加载成本 = 专家数 × 平均 Persona 大小 (700 tokens/专家)
- RFC 生成成本 = 阶段数 × 平均输出 (5000 tokens/阶段)
- 用户交互成本 = 门禁数 × 平均交互 (1000 tokens/门禁)
```

#### 估算示例

**SIMPLE 任务**：
```
代码扫描：5 文件 × 200 行 × 4 = 4,000 tokens
Persona：2 专家 × 700 = 1,400 tokens
RFC 生成：2 阶段 × 5,000 = 10,000 tokens
用户交互：1 门禁 × 1,000 = 1,000 tokens
总计：16,400 tokens (8.2%)
```

**MEDIUM 任务**：
```
代码扫描：30 文件 × 200 行 × 4 = 24,000 tokens
Persona：3 专家 × 700 = 2,100 tokens
RFC 生成：3 阶段 × 5,000 = 15,000 tokens
用户交互：2 门禁 × 1,000 = 2,000 tokens
总计：43,100 tokens (21.6%)
```

**COMPLEX 任务**：
```
代码扫描：80 文件 × 200 行 × 4 = 64,000 tokens
Persona：4 专家 × 700 = 2,800 tokens
RFC 生成：4 阶段 × 5,000 = 20,000 tokens
用户交互：4 门禁 × 1,000 = 4,000 tokens
总计：90,800 tokens (45.4%)
```

### 步骤 4：预算预警

根据估算成本，触发预警机制。

#### 预警阈值

| 级别 | 阈值 | 颜色 | 动作 |
|------|------|------|------|
| 正常 | < 50% | 绿色 | 无需干预 |
| 黄色预警 | 50-70% | 黄色 | 建议优化 |
| 橙色预警 | 70-85% | 橙色 | 强制优化 |
| 红色预警 | > 85% | 红色 | 建议新会话 |

#### 预警动作

**黄色预警（50-70%）**：
- 归档旧 RFC 到 findings.json
- 压缩 findings 中的详细扫描结果
- 移除冗余的代码片段引用

**橙色预警（70-85%）**：
- 只保留当前 RFC 相关上下文
- 创建检查点（checkpoint）
- 清理历史交互记录

**红色预警（> 85%）**：
- 切换到最小上下文模式
- 建议用户开启新会话
- 保存完整状态到 progress.json

### 步骤 5：输出结果

将分析结果写入 `findings.json` 和 `progress.json`。

#### findings.json 输出

```json
{
  "dispatcher": {
    "intent": "为音频服务增加 3D 音效开关",
    "complexity": "MEDIUM",
    "scope": {
      "files": ["src/audio/service.ts", "src/audio/effects.ts"],
      "modules": ["audio"],
      "dependencies": ["audio-engine"]
    },
    "experts": ["需求分析师", "架构设计师", "质量审查员"],
    "signals": ["SIMPLIFY_CLARIFY"],
    "cost_estimate": {
      "total_tokens": 43100,
      "usage_ratio": 0.216,
      "alert_level": "none",
      "breakdown": {
        "code_scan": 24000,
        "persona": 2100,
        "rfc_generation": 15000,
        "user_interaction": 2000
      }
    }
  }
}
```

#### progress.json 输出

```json
{
  "token_usage": {
    "current": 0,
    "max": 200000,
    "estimated_total": 43100,
    "usage_ratio": 0.216,
    "alert_level": "none",
    "alert_triggered_at": null
  },
  "phases": {
    "dispatcher": {
      "status": "complete",
      "completed_at": "2026-01-19T10:30:00Z",
      "cost_estimate": {
        "total": 43100,
        "breakdown": {
          "code_scan": 24000,
          "persona": 2100,
          "rfc_generation": 15000,
          "user_interaction": 2000
        }
      }
    }
  }
}
```

---

## 成本优化策略

### 自动触发条件

当预警级别达到黄色或以上时，自动触发优化策略。

### 优化策略清单

#### 策略 1：归档历史 RFC（黄色预警）

```
动作：将已完成的 RFC 内容压缩为摘要
节省：~10,000 tokens
触发：usage_ratio >= 0.50
```

#### 策略 2：压缩扫描结果（黄色预警）

```
动作：只保留关键代码片段，移除完整文件内容
节省：~15,000 tokens
触发：usage_ratio >= 0.50
```

#### 策略 3：创建检查点（橙色预警）

```
动作：保存当前状态到 checkpoint.json，清理主上下文
节省：~30,000 tokens
触发：usage_ratio >= 0.70
```

#### 策略 4：建议新会话（红色预警）

```
动作：提示用户开启新会话，保存完整状态
节省：重置上下文
触发：usage_ratio >= 0.85
```

---

## 成本监控

在整个执行过程中持续监控成本：

1. **每个阶段开始前**：检查当前 token 使用量
2. **每个阶段结束后**：更新实际消耗，对比估算
3. **触发预警时**：立即执行优化策略
4. **接近预算上限时**：暂停执行，等待用户决策

---

## 示例：成本估算和预警

### 场景 1：SIMPLE 任务（正常）

```json
{
  "cost_estimate": {
    "total_tokens": 16400,
    "usage_ratio": 0.082,
    "alert_level": "none"
  }
}
```

**结果**：绿色，无需干预

### 场景 2：MEDIUM 任务（正常）

```json
{
  "cost_estimate": {
    "total_tokens": 43100,
    "usage_ratio": 0.216,
    "alert_level": "none"
  }
}
```

**结果**：绿色，无需干预

### 场景 3：COMPLEX 任务（黄色预警）

```json
{
  "cost_estimate": {
    "total_tokens": 110000,
    "usage_ratio": 0.55,
    "alert_level": "yellow",
    "recommended_actions": [
      "归档旧 RFC",
      "压缩扫描结果"
    ]
  }
}
```

**结果**：黄色预警，建议优化

### 场景 4：超大型任务（橙色预警）

```json
{
  "cost_estimate": {
    "total_tokens": 150000,
    "usage_ratio": 0.75,
    "alert_level": "orange",
    "recommended_actions": [
      "创建检查点",
      "清理历史记录",
      "只保留当前 RFC 上下文"
    ]
  }
}
```

**结果**：橙色预警，强制优化

### 场景 5：极限任务（红色预警）

```json
{
  "cost_estimate": {
    "total_tokens": 180000,
    "usage_ratio": 0.90,
    "alert_level": "red",
    "recommended_actions": [
      "建议用户开启新会话",
      "保存完整状态到 progress.json"
    ]
  }
}
```

**结果**：红色预警，建议新会话

---

## 注意事项

1. **保守估算**：使用保守值，避免低估成本
2. **动态调整**：根据实际消耗调整后续阶段的估算
3. **用户透明**：向用户展示成本估算和预警信息
4. **自动优化**：预警触发时自动执行优化策略
5. **误差容忍**：估算误差 < 20% 为可接受范围
