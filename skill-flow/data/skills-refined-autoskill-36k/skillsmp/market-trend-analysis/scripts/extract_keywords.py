# -*- coding: utf-8 -*-
"""キーワード抽出スクリプト - 確定性処理.

このスクリプトはLLM推論を使用せず、確定的にキーワードを抽出します。
簡易的な形態素解析とTF-IDF相当の処理を実行。

使用例:
    >>> from agentflow.skills.builtin.market_trend_analysis.scripts.extract_keywords import (
    ...     extract_keywords_from_articles,
    ... )
    >>> result = extract_keywords_from_articles(articles, min_frequency=2)
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Any


@dataclass
class KeywordExtractionResult:
    """キーワード抽出結果.

    Attributes:
        keywords: キーワードと出現回数のマップ
        top_keywords: 上位キーワードリスト
        total_words: 総単語数
    """

    keywords: dict[str, int] = field(default_factory=dict)
    top_keywords: list[str] = field(default_factory=list)
    total_words: int = 0


# 除外する一般的な単語（ストップワード）
STOP_WORDS = frozenset([
    # 英語
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "must", "shall", "can", "need", "dare",
    "to", "of", "in", "for", "on", "with", "at", "by", "from", "as",
    "into", "through", "during", "before", "after", "above", "below",
    "between", "under", "again", "further", "then", "once", "and", "but",
    "or", "nor", "so", "yet", "both", "either", "neither", "not", "only",
    "own", "same", "than", "too", "very", "just", "also", "now", "here",
    "there", "when", "where", "why", "how", "all", "each", "every", "both",
    "few", "more", "most", "other", "some", "such", "no", "any", "this",
    "that", "these", "those", "what", "which", "who", "whom", "whose",
    # 日本語（簡易）
    "の", "に", "は", "を", "た", "が", "で", "て", "と", "し", "れ",
    "さ", "ある", "いる", "する", "こと", "これ", "それ", "ため", "など",
])

# 技術キーワードの重み付け
TECH_KEYWORDS_BOOST = frozenset([
    "cobol", "java", "python", "ai", "ml", "llm", "migration", "legacy",
    "modernization", "cloud", "api", "microservice", "devops", "kubernetes",
    "docker", "serverless", "aws", "azure", "gcp", "transformation",
    "automation", "integration", "architecture", "framework", "platform",
])


def extract_keywords_from_articles(
    input_data: dict[str, Any] | list[dict[str, Any]],
    *,
    min_frequency: int | None = None,
    top_n: int | None = None,
) -> KeywordExtractionResult:
    """記事群からキーワードを抽出.

    Args:
        input_data: 入力データ辞書（articles, min_frequency, top_n）またはarticlesリスト
        min_frequency: 最小出現回数（input_data内で指定可能）
        top_n: 上位N件を返す（input_data内で指定可能）

    Returns:
        KeywordExtractionResult
    """
    # 入力データの正規化
    if isinstance(input_data, dict):
        articles = input_data.get("articles", [])
        min_frequency = min_frequency or input_data.get("min_frequency", 2)
        top_n = top_n or input_data.get("top_n", 50)
    else:
        articles = input_data
        min_frequency = min_frequency or 2
        top_n = top_n or 50
    all_words: list[str] = []

    for article in articles:
        # タイトルと本文からテキスト抽出
        title = str(article.get("title", ""))
        content = str(article.get("content", ""))
        existing_keywords = article.get("keywords", [])

        # 既存キーワードは重み2倍
        all_words.extend(existing_keywords)
        all_words.extend(existing_keywords)

        # テキストからトークン抽出
        text = f"{title} {content}"
        tokens = _tokenize(text)
        all_words.extend(tokens)

    # カウント
    word_counts = Counter(all_words)

    # フィルタリング
    filtered: dict[str, int] = {}
    for word, count in word_counts.items():
        # 最小頻度チェック
        if count < min_frequency:
            continue
        # ストップワード除外
        if word.lower() in STOP_WORDS:
            continue
        # 短すぎる単語除外
        if len(word) < 2:
            continue

        # 技術キーワードは重み付け
        if word.lower() in TECH_KEYWORDS_BOOST:
            count = int(count * 1.5)

        filtered[word] = count

    # ソート
    sorted_keywords = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
    top_keywords = [kw for kw, _ in sorted_keywords[:top_n]]

    return KeywordExtractionResult(
        keywords=filtered,
        top_keywords=top_keywords,
        total_words=len(all_words),
    )


def _tokenize(text: str) -> list[str]:
    """テキストをトークン化（簡易版）.

    Args:
        text: 入力テキスト

    Returns:
        トークンリスト
    """
    # 英数字とハイフンのみ残す
    text = re.sub(r"[^\w\s\-]", " ", text)
    # 連続空白を正規化
    text = re.sub(r"\s+", " ", text)
    # 分割
    tokens = text.strip().lower().split()
    return tokens

