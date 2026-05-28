---
name: cga-tf-refactoring
description: 機能追加前に構造を整理する簡単なリファクタリング。Kent Beckの「Tidy First?」に基づく。
allowed-tools: Read Glob Grep Edit Write Bash AskUserQuestion
disable-model-invocation: true
---

## いつ使うか

- 新機能を追加する前に、コードの構造を整理したいとき
- 既存コードに手を入れる前に、変更しやすくしたいとき
- 「このコード、もう少し整理してから機能追加したい」と感じたとき

## いつ使わないか

- テストがなく安全に変更できないとき（先にテストを書く）
- 大規模な書き換えが必要なとき（別タスクとして計画する）
- 今回の変更に関係ない箇所の整理（スコープ外）

## 何をするか

**Tidy First = 機能変更の前に、小さな構造改善を先に行う**

1. 対象コードを分析し、変更を妨げる「構造の問題」を特定
2. 機能変更に必要な最小限の整理（Tidying）を提案
3. 整理を実施（テストが通ることを確認）
4. その後、本来の機能変更に進む

## Tidyingのパターン

| パターン | 説明 | 例 |
|---------|------|-----|
| Guard Clauses | ネストを減らす早期リターン | if-else の深いネスト → 早期return |
| Extract Helper | 重複コードを関数に抽出 | 同じ処理が3箇所 → 共通関数化 |
| Normalize Symmetries | 似た処理を同じ形に統一 | 一方はfor、他方はmap → 両方mapに |
| Chunk Statements | 関連する処理をまとめる | バラバラの変数宣言 → 関連グループ化 |
| Rename | 意図が伝わる名前に変更 | `data` → `orderDetails` |
| Explicit Parameters | 暗黙の依存を引数に | グローバル参照 → 引数で渡す |
| Delete Dead Code | 使われていないコードを削除 | 呼ばれない関数、到達しない分岐 |
| Move to Model | UseCaseの判定・状態遷移を集約モデルへ移動 | UseCase内のif判定 → モデルの純粋関数へ |
| Move to Service | 複数集約にまたがるロジックをサービスへ移動 | UseCase内の横断処理 → ドメインサービスへ |

## 中断条件

以下の場合は整理を中断し、開発者に状況を報告する:

- **テスト失敗**: 整理後にテストが通らない場合はrevertして報告
- **スコープ超過**: 整理対象が3ファイルを超える場合は停止して確認を求める
- **振る舞い変更の懸念**: 整理がロジックの振る舞いに影響する可能性がある場合

## 使用例

```text
/cga-tf-refactoring src/ordering/usecases/create-order.ts に商品バリデーション追加したいので整理して
/cga-tf-refactoring このファイルをキャンセル機能追加しやすくして
```

## ワークフロー位置

```
/cga-explore-planning → /cga-tf-refactoring → /cga-programming → /cga-review
```

## 詳細

[guide.md](guide.md) を参照
