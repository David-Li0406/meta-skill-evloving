"""Auth Provider - 认证提供商统一接口.

支持 Supabase Auth、Clerk、Firebase Auth 等主流认证服务。
"""

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from agentflow.skills.builtin.auth_provider.exceptions import (
    AuthError,
    EmailNotConfirmedError,
    InvalidCredentialsError,
    MFARequiredError,
    TokenExpiredError,
    UserNotFoundError,
)

logger = logging.getLogger(__name__)


# ============================================================================
# 配置模型
# ============================================================================


class AuthConfig(BaseModel):
    """认证配置基类."""

    provider: str = Field(..., description="认证提供商")


class SupabaseAuthConfig(AuthConfig):
    """Supabase Auth 配置."""

    provider: str = Field(default="supabase")
    url: str = Field(..., description="Supabase URL")
    anon_key: str = Field(..., description="匿名密钥")
    jwt_secret: str | None = Field(default=None, description="JWT 密钥（用于验证）")


class ClerkConfig(AuthConfig):
    """Clerk 配置."""

    provider: str = Field(default="clerk")
    secret_key: str = Field(..., description="后端密钥")
    publishable_key: str | None = Field(default=None, description="前端密钥")


# ============================================================================
# 数据模型
# ============================================================================


class User(BaseModel):
    """用户模型."""

    id: str = Field(..., description="用户 ID")
    email: str | None = Field(default=None, description="邮箱")
    phone: str | None = Field(default=None, description="手机号")
    email_confirmed: bool = Field(default=False, description="邮箱已确认")
    phone_confirmed: bool = Field(default=False, description="手机已确认")
    created_at: datetime | None = Field(default=None, description="创建时间")
    updated_at: datetime | None = Field(default=None, description="更新时间")
    last_sign_in: datetime | None = Field(default=None, description="最后登录时间")
    metadata: dict[str, Any] = Field(default_factory=dict, description="用户元数据")
    app_metadata: dict[str, Any] = Field(default_factory=dict, description="应用元数据")


class Session(BaseModel):
    """会话模型."""

    access_token: str = Field(..., description="访问令牌")
    refresh_token: str | None = Field(default=None, description="刷新令牌")
    expires_at: datetime | None = Field(default=None, description="过期时间")
    expires_in: int | None = Field(default=None, description="过期秒数")
    token_type: str = Field(default="bearer", description="令牌类型")
    user: User | None = Field(default=None, description="用户信息")
    mfa_required: bool = Field(default=False, description="是否需要 MFA")
    mfa_factors: list[dict] = Field(default_factory=list, description="MFA 因素")


class OAuthResponse(BaseModel):
    """OAuth 响应."""

    url: str = Field(..., description="授权 URL")
    provider: str = Field(..., description="提供商")


class MFAEnrollment(BaseModel):
    """MFA 注册信息."""

    id: str = Field(..., description="因素 ID")
    type: str = Field(..., description="因素类型")
    qr_code: str | None = Field(default=None, description="二维码 URI")
    secret: str | None = Field(default=None, description="密钥")


# ============================================================================
# 认证提供商抽象基类
# ============================================================================


