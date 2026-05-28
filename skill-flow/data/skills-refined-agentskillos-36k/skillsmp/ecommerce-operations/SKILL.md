---
name: ecommerce-operations
description: 跨境電商運営のための包括的なスキルセット。競品採集、価格分析、Listing生成、在庫調整、広告監視、日報生成を提供。
version: "1.0.0"
triggers:
  - 競品
  - 価格分析
  - listing
  - 在庫
  - 広告
  - EC運営
  - 電商
requirements:
  - httpx
  - pydantic
tags:
  - ecommerce
  - cross-border
  - automation
---

# 跨境電商運営スキルパッケージ

## 概要

このスキルパッケージは、跨境電商運営に必要な一連の作業を自動化します。

## 含まれるスキル

### 1. CompetitorScraper（競品採集）
ECプラットフォームから競合商品の情報を収集します。

```python
from agentflow.skills.builtin.ecommerce import CompetitorScraper

scraper = CompetitorScraper()
products = await scraper.scrape_competitors(
    keywords=["wireless earbuds"],
    platforms=["amazon", "ebay"],
    max_results=50,
)
```

**対応プラットフォーム**:
- Amazon
- eBay
- AliExpress
- Shopify
- 楽天

### 2. PriceAnalyzer（価格分析）
競合商品の価格を分析し、最適な価格戦略を提案します。

```python
from agentflow.skills.builtin.ecommerce import PriceAnalyzer

analyzer = PriceAnalyzer(target_margin=0.3)
analysis = await analyzer.analyze(price_points=products)
```

**出力**:
- 平均/中央値/最小/最大価格
- 推奨価格
- 価格戦略（浸透、競争、プレミアム等）
- 市場ポジション分析

### 3. ListingGenerator（Listing生成）
SEO最適化された商品リスティングを生成します。

```python
from agentflow.skills.builtin.ecommerce import ListingGenerator

generator = ListingGenerator(llm_client=llm)
listing = await generator.generate(
    product_info={"name": "...", "features": [...]},
    competitor_data=analysis,
    target_platform="amazon",
)
```

**出力**:
- 最適化されたタイトル
- 箇条書きポイント
- 商品説明
- バックエンドキーワード
- SEOスコア

### 4. InventoryAdjuster（在庫・価格調整）
市場分析に基づいて在庫と価格を調整します。

```python
from agentflow.skills.builtin.ecommerce import InventoryAdjuster

adjuster = InventoryAdjuster()
plan = await adjuster.create_adjustment_plan(
    current_inventory={"sku1": 100},
    current_prices={"sku1": 29.99},
    price_analysis=analysis,
)
```

**出力**:
- 調整アイテムリスト
- 緊急度レベル
- 推奨アクション
- 収益/コスト影響予測

### 5. AdMonitor（広告監視）
広告キャンペーンのパフォーマンスを監視します。

```python
from agentflow.skills.builtin.ecommerce import AdMonitor

monitor = AdMonitor()
analysis = await monitor.analyze_campaigns(
    campaigns=[{"id": "camp1", "spend": 1000, ...}],
    time_range="7d",
)
```

**出力**:
- キャンペーン別パフォーマンス
- CTR/CVR/CPA/ROAS
- アラート
- 最適化提案

### 6. DailyReportGenerator（日報生成）
毎日の運営データを集約してレポートを生成します。

```python
from agentflow.skills.builtin.ecommerce import DailyReportGenerator

generator = DailyReportGenerator()
report = await generator.generate(
    sales_data=sales,
    ad_data=ad_performance,
    inventory_data=inventory,
)
```

**出力**:
- エグゼクティブサマリー
- 売上/広告/在庫セクション
- アクションアイテム
- Markdown/HTML/JSON形式

## ワークフロー

```
競品採集 → 価格分析 → Listing生成 → 在庫調整 → 広告監視 → 日報生成
    ↓         ↓          ↓           ↓          ↓          ↓
  商品情報   価格戦略   最適化Listing  調整計画   アラート    レポート
```

## 統合例

```python
from agentflow.skills.builtin.ecommerce import (
    CompetitorScraper,
    PriceAnalyzer,
    ListingGenerator,
)

# 1. 競品採集
scraper = CompetitorScraper()
products = await scraper.run({
    "keywords": ["wireless earbuds"],
    "platforms": ["amazon"],
})

# 2. 価格分析
analyzer = PriceAnalyzer()
analysis = await analyzer.run({
    "products": products["products"],
})

# 3. Listing生成
generator = ListingGenerator(llm_client=llm)
listing = await generator.run({
    "product_info": {"name": "Premium Wireless Earbuds", ...},
    "competitor_data": analysis,
})
```

## 注意事項

- スクレイピングは各プラットフォームの利用規約に従ってください
- レート制限を守るため、適切な間隔を設けてください
- 実際の商用利用前に法的確認を行ってください
