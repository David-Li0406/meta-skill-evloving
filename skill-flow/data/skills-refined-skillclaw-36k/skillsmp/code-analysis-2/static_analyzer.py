# -*- coding: utf-8 -*-
"""静的分析スキル - Static Analyzer.

コードの静的分析を行い、品質問題を検出するスキル。

使用例:
    >>> analyzer = StaticAnalyzer()
    >>> result = await analyzer.analyze(
    ...     repo_info=repo,
    ...     languages=["python", "javascript"],
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


class IssueSeverity(str, Enum):
    """問題の重要度."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class IssueCategory(str, Enum):
    """問題のカテゴリ."""

    BUG = "bug"  # バグ
    CODE_SMELL = "code_smell"  # コードスメル
    VULNERABILITY = "vulnerability"  # 脆弱性
    DUPLICATION = "duplication"  # 重複
    STYLE = "style"  # スタイル違反
    COMPLEXITY = "complexity"  # 複雑度


@dataclass
class CodeIssue:
    """検出された問題."""

    issue_id: str
    file_path: str
    line_number: int
    column: int | None = None
    severity: IssueSeverity = IssueSeverity.MEDIUM
    category: IssueCategory = IssueCategory.CODE_SMELL
    rule_id: str = ""
    message: str = ""
    suggestion: str | None = None
    code_snippet: str | None = None


@dataclass
class FileSummary:
    """ファイル別サマリー."""

    file_path: str
    issues_count: int
    critical_count: int = 0
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0


@dataclass
class AnalysisResult:
    """分析結果."""

    total_files_analyzed: int
    total_issues: int
    issues_by_severity: dict[str, int]
    issues_by_category: dict[str, int]
    issues: list[CodeIssue]
    file_summaries: list[FileSummary]
    tech_debt_hours: float  # 技術的負債（修正時間）
    quality_score: float  # 0-100
    analyzed_at: datetime = field(default_factory=datetime.now)


