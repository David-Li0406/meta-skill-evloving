---
name: github-task-planning
description: Use this skill to review GitHub issues and pull requests, and create corresponding task files for improvements or responses.
---

# 使用方法

## 作業手順

1. **GitHub issueまたはPRの内容を把握する**
   - issueまたはPR番号を引数として受け取る
   - リポジトリ情報は `git remote -v` で確認

2. **デフォルトブランチとの差分を確認**（issueの場合）
   - デフォルトブランチを特定
   - そのブランチと現在のブランチの差分を確認して修正内容を把握

3. **レビューコメントを確認する**（PRの場合）
   - `github` スキルを使用してPRのレビューコメントを取得

4. **専門家エージェントでレビューを行う**（issueの場合）
   - **coding-specialist**: コーディングルールへの準拠を確認
   - **architecture-specialist**: アーキテクチャルールへの準拠を確認
   - **testing-specialist**: テストルールへの準拠を確認
   - **document-specialist**: 文書化ルールへの準拠を確認

5. **レビューでの指摘点やコメントを元にタスクファイルを作成**
   - 1ファイル1タスクとして`tmp/todo`フォルダにファイルを作成

## タスクファイル作成ガイド

### ファイル名フォーマット

- **Issueの場合**:
```
issue_{GitHub issue番号（#なし）}_plan_{2桁0埋めの1からの連番}_{タスク概要（英語）}.md
```
- **PRの場合**:
```
pr_{PRの番号}_task_{2桁0埋めの1からの連番}_{タスク概要（英語）}.md
```

### ファイル内容のテンプレート

```markdown
## 対応内容の概要

## 対応内容の詳細

### 編集対象ファイル

### 完了条件

### 備考
- 適当な粒度でコミットすること。
```

## 注意事項

- `tmp/todo`フォルダが存在しない場合は自動的に作成されます
- GitHub CLI (`gh`) が必要です
- 未解決のコメントのみが対象となります（PRの場合）
- タスクの粒度は、issueまたはPRの内容に応じて適切に調整してください

## 関連ドキュメント

- [コントリビューションガイド](../../../docs/04_contributing.md)
- [コーディングルール](../../../docs/01_coding_rules.md)
- [アーキテクチャルール](../../../docs/02_architecture_rules.md)
- [テストルール](../../../docs/03_testing_rules.md)
- [文書化ルール](../../../docs/07_document_rules.md)