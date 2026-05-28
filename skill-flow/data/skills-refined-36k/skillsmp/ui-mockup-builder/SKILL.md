---
name: ui-mockup-builder
description: >
  Web/アプリの「画面モックアップ(UI Mockup / high-fidelity mockup)」を作成するためのSkill。
  依頼に「モックアップ」「UIデザイン」「見た目を最終に寄せたい」「開発に渡せる画面デザイン」「Figmaに起こす前の叩き」「画面ごとの状態(空/エラー/ローディング等)込みで作りたい」
  などが含まれるときに発動する。
  目的に応じて wireframe / mockup / prototype のどれが必要かをまず判定し、モックアップが適切なら
  画面ごとの静的な高フィデリティ設計(色/タイポ/余白/コンポーネント/状態)と、開発引き渡し用の注釈・仕様をまとめた「Mockup Pack」をリポジトリ内に生成する。
---

# UI Mockup Builder

画面モックアップは、最終プロダクトに近い「見た目」を具体化する静的な設計図(高フィデリティ)です。

## Purpose
- 合意形成を早く・安く、実装前に見た目の地雷を潰す
- 開発引き渡しを滑らかにする
- 静的画だけで誤解される「状態」を先に明確にする

## Output (default)
リポジトリに「Mockup Pack(モックアップ一式)」を作成します。Figma自体の操作はせず、**Figmaに起こせる粒度の仕様**と、必要なら**HTML/Tailwindで再現できる静的モック**を生成します。

推奨の出力先:
- `docs/mockups/<feature-or-epic>/`
  - `README.md`(目的・前提・対象画面・参照・決定事項)
  - `style-guide.md`(色/タイポ/余白/角丸/影/アイコン方針)
  - `tokens.json`(色・スペーシング・タイポなどのトークン)
  - `screens/`
    - `<screen-id>__spec.md`(画面仕様)
  - `components/`
    - `<component-id>__spec.md`(コンポーネント仕様)
  - `copy/`
    - `strings.md`(文言案、i18n注意、可変長対策)
  - `state-matrix.md`(主要状態一覧)
  - `html/`(任意:静的HTMLモック)
  - `exports/`(任意:スクリーンショット、PNG出力物など)

## Operating Principles
1. **最初にWireframe/Mockup/Prototypeを判定**:早期にフィデリティを間違えない
2. **既存資産を最優先**:デザインシステム/トークン/コンポーネントがあれば必ず寄せる
3. **状態を先に潰す**:通常/空/ローディング/エラー/成功を最低限揃える
4. **作り込みすぎない**:目的に対して過剰なフィデリティは避ける
5. **実データで検証**:ダミーテキストでなく、実データ寄りで桁・改行・i18nを確認

## Workflow

### Step 0: Activation check(最初に必ずやる判定)
1. 依頼が「ワイヤー」「モック」「プロトタイプ」のどれかを判定する
   - **Wireframe**:構造・情報設計・導線のラフ(未完成に見せて議論をロジックに寄せる)
   - **Mockup**:見た目を最終に寄せた静的画(色/タイポ/余白/コンポーネント/状態)
   - **Prototype**:遷移や操作感の検証(インタラクティブ)
2. モックアップが適切なら、このSkillを続行
3. ワイヤーが先なら「まずワイヤー→確定後にモックアップ」の順に提案し、同じフォルダに段階成果物として残す

### Step 1: Repo scan(既存資産の確認)
- 既存のデザインシステム/UIライブラリ/トークンがあれば最優先で寄せる
  - 例:`design/`, `docs/design-system/`, `tokens/`, `tailwind.config.*`, `shadcn/ui`, `MUI`, `Chakra`, `Ant` 等
- 既存の画面遷移図/PRD/要件/ユーザーフローがあれば読み、画面一覧を確定する

### Step 2: Minimal questions(不足があるときの最小ヒアリング)
- `resources/intake_questions.md` を参照し、足りない情報だけを質問する
- ユーザーに確認するのは「作るために絶対必要」なものだけ
- なければ仮定して進め、仮定はREADMEに明記

### Step 3: Foundation(見た目の土台を決める)
- `resources/style_guide_template.md` と `tokens.json` を作る(既存があれば拡張・補完のみ)
- タイポ/カラー/レイアウト/コンポーネント方針を決定

### Step 4: Screen-by-screen mockup spec(画面ごとに静的モック仕様を作る)
- 各画面 `screens/<screen>__spec.md` を作成
- `resources/screen_spec_template.md` をベースに仕様を埋める
- 画面の目的/レイアウト/コンポーネント/表示データ/状態/注釈を必ず含める

### Step 5: Components(ズレを防ぐためにコンポーネントを先に固める)
- 新規コンポーネントが必要なら `components/<component>__spec.md` を作る
- `resources/component_spec_template.md` をベースに作成
- variants / states / props を明確にし、画面間で使い回せる前提にする

### Step 6: State matrix(例外や落とし穴を先に潰す)
- `state-matrix.md` に「画面×状態」を表でまとめる
- 最低限:空(0件)/ローディング/エラー/成功/無効

### Step 7: Optional HTML mock(必要な場合だけ)
- 開発側との合意形成やレビュー効率のために、静的HTMLで見た目を再現する(任意)
- ルール:**動的ロジックは作らない**(見た目と状態だけ)
- Tailwind等があるならそれに寄せる

### Step 8: Handoff pack(開発引き渡しの不足情報を埋める)
- `README.md` に以下をまとめる
  - 対象画面一覧、到達条件(権限/ルート)
  - 画面ごとの仕様ファイルへのリンク
  - 未確定事項(要確認)と暫定仮定
  - 重要なデザイン判断

### Step 9: Quality check(品質チェック)
- `resources/quality_checklist.md` で自己レビューし、問題があれば修正
- 特に以下を重点確認:
  - 目的に対してフィデリティが適切
  - 静的画で誤解される「状態」が揃っている
  - 実データ寄りの内容で崩れ検証している
  - レスポンシブとアクセシビリティを意識している
  - コンポーネント/トークンに寄せて、画面ごとのズレが生まれない

## Formatting Rules
- Markdownを基本にし、読みやすさ優先
- テーブル、箇条書き、画像リンクを活用
- 重要な判断は太字、参照はリンク
- コード例はシンタックスハイライト付き

## Examples (triggers)
- 「この機能の画面モックアップ作って。開発に渡せる状態(空・エラー・ローディング込み)で」
- 「Figmaに起こす前に、画面の見た目を最終に寄せたモック仕様をMarkdownで作りたい」
- 「この画面群、ブランドカラーとタイポまで決めた高フィデリティの静的デザインが欲しい」
- 「UI mockupを作って」
- 「画面デザインの状態パターンも含めて設計書を作って」

## References
- https://www.figma.com/resource-library/wireframe-vs-mockup/
- https://www.interaction-design.org/literature/topics/mockups
- https://balsamiq.com/blog/wireframe-vs-mockup-vs-prototype/
- https://www.aha.io/roadmapping/guide/product-management/wireframe-mockup-prototype
- https://www.nngroup.com/articles/ux-prototype-hi-lo-fidelity/
