# -*- coding: utf-8 -*-
"""在庫・価格調整スキル - Inventory Adjuster.

市場分析に基づいて在庫と価格を調整するスキル。

使用例:
    >>> adjuster = InventoryAdjuster()
    >>> plan = await adjuster.create_adjustment_plan(
    ...     current_inventory={"sku1": 100, "sku2": 50},
    ...     price_analysis=analysis_result,
    ...     sales_data=recent_sales,
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


class AdjustmentType(str, Enum):
    """調整タイプ."""

    PRICE_INCREASE = "price_increase"  # 値上げ
    PRICE_DECREASE = "price_decrease"  # 値下げ
    RESTOCK = "restock"  # 補充
    CLEARANCE = "clearance"  # 在庫処分
    HOLD = "hold"  # 現状維持


class UrgencyLevel(str, Enum):
    """緊急度."""

    CRITICAL = "critical"  # 即座に対応必要
    HIGH = "high"  # 24時間以内
    MEDIUM = "medium"  # 1週間以内
    LOW = "low"  # 1ヶ月以内


@dataclass
class AdjustmentItem:
    """調整アイテム."""

    sku: str
    product_name: str
    adjustment_type: AdjustmentType
    current_price: float
    recommended_price: float | None = None
    current_stock: int = 0
    recommended_stock: int | None = None
    urgency: UrgencyLevel = UrgencyLevel.MEDIUM
    reason: str = ""
    expected_impact: str = ""


@dataclass
class AdjustmentPlan:
    """調整計画."""

    plan_id: str
    items: list[AdjustmentItem]
    total_items: int
    price_adjustments: int
    stock_adjustments: int
    estimated_revenue_impact: float
    estimated_cost_impact: float
    created_at: datetime = field(default_factory=datetime.now)
    valid_until: datetime | None = None
    notes: list[str] = field(default_factory=list)


@dataclass
class InventoryStatus:
    """在庫状況."""

    sku: str
    current_stock: int
    reserved_stock: int = 0
    incoming_stock: int = 0
    days_of_supply: float = 0.0
    turnover_rate: float = 0.0
    last_sale_date: datetime | None = None


class InventoryAdjuster(AgentBlock):
    """在庫・価格調整スキル.

    市場動向と販売データに基づいて、
    最適な在庫量と価格を提案します。
    """

    def __init__(
        self,
        min_days_of_supply: int = 14,
        max_days_of_supply: int = 90,
        price_change_threshold: float = 0.05,
        llm_client: Any | None = None,
    ) -> None:
        """初期化.

        Args:
            min_days_of_supply: 最小在庫日数
            max_days_of_supply: 最大在庫日数
            price_change_threshold: 価格変更しきい値（5%）
            llm_client: LLMクライアント
        """
        super().__init__()
        self._min_dos = min_days_of_supply
        self._max_dos = max_days_of_supply
        self._price_threshold = price_change_threshold
        self._llm_client = llm_client

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """スキル実行.

        Args:
            input_data: 入力データ
                - current_inventory: 現在の在庫 {sku: quantity}
                - current_prices: 現在の価格 {sku: price}
                - price_analysis: 価格分析結果
                - sales_data: 販売データ

        Returns:
            調整計画
        """
        current_inventory = input_data.get("current_inventory", {})
        current_prices = input_data.get("current_prices", {})
        price_analysis = input_data.get("price_analysis", {})
        sales_data = input_data.get("sales_data", {})

        plan = await self.create_adjustment_plan(
            current_inventory=current_inventory,
            current_prices=current_prices,
            price_analysis=price_analysis,
            sales_data=sales_data,
        )

        return {
            "plan_id": plan.plan_id,
            "items": [self._item_to_dict(item) for item in plan.items],
            "total_items": plan.total_items,
            "price_adjustments": plan.price_adjustments,
            "stock_adjustments": plan.stock_adjustments,
            "estimated_revenue_impact": plan.estimated_revenue_impact,
            "estimated_cost_impact": plan.estimated_cost_impact,
            "created_at": plan.created_at.isoformat(),
            "notes": plan.notes,
        }

    async def create_adjustment_plan(
        self,
        current_inventory: dict[str, int],
        current_prices: dict[str, float] | None = None,
        price_analysis: dict[str, Any] | None = None,
        sales_data: dict[str, Any] | None = None,
    ) -> AdjustmentPlan:
        """調整計画を作成.

        Args:
            current_inventory: 現在の在庫
            current_prices: 現在の価格
            price_analysis: 価格分析結果
            sales_data: 販売データ

        Returns:
            調整計画
        """
        import uuid

        plan_id = f"adj-{uuid.uuid4().hex[:8]}"
        current_prices = current_prices or {}
        price_analysis = price_analysis or {}
        sales_data = sales_data or {}

        items: list[AdjustmentItem] = []
        notes: list[str] = []

        recommended_price = price_analysis.get("recommended_price")

        for sku, stock in current_inventory.items():
            current_price = current_prices.get(sku, 0)

            # 在庫調整判定
            stock_adjustment = self._evaluate_stock(sku, stock, sales_data)

            # 価格調整判定
            price_adjustment = self._evaluate_price(
                sku, current_price, recommended_price
            )

            # 調整アイテム作成
            if stock_adjustment or price_adjustment:
                adjustment_type, urgency, reason = self._determine_adjustment(
                    stock, current_price, recommended_price, stock_adjustment
                )

                item = AdjustmentItem(
                    sku=sku,
                    product_name=f"Product {sku}",
                    adjustment_type=adjustment_type,
                    current_price=current_price,
                    recommended_price=recommended_price if price_adjustment else None,
                    current_stock=stock,
                    recommended_stock=self._calculate_optimal_stock(sku, sales_data),
                    urgency=urgency,
                    reason=reason,
                )
                items.append(item)

        # 影響計算
        revenue_impact = self._calculate_revenue_impact(items)
        cost_impact = self._calculate_cost_impact(items)

        # 注釈追加
        if len(items) == 0:
            notes.append("現時点で調整が必要な商品はありません")
        else:
            critical_count = sum(
                1 for i in items if i.urgency == UrgencyLevel.CRITICAL
            )
            if critical_count > 0:
                notes.append(f"緊急対応が必要な商品: {critical_count}件")

        logger.info(
            "調整計画作成完了: %d items, revenue_impact=%.2f",
            len(items), revenue_impact,
        )

        return AdjustmentPlan(
            plan_id=plan_id,
            items=items,
            total_items=len(items),
            price_adjustments=sum(
                1 for i in items
                if i.adjustment_type in [
                    AdjustmentType.PRICE_INCREASE,
                    AdjustmentType.PRICE_DECREASE,
                ]
            ),
            stock_adjustments=sum(
                1 for i in items
                if i.adjustment_type in [
                    AdjustmentType.RESTOCK,
                    AdjustmentType.CLEARANCE,
                ]
            ),
            estimated_revenue_impact=revenue_impact,
            estimated_cost_impact=cost_impact,
            notes=notes,
        )

    def _evaluate_stock(
        self,
        sku: str,
        stock: int,
        sales_data: dict[str, Any],
    ) -> bool:
        """在庫調整が必要か評価."""
        # 簡易実装: 在庫が少なすぎるか多すぎる場合
        daily_sales = sales_data.get(sku, {}).get("daily_avg", 1)
        days_of_supply = stock / daily_sales if daily_sales > 0 else float("inf")

        return days_of_supply < self._min_dos or days_of_supply > self._max_dos

    def _evaluate_price(
        self,
        sku: str,
        current_price: float,
        recommended_price: float | None,
    ) -> bool:
        """価格調整が必要か評価."""
        if recommended_price is None or current_price == 0:
            return False

        price_diff = abs(recommended_price - current_price) / current_price
        return price_diff > self._price_threshold

    def _determine_adjustment(
        self,
        stock: int,
        current_price: float,
        recommended_price: float | None,
        stock_needs_adjustment: bool,
    ) -> tuple[AdjustmentType, UrgencyLevel, str]:
        """調整タイプと緊急度を決定."""
        # 在庫切れ危機
        if stock < 10:
            return (
                AdjustmentType.RESTOCK,
                UrgencyLevel.CRITICAL,
                "在庫切れ危機",
            )

        # 過剰在庫
        if stock > 1000:
            return (
                AdjustmentType.CLEARANCE,
                UrgencyLevel.HIGH,
                "過剰在庫の処分推奨",
            )

        # 価格調整
        if recommended_price and current_price > 0:
            if recommended_price > current_price * 1.1:
                return (
                    AdjustmentType.PRICE_INCREASE,
                    UrgencyLevel.MEDIUM,
                    "競合価格に基づく値上げ推奨",
                )
            elif recommended_price < current_price * 0.9:
                return (
                    AdjustmentType.PRICE_DECREASE,
                    UrgencyLevel.HIGH,
                    "競争力向上のための値下げ推奨",
                )

        return (
            AdjustmentType.HOLD,
            UrgencyLevel.LOW,
            "現状維持推奨",
        )

    def _calculate_optimal_stock(
        self,
        sku: str,
        sales_data: dict[str, Any],
    ) -> int:
        """最適在庫量を計算."""
        daily_sales = sales_data.get(sku, {}).get("daily_avg", 1)
        # 安全在庫 = 30日分
        return int(daily_sales * 30)

    def _calculate_revenue_impact(self, items: list[AdjustmentItem]) -> float:
        """収益影響を計算."""
        impact = 0.0
        for item in items:
            if item.recommended_price and item.current_price > 0:
                price_change = item.recommended_price - item.current_price
                estimated_units = item.current_stock * 0.1  # 10%販売想定
                impact += price_change * estimated_units
        return round(impact, 2)

    def _calculate_cost_impact(self, items: list[AdjustmentItem]) -> float:
        """コスト影響を計算."""
        impact = 0.0
        for item in items:
            if item.adjustment_type == AdjustmentType.RESTOCK:
                restock_qty = (item.recommended_stock or 0) - item.current_stock
                unit_cost = item.current_price * 0.6  # 原価60%想定
                impact += restock_qty * unit_cost
        return round(impact, 2)

    def _item_to_dict(self, item: AdjustmentItem) -> dict[str, Any]:
        """アイテムをdict形式に変換."""
        return {
            "sku": item.sku,
            "product_name": item.product_name,
            "adjustment_type": item.adjustment_type.value,
            "current_price": item.current_price,
            "recommended_price": item.recommended_price,
            "current_stock": item.current_stock,
            "recommended_stock": item.recommended_stock,
            "urgency": item.urgency.value,
            "reason": item.reason,
            "expected_impact": item.expected_impact,
        }
