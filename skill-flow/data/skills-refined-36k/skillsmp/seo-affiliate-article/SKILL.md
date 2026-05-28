---
name: seo-affiliate-article
description: 'SEO対策されたアフィリエイト記事（製品レビュー、まとめ記事、比較記事）をMDX形式で作成する。AffiliateCardコンポーネント、E-E-A-T準拠、長尾キーワードH2見出し、内部リンク戦略を含む。Use when: (1) 製品レビュー記事を書く, (2) ベストバイ・おすすめ○選記事を書く, (3) 製品比較記事を書く, (4) アフィリエイトリンク付き記事を作成する'
---

# SEO Affiliate Article

日本語テック・ガジェットブログ向けのSEO最適化アフィリエイト記事作成スキル。

## ワークフロー

```text
1. 記事タイプ決定 → 2. 情報収集・検証 → 3. 構成設計 → 4. 執筆 → 5. SEO/品質チェック → 6. 公開
```

## Step 1: 記事タイプの決定

| タイプ       | 用途                 | 例                         |
| :----------- | :------------------- | :------------------------- |
| 単品レビュー | 1製品の詳細レビュー  | 「Dell U4025QW レビュー」  |
| まとめ記事   | 複数製品のランキング | 「買ってよかったもの5選」  |
| 比較記事     | 2-3製品の比較        | 「MX Master 3 vs MX Ergo」 |

詳細テンプレートは `references/article-templates.md` を参照。

## Step 2: 情報収集と検証

### ハルシネーション防止

**必須確認項目:**

- 受賞歴（VGP, iF Design Award等）→ 公式サイトで確認
- スペック数値 → メーカー公式ページで確認
- 価格 → Amazon/楽天の現在価格を確認

**検証方法:**

```text
WebSearch: "[製品名] [確認したい情報]"
```

### ASIN取得

AffiliateCardに必要なASINをAmazon商品ページから取得:

```text
WebSearch: "[製品名] Amazon ASIN"
または商品URLから: amazon.co.jp/dp/[ASIN]
```

## Step 3: 構成設計

### SEO最適化H2見出し

**悪い例:** `## スペック`
**良い例:** `## Dell U4025QW スペック｜5K2K解像度と120Hz対応`

**パターン:**

- `[製品名] レビュー｜[特徴キーワード]`
- `[製品名] [機能]｜[ベネフィット]`
- `[製品カテゴリ] おすすめポイント｜[差別化要素]`

### 内部リンク戦略

記事内で関連する既存記事へリンク:

```markdown
[KANADEMONOのデスク](/blog/2023/kanademono-desk-review)と組み合わせて使用しています。
```

## Step 4: 執筆

### 文体ルール

- **丁寧語（です・ます調）** を一貫使用
- 一人称は「僕」
- 冗長表現を避け簡潔に

### AffiliateCard使用法

```mdx
import AffiliateCard from '@/components/AffiliateCard.astro';

<AffiliateCard
  title="製品名"
  description="製品の特徴（50-80文字）"
  amazon={{ asin: 'B0XXXXXXXX', price: '¥XX,XXX' }}
/>
```

### E-E-A-T準拠

必須要素:

- **Experience**: 使用期間を明記（例: 「7ヶ月使用」）
- **Expertise**: 具体的な使用シーン
- **Authoritativeness**: 受賞歴・第三者評価への言及
- **Trustworthiness**: デメリットも正直に記載

詳細は `references/eeat-checklist.md` を参照。

### 表形式

スペック・比較には表を使用:

```markdown
| 項目 |      値 |
| :--- | ------: |
| 価格 | ¥19,800 |
```

## Step 5: 品質チェック

### SEOチェックリスト

- [ ] タイトルに主要キーワード含む（60文字以内）
- [ ] H2見出しにロングテールキーワード
- [ ] meta description にキーワード（120文字以内）
- [ ] 内部リンク 2本以上
- [ ] 画像altに説明文

### コンテンツチェック

- [ ] ハルシネーションなし（情報源確認済み）
- [ ] デメリット・注意点を記載
- [ ] 使用期間を明記
- [ ] 価格情報が最新

### 技術チェック

- [ ] `pnpm build` 成功
- [ ] AffiliateCard ASIN正確
- [ ] markdownlint エラーなし

## Step 6: 公開

```bash
git add .
git commit -m "feat: add [記事タイトル]"
git push
gh pr create
```