class StaticAnalyzer(AgentBlock):
    """静的分析スキル.

    コードの品質問題、バグ、セキュリティ問題を検出します。
    """

    def __init__(
        self,
        enabled_rules: list[str] | None = None,
        severity_threshold: IssueSeverity = IssueSeverity.LOW,
        llm_client: Any | None = None,
    ) -> None:
        """初期化.

        Args:
            enabled_rules: 有効なルール
            severity_threshold: 報告する最低重要度
            llm_client: LLMクライアント
        """
        super().__init__()
        self._enabled_rules = enabled_rules
        self._severity_threshold = severity_threshold
        self._llm_client = llm_client

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """スキル実行.

        Args:
            input_data: 入力データ
                - repo_info: リポジトリ情報
                - files: 分析対象ファイルリスト
                - languages: 対象言語

        Returns:
            分析結果
        """
        files = input_data.get("files", [])
        languages = input_data.get("languages", [])

        result = await self.analyze(files=files, languages=languages)

        return {
            "total_files_analyzed": result.total_files_analyzed,
            "total_issues": result.total_issues,
            "issues_by_severity": result.issues_by_severity,
            "issues_by_category": result.issues_by_category,
            "tech_debt_hours": result.tech_debt_hours,
            "quality_score": result.quality_score,
            "issues": [self._issue_to_dict(i) for i in result.issues[:100]],
            "analyzed_at": result.analyzed_at.isoformat(),
        }

    async def analyze(
        self,
        files: list[str] | list[dict] | None = None,
        languages: list[str] | None = None,
    ) -> AnalysisResult:
        """静的分析を実行.

        Args:
            files: 分析対象ファイル
            languages: 対象言語

        Returns:
            分析結果
        """
        logger.info("静的分析開始: %d files", len(files or []))

        # プレースホルダー実装
        # 実際はSonarQube、ESLint、Pylint等のツールを呼び出す

        issues = self._generate_sample_issues()
        file_summaries = self._generate_file_summaries(issues)

        # 重要度別集計
        issues_by_severity = {s.value: 0 for s in IssueSeverity}
        for issue in issues:
            issues_by_severity[issue.severity.value] += 1

        # カテゴリ別集計
        issues_by_category = {c.value: 0 for c in IssueCategory}
        for issue in issues:
            issues_by_category[issue.category.value] += 1

        # 技術的負債計算（各問題に平均修正時間を割り当て）
        debt_per_issue = {
            IssueSeverity.CRITICAL: 4.0,
            IssueSeverity.HIGH: 2.0,
            IssueSeverity.MEDIUM: 1.0,
            IssueSeverity.LOW: 0.5,
            IssueSeverity.INFO: 0.1,
        }
        tech_debt = sum(debt_per_issue[i.severity] for i in issues)

        # 品質スコア計算
        quality_score = self._calculate_quality_score(issues_by_severity)

        return AnalysisResult(
            total_files_analyzed=len(files or []) or 10,
            total_issues=len(issues),
            issues_by_severity=issues_by_severity,
            issues_by_category=issues_by_category,
            issues=issues,
            file_summaries=file_summaries,
            tech_debt_hours=tech_debt,
            quality_score=quality_score,
        )

    def _generate_sample_issues(self) -> list[CodeIssue]:
        """サンプル問題を生成（デモ用）."""
        return [
            CodeIssue(
                issue_id="issue-001",
                file_path="src/main.py",
                line_number=45,
                severity=IssueSeverity.HIGH,
                category=IssueCategory.BUG,
                rule_id="E501",
                message="潜在的なNullポインタ参照",
                suggestion="None チェックを追加してください",
            ),
            CodeIssue(
                issue_id="issue-002",
                file_path="src/utils.py",
                line_number=120,
                severity=IssueSeverity.MEDIUM,
                category=IssueCategory.CODE_SMELL,
                rule_id="C901",
                message="関数の複雑度が高すぎます（CCN=15）",
                suggestion="関数を分割してください",
            ),
            CodeIssue(
                issue_id="issue-003",
                file_path="src/auth.py",
                line_number=78,
                severity=IssueSeverity.CRITICAL,
                category=IssueCategory.VULNERABILITY,
                rule_id="S2068",
                message="ハードコードされた認証情報",
                suggestion="環境変数を使用してください",
            ),
        ]

    def _generate_file_summaries(
        self, issues: list[CodeIssue]
    ) -> list[FileSummary]:
        """ファイル別サマリーを生成."""
        file_issues: dict[str, list[CodeIssue]] = {}
        for issue in issues:
            if issue.file_path not in file_issues:
                file_issues[issue.file_path] = []
            file_issues[issue.file_path].append(issue)

        summaries = []
        for file_path, file_issue_list in file_issues.items():
            summary = FileSummary(
                file_path=file_path,
                issues_count=len(file_issue_list),
                critical_count=sum(
                    1 for i in file_issue_list
                    if i.severity == IssueSeverity.CRITICAL
                ),
                high_count=sum(
                    1 for i in file_issue_list
                    if i.severity == IssueSeverity.HIGH
                ),
                medium_count=sum(
                    1 for i in file_issue_list
                    if i.severity == IssueSeverity.MEDIUM
                ),
                low_count=sum(
                    1 for i in file_issue_list
                    if i.severity == IssueSeverity.LOW
                ),
            )
            summaries.append(summary)

        return summaries

    def _calculate_quality_score(
        self, issues_by_severity: dict[str, int]
    ) -> float:
        """品質スコアを計算（0-100）."""
        # 各重要度にペナルティを設定
        penalties = {
            "critical": 20,
            "high": 10,
            "medium": 5,
            "low": 2,
            "info": 0,
        }

        total_penalty = sum(
            issues_by_severity.get(sev, 0) * pen
            for sev, pen in penalties.items()
        )

        score = max(0, 100 - total_penalty)
        return round(score, 1)

    def _issue_to_dict(self, issue: CodeIssue) -> dict[str, Any]:
        """問題をdict形式に変換."""
        return {
            "issue_id": issue.issue_id,
            "file_path": issue.file_path,
            "line_number": issue.line_number,
            "column": issue.column,
            "severity": issue.severity.value,
            "category": issue.category.value,
            "rule_id": issue.rule_id,
            "message": issue.message,
            "suggestion": issue.suggestion,
        }
