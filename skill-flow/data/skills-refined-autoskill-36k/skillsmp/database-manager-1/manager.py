"""Database Manager - 数据库统一管理器.

提供 Supabase、Turso、PostgreSQL、PlanetScale 等数据库的统一接口。
"""

import logging
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Callable, TypeVar

from pydantic import BaseModel, Field

from agentflow.skills.builtin.database_manager.exceptions import (
    ConnectionError,
    MigrationError,
    QueryError,
    RLSError,
    TransactionError,
)

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


# ============================================================================
# 配置模型
# ============================================================================


class DatabaseConfig(BaseModel):
    """数据库基础配置."""

    provider: str = Field(..., description="数据库提供商")


class SupabaseConfig(DatabaseConfig):
    """Supabase 配置."""

    provider: str = Field(default="supabase")
    url: str = Field(..., description="Supabase URL")
    anon_key: str = Field(..., description="匿名密钥")
    service_role_key: str | None = Field(default=None, description="服务角色密钥（绕过RLS）")


class TursoConfig(DatabaseConfig):
    """Turso (libSQL) 配置."""

    provider: str = Field(default="turso")
    url: str = Field(..., description="Turso URL (libsql://...)")
    auth_token: str = Field(..., description="认证令牌")


class PostgresConfig(DatabaseConfig):
    """PostgreSQL 配置."""

    provider: str = Field(default="postgres")
    host: str = Field(default="localhost", description="主机")
    port: int = Field(default=5432, description="端口")
    database: str = Field(..., description="数据库名")
    user: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")
    ssl: bool = Field(default=False, description="启用 SSL")


class PlanetScaleConfig(DatabaseConfig):
    """PlanetScale 配置."""

    provider: str = Field(default="planetscale")
    host: str = Field(..., description="主机")
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")
    database: str = Field(..., description="数据库名")


# ============================================================================
# 订阅接口
# ============================================================================


class Subscription:
    """实时订阅句柄."""

    def __init__(self, unsubscribe_fn: Callable) -> None:
        """初始化订阅."""
        self._unsubscribe = unsubscribe_fn

    async def unsubscribe(self) -> None:
        """取消订阅."""
        await self._unsubscribe()


# ============================================================================
# 数据库提供商抽象基类
# ============================================================================


