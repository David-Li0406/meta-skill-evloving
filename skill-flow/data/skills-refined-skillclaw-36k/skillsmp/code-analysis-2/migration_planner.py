# -*- coding: utf-8 -*-
"""移行計画策定スキル - Migration Planner.

レガシーコードの移行計画を策定するスキル。

使用例:
    >>> planner = MigrationPlanner()
    >>> plan = await planner.create_plan(
    ...     source_stack={"language": "cobol", "framework": "mainframe"},
    ...     target_stack={"language": "java", "framework": "spring-boot"},
    ...     analysis_results=analysis,
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


class MigrationStrategy(str, Enum):
    """移行戦略."""

    BIG_BANG = "big_bang"  # 一括移行
    PHASED = "phased"  # 段階的移行
    STRANGLER = "strangler"  # 絞め殺し戦略
    PARALLEL = "parallel"  # 並行運用


class MigrationRisk(str, Enum):
    """移行リスク."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class MigrationTask:
    """移行タスク."""

    task_id: str
    title: str
    description: str
    estimated_hours: float
    dependencies: list[str] = field(default_factory=list)
    assigned_to: str | None = None
    status: str = "pending"


@dataclass
class MigrationPhase:
    """移行フェーズ."""

    phase_id: str
    name: str
    description: str
    scope: list[str]
    tasks: list[MigrationTask]
    estimated_days: int
    risk: MigrationRisk
    prerequisites: list[str] = field(default_factory=list)
    deliverables: list[str] = field(default_factory=list)
    success_criteria: list[str] = field(default_factory=list)


@dataclass
class MigrationPlan:
    """移行計画."""

    plan_id: str
    title: str
    source_stack: dict[str, str]
    target_stack: dict[str, str]
    strategy: MigrationStrategy
    phases: list[MigrationPhase]
    total_estimated_days: int
    total_estimated_cost: float
    overall_risk: MigrationRisk
    key_risks: list[str]
    mitigation_strategies: list[str]
    rollback_plan: str
    created_at: datetime = field(default_factory=datetime.now)


