---
name: database-manager
description: |
  数据库管理统一接口，支持 Supabase (PostgreSQL)、PlanetScale (MySQL)、Turso (SQLite) 等主流数据库服务。
  提供连接管理、CRUD 操作、迁移、RLS 策略配置等功能。用于快速集成数据库到 Agent 系统。
version: 1.0.0
author: AgentFlow Team
triggers:
  - database
  - db
  - supabase
  - planetscale
  - turso
  - postgresql
  - mysql
  - sqlite
  - crud
  - migration
  - rls
  - schema
requirements:
  - supabase>=2.0.0
  - libsql-experimental>=0.0.34
  - asyncpg>=0.29.0
  - sqlalchemy>=2.0.0
tags:
  - database
  - backend
  - infrastructure
  - production-ready
examples:
  - "连接 Supabase 数据库"
  - "创建用户表并设置 RLS"
  - "执行数据库迁移"
  - "CRUD 操作示例"
---

# Database Manager Skill

## 概述

统一的数据库管理接口，让 Agent 能够快速、安全地操作数据库。

## 支持的数据库

| 数据库 | 类型 | 免费额度 | 特点 |
|--------|------|----------|------|
| **Supabase** | PostgreSQL | 500MB | RLS、实时订阅、Edge Functions |
| **PlanetScale** | MySQL | 5GB | 分支功能、无锁 Schema 变更 |
| **Turso** | SQLite (libSQL) | 9GB | 边缘部署、低延迟 |
| **Neon** | PostgreSQL | 512MB | Serverless、分支 |

## 快速开始

### 1. Supabase 连接

```python
from agentflow.skills.builtin.database_manager import DatabaseManager, SupabaseConfig

# 配置
config = SupabaseConfig(
    url="https://xxx.supabase.co",
    anon_key="eyJ...",
    service_role_key="eyJ..."  # 可选，用于绕过 RLS
)

# 初始化
db = DatabaseManager(provider="supabase", config=config)
await db.connect()

# CRUD 操作
users = await db.select("users", filters={"status": "active"})
new_user = await db.insert("users", {"email": "test@example.com", "name": "Test"})
await db.update("users", {"name": "Updated"}, filters={"id": new_user["id"]})
await db.delete("users", filters={"id": new_user["id"]})
```

### 2. Turso 连接

```python
from agentflow.skills.builtin.database_manager import DatabaseManager, TursoConfig

config = TursoConfig(
    url="libsql://xxx.turso.io",
    auth_token="your-token"
)

db = DatabaseManager(provider="turso", config=config)
await db.connect()

# 使用原生 SQL
result = await db.execute("SELECT * FROM users WHERE status = ?", ["active"])
```

### 3. 通用 PostgreSQL

```python
from agentflow.skills.builtin.database_manager import DatabaseManager, PostgresConfig

config = PostgresConfig(
    host="localhost",
    port=5432,
    database="myapp",
    user="postgres",
    password="password"
)

db = DatabaseManager(provider="postgres", config=config)
await db.connect()
```

## Schema 管理

### 创建表

```python
# 定义 Schema
schema = {
    "users": {
        "columns": [
            {"name": "id", "type": "uuid", "primary": True, "default": "gen_random_uuid()"},
            {"name": "email", "type": "text", "unique": True, "not_null": True},
            {"name": "name", "type": "text"},
            {"name": "created_at", "type": "timestamptz", "default": "now()"},
        ],
        "rls": {
            "enabled": True,
            "policies": [
                {
                    "name": "users_select_own",
                    "operation": "SELECT",
                    "check": "auth.uid() = id"
                },
                {
                    "name": "users_update_own",
                    "operation": "UPDATE",
                    "check": "auth.uid() = id"
                }
            ]
        }
    }
}

# 应用 Schema
await db.apply_schema(schema)
```

### 迁移

```python
# 创建迁移
migration = await db.create_migration("add_avatar_to_users", """
    ALTER TABLE users ADD COLUMN avatar_url TEXT;
""")

# 执行迁移
await db.run_migrations()

# 回滚
await db.rollback_migration("add_avatar_to_users")
```

## RLS 策略（Row Level Security）

### Supabase RLS 最佳实践

```python
# 启用 RLS
await db.enable_rls("users")

# 添加策略
await db.add_rls_policy(
    table="users",
    name="users_isolation",
    operation="ALL",
    using="auth.uid() = user_id",
    with_check="auth.uid() = user_id"
)

# 服务端绕过 RLS（使用 service_role_key）
admin_db = DatabaseManager(
    provider="supabase",
    config=SupabaseConfig(
        url="...",
        service_role_key="..."  # 绕过 RLS
    )
)
```

## 实时订阅（Supabase）

```python
# 订阅表变更
async def on_change(payload):
    print(f"变更: {payload}")

subscription = await db.subscribe(
    table="messages",
    event="INSERT",
    callback=on_change,
    filters={"room_id": "eq.123"}
)

# 取消订阅
await subscription.unsubscribe()
```

## 事务处理

```python
async with db.transaction() as tx:
    user = await tx.insert("users", {"email": "test@example.com"})
    await tx.insert("profiles", {"user_id": user["id"], "bio": "Hello"})
    # 自动提交或回滚
```

## 连接池管理

```python
# 配置连接池
db = DatabaseManager(
    provider="postgres",
    config=PostgresConfig(...),
    pool_size=10,
    max_overflow=20
)

# 健康检查
is_healthy = await db.health_check()

# 获取连接统计
stats = db.get_pool_stats()
print(f"活跃连接: {stats['active']}, 空闲: {stats['idle']}")
```

## 最佳实践

### 1. 环境变量管理

```python
import os

config = SupabaseConfig(
    url=os.environ["SUPABASE_URL"],
    anon_key=os.environ["SUPABASE_ANON_KEY"],
    service_role_key=os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
)
```

### 2. 类型安全的查询

```python
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: str
    email: str
    name: Optional[str]

# 带类型验证的查询
users: list[User] = await db.select("users", model=User)
```

### 3. 错误处理

```python
from agentflow.skills.builtin.database_manager import (
    DatabaseError,
    ConnectionError,
    QueryError,
    RLSError
)

try:
    await db.insert("users", data)
except ConnectionError as e:
    logger.error(f"连接失败: {e}")
except RLSError as e:
    logger.error(f"RLS 策略阻止: {e}")
except QueryError as e:
    logger.error(f"查询错误: {e}")
```

## Agent 集成示例

```python
from agentflow.skills import SkillEngine
from agentflow.skills.builtin.database_manager import DatabaseManager

# 作为 Agent Tool 注册
engine = SkillEngine()

@engine.tool("query_database")
async def query_database(table: str, filters: dict = None) -> list:
    """查询数据库表"""
    return await db.select(table, filters=filters)

@engine.tool("save_to_database")
async def save_to_database(table: str, data: dict) -> dict:
    """保存数据到数据库"""
    return await db.insert(table, data)
```

## 技术选型指南

| 场景 | 推荐 | 理由 |
|------|------|------|
| 全栈应用 | Supabase | RLS、Auth、Storage 一体 |
| 高并发 | PlanetScale | 水平扩展、无锁 DDL |
| 边缘计算 | Turso | 全球复制、低延迟 |
| 开发测试 | SQLite | 零配置、本地运行 |

