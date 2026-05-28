# RFC 注册表使用指南

> 文档版本: 1.0.0
> 最后更新: 2026-01-16
> 相关文件: `docs/unimplemented/rfc-registry.json`

---

## 概述

RFC 注册表是 OHSpec 项目的中央 RFC 管理系统，用于维护所有 RFC 的列表、状态、分类和关系。它提供了完整的生命周期管理、多维分类、统计分析和自动化维护能力。

## 核心概念

### RFC 生命周期

```
DRAFT → ANALYZING → DESIGNING → PRECHECKING → AUDITING → APPROVED → ARCHIVED
  ↓         ↓           ↓            ↓           ↓
  └─────────┴───────────┴────────────┴───────────┴─→ REJECTED → ARCHIVED
```

**状态说明**：

| 状态 | 描述 | 主要活动 | 下一步 |
|------|------|---------|--------|
| DRAFT | 草稿 | RFC 已创建，等待分析 | 开始分析 |
| ANALYZING | 分析中 | 需求分析、代码扫描、可行性评估 | 进入设计 |
| DESIGNING | 设计中 | 架构设计、接口定义、流程设计 | 进入预检 |
| PRECHECKING | 预检中 | 结构完整性检查、覆盖度检查 | 进入审核 |
| AUDITING | 审核中 | 质量审查、合规性检查、风险评估 | 批准或拒绝 |
| APPROVED | 已批准 | RFC 通过审核，可进入实现 | 归档 |
| REJECTED | 已拒绝 | RFC 未通过审核 | 重新设计或归档 |
| ARCHIVED | 已归档 | RFC 已完成或已放弃 | (终态) |

### 分类标签体系

RFC 注册表支持 7 个独立的标签维度，可组合使用：

1. **功能领域 (domain)**: 10 个值
   - 标识 RFC 涉及的功能领域
   - 示例: audio, video, network, storage, ui, security, performance, testing, devops, api

2. **目标平台 (platform)**: 7 个值
   - 标识 RFC 适用的平台
   - 示例: ios, android, windows, macos, linux, web, cross-platform

3. **优先级 (priority)**: 4 个值
   - 标识 RFC 的优先级
   - 值: critical (紧急), high (高), medium (中), low (低)

4. **复杂度 (complexity)**: 3 个值
   - 标识 RFC 的实现复杂度
   - 值: simple (简单), medium (中等), complex (复杂)

5. **RFC 类型 (type)**: 7 个值
   - 标识 RFC 的类型
   - 示例: feature, enhancement, bugfix, refactor, architecture, documentation, testing

6. **依赖关系 (dependency)**: 4 个值
   - 标识 RFC 间的依赖关系
   - 值: blocks (阻塞), blocked-by (被阻塞), related (相关), duplicates (重复)

7. **风险等级 (risk)**: 4 个值
   - 标识 RFC 的风险等级
   - 值: low-risk (低风险), medium-risk (中风险), high-risk (高风险), breaking-change (破坏性变更)

## RFC 条目结构

### 完整的 RFC 条目示例