class AuthProviderBase(ABC):
    """认证提供商抽象基类."""

    @abstractmethod
    async def sign_up(
        self,
        email: str,
        password: str,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> User:
        """用户注册."""
        ...

    @abstractmethod
    async def sign_in(
        self,
        email: str,
        password: str,
    ) -> Session:
        """邮箱密码登录."""
        ...

    @abstractmethod
    async def sign_in_with_oauth(
        self,
        provider: str,
        redirect_to: str,
        scopes: list[str] | None = None,
    ) -> OAuthResponse:
        """OAuth 登录."""
        ...

    @abstractmethod
    async def sign_out(self, scope: str = "local") -> None:
        """登出."""
        ...

    @abstractmethod
    async def get_session(self) -> Session | None:
        """获取当前会话."""
        ...

    @abstractmethod
    async def refresh_session(self, refresh_token: str) -> Session:
        """刷新会话."""
        ...

    @abstractmethod
    async def verify_jwt(self, token: str) -> dict[str, Any]:
        """验证 JWT."""
        ...

    @abstractmethod
    async def get_user(self, user_id: str) -> User:
        """获取用户信息."""
        ...


# ============================================================================
# Supabase Auth 提供商
# ============================================================================


class SupabaseAuthProvider(AuthProviderBase):
    """Supabase Auth 提供商."""

    def __init__(self, config: SupabaseAuthConfig) -> None:
        """初始化 Supabase Auth 提供商."""
        self._config = config
        self._client: Any = None
        self._current_session: Session | None = None

        self._initialize()

    def _initialize(self) -> None:
        """初始化客户端."""
        try:
            from supabase import create_client
        except ImportError:
            raise AuthError("supabase 库未安装，请运行: pip install supabase")

        self._client = create_client(self._config.url, self._config.anon_key)
        logger.info("Supabase Auth 已初始化")

    async def sign_up(
        self,
        email: str,
        password: str,
        metadata: dict[str, Any] | None = None,
        email_confirm: bool = True,
        **kwargs: Any,
    ) -> User:
        """用户注册."""
        try:
            response = self._client.auth.sign_up(
                {
                    "email": email,
                    "password": password,
                    "options": {
                        "data": metadata or {},
                        "email_redirect_to": kwargs.get("redirect_to"),
                    },
                }
            )

            if response.user:
                return self._parse_user(response.user)
            raise AuthError("注册失败")

        except Exception as e:
            error_msg = str(e)
            if "User already registered" in error_msg:
                raise AuthError("用户已存在", code="user_exists")
            raise AuthError(f"注册失败: {e}")

    async def sign_in(
        self,
        email: str,
        password: str,
    ) -> Session:
        """邮箱密码登录."""
        try:
            response = self._client.auth.sign_in_with_password(
                {"email": email, "password": password}
            )

            if response.session:
                session = self._parse_session(response.session, response.user)
                self._current_session = session
                return session

            raise InvalidCredentialsError("邮箱或密码错误")

        except Exception as e:
            error_msg = str(e).lower()
            if "invalid" in error_msg or "credentials" in error_msg:
                raise InvalidCredentialsError("邮箱或密码错误")
            if "email not confirmed" in error_msg:
                raise EmailNotConfirmedError("请先确认邮箱")
            raise AuthError(f"登录失败: {e}")

    async def sign_in_with_magic_link(
        self,
        email: str,
        redirect_to: str | None = None,
    ) -> None:
        """Magic Link 登录."""
        try:
            self._client.auth.sign_in_with_otp(
                {
                    "email": email,
                    "options": {"email_redirect_to": redirect_to},
                }
            )
            logger.info(f"Magic Link 已发送到: {email}")
        except Exception as e:
            raise AuthError(f"发送 Magic Link 失败: {e}")

    async def sign_in_with_otp(
        self,
        email: str | None = None,
        phone: str | None = None,
    ) -> None:
        """OTP 登录."""
        try:
            if email:
                self._client.auth.sign_in_with_otp({"email": email})
            elif phone:
                self._client.auth.sign_in_with_otp({"phone": phone})
            else:
                raise AuthError("需要提供邮箱或手机号")
        except Exception as e:
            raise AuthError(f"发送 OTP 失败: {e}")

    async def verify_otp(
        self,
        token: str,
        type: str = "email",
        email: str | None = None,
        phone: str | None = None,
    ) -> Session:
        """验证 OTP."""
        try:
            response = self._client.auth.verify_otp(
                {
                    "token": token,
                    "type": type,
                    "email": email,
                    "phone": phone,
                }
            )

            if response.session:
                session = self._parse_session(response.session, response.user)
                self._current_session = session
                return session

            raise AuthError("OTP 验证失败")
        except Exception as e:
            raise AuthError(f"OTP 验证失败: {e}")

    async def sign_in_with_oauth(
        self,
        provider: str,
        redirect_to: str,
        scopes: list[str] | None = None,
    ) -> OAuthResponse:
        """OAuth 登录."""
        try:
            response = self._client.auth.sign_in_with_oauth(
                {
                    "provider": provider,
                    "options": {
                        "redirect_to": redirect_to,
                        "scopes": " ".join(scopes) if scopes else None,
                    },
                }
            )

            return OAuthResponse(url=response.url, provider=provider)
        except Exception as e:
            raise AuthError(f"OAuth 登录失败: {e}")

    async def handle_oauth_callback(
        self,
        code: str,
        state: str | None = None,
    ) -> Session:
        """处理 OAuth 回调."""
        try:
            response = self._client.auth.exchange_code_for_session({"auth_code": code})

            if response.session:
                session = self._parse_session(response.session, response.user)
                self._current_session = session
                return session

            raise AuthError("OAuth 回调处理失败")
        except Exception as e:
            raise AuthError(f"OAuth 回调处理失败: {e}")

    async def sign_out(self, scope: str = "local") -> None:
        """登出."""
        try:
            if scope == "global":
                self._client.auth.sign_out({"scope": "global"})
            else:
                self._client.auth.sign_out()

            self._current_session = None
            logger.info("已登出")
        except Exception as e:
            raise AuthError(f"登出失败: {e}")

    async def get_session(self) -> Session | None:
        """获取当前会话."""
        try:
            response = self._client.auth.get_session()
            if response:
                return self._parse_session(response, None)
            return self._current_session
        except Exception:
            return self._current_session

    async def refresh_session(self, refresh_token: str) -> Session:
        """刷新会话."""
        try:
            response = self._client.auth.refresh_session(refresh_token)

            if response.session:
                session = self._parse_session(response.session, response.user)
                self._current_session = session
                return session

            raise TokenExpiredError("刷新令牌已过期")
        except Exception as e:
            raise TokenExpiredError(f"刷新会话失败: {e}")

    async def verify_jwt(self, token: str) -> dict[str, Any]:
        """验证 JWT."""
        try:
            import jwt
        except ImportError:
            raise AuthError("pyjwt 库未安装，请运行: pip install pyjwt")

        try:
            # 如果没有 JWT 密钥，使用 Supabase 的验证
            if not self._config.jwt_secret:
                # 通过 API 验证
                response = self._client.auth.get_user(token)
                if response.user:
                    return {
                        "sub": response.user.id,
                        "email": response.user.email,
                        "role": response.user.role,
                    }
                raise TokenExpiredError("无效的令牌")

            # 本地验证
            payload = jwt.decode(
                token,
                self._config.jwt_secret,
                algorithms=["HS256"],
                audience="authenticated",
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise TokenExpiredError("令牌已过期")
        except jwt.InvalidTokenError as e:
            raise AuthError(f"无效的令牌: {e}")

    async def get_user(self, user_id: str) -> User:
        """获取用户信息."""
        try:
            # 需要管理员权限或使用 service_role_key
            response = self._client.auth.admin.get_user_by_id(user_id)
            if response.user:
                return self._parse_user(response.user)
            raise UserNotFoundError(f"用户不存在: {user_id}")
        except Exception as e:
            if "not found" in str(e).lower():
                raise UserNotFoundError(f"用户不存在: {user_id}")
            raise AuthError(f"获取用户失败: {e}")

    async def get_current_user(self) -> User | None:
        """获取当前用户."""
        try:
            response = self._client.auth.get_user()
            if response.user:
                return self._parse_user(response.user)
            return None
        except Exception:
            return None

    async def update_user(
        self,
        user_id: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> User:
        """更新用户信息."""
        try:
            response = self._client.auth.update_user({"data": data or {}})
            if response.user:
                return self._parse_user(response.user)
            raise AuthError("更新用户失败")
        except Exception as e:
            raise AuthError(f"更新用户失败: {e}")

    async def update_password(
        self,
        new_password: str,
        current_password: str | None = None,
    ) -> None:
        """更新密码."""
        try:
            self._client.auth.update_user({"password": new_password})
            logger.info("密码已更新")
        except Exception as e:
            raise AuthError(f"更新密码失败: {e}")

    async def reset_password_for_email(
        self,
        email: str,
        redirect_to: str | None = None,
    ) -> None:
        """发送密码重置邮件."""
        try:
            self._client.auth.reset_password_email(
                email,
                {"redirect_to": redirect_to} if redirect_to else {},
            )
            logger.info(f"密码重置邮件已发送到: {email}")
        except Exception as e:
            raise AuthError(f"发送重置邮件失败: {e}")

    # MFA 方法
    async def enroll_mfa(
        self,
        factor_type: str = "totp",
        friendly_name: str | None = None,
    ) -> MFAEnrollment:
        """注册 MFA."""
        try:
            response = self._client.auth.mfa.enroll(
                {
                    "factor_type": factor_type,
                    "friendly_name": friendly_name,
                }
            )

            return MFAEnrollment(
                id=response.id,
                type=response.type,
                qr_code=response.totp.qr_code if hasattr(response, "totp") else None,
                secret=response.totp.secret if hasattr(response, "totp") else None,
            )
        except Exception as e:
            raise AuthError(f"注册 MFA 失败: {e}")

    async def verify_mfa(
        self,
        factor_id: str,
        code: str,
    ) -> None:
        """验证并激活 MFA."""
        try:
            self._client.auth.mfa.verify(
                {
                    "factor_id": factor_id,
                    "code": code,
                }
            )
            logger.info("MFA 已激活")
        except Exception as e:
            raise AuthError(f"MFA 验证失败: {e}")

    def _parse_user(self, user: Any) -> User:
        """解析用户数据."""
        return User(
            id=user.id,
            email=user.email,
            phone=getattr(user, "phone", None),
            email_confirmed=getattr(user, "email_confirmed_at", None) is not None,
            phone_confirmed=getattr(user, "phone_confirmed_at", None) is not None,
            created_at=user.created_at if hasattr(user, "created_at") else None,
            updated_at=user.updated_at if hasattr(user, "updated_at") else None,
            last_sign_in=getattr(user, "last_sign_in_at", None),
            metadata=user.user_metadata if hasattr(user, "user_metadata") else {},
            app_metadata=user.app_metadata if hasattr(user, "app_metadata") else {},
        )

    def _parse_session(self, session: Any, user: Any) -> Session:
        """解析会话数据."""
        return Session(
            access_token=session.access_token,
            refresh_token=session.refresh_token,
            expires_at=datetime.fromtimestamp(session.expires_at)
            if hasattr(session, "expires_at") and session.expires_at
            else None,
            expires_in=session.expires_in if hasattr(session, "expires_in") else None,
            user=self._parse_user(user) if user else None,
        )


# ============================================================================
# 统一认证提供商
# ============================================================================


class AuthProvider:
    """统一认证提供商.

    支持 Supabase Auth、Clerk 等主流认证服务。

    使用示例:
        ```python
        config = SupabaseAuthConfig(url="...", anon_key="...")
        auth = AuthProvider(provider="supabase", config=config)

        # 注册
        user = await auth.sign_up(email="...", password="...")

        # 登录
        session = await auth.sign_in(email="...", password="...")
        ```
    """

    def __init__(
        self,
        provider: str = "supabase",
        config: AuthConfig | None = None,
    ) -> None:
        """初始化认证提供商.

        Args:
            provider: 提供商名称（supabase/clerk）
            config: 提供商配置
        """
        self._provider_name = provider
        self._config = config
        self._provider: AuthProviderBase | None = None

        self._initialize_provider()

    def _initialize_provider(self) -> None:
        """初始化提供商."""
        if self._provider_name == "supabase":
            if not isinstance(self._config, SupabaseAuthConfig):
                raise AuthError("Supabase 需要 SupabaseAuthConfig 配置")
            self._provider = SupabaseAuthProvider(self._config)
        else:
            raise AuthError(f"不支持的认证提供商: {self._provider_name}")

        logger.info(f"认证提供商已初始化: {self._provider_name}")

    # 代理所有方法到具体提供商
    async def sign_up(
        self,
        email: str,
        password: str,
        metadata: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> User:
        """用户注册."""
        return await self._provider.sign_up(email, password, metadata, **kwargs)

    async def sign_in(
        self,
        email: str,
        password: str,
    ) -> Session:
        """邮箱密码登录."""
        return await self._provider.sign_in(email, password)

    async def sign_in_with_oauth(
        self,
        provider: str,
        redirect_to: str,
        scopes: list[str] | None = None,
    ) -> OAuthResponse:
        """OAuth 登录."""
        return await self._provider.sign_in_with_oauth(provider, redirect_to, scopes)

    async def sign_out(self, scope: str = "local") -> None:
        """登出."""
        await self._provider.sign_out(scope)

    async def get_session(self) -> Session | None:
        """获取当前会话."""
        return await self._provider.get_session()

    async def refresh_session(self, refresh_token: str) -> Session:
        """刷新会话."""
        return await self._provider.refresh_session(refresh_token)

    async def verify_jwt(self, token: str) -> dict[str, Any]:
        """验证 JWT."""
        return await self._provider.verify_jwt(token)

    async def get_user(self, user_id: str) -> User:
        """获取用户信息."""
        return await self._provider.get_user(user_id)

    # Supabase 特有方法
    async def sign_in_with_magic_link(
        self,
        email: str,
        redirect_to: str | None = None,
    ) -> None:
        """Magic Link 登录（仅 Supabase）."""
        if isinstance(self._provider, SupabaseAuthProvider):
            await self._provider.sign_in_with_magic_link(email, redirect_to)
        else:
            raise AuthError(f"{self._provider_name} 不支持 Magic Link 登录")

    async def sign_in_with_otp(
        self,
        email: str | None = None,
        phone: str | None = None,
    ) -> None:
        """OTP 登录（仅 Supabase）."""
        if isinstance(self._provider, SupabaseAuthProvider):
            await self._provider.sign_in_with_otp(email, phone)
        else:
            raise AuthError(f"{self._provider_name} 不支持 OTP 登录")

    async def verify_otp(
        self,
        token: str,
        type: str = "email",
        email: str | None = None,
        phone: str | None = None,
    ) -> Session:
        """验证 OTP（仅 Supabase）."""
        if isinstance(self._provider, SupabaseAuthProvider):
            return await self._provider.verify_otp(token, type, email, phone)
        raise AuthError(f"{self._provider_name} 不支持 OTP 验证")

    async def handle_oauth_callback(
        self,
        code: str,
        state: str | None = None,
    ) -> Session:
        """处理 OAuth 回调（仅 Supabase）."""
        if isinstance(self._provider, SupabaseAuthProvider):
            return await self._provider.handle_oauth_callback(code, state)
        raise AuthError(f"{self._provider_name} 不支持 OAuth 回调处理")

    async def get_current_user(self) -> User | None:
        """获取当前用户."""
        if isinstance(self._provider, SupabaseAuthProvider):
            return await self._provider.get_current_user()
        return None

    async def update_user(
        self,
        user_id: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> User:
        """更新用户信息."""
        if isinstance(self._provider, SupabaseAuthProvider):
            return await self._provider.update_user(user_id, data)
        raise AuthError(f"{self._provider_name} 不支持更新用户")

    async def update_password(
        self,
        new_password: str,
        current_password: str | None = None,
    ) -> None:
        """更新密码."""
        if isinstance(self._provider, SupabaseAuthProvider):
            await self._provider.update_password(new_password, current_password)
        else:
            raise AuthError(f"{self._provider_name} 不支持更新密码")

    async def reset_password_for_email(
        self,
        email: str,
        redirect_to: str | None = None,
    ) -> None:
        """发送密码重置邮件."""
        if isinstance(self._provider, SupabaseAuthProvider):
            await self._provider.reset_password_for_email(email, redirect_to)
        else:
            raise AuthError(f"{self._provider_name} 不支持密码重置")

    async def enroll_mfa(
        self,
        factor_type: str = "totp",
        friendly_name: str | None = None,
    ) -> MFAEnrollment:
        """注册 MFA."""
        if isinstance(self._provider, SupabaseAuthProvider):
            return await self._provider.enroll_mfa(factor_type, friendly_name)
        raise AuthError(f"{self._provider_name} 不支持 MFA")

    async def verify_mfa(
        self,
        factor_id: str,
        code: str,
    ) -> None:
        """验证并激活 MFA."""
        if isinstance(self._provider, SupabaseAuthProvider):
            await self._provider.verify_mfa(factor_id, code)
        else:
            raise AuthError(f"{self._provider_name} 不支持 MFA")

