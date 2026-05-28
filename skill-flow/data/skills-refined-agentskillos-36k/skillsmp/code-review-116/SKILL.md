---
name: code-review
description: Review frontend code for best practices, bugs, and improvements. Use when reviewing PRs, checking code quality, or before committing.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
argument-hint: <file_path>
user-invocable: true
---

# 前端代码审查

对前端代码进行审查，检查最佳实践、潜在错误和改进建议。

## Instructions

1. 读取指定的文件或目录
2. 检查以下方面：
   - 代码风格一致性（ESLint、Prettier 等）
   - 潜在的 bug 或错误
   - 性能问题
   - 安全漏洞
   - 可读性和可维护性
   - 前端特定问题（如 React hooks 规则、状态管理、组件设计等）
   - TypeScript 类型安全
   - CSS/样式最佳实践
3. 提供具体的改进建议

## 审查要点

### JavaScript/TypeScript
- 检查未使用的变量和导入
- 确保正确使用异步操作（async/await, Promise）
- 检查错误处理是否完善
- 验证 React hooks 使用是否符合规则
- 检查状态管理是否合理
- 确保组件设计遵循单一职责原则

### 性能
- 检查不必要的组件重渲染
- 验证是否使用了适当的 memoization
- 检查是否有内存泄漏风险
- 确保资源（如事件监听器）被正确清理

### 安全性
- 检查 XSS 漏洞（如 dangerouslySetInnerHTML 的使用）
- 验证用户输入是否被正确验证和转义
- 检查 API 调用是否安全

### 可访问性 (Accessibility)
- 检查是否使用了适当的 ARIA 属性
- 验证语义化 HTML 标签的使用
- 确保键盘导航支持

### TypeScript
- 检查类型定义是否完整和准确
- 验证是否避免了 any 类型的滥用
- 确保接口和类型定义清晰

## Output Format

- 问题严重程度：🔴 严重 | 🟡 警告 | 🔵 建议
- 具体位置和代码片段
- 问题描述
- 改进建议和示例代码
- 相关最佳实践链接（如适用）

## Examples

### 严重问题示例
```
🔴 严重: 潜在 XSS 漏洞
文件: src/components/UserProfile.tsx:25
问题: 使用了 dangerouslySetInnerHTML 且未对内容进行适当清理
建议: 使用 React 组件替代或对内容进行适当的 HTML 转义
```

### 警告问题示例
```
🟡 警告: 性能问题
文件: src/components/ItemList.tsx:42
问题: 在渲染循环中创建新函数，可能导致不必要的重渲染
建议: 将函数移出渲染函数或使用 useCallback 包装
```

### 建议改进示例
```
🔵 建议: 代码可读性
文件: src/utils/helpers.ts:15
问题: 函数名称不够描述性
建议: 将函数名从 processData 更改为更具体的 transformUserData
```