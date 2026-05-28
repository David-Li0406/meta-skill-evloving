---
name: commit
description: "変更内容を確認し、適切なコミットメッセージを生成してコミットする。「コミットして」「変更をコミット」などの依頼時に使用。"
argument-hint: "[optional: specific message or scope]"
disable-model-invocation: false
allowed-tools: Bash, Read, Grep, Glob
---

# コミットスキル

現在の変更内容を確認し、Conventional Commits 形式でコミットメッセージを生成してコミットする。

## 実行手順

1. `git status` と `git diff` で変更内容を確認
2. 変更の種類と範囲を分析
3. Conventional Commits 形式でメッセージを生成
4. ユーザーに確認後、コミットを実行

## Conventional Commits 形式

```
type(scope): description

[optional body]

[optional footer]
```

### type

| type | 説明 |
|------|------|
| feat | 新機能 |
| fix | バグ修正 |
| docs | ドキュメントのみの変更 |
| style | コードの意味に影響しない変更（空白、フォーマット等） |
| refactor | バグ修正や機能追加ではないコード変更 |
| perf | パフォーマンス改善 |
| test | テストの追加・修正 |
| chore | ビルドプロセスや補助ツールの変更 |

### scope

変更の影響範囲を示す（任意）。例: `auth`, `api`, `ui`

### description

- 命令形で記述（Add, Fix, Update など）
- 50文字以内
- 末尾にピリオドを付けない

## 注意事項

- 機密情報を含むファイル（`.env` など）は除外
- 大量の変更がある場合は分割を提案
- `--amend` は明示的に指示された場合のみ使用
- push は自動で行わない（明示的に指示された場合のみ）

## 引数

`$ARGUMENTS` が指定された場合:
- 特定のメッセージやスコープとして使用
- 例: `/commit auth` → `feat(auth): ...` のようにスコープを設定
