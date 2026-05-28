# -*- coding: utf-8 -*-
"""リポジトリ接続スキル - Repository Connector.

Git/SVNリポジトリに接続し、コードを取得するスキル。

使用例:
    >>> connector = RepoConnector()
    >>> repo = await connector.connect(
    ...     url="https://github.com/org/repo.git",
    ...     branch="main",
    ... )
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

from agentflow.core.agent_block import AgentBlock


logger = logging.getLogger(__name__)


class VCSType(str, Enum):
    """バージョン管理システムタイプ."""

    GIT = "git"
    SVN = "svn"
    MERCURIAL = "hg"


@dataclass
class RepoConfig:
    """リポジトリ設定."""

    vcs_type: VCSType = VCSType.GIT
    branch: str = "main"
    commit_id: str | None = None
    depth: int = 1  # shallow clone depth
    timeout_seconds: float = 300.0
    include_submodules: bool = False
    auth_token: str | None = None


@dataclass
class FileInfo:
    """ファイル情報."""

    path: str
    size_bytes: int
    language: str | None = None
    lines_of_code: int = 0
    last_modified: datetime | None = None


@dataclass
class RepoInfo:
    """リポジトリ情報."""

    url: str
    vcs_type: VCSType
    branch: str
    commit_id: str
    local_path: Path | None = None
    total_files: int = 0
    total_lines: int = 0
    languages: dict[str, int] = field(default_factory=dict)
    files: list[FileInfo] = field(default_factory=list)
    cloned_at: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)


class RepoConnector(AgentBlock):
    """リポジトリ接続スキル.

    Git/SVNリポジトリに接続し、
    コードベースの情報を取得します。
    """

    def __init__(
        self,
        config: RepoConfig | None = None,
        work_dir: str | Path | None = None,
    ) -> None:
        """初期化.

        Args:
            config: リポジトリ設定
            work_dir: 作業ディレクトリ
        """
        super().__init__()
        self._config = config or RepoConfig()
        self._work_dir = Path(work_dir) if work_dir else Path("/tmp/repo_work")

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """スキル実行.

        Args:
            input_data: 入力データ
                - url: リポジトリURL
                - branch: ブランチ名
                - commit_id: コミットID

        Returns:
            リポジトリ情報
        """
        url = input_data.get("url", "")
        branch = input_data.get("branch", self._config.branch)
        commit_id = input_data.get("commit_id")

        if not url:
            return {"error": "リポジトリURLが指定されていません"}

        repo_info = await self.connect(url, branch, commit_id)

        return {
            "url": repo_info.url,
            "vcs_type": repo_info.vcs_type.value,
            "branch": repo_info.branch,
            "commit_id": repo_info.commit_id,
            "total_files": repo_info.total_files,
            "total_lines": repo_info.total_lines,
            "languages": repo_info.languages,
            "cloned_at": repo_info.cloned_at.isoformat(),
        }

    async def connect(
        self,
        url: str,
        branch: str | None = None,
        commit_id: str | None = None,
    ) -> RepoInfo:
        """リポジトリに接続.

        Args:
            url: リポジトリURL
            branch: ブランチ名
            commit_id: コミットID

        Returns:
            リポジトリ情報
        """
        branch = branch or self._config.branch

        logger.info("リポジトリ接続: %s (branch: %s)", url, branch)

        # VCSタイプ検出
        vcs_type = self._detect_vcs_type(url)

        # クローン実行（プレースホルダー - 実際はMCPツールで実行）
        local_path = await self._clone_repo(url, branch, vcs_type)

        # リポジトリ分析
        repo_info = await self._analyze_repo(
            url=url,
            vcs_type=vcs_type,
            branch=branch,
            commit_id=commit_id or "HEAD",
            local_path=local_path,
        )

        return repo_info

    def _detect_vcs_type(self, url: str) -> VCSType:
        """VCSタイプを検出."""
        url_lower = url.lower()
        if "github.com" in url_lower or "gitlab.com" in url_lower or url_lower.endswith(".git"):
            return VCSType.GIT
        elif "svn" in url_lower:
            return VCSType.SVN
        return VCSType.GIT

    async def _clone_repo(
        self,
        url: str,
        branch: str,
        vcs_type: VCSType,
    ) -> Path | None:
        """リポジトリをクローン（プレースホルダー）."""
        # 実際のクローンはMCPツールで実行
        # ここではシミュレーション
        logger.info("クローン: %s -> %s", url, self._work_dir)
        return self._work_dir

    async def _analyze_repo(
        self,
        url: str,
        vcs_type: VCSType,
        branch: str,
        commit_id: str,
        local_path: Path | None,
    ) -> RepoInfo:
        """リポジトリを分析."""
        # プレースホルダー実装
        # 実際はファイルシステムを走査して言語別行数等を計算

        # デモ用データ
        languages = {
            "Python": 5000,
            "JavaScript": 3000,
            "TypeScript": 2000,
            "YAML": 500,
            "Markdown": 300,
        }

        files = [
            FileInfo(path="src/main.py", size_bytes=1024, language="Python", lines_of_code=100),
            FileInfo(path="src/utils.py", size_bytes=2048, language="Python", lines_of_code=200),
        ]

        return RepoInfo(
            url=url,
            vcs_type=vcs_type,
            branch=branch,
            commit_id=commit_id,
            local_path=local_path,
            total_files=len(files),
            total_lines=sum(languages.values()),
            languages=languages,
            files=files,
        )

    def get_supported_languages(self) -> list[str]:
        """サポートする言語一覧を取得."""
        return [
            "Python", "JavaScript", "TypeScript", "Java", "Go",
            "Rust", "C", "C++", "C#", "Ruby", "PHP", "Swift",
            "Kotlin", "Scala", "COBOL", "Fortran",
        ]
