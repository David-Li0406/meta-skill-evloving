---
name: dependency-updater
description: 智能依赖更新助手。自动检查、分析和更新项目依赖，确保安全性和兼容性。
trigger: 当用户需要更新依赖、检查漏洞或管理包版本时使用
---

# Dependency Updater

智能依赖管理和更新助手，帮助保持项目依赖的安全性和最新性。

## 功能特性

- 自动检测过时的依赖
- 安全漏洞扫描
- 破坏性变更分析
- 兼容性检查
- 批量更新建议
- 更新日志生成

## 使用场景

1. **定期维护**: 每月/季度依赖更新
2. **安全修复**: 紧急修复已知漏洞
3. **版本升级**: 主要版本升级规划
4. **新项目审计**: 检查依赖健康度

## 核心功能

### 依赖分析
- 检测过时的包
- 识别安全漏洞
- 分析依赖树
- 检查许可证兼容性
- 评估包质量

### 更新策略
- **Conservative**: 仅补丁版本更新
- **Moderate**: 次要版本更新
- **Aggressive**: 主要版本更新
- **Security**: 仅安全修复

### 兼容性检查
- 破坏性变更检测
- API 变更分析
- 依赖冲突解决
- TypeScript 类型兼容性

## 使用方法

```bash
# 检查所有过时的依赖
/dependency-updater check

# 检查安全漏洞
/dependency-updater audit

# 更新所有依赖（保守策略）
/dependency-updater update --conservative

# 更新特定包
/dependency-updater update react react-dom

# 主要版本升级
/dependency-updater upgrade --major

# 生成更新报告
/dependency-updater report

# 交互式更新
/dependency-updater interactive
```

## 更新流程

1. **分析阶段**
   - 扫描 package.json
   - 检查可用更新
   - 识别安全漏洞
   - 分析破坏性变更

2. **规划阶段**
   - 生成更新计划
   - 评估风险等级
   - 建议更新顺序
   - 预估影响范围

3. **执行阶段**
   - 创建备份分支
   - 逐步更新依赖
   - 运行测试套件
   - 验证构建

4. **验证阶段**
   - 运行单元测试
   - 执行 E2E 测试
   - 检查类型错误
   - 验证功能完整性

## 输出格式

### 依赖报告

```
📦 Dependency Update Report

🔴 Critical Security Issues (2)
  - axios@0.21.1 → 1.6.0 (CVE-2023-45857)
  - lodash@4.17.19 → 4.17.21 (Prototype Pollution)

🟠 Major Updates Available (5)
  - react@18.2.0 → 19.0.0 (Breaking changes)
  - typescript@5.0.0 → 5.3.0 (New features)

🟡 Minor Updates (12)
  - vite@4.5.0 → 4.5.2 (Bug fixes)
  - eslint@8.50.0 → 8.57.0 (Improvements)

✅ Up to date (45 packages)

Total: 64 dependencies
Outdated: 19 (29.7%)
Vulnerable: 2 (3.1%)
```

### 更新计划

```
📋 Update Plan (Conservative Strategy)

Phase 1: Security Fixes (High Priority)
  ✓ axios@0.21.1 → 1.6.0
  ✓ lodash@4.17.19 → 4.17.21

Phase 2: Patch Updates (Low Risk)
  ○ vite@4.5.0 → 4.5.2
  ○ eslint@8.50.0 → 8.57.0
  ○ prettier@3.0.0 → 3.0.3

Phase 3: Minor Updates (Medium Risk)
  ○ typescript@5.0.0 → 5.3.0
  ○ @types/react@18.2.0 → 18.2.45

Phase 4: Major Updates (High Risk - Manual Review)
  ⚠ react@18.2.0 → 19.0.0
  ⚠ react-dom@18.2.0 → 19.0.0

Estimated time: 2-3 hours
Risk level: Medium
```

## 配置

在 `.claude/settings.json` 中配置更新策略：

```json
{
  "dependencyUpdater": {
    "strategy": "moderate",
    "autoUpdate": {
      "patch": true,
      "minor": false,
      "major": false
    },
    "excludePackages": ["legacy-package"],
    "testBeforeUpdate": true,
    "createBackupBranch": true,
    "notifyOnVulnerabilities": true
  }
}
```

## 最佳实践

1. **定期检查**: 每周运行依赖审计
2. **安全优先**: 立即修复安全漏洞
3. **渐进更新**: 分阶段更新依赖
4. **充分测试**: 更新后运行完整测试
5. **文档记录**: 记录重大更新和变更
6. **回滚准备**: 保持回滚能力

## 风险评估

### 低风险更新
- 补丁版本更新
- 安全修复
- Bug 修复

### 中风险更新
- 次要版本更新
- 新功能添加
- 性能改进

### 高风险更新
- 主要版本更新
- 破坏性变更
- API 重构

## 集成

与其他 Skills 配合使用：

- `security-audit`: 安全漏洞深度分析
- `test-driven-development`: 更新后测试验证
- `verification-before-completion`: 更新验证
- `systematic-debugging`: 更新问题排查