```json
{
  "id": "RFC-20260115-3d-audio-toggle-a3f2",
  "title": "3D 音频切换功能",
  "description": "实现 3D 音频效果的开启/关闭切换",
  "status": "analyzing",
  "created_at": "2026-01-15T10:30:00Z",
  "updated_at": "2026-01-15T14:45:00Z",
  "created_by": "user@example.com",
  "owner": "user@example.com",

  "tags": {
    "domain": ["audio"],
    "platform": ["ios", "android"],
    "priority": "high",
    "complexity": "medium",
    "type": "feature",
    "risk": "medium-risk"
  },

  "metadata": {
    "scope": "MEDIUM",
    "needs_spike": false,
    "estimated_effort_hours": 8,
    "target_release": "v2.1.0"
  },

  "progress": {
    "completion_percentage": 25,
    "current_phase": "analyzing",
    "phases_completed": ["dispatcher"]
  },

  "links": {
    "rfc_document": "rfcs/RFC-20260115-3d-audio-toggle-a3f2/rfc.md",
    "findings": "rfcs/RFC-20260115-3d-audio-toggle-a3f2/findings.json",
    "progress": "rfcs/RFC-20260115-3d-audio-toggle-a3f2/progress.json"
  },

  "related_rfcs": [
    {
      "id": "RFC-20260110-audio-effects-b1c3",
      "relationship": "related"
    }
  ],

  "notes": "等待音频框架升级完成"
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | RFC 唯一标识符，格式: RFC-YYYYMMDD-slug-hash4 |
| title | string | 是 | RFC 标题 |
| description | string | 是 | RFC 简短描述 |
| status | string | 是 | 当前状态 |
| created_at | ISO8601 | 是 | 创建时间 |
| updated_at | ISO8601 | 是 | 最后更新时间 |
| created_by | string | 是 | 创建者邮箱 |
| owner | string | 是 | 所有者邮箱 |
| tags | object | 是 | 分类标签 |
| metadata | object | 否 | 元数据 |
| progress | object | 否 | 进度信息 |
| links | object | 是 | 相关文件链接 |
| related_rfcs | array | 否 | 相关 RFC 列表 |
| notes | string | 否 | 备注 |

## 常见操作

### 1. 创建新 RFC

**步骤**:
1. 生成 RFC ID: `RFC-{YYYYMMDD}-{slug}-{hash4}`
2. 创建 RFC 目录: `rfcs/{RFC_ID}/`
3. 初始化文件:
   - `rfc.md` - RFC 文档
   - `findings.json` - 代码扫描结果
   - `progress.json` - 执行进度
4. 添加到注册表:
```json
   {
     "id": "RFC-20260115-...",
     "title": "...",
     "status": "draft",
     "created_at": "2026-01-15T...",
     "tags": { ... },
     "links": { ... }
   }
```

### 2. 更新 RFC 状态

**步骤**:
1. 验证状态转换是否合法
2. 更新 `status` 字段
3. 更新 `updated_at` 时间戳
4. 更新 `progress` 信息
5. 更新统计汇总

**示例**:
```json
{
  "status": "designing",
  "updated_at": "2026-01-15T15:30:00Z",
  "progress": {
    "completion_percentage": 50,
    "current_phase": "designing",
    "phases_completed": ["dispatcher", "analyze"]
  }
}
```

### 3. 查询 RFC

**预定义查询**:

```json
{
  "query": "active",
  "filter": {
    "status": ["analyzing", "designing", "prechecking", "auditing"]
  }
}

{
  "query": "high-priority",
  "filter": {
    "tags.priority": ["critical", "high"]
  }
}

{
  "query": "blocked",
  "filter": {
    "tags.dependency": ["blocked-by"]
  }
}
```

### 4. 生成报告

**支持的报告类型**:

1. **状态报告** (status-report)
   - 显示所有 RFC 的当前状态
   - 字段: id, title, status, priority, created_at, updated_at, owner

2. **时间线报告** (timeline-report)
   - 显示 RFC 创建和完成时间线
   - 字段: id, title, created_at, completed_at, duration_days

3. **依赖关系报告** (dependency-report)
   - 显示 RFC 间的依赖关系
   - 字段: id, title, related_rfcs, blocking_rfcs, blocked_by_rfcs

4. **风险评估报告** (risk-report)
   - 显示 RFC 的风险评估
   - 字段: id, title, risk_level, impact_scope, mitigation_plan

### 5. 归档 RFC

**自动归档规则**:
- 已批准的 RFC: 90 天后自动归档
- 已拒绝的 RFC: 90 天后自动归档

**手动归档**:
```json
{
  "status": "archived",
  "updated_at": "2026-01-15T16:00:00Z"
}
```

## 统计和分析

### 元数据统计

注册表的 `meta` 字段包含实时统计：

```json
"meta": {
  "total_count": 42,
  "status_summary": {
    "draft": 5,
    "analyzing": 8,
    "designing": 12,
    "prechecking": 6,
    "auditing": 7,
    "approved": 3,
    "rejected": 1,
    "archived": 0
  },
  "priority_summary": {
    "critical": 2,
    "high": 15,
    "medium": 20,
    "low": 5
  },
  "complexity_summary": {
    "simple": 10,
    "medium": 22,
    "complex": 10
  }
}
```

### 分析维度

`analytics` 字段支持多维度分析：

- **按状态分组**: 了解各阶段 RFC 数量
- **按优先级分组**: 识别高优先级 RFC
- **按复杂度分组**: 评估工作量
- **按平台分组**: 了解平台覆盖
- **按功能领域分组**: 了解功能分布
- **按类型分组**: 了解变更类型
- **时间线统计**: 了解趋势

## 与其他文件的集成

### 与 progress.json 的关系

```
rfc-registry.json (注册表)
    ↓ 引用
