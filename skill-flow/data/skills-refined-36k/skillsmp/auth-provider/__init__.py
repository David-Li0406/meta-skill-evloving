"""Auth Provider Skill - 认证集成.

支持 Supabase Auth、Clerk、Firebase Auth 等主流认证服务。
"""

from agentflow.skills.builtin.auth_provider.provider import (
    AuthProvider,
    AuthConfig,
    SupabaseAuthConfig,
    ClerkConfig,
    User,
    Session,
)
from agentflow.skills.builtin.auth_provider.exceptions import (
    AuthError,
    InvalidCredentialsError,
    UserNotFoundError,
    TokenExpiredError,
    EmailNotConfirmedError,
    MFARequiredError,
)

__all__ = [
    "AuthProvider",
    "AuthConfig",
    "SupabaseAuthConfig",
    "ClerkConfig",
    "User",
    "Session",
    "AuthError",
    "InvalidCredentialsError",
    "UserNotFoundError",
    "TokenExpiredError",
    "EmailNotConfirmedError",
    "MFARequiredError",
]

