---
name: comprehensive-architecture-and-performance-analysis
description: Use this skill for deep reasoning in architecture design, performance optimization, and database schema exploration.
---

# Comprehensive Architecture and Performance Analysis Skill

This skill combines deep reasoning for complex decision-making, performance optimization techniques, and database schema exploration.

## 1. Thinking Skill (Sequential Thinking)

### 深度推理引擎

用于复杂问题分析和架构决策。

### 使用场景

| 场景 | 触发 |
|:---|:---|
| 架构设计 | Path C |
| 方案对比 | 多个可行方案 |
| 技术选型 | 框架/库选择 |
| 复杂问题分析 | 难以直接解决的问题 |

### 调用方式

```javascript
sequential_thinking({
  thought: "分析用户认证方案...",
  thoughtNumber: 1,
  totalThoughts: 5,
  nextThoughtNeeded: true
})
```

### Linus 审查清单 (Torvalds' Test)

每次深度思考后必须检查：

- [ ] **Data First**: 数据结构是最简的吗？
- [ ] **Naming**: 命名准确反映本质？
- [ ] **Simplicity**: 是否过度设计？
- [ ] **Compatibility**: 向后兼容？

### I阶段（创新）标准流程

```
1. 使用 sequential-thinking 深度推演
2. 应用 Linus 审查清单
3. 若存在 >= 2 个可行方案:
   → 调用 寸止 展示选项
   → 等待用户选择
   → 禁止自作主张
```

## 2. Performance Skill

### 性能优化技能

> **性能是功能的一部分**
> 用户感知的响应时间决定产品体验

### 🎯 性能指标

#### 前端指标

| 指标 | 目标 | 说明 |
|:---|:---|:---|
| **FCP** | < 1.8s | 首次内容渲染 |
| **LCP** | < 2.5s | 最大内容渲染 |
| **FID** | < 100ms | 首次输入延迟 |
| **CLS** | < 0.1 | 累积布局偏移 |
| **TTI** | < 3.8s | 可交互时间 |

#### 后端指标

| 指标 | 目标 | 说明 |
|:---|:---|:---|
| **响应时间** | < 200ms | API 响应 |
| **吞吐量** | 根据需求 | QPS |
| **错误率** | < 0.1% | 5xx 错误 |
| **P99 延迟** | < 1s | 99分位延迟 |

### 🔍 性能问题检测

#### 前端检测清单

```markdown
## 前端性能检查

### 渲染性能
- [ ] 是否有不必要的重渲染？
- [ ] 列表是否使用了虚拟滚动？
- [ ] 大数据是否分页？
- [ ] 是否使用了 memo/useMemo/useCallback？

### 资源加载
- [ ] 图片是否压缩/懒加载？
- [ ] JS/CSS 是否分包？
- [ ] 是否使用了 CDN？
- [ ] 是否启用了缓存？

### 包体积
- [ ] 是否有未使用的依赖？
- [ ] 是否按需加载？
- [ ] 是否 tree-shaking？
```

#### 后端检测清单

```markdown
## 后端性能检查

### 数据库
- [ ] 是否有 N+1 查询？
- [ ] 索引是否合理？
- [ ] 是否有慢查询？
- [ ] 是否使用了连接池？

### 缓存
- [ ] 热点数据是否缓存？
- [ ] 缓存策略是否合理？
- [ ] 缓存是否会穿透？

### 并发
- [ ] 是否有竞态条件？
- [ ] 锁粒度是否合适？
- [ ] 是否有死锁风险？
```

## 3. Schema Exploration Skill

### 架构探索技能

用于发现和理解数据库结构、表、列和关系。

### 何时使用此技能

当您需要以下操作时使用此技能：
- 理解数据库结构
- 查找包含特定类型数据的表
- 发现列名和数据类型
- 映射表之间的关系
- 回答诸如"有哪些表可用？"或"Customer 表有哪些列？"等问题

### 工作流程

#### 1. 列出所有表
使用 `sql_db_list_tables` 工具查看数据库中所有可用的表。

#### 2. 获取特定表的架构
使用 `sql_db_schema` 工具配合表名来检查：
- **列名** - 有哪些字段可用
- **数据类型** - INTEGER, TEXT, DATETIME 等
- **示例数据** - 3 行示例数据以了解内容
- **主键** - 行的唯一标识符
- **外键** - 与其他表的关系

#### 3. 映射关系
识别表之间的连接方式：
- 查找以 "Id" 结尾的列（例如，CustomerId, ArtistId）
- 外键链接到其他表的主键
- 记录父子关系

#### 4. 回答问题
提供清晰的信息：
- 可用表及其用途
- 列名及其包含的内容
- 表之间的关联方式
- 示例数据以说明内容

## 常见探索模式

### 模式 1：查找表
"哪个表包含客户信息？"
→ 使用 list_tables，然后描述 Customer 表

### 模式 2：理解结构
"Invoice 表中有什么？"
→ 使用 schema 工具显示列和示例数据

### 模式 3：映射关系
"客户如何与发票关联？"
→ 追踪外键链：Customer → Invoice → InvoiceLine

## 提示

- 外键通常以 "Id" 结尾，并匹配表名
- 使用示例数据了解值的格式
- 不确定使用哪个表时，先列出所有表