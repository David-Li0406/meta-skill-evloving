---
name: implementation-workflow
description: TypeScript実装ワークフロースキル。実装時のエントリーポイントとして、状況に応じて適切なスキル（coding-standards、tdd、testing、react等）を参照させる。品質チェック、Gitワークフロー、コミットルールを定義。
---

# TypeScript実装ワークフロー

TypeScript開発における実装フローのエントリーポイント。状況に応じて適切なスキルを参照する。

## 関連スキル参照ガイド

| 状況 | 参照スキル |
|:-|:-|
| コーディング中 | `coding-standards` |
| テスト作成時 | `tdd`, `testing` |
| Reactコンポーネント実装時 | `react` |
| コード重複検出時 | `code-similarity-ts` |
| コミット時 | `commit`（git-workflow-plugin） |
| PR作成時 | `pull-request`（git-workflow-plugin） |

## 実装フロー

### 1. 作業開始

```bash
# mainで作業しない！必ず新ブランチを作成
git checkout -b feature/機能名
```

### 2. 実装計画を提示

コード変更前に以下を提示し承認を得る：
- タスクの理解と分析
- 実装すべき機能・コンポーネントの概要
- ファイル構成と変更対象
- 実装手順とステップ

### 3. TDDで実装

→ 詳細は `tdd` スキルを参照

- Red → Green → Refactor のサイクル
- 先にテストを書いてから実装

### 4. コーディング規約に従う

→ 詳細は `coding-standards` スキルを参照

- 早期return、不変性、単一責任
- 型定義、命名規則

### 5. React実装時

→ 詳細は `react` スキルを参照

- コンポーネント、カスタムフック、Storybook

### 6. 品質チェック（必須）

```bash
pnpm test        # テスト実行
pnpm lint        # Lintチェック
pnpm type-check  # 型チェック
```

**全て通るまでコミット禁止**

### 7. コミット

→ 詳細は `commit` スキルを参照

## 禁止事項

- `npx` の使用禁止（必ず `pnpm` を使用）
- ESLint無効化禁止（`eslint-disable` 系ディレクティブ禁止）
- mainブランチで直接作業禁止

## ブランチ命名規則

| プレフィックス | 用途 |
|:-|:-|
| `feature/` | 新機能追加 |
| `fix/` | バグ修正 |
| `refactor/` | リファクタリング |
| `docs/` | ドキュメント更新 |

## チェックリスト

```
## 実装前
- [ ] 新ブランチを作成した
- [ ] 実装計画を提示し承認を得た

## 実装中
- [ ] TDDサイクルを守っている（tddスキル参照）
- [ ] コーディング規約に従っている（coding-standardsスキル参照）
- [ ] React実装時はreactスキルを参照した

## 実装後
- [ ] `pnpm test` 通過
- [ ] `pnpm lint` 通過
- [ ] `pnpm type-check` 通過
- [ ] コミットルールに従っている（commitスキル参照）
```
