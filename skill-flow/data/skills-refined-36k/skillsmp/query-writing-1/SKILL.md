---
name: query-writing
description: 用于编写和执行 SQL 查询 - 从简单的单表查询到复杂的多表 JOIN 和聚合操作
---

# 查询编写技能

## 何时使用此技能

当您需要通过编写和执行 SQL 查询来回答问题时应使用此技能。

## 简单查询工作流程

对于涉及单个表的直接问题：

1. **识别表** - 哪个表包含所需数据？
2. **获取架构** - 使用 `sql_db_schema` 查看列
3. **编写查询** - 使用 WHERE/LIMIT/ORDER BY 选择相关列
4. **执行** - 使用 `sql_db_query` 运行
5. **格式化答案** - 清晰地呈现结果

## 复杂查询工作流程

对于需要多个表的问题：

### 1. 规划方法
**使用 `write_todos` 分解任务：**
- 识别所有需要的表
- 映射关系（外键）
- 规划 JOIN 结构
- 确定聚合操作

### 2. 检查架构
对每个表使用 `sql_db_schema` 查找连接列和所需字段。

### 3. 构建查询
- SELECT - 列和聚合函数
- FROM/JOIN - 通过 FK = PK 连接表
- WHERE - 聚合前的过滤条件
- GROUP BY - 所有非聚合列
- ORDER BY - 有意义的排序
- LIMIT - 默认 5 行

### 4. 验证和执行
检查所有 JOIN 都有条件，GROUP BY 正确，然后运行查询。

## 示例：按国家统计收入
```sql
SELECT
    c.Country,
    ROUND(SUM(i.Total), 2) as TotalRevenue
FROM Invoice i
INNER JOIN Customer c ON i.CustomerId = c.CustomerId
GROUP BY c.Country
ORDER BY TotalRevenue DESC
LIMIT 5;
```

## 质量指南

- 只查询相关列（不使用 SELECT *）
- 始终应用 LIMIT（默认 10）
- 使用表别名以提高清晰度
- 对于复杂查询：使用 write_todos 进行规划
- 绝不使用 DML 语句（INSERT, UPDATE, DELETE, DROP）
