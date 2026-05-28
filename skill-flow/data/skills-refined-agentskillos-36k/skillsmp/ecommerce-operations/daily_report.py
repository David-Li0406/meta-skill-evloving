# -*- coding: utf-8 -*-
"""日報生成スキル - Daily Report Generator.

毎日の運営データを集約し、日報レポートを生成するスキル。

使用例:
    >>> generator = DailyReportGenerator()
    >>> report = await generator.generate(
    ...     sales_data=sales,
    ...     ad_data=ad_performance,
    ...     inventory_data=inventory,
    ... )
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
from typing import Any

from agentflow.core.agent_block import AgentBlock


logger = logging.getLogger(__name__)


class ReportFormat(str, Enum):
    """レポート形式."""

    MARKDOWN = "markdown"
    HTML = "html"
    JSON = "json"
    TEXT = "text"


class TrendIndicator(str, Enum):
    """トレンド指標."""

    UP = "↑"
    DOWN = "↓"
    STABLE = "→"


@dataclass
class ReportSection:
    """レポートセクション."""

    title: str
    content: str
    metrics: dict[str, Any] = field(default_factory=dict)
    highlights: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    order: int = 0


@dataclass
class DailySummary:
    """日次サマリー."""

    total_sales: float
    total_orders: int
    avg_order_value: float
    total_ad_spend: float
    total_ad_revenue: float
    roas: float
    new_customers: int
    returning_customers: int
    inventory_alerts: int
    top_products: list[str] = field(default_factory=list)


@dataclass
class DailyReport:
    """日報レポート."""

    report_id: str
    report_date: date
    title: str
    summary: DailySummary
    sections: list[ReportSection]
    executive_summary: str
    action_items: list[str]
    format: ReportFormat
    generated_at: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)


class DailyReportGenerator(AgentBlock):
    """日報生成スキル.

    売上、広告、在庫などのデータを集約し、
    経営判断に役立つ日報レポートを生成します。
    """

    def __init__(
        self,
        report_format: ReportFormat = ReportFormat.MARKDOWN,
        include_charts: bool = False,
        llm_client: Any | None = None,
    ) -> None:
        """初期化.

        Args:
            report_format: レポート形式
            include_charts: チャートを含めるか
            llm_client: LLMクライアント（サマリー生成用）
        """
        super().__init__()
        self._format = report_format
        self._include_charts = include_charts
        self._llm_client = llm_client

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """スキル実行.

        Args:
            input_data: 入力データ
                - sales_data: 売上データ
                - ad_data: 広告データ
                - inventory_data: 在庫データ
                - report_date: レポート日付（省略時は今日）

        Returns:
            生成されたレポート
        """
        sales_data = input_data.get("sales_data", {})
        ad_data = input_data.get("ad_data", {})
        inventory_data = input_data.get("inventory_data", {})
        report_date = input_data.get("report_date")

        if isinstance(report_date, str):
            report_date = datetime.fromisoformat(report_date).date()
        elif report_date is None:
            report_date = date.today()

        report = await self.generate(
            sales_data=sales_data,
            ad_data=ad_data,
            inventory_data=inventory_data,
            report_date=report_date,
        )

        return {
            "report_id": report.report_id,
            "report_date": report.report_date.isoformat(),
            "title": report.title,
            "executive_summary": report.executive_summary,
            "summary": {
                "total_sales": report.summary.total_sales,
                "total_orders": report.summary.total_orders,
                "avg_order_value": report.summary.avg_order_value,
                "total_ad_spend": report.summary.total_ad_spend,
                "total_ad_revenue": report.summary.total_ad_revenue,
                "roas": report.summary.roas,
                "new_customers": report.summary.new_customers,
                "returning_customers": report.summary.returning_customers,
                "inventory_alerts": report.summary.inventory_alerts,
                "top_products": report.summary.top_products,
            },
            "sections": [
                {
                    "title": s.title,
                    "content": s.content,
                    "metrics": s.metrics,
                    "highlights": s.highlights,
                    "warnings": s.warnings,
                }
                for s in report.sections
            ],
            "action_items": report.action_items,
            "format": report.format.value,
            "generated_at": report.generated_at.isoformat(),
        }

    async def generate(
        self,
        sales_data: dict[str, Any],
        ad_data: dict[str, Any],
        inventory_data: dict[str, Any],
        report_date: date | None = None,
    ) -> DailyReport:
        """日報を生成.

        Args:
            sales_data: 売上データ
            ad_data: 広告データ
            inventory_data: 在庫データ
            report_date: レポート日付

        Returns:
            生成されたレポート
        """
        import uuid

        report_date = report_date or date.today()
        report_id = f"report-{report_date.isoformat()}-{uuid.uuid4().hex[:6]}"

        logger.info("日報生成開始: %s", report_date)

        # サマリー作成
        summary = self._create_summary(sales_data, ad_data, inventory_data)

        # セクション生成
        sections: list[ReportSection] = []

        # 売上セクション
        sections.append(self._create_sales_section(sales_data, summary))

        # 広告セクション
        sections.append(self._create_ad_section(ad_data, summary))

        # 在庫セクション
        sections.append(self._create_inventory_section(inventory_data))

        # エグゼクティブサマリー生成
        executive_summary = await self._generate_executive_summary(
            summary, sections
        )

        # アクションアイテム抽出
        action_items = self._extract_action_items(sections)

        return DailyReport(
            report_id=report_id,
            report_date=report_date,
            title=f"日次運営レポート - {report_date.isoformat()}",
            summary=summary,
            sections=sections,
            executive_summary=executive_summary,
            action_items=action_items,
            format=self._format,
        )

    def _create_summary(
        self,
        sales_data: dict[str, Any],
        ad_data: dict[str, Any],
        inventory_data: dict[str, Any],
    ) -> DailySummary:
        """サマリーを作成."""
        total_sales = sales_data.get("total_revenue", 0.0)
        total_orders = sales_data.get("total_orders", 0)
        avg_order_value = total_sales / total_orders if total_orders > 0 else 0.0

        total_ad_spend = ad_data.get("total_spend", 0.0)
        total_ad_revenue = ad_data.get("total_revenue", 0.0)
        roas = total_ad_revenue / total_ad_spend if total_ad_spend > 0 else 0.0

        return DailySummary(
            total_sales=round(total_sales, 2),
            total_orders=total_orders,
            avg_order_value=round(avg_order_value, 2),
            total_ad_spend=round(total_ad_spend, 2),
            total_ad_revenue=round(total_ad_revenue, 2),
            roas=round(roas, 2),
            new_customers=sales_data.get("new_customers", 0),
            returning_customers=sales_data.get("returning_customers", 0),
            inventory_alerts=inventory_data.get("alert_count", 0),
            top_products=sales_data.get("top_products", [])[:5],
        )

    def _create_sales_section(
        self,
        sales_data: dict[str, Any],
        summary: DailySummary,
    ) -> ReportSection:
        """売上セクションを作成."""
        highlights: list[str] = []
        warnings: list[str] = []

        # ハイライト判定
        if summary.total_orders > 0:
            highlights.append(f"本日の受注件数: {summary.total_orders}件")
            highlights.append(f"平均注文金額: ${summary.avg_order_value:.2f}")

        # 警告判定
        yesterday_sales = sales_data.get("yesterday_sales", summary.total_sales)
        if summary.total_sales < yesterday_sales * 0.8:
            warnings.append("売上が前日比20%以上減少しています")

        content = f"""
