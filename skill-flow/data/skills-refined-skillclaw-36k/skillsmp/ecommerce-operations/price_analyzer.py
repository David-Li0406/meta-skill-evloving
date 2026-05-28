# -*- coding: utf-8 -*-
"""価格分析スキル - Price Analyzer.

競合商品の価格を分析し、最適な価格戦略を提案するスキル。

使用例:
    >>> analyzer = PriceAnalyzer()
    >>> analysis = await analyzer.analyze(products=scraped_products)
"""

from __future__ import annotations

import logging
import statistics
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from agentflow.core.agent_block import AgentBlock


logger = logging.getLogger(__name__)


class PriceStrategy(str, Enum):
    """価格戦略."""

    PENETRATION = "penetration"  # 市場浸透価格（低価格参入）
    SKIMMING = "skimming"  # 上澄み吸収価格（高価格開始）
    COMPETITIVE = "competitive"  # 競争価格（市場平均）
    PREMIUM = "premium"  # プレミアム価格（高付加価値）
    ECONOMY = "economy"  # エコノミー価格（低価格維持）


class MarketPosition(str, Enum):
    """市場ポジション."""

    LEADER = "leader"  # 市場リーダー
    CHALLENGER = "challenger"  # 挑戦者
    FOLLOWER = "follower"  # 追従者
    NICHER = "nicher"  # ニッチャー


@dataclass
class PricePoint:
    """価格ポイント."""

    price: float
    currency: str
    product_id: str
    platform: str
    rating: float | None = None
    review_count: int = 0


@dataclass
class PriceAnalysis:
    """価格分析結果."""

    average_price: float
    median_price: float
    min_price: float
    max_price: float
    price_std_dev: float
    price_range: tuple[float, float]
    percentile_25: float
    percentile_75: float
    recommended_price: float
    recommended_strategy: PriceStrategy
    market_position: MarketPosition
    price_points: list[PricePoint] = field(default_factory=list)
    insights: list[str] = field(default_factory=list)
    analyzed_at: datetime = field(default_factory=datetime.now)


@dataclass
class CompetitorPriceInfo:
    """競合価格情報."""

    competitor_id: str
    name: str
    price: float
    market_share: float | None = None
    price_change_30d: float | None = None  # 30日間の価格変動率


