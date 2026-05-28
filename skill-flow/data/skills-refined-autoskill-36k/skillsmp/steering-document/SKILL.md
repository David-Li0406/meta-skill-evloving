---
description: |
  プロジェクトのステアリングドキュメント（永続的コンテキスト）の初期化・移行ガイド。以下の状況で使用:
  (1) ユーザーが「プロジェクト方針を定義したい」「技術スタックを整理したい」と言った時
  (2) `.claude/skills/steering/` の初期化方法を知りたい時
  (3) 既存の `specs/_steering/` から移行したい時
  (4) ステアリングテンプレートの書き方を確認したい時
---

# ステアリングドキュメント初期化ガイド

ユーザープロジェクトに `.claude/skills/steering/SKILL.md` を生成するためのガイド。

## 概要

ステアリングドキュメントはプロジェクト全体の永続的なコンテキスト:
- **Product**: プロダクト方針、ビジョン、ターゲットユーザー
- **Tech Stack**: 技術スタック、アーキテクチャ、開発標準
- **Structure**: プロジェクト構造、命名規則
- **Principles**: 開発原則（TDD, SOLID, YAGNI）

## 配置場所

**新しい構造**: `.claude/skills/steering/SKILL.md`

Progressive Disclosure により、Claude は文脈に応じて自動的に参照する。

## 初期化手順

### テンプレートコピースクリプト

```bash
# テンプレートを .claude/skills/steering/ にコピー
bun run ${CLAUDE_PLUGIN_ROOT}/skills/steering/scripts/copy-templates.ts .claude/skills/steering
```

コピーされるファイル:
- `product.md` - プロダクト方針
- `tech.md` - 技術スタック
- `structure.md` - プロジェクト構造
- `principles.md` - 開発原則

### テンプレートの更新

コピー後、各ファイルをプロジェクトに合わせて更新する:

1. **既存ドキュメントの確認**: README.md、AGENTS.md、package.json 等に既に記載されている情報をチェック
2. **重複を避ける**: 既存ドキュメントと競合する情報は書かない
3. **各テンプレートの指示に従う**: テンプレート内の「記載のポイント」を参照

### sdd-webapp登録

ステアリング作成後、`sdd_webapp_add_project` でプロジェクトを登録。

### 完了報告

```
✅ ステアリングドキュメントを作成しました
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 作成先: .claude/skills/steering/
🌐 sdd-webapp: 登録済み

💡 次のアクション:
   - 内容を確認・編集
   - SDD コマンドで仕様書作成: `/sdd:spec:init`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 移行手順（既存 `specs/_steering/` がある場合）

### 1. 既存ファイルの検出

`specs/_steering/` 配下の4ファイルを読み込み:
- product.md
- tech.md
- structure.md
- principles.md

### 2. 内容の統合

4ファイルの内容を `.claude/skills/steering/SKILL.md` に統合。

### 3. 完了報告

```
✅ ステアリングドキュメントを移行しました
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 移行元: specs/_steering/
📍 移行先: .claude/skills/steering/SKILL.md

⚠️ 古いファイルは手動で削除してください:
   rm -rf specs/_steering/
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 重要な原則

- **Progressive Disclosure**: 明示的に読み込む必要なし（Claude が文脈から判断）
- **唯一の真実の源**: プロジェクト方針の矛盾を防ぐ
- **抽象レベルを維持**: 具体的なファイル名やコマンドは列挙しない

## 関連リソース

- **steering-reviewer エージェント**: ステアリング準拠レビュー
