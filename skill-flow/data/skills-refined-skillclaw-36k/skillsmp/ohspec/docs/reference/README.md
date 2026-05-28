# 参考文档目录

本目录存放参考和设计文档，**SKILL 运行时不会加载这些文档**。

## 文档说明

### 设计文档

**context-transfer.md**
- 上下文传递机制设计
- 定义了如何在不同阶段之间传递上下文信息

**observability.md**
- 可观测性设计
- 定义了性能监控和指标收集机制

**token-budget.md**
- Token 预算管理设计
- 定义了 Token 使用监控和预警机制
- 相关实现：config.yaml 中的 token_budget 配置

**tool-fallback.md**
- 工具回退策略设计
- 定义了搜索工具的优先级和回退机制
- 包含 ripgrep 性能优化方案

### 参考文档

**quick-reference.md**
- 快速参考指南
- 提供常用命令和操作的快速查询

---

## 与运行时文档的区别

| 类型 | 位置 | 用途 | 是否加载 |
|------|------|------|---------|
| **运行时文档** | docs/*.md | SKILL 执行时引用 | ✅ 是 |
| **参考文档** | docs/reference/ | 设计参考和说明 | ❌ 否 |
| **未实施功能** | docs/unimplemented/ | 未来扩展参考 | ❌ 否 |

---

## 运行时文档列表

以下文档被 SKILL.md 或 workflows 引用，参与运行时执行：

- best-practices.md
- error-handling.md
- implementation-guide.md
- phases.md
- quality-gates.md
- resume-mode.md
- rfc-format.md
- routing-signals.md
- subagent-contract.md

---

**归档时间**：2026-01-19
**归档原因**：区分运行时文档和参考文档，简化 SKILL 加载
