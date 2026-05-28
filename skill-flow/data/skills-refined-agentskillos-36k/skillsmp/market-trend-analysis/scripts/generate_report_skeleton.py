# -*- coding: utf-8 -*-
"""レポート骨格生成スクリプト - 確定性処理.

このスクリプトはLLM推論を使用せず、確定的にレポート骨格を生成します。
テンプレートに基づいてMarkdown形式のレポート構造を出力。

使用例:
    >>> from agentflow.skills.builtin.market_trend_analysis.scripts.generate_report_skeleton import (
    ...     generate_report_skeleton,
    ... )
    >>> skeleton = generate_report_skeleton(trends, metadata)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class ReportSkeleton:
    """レポート骨格.

    Attributes:
        title: レポートタイトル
        sections: セクションリスト
        metadata: メタ情報
        markdown: Markdown形式の出力
    """

    title: str = ""
    sections: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    markdown: str = ""


def generate_report_skeleton(
    trends: list[dict[str, Any]],
    *,
    period: str | None = None,
    report_type: str = "daily",
) -> ReportSkeleton:
    """トレンドデータからレポート骨格を生成.

    Args:
        trends: トレンドリスト
        period: レポート期間（省略時は自動生成）
        report_type: レポートタイプ（daily/weekly/monthly）

    Returns:
        ReportSkeleton
    """
    now = datetime.now()
    if not period:
        period = now.strftime("%Y-%m-%d") if report_type == "daily" else now.strftime("%Y-W%U")

    title = f"市場動向レポート - {period}"

    sections: list[dict[str, Any]] = []

    # 1. エグゼクティブサマリーセクション
    sections.append({
        "title": "エグゼクティブサマリー",
        "type": "summary",
        "placeholder": "[LLM生成: 主要トレンドの要約]",
        "data": {"trends_count": len(trends)},
    })

    # 2. 主要トレンドセクション
    top_trends = sorted(trends, key=lambda t: t.get("score", 0), reverse=True)[:5]
    trends_section = {
        "title": "主要トレンド",
        "type": "trends",
        "items": [],
    }
    for i, trend in enumerate(top_trends, 1):
        trends_section["items"].append({
            "rank": i,
            "topic": trend.get("topic", "Unknown"),
            "score": trend.get("score", 0),
            "sentiment": trend.get("sentiment", "neutral"),
            "growth_rate": trend.get("growth_rate", 0),
        })
    sections.append(trends_section)

    # 3. センチメント分析セクション
    sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
    for trend in trends:
        sentiment = trend.get("sentiment", "neutral")
        if sentiment in sentiment_counts:
            sentiment_counts[sentiment] += 1
    sections.append({
        "title": "センチメント分析",
        "type": "sentiment",
        "data": sentiment_counts,
    })

    # 4. 推奨アクションセクション
    sections.append({
        "title": "推奨アクション",
        "type": "recommendations",
        "placeholder": "[LLM生成: トレンドに基づく推奨事項]",
    })

    # Markdown生成
    markdown = _generate_markdown(title, sections)

    return ReportSkeleton(
        title=title,
        sections=sections,
        metadata={
            "generated_at": now.isoformat(),
            "period": period,
            "report_type": report_type,
            "trends_analyzed": len(trends),
        },
        markdown=markdown,
    )


def _generate_markdown(title: str, sections: list[dict[str, Any]]) -> str:
    """セクションからMarkdownを生成.

    Args:
        title: レポートタイトル
        sections: セクションリスト

    Returns:
        Markdown文字列
    """
    lines: list[str] = [f"# {title}", ""]

    for section in sections:
        lines.append(f"## {section['title']}")
        lines.append("")

        section_type = section.get("type", "")

        if section_type == "summary":
            lines.append(section.get("placeholder", ""))
            lines.append(f"- 分析トレンド数: {section['data']['trends_count']}")

        elif section_type == "trends":
            lines.append("| 順位 | トピック | スコア | センチメント | 成長率 |")
            lines.append("|------|----------|--------|--------------|--------|")
            for item in section.get("items", []):
                growth_pct = f"{item['growth_rate']*100:+.1f}%"
                lines.append(
                    f"| {item['rank']} | {item['topic']} | {item['score']:.2f} | "
                    f"{item['sentiment']} | {growth_pct} |"
                )

        elif section_type == "sentiment":
            data = section.get("data", {})
            lines.append(f"- ポジティブ: {data.get('positive', 0)}")
            lines.append(f"- ネガティブ: {data.get('negative', 0)}")
            lines.append(f"- ニュートラル: {data.get('neutral', 0)}")

        elif section_type == "recommendations":
            lines.append(section.get("placeholder", ""))

        lines.append("")

    return "\n".join(lines)

