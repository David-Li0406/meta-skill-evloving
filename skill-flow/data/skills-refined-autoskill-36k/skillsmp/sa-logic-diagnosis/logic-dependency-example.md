# 逻辑依赖管理示例 (Logic Dependency Management Example)

在学术写作中，各个章节之间存在严格的逻辑依赖关系。忽视这些依赖会导致返工和逻辑混乱。

## 示例：基于条件的写作 (Condition-Based Writing)

类似于编程中的 `await`，你不应该在前提条件满足之前开始后续章节的写作。

### 场景：等待数据分析结果

**错误做法 (非阻塞式)**：
- 在数据分析完成前，先写“结果”部分的草稿，留出空白填数字。
- **风险**：如果分析结果与预期相反，整个章节的叙事逻辑需要重写。

**正确做法 (阻塞式)**：

```typescript
// 伪代码示例：学术写作流程
async function writeResultsSection() {
  // 1. 等待核心数据分析完成
  const data = await analyzeData();
  
  // 2. 检查数据是否支持主要假设
  if (!data.supportsHypothesis) {
    // 路径分支：如果不支持，重构引言或修改假设
    await pivotResearchQuestion();
  }
  
  // 3. 只有在逻辑基础稳固后，才开始撰写结果文本
  await draftText(data);
}
```

### 依赖检查清单

在开始写新章节前，检查以下依赖：

1.  **写 Discussion 之前**：
    - [ ] Results 部分的所有图表是否已定稿？
    - [ ] 核心发现是否已经用一句话总结出来？

2.  **写 Introduction 之前**：
    - [ ] 核心 Research Question 是否已明确定义？
    - [ ] 目标投稿期刊的 Scope 是否已确认？

3.  **写 Abstract 之前**：
    - [ ] 全文结论是否已确定？(Abstract 应最后写)

## 优势

- **减少浪费**：避免为最终会被删除的论点投入写作时间。
- **逻辑一致**：确保每一句话都建立在已验证的事实之上。
- **心理清晰**：明确知道当前处于“等待数据”还是“可以写作”的状态。
