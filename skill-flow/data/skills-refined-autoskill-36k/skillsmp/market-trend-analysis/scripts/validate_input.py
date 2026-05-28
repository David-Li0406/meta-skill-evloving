# -*- coding: utf-8 -*-
"""入力検証スクリプト - 確定性処理.

このスクリプトはLLM推論を使用せず、確定的に入力データを検証します。
Agent は「いつ実行するか」を判断し、このスクリプトは「どう実行するか」を担当。

使用例:
    >>> from agentflow.skills.builtin.market_trend_analysis.scripts.validate_input import (
    ...     validate_articles_input,
    ... )
    >>> result = validate_articles_input(input_data)
    >>> if not result.valid:
    ...     raise ValueError(result.errors)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class ValidationResult:
    """検証結果.

    Attributes:
        valid: 検証成功したか
        errors: エラーメッセージリスト
        warnings: 警告メッセージリスト
        normalized_data: 正規化されたデータ（検証成功時）
    """

    valid: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    normalized_data: dict[str, Any] | None = None


def validate_articles_input(input_data: dict[str, Any]) -> ValidationResult:
    """記事入力データを検証.

    Args:
        input_data: 入力データ辞書

    Returns:
        ValidationResult
    """
    result = ValidationResult()
    errors: list[str] = []
    warnings: list[str] = []

    # 必須フィールドチェック
    if "articles" not in input_data:
        errors.append("Missing required field: 'articles'")
        result.valid = False
        result.errors = errors
        return result

    articles = input_data.get("articles", [])

    # 型チェック
    if not isinstance(articles, list):
        errors.append("'articles' must be a list")
        result.valid = False
        result.errors = errors
        return result

    # 空チェック（警告のみ）
    if len(articles) == 0:
        warnings.append("Empty articles list - will return empty trends")

    # 各記事の検証
    normalized_articles: list[dict[str, Any]] = []
    for i, article in enumerate(articles):
        article_errors, normalized = _validate_article(article, i)
        errors.extend(article_errors)
        if normalized:
            normalized_articles.append(normalized)

    # analysis_options検証
    options = input_data.get("analysis_options", {})
    normalized_options = _normalize_options(options)

    if errors:
        result.valid = False
        result.errors = errors
        result.warnings = warnings
        return result

    result.valid = True
    result.warnings = warnings
    result.normalized_data = {
        "articles": normalized_articles,
        "analysis_options": normalized_options,
    }
    return result


def _validate_article(article: Any, index: int) -> tuple[list[str], dict[str, Any] | None]:
    """単一記事を検証.

    Args:
        article: 記事データ
        index: 配列インデックス

    Returns:
        (エラーリスト, 正規化データ)
    """
    errors: list[str] = []
    prefix = f"articles[{index}]"

    if not isinstance(article, dict):
        errors.append(f"{prefix}: must be an object")
        return errors, None

    # 必須フィールド
    required_fields = ["id", "title"]
    for field_name in required_fields:
        if field_name not in article:
            errors.append(f"{prefix}: missing required field '{field_name}'")

    if errors:
        return errors, None

    # 正規化
    normalized: dict[str, Any] = {
        "id": str(article.get("id", "")),
        "title": str(article.get("title", "")),
        "content": str(article.get("content", "")),
        "source": str(article.get("source", "unknown")),
        "keywords": article.get("keywords", []),
        "published_at": article.get("published_at", datetime.now().isoformat()),
    }

    return errors, normalized


def _normalize_options(options: dict[str, Any]) -> dict[str, Any]:
    """分析オプションを正規化.

    Args:
        options: オプション辞書

    Returns:
        正規化されたオプション
    """
    return {
        "enable_sentiment": bool(options.get("enable_sentiment", True)),
        "min_keyword_frequency": int(options.get("min_keyword_frequency", 2)),
        "top_trends_count": int(options.get("top_trends_count", 10)),
    }

