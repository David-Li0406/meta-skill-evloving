---
name: sqlite-db-ops
description: SQLite 数据库操作技能，提供完整的增删改查 (CRUD) 功能。使用此技能当需要：(1) 创建或管理 SQLite 数据库，(2) 执行数据库的增删改查操作，(3) 批量数据导入导出，(4) 执行自定义 SQL 查询，(5) 查看数据库结构和表信息。支持通过本地 Python 脚本进行可靠的数据库操作。
---

# SQLite 数据库操作技能

此技能提供完整的 SQLite 数据库操作功能，包括创建表、插入数据、查询数据、更新数据和删除数据。

## 核心脚本

使用 [`scripts/db_operations.py`](scripts/db_operations.py) 执行所有数据库操作。此脚本提供：

- 创建数据库和表
- 插入单条或批量数据
- 灵活的查询功能（支持 WHERE、ORDER BY、LIMIT）
- 更新和删除数据
- 执行自定义 SQL 语句
- 查看数据库表结构

## 使用方法

### 1. 创建表

```bash
python3 scripts/db_operations.py <数据库路径> create_table \
  --table <表名> \
  --columns '<列定义JSON>'
```

**示例**：
```bash
python3 scripts/db_operations.py data.db create_table \
  --table users \
  --columns '{"id": "INTEGER PRIMARY KEY AUTOINCREMENT", "name": "TEXT NOT NULL", "email": "TEXT", "age": "INTEGER"}'
```

### 2. 插入数据

**插入单条数据**：
```bash
python3 scripts/db_operations.py <数据库路径> insert \
  --table <表名> \
  --data '<数据JSON>'
```

**示例**：
```bash
python3 scripts/db_operations.py data.db insert \
  --table users \
  --data '{"name": "张三", "email": "zhangsan@example.com", "age": 25}'
```

**批量插入**：
```bash
python3 scripts/db_operations.py data.db insert \
  --table users \
  --data '[{"name": "李四", "email": "lisi@example.com", "age": 30}, {"name": "王五", "email": "wangwu@example.com", "age": 28}]'
```

### 3. 查询数据

```bash
python3 scripts/db_operations.py <数据库路径> query \
  --table <表名> \
  [--columns <列名>] \
  [--where <WHERE子句>] \
  [--params <参数JSON数组>] \
  [--order-by <排序字段>] \
  [--limit <限制数量>]
```

**示例**：

查询所有数据：
```bash
python3 scripts/db_operations.py data.db query --table users
```

条件查询：
```bash
python3 scripts/db_operations.py data.db query \
  --table users \
  --where 'age > ?' \
  --params '[25]'
```

指定列和排序：
```bash
python3 scripts/db_operations.py data.db query \
  --table users \
  --columns 'name, email' \
  --order-by 'age DESC' \
  --limit 10
```

### 4. 更新数据

```bash
python3 scripts/db_operations.py <数据库路径> update \
  --table <表名> \
  --data '<更新数据JSON>' \
  --where <WHERE子句> \
  [--params <参数JSON数组>]
```

**示例**：
```bash
python3 scripts/db_operations.py data.db update \
  --table users \
  --data '{"age": 26}' \
  --where 'name = ?' \
  --params '["张三"]'
```

### 5. 删除数据

```bash
python3 scripts/db_operations.py <数据库路径> delete \
  --table <表名> \
  --where <WHERE子句> \
  [--params <参数JSON数组>]
```

**示例**：
```bash
python3 scripts/db_operations.py data.db delete \
  --table users \
  --where 'age < ?' \
  --params '[20]'
```

### 6. 执行自定义 SQL

```bash
python3 scripts/db_operations.py <数据库路径> execute \
  --sql '<SQL语句>' \
  [--params <参数JSON数组>]
```

**示例**：
```bash
python3 scripts/db_operations.py data.db execute \
  --sql 'SELECT name, COUNT(*) as count FROM users GROUP BY name'
```

### 7. 查看数据库信息

**列出所有表**：
```bash
python3 scripts/db_operations.py data.db list_tables
```

**查看表结构**：
```bash
python3 scripts/db_operations.py data.db table_info --table users
```

### 8. 输出到文件

