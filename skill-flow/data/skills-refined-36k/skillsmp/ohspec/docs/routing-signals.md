# 路由信号机制

## 目录
- [概述](#概述)
- [信号定义](#信号定义)
- [信号检测规则](#信号检测规则)
- [信号组合](#信号组合)
- [与复杂度路由的关系](#与复杂度路由的关系)
- [Dispatcher 输出扩展](#dispatcher-输出扩展)
- [编排器处理逻辑](#编排器处理逻辑)

---

## 概述

路由信号机制将固定流水线改为信号驱动，根据需求特征动态调整执行路径。

## 信号定义

| 信号 | 检测条件 | 动作 |
|------|----------|------|
| `SKIP_ANALYZE` | 需求明确、单文件影响 | 跳过 analyze 阶段，直接进入 design |
| `LOAD_DIPLOMAT` | 跨子系统依赖 | 加载 Diplomat 扩展专家 |
| `TRIGGER_SPIKE` | 技术不确定性高 | 触发 Spike 验证流程 |
| `SIMPLIFY_CLARIFY` | 用户已提供详细需求 | 简化澄清阶段，减少问题数量 |

## 信号检测规则

### SKIP_ANALYZE

**触发条件**（全部满足）：
- 用户需求描述 ≥100 字且包含具体实现细节
- 影响范围 ≤1 个文件
- 无歧义词（"可能"、"或者"、"大概"）
- 无跨模块依赖

**效果**：合并 analyze + design 为单阶段执行

### LOAD_DIPLOMAT

**触发条件**（任一满足）：
- `scope.modules` 包含 ≥2 个不同子系统
- `scope.dependencies` 包含外部团队维护的模块
- 需要修改公共接口或协议

**效果**：在 design 阶段前加载 Diplomat 专家协调依赖方

### TRIGGER_SPIKE

**触发条件**（任一满足）：
- 使用未验证的技术方案
- 性能要求无历史基准
- 涉及第三方库的未知行为
- Dispatcher 标记 `complexity: COMPLEX` 且 `reasoning` 包含"不确定"

**效果**：在 design 阶段前执行 Spike 验证，输出可行性报告

### SIMPLIFY_CLARIFY

**触发条件**（全部满足）：
- 用户需求包含验收标准
- 用户需求包含技术约束
- 用户需求包含边界条件说明

**效果**：analyze 阶段最多提 2 个澄清问题（默认上限 5 个）

## 信号组合

信号可组合触发，执行顺序：

```
TRIGGER_SPIKE → LOAD_DIPLOMAT → SKIP_ANALYZE/SIMPLIFY_CLARIFY
```

**示例**：跨子系统 + 技术不确定
- 信号：`LOAD_DIPLOMAT` + `TRIGGER_SPIKE`
- 执行：Spike验证 → Diplomat协调 → 标准流程

## 与复杂度路由的关系

| 复杂度 | 可触发信号 | 不可触发信号 |
|--------|-----------|-------------|
| SIMPLE | `SKIP_ANALYZE`, `SIMPLIFY_CLARIFY` | `LOAD_DIPLOMAT`, `TRIGGER_SPIKE` |
| MEDIUM | `SIMPLIFY_CLARIFY`, `LOAD_DIPLOMAT` | `SKIP_ANALYZE` |
| COMPLEX | `LOAD_DIPLOMAT`, `TRIGGER_SPIKE` | `SKIP_ANALYZE`, `SIMPLIFY_CLARIFY` |

## Dispatcher 输出扩展

Dispatcher 返回的 JSON 需包含 `signals` 字段：

```json
{
  "intent": "...",
  "complexity": "MEDIUM",
  "signals": ["LOAD_DIPLOMAT"],
  "scope": { ... },
  "experts": { ... }
}
```

## 编排器处理逻辑

```
1. 接收 Dispatcher 返回的 signals 数组
2. 按优先级排序：TRIGGER_SPIKE > LOAD_DIPLOMAT > SKIP_ANALYZE > SIMPLIFY_CLARIFY
3. 依次执行信号对应的动作
4. 进入调整后的阶段流程
```