class MigrationPlanner(AgentBlock):
    """移行計画策定スキル.

    レガシーコードの分析結果に基づいて、
    最適な移行計画を策定します。
    """

    def __init__(
        self,
        preferred_strategy: MigrationStrategy = MigrationStrategy.PHASED,
        max_phase_loc: int = 50000,
        llm_client: Any | None = None,
    ) -> None:
        """初期化.

        Args:
            preferred_strategy: 推奨移行戦略
            max_phase_loc: フェーズあたり最大LOC
            llm_client: LLMクライアント
        """
        super().__init__()
        self._preferred_strategy = preferred_strategy
        self._max_phase_loc = max_phase_loc
        self._llm_client = llm_client

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """スキル実行.

        Args:
            input_data: 入力データ
                - source_stack: 移行元スタック
                - target_stack: 移行先スタック
                - analysis_results: 分析結果

        Returns:
            移行計画
        """
        source_stack = input_data.get("source_stack", {})
        target_stack = input_data.get("target_stack", {})
        analysis_results = input_data.get("analysis_results", {})

        plan = await self.create_plan(
            source_stack=source_stack,
            target_stack=target_stack,
            analysis_results=analysis_results,
        )

        return {
            "plan_id": plan.plan_id,
            "title": plan.title,
            "source_stack": plan.source_stack,
            "target_stack": plan.target_stack,
            "strategy": plan.strategy.value,
            "total_estimated_days": plan.total_estimated_days,
            "total_estimated_cost": plan.total_estimated_cost,
            "overall_risk": plan.overall_risk.value,
            "phases": [
                {
                    "phase_id": p.phase_id,
                    "name": p.name,
                    "scope": p.scope,
                    "estimated_days": p.estimated_days,
                    "risk": p.risk.value,
                    "tasks_count": len(p.tasks),
                }
                for p in plan.phases
            ],
            "key_risks": plan.key_risks,
            "mitigation_strategies": plan.mitigation_strategies,
            "created_at": plan.created_at.isoformat(),
        }

    async def create_plan(
        self,
        source_stack: dict[str, str],
        target_stack: dict[str, str],
        analysis_results: dict[str, Any] | None = None,
    ) -> MigrationPlan:
        """移行計画を作成.

        Args:
            source_stack: 移行元スタック
            target_stack: 移行先スタック
            analysis_results: 分析結果

        Returns:
            移行計画
        """
        import uuid

        plan_id = f"mig-{uuid.uuid4().hex[:8]}"
        analysis = analysis_results or {}

        logger.info(
            "移行計画作成: %s -> %s",
            source_stack.get("language", "unknown"),
            target_stack.get("language", "unknown"),
        )

        # 戦略決定
        strategy = self._determine_strategy(analysis)

        # フェーズ生成
        phases = self._generate_phases(source_stack, target_stack, analysis)

        # リスク評価
        overall_risk, key_risks = self._assess_risks(analysis)

        # 緩和策
        mitigation = self._generate_mitigation_strategies(key_risks)

        # 合計見積もり
        total_days = sum(p.estimated_days for p in phases)
        total_cost = total_days * 8 * 150  # 1日8時間 x $150/時間

        return MigrationPlan(
            plan_id=plan_id,
            title=f"{source_stack.get('language', 'Legacy')} → {target_stack.get('language', 'Modern')} 移行計画",
            source_stack=source_stack,
            target_stack=target_stack,
            strategy=strategy,
            phases=phases,
            total_estimated_days=total_days,
            total_estimated_cost=total_cost,
            overall_risk=overall_risk,
            key_risks=key_risks,
            mitigation_strategies=mitigation,
            rollback_plan="各フェーズ完了後にロールバックポイントを設定",
        )

    def _determine_strategy(
        self, analysis: dict[str, Any]
    ) -> MigrationStrategy:
        """移行戦略を決定."""
        total_loc = analysis.get("total_loc", 0)
        complexity_score = analysis.get("complexity_score", 0.5)

        if total_loc < 10000 and complexity_score < 0.3:
            return MigrationStrategy.BIG_BANG
        elif total_loc > 500000:
            return MigrationStrategy.STRANGLER
        else:
            return self._preferred_strategy

    def _generate_phases(
        self,
        source_stack: dict[str, str],
        target_stack: dict[str, str],
        analysis: dict[str, Any],
    ) -> list[MigrationPhase]:
        """移行フェーズを生成."""
        phases = []

        # フェーズ1: 準備
        phases.append(MigrationPhase(
            phase_id="phase-1",
            name="準備フェーズ",
            description="移行環境の構築と基盤整備",
            scope=["インフラ構築", "CI/CD設定", "テスト環境"],
            tasks=[
                MigrationTask(
                    task_id="task-1-1",
                    title="移行先環境構築",
                    description="開発/ステージング/本番環境の構築",
                    estimated_hours=40,
                ),
                MigrationTask(
                    task_id="task-1-2",
                    title="CI/CDパイプライン構築",
                    description="自動ビルド・テスト・デプロイの設定",
                    estimated_hours=24,
                ),
            ],
            estimated_days=10,
            risk=MigrationRisk.LOW,
            deliverables=["環境構築完了", "CI/CDパイプライン稼働"],
            success_criteria=["全環境でアプリ起動確認"],
        ))

        # フェーズ2: コアモジュール移行
        phases.append(MigrationPhase(
            phase_id="phase-2",
            name="コアモジュール移行",
            description="ビジネスロジックの移行",
            scope=["データモデル", "ビジネスロジック", "API層"],
            tasks=[
                MigrationTask(
                    task_id="task-2-1",
                    title="データモデル移行",
                    description="エンティティとスキーマの移行",
                    estimated_hours=80,
                    dependencies=["task-1-1"],
                ),
                MigrationTask(
                    task_id="task-2-2",
                    title="ビジネスロジック移行",
                    description="コアビジネスルールの移行",
                    estimated_hours=120,
                    dependencies=["task-2-1"],
                ),
            ],
            estimated_days=30,
            risk=MigrationRisk.MEDIUM,
            prerequisites=["phase-1完了"],
            deliverables=["コアモジュール移行完了"],
            success_criteria=["単体テスト80%以上カバレッジ"],
        ))

        # フェーズ3: 統合テスト
        phases.append(MigrationPhase(
            phase_id="phase-3",
            name="統合テスト・検証",
            description="移行システムの検証",
            scope=["統合テスト", "性能テスト", "UAT"],
            tasks=[
                MigrationTask(
                    task_id="task-3-1",
                    title="統合テスト実施",
                    description="End-to-Endテストの実行",
                    estimated_hours=60,
                    dependencies=["task-2-2"],
                ),
            ],
            estimated_days=15,
            risk=MigrationRisk.MEDIUM,
            prerequisites=["phase-2完了"],
            deliverables=["テスト完了レポート"],
            success_criteria=["全テストケース合格"],
        ))

        # フェーズ4: 本番移行
        phases.append(MigrationPhase(
            phase_id="phase-4",
            name="本番移行",
            description="本番環境への切り替え",
            scope=["データ移行", "本番切替", "監視"],
            tasks=[
                MigrationTask(
                    task_id="task-4-1",
                    title="データ移行",
                    description="本番データの移行",
                    estimated_hours=24,
                    dependencies=["task-3-1"],
                ),
            ],
            estimated_days=5,
            risk=MigrationRisk.HIGH,
            prerequisites=["phase-3完了", "Go/No-Go判定"],
            deliverables=["本番稼働"],
            success_criteria=["SLA達成", "ロールバックなし"],
        ))

        return phases

    def _assess_risks(
        self, analysis: dict[str, Any]
    ) -> tuple[MigrationRisk, list[str]]:
        """リスクを評価."""
        risks = []
        risk_level = MigrationRisk.MEDIUM

        complexity = analysis.get("complexity_score", 0.5)
        if complexity > 0.7:
            risks.append("コードの複雑度が高く、移行リスクが大きい")
            risk_level = MigrationRisk.HIGH

        security_issues = analysis.get("security_issues", 0)
        if security_issues > 5:
            risks.append(f"{security_issues}件のセキュリティ問題を移行前に解決必要")

        tech_debt = analysis.get("tech_debt_days", 0)
        if tech_debt > 30:
            risks.append(f"技術的負債が{tech_debt}日分あり、スケジュールに影響")

        if not risks:
            risks.append("大きなリスクは特定されていません")
            risk_level = MigrationRisk.LOW

        return risk_level, risks

    def _generate_mitigation_strategies(
        self, risks: list[str]
    ) -> list[str]:
        """緩和策を生成."""
        strategies = [
            "段階的な移行で各フェーズのリスクを最小化",
            "ロールバック計画を各フェーズで準備",
            "並行運用期間を設けて本番切替リスクを軽減",
            "自動テストカバレッジ80%以上を維持",
        ]
        return strategies
