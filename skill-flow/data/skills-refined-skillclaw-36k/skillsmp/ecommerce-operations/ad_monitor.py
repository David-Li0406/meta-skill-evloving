# -*- coding: utf-8 -*-
"""広告監視スキル - Ad Monitor.

広告キャンペーンのパフォーマンスを監視し、最適化提案を行うスキル。

使用例:
    >>> monitor = AdMonitor()
    >>> performance = await monitor.analyze_campaigns(
    ...     campaigns=[{"id": "camp1", "spend": 1000, "clicks": 500}],
    ...     time_range="7d",
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


class AlertSeverity(str, Enum):
    """アラート重要度."""

    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


class MetricTrend(str, Enum):
    """指標トレンド."""

    UP = "up"
    DOWN = "down"
    STABLE = "stable"


@dataclass
class AdMetrics:
    """広告指標."""

    impressions: int = 0
    clicks: int = 0
    conversions: int = 0
    spend: float = 0.0
    revenue: float = 0.0

    @property
    def ctr(self) -> float:
        """クリック率."""
        return self.clicks / self.impressions if self.impressions > 0 else 0.0

    @property
    def cvr(self) -> float:
        """コンバージョン率."""
        return self.conversions / self.clicks if self.clicks > 0 else 0.0

    @property
    def cpc(self) -> float:
        """クリック単価."""
        return self.spend / self.clicks if self.clicks > 0 else 0.0

    @property
    def cpa(self) -> float:
        """獲得単価."""
        return self.spend / self.conversions if self.conversions > 0 else 0.0

    @property
    def roas(self) -> float:
        """広告費用対効果."""
        return self.revenue / self.spend if self.spend > 0 else 0.0


@dataclass
class AdPerformance:
    """広告パフォーマンス."""

    campaign_id: str
    campaign_name: str
    platform: str
    metrics: AdMetrics
    metrics_trend: dict[str, MetricTrend] = field(default_factory=dict)
    performance_score: float = 0.0  # 0-100
    optimization_suggestions: list[str] = field(default_factory=list)
    analyzed_at: datetime = field(default_factory=datetime.now)


@dataclass
class AdAlert:
    """広告アラート."""

    alert_id: str
    campaign_id: str
    severity: AlertSeverity
    title: str
    message: str
    metric_name: str
    current_value: float
    threshold_value: float
    recommended_action: str
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class CampaignAnalysis:
    """キャンペーン分析結果."""

    performances: list[AdPerformance]
    alerts: list[AdAlert]
    total_spend: float
    total_revenue: float
    overall_roas: float
    top_performers: list[str]
    underperformers: list[str]
    analysis_period: str
    analyzed_at: datetime = field(default_factory=datetime.now)


class AdMonitor(AgentBlock):
    """広告監視スキル.

    広告キャンペーンのパフォーマンスをモニタリングし、
    異常検知と最適化提案を行います。
    """

    def __init__(
        self,
        ctr_threshold: float = 0.01,  # 1%
        cvr_threshold: float = 0.02,  # 2%
        roas_threshold: float = 2.0,  # 200%
        llm_client: Any | None = None,
    ) -> None:
        """初期化.

        Args:
            ctr_threshold: CTRしきい値
            cvr_threshold: CVRしきい値
            roas_threshold: ROASしきい値
            llm_client: LLMクライアント
        """
        super().__init__()
        self._ctr_threshold = ctr_threshold
        self._cvr_threshold = cvr_threshold
        self._roas_threshold = roas_threshold
        self._llm_client = llm_client

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """スキル実行.

        Args:
            input_data: 入力データ
                - campaigns: キャンペーンデータリスト
                - time_range: 分析期間

        Returns:
            分析結果
        """
        campaigns = input_data.get("campaigns", [])
        time_range = input_data.get("time_range", "7d")

        analysis = await self.analyze_campaigns(campaigns, time_range)

        return {
            "performances": [
                self._performance_to_dict(p) for p in analysis.performances
            ],
            "alerts": [self._alert_to_dict(a) for a in analysis.alerts],
            "total_spend": analysis.total_spend,
            "total_revenue": analysis.total_revenue,
            "overall_roas": analysis.overall_roas,
            "top_performers": analysis.top_performers,
            "underperformers": analysis.underperformers,
            "analysis_period": analysis.analysis_period,
            "analyzed_at": analysis.analyzed_at.isoformat(),
        }

    async def analyze_campaigns(
        self,
        campaigns: list[dict[str, Any]],
        time_range: str = "7d",
    ) -> CampaignAnalysis:
        """キャンペーンを分析.

        Args:
            campaigns: キャンペーンデータリスト
            time_range: 分析期間

        Returns:
            分析結果
        """
        logger.info("広告分析開始: %d campaigns, period=%s", len(campaigns), time_range)

        performances: list[AdPerformance] = []
        alerts: list[AdAlert] = []
        total_spend = 0.0
        total_revenue = 0.0

        for campaign in campaigns:
            # パフォーマンス分析
            perf = self._analyze_campaign(campaign)
            performances.append(perf)

            total_spend += perf.metrics.spend
            total_revenue += perf.metrics.revenue

            # アラート生成
            campaign_alerts = self._generate_alerts(perf)
            alerts.extend(campaign_alerts)

        # ランキング
        sorted_perfs = sorted(
            performances, key=lambda p: p.metrics.roas, reverse=True
        )
        top_performers = [p.campaign_id for p in sorted_perfs[:3]]
        underperformers = [
            p.campaign_id for p in sorted_perfs
            if p.metrics.roas < self._roas_threshold
        ][:3]

        overall_roas = total_revenue / total_spend if total_spend > 0 else 0.0

        return CampaignAnalysis(
            performances=performances,
            alerts=alerts,
            total_spend=round(total_spend, 2),
            total_revenue=round(total_revenue, 2),
            overall_roas=round(overall_roas, 2),
            top_performers=top_performers,
            underperformers=underperformers,
            analysis_period=time_range,
        )

    def _analyze_campaign(self, campaign: dict[str, Any]) -> AdPerformance:
        """単一キャンペーンを分析."""
        metrics = AdMetrics(
            impressions=campaign.get("impressions", 0),
            clicks=campaign.get("clicks", 0),
            conversions=campaign.get("conversions", 0),
            spend=campaign.get("spend", 0.0),
            revenue=campaign.get("revenue", 0.0),
        )

        # パフォーマンススコア計算
        score = self._calculate_performance_score(metrics)

        # 最適化提案
        suggestions = self._generate_suggestions(metrics)

        return AdPerformance(
            campaign_id=campaign.get("id", "unknown"),
            campaign_name=campaign.get("name", "Unnamed Campaign"),
            platform=campaign.get("platform", "unknown"),
            metrics=metrics,
            performance_score=score,
            optimization_suggestions=suggestions,
        )

    def _calculate_performance_score(self, metrics: AdMetrics) -> float:
        """パフォーマンススコアを計算（0-100）."""
        score = 0.0

        # CTRスコア（25点満点）
        ctr_score = min(metrics.ctr / self._ctr_threshold, 1.0) * 25
        score += ctr_score

        # CVRスコア（25点満点）
        cvr_score = min(metrics.cvr / self._cvr_threshold, 1.0) * 25
        score += cvr_score

        # ROASスコア（50点満点）
        roas_score = min(metrics.roas / self._roas_threshold, 1.0) * 50
        score += roas_score

        return round(score, 1)

    def _generate_suggestions(self, metrics: AdMetrics) -> list[str]:
        """最適化提案を生成."""
        suggestions: list[str] = []

        if metrics.ctr < self._ctr_threshold:
            suggestions.append("広告クリエイティブの改善を検討してください")
            suggestions.append("ターゲティングの見直しを推奨します")

        if metrics.cvr < self._cvr_threshold:
            suggestions.append("ランディングページの最適化を検討してください")
            suggestions.append("商品説明の改善を推奨します")

        if metrics.roas < self._roas_threshold:
            suggestions.append("入札戦略の見直しを検討してください")
            suggestions.append("不採算キーワードの除外を推奨します")

        if metrics.cpc > 1.0:  # $1以上
            suggestions.append("クリック単価が高いです。入札を調整してください")

        if not suggestions:
            suggestions.append("パフォーマンスは良好です。現状維持を推奨します")

        return suggestions

    def _generate_alerts(self, performance: AdPerformance) -> list[AdAlert]:
        """アラートを生成."""
        import uuid

        alerts: list[AdAlert] = []
        metrics = performance.metrics

        # CTRアラート
        if metrics.ctr < self._ctr_threshold * 0.5:
            alerts.append(AdAlert(
                alert_id=f"alert-{uuid.uuid4().hex[:8]}",
                campaign_id=performance.campaign_id,
                severity=AlertSeverity.WARNING,
                title="低CTR警告",
                message=f"CTRが{metrics.ctr:.2%}と低下しています",
                metric_name="ctr",
                current_value=metrics.ctr,
                threshold_value=self._ctr_threshold,
                recommended_action="広告クリエイティブを見直してください",
            ))

        # ROASアラート
        if metrics.roas < 1.0:
            alerts.append(AdAlert(
                alert_id=f"alert-{uuid.uuid4().hex[:8]}",
                campaign_id=performance.campaign_id,
                severity=AlertSeverity.CRITICAL,
                title="ROAS危機",
                message=f"ROASが{metrics.roas:.1f}で赤字状態です",
                metric_name="roas",
                current_value=metrics.roas,
                threshold_value=self._roas_threshold,
                recommended_action="キャンペーンの一時停止を検討してください",
            ))

        return alerts

    def _performance_to_dict(self, perf: AdPerformance) -> dict[str, Any]:
        """パフォーマンスをdict形式に変換."""
        return {
            "campaign_id": perf.campaign_id,
            "campaign_name": perf.campaign_name,
            "platform": perf.platform,
            "metrics": {
                "impressions": perf.metrics.impressions,
                "clicks": perf.metrics.clicks,
                "conversions": perf.metrics.conversions,
                "spend": perf.metrics.spend,
                "revenue": perf.metrics.revenue,
                "ctr": round(perf.metrics.ctr, 4),
                "cvr": round(perf.metrics.cvr, 4),
                "cpc": round(perf.metrics.cpc, 2),
                "cpa": round(perf.metrics.cpa, 2),
                "roas": round(perf.metrics.roas, 2),
            },
            "performance_score": perf.performance_score,
            "optimization_suggestions": perf.optimization_suggestions,
        }

    def _alert_to_dict(self, alert: AdAlert) -> dict[str, Any]:
        """アラートをdict形式に変換."""
        return {
            "alert_id": alert.alert_id,
            "campaign_id": alert.campaign_id,
            "severity": alert.severity.value,
            "title": alert.title,
            "message": alert.message,
            "metric_name": alert.metric_name,
            "current_value": alert.current_value,
            "threshold_value": alert.threshold_value,
            "recommended_action": alert.recommended_action,
            "created_at": alert.created_at.isoformat(),
        }
