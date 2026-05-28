---
name: ai-code-reviewer
description: AI 驱动的代码审查助手。自动分析代码质量、安全漏洞、性能问题和最佳实践违规。
trigger: 当用户请求代码审查、质量检查或安全审计时使用
---

# AI Code Reviewer

AI 驱动的智能代码审查助手，提供全面的代码质量分析。

## 功能特性

- 自动检测代码质量问题
- 识别安全漏洞和潜在风险
- 性能优化建议
- 最佳实践检查
- 代码复杂度分析
- 依赖安全审计

## 使用场景

1. **Pull Request 审查**: 在合并前进行全面代码审查
2. **重构前评估**: 识别需要重构的代码区域
3. **安全审计**: 检查安全漏洞和风险
4. **性能优化**: 发现性能瓶颈

## 审查维度

### 代码质量
- 代码可读性和可维护性
- 命名规范
- 代码复杂度（圈复杂度）
- 重复代码检测
- 代码异味识别

### 安全性
- OWASP Top 10 漏洞检查
- SQL 注入风险
- XSS 漏洞
- CSRF 防护
- 敏感信息泄露
- 依赖安全漏洞

### 性能
- 算法复杂度分析
- 内存泄漏风险
- 不必要的重渲染
- 数据库查询优化
- 缓存策略

### 最佳实践
- TypeScript 类型安全
- React Hooks 使用规范
- 错误处理
- 日志记录
- 测试覆盖率

## 使用方法

```bash
# 审查当前分支的所有更改
/ai-code-reviewer

# 审查特定文件
/ai-code-reviewer src/components/UserProfile.tsx

# 审查特定 PR
/ai-code-reviewer --pr 123

# 仅检查安全问题
/ai-code-reviewer --security-only

# 生成详细报告
/ai-code-reviewer --detailed
```

## 输出格式

审查结果按严重程度分类：

- 🔴 **Critical**: 必须立即修复的严重问题
- 🟠 **High**: 应该尽快修复的重要问题
- 🟡 **Medium**: 建议修复的中等问题
- 🔵 **Low**: 可选的改进建议
- ℹ️ **Info**: 信息性提示

## 配置

在 `.claude/settings.json` 中配置审查规则：

```json
{
  "aiCodeReviewer": {
    "severity": ["critical", "high", "medium"],
    "categories": ["security", "performance", "quality"],
    "excludePatterns": ["*.test.ts", "*.spec.ts"],
    "customRules": []
  }
}
```

## 最佳实践

1. 在提交 PR 前运行审查
2. 优先修复 Critical 和 High 级别问题
3. 定期审查核心代码模块
4. 结合自动化 CI/CD 流程
5. 团队共享审查标准

## 示例

### 审查结果示例

```
🔴 Critical: SQL Injection vulnerability detected
  File: src/services/userService.ts:42
  Issue: Unsanitized user input in SQL query
  Fix: Use parameterized queries or ORM

🟠 High: Memory leak risk
  File: src/components/Dashboard.tsx:78
  Issue: Event listener not cleaned up in useEffect
  Fix: Add cleanup function to useEffect

🟡 Medium: Code complexity
  File: src/utils/dataProcessor.ts:156
  Issue: Function has cyclomatic complexity of 15
  Fix: Break down into smaller functions
```

## 集成

与其他 Skills 配合使用：

- `security-audit`: 深度安全审计
- `performance-optimization`: 性能优化建议
- `code-review-checklist`: 人工审查清单
- `typescript-standards`: TypeScript 规范检查
