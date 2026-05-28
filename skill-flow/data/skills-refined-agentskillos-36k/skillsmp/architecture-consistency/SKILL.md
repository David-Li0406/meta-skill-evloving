---
name: architecture-consistency
version: 1.0.0
description: 架构一致性审查（分层约束、模块边界、依赖倒置）
language: common
tags: [architecture, common]
---

# architecture-consistency

## 重点检查项（Checklist）

- 分层约束：是否破坏层次（如 handler 直接访问 DB、跨层调用）
- 模块边界：是否引入不必要的耦合；是否应该抽取接口或公共模块
- 依赖倒置：是否从高层依赖低层实现细节；是否需要抽象/注入
- 一致性：是否符合已有的目录结构、DDD/分层约定、命名空间规则
