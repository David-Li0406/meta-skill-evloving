---
name: cga-planning-and-review
description: Use this skill to conduct parallel investigations and code reviews using sub-agents, facilitating decision-making and planning in software development.
---

## いつ使うか

- 仕様(Spec)を元に実装方針を調査・計画したいとき
- 技術的負債の返済のための調査と計画が必要なとき
- 技術選定・アプローチを検討したいとき
- コードベースの現状を把握し、方針を決めたいとき
- プルリクエストのレビュー時
- 特定ファイル・ディレクトリのレビュー時
- リファクタリング前の品質チェック時

## 何をするか

### 実装計画の調査と決定

1. **Phase 0**: 実装計画の有無を確認、計画済みなら `/cga-programming` へ誘導
2. **Phase 1**: Specと `glossary.md`、`doc/decisions/` 確認、Explore でコードベース調査
3. **Phase 1.5**: コード調査の結果を確認し、必要ならGit履歴調査を追加実施
4. **Phase 2**: 選択肢設計、トレードオフ分析、ユーザーと対話、TDD準拠の実装計画作成
5. **Phase 3**: `doc/plans/{issue-name}.md` に Write
6. **Phase 4**: 次スキルへ誘導

### コードレビューの実施

1. **Task(Bash)**: 自動チェック（`npm run review:json`）
2. **Task(Explore)**: ビジネスロジックの正しさレビュー
3. **Task(Explore)**: 設計・命名レビュー
4. **Task(Explore)**: セキュリティレビュー

結果をマージして問題点と改善提案をまとめる。

## 基本ルール

- Specが起点、無ければユーザーに確認
- src配下のコード変更は行わない（doc/plans への出力のみ）
- `glossary.md` と `doc/decisions/` 必須確認
- コード調査のあと、必要があればGit履歴を調査
- 対話はメインで実施（透明性重視）
- TDD準拠の実装計画を作成

## 使用例

```text
/cga-explore-planning
### ORD-004: 注文キャンセルAPI
**概要** 顧客が注文をキャンセルできるAPIを実装する。
**受け入れ条件**
- [ ] `PENDING` または `CONFIRMED` 状態の注文のみキャンセル可能
- [ ] キャンセル後の状態は `CANCELLED` になる

/cga-review src/ordering/usecases/
/cga-review src/ordering/usecases/create-order.ts
```

## 詳細

[guide.md](guide.md) を参照