所有查询操作都支持 `--output` 参数将结果保存为 JSON 文件：

```bash
python3 scripts/db_operations.py data.db query \
  --table users \
  --output results.json
```

## 在代码中使用

脚本也可以作为 Python 模块导入使用：

```python
from scripts.db_operations import SQLiteDB

# 使用上下文管理器
with SQLiteDB('data.db') as db:
    # 创建表
    db.create_table('users', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'name': 'TEXT NOT NULL',
        'email': 'TEXT',
        'age': 'INTEGER'
    })
    
    # 插入数据
    db.insert('users', {'name': '张三', 'email': 'zhangsan@example.com', 'age': 25})
    
    # 查询数据
    results = db.query('users', where='age > ?', params=(20,))
    
    # 更新数据
    db.update('users', {'age': 26}, where='name = ?', params=('张三',))
    
    # 删除数据
    db.delete('users', where='id = ?', params=(1,))
```

## 最佳实践

1. **使用参数化查询**：始终使用 `?` 占位符和 `--params` 参数来防止 SQL 注入
2. **备份数据库**：在执行批量更新或删除操作前，先备份数据库文件
3. **验证数据**：使用查询操作验证插入、更新或删除的结果
4. **事务处理**：脚本会自动提交事务，批量操作会在一个事务中完成
5. **错误处理**：脚本会捕获并显示详细的错误信息

## 常见 SQLite 数据类型

- `INTEGER` - 整数
- `REAL` - 浮点数
- `TEXT` - 文本字符串
- `BLOB` - 二进制数据
- `NULL` - 空值

## 常见约束

- `PRIMARY KEY` - 主键
- `AUTOINCREMENT` - 自动递增
- `NOT NULL` - 非空
- `UNIQUE` - 唯一
- `DEFAULT <值>` - 默认值
- `CHECK (<条件>)` - 检查约束
- `FOREIGN KEY` - 外键

## 工作流程示例

### 示例 1：创建用户管理系统

```bash
# 1. 创建数据库和表
python3 scripts/db_operations.py users.db create_table \
  --table users \
  --columns '{"id": "INTEGER PRIMARY KEY AUTOINCREMENT", "username": "TEXT UNIQUE NOT NULL", "email": "TEXT NOT NULL", "created_at": "TEXT DEFAULT CURRENT_TIMESTAMP"}'

# 2. 插入用户
python3 scripts/db_operations.py users.db insert \
  --table users \
  --data '{"username": "admin", "email": "admin@example.com"}'

# 3. 查询所有用户
python3 scripts/db_operations.py users.db query --table users

# 4. 更新用户邮箱
python3 scripts/db_operations.py users.db update \
  --table users \
  --data '{"email": "newemail@example.com"}' \
  --where 'username = ?' \
  --params '["admin"]'
```

### 示例 2：数据分析

```bash
# 1. 创建销售数据表
python3 scripts/db_operations.py sales.db create_table \
  --table sales \
  --columns '{"id": "INTEGER PRIMARY KEY AUTOINCREMENT", "product": "TEXT", "amount": "REAL", "date": "TEXT"}'

# 2. 批量导入数据
python3 scripts/db_operations.py sales.db insert \
  --table sales \
  --data '[
    {"product": "产品A", "amount": 1500.50, "date": "2024-01-01"},
    {"product": "产品B", "amount": 2300.00, "date": "2024-01-02"},
    {"product": "产品A", "amount": 1800.00, "date": "2024-01-03"}
  ]'

# 3. 执行聚合查询
python3 scripts/db_operations.py sales.db execute \
  --sql 'SELECT product, SUM(amount) as total, COUNT(*) as count FROM sales GROUP BY product'

# 4. 导出结果
python3 scripts/db_operations.py sales.db query \
  --table sales \
  --order-by 'date DESC' \
  --output sales_report.json
```

## 注意事项

- 数据库文件路径可以是相对路径或绝对路径
- 如果数据库文件不存在，会自动创建
- JSON 参数需要使用单引号包裹（在 shell 中）
- WHERE 子句不需要包含 `WHERE` 关键字
- 使用参数化查询时，参数必须是 JSON 数组格式
