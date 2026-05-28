# -*- coding: utf-8 -*-
"""Listing生成スキル - Listing Generator.

競合分析に基づいて最適化された商品リスティングを生成するスキル。

使用例:
    >>> generator = ListingGenerator(llm_client=llm)
    >>> listing = await generator.generate(
    ...     product_info={"name": "Wireless Earbuds", "features": [...]},
    ...     competitor_data=analysis_result,
    ...     target_platform="amazon",
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


class ListingStyle(str, Enum):
    """リスティングスタイル."""

    PROFESSIONAL = "professional"  # プロフェッショナル
    CASUAL = "casual"  # カジュアル
    TECHNICAL = "technical"  # 技術的
    EMOTIONAL = "emotional"  # 感情訴求
    MINIMALIST = "minimalist"  # ミニマリスト


@dataclass
class ListingConfig:
    """リスティング生成設定."""

    target_platform: str = "amazon"
    language: str = "en"
    style: ListingStyle = ListingStyle.PROFESSIONAL
    max_title_length: int = 200
    max_bullet_points: int = 5
    include_keywords: list[str] = field(default_factory=list)
    exclude_keywords: list[str] = field(default_factory=list)
    tone: str = "persuasive"  # persuasive, informative, friendly


@dataclass
class GeneratedListing:
    """生成されたリスティング."""

    title: str
    bullet_points: list[str]
    description: str
    backend_keywords: list[str]
    search_terms: list[str]
    target_platform: str
    language: str
    style: ListingStyle
    seo_score: float  # 0.0-1.0
    generated_at: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)


class ListingGenerator(AgentBlock):
    """Listing生成スキル.

    商品情報と競合分析に基づいて、
    SEO最適化されたリスティングを生成します。
    """

    def __init__(
        self,
        config: ListingConfig | None = None,
        llm_client: Any | None = None,
    ) -> None:
        """初期化.

        Args:
            config: リスティング設定
            llm_client: LLMクライアント
        """
        super().__init__()
        self._config = config or ListingConfig()
        self._llm_client = llm_client

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """スキル実行.

        Args:
            input_data: 入力データ
                - product_info: 商品情報
                - competitor_data: 競合分析データ（省略可）
                - target_platform: 対象プラットフォーム
                - language: 言語

        Returns:
            生成されたリスティング
        """
        product_info = input_data.get("product_info", {})
        competitor_data = input_data.get("competitor_data", {})
        platform = input_data.get("target_platform", self._config.target_platform)
        language = input_data.get("language", self._config.language)

        listing = await self.generate(
            product_info=product_info,
            competitor_data=competitor_data,
            target_platform=platform,
            language=language,
        )

        return {
            "title": listing.title,
            "bullet_points": listing.bullet_points,
            "description": listing.description,
            "backend_keywords": listing.backend_keywords,
            "search_terms": listing.search_terms,
            "seo_score": listing.seo_score,
            "target_platform": listing.target_platform,
            "language": listing.language,
            "style": listing.style.value,
            "generated_at": listing.generated_at.isoformat(),
        }

    async def generate(
        self,
        product_info: dict[str, Any],
        competitor_data: dict[str, Any] | None = None,
        target_platform: str | None = None,
        language: str | None = None,
    ) -> GeneratedListing:
        """リスティングを生成.

        Args:
            product_info: 商品情報
            competitor_data: 競合分析データ
            target_platform: 対象プラットフォーム
            language: 言語

        Returns:
            生成されたリスティング
        """
        platform = target_platform or self._config.target_platform
        lang = language or self._config.language

        logger.info(
            "Listing生成開始: platform=%s, language=%s",
            platform, lang,
        )

        # キーワード抽出
        keywords = self._extract_keywords(product_info, competitor_data)

        # タイトル生成
        title = await self._generate_title(product_info, keywords, platform)

        # 箇条書き生成
        bullet_points = await self._generate_bullet_points(
            product_info, keywords, platform
        )

        # 説明文生成
        description = await self._generate_description(
            product_info, keywords, platform
        )

        # バックエンドキーワード生成
        backend_keywords = self._generate_backend_keywords(keywords)

        # SEOスコア計算
        seo_score = self._calculate_seo_score(
            title, bullet_points, description, keywords
        )

        return GeneratedListing(
            title=title,
            bullet_points=bullet_points,
            description=description,
            backend_keywords=backend_keywords,
            search_terms=keywords[:10],
            target_platform=platform,
            language=lang,
            style=self._config.style,
            seo_score=seo_score,
            metadata={"product_info": product_info},
        )

    def _extract_keywords(
        self,
        product_info: dict[str, Any],
        competitor_data: dict[str, Any] | None,
    ) -> list[str]:
        """キーワードを抽出."""
        keywords: list[str] = []

        # 商品名からキーワード抽出
        name = product_info.get("name", "")
        if name:
            keywords.extend(name.lower().split())

        # 特徴からキーワード抽出
        features = product_info.get("features", [])
        for feature in features:
            keywords.extend(feature.lower().split()[:3])

        # 設定のキーワードを追加
        keywords.extend(self._config.include_keywords)

        # 除外キーワードを削除
        keywords = [
            k for k in keywords
            if k not in self._config.exclude_keywords
        ]

        # 重複削除
        return list(dict.fromkeys(keywords))

    async def _generate_title(
        self,
        product_info: dict[str, Any],
        keywords: list[str],
        platform: str,
    ) -> str:
        """タイトルを生成."""
        if self._llm_client:
            # LLMを使用してタイトル生成
            prompt = f"""
