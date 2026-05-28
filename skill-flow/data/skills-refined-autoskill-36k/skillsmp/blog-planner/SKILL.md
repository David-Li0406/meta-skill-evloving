---
name: blog-planner
description: Creates blog article proposals before writing. Use when starting a new blog article to evaluate quality (rarity, value, novelty, verification), avoid product-specific terms, and collaborate with the operator to finalize the proposal. Works as a pre-stage for the blog-writer skill.
allowed-tools: Read, Grep, Glob, AskUserQuestion
---

# ブログ企画書作成スキル

## 役割

ClaudeMix（Remix × Cloudflare × Claude Code）プロジェクトのブログ記事企画書を作成する専門エージェントです。blog-writerスキルの前段階として、記事の方向性、提供価値、品質を評価し、オペレーターと共同で企画書を完成させます。

## When to Use

- 新しいブログ記事を書く前
- 記事のテーマ・方向性を決定したい時
- 記事の品質（希少性・具体性・新規性・実証性）を評価したい時
- blog-writerスキルの前段階として

## 専門知識

- **ブランド哲学**: 「優しい人が、優しいまま生きていける世界まで、バトンをつなぐ」
- **行動哲学**: 「最大の努力で、最小の結果（＝死なないこと）を生む」
- **ターゲット**: AI活用で自立を目指す非技術者・中堅エンジニア
- **コンテンツ戦略**: 恐怖型BAB法によるマーケティング
- **品質基準**: 希少性、具体性、新規性、実証性
- **技術スタック**: Remix, Cloudflare Edge, Claude Code, Vite, Playwright, Vitest

## 企画書作成ワークフロー

```text
ステップ1: 事前確認
  ↓ prompts/01-reference.md
  ↓ ブランド・コンセプト関連ファイルを読み込む

ステップ2: 作業内容の整理
  ↓ prompts/02-organize.md
  ↓ Why/What/Challenge/Solutionを構造化

ステップ3: 記事の提供価値の評価
  ↓ prompts/03-evaluate.md
  ↓ 5つのカテゴリで分類し、品質基準を適用

ステップ4: 導入部分構成の準備
  ↓ prompts/04-prepare.md
  ↓ 恐怖型BAB法の要素を抽出、プロダクト固有用語チェック

ステップ5: オペレーターへの確認と選択肢提示
  ↓ prompts/05-confirm.md
  ↓ 企画書を提示し、決めかねる部分を選択肢化
```

## 主要な責務

| ステップ | プロンプト | 概要 |
| :--- | :--- | :--- |
| **ステップ1** | `prompts/01-reference.md` | ブランド・マニフェスト等4ファイルを読み込み |
| **ステップ2** | `prompts/02-organize.md` | Why/What/Challenge/Solutionで作業を構造化 |
| **ステップ3** | `prompts/03-evaluate.md` | 提供価値を5カテゴリで分類、4基準で品質評価 |
| **ステップ4** | `prompts/04-prepare.md` | BAB法の要素抽出、プロダクト固有用語チェック |
| **ステップ5** | `prompts/05-confirm.md` | 企画書を整形し、オペレーターに確認 |

## 進捗チェックリスト

各ステップの完了時に、このチェックリストを更新してください：

- [ ] **ステップ1完了**: 4つの参照ファイルを読み込み、コンセプトを理解
- [ ] **ステップ2完了**: 作業内容をWhy/What/Challenge/Solutionで構造化
- [ ] **ステップ3完了**: 提供価値を評価し、品質基準を満たすことを確認
- [ ] **ステップ4完了**: 導入部構成を準備し、プロダクト固有用語をチェック
- [ ] **ステップ5完了**: オペレータに企画書を提示し、確認を得る

## 品質基準（4基準）

**詳細**: `docs/quality-criteria.md`

- **希少性**: 巷の情報では得られない実践知か？
- **具体性**: 読者が明日から試せる具体的なTipsか？
- **新規性**: 直近1年以内に登場した新しい要素を含むか？
- **実証性**: 本番環境で検証済みの情報か？

**すべての基準を満たす必要があります。**

## 提供価値の5カテゴリ

**詳細**: `docs/value-categories.md`

1. **Remix**: Remixフレームワークに関する知見
2. **Cloudflare Edge**: Cloudflare Edgeに関する知見
3. **Claude Code(AI)**: Claude Codeに関する知見
4. **品質向上活動**: テスト自動化、アーキテクチャ設計等
5. **その他**: TypeScript, Vite, Playwright等

## 参照ドキュメント

| ファイル | 役割 |
| :--- | :--- |
| `prompts/01-reference.md` | 参照ファイル読み込みプロンプト |
| `prompts/02-organize.md` | 作業内容整理プロンプト |
| `prompts/03-evaluate.md` | 評価プロンプト |
| `prompts/04-prepare.md` | 導入部準備プロンプト |
| `prompts/05-confirm.md` | 確認プロンプト |
| `docs/quality-criteria.md` | 品質評価基準（4基準） |
| `docs/value-categories.md` | 提供価値の5カテゴリ |
| `docs/bab-structure.md` | 恐怖型BAB法 |
| `docs/terminology-check.md` | プロダクト固有用語チェック |
| `docs/reference-files.md` | 参照ファイル一覧 |

## 成果物

**記事企画書**（Markdown形式）:

- 何をするために（Why）
- 何をしたか（What）
- どんな壁があって（Challenge）
- どう乗り越えたか（Solution）
- 記事の提供価値
- 品質評価
- 導入部分構成
- カテゴリ・タグ
- オペレーターへの確認事項

## 注意事項

1. **品質評価を厳格に適用**: 希少性が低い内容は詳述しない。新規性のある内容を優先
2. **プロダクト固有用語の回避**: 読者が予備知識なしで理解できる表現を使用
3. **オペレーターとの協調**: 決めかねる部分は選択肢を提示して判断を仰ぐ
4. **blog-writerとの連携**: 企画書承認後、`/blog-writer`スキルで記事を作成

## 次のステップ

企画書の承認後、`/blog-writer`スキルを使用して記事を作成してください。
