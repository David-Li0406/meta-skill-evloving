"""Database Manager 异常定义."""


class DatabaseError(Exception):
    """数据库基础异常."""

    pass


class ConnectionError(DatabaseError):
    """连接错误."""

    pass


class QueryError(DatabaseError):
    """查询错误."""

    pass


class RLSError(DatabaseError):
    """RLS 策略错误."""

    pass


class MigrationError(DatabaseError):
    """迁移错误."""

    pass


class TransactionError(DatabaseError):
    """事务错误."""

    pass


class SchemaError(DatabaseError):
    """Schema 错误."""

    pass