商品情報: {product_info}
キーワード: {', '.join(keywords[:10])}
プラットフォーム: {platform}

上記の情報に基づいて、SEO最適化された商品タイトルを生成してください。
最大{self._config.max_title_length}文字以内で。
"""
            try:
                response = await self._llm_client.chat([
                    {"role": "user", "content": prompt}
                ])
                return response.get("content", "")[:self._config.max_title_length]
            except Exception as e:
                logger.warning("LLMタイトル生成エラー: %s", e)

        # フォールバック: 基本的なタイトル生成
        name = product_info.get("name", "Product")
        brand = product_info.get("brand", "")
        features = product_info.get("features", [])[:2]

        parts = [brand, name] if brand else [name]
        if features:
            parts.append(" - ".join(features))

        title = " | ".join(filter(None, parts))
        return title[:self._config.max_title_length]

    async def _generate_bullet_points(
        self,
        product_info: dict[str, Any],
        keywords: list[str],
        platform: str,
    ) -> list[str]:
        """箇条書きを生成."""
        features = product_info.get("features", [])
        benefits = product_info.get("benefits", [])

        bullet_points: list[str] = []

        # 特徴から箇条書き生成
        for feature in features[:self._config.max_bullet_points]:
            bullet_points.append(f"【特徴】{feature}")

        # 利点から追加
        for benefit in benefits[:self._config.max_bullet_points - len(bullet_points)]:
            bullet_points.append(f"【利点】{benefit}")

        # 不足分を補完
        if len(bullet_points) < self._config.max_bullet_points:
            bullet_points.append("【品質】高品質素材使用")

        return bullet_points[:self._config.max_bullet_points]

    async def _generate_description(
        self,
        product_info: dict[str, Any],
        keywords: list[str],
        platform: str,
    ) -> str:
        """説明文を生成."""
        if self._llm_client:
            prompt = f"""
商品情報: {product_info}
キーワード: {', '.join(keywords[:15])}

上記の情報に基づいて、魅力的な商品説明文を300-500文字で生成してください。
"""
            try:
                response = await self._llm_client.chat([
                    {"role": "user", "content": prompt}
                ])
                return response.get("content", "")
            except Exception as e:
                logger.warning("LLM説明生成エラー: %s", e)

        # フォールバック
        name = product_info.get("name", "この商品")
        features = product_info.get("features", [])
        description_parts = [
            f"{name}は、お客様のニーズに応える高品質な製品です。",
        ]
        for f in features[:3]:
            description_parts.append(f"・{f}")
        description_parts.append("ぜひお試しください。")

        return "\n".join(description_parts)

    def _generate_backend_keywords(self, keywords: list[str]) -> list[str]:
        """バックエンドキーワードを生成."""
        # プラットフォーム制限に合わせて調整
        backend = keywords[:50]  # Amazon制限に合わせる
        return backend

    def _calculate_seo_score(
        self,
        title: str,
        bullet_points: list[str],
        description: str,
        keywords: list[str],
    ) -> float:
        """SEOスコアを計算."""
        score = 0.0
        max_score = 100.0

        # タイトルにキーワードが含まれているか
        title_lower = title.lower()
        keyword_in_title = sum(1 for k in keywords[:5] if k in title_lower)
        score += keyword_in_title * 10  # 最大50点

        # 箇条書きの数
        score += min(len(bullet_points) * 5, 25)  # 最大25点

        # 説明文の長さ
        desc_len = len(description)
        if 300 <= desc_len <= 1000:
            score += 15
        elif desc_len > 100:
            score += 10

        # タイトルの長さ
        if 50 <= len(title) <= 150:
            score += 10

        return min(score / max_score, 1.0)
