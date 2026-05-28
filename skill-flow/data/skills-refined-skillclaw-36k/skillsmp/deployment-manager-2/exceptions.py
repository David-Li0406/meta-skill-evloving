"""Deployment Manager 异常定义."""


class DeploymentError(Exception):
    """部署基础异常."""

    def __init__(self, message: str, code: str | None = None) -> None:
        """初始化异常."""
        super().__init__(message)
        self.message = message
        self.code = code


class BuildError(DeploymentError):
    """构建错误."""

    pass


class ConfigError(DeploymentError):
    """配置错误."""

    pass


class DomainError(DeploymentError):
    """域名错误."""

    pass


class RollbackError(DeploymentError):
    """回滚错误."""

    pass


class ProviderError(DeploymentError):
    """提供商 API 错误."""

    pass


class TimeoutError(DeploymentError):
    """超时错误."""

    pass

