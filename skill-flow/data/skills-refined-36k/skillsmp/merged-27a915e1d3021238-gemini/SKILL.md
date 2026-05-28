---
name: gemini
description: Use this skill when you need to execute tasks with the Gemini AI engine, which is designed for long context processing and multimodal tasks.
---

# Gemini Skill

Gemini AI执行引擎，作为**可选引擎之一**。

## 定位

Gemini是LD角色可调用的**引擎之一**，与Codex形成互补：
- 长上下文处理
- 多模态任务
- 特定场景优化

## 调用方式

### 通过指令指定
```bash
/vibe-code --engine=gemini "优化性能"
```

### 直接调用
```bash
gemini "任务描述"
```

## 能力范围

### 代码任务
- 代码优化
- 性能分析
- 长文件处理

### 多模态任务
- 图片理解
- 文档分析
- 视觉相关代码

## 使用建议

根据 orchestrator.yaml 配置或用户指定使用。如果没有配置或指定，默认使用主引擎。

## 与Codex对比

| 维度 | Codex | Gemini |
|:---|:---|:---|
| 状态 | 可用 | 规划中 |
| 特长 | 代码执行 | 长上下文 |
| 适用 | 通用任务 | 特定优化 |

## 集成计划

```markdown
Phase 1: 接口定义
Phase 2: 基础集成
Phase 3: 场景优化
Phase 4: 自动选择
```