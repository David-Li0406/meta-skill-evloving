---
name: decision-making-and-architecture
description: Use this skill when you need to analyze complex problems, make architectural decisions, or optimize performance in software systems.
---

# Skill body

## 使用场景

| 场景 | 触发 |
|:---|:---|
| 架构设计 | Path C |
| 方案对比 | 多个可行方案 |
| 技术选型 | 框架/库选择 |
| 复杂问题分析 | 难以直接解决的问题 |
| 性能审查 | 性能优化需求时 |
| 数据库结构探索 | 理解数据库表和关系 |

## 调用方式

### 深度推理与决策

```javascript
sequential_thinking({
  thought: "分析用户认证方案...",
  thoughtNumber: 1,
  totalThoughts: 5,
  nextThoughtNeeded: true
})
```

### 多方案决策模板

```javascript
寸止.ask({
  question: "发现两个可行方案",
  options: [
    "方案A: JWT + Redis 缓存，性能高，复杂度中",
    "方案B: Session + DB，简单，性能一般"
  ]
})
```

### 性能优化

#### 性能指标

| 指标 | 目标 | 说明 |
|:---|:---|:---|
| **FCP** | < 1.8s | 首次内容渲染 |
| **LCP** | < 2.5s | 最大内容渲染 |
| **FID** | < 100ms | 首次输入延迟 |
| **CLS** | < 0.1 | 累积布局偏移 |
| **TTI** | < 3.8s | 可交互时间 |

#### 性能问题检测

```markdown
## 前端性能检查
- [ ] 是否有不必要的重渲染？
- [ ] 列表是否使用了虚拟滚动？
- [ ] 大数据是否分页？
- [ ] 是否使用了 memo/useMemo/useCallback？

## 后端性能检查
- [ ] 是否有 N+1 查询？
- [ ] 索引是否合理？
- [ ] 是否有慢查询？
```

### 架构探索

#### 工作流程

1. 列出所有表
   ```javascript
   sql_db_list_tables()
   ```

2. 获取特定表的架构
   ```javascript
   sql_db_schema("表名")
   ```

3. 映射关系
   - 查找以 "Id" 结尾的列
   - 识别外键与主键的关系

4. 回答问题
   - 提供可用表及其用途
   - 列名及其内容
   - 表之间的关联方式

## 质量指南

- 对于"列出表"问题，显示所有表名及简要描述。
- 对于"描述表"问题，列出所有列及其数据类型，示例数据，主键和外键信息。

## 常见探索模式

- "哪个表包含客户信息？" → 使用 list_tables，然后描述 Customer 表。
- "Invoice 表中有什么？" → 使用 schema 工具显示列和示例数据。
- "客户如何与发票关联？" → 追踪外键链：Customer → Invoice → InvoiceLine。

## 降级方案

sequential-thinking不可用时 → 使用 Extended Thinking 模式。