---
name: market-trend-analysis
description: |
  市場動向分析Skill。ニュース・技術記事からトレンド抽出、キーワード分析、センチメント評価を実行。
  COBOL→Java移行、AI技術動向、業界トレンド監視に使用。
version: 1.0.0
author: AgentFlow Team
owner: market-intelligence
tags:
  - trend-analysis
  - market-intelligence
  - news-analysis
  - sentiment
  - core-skill
triggers:
  - market trend
  - トレンド分析
  - 市場動向
  - trend analysis
  - ニュース分析
  - 技術トレンド
  - sentiment
  - センチメント
  - キーワード抽出
requirements:
  - openai>=1.0.0
  - httpx>=0.25.0
dependencies: []
examples:
  - "COBOL移行の市場トレンドを分析"
  - "AI関連ニュースからトレンド抽出"
  - "技術キーワードのセンチメント分析"
acceptance_criteria:
  - trends配列が存在すること
  - 各trendにtopic, score, sentiment, growth_rateが含まれること
  - 入力articles数 > 0 の場合、trends数 >= 1
  - スコアは0.0-1.0の範囲内
---

# Market Trend Analysis Skill

## 概要

市場動向を自動分析するためのSkillです。収集されたニュース・技術記事を入力として、
トレンドトピック、キーワード頻度、センチメント（感情）を抽出します。

## 入力仕様

```json
{
  "articles": [
    {
      "id": "string",
      "title": "string",
      "content": "string",
      "source": "news|github|arxiv|rss",
      "published_at": "ISO8601",
      "keywords": ["string"]
    }
  ],
  "analysis_options": {
    "enable_sentiment": true,
    "min_keyword_frequency": 2,
    "top_trends_count": 10
  }
}
```

## 出力仕様

```json
{
  "trends": [
    {
      "topic": "string",
      "score": 0.0-1.0,
      "sentiment": "positive|negative|neutral",
      "growth_rate": -1.0 to 1.0,
      "keywords": ["string"],
      "articles_count": number
    }
  ],
  "summary": "string",
  "metadata": {
    "analysis_timestamp": "ISO8601",
    "total_articles_analyzed": number
  }
}
```

## 処理フロー

1. **入力検証** → `scripts/validate_input.py`
2. **キーワード抽出** → `scripts/extract_keywords.py`
3. **トレンドスコア計算** → LLM推論
4. **センチメント分析** → LLM推論（オプション）
5. **レポート骨格生成** → `scripts/generate_report_skeleton.py`

## 確定性処理（スクリプト化）

以下の処理はLLM推論を使用せず、確定的に実行：

| 処理 | スクリプト | 説明 |
|------|----------|------|
| 入力検証 | `validate_input.py` | JSON Schema検証 |
| キーワード抽出 | `extract_keywords.py` | 形態素解析ベース |
| 骨格生成 | `generate_report_skeleton.py` | テンプレート適用 |

## 境界条件

- 記事数 0 件 → 空のtrends配列を返却
- 記事数 > 1000 件 → バッチ処理（100件単位）
- キーワード抽出失敗 → タイトルからフォールバック

## 参照資料

詳細なSOPは `references/trend_analysis_sop.md` を参照。

