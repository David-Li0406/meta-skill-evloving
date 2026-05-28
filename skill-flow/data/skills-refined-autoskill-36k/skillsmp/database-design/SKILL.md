---
name: database-design
description: 数据库表结构设计工具。当用户需要设计数据库、创建表结构、建立实体关系或优化索引时使用。支持 MySQL、PostgreSQL 等关系型数据库。
---

# 数据库设计

## 概述
本 Skill 用于数据库表结构设计，确保数据模型规范、可扩展、高性能。适用于任何关系型数据库。

## 使用场景
- 新项目数据库设计
- 功能模块数据建模
- 数据库重构优化

---

## 设计流程

```
需求分析 → 实体识别 → 关系建模 → 表结构设计 → 索引优化 → 迁移脚本
```

---

## 命名规范

### 表名规范
| 规则 | 示例 |
|------|------|
| 使用小写下划线 | `user_role` |
| 使用单数名词 | `user` 而非 `users` |
| 关联表：两表名拼接 | `user_role`、`role_permission` |

### 字段名规范
| 规则 | 示例 |
|------|------|
| 使用小写下划线 | `created_at` |
| 主键统一命名 | `id` |
| 外键：表名_id | `user_id`、`role_id` |
| 布尔字段：is_前缀 | `is_active`、`is_deleted` |
| 时间字段：_at后缀 | `created_at`、`updated_at` |

---

## 必备字段

### 基础字段
```sql
id          BIGINT PRIMARY KEY AUTO_INCREMENT,  -- 主键
created_at  DATETIME DEFAULT CURRENT_TIMESTAMP, -- 创建时间
updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- 更新时间
```

### 软删除字段
```sql
is_deleted  TINYINT DEFAULT 0,  -- 删除标记
deleted_at  DATETIME            -- 删除时间
```

---

## 数据类型选择

| 场景 | MySQL | PostgreSQL |
|------|-------|------------|
| 主键 | BIGINT | BIGSERIAL |
| 短文本 | VARCHAR(N) | VARCHAR(N) |
| 长文本 | TEXT | TEXT |
| 小数 | DECIMAL(M,N) | NUMERIC(M,N) |
| 布尔 | TINYINT(1) | BOOLEAN |
| 日期时间 | DATETIME | TIMESTAMP |
| JSON | JSON | JSONB |

---

## 索引设计原则

1. **WHERE 条件字段**：经常用于查询的字段
2. **外键字段**：关联查询必须有索引
3. **排序字段**：ORDER BY 的字段
4. **联合索引最左原则**：把区分度高的字段放前面
5. **避免过度索引**：索引会降低写入性能

### 索引命名规范
```sql
pk_表名           -- 主键
uk_表名_字段名    -- 唯一索引
idx_表名_字段名   -- 普通索引
```

---

## 输出物清单

- [ ] 实体关系图（ER图描述）
- [ ] 表结构设计文档 (`docs/database-design.md`)
- [ ] SQL 建表脚本 (`sql/schema.sql`)
- [ ] 索引设计说明
- [ ] 初始化数据脚本 (`sql/init-data.sql`)
