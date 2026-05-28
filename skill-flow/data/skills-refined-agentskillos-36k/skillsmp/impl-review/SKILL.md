---
name: impl-review
description: GitHub PR Review Comment Implementation
---

# GitHub PR Review Comment Implementation

GitHub PRのレビューコメントURLから指摘事項を分析し、実装まで行います。

## 入力形式

ユーザーは以下の形式でURLを提供します：

```
https://github.com/{org}/{repo}/pull/{pr}/files#r{comment_id}
https://github.com/{org}/{repo}/pull/{pr}/files#r{comment_id}
...
```

## 処理フロー

### 1. コメント取得（並列実行）

各URLから以下の情報を抽出：
- URLから`{org}`, `{repo}`, `{comment_id}`をパース
- `gh api repos/{org}/{repo}/pulls/comments/{comment_id}`で各コメントを並列取得
- 抽出項目：`body`, `path`, `diff_hunk`, `start_line`, `line`

### 2. 影響範囲分析（効率重視）

最小限のファイル読み込みで影響範囲を特定：

1. 指摘ファイルをRead（対象行±20行程度、offset/limit使用）
2. 指摘内容から関連パターン（関数名/変数名）を特定
3. Grepで関連コードを検索（glob patternで範囲限定）
4. 必要なファイルのみ追加でRead

効率化：
- 複数のRead/Grepは並列実行
- offset/limitで必要範囲のみ取得
- glob patternで検索範囲を限定（例：`**/*.go`, `internal/**/*.go`）

### 3. 実装計画提示

以下の形式で計画を提示：

```
## 指摘事項

- [ファイル:行] 内容
- [ファイル:行] 内容

## 修正方針

1. ...
2. ...

## 影響ファイル

- file1: 変更内容
- file2: 変更内容
```

AskUserQuestionで承認を取得（Yes/No形式）

### 4. 実装（承認後）

1. TodoWriteでタスクリスト作成
2. 各ファイルをEditで変更
   - 同一ファイルへの複数変更は1回のEditにまとめる
   - 変更ごとにTodoを更新（in_progress → completed）
3. 変更完了後、全Todoをcompletedに

### 5. 完了報告

以下を表示：
- `git diff`で変更内容
- 変更ファイル一覧（`file:line`形式）

## エラー処理

- `gh api`が404: その旨を報告し、他のURLの処理を継続
- 指摘内容が不明瞭: AskUserQuestionで確認
- ファイルが見つからない: エラー報告して継続

## 出力スタイル

- 簡潔な日本語
- ファイル参照は`file:line`形式
- 挨拶や感嘆表現は不要
- 処理状況を明確に報告

## 実行手順

1. ユーザーからURL一覧を受け取る
2. URLをパースして`gh api`コマンドを並列実行
3. コメント内容を分析
4. 影響範囲を効率的に調査
5. 実装計画を提示し、承認を待つ
6. 承認後、TodoWriteでタスク管理しながら実装
7. 完了報告
