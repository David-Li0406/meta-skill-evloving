# 子代理输入契约标准

本文档定义 OHSpec 子代理（Subagent）的标准化输入格式，确保所有子代理接收一致的上下文信息。

---

## 契约结构

每个子代理调用必须包含以下 4 个部分：

```markdown
## 原始需求
{user_requirement}

## 上下文包
- findings.json 摘要: {summary}
- progress.json 状态: {current_phase}
- 前序输出: {prior_outputs}

## 当前任务
{task_description}

## 验收标准
{acceptance_criteria}
```

---

## 字段说明

### 1. 原始需求（user_requirement）

用户的原始输入，保持原文不做修改。

**示例**：
```
为音频服务增加 3D 音效开关功能
```

### 2. 上下文包

| 字段 | 说明 | 来源 |
|------|------|------|
| findings.json 摘要 | 代码扫描结果的关键信息（key_files、facts、依赖、约束） | `{rfc_dir}/findings.json` |
| progress.json 状态 | 当前阶段和已完成阶段 | `{rfc_dir}/progress.json` |
| 前序输出 | 前一阶段子代理的关键输出 | 上一阶段返回的 JSON |

**示例**：
```yaml
findings.json 摘要:
  modules: [AudioService, AudioConfig]
  key_files:
    - {path: main@HEAD:src/audio/service.ts#L123, role: entry}
    - {path: main@HEAD:src/audio/config.ts#L45, role: config}
  facts:
    - {id: FACT-001, fact: "设置项通过 Settings DB 读取并监听变更", evidence: ["main@HEAD:src/audio/config.ts#L45"]}
  dependencies: [AudioManager, PermissionManager]

progress.json 状态:
  current_phase: design
  completed: [dispatcher, analyze]

前序输出:
  analyst_summary: "需求已澄清，用户选择方案 A"
  key_decisions: ["使用现有 AudioManager 接口", "不需要新增权限"]
```

### 3. 当前任务（task_description）

本阶段子代理需要完成的具体任务，简洁明确。

**示例**：
```
设计 3D 音效开关的接口契约，输出 RFC §3-§5
```

### 4. 验收标准（acceptance_criteria）

子代理输出必须满足的条件，用于自检和审查。

**示例**：
```
- [ ] 接口定义完整（参数、返回值、异常）
- [ ] 约束已量化（性能、资源）
- [ ] 依赖图已绘制
- [ ] 输出 JSON 格式正确
```

---

## 完整示例

```markdown
## 原始需求
为音频服务增加 3D 音效开关功能

## 上下文包
- findings.json 摘要:
  - modules: [AudioService, AudioConfig]
  - key_files:
    - {path: main@HEAD:src/audio/service.ts#L123, role: entry}
    - {path: main@HEAD:src/audio/config.ts#L45, role: config}
  - facts:
    - {id: FACT-001, fact: "设置项通过 Settings DB 读取并监听变更", evidence: ["main@HEAD:src/audio/config.ts#L45"]}
  - patterns: 现有开关使用 ConfigManager.setBoolean()
- progress.json 状态: analyze → design
- 前序输出: 用户确认使用方案 A（复用 AudioManager）

## 当前任务
设计 3D 音效开关的接口契约与落地计划（不写实现）

## 验收标准
- [ ] 定义 IEnable3DAudio 接口
- [ ] 约束：延迟 < 50ms，内存增量 < 1MB
- [ ] 绘制依赖图（AudioService → AudioManager → ConfigManager）
- [ ] 输出符合 architect JSON 格式
```

---

## 使用方式

Orchestrator 在调用 Task 工具时，按此契约格式构造 prompt：

```python
prompt = f"""
## 原始需求
{user_requirement}

## 上下文包
- findings.json 摘要: {extract_findings_summary(rfc_dir)}
- progress.json 状态: {get_current_phase(rfc_dir)}
- 前序输出: {prior_output_summary}

## 当前任务
{task_for_this_phase}

## 验收标准
{acceptance_criteria_for_this_phase}

---
## Persona
{persona_content}
"""
```

---

## 相关文档

- [实现指南](./implementation-guide.md) - Orchestrator 实现细节
- [核心专家](../personas/core/) - 各专家的输出格式定义