## 売上概要

| 指標 | 値 | 前日比 |
|------|------|--------|
| 総売上 | ${summary.total_sales:,.2f} | - |
| 受注件数 | {summary.total_orders} | - |
| 平均注文金額 | ${summary.avg_order_value:.2f} | - |
| 新規顧客 | {summary.new_customers} | - |
| リピーター | {summary.returning_customers} | - |

### トップ商品
{chr(10).join(f'- {p}' for p in summary.top_products[:5]) or '- データなし'}
"""

        return ReportSection(
            title="売上レポート",
            content=content,
            metrics={
                "total_sales": summary.total_sales,
                "total_orders": summary.total_orders,
                "avg_order_value": summary.avg_order_value,
            },
            highlights=highlights,
            warnings=warnings,
            order=1,
        )

    def _create_ad_section(
        self,
        ad_data: dict[str, Any],
        summary: DailySummary,
    ) -> ReportSection:
        """広告セクションを作成."""
        highlights: list[str] = []
        warnings: list[str] = []

        if summary.roas >= 2.0:
            highlights.append(f"ROAS {summary.roas:.1f}x - 好調")
        elif summary.roas < 1.0:
            warnings.append(f"ROAS {summary.roas:.1f}x - 赤字状態")

        content = f"""
## 広告パフォーマンス

