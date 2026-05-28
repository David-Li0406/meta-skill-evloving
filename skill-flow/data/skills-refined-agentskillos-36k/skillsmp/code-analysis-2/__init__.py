# -*- coding: utf-8 -*-
"""コード分析・移行 Skills パッケージ.

このパッケージはコード分析と移行に必要なスキルセットを提供します。

含まれるスキル:
- repo_connector: リポジトリ接続
- static_analyzer: 静的コード分析
- complexity_scorer: 複雑度評価
- dependency_mapper: 依存関係マッピング
- security_scanner: セキュリティスキャン
- migration_planner: 移行計画策定

ワークフロー:
    リポジトリ接続 → 静的分析 → 複雑度評価 → 依存関係分析 → セキュリティスキャン → 移行計画

使用例:
    >>> from agentflow.skills.builtin.code_analysis import (
    ...     RepoConnector,
    ...     StaticAnalyzer,
    ...     ComplexityScorer,
    ... )
    >>>
    >>> connector = RepoConnector()
    >>> repo = await connector.connect("https://github.com/org/repo.git")
"""

from agentflow.skills.builtin.code_analysis.repo_connector import (
    RepoConnector,
    RepoInfo,
    RepoConfig,
)
from agentflow.skills.builtin.code_analysis.static_analyzer import (
    StaticAnalyzer,
    AnalysisResult,
    CodeIssue,
    IssueSeverity,
)
from agentflow.skills.builtin.code_analysis.complexity_scorer import (
    ComplexityScorer,
    ComplexityReport,
    FileComplexity,
    ComplexityMetrics,
)
from agentflow.skills.builtin.code_analysis.dependency_mapper import (
    DependencyMapper,
    DependencyGraph,
    DependencyNode,
)
from agentflow.skills.builtin.code_analysis.security_scanner import (
    SecurityScanner,
    SecurityReport,
    Vulnerability,
    VulnerabilitySeverity,
)
from agentflow.skills.builtin.code_analysis.migration_planner import (
    MigrationPlanner,
    MigrationPlan,
    MigrationPhase,
    MigrationRisk,
)

__all__ = [
    # リポジトリ接続
    "RepoConnector",
    "RepoInfo",
    "RepoConfig",
    # 静的分析
    "StaticAnalyzer",
    "AnalysisResult",
    "CodeIssue",
    "IssueSeverity",
    # 複雑度評価
    "ComplexityScorer",
    "ComplexityReport",
    "FileComplexity",
    "ComplexityMetrics",
    # 依存関係
    "DependencyMapper",
    "DependencyGraph",
    "DependencyNode",
    # セキュリティ
    "SecurityScanner",
    "SecurityReport",
    "Vulnerability",
    "VulnerabilitySeverity",
    # 移行計画
    "MigrationPlanner",
    "MigrationPlan",
    "MigrationPhase",
    "MigrationRisk",
]
