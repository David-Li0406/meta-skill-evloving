# 未实施功能归档

本目录存放已设计但未实施的功能文档，供未来参考。

## 目录说明

**SKILL 运行时不会加载此目录中的文档。**

## 归档的功能

### 1. RFC Registry（RFC 注册表）

**文件**：
- rfc-registry-guide.md
- rfc-registry-integration.md
- rfc-registry.json

**设计目的**：
- 中央 RFC 管理系统
- 生命周期管理、多维分类、依赖关系管理
- 统计分析和报告生成

**为什么未实施**：
- workflows/list.md 已提供动态扫描功能
- 对于小型项目，动态扫描更简洁
- 如需依赖管理，可增强 workflows/list.md

**未来考虑**：
- 如果需要管理多个并行 RFC
- 如果需要复杂的依赖关系管理
- 如果需要统计分析和报告

---

### 2. Cleanup Strategy（清理策略）

**文件**：
- cleanup-strategy.md
- cleanup-README.md
- cleanup-quick-ref.md
- cleanup-operations.md
- cleanup-integration.md

**设计目的**：
- Token 预算管理（黄/橙/红预警）
- 知识库提炼（模式识别）
- 定期维护（每周清理）
- 里程碑清理（检查点）

**为什么未实施**：
- workflows/list.md 已实现基本清理功能
- 复杂的 Token 管理策略暂无需求
- 知识库提炼功能暂无需求

**未来考虑**：
- 如果 Token 使用频繁超限
- 如果需要自动化的知识库管理
- 如果需要复杂的清理策略

---

### 3. Competitive Analysis（竞品分析）

**文件**：
- competitive-analysis.md
- knowledge-base/android/（4个文件）
- knowledge-base/ios-macos/（4个文件）
- knowledge-base/windows/（4个文件）

**设计目的**：
- 竞品平台分析（Android、iOS/macOS、Windows）
- 提供竞品设计参考和最佳实践
- 辅助需求分析阶段的决策

**为什么未实施**：
- workflows/dispatcher.md 中未集成加载逻辑
- 属于部分实施的功能
- 需要外部工具支持（context7、firecrawl）

**未来考虑**：
- 如果需要跨平台竞品分析
- 如果需要参考其他平台的设计模式
- 可以集成到 analyze 阶段作为可选功能

---

## 如何使用这些文档

1. **参考设计**：这些文档包含完整的设计思路，可作为未来实施的参考
2. **选择性实施**：可以选择部分功能实施，不必全部实现
3. **增强现有功能**：可以将这些设计融入现有的 workflows/list.md 等文件

---

**归档时间**：2026-01-19
**归档原因**：简化 SKILL 结构，保留未来扩展可能性
