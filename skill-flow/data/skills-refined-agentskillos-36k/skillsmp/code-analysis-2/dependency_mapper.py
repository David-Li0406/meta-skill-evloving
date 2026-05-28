# -*- coding: utf-8 -*-
"""依存関係マッピングスキル - Dependency Mapper.

コードベースの依存関係を分析し、依存グラフを構築するスキル。

使用例:
    >>> mapper = DependencyMapper()
    >>> graph = await mapper.map_dependencies(
    ...     repo_info=repo,
    ...     include_external=True,
    ... )
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from agentflow.core.agent_block import AgentBlock


logger = logging.getLogger(__name__)


class DependencyType(str, Enum):
    """依存タイプ."""

    INTERNAL = "internal"  # 内部モジュール
    EXTERNAL = "external"  # 外部パッケージ
    SYSTEM = "system"  # システムライブラリ
    DEV = "dev"  # 開発用依存


class DependencyHealth(str, Enum):
    """依存の健全性."""

    HEALTHY = "healthy"
    OUTDATED = "outdated"
    VULNERABLE = "vulnerable"
    DEPRECATED = "deprecated"


@dataclass
class DependencyNode:
    """依存ノード."""

    name: str
    version: str | None = None
    dep_type: DependencyType = DependencyType.EXTERNAL
    health: DependencyHealth = DependencyHealth.HEALTHY
    latest_version: str | None = None
    license: str | None = None
    dependencies: list[str] = field(default_factory=list)
    dependents: list[str] = field(default_factory=list)
    usage_count: int = 0
    is_direct: bool = True


@dataclass
class CircularDependency:
    """循環依存."""

    path: list[str]
    severity: str = "warning"


@dataclass
class DependencyGraph:
    """依存グラフ."""

    nodes: list[DependencyNode]
    edges: list[tuple[str, str]]  # (from, to)
    total_dependencies: int
    direct_dependencies: int
    indirect_dependencies: int
    external_dependencies: int
    internal_dependencies: int
    circular_dependencies: list[CircularDependency]
    outdated_count: int
    vulnerable_count: int
    analyzed_at: datetime = field(default_factory=datetime.now)


class DependencyMapper(AgentBlock):
    """依存関係マッピングスキル.

    コードベースの依存関係を分析し、
    依存グラフを構築します。
    """

    def __init__(
        self,
        include_dev: bool = False,
        check_versions: bool = True,
        llm_client: Any | None = None,
    ) -> None:
        """初期化.

        Args:
            include_dev: 開発用依存を含めるか
            check_versions: バージョンチェックを行うか
            llm_client: LLMクライアント
        """
        super().__init__()
        self._include_dev = include_dev
        self._check_versions = check_versions
        self._llm_client = llm_client

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """スキル実行.

        Args:
            input_data: 入力データ
                - repo_info: リポジトリ情報
                - include_external: 外部依存を含めるか

        Returns:
            依存グラフ
        """
        include_external = input_data.get("include_external", True)

        graph = await self.map_dependencies(include_external=include_external)

        return {
            "total_dependencies": graph.total_dependencies,
            "direct_dependencies": graph.direct_dependencies,
            "indirect_dependencies": graph.indirect_dependencies,
            "external_dependencies": graph.external_dependencies,
            "internal_dependencies": graph.internal_dependencies,
            "outdated_count": graph.outdated_count,
            "vulnerable_count": graph.vulnerable_count,
            "circular_dependencies": [
                {"path": cd.path, "severity": cd.severity}
                for cd in graph.circular_dependencies
            ],
            "nodes": [self._node_to_dict(n) for n in graph.nodes[:50]],
            "analyzed_at": graph.analyzed_at.isoformat(),
        }

    async def map_dependencies(
        self,
        include_external: bool = True,
    ) -> DependencyGraph:
        """依存関係をマッピング.

        Args:
            include_external: 外部依存を含めるか

        Returns:
            依存グラフ
        """
        logger.info("依存関係マッピング開始")

        # プレースホルダー実装
        # 実際はpip show, npm ls等のツールを使用

        nodes = self._build_dependency_nodes()
        edges = self._build_edges(nodes)
        circular = self._detect_circular_dependencies(edges)

        external_count = sum(
            1 for n in nodes if n.dep_type == DependencyType.EXTERNAL
        )
        internal_count = sum(
            1 for n in nodes if n.dep_type == DependencyType.INTERNAL
        )
        direct_count = sum(1 for n in nodes if n.is_direct)
        outdated_count = sum(
            1 for n in nodes if n.health == DependencyHealth.OUTDATED
        )
        vulnerable_count = sum(
            1 for n in nodes if n.health == DependencyHealth.VULNERABLE
        )

        return DependencyGraph(
            nodes=nodes,
            edges=edges,
            total_dependencies=len(nodes),
            direct_dependencies=direct_count,
            indirect_dependencies=len(nodes) - direct_count,
            external_dependencies=external_count,
            internal_dependencies=internal_count,
            circular_dependencies=circular,
            outdated_count=outdated_count,
            vulnerable_count=vulnerable_count,
        )

    def _build_dependency_nodes(self) -> list[DependencyNode]:
        """依存ノードを構築（デモ用）."""
        return [
            DependencyNode(
                name="pydantic",
                version="2.5.0",
                dep_type=DependencyType.EXTERNAL,
                health=DependencyHealth.HEALTHY,
                latest_version="2.5.2",
                license="MIT",
                usage_count=45,
                is_direct=True,
            ),
            DependencyNode(
                name="httpx",
                version="0.25.0",
                dep_type=DependencyType.EXTERNAL,
                health=DependencyHealth.OUTDATED,
                latest_version="0.27.0",
                license="BSD-3-Clause",
                usage_count=20,
                is_direct=True,
            ),
            DependencyNode(
                name="typing-extensions",
                version="4.8.0",
                dep_type=DependencyType.EXTERNAL,
                health=DependencyHealth.HEALTHY,
                license="PSF",
                dependents=["pydantic"],
                usage_count=100,
                is_direct=False,
            ),
            DependencyNode(
                name="src.utils",
                dep_type=DependencyType.INTERNAL,
                health=DependencyHealth.HEALTHY,
                usage_count=30,
                is_direct=True,
            ),
        ]

    def _build_edges(
        self, nodes: list[DependencyNode]
    ) -> list[tuple[str, str]]:
        """依存エッジを構築."""
        edges = []
        for node in nodes:
            for dep in node.dependencies:
                edges.append((node.name, dep))
            for dependent in node.dependents:
                edges.append((dependent, node.name))
        return edges

    def _detect_circular_dependencies(
        self, edges: list[tuple[str, str]]
    ) -> list[CircularDependency]:
        """循環依存を検出."""
        # 簡易DFS実装
        graph: dict[str, list[str]] = {}
        for src, dst in edges:
            if src not in graph:
                graph[src] = []
            graph[src].append(dst)

        circular: list[CircularDependency] = []

        # 実際の循環検出はより複雑な実装が必要
        # ここではプレースホルダー
        return circular

    def _node_to_dict(self, node: DependencyNode) -> dict[str, Any]:
        """ノードをdict形式に変換."""
        return {
            "name": node.name,
            "version": node.version,
            "type": node.dep_type.value,
            "health": node.health.value,
            "latest_version": node.latest_version,
            "license": node.license,
            "usage_count": node.usage_count,
            "is_direct": node.is_direct,
        }
