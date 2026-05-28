---
name: requirements-and-assertions-merger
description: Use this skill to analyze function logic, generate assertions, and merge requirement clarifications into a comprehensive document.
---

# 需求与断言合并技能

此技能负责分析函数逻辑并生成合适的断言，同时将需求问题答案整合到需求文档中，生成完备需求。

## 技能能力

### 1. 逻辑分析与断言生成
- 分析函数的返回值类型和结构
- 识别可能的输出范围
- 检测副作用（如状态修改、事件触发）
- 生成精确的类型断言
- 创建边界值验证
- 生成深度对象比较
- 添加函数调用验证

### 2. 需求合并
- 将问题答案整合到需求文档中，生成完备需求
- 维持原需求文档的结构和格式，必要时可调整以提升清晰度
- 确保新增内容清晰可辨识

## 使用方式

### 断言生成示例

```typescript
// 为函数生成断言
await generateAssertions('<function_name>', {
  inputs: [{ <input_parameters> }],
  framework: '<testing_framework>'
});
```

### 需求合并示例

1. 复制 `cleaned-requirements/index.md` 到 `clarified-requirements/index.md`
2. 读取 `cleaned-requirements/issues.md` 中的所有问题和答案
3. 逐个问题处理，整合答案到文档

### 答案检查

- 确认所有 critical 优先级问题已回答
- 确认所有 warning 优先级问题已回答或标记为"待补充"

## 最佳实践

### 断言选择原则
- 使用最具体的断言
- 避免过度脆弱的断言
- 关注行为而非实现

### 需求合并原则
- 忠实整合：准确反映问题答案，不自行发挥
- 清晰标注：新增内容要清晰可辨识