class DatabaseProvider(ABC):
    """数据库提供商抽象基类."""

    @abstractmethod
    async def connect(self) -> None:
        """建立连接."""
        ...

    @abstractmethod
    async def disconnect(self) -> None:
        """断开连接."""
        ...

    @abstractmethod
    async def select(
        self,
        table: str,
        columns: list[str] | None = None,
        filters: dict[str, Any] | None = None,
        order_by: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[dict[str, Any]]:
        """查询数据."""
        ...

    @abstractmethod
    async def insert(
        self,
        table: str,
        data: dict[str, Any] | list[dict[str, Any]],
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """插入数据."""
        ...

    @abstractmethod
    async def update(
        self,
        table: str,
        data: dict[str, Any],
        filters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """更新数据."""
        ...

    @abstractmethod
    async def delete(
        self,
        table: str,
        filters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """删除数据."""
        ...

    @abstractmethod
    async def execute(
        self,
        query: str,
        params: list[Any] | None = None,
    ) -> list[dict[str, Any]]:
        """执行原生 SQL."""
        ...

    @abstractmethod
    async def health_check(self) -> bool:
        """健康检查."""
        ...


# ============================================================================
# Supabase 提供商
# ============================================================================


class SupabaseProvider(DatabaseProvider):
    """Supabase 数据库提供商."""

    def __init__(self, config: SupabaseConfig) -> None:
        """初始化 Supabase 提供商."""
        self._config = config
        self._client: Any = None

    async def connect(self) -> None:
        """建立 Supabase 连接."""
        try:
            from supabase import create_client
        except ImportError:
            raise ConnectionError("supabase 库未安装，请运行: pip install supabase")

        try:
            # 使用 service_role_key 绕过 RLS（如果提供）
            key = self._config.service_role_key or self._config.anon_key
            self._client = create_client(self._config.url, key)
            logger.info("Supabase 连接成功")
        except Exception as e:
            raise ConnectionError(f"Supabase 连接失败: {e}")

    async def disconnect(self) -> None:
        """断开 Supabase 连接."""
        self._client = None
        logger.info("Supabase 连接已断开")

    async def select(
        self,
        table: str,
        columns: list[str] | None = None,
        filters: dict[str, Any] | None = None,
        order_by: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[dict[str, Any]]:
        """查询 Supabase 表."""
        try:
            query = self._client.table(table).select(
                ",".join(columns) if columns else "*"
            )

            if filters:
                for key, value in filters.items():
                    query = query.eq(key, value)

            if order_by:
                desc = order_by.startswith("-")
                column = order_by.lstrip("-")
                query = query.order(column, desc=desc)

            if limit:
                query = query.limit(limit)

            if offset:
                query = query.offset(offset)

            response = query.execute()
            return response.data
        except Exception as e:
            raise QueryError(f"Supabase 查询失败: {e}")

    async def insert(
        self,
        table: str,
        data: dict[str, Any] | list[dict[str, Any]],
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """插入数据到 Supabase."""
        try:
            response = self._client.table(table).insert(data).execute()
            if isinstance(data, list):
                return response.data
            return response.data[0] if response.data else {}
        except Exception as e:
            if "RLS" in str(e) or "policy" in str(e).lower():
                raise RLSError(f"RLS 策略阻止操作: {e}")
            raise QueryError(f"Supabase 插入失败: {e}")

    async def update(
        self,
        table: str,
        data: dict[str, Any],
        filters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """更新 Supabase 数据."""
        try:
            query = self._client.table(table).update(data)
            for key, value in filters.items():
                query = query.eq(key, value)
            response = query.execute()
            return response.data
        except Exception as e:
            if "RLS" in str(e) or "policy" in str(e).lower():
                raise RLSError(f"RLS 策略阻止操作: {e}")
            raise QueryError(f"Supabase 更新失败: {e}")

    async def delete(
        self,
        table: str,
        filters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """删除 Supabase 数据."""
        try:
            query = self._client.table(table).delete()
            for key, value in filters.items():
                query = query.eq(key, value)
            response = query.execute()
            return response.data
        except Exception as e:
            if "RLS" in str(e) or "policy" in str(e).lower():
                raise RLSError(f"RLS 策略阻止操作: {e}")
            raise QueryError(f"Supabase 删除失败: {e}")

    async def execute(
        self,
        query: str,
        params: list[Any] | None = None,
    ) -> list[dict[str, Any]]:
        """执行原生 SQL（通过 RPC）."""
        try:
            response = self._client.rpc("exec_sql", {"query": query}).execute()
            return response.data or []
        except Exception as e:
            raise QueryError(f"Supabase SQL 执行失败: {e}")

    async def health_check(self) -> bool:
        """Supabase 健康检查."""
        try:
            self._client.table("_health").select("*").limit(1).execute()
            return True
        except Exception:
            return False

    async def subscribe(
        self,
        table: str,
        event: str,
        callback: Callable[[dict], None],
        filters: dict[str, str] | None = None,
    ) -> Subscription:
        """订阅 Supabase 实时变更."""
        channel = self._client.channel(f"{table}_changes")

        def handle_change(payload: dict) -> None:
            callback(payload)

        postgres_changes = {
            "event": event.upper(),
            "schema": "public",
            "table": table,
        }
        if filters:
            postgres_changes["filter"] = ",".join(
                f"{k}.{v}" for k, v in filters.items()
            )

        channel.on_postgres_changes(
            postgres_changes,
            callback=handle_change,
        )
        channel.subscribe()

        async def unsubscribe() -> None:
            await channel.unsubscribe()

        return Subscription(unsubscribe)


# ============================================================================
# Turso 提供商
# ============================================================================


class TursoProvider(DatabaseProvider):
    """Turso (libSQL) 数据库提供商."""

    def __init__(self, config: TursoConfig) -> None:
        """初始化 Turso 提供商."""
        self._config = config
        self._client: Any = None

    async def connect(self) -> None:
        """建立 Turso 连接."""
        try:
            import libsql_experimental as libsql
        except ImportError:
            raise ConnectionError(
                "libsql-experimental 库未安装，请运行: pip install libsql-experimental"
            )

        try:
            self._client = libsql.connect(
                self._config.url,
                auth_token=self._config.auth_token,
            )
            logger.info("Turso 连接成功")
        except Exception as e:
            raise ConnectionError(f"Turso 连接失败: {e}")

    async def disconnect(self) -> None:
        """断开 Turso 连接."""
        if self._client:
            self._client.close()
        self._client = None
        logger.info("Turso 连接已断开")

    async def select(
        self,
        table: str,
        columns: list[str] | None = None,
        filters: dict[str, Any] | None = None,
        order_by: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[dict[str, Any]]:
        """查询 Turso 表."""
        cols = ", ".join(columns) if columns else "*"
        query = f"SELECT {cols} FROM {table}"
        params: list[Any] = []

        if filters:
            conditions = []
            for key, value in filters.items():
                conditions.append(f"{key} = ?")
                params.append(value)
            query += " WHERE " + " AND ".join(conditions)

        if order_by:
            desc = " DESC" if order_by.startswith("-") else ""
            column = order_by.lstrip("-")
            query += f" ORDER BY {column}{desc}"

        if limit:
            query += f" LIMIT {limit}"

        if offset:
            query += f" OFFSET {offset}"

        return await self.execute(query, params)

    async def insert(
        self,
        table: str,
        data: dict[str, Any] | list[dict[str, Any]],
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """插入数据到 Turso."""
        records = [data] if isinstance(data, dict) else data
        results = []

        for record in records:
            columns = ", ".join(record.keys())
            placeholders = ", ".join(["?"] * len(record))
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING *"
            result = await self.execute(query, list(record.values()))
            if result:
                results.extend(result)

        return results[0] if isinstance(data, dict) and results else results

    async def update(
        self,
        table: str,
        data: dict[str, Any],
        filters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """更新 Turso 数据."""
        set_clause = ", ".join(f"{k} = ?" for k in data.keys())
        where_clause = " AND ".join(f"{k} = ?" for k in filters.keys())
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause} RETURNING *"
        params = list(data.values()) + list(filters.values())
        return await self.execute(query, params)

    async def delete(
        self,
        table: str,
        filters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """删除 Turso 数据."""
        where_clause = " AND ".join(f"{k} = ?" for k in filters.keys())
        query = f"DELETE FROM {table} WHERE {where_clause} RETURNING *"
        return await self.execute(query, list(filters.values()))

    async def execute(
        self,
        query: str,
        params: list[Any] | None = None,
    ) -> list[dict[str, Any]]:
        """执行原生 SQL."""
        try:
            cursor = self._client.execute(query, params or [])
            if cursor.description:
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
            return []
        except Exception as e:
            raise QueryError(f"Turso 查询失败: {e}")

    async def health_check(self) -> bool:
        """Turso 健康检查."""
        try:
            await self.execute("SELECT 1")
            return True
        except Exception:
            return False


# ============================================================================
# PostgreSQL 提供商
# ============================================================================


class PostgresProvider(DatabaseProvider):
    """PostgreSQL 数据库提供商."""

    def __init__(self, config: PostgresConfig, pool_size: int = 10) -> None:
        """初始化 PostgreSQL 提供商."""
        self._config = config
        self._pool_size = pool_size
        self._pool: Any = None

    async def connect(self) -> None:
        """建立 PostgreSQL 连接池."""
        try:
            import asyncpg
        except ImportError:
            raise ConnectionError("asyncpg 库未安装，请运行: pip install asyncpg")

        try:
            self._pool = await asyncpg.create_pool(
                host=self._config.host,
                port=self._config.port,
                database=self._config.database,
                user=self._config.user,
                password=self._config.password,
                ssl="require" if self._config.ssl else None,
                min_size=1,
                max_size=self._pool_size,
            )
            logger.info("PostgreSQL 连接池创建成功")
        except Exception as e:
            raise ConnectionError(f"PostgreSQL 连接失败: {e}")

    async def disconnect(self) -> None:
        """关闭 PostgreSQL 连接池."""
        if self._pool:
            await self._pool.close()
        self._pool = None
        logger.info("PostgreSQL 连接池已关闭")

    async def select(
        self,
        table: str,
        columns: list[str] | None = None,
        filters: dict[str, Any] | None = None,
        order_by: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[dict[str, Any]]:
        """查询 PostgreSQL 表."""
        cols = ", ".join(columns) if columns else "*"
        query = f"SELECT {cols} FROM {table}"
        params: list[Any] = []
        param_idx = 1

        if filters:
            conditions = []
            for key, value in filters.items():
                conditions.append(f"{key} = ${param_idx}")
                params.append(value)
                param_idx += 1
            query += " WHERE " + " AND ".join(conditions)

        if order_by:
            desc = " DESC" if order_by.startswith("-") else ""
            column = order_by.lstrip("-")
            query += f" ORDER BY {column}{desc}"

        if limit:
            query += f" LIMIT {limit}"

        if offset:
            query += f" OFFSET {offset}"

        return await self.execute(query, params)

    async def insert(
        self,
        table: str,
        data: dict[str, Any] | list[dict[str, Any]],
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """插入数据到 PostgreSQL."""
        records = [data] if isinstance(data, dict) else data
        results = []

        for record in records:
            columns = ", ".join(record.keys())
            placeholders = ", ".join(f"${i + 1}" for i in range(len(record)))
            query = (
                f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING *"
            )
            result = await self.execute(query, list(record.values()))
            if result:
                results.extend(result)

        return results[0] if isinstance(data, dict) and results else results

    async def update(
        self,
        table: str,
        data: dict[str, Any],
        filters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """更新 PostgreSQL 数据."""
        set_parts = []
        params = []
        idx = 1

        for key, value in data.items():
            set_parts.append(f"{key} = ${idx}")
            params.append(value)
            idx += 1

        where_parts = []
        for key, value in filters.items():
            where_parts.append(f"{key} = ${idx}")
            params.append(value)
            idx += 1

        query = f"UPDATE {table} SET {', '.join(set_parts)} WHERE {' AND '.join(where_parts)} RETURNING *"
        return await self.execute(query, params)

    async def delete(
        self,
        table: str,
        filters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """删除 PostgreSQL 数据."""
        where_parts = []
        params = []
        idx = 1

        for key, value in filters.items():
            where_parts.append(f"{key} = ${idx}")
            params.append(value)
            idx += 1

        query = f"DELETE FROM {table} WHERE {' AND '.join(where_parts)} RETURNING *"
        return await self.execute(query, params)

    async def execute(
        self,
        query: str,
        params: list[Any] | None = None,
    ) -> list[dict[str, Any]]:
        """执行原生 SQL."""
        try:
            async with self._pool.acquire() as conn:
                rows = await conn.fetch(query, *(params or []))
                return [dict(row) for row in rows]
        except Exception as e:
            raise QueryError(f"PostgreSQL 查询失败: {e}")

    async def health_check(self) -> bool:
        """PostgreSQL 健康检查."""
        try:
            await self.execute("SELECT 1")
            return True
        except Exception:
            return False

    def get_pool_stats(self) -> dict[str, int]:
        """获取连接池统计."""
        if not self._pool:
            return {"active": 0, "idle": 0, "total": 0}
        return {
            "active": self._pool.get_size() - self._pool.get_idle_size(),
            "idle": self._pool.get_idle_size(),
            "total": self._pool.get_size(),
        }


# ============================================================================
# 数据库管理器（统一入口）
# ============================================================================


class DatabaseManager:
    """数据库统一管理器.

    提供 Supabase、Turso、PostgreSQL、PlanetScale 等数据库的统一接口。

    使用示例:
        ```python
        # Supabase
        db = DatabaseManager(
            provider="supabase",
            config=SupabaseConfig(url="...", anon_key="...")
        )
        await db.connect()

        # CRUD
        users = await db.select("users", filters={"status": "active"})
        new_user = await db.insert("users", {"email": "test@example.com"})
        ```
    """

    def __init__(
        self,
        provider: str = "supabase",
        config: DatabaseConfig | None = None,
        pool_size: int = 10,
    ) -> None:
        """初始化数据库管理器.

        Args:
            provider: 数据库提供商（supabase/turso/postgres/planetscale）
            config: 数据库配置
            pool_size: 连接池大小（仅 PostgreSQL）
        """
        self._provider_name = provider
        self._config = config
        self._pool_size = pool_size
        self._provider: DatabaseProvider | None = None
        self._in_transaction = False

    async def connect(self) -> None:
        """建立数据库连接."""
        if self._provider_name == "supabase":
            if not isinstance(self._config, SupabaseConfig):
                raise ValueError("Supabase 需要 SupabaseConfig 配置")
            self._provider = SupabaseProvider(self._config)
        elif self._provider_name == "turso":
            if not isinstance(self._config, TursoConfig):
                raise ValueError("Turso 需要 TursoConfig 配置")
            self._provider = TursoProvider(self._config)
        elif self._provider_name == "postgres":
            if not isinstance(self._config, PostgresConfig):
                raise ValueError("PostgreSQL 需要 PostgresConfig 配置")
            self._provider = PostgresProvider(self._config, self._pool_size)
        else:
            raise ValueError(f"不支持的数据库提供商: {self._provider_name}")

        await self._provider.connect()

    async def disconnect(self) -> None:
        """断开数据库连接."""
        if self._provider:
            await self._provider.disconnect()
            self._provider = None

    async def __aenter__(self) -> "DatabaseManager":
        """异步上下文管理器入口."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """异步上下文管理器出口."""
        await self.disconnect()

    def _ensure_connected(self) -> None:
        """确保已连接."""
        if not self._provider:
            raise ConnectionError("数据库未连接，请先调用 connect()")

    async def select(
        self,
        table: str,
        columns: list[str] | None = None,
        filters: dict[str, Any] | None = None,
        order_by: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        model: type[T] | None = None,
    ) -> list[dict[str, Any]] | list[T]:
        """查询数据.

        Args:
            table: 表名
            columns: 要查询的列（None 表示所有列）
            filters: 过滤条件 {"column": "value"}
            order_by: 排序字段（"-column" 表示降序）
            limit: 限制返回行数
            offset: 跳过行数
            model: Pydantic 模型（可选，用于类型验证）

        Returns:
            查询结果列表
        """
        self._ensure_connected()
        results = await self._provider.select(
            table, columns, filters, order_by, limit, offset
        )
        if model:
            return [model(**row) for row in results]
        return results

    async def insert(
        self,
        table: str,
        data: dict[str, Any] | list[dict[str, Any]],
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """插入数据.

        Args:
            table: 表名
            data: 要插入的数据（单条或多条）

        Returns:
            插入后的数据（包含生成的 ID 等）
        """
        self._ensure_connected()
        return await self._provider.insert(table, data)

    async def update(
        self,
        table: str,
        data: dict[str, Any],
        filters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """更新数据.

        Args:
            table: 表名
            data: 要更新的数据
            filters: 过滤条件

        Returns:
            更新后的数据
        """
        self._ensure_connected()
        return await self._provider.update(table, data, filters)

    async def delete(
        self,
        table: str,
        filters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """删除数据.

        Args:
            table: 表名
            filters: 过滤条件

        Returns:
            被删除的数据
        """
        self._ensure_connected()
        return await self._provider.delete(table, filters)

    async def execute(
        self,
        query: str,
        params: list[Any] | None = None,
    ) -> list[dict[str, Any]]:
        """执行原生 SQL.

        Args:
            query: SQL 语句
            params: 参数列表

        Returns:
            查询结果
        """
        self._ensure_connected()
        return await self._provider.execute(query, params)

    async def health_check(self) -> bool:
        """健康检查.

        Returns:
            True 表示健康
        """
        self._ensure_connected()
        return await self._provider.health_check()

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator["TransactionContext"]:
        """事务上下文管理器.

        使用示例:
            ```python
            async with db.transaction() as tx:
                await tx.insert("users", {...})
                await tx.insert("profiles", {...})
            ```
        """
        self._ensure_connected()
        if self._provider_name not in ("postgres",):
            raise TransactionError(
                f"{self._provider_name} 不支持事务，请使用 PostgreSQL"
            )

        # 对于 PostgreSQL，使用真正的事务
        if isinstance(self._provider, PostgresProvider):
            async with self._provider._pool.acquire() as conn:
                async with conn.transaction():
                    yield TransactionContext(conn, self._provider_name)
        else:
            yield TransactionContext(None, self._provider_name)

    # Supabase 特有功能
    async def subscribe(
        self,
        table: str,
        event: str,
        callback: Callable[[dict], None],
        filters: dict[str, str] | None = None,
    ) -> Subscription:
        """订阅实时变更（仅 Supabase）.

        Args:
            table: 表名
            event: 事件类型（INSERT/UPDATE/DELETE/ALL）
            callback: 回调函数
            filters: 过滤条件

        Returns:
            订阅句柄
        """
        self._ensure_connected()
        if not isinstance(self._provider, SupabaseProvider):
            raise NotImplementedError("实时订阅仅支持 Supabase")
        return await self._provider.subscribe(table, event, callback, filters)

    # RLS 管理（仅 Supabase/PostgreSQL）
    async def enable_rls(self, table: str) -> None:
        """启用 RLS.

        Args:
            table: 表名
        """
        await self.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
        logger.info(f"已为表 {table} 启用 RLS")

    async def add_rls_policy(
        self,
        table: str,
        name: str,
        operation: str,
        using: str,
        with_check: str | None = None,
    ) -> None:
        """添加 RLS 策略.

        Args:
            table: 表名
            name: 策略名
            operation: 操作类型（SELECT/INSERT/UPDATE/DELETE/ALL）
            using: USING 表达式
            with_check: WITH CHECK 表达式（可选）
        """
        query = f"CREATE POLICY {name} ON {table} FOR {operation} USING ({using})"
        if with_check:
            query += f" WITH CHECK ({with_check})"
        await self.execute(query)
        logger.info(f"已为表 {table} 添加 RLS 策略: {name}")

    # Schema 管理
    async def apply_schema(self, schema: dict[str, Any]) -> None:
        """应用 Schema 定义.

        Args:
            schema: Schema 定义字典
        """
        for table_name, table_def in schema.items():
            # 构建 CREATE TABLE 语句
            columns = table_def.get("columns", [])
            col_defs = []
            primary_keys = []

            for col in columns:
                col_def = f"{col['name']} {col['type']}"
                if col.get("not_null"):
                    col_def += " NOT NULL"
                if col.get("unique"):
                    col_def += " UNIQUE"
                if col.get("default"):
                    col_def += f" DEFAULT {col['default']}"
                if col.get("primary"):
                    primary_keys.append(col["name"])
                col_defs.append(col_def)

            if primary_keys:
                col_defs.append(f"PRIMARY KEY ({', '.join(primary_keys)})")

            create_sql = (
                f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(col_defs)})"
            )
            await self.execute(create_sql)
            logger.info(f"已创建表: {table_name}")

            # RLS 配置
            rls_config = table_def.get("rls", {})
            if rls_config.get("enabled"):
                await self.enable_rls(table_name)
                for policy in rls_config.get("policies", []):
                    await self.add_rls_policy(
                        table=table_name,
                        name=policy["name"],
                        operation=policy["operation"],
                        using=policy["check"],
                        with_check=policy.get("with_check"),
                    )

    # 迁移管理
    async def create_migration(self, name: str, sql: str) -> dict[str, Any]:
        """创建迁移.

        Args:
            name: 迁移名
            sql: SQL 语句

        Returns:
            迁移信息
        """
        # 确保迁移表存在
        await self.execute("""
            CREATE TABLE IF NOT EXISTS _migrations (
                id SERIAL PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                sql TEXT NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                rolled_back_at TIMESTAMP
            )
        """)

        # 插入迁移记录
        result = await self.insert(
            "_migrations",
            {"name": name, "sql": sql},
        )
        logger.info(f"已创建迁移: {name}")
        return result

    async def run_migrations(self) -> list[str]:
        """执行所有待处理的迁移.

        Returns:
            已执行的迁移名列表
        """
        # 获取待执行的迁移
        pending = await self.select(
            "_migrations",
            filters={"rolled_back_at": None},
            order_by="id",
        )

        executed = []
        for migration in pending:
            try:
                await self.execute(migration["sql"])
                executed.append(migration["name"])
                logger.info(f"已执行迁移: {migration['name']}")
            except Exception as e:
                raise MigrationError(f"迁移 {migration['name']} 执行失败: {e}")

        return executed

    async def rollback_migration(self, name: str) -> None:
        """回滚指定迁移.

        Args:
            name: 迁移名
        """
        await self.update(
            "_migrations",
            {"rolled_back_at": "CURRENT_TIMESTAMP"},
            {"name": name},
        )
        logger.info(f"已标记迁移为回滚: {name}")

    # 连接池统计（仅 PostgreSQL）
    def get_pool_stats(self) -> dict[str, int]:
        """获取连接池统计（仅 PostgreSQL）."""
        if isinstance(self._provider, PostgresProvider):
            return self._provider.get_pool_stats()
        return {"active": 0, "idle": 0, "total": 0}


class TransactionContext:
    """事务上下文."""

    def __init__(self, conn: Any, provider: str) -> None:
        """初始化事务上下文."""
        self._conn = conn
        self._provider = provider

    async def execute(
        self,
        query: str,
        params: list[Any] | None = None,
    ) -> list[dict[str, Any]]:
        """在事务中执行 SQL."""
        if self._provider == "postgres" and self._conn:
            rows = await self._conn.fetch(query, *(params or []))
            return [dict(row) for row in rows]
        raise TransactionError("事务上下文不可用")

    async def insert(
        self,
        table: str,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        """在事务中插入数据."""
        columns = ", ".join(data.keys())
        placeholders = ", ".join(f"${i + 1}" for i in range(len(data)))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING *"
        result = await self.execute(query, list(data.values()))
        return result[0] if result else {}

