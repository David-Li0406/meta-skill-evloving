---
name: unreal-gameplayframework
description: 用于 Unreal Engine Gameplay Framework 的框架设计、代码撰写与 code review。适用于规划模块边界、生命周期、接口约定、性能与可测试性建议时调用。
---

# Unreal Gameplay Framework Skill

## Skill 定位
提供 Gameplay Framework 的架构设计指导、实现建议与评审清单，帮助统一模块拆分、职责边界与接口风格。

## 适用场景
- 架构设计：系统分层、模块依赖与生命周期规划
- 代码撰写：基于 UE 玩法框架的实现建议与最佳实践
- Code Review：检查职责边界、性能、可维护性与一致性

## 输出预期
- 结构化设计建议（责任边界、依赖方向、生命周期）
- 实现要点与示例约束（命名、接口组织、线程/性能注意）
- Code Review 检查项（可维护性、扩展性、错误处理）

## References
- FName GetOptions filter: [references/FName.md](references/FName.md)
- Gameplay Tag category filter: [references/GameplayTags.md](references/GameplayTags.md)
- Inline allocators: [references/InlineAllocators.md](references/InlineAllocators.md)
- ParallelFor optimization: [references/ParallelFor.md](references/ParallelFor.md)
- Deferred execution (ON_SCOPE_EXIT): [references/DeferredExecution.md](references/DeferredExecution.md)
- Algo namespace: [references/Algo.md](references/Algo.md)