progress.json (执行进度)
    ├── state_machine: 状态转换
    ├── phases: 各阶段进度
    └── observability: 性能指标
```

**同步规则**:
- RFC 状态变更时，同时更新 progress.json 的 `state_machine.current_state`
- progress.json 的 `completion` 字段映射到注册表的 `progress.completion_percentage`

### 与 findings.json 的关系

```
rfc-registry.json (注册表)
    ↓ 引用
findings.json (代码扫描结果)
    ├── confirmed: 已确认的决策和约束
    └── working: 当前阶段的扫描结果
```

**同步规则**:
- findings.json 中的关键决策自动标记为标签
- 风险评估自动更新 RFC 的风险标签

### 与 rfc.md 的关系

```
rfc-registry.json (注册表)
    ↓ 引用
rfc.md (RFC 文档)
    ├── §1: 上下文
    ├── §2: 需求
    ├── §3: 契约
    ├── §4: DFX 约束
    └── §5: 设计决策
```

**同步规则**:
- rfc.md 的元数据自动提取到注册表
- rfc.md 的状态标记自动更新注册表的 status 字段

## 维护策略

### 自动归档

**规则**:
```
IF status == 'approved' AND completed_at < 90 days ago
   THEN status = 'archived'

IF status == 'rejected' AND updated_at < 90 days ago
   THEN status = 'archived'
```

### 自动清理

**规则**:
```
IF status == 'draft' AND created_at < 180 days ago AND no_activity
   THEN remove from registry
```

### 定期备份

**规则**:
- 频率: 每日
- 保留期: 30 天
- 格式: JSON

## 最佳实践

### 1. 及时更新状态

- 每次 RFC 状态变更时立即更新注册表
- 更新 `updated_at` 时间戳
- 添加相关的备注说明

### 2. 准确分类

- 为每个 RFC 分配所有适用的标签
- 优先级应反映业务重要性
- 复杂度应基于实际工作量估计

### 3. 维护关系

- 及时更新 `related_rfcs` 字段
- 标记依赖关系 (blocks, blocked-by)
- 识别重复的 RFC

### 4. 定期审查

- 每周审查活跃 RFC 的进度
- 每月生成状态报告
- 每季度审查已归档 RFC

### 5. 清理过期数据

- 定期清理无活动的草稿 RFC
- 及时归档已完成的 RFC
- 维护备份和历史记录

## 常见问题

### Q1: 如何处理被阻塞的 RFC?

**A**:
1. 在 `tags.dependency` 中标记为 "blocked-by"
2. 在 `related_rfcs` 中指向阻塞它的 RFC
3. 在 `notes` 中说明阻塞原因
4. 定期检查阻塞状态，及时解除

### Q2: 如何处理重复的 RFC?

**A**:
1. 在 `tags.dependency` 中标记为 "duplicates"
2. 在 `related_rfcs` 中指向原始 RFC
3. 将状态设置为 "rejected"
4. 在 `notes` 中说明重复原因

### Q3: 如何处理破坏性变更?

**A**:
1. 在 `tags.risk` 中标记为 "breaking-change"
2. 在 `tags.priority` 中设置为 "high" 或 "critical"
3. 在 RFC 文档中详细说明迁移方案
4. 在 `notes` 中标记需要特别关注

### Q4: 如何查询特定条件的 RFC?

**A**: 使用 `queries.predefined` 中的预定义查询，或自定义过滤条件：
```json
{
  "filter": {
    "status": ["analyzing", "designing"],
    "tags.priority": ["critical", "high"],
    "tags.platform": ["ios"]
  }
}
```

### Q5: 如何生成自定义报告?

**A**: 使用 `export.reports` 中的报告模板，或自定义字段：
```json
{
  "report_id": "custom-report",
  "fields": ["id", "title", "status", "owner", "created_at", "tags.priority"]
}
```

## 相关文档

- [RFC 格式说明](rfc-format.md)
- [RFC 模板](../templates/rfc.md)
- [进度跟踪](../templates/progress.json)
- [代码扫描结果](../templates/findings.json)
- [项目知识库](../templates/project-knowledge.json)

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-01-16 | 初始版本 |

---

**最后更新**: 2026-01-16
**维护者**: OHSpec 项目团队
