# -*- coding: utf-8 -*-
"""複雑度評価スキル - Complexity Scorer.

コードの複雑度を評価し、リファクタリング優先度を提案するスキル。

使用例:
    >>> scorer = ComplexityScorer()
    >>> report = await scorer.score(
    ...     files=["src/main.py", "src/utils.py"],
    ...     thresholds={"max_ccn": 10, "max_loc": 200},
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


class ComplexityLevel(str, Enum):
    """複雑度レベル."""

    LOW = "low"  # CCN 1-5
    MODERATE = "moderate"  # CCN 6-10
    HIGH = "high"  # CCN 11-20
    VERY_HIGH = "very_high"  # CCN 21-50
    UNMAINTAINABLE = "unmaintainable"  # CCN 50+


@dataclass
class ComplexityMetrics:
    """複雑度メトリクス."""

    cyclomatic_complexity: float  # 循環的複雑度
    cognitive_complexity: float  # 認知的複雑度
    lines_of_code: int  # コード行数
    comment_ratio: float  # コメント率
    duplication_ratio: float  # 重複率
    nesting_depth: int  # 最大ネスト深度
    parameters_count: int  # パラメータ数


@dataclass
class FunctionComplexity:
    """関数別複雑度."""

    function_name: str
    file_path: str
    start_line: int
    end_line: int
    metrics: ComplexityMetrics
    level: ComplexityLevel
    refactor_priority: int  # 1-5 (5が最優先)


@dataclass
class FileComplexity:
    """ファイル別複雑度."""

    file_path: str
    total_functions: int
    average_ccn: float
    max_ccn: float
    total_loc: int
    functions: list[FunctionComplexity] = field(default_factory=list)
    hotspots: list[str] = field(default_factory=list)


@dataclass
class ComplexityReport:
    """複雑度レポート."""

    total_files: int
    total_functions: int
    average_ccn: float
    max_ccn: float
    total_loc: int
    maintainability_index: float  # 保守性指数 (0-100)
    tech_debt_days: float  # 技術的負債（日数）
    files: list[FileComplexity]
    hotspots: list[FunctionComplexity]
    refactor_recommendations: list[str]
    analyzed_at: datetime = field(default_factory=datetime.now)


class ComplexityScorer(AgentBlock):
    """複雑度評価スキル.

    コードの複雑度を評価し、
    リファクタリングの優先度を提案します。
    """

    def __init__(
        self,
        ccn_threshold: int = 10,
        loc_threshold: int = 200,
        nesting_threshold: int = 4,
        llm_client: Any | None = None,
    ) -> None:
        """初期化.

        Args:
            ccn_threshold: CCN警告しきい値
            loc_threshold: LOC警告しきい値
            nesting_threshold: ネスト深度警告しきい値
            llm_client: LLMクライアント
        """
        super().__init__()
        self._ccn_threshold = ccn_threshold
        self._loc_threshold = loc_threshold
        self._nesting_threshold = nesting_threshold
        self._llm_client = llm_client

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """スキル実行.

        Args:
            input_data: 入力データ
                - files: 分析対象ファイルリスト
                - thresholds: しきい値設定

        Returns:
            複雑度レポート
        """
        files = input_data.get("files", [])
        thresholds = input_data.get("thresholds", {})

        if thresholds:
            self._ccn_threshold = thresholds.get("max_ccn", self._ccn_threshold)
            self._loc_threshold = thresholds.get("max_loc", self._loc_threshold)

        report = await self.score(files=files)

        return {
            "total_files": report.total_files,
            "total_functions": report.total_functions,
            "average_ccn": report.average_ccn,
            "max_ccn": report.max_ccn,
            "total_loc": report.total_loc,
            "maintainability_index": report.maintainability_index,
            "tech_debt_days": report.tech_debt_days,
            "hotspots": [
                {
                    "function_name": h.function_name,
                    "file_path": h.file_path,
                    "ccn": h.metrics.cyclomatic_complexity,
                    "level": h.level.value,
                    "priority": h.refactor_priority,
                }
                for h in report.hotspots[:10]
            ],
            "refactor_recommendations": report.refactor_recommendations,
            "analyzed_at": report.analyzed_at.isoformat(),
        }

    async def score(
        self,
        files: list[str] | None = None,
    ) -> ComplexityReport:
        """複雑度を評価.

        Args:
            files: 分析対象ファイル

        Returns:
            複雑度レポート
        """
        logger.info("複雑度評価開始: %d files", len(files or []))

        # プレースホルダー実装
        # 実際はradon, lizard等のツールを使用

        file_complexities = self._analyze_files(files or [])
        hotspots = self._identify_hotspots(file_complexities)
        recommendations = self._generate_recommendations(hotspots)

        # 集計
        all_functions = []
        for fc in file_complexities:
            all_functions.extend(fc.functions)

        total_functions = len(all_functions)
        all_ccn = [f.metrics.cyclomatic_complexity for f in all_functions]
        average_ccn = sum(all_ccn) / total_functions if total_functions else 0
        max_ccn = max(all_ccn) if all_ccn else 0
        total_loc = sum(fc.total_loc for fc in file_complexities)

        # 保守性指数計算
        maintainability = self._calculate_maintainability_index(
            average_ccn, total_loc, total_functions
        )

        # 技術的負債（日数）
        tech_debt = self._calculate_tech_debt(hotspots)

        return ComplexityReport(
            total_files=len(file_complexities),
            total_functions=total_functions,
            average_ccn=round(average_ccn, 2),
            max_ccn=round(max_ccn, 2),
            total_loc=total_loc,
            maintainability_index=maintainability,
            tech_debt_days=tech_debt,
            files=file_complexities,
            hotspots=hotspots,
            refactor_recommendations=recommendations,
        )

    def _analyze_files(self, files: list[str]) -> list[FileComplexity]:
        """ファイルを分析（デモ用サンプルデータ）."""
        # デモ用サンプルデータ
        sample_files = [
            FileComplexity(
                file_path="src/main.py",
                total_functions=5,
                average_ccn=8.5,
                max_ccn=15.0,
                total_loc=350,
                functions=[
                    FunctionComplexity(
                        function_name="process_data",
                        file_path="src/main.py",
                        start_line=10,
                        end_line=80,
                        metrics=ComplexityMetrics(
                            cyclomatic_complexity=15,
                            cognitive_complexity=20,
                            lines_of_code=70,
                            comment_ratio=0.1,
                            duplication_ratio=0.05,
                            nesting_depth=5,
                            parameters_count=6,
                        ),
                        level=ComplexityLevel.HIGH,
                        refactor_priority=5,
                    ),
                ],
                hotspots=["process_data"],
            ),
            FileComplexity(
                file_path="src/utils.py",
                total_functions=10,
                average_ccn=4.5,
                max_ccn=8.0,
                total_loc=200,
                functions=[],
                hotspots=[],
            ),
        ]
        return sample_files

    def _identify_hotspots(
        self, file_complexities: list[FileComplexity]
    ) -> list[FunctionComplexity]:
        """ホットスポットを特定."""
        all_functions = []
        for fc in file_complexities:
            all_functions.extend(fc.functions)

        # CCNでソートして上位を返す
        hotspots = [
            f for f in all_functions
            if f.metrics.cyclomatic_complexity > self._ccn_threshold
        ]
        hotspots.sort(
            key=lambda f: f.metrics.cyclomatic_complexity, reverse=True
        )
        return hotspots[:20]

    def _generate_recommendations(
        self, hotspots: list[FunctionComplexity]
    ) -> list[str]:
        """リファクタリング推奨を生成."""
        recommendations = []

        for func in hotspots[:5]:
            if func.metrics.cyclomatic_complexity > 20:
                recommendations.append(
                    f"[優先度高] {func.function_name}を複数の小さな関数に分割"
                )
            elif func.metrics.nesting_depth > 4:
                recommendations.append(
                    f"[優先度中] {func.function_name}のネスト深度を削減（ガード節使用）"
                )
            elif func.metrics.parameters_count > 5:
                recommendations.append(
                    f"[優先度低] {func.function_name}のパラメータをオブジェクトに集約"
                )

        if not recommendations:
            recommendations.append("複雑度は許容範囲内です")

        return recommendations

    def _calculate_maintainability_index(
        self, avg_ccn: float, loc: int, functions: int
    ) -> float:
        """保守性指数を計算（0-100）."""
        # 簡易計算: MI = 171 - 5.2*ln(V) - 0.23*G - 16.2*ln(LOC)
        # ここでは簡略化
        import math

        if loc == 0:
            return 100.0

        mi = 171 - 0.23 * avg_ccn - 16.2 * math.log(loc + 1)
        mi = max(0, min(100, mi))
        return round(mi, 1)

    def _calculate_tech_debt(
        self, hotspots: list[FunctionComplexity]
    ) -> float:
        """技術的負債を日数で計算."""
        debt_hours = 0.0
        for func in hotspots:
            ccn = func.metrics.cyclomatic_complexity
            if ccn > 50:
                debt_hours += 16  # 2日
            elif ccn > 20:
                debt_hours += 8  # 1日
            elif ccn > 10:
                debt_hours += 4  # 半日

        return round(debt_hours / 8, 1)  # 日数に変換

    def _get_complexity_level(self, ccn: float) -> ComplexityLevel:
        """複雑度レベルを判定."""
        if ccn <= 5:
            return ComplexityLevel.LOW
        elif ccn <= 10:
            return ComplexityLevel.MODERATE
        elif ccn <= 20:
            return ComplexityLevel.HIGH
        elif ccn <= 50:
            return ComplexityLevel.VERY_HIGH
        else:
            return ComplexityLevel.UNMAINTAINABLE