class PriceAnalyzer(AgentBlock):
    """価格分析スキル.

    競合商品の価格データを分析し、
    最適な価格戦略と推奨価格を提案します。
    """

    def __init__(
        self,
        target_margin: float = 0.3,
        llm_client: Any | None = None,
    ) -> None:
        """初期化.

        Args:
            target_margin: 目標利益率（デフォルト30%）
            llm_client: LLMクライアント（インサイト生成用）
        """
        super().__init__()
        self._target_margin = target_margin
        self._llm_client = llm_client

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """スキル実行.

        Args:
            input_data: 入力データ
                - products: 商品リスト（ScrapedProductのdict形式）
                - cost: 原価（省略時は推奨価格計算に影響）
                - target_margin: 目標利益率

        Returns:
            価格分析結果
        """
        products = input_data.get("products", [])
        cost = input_data.get("cost")
        target_margin = input_data.get("target_margin", self._target_margin)

        # 価格ポイントを抽出
        price_points = self._extract_price_points(products)

        if not price_points:
            return {
                "error": "分析対象の商品がありません",
                "products_count": 0,
            }

        analysis = await self.analyze(price_points, cost, target_margin)

        return {
            "average_price": analysis.average_price,
            "median_price": analysis.median_price,
            "min_price": analysis.min_price,
            "max_price": analysis.max_price,
            "price_std_dev": analysis.price_std_dev,
            "percentile_25": analysis.percentile_25,
            "percentile_75": analysis.percentile_75,
            "recommended_price": analysis.recommended_price,
            "recommended_strategy": analysis.recommended_strategy.value,
            "market_position": analysis.market_position.value,
            "insights": analysis.insights,
            "products_analyzed": len(price_points),
            "analyzed_at": analysis.analyzed_at.isoformat(),
        }

    async def analyze(
        self,
        price_points: list[PricePoint],
        cost: float | None = None,
        target_margin: float | None = None,
    ) -> PriceAnalysis:
        """価格分析を実行.

        Args:
            price_points: 価格ポイントリスト
            cost: 原価
            target_margin: 目標利益率

        Returns:
            価格分析結果
        """
        target_margin = target_margin or self._target_margin
        prices = [pp.price for pp in price_points]

        # 基本統計量計算
        avg_price = statistics.mean(prices)
        median_price = statistics.median(prices)
        min_price = min(prices)
        max_price = max(prices)
        std_dev = statistics.stdev(prices) if len(prices) > 1 else 0.0

        # パーセンタイル計算
        sorted_prices = sorted(prices)
        n = len(sorted_prices)
        p25_idx = int(n * 0.25)
        p75_idx = int(n * 0.75)
        percentile_25 = sorted_prices[p25_idx] if p25_idx < n else min_price
        percentile_75 = sorted_prices[p75_idx] if p75_idx < n else max_price

        # 推奨価格と戦略を決定
        recommended_price, strategy = self._determine_price_strategy(
            avg_price, median_price, percentile_25, percentile_75,
            cost, target_margin,
        )

        # 市場ポジション判定
        market_position = self._determine_market_position(
            recommended_price, avg_price, std_dev
        )

        # インサイト生成
        insights = self._generate_insights(
            avg_price, median_price, std_dev, min_price, max_price,
            strategy, market_position,
        )

        logger.info(
            "価格分析完了: avg=%.2f, median=%.2f, recommended=%.2f, strategy=%s",
            avg_price, median_price, recommended_price, strategy.value,
        )

        return PriceAnalysis(
            average_price=round(avg_price, 2),
            median_price=round(median_price, 2),
            min_price=round(min_price, 2),
            max_price=round(max_price, 2),
            price_std_dev=round(std_dev, 2),
            price_range=(round(min_price, 2), round(max_price, 2)),
            percentile_25=round(percentile_25, 2),
            percentile_75=round(percentile_75, 2),
            recommended_price=round(recommended_price, 2),
            recommended_strategy=strategy,
            market_position=market_position,
            price_points=price_points,
            insights=insights,
        )

    def _extract_price_points(
        self, products: list[dict[str, Any]]
    ) -> list[PricePoint]:
        """商品リストから価格ポイントを抽出."""
        price_points: list[PricePoint] = []
        for p in products:
            if "price" in p and p["price"] is not None:
                pp = PricePoint(
                    price=float(p["price"]),
                    currency=p.get("currency", "USD"),
                    product_id=p.get("product_id", ""),
                    platform=p.get("platform", ""),
                    rating=p.get("rating"),
                    review_count=p.get("review_count", 0),
                )
                price_points.append(pp)
        return price_points

    def _determine_price_strategy(
        self,
        avg_price: float,
        median_price: float,
        p25: float,
        p75: float,
        cost: float | None,
        target_margin: float,
    ) -> tuple[float, PriceStrategy]:
        """推奨価格と戦略を決定."""
        # 原価ベースの最低価格
        min_viable = cost * (1 + target_margin) if cost else p25

        # 戦略決定ロジック
        if cost and min_viable > p75:
            # 原価が高すぎる場合はプレミアム戦略
            return (p75 * 1.1, PriceStrategy.PREMIUM)

        # 市場平均付近が安全
        competitive_price = (avg_price + median_price) / 2

        if competitive_price < min_viable:
            # 利益確保のため若干高め
            return (min_viable * 1.05, PriceStrategy.COMPETITIVE)

        # 中央値付近で競争価格
        return (competitive_price, PriceStrategy.COMPETITIVE)

    def _determine_market_position(
        self,
        recommended_price: float,
        avg_price: float,
        std_dev: float,
    ) -> MarketPosition:
        """市場ポジションを判定."""
        if std_dev == 0:
            return MarketPosition.FOLLOWER

        z_score = (recommended_price - avg_price) / std_dev

        if z_score > 1.0:
            return MarketPosition.LEADER
        elif z_score > 0.0:
            return MarketPosition.CHALLENGER
        elif z_score > -1.0:
            return MarketPosition.FOLLOWER
        else:
            return MarketPosition.NICHER

    def _generate_insights(
        self,
        avg_price: float,
        median_price: float,
        std_dev: float,
        min_price: float,
        max_price: float,
        strategy: PriceStrategy,
        position: MarketPosition,
    ) -> list[str]:
        """分析インサイトを生成."""
        insights: list[str] = []

        # 価格分布の傾向
        if avg_price > median_price * 1.1:
            insights.append(
                "価格分布は右に歪んでいます（高価格帯の商品が多い）"
            )
        elif avg_price < median_price * 0.9:
            insights.append(
                "価格分布は左に歪んでいます（低価格帯の商品が多い）"
            )
        else:
            insights.append("価格分布は比較的均等です")

        # 価格変動
        cv = std_dev / avg_price if avg_price > 0 else 0
        if cv > 0.3:
            insights.append(
                f"価格の変動が大きい市場です（変動係数: {cv:.2%}）"
            )
        else:
            insights.append(
                f"価格が安定した市場です（変動係数: {cv:.2%}）"
            )

        # 戦略アドバイス
        strategy_advice = {
            PriceStrategy.PENETRATION: "市場浸透を狙った低価格戦略を推奨",
            PriceStrategy.COMPETITIVE: "競争価格での参入を推奨",
            PriceStrategy.PREMIUM: "高付加価値でのプレミアム価格を推奨",
            PriceStrategy.SKIMMING: "初期高価格での利益確保を推奨",
            PriceStrategy.ECONOMY: "低コスト運営での低価格戦略を推奨",
        }
        insights.append(strategy_advice.get(strategy, ""))

        return insights
