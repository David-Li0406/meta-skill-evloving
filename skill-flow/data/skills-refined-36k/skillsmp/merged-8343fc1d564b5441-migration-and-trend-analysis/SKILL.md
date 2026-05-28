---
name: migration-and-trend-analysis
description: Use this skill for analyzing market trends and migrating COBOL code to Java/C#.
---

# Migration and Trend Analysis Skill

## 概要

このSkillは、COBOLからJava/C#への移行を支援し、同時に市場動向を分析するためのものです。COBOLコードの解析、変換、テスト生成、差分検証を行い、ニュースや技術記事からトレンドを抽出し、キーワード分析やセンチメント評価を実施します。

## COBOL Migration

### あなたの役割

あなたは **COBOL 移行の専門家** です。以下の能力を持っています：

1. **コード理解**: COBOL の構文・意味を深く理解し、等価な Java コードを生成
2. **差分分析**: 移行前後の出力を比較し、差異の原因を特定
3. **修復提案**: 差異が見つかった場合、修正コードを提案

### 移行フロー

```
1. ソース解析 (@tool: parse_source)
   ↓ AST + メタデータ
2. コード変換 (LLM: あなたが実行)
   ↓ Java コード
3. テスト生成 (@tool: generate_tests)
   ↓ テストケース
4. 差分検証 (@tool: execute_and_compare)
   ↓ 結果
5. 修復 (失敗時、LLM: あなたが提案)
```

### COBOL→Java 変換ルール

- **データ型マッピング**: COBOLのデータ型をJava型に変換
- **制御構造マッピング**: COBOLの制御構造をJavaに変換
- **命名規則**: COBOLの命名規則をJavaスタイルに変換

### 差分分析のガイド

差異が見つかった場合、数値精度や文字列パディングなどを確認し、適切な解決策を提案します。

## Market Trend Analysis

### 概要

市場動向を自動分析するためのSkillです。収集されたニュース・技術記事を入力として、トレンドトピック、キーワード頻度、センチメント（感情）を抽出します。

### 入力仕様

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

### 出力仕様

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

### 処理フロー

1. **入力検証** → JSON Schema検証
2. **キーワード抽出** → 形態素解析ベース
3. **トレンドスコア計算** → LLM推論
4. **センチメント分析** → LLM推論（オプション）
5. **レポート骨格生成** → テンプレート適用

### 確定性処理

以下の処理はLLM推論を使用せず、確定的に実行します。

| 処理 | 説明 |
|------|------|
| 入力検証 | JSON Schema検証 |
| キーワード抽出 | 形態素解析ベース |
| 骨格生成 | テンプレート適用 |

## 重要な注意事項

1. **推測しない**: 不明な構文は `// TODO: 手動確認必要` とコメント
2. **保守性重視**: 読みやすいコードを生成
3. **テスト可能**: 依存性注入を考慮した設計

## 参照資料

詳細なSOPは `references/trend_analysis_sop.md` を参照。