"""Auth Provider 异常定义."""


class AuthError(Exception):
    """认证基础异常."""

    def __init__(self, message: str, code: str | None = None) -> None:
        """初始化异常."""
        super().__init__(message)
        self.message = message
        self.code = code


class InvalidCredentialsError(AuthError):
    """凭证无效错误."""

    pass


class UserNotFoundError(AuthError):
    """用户不存在错误."""

    pass


class TokenExpiredError(AuthError):
    """令牌过期错误."""

    pass


class EmailNotConfirmedError(AuthError):
    """邮箱未确认错误."""

    pass


class MFARequiredError(AuthError):
    """需要 MFA 验证."""

    def __init__(
        self,
        message: str,
        mfa_factors: list[dict] | None = None,
    ) -> None:
        """初始化 MFA 异常."""
        super().__init__(message, code="mfa_required")
        self.mfa_factors = mfa_factors or []


class UserExistsError(AuthError):
    """用户已存在错误."""

    pass


class WeakPasswordError(AuthError):
    """弱密码错误."""

    pass


class RateLimitError(AuthError):
    """请求频率限制错误."""

    pass

