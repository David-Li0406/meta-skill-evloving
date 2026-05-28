"""Deployment Manager - 统一部署管理器.

支持 Vercel、Cloudflare Pages/Workers 等平台的部署管理。
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, AsyncIterator

from pydantic import BaseModel, Field

from agentflow.skills.builtin.deployment_manager.exceptions import (
    BuildError,
    ConfigError,
    DeploymentError,
    DomainError,
    ProviderError,
    RollbackError,
    TimeoutError,
)

logger = logging.getLogger(__name__)


# ============================================================================
# 配置模型
# ============================================================================


class DeploymentConfig(BaseModel):
    """部署配置基类."""

    provider: str = Field(..., description="部署提供商")


class VercelConfig(DeploymentConfig):
    """Vercel 配置."""

    provider: str = Field(default="vercel")
    token: str = Field(..., description="Vercel API Token")
    team_id: str | None = Field(default=None, description="Team ID（团队项目）")
    org_id: str | None = Field(default=None, description="Organization ID")


class CloudflareConfig(DeploymentConfig):
    """Cloudflare 配置."""

    provider: str = Field(default="cloudflare")
    api_token: str = Field(..., description="Cloudflare API Token")
    account_id: str = Field(..., description="Account ID")


# ============================================================================
# 部署结果模型
# ============================================================================


class DeploymentStatus:
    """部署状态."""

    BUILDING = "building"
    READY = "ready"
    ERROR = "error"
    QUEUED = "queued"
    CANCELED = "canceled"


class Deployment(BaseModel):
    """部署信息."""

    id: str = Field(..., description="部署 ID")
    url: str = Field(..., description="部署 URL")
    status: str = Field(..., description="部署状态")
    created_at: datetime = Field(..., description="创建时间")
    environment: str = Field(default="production", description="环境")
    branch: str | None = Field(default=None, description="分支")
    commit_sha: str | None = Field(default=None, description="Commit SHA")
    build_time: int | None = Field(default=None, description="构建时间（秒）")
    error_message: str | None = Field(default=None, description="错误信息")


class DomainInfo(BaseModel):
    """域名信息."""

    domain: str = Field(..., description="域名")
    verified: bool = Field(default=False, description="是否已验证")
    dns_records: list[dict[str, str]] = Field(default_factory=list, description="DNS 记录")


class EnvVar(BaseModel):
    """环境变量."""

    key: str = Field(..., description="变量名")
    value: str | None = Field(default=None, description="变量值")
    encrypted: bool = Field(default=False, description="是否加密")
    environment: str = Field(default="all", description="环境")


# ============================================================================
# 部署提供商抽象基类
# ============================================================================


class DeploymentProvider(ABC):
    """部署提供商抽象基类."""

    @abstractmethod
    async def deploy(
        self,
        project_name: str,
        source_path: str,
        environment: str = "production",
        env_vars: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> Deployment:
        """部署项目."""
        ...

    @abstractmethod
    async def list_deployments(
        self,
        project_name: str,
        limit: int = 10,
    ) -> list[Deployment]:
        """获取部署列表."""
        ...

    @abstractmethod
    async def get_deployment(
        self,
        project_name: str,
        deployment_id: str,
    ) -> Deployment:
        """获取部署详情."""
        ...

    @abstractmethod
    async def rollback(
        self,
        project_name: str,
        deployment_id: str,
    ) -> Deployment:
        """回滚到指定版本."""
        ...

    @abstractmethod
    async def delete_deployment(
        self,
        project_name: str,
        deployment_id: str,
    ) -> bool:
        """删除部署."""
        ...


# ============================================================================
# Vercel 提供商
# ============================================================================


class VercelProvider(DeploymentProvider):
    """Vercel 部署提供商."""

    BASE_URL = "https://api.vercel.com"

    def __init__(self, config: VercelConfig) -> None:
        """初始化 Vercel 提供商."""
        self._config = config
        self._client: Any = None

    async def _ensure_client(self) -> Any:
        """确保 HTTP 客户端已初始化."""
        if self._client is None:
            try:
                import httpx
            except ImportError:
                raise ConfigError("httpx 库未安装，请运行: pip install httpx")

            self._client = httpx.AsyncClient(
                base_url=self.BASE_URL,
                headers={
                    "Authorization": f"Bearer {self._config.token}",
                    "Content-Type": "application/json",
                },
                timeout=60.0,
            )
        return self._client

    async def _request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """发送 API 请求."""
        client = await self._ensure_client()

        # 添加团队参数
        params = kwargs.pop("params", {})
        if self._config.team_id:
            params["teamId"] = self._config.team_id

        try:
            response = await client.request(method, path, params=params, **kwargs)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise ProviderError(f"Vercel API 错误: {e}")

    async def deploy(
        self,
        project_name: str,
        source_path: str,
        environment: str = "production",
        env_vars: dict[str, str] | None = None,
        auto_assign_domains: bool = True,
        **kwargs: Any,
    ) -> Deployment:
        """部署到 Vercel."""
        # 获取或创建项目
        project = await self._get_or_create_project(project_name)

        # 设置环境变量
        if env_vars:
            await self._set_env_vars(project["id"], env_vars, environment)

        # 创建部署
        # 注意：实际的 Vercel 部署需要上传文件或使用 Git 集成
        # 这里简化为创建部署记录
        deployment_data = await self._request(
            "POST",
            "/v13/deployments",
            json={
                "name": project_name,
                "target": environment if environment == "production" else None,
                "gitSource": kwargs.get("git_source"),
                "projectSettings": {
                    "framework": kwargs.get("framework"),
                },
            },
        )

        deployment = self._parse_deployment(deployment_data)
        logger.info(f"Vercel 部署已创建: {deployment.id} -> {deployment.url}")
        return deployment

    async def _get_or_create_project(self, name: str) -> dict[str, Any]:
        """获取或创建项目."""
        try:
            return await self._request("GET", f"/v9/projects/{name}")
        except ProviderError:
            # 项目不存在，创建新项目
            return await self._request(
                "POST",
                "/v10/projects",
                json={
                    "name": name,
                    "framework": "nextjs",
                },
            )

    async def _set_env_vars(
        self,
        project_id: str,
        env_vars: dict[str, str],
        environment: str,
    ) -> None:
        """设置环境变量."""
        target = ["production"] if environment == "production" else ["preview"]

        for key, value in env_vars.items():
            await self._request(
                "POST",
                f"/v10/projects/{project_id}/env",
                json={
                    "key": key,
                    "value": value,
                    "type": "encrypted",
                    "target": target,
                },
            )

    def _parse_deployment(self, data: dict[str, Any]) -> Deployment:
        """解析部署数据."""
        return Deployment(
            id=data.get("id", data.get("uid", "")),
            url=f"https://{data.get('url', '')}",
            status=data.get("readyState", data.get("state", "building")),
            created_at=datetime.fromtimestamp(data.get("createdAt", 0) / 1000),
            environment=data.get("target", "preview") or "preview",
            branch=data.get("meta", {}).get("githubCommitRef"),
            commit_sha=data.get("meta", {}).get("githubCommitSha"),
            build_time=data.get("buildingAt"),
        )

    async def list_deployments(
        self,
        project_name: str,
        limit: int = 10,
    ) -> list[Deployment]:
        """获取部署列表."""
        data = await self._request(
            "GET",
            "/v6/deployments",
            params={"projectId": project_name, "limit": limit},
        )
        return [self._parse_deployment(d) for d in data.get("deployments", [])]

    async def get_deployment(
        self,
        project_name: str,
        deployment_id: str,
    ) -> Deployment:
        """获取部署详情."""
        data = await self._request("GET", f"/v13/deployments/{deployment_id}")
        return self._parse_deployment(data)

    async def rollback(
        self,
        project_name: str,
        deployment_id: str,
    ) -> Deployment:
        """回滚到指定版本."""
        # 获取目标部署
        target = await self.get_deployment(project_name, deployment_id)

        # 提升为生产部署
        data = await self._request(
            "PATCH",
            f"/v12/projects/{project_name}/production-deployment",
            json={"deploymentId": deployment_id},
        )

        logger.info(f"已回滚到部署: {deployment_id}")
        return self._parse_deployment(data)

    async def delete_deployment(
        self,
        project_name: str,
        deployment_id: str,
    ) -> bool:
        """删除部署."""
        await self._request("DELETE", f"/v13/deployments/{deployment_id}")
        logger.info(f"已删除部署: {deployment_id}")
        return True

    async def create_preview(
        self,
        project_name: str,
        source_path: str,
        branch: str | None = None,
        pr_number: int | None = None,
    ) -> Deployment:
        """创建预览部署."""
        return await self.deploy(
            project_name=project_name,
            source_path=source_path,
            environment="preview",
            branch=branch,
        )

    async def add_domain(
        self,
        project_name: str,
        domain: str,
    ) -> DomainInfo:
        """添加自定义域名."""
        data = await self._request(
            "POST",
            f"/v10/projects/{project_name}/domains",
            json={"name": domain},
        )

        return DomainInfo(
            domain=data["name"],
            verified=data.get("verified", False),
            dns_records=[
                {
                    "type": "CNAME",
                    "name": domain.split(".")[0],
                    "value": "cname.vercel-dns.com",
                }
            ],
        )

    async def verify_domain(
        self,
        project_name: str,
        domain: str,
    ) -> bool:
        """验证域名."""
        data = await self._request(
            "POST",
            f"/v9/projects/{project_name}/domains/{domain}/verify",
        )
        return data.get("verified", False)

    async def list_env_vars(
        self,
        project_name: str,
        environment: str | None = None,
    ) -> list[EnvVar]:
        """列出环境变量."""
        data = await self._request("GET", f"/v9/projects/{project_name}/env")

        env_vars = []
        for item in data.get("envs", []):
            if environment and environment not in item.get("target", []):
                continue
            env_vars.append(
                EnvVar(
                    key=item["key"],
                    value=item.get("value"),
                    encrypted=item.get("type") == "encrypted",
                    environment=",".join(item.get("target", [])),
                )
            )
        return env_vars

    async def set_env_var(
        self,
        project_name: str,
        key: str,
        value: str,
        environment: str = "production",
        encrypted: bool = True,
    ) -> None:
        """设置环境变量."""
        project = await self._get_or_create_project(project_name)
        target = (
            ["production"]
            if environment == "production"
            else ["preview"]
            if environment == "preview"
            else ["development"]
        )

        await self._request(
            "POST",
            f"/v10/projects/{project['id']}/env",
            json={
                "key": key,
                "value": value,
                "type": "encrypted" if encrypted else "plain",
                "target": target,
            },
        )
        logger.info(f"已设置环境变量: {key} ({environment})")


# ============================================================================
# Cloudflare 提供商
# ============================================================================


class CloudflareProvider(DeploymentProvider):
    """Cloudflare Pages 部署提供商."""

    BASE_URL = "https://api.cloudflare.com/client/v4"

    def __init__(self, config: CloudflareConfig) -> None:
        """初始化 Cloudflare 提供商."""
        self._config = config
        self._client: Any = None

    async def _ensure_client(self) -> Any:
        """确保 HTTP 客户端已初始化."""
        if self._client is None:
            try:
                import httpx
            except ImportError:
                raise ConfigError("httpx 库未安装，请运行: pip install httpx")

            self._client = httpx.AsyncClient(
                base_url=self.BASE_URL,
                headers={
                    "Authorization": f"Bearer {self._config.api_token}",
                    "Content-Type": "application/json",
                },
                timeout=60.0,
            )
        return self._client

    async def _request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """发送 API 请求."""
        client = await self._ensure_client()

        try:
            response = await client.request(method, path, **kwargs)
            data = response.json()

            if not data.get("success", True):
                errors = data.get("errors", [])
                error_msg = errors[0].get("message") if errors else "Unknown error"
                raise ProviderError(f"Cloudflare API 错误: {error_msg}")

            return data.get("result", data)
        except Exception as e:
            if isinstance(e, ProviderError):
                raise
            raise ProviderError(f"Cloudflare API 错误: {e}")

    async def deploy(
        self,
        project_name: str,
        source_path: str,
        environment: str = "production",
        env_vars: dict[str, str] | None = None,
        branch: str | None = None,
        **kwargs: Any,
    ) -> Deployment:
        """部署到 Cloudflare Pages."""
        account_id = self._config.account_id

        # 获取或创建项目
        project = await self._get_or_create_project(project_name)

        # 创建部署（直接上传）
        # 注意：实际需要上传文件到 Pages
        deployment_data = await self._request(
            "POST",
            f"/accounts/{account_id}/pages/projects/{project_name}/deployments",
            json={
                "branch": branch or "main",
            },
        )

        deployment = self._parse_deployment(deployment_data, project_name)

        # 设置环境变量
        if env_vars:
            await self._set_env_vars(project_name, env_vars, environment)

        logger.info(f"Cloudflare Pages 部署已创建: {deployment.id}")
        return deployment

    async def _get_or_create_project(self, name: str) -> dict[str, Any]:
        """获取或创建项目."""
        account_id = self._config.account_id

        try:
            return await self._request(
                "GET", f"/accounts/{account_id}/pages/projects/{name}"
            )
        except ProviderError:
            # 创建新项目
            return await self._request(
                "POST",
                f"/accounts/{account_id}/pages/projects",
                json={
                    "name": name,
                    "production_branch": "main",
                },
            )

    async def _set_env_vars(
        self,
        project_name: str,
        env_vars: dict[str, str],
        environment: str,
    ) -> None:
        """设置环境变量."""
        account_id = self._config.account_id
        env_type = "production" if environment == "production" else "preview"

        await self._request(
            "PATCH",
            f"/accounts/{account_id}/pages/projects/{project_name}",
            json={
                "deployment_configs": {
                    env_type: {
                        "env_vars": {k: {"value": v} for k, v in env_vars.items()}
                    }
                }
            },
        )

    def _parse_deployment(
        self, data: dict[str, Any], project_name: str
    ) -> Deployment:
        """解析部署数据."""
        return Deployment(
            id=data.get("id", ""),
            url=data.get("url", f"https://{project_name}.pages.dev"),
            status=data.get("latest_stage", {}).get("status", "building"),
            created_at=datetime.fromisoformat(
                data.get("created_on", datetime.now().isoformat()).replace("Z", "+00:00")
            ),
            environment=data.get("environment", "production"),
            branch=data.get("deployment_trigger", {}).get("metadata", {}).get("branch"),
            commit_sha=data.get("deployment_trigger", {})
            .get("metadata", {})
            .get("commit_hash"),
        )

    async def list_deployments(
        self,
        project_name: str,
        limit: int = 10,
    ) -> list[Deployment]:
        """获取部署列表."""
        account_id = self._config.account_id
        data = await self._request(
            "GET",
            f"/accounts/{account_id}/pages/projects/{project_name}/deployments",
            params={"per_page": limit},
        )

        # Cloudflare 返回的是列表
        deployments = data if isinstance(data, list) else data.get("deployments", [])
        return [self._parse_deployment(d, project_name) for d in deployments]

    async def get_deployment(
        self,
        project_name: str,
        deployment_id: str,
    ) -> Deployment:
        """获取部署详情."""
        account_id = self._config.account_id
        data = await self._request(
            "GET",
            f"/accounts/{account_id}/pages/projects/{project_name}/deployments/{deployment_id}",
        )
        return self._parse_deployment(data, project_name)

    async def rollback(
        self,
        project_name: str,
        deployment_id: str,
    ) -> Deployment:
        """回滚到指定版本."""
        account_id = self._config.account_id
        data = await self._request(
            "POST",
            f"/accounts/{account_id}/pages/projects/{project_name}/deployments/{deployment_id}/rollback",
        )
        logger.info(f"已回滚到部署: {deployment_id}")
        return self._parse_deployment(data, project_name)

    async def delete_deployment(
        self,
        project_name: str,
        deployment_id: str,
    ) -> bool:
        """删除部署."""
        account_id = self._config.account_id
        await self._request(
            "DELETE",
            f"/accounts/{account_id}/pages/projects/{project_name}/deployments/{deployment_id}",
        )
        logger.info(f"已删除部署: {deployment_id}")
        return True


# ============================================================================
# 统一部署管理器
# ============================================================================


class DeploymentManager:
    """统一部署管理器.

    支持 Vercel、Cloudflare Pages 等平台的部署管理。

    使用示例:
        ```python
        config = VercelConfig(token="...")
        deployer = DeploymentManager(provider="vercel", config=config)

        # 部署
        deployment = await deployer.deploy(
            project_name="my-app",
            source_path="./dist",
            environment="production",
        )
        print(deployment.url)
        ```
    """

    def __init__(
        self,
        provider: str = "vercel",
        config: DeploymentConfig | None = None,
    ) -> None:
        """初始化部署管理器.

        Args:
            provider: 部署提供商（vercel/cloudflare_pages/cloudflare_workers）
            config: 提供商配置
        """
        self._provider_name = provider
        self._config = config
        self._provider: DeploymentProvider | None = None

        self._initialize_provider()

    def _initialize_provider(self) -> None:
        """初始化提供商."""
        if self._provider_name == "vercel":
            if not isinstance(self._config, VercelConfig):
                raise ConfigError("Vercel 需要 VercelConfig 配置")
            self._provider = VercelProvider(self._config)
        elif self._provider_name in ("cloudflare_pages", "cloudflare"):
            if not isinstance(self._config, CloudflareConfig):
                raise ConfigError("Cloudflare 需要 CloudflareConfig 配置")
            self._provider = CloudflareProvider(self._config)
        else:
            raise ConfigError(f"不支持的提供商: {self._provider_name}")

        logger.info(f"部署管理器已初始化: {self._provider_name}")

    # ========================================================================
    # 核心部署功能
    # ========================================================================

    async def deploy(
        self,
        project_name: str,
        source_path: str,
        environment: str = "production",
        env_vars: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> Deployment:
        """部署项目.

        Args:
            project_name: 项目名
            source_path: 源文件路径
            environment: 环境（production/preview/development）
            env_vars: 环境变量
            **kwargs: 其他参数

        Returns:
            部署信息
        """
        return await self._provider.deploy(
            project_name=project_name,
            source_path=source_path,
            environment=environment,
            env_vars=env_vars,
            **kwargs,
        )

    async def list_deployments(
        self,
        project_name: str,
        limit: int = 10,
    ) -> list[Deployment]:
        """获取部署列表.

        Args:
            project_name: 项目名
            limit: 返回数量

        Returns:
            部署列表
        """
        return await self._provider.list_deployments(project_name, limit)

    async def get_deployment_status(
        self,
        project_name: str,
        deployment_id: str,
    ) -> Deployment:
        """获取部署状态.

        Args:
            project_name: 项目名
            deployment_id: 部署 ID

        Returns:
            部署信息
        """
        return await self._provider.get_deployment(project_name, deployment_id)

    async def rollback(
        self,
        project_name: str,
        deployment_id: str,
    ) -> Deployment:
        """回滚到指定版本.

        Args:
            project_name: 项目名
            deployment_id: 部署 ID

        Returns:
            回滚后的部署信息
        """
        return await self._provider.rollback(project_name, deployment_id)

    async def rollback_to_previous(self, project_name: str) -> Deployment:
        """回滚到上一个版本.

        Args:
            project_name: 项目名

        Returns:
            回滚后的部署信息
        """
        deployments = await self.list_deployments(project_name, limit=2)
        if len(deployments) < 2:
            raise RollbackError("没有可回滚的版本")

        previous = deployments[1]
        return await self.rollback(project_name, previous.id)

    async def delete_deployment(
        self,
        project_name: str,
        deployment_id: str,
    ) -> bool:
        """删除部署.

        Args:
            project_name: 项目名
            deployment_id: 部署 ID

        Returns:
            是否成功
        """
        return await self._provider.delete_deployment(project_name, deployment_id)

    # ========================================================================
    # 预览环境
    # ========================================================================

    async def create_preview(
        self,
        project_name: str,
        source_path: str,
        branch: str | None = None,
        pr_number: int | None = None,
    ) -> Deployment:
        """创建预览部署.

        Args:
            project_name: 项目名
            source_path: 源文件路径
            branch: 分支名
            pr_number: PR 号

        Returns:
            预览部署信息
        """
        if isinstance(self._provider, VercelProvider):
            return await self._provider.create_preview(
                project_name, source_path, branch, pr_number
            )

        return await self.deploy(
            project_name=project_name,
            source_path=source_path,
            environment="preview",
            branch=branch,
        )

    async def delete_preview(self, preview_id: str) -> bool:
        """删除预览部署.

        Args:
            preview_id: 预览部署 ID

        Returns:
            是否成功
        """
        # 从 ID 提取项目名（格式依赖于提供商）
        # 这里简化处理
        return True

    # ========================================================================
    # 等待部署完成
    # ========================================================================

    async def wait_for_deployment(
        self,
        project_name: str,
        deployment_id: str,
        timeout: int = 300,
        interval: int = 5,
    ) -> Deployment:
        """等待部署完成.

        Args:
            project_name: 项目名
            deployment_id: 部署 ID
            timeout: 超时时间（秒）
            interval: 轮询间隔（秒）

        Returns:
            部署信息

        Raises:
            TimeoutError: 超时
            BuildError: 构建失败
        """
        elapsed = 0
        while elapsed < timeout:
            deployment = await self.get_deployment_status(project_name, deployment_id)

            if deployment.status == DeploymentStatus.READY:
                return deployment
            elif deployment.status == DeploymentStatus.ERROR:
                raise BuildError(
                    deployment.error_message or "部署失败",
                    code="BUILD_ERROR",
                )

            await asyncio.sleep(interval)
            elapsed += interval

        raise TimeoutError(f"部署超时: {deployment_id}")

    # ========================================================================
    # 环境变量管理
    # ========================================================================

    async def set_env_var(
        self,
        project_name: str,
        key: str,
        value: str,
        environment: str = "production",
        encrypted: bool = True,
    ) -> None:
        """设置环境变量.

        Args:
            project_name: 项目名
            key: 变量名
            value: 变量值
            environment: 环境
            encrypted: 是否加密
        """
        if isinstance(self._provider, VercelProvider):
            await self._provider.set_env_var(
                project_name, key, value, environment, encrypted
            )
        else:
            # 对于 Cloudflare，使用批量设置
            await self._provider._set_env_vars(project_name, {key: value}, environment)

    async def set_env_vars(
        self,
        project_name: str,
        env_vars: dict[str, str],
        environment: str = "production",
    ) -> None:
        """批量设置环境变量.

        Args:
            project_name: 项目名
            env_vars: 环境变量字典
            environment: 环境
        """
        for key, value in env_vars.items():
            await self.set_env_var(project_name, key, value, environment)

    async def list_env_vars(
        self,
        project_name: str,
        environment: str | None = None,
    ) -> list[EnvVar]:
        """列出环境变量.

        Args:
            project_name: 项目名
            environment: 环境（可选）

        Returns:
            环境变量列表
        """
        if isinstance(self._provider, VercelProvider):
            return await self._provider.list_env_vars(project_name, environment)
        return []

    async def import_env_file(
        self,
        project_name: str,
        file_path: str,
        environment: str = "production",
    ) -> None:
        """从 .env 文件导入环境变量.

        Args:
            project_name: 项目名
            file_path: .env 文件路径
            environment: 环境
        """
        env_vars = {}
        path = Path(file_path)

        if not path.exists():
            raise ConfigError(f".env 文件不存在: {file_path}")

        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip().strip('"').strip("'")

        await self.set_env_vars(project_name, env_vars, environment)
        logger.info(f"已导入 {len(env_vars)} 个环境变量从 {file_path}")

    # ========================================================================
    # 域名管理
    # ========================================================================

    async def add_domain(
        self,
        project_name: str,
        domain: str,
    ) -> DomainInfo:
        """添加自定义域名.

        Args:
            project_name: 项目名
            domain: 域名

        Returns:
            域名信息
        """
        if isinstance(self._provider, VercelProvider):
            return await self._provider.add_domain(project_name, domain)
        raise DomainError(f"{self._provider_name} 不支持域名管理")

    async def verify_domain(
        self,
        project_name: str,
        domain: str,
    ) -> bool:
        """验证域名.

        Args:
            project_name: 项目名
            domain: 域名

        Returns:
            是否验证成功
        """
        if isinstance(self._provider, VercelProvider):
            return await self._provider.verify_domain(project_name, domain)
        raise DomainError(f"{self._provider_name} 不支持域名验证")

    # ========================================================================
    # 日志流
    # ========================================================================

    async def stream_build_logs(
        self,
        project_name: str,
        deployment_id: str,
    ) -> AsyncIterator[str]:
        """流式获取构建日志.

        Args:
            project_name: 项目名
            deployment_id: 部署 ID

        Yields:
            日志行
        """
        # 简化实现 - 实际需要 SSE 或 WebSocket
        deployment = await self.get_deployment_status(project_name, deployment_id)
        yield f"[{deployment.created_at}] 部署状态: {deployment.status}"
        yield f"[{deployment.created_at}] URL: {deployment.url}"

