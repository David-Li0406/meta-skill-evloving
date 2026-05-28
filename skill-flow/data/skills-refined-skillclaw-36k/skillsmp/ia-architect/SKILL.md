---
name: ia-architect
description: >
  情報設計（Information Architecture / IA）を「設計」し、設計が妥当かを「検証（監査）」するためのClaude Code Skill。
  対象プロダクト/サイト/アプリの情報を、ユーザーが理解できる形で到達できるように構造化（分類・階層・メタデータ・命名）し、
  辿れる導線（ナビ）と探せる仕組み（検索）まで含めて設計する。
  さらにカードソート/ツリーテスト等の検証設計と、IA品質チェック（Findable/Understandable、スケール、命名一貫性）を行い、
  改善案と改訂版IA成果物を出力する。
  トリガー例: 情報設計/IA/サイトマップ/ナビ/カテゴリ/タクソノミー/メタデータ/ラベリング/検索/ファセット/ツリーテスト/カードソート
---

# IA Architect — 情報設計の作成と検証

## 目的
- ユーザーが目的の情報に「理解できる形で」到達できるように、情報を構造化し、分類し、命名し、辿れる導線（ナビ）と探せる仕組み（検索）を設計する。
  参考: [IAは「人が理解し、探し物を見つけられる」ための設計](https://www.iainstitute.org/sites/default/files/what_is_ia.pdf) / [IAは findable / understandable を目的](https://www.interaction-design.org/literature/topics/information-architecture)
- 設計したIAが妥当かを、チェックリスト + スコアカード + 検証計画（カードソート/ツリーテスト）で監査し、改善ループを回す。

## 重要な原則（必ず守る）
1. **IA（情報の背骨）とナビ（UIの移動手段）を混同しない**
   参考: [IAは"information backbone"、ナビはUI要素](https://www.nngroup.com/articles/ia-vs-navigation/)
2. **分類は社内都合ではなくユーザーのタスク中心で設計する**（Top tasks起点）
3. **ラベル（命名）は辞書化し、一貫性を守る**（同義語・表記揺れ・略語ルール込み）
4. **スケールする構造にする**（階層 + メタデータ / タグ / 属性。カテゴリ一本道依存を避ける）
5. **想像で決めず検証する**（カードソート、ツリーテスト）
   参考: [カードソート定義](https://www.nngroup.com/articles/card-sorting-definition/) / [ツリーテスト概要](https://www.optimalworkshop.com/101-guides/information-architecture-101/tree-testing-and-information-architecture)

---

## このSkillの対応モード
- **Mode A: IAを設計する（Design）**
- **Mode B: IAを検証する（Audit / Review）**
- **Mode C: 設計→検証→改訂（Iterate）**（基本はこれ）

ユーザーが明示しない場合は **Mode C** として扱う。

---

## 入力（足りない場合は、分かる範囲で仮置きして進める）
優先度順。リポジトリ/ドキュメントがあれば読み取り優先。

1. 対象範囲（どの情報空間か）・制約（権限、運用、検索の有無、CMS/DBなど）
2. 主要ユーザーと主要タスク（Top tasks仮説でOK）
3. 現状の構造（画面一覧、メニュー、サイトマップ、URL、カテゴリ、タグ、検索UI）
4. コンテンツ一覧（なければ代表コンテンツ10〜30件でもOK）
5. 既存データ（検索ログ、問い合わせ、ゼロ件検索、回遊データ等）があれば最優先で取り込む

---

## 実行手順（Design）
### Step 0. IAブリーフ（目的・スコープ・成功指標）
- resources/ia-brief-template.md に沿ってブリーフを作る
- 成功指標は最低1つは置く（例: 目的到達率、探索時間、ゼロ件検索率）

### Step 1. ユーザー理解（タスク・探し方・用語）
- Top tasks（主要タスク）を5〜15件に収束
- 探し方タイプ（検索派/回遊派/フィルタ派）を仮説化
- 用語候補（現場用語・俗称・同義語）を収集し、後で用語集に統合

### Step 2. コンテンツ棚卸し（Inventory & Audit）
- コンテンツインベントリ（最小でも: タイトル/種類/目的/所有者/更新頻度/品質/現行の置き場所）
- 監査ラベル（残す/統合/削除/作り直し）と、ギャップ（必要だが無い）を出す

### Step 3. 構造設計（分類・階層・メタデータ・関係）
- **タクソノミー（カテゴリ体系）**を提案（ユーザータスク起点）
- **メタデータ（属性）**を定義（必須/任意、入力ルール、同義語、正規化）
- **コンテンツモデル**（タイプと関係）を図または表で定義（例: 作品→話数→カット→素材）

### Step 4. ナビゲーション設計（辿れる導線）
- グローバル/ローカル/パンくずの方針
- サイトマップ（IAの可視化として作る。IAそのものと混同しない）
  参考: [IAとサイトマップの違い](https://www.nngroup.com/articles/information-architecture-sitemaps/)

### Step 5. ラベリング（命名）設計
- 用語集（ラベル辞書）を作る（同義語・表記揺れ・略語・禁則）
- メニュー名/カテゴリ名/フィルタ名/ボタン文言まで射程に含める

### Step 6. 検索・絞り込み（Findability）設計
- 検索対象フィールド、同義語、最低限のランキング方針
- ファセット（絞り込み）一覧、優先順、組み合わせ制約
  参考: [IAの主要構成要素に Search が含まれる](https://baymard.com/learn/information-architecture-ux)

### Step 7. 検証計画（カードソート / ツリーテスト）
- resources/card-sort-plan.md / resources/tree-test-plan.md で計画を作成
- 可能なら、想定タスク別に「正解ルート」と「迷いやすい分岐」を明示

### Step 8. 実装・運用（ガバナンス）
- IA仕様として統合（構造/ラベル/メタデータ/検索）
- 追加/変更時のレビュー責任、変更基準、計測（ゼロ件率など）

---

## 実行手順（Audit / Review）
### 1) 成果物を収集
- 既存のサイトマップ、メニュー、カテゴリ、タグ、検索UI、URL、コンテンツ一覧、用語集を収集
- なければ、画面キャプチャやルーティング一覧から推定してでも作る

### 2) チェック（致命度つき）
- resources/ia-audit-checklist.md を使って **Fail / Risk / OK** 判定
- resources/ia-audit-scorecard.md で **0〜2点**採点し、合計と優先度を出す

### 3) 改善案（必ず「具体」まで落とす）
- 「問題 → 影響 → 原因 → 修正案 → 代替案（あれば） → 期待効果 → 検証方法」
- 改訂版の **サイトマップ / タクソノミー / メタデータ / 用語集 / 検索・ファセット** を提示

---

## 出力形式（必須）
最終的に、resources/ia-design-output-template.md の構成で出力すること。

- IAブリーフ
- Top tasks / ユースケース
- コンテンツインベントリ（最小版でも可）
- タクソノミー（カテゴリ体系）
- メタデータ定義（表）
- コンテンツモデル（表 or 図）
- サイトマップ（ツリー）
- ナビ構造（グロ/ローカル/パンくず）
- 用語集（ラベル辞書）
- 検索要件 & ファセット設計
- 検証計画（カードソート / ツリーテスト）
- IA仕様（運用・変更管理）

---

## 例（このSkillが発動すべき依頼）
- 「このSaaSの情報設計を作って。検索とフィルタも含めて」
- 「今のメニュー構造がぐちゃぐちゃなのでIA監査して、直し案出して」
- 「サイトマップはあるけど、findabilityが低い気がする。ツリーテスト計画も作って」
- 「用語が揺れているので、ラベル辞書と命名ガイド作って」

---

## References
- [Information Architecture Institute: "What is IA?" (PDF)](https://www.iainstitute.org/sites/default/files/what_is_ia.pdf)
- [Interaction Design Foundation: Information Architecture](https://www.interaction-design.org/literature/topics/information-architecture)
- [NN/g: The Difference Between IA and Navigation](https://www.nngroup.com/articles/ia-vs-navigation/)
- [NN/g: IA vs. Sitemaps](https://www.nngroup.com/articles/information-architecture-sitemaps/)
- [Baymard: A Guide to Information Architecture UX](https://baymard.com/learn/information-architecture-ux)
- [NN/g: Card Sorting](https://www.nngroup.com/articles/card-sorting-definition/)
- [Optimal Workshop: Tree testing and IA](https://www.optimalworkshop.com/101-guides/information-architecture-101/tree-testing-and-information-architecture)
