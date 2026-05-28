---
name: code-review
description: Reviews code changes for bugs, style issues, performance problems, and best practices. Use when reviewing PRs, checking code quality, or auditing existing code.
---

# Code Review Skill

帮助审查代码质量、发现潜在问题并提供改进建议。

## When to use this skill

- 审查拉取请求 (PR) 或代码变更
- 检查代码质量和最佳实践
- 发现潜在的 bug 和安全问题
- 优化代码性能

## Review Checklist

### 1. 正确性 (Correctness)
- 代码是否实现了预期功能？
- 边界条件是否正确处理？
- 错误处理是否完善？

### 2. 代码风格 (Style)
- 是否遵循项目的编码规范？
- 命名是否清晰有意义？
- 代码是否有适当的注释？

### 3. 性能 (Performance)
- 是否存在明显的性能问题？
- 算法复杂度是否合理？
- 是否有不必要的重复计算？

### 4. 安全性 (Security)
- 是否存在安全漏洞？
- 输入是否经过验证？
- 敏感数据是否正确处理？

### 5. 可维护性 (Maintainability)
- 代码是否易于理解和修改？
- 是否遵循 DRY 原则？
- 模块化程度是否合适？

## How to provide feedback

1. **具体明确** - 指出问题的具体位置和原因
2. **解释原因** - 说明为什么这是个问题
3. **提供建议** - 给出改进方案或替代实现
4. **区分优先级** - 标注哪些是必须修改的，哪些是建议优化的

## Output Format

```markdown
## 代码审查报告

### 🔴 严重问题 (必须修改)
- [文件:行号] 问题描述及修复建议

### 🟡 建议改进 (推荐修改)
- [文件:行号] 优化建议

### 🟢 良好实践 (值得肯定)
- 代码中做得好的地方

### 📊 总体评估
- 代码质量评分: X/10
- 主要改进方向
```