| 指標 | 値 |
|------|------|
| 広告費用 | ${summary.total_ad_spend:,.2f} |
| 広告経由売上 | ${summary.total_ad_revenue:,.2f} |
| ROAS | {summary.roas:.2f}x |

### キャンペーン別パフォーマンス
{self._format_campaign_table(ad_data.get('campaigns', []))}
"""

        return ReportSection(
            title="広告レポート",
            content=content,
            metrics={
                "total_ad_spend": summary.total_ad_spend,
                "total_ad_revenue": summary.total_ad_revenue,
                "roas": summary.roas,
            },
            highlights=highlights,
            warnings=warnings,
            order=2,
        )

    def _create_inventory_section(
        self,
        inventory_data: dict[str, Any],
    ) -> ReportSection:
        """在庫セクションを作成."""
        alert_count = inventory_data.get("alert_count", 0)
        low_stock = inventory_data.get("low_stock_items", [])
        overstock = inventory_data.get("overstock_items", [])

        warnings: list[str] = []
        if alert_count > 0:
            warnings.append(f"{alert_count}件の在庫アラートがあります")

        content = f"""
## 在庫状況

- アラート件数: {alert_count}

### 在庫切れ警告
{chr(10).join(f'- {item}' for item in low_stock[:5]) or '- なし'}

### 過剰在庫
{chr(10).join(f'- {item}' for item in overstock[:5]) or '- なし'}
"""

        return ReportSection(
            title="在庫レポート",
            content=content,
            metrics={"alert_count": alert_count},
            highlights=[],
            warnings=warnings,
            order=3,
        )

    def _format_campaign_table(self, campaigns: list[dict]) -> str:
        """キャンペーンテーブルをフォーマット."""
        if not campaigns:
            return "- データなし"

        lines = ["| キャンペーン | 費用 | 売上 | ROAS |", "|---|---|---|---|"]
        for c in campaigns[:5]:
            name = c.get("name", "Unknown")
            spend = c.get("spend", 0)
            revenue = c.get("revenue", 0)
            roas = revenue / spend if spend > 0 else 0
            lines.append(f"| {name} | ${spend:.2f} | ${revenue:.2f} | {roas:.2f}x |")

        return "\n".join(lines)

    async def _generate_executive_summary(
        self,
        summary: DailySummary,
        sections: list[ReportSection],
    ) -> str:
        """エグゼクティブサマリーを生成."""
        if self._llm_client:
            prompt = f"""
以下のデータに基づいて、経営者向けの簡潔な日次サマリーを生成してください（3-5文）:

- 総売上: ${summary.total_sales:,.2f}
- 受注件数: {summary.total_orders}
- 広告ROAS: {summary.roas:.2f}x
- 在庫アラート: {summary.inventory_alerts}件
"""
            try:
                response = await self._llm_client.chat([
                    {"role": "user", "content": prompt}
                ])
                return response.get("content", "")
            except Exception as e:
                logger.warning("LLMサマリー生成エラー: %s", e)

        # フォールバック
        return f"""
本日の売上は${summary.total_sales:,.2f}（{summary.total_orders}件）でした。
広告ROASは{summary.roas:.2f}xで{'好調' if summary.roas >= 2 else '改善が必要'}です。
在庫アラートは{summary.inventory_alerts}件あります。
""".strip()

    def _extract_action_items(self, sections: list[ReportSection]) -> list[str]:
        """アクションアイテムを抽出."""
        items: list[str] = []

        for section in sections:
            for warning in section.warnings:
                items.append(f"[{section.title}] {warning}")

        if not items:
            items.append("特に対応が必要な項目はありません")

        return items
