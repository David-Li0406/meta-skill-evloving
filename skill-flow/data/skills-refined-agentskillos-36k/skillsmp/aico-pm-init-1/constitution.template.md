# [PRODUCT_NAME] 产品宪章

> Project: [PROJECT_NAME]
> Created: [CREATED_DATE]
> Last Updated: [UPDATED_DATE]

本文档为所有产品管理活动提供共享约束和领域信息。

---

## 产品概述

### 基本信息

| 项目           | 内容                   |
| -------------- | ---------------------- |
| **产品名称**   | [PRODUCT_NAME]         |
| **一句话定义** | [ONE_LINE_DESCRIPTION] |
| **Slogan**     | [SLOGAN]               |
| **当前版本**   | v1.0.0                 |

### 目标用户

| 用户类型     | 描述                         |
| ------------ | ---------------------------- |
| **主要用户** | [PRIMARY_USER_DESCRIPTION]   |
| **次要用户** | [SECONDARY_USER_DESCRIPTION] |

### 核心价值主张

[CORE_VALUE_PROPOSITION]

---

## 领域信息

### 行业/市场背景

[INDUSTRY_CONTEXT]

### 核心术语

| 术语         | 定义           |
| ------------ | -------------- |
| **[TERM_1]** | [DEFINITION_1] |
| **[TERM_2]** | [DEFINITION_2] |

### 合规要求

- [ ] 无特殊合规要求
- [ ] GDPR
- [ ] SOC 2
- [ ] 其他: [SPECIFY]

---

## 技术约束

| 约束         | 说明              |
| ------------ | ----------------- |
| **语言**     | [LANGUAGE]        |
| **运行环境** | [RUNTIME]         |
| **主要框架** | [FRAMEWORK]       |
| **包管理**   | [PACKAGE_MANAGER] |

---

## 业务约束

| 约束类型 | 说明                   |
| -------- | ---------------------- |
| **预算** | [BUDGET_CONSTRAINTS]   |
| **时间** | [TIMELINE_CONSTRAINTS] |
| **资源** | [RESOURCE_CONSTRAINTS] |

---

## 标准规范

### 文档语言

- [ ] 中文
- [ ] English
- [ ] 双语

### 命名规范

| 类型     | 规范       | 示例           |
| -------- | ---------- | -------------- |
| 版本号   | 语义化版本 | v1.0.0, v1.1.0 |
| 故事编号 | S-XXX      | S-001, S-002   |
| 任务编号 | T-XXX      | T-001, T-002   |

### 版本规范

- 遵循语义化版本（SemVer）
- 格式：`v{major}.{minor}.{patch}`
- Major: 重大变更，不兼容
- Minor: 新功能，向后兼容
- Patch: Bug 修复

---

## 项目结构

```
docs/reference/
├── pm/
│   ├── constitution.md     # 本文档
│   ├── versions/           # 版本规划
│   │   └── v1.0.0.md
│   └── stories/            # 用户故事
│       ├── S-001.md
│       └── ...
├── frontend/
│   ├── design-system.md    # 设计系统
│   ├── constraints.md      # 前端约束
│   ├── designs/            # 页面设计
│   └── tasks/              # 前端任务
└── backend/
    ├── constraints.md      # 后端约束
    └── tasks/              # 后端任务
```

---

## Git 规范

### 提交信息

- 使用 Conventional Commits
- 格式：`type(scope): subject`
- 类型：feat, fix, docs, style, refactor, test, chore

### 分支命名

```
feature/[feature-name]
fix/[bug-description]
refactor/[area]
```
