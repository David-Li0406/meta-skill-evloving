---
name: manage-github-tasks
description: Use this skill when you need to create task files based on GitHub issue or pull request reviews, ensuring all necessary actions are documented and tracked.
---

# Skill body

## 使用方法

### 作業手順

1. **GitHub issueまたはPRの情報を取得する**
   - GitHub issueの場合:
     ```bash
     gh issue view <ISSUE_NUMBER> --json number,title,body,state,labels,assignees,milestone,createdAt,updatedAt
     ```
   - PRの場合:
     ```bash
     githubスキルを使用してPRのレビューコメントを取得
     ```

2. **レビューコメントを確認する**
   - `github` スキル（thread-list.sh）を使用してPRのレビューコメントを取得
   - 必要に応じてスレッドの詳細を確認する（`github` スキルのthread-details.shを使用）

3. **タスクファイルを作成する**
   - レビューコメントやissueの内容に基づいて、以下のようにタスクファイルを作成します。
   - **ファイル名フォーマット**:
     - GitHub issue: 
       ```
       issue_{GitHub issue番号}_plan_{2桁0埋めの1からの連番}_{タスク概要（英語）}.md
       ```
     - PR:
       ```
       pr_{PRの番号}_task_{2桁0埋めの1からの連番}_{タスク概要（英語）}.md
       ```

### タスクファイル内容のテンプレート

```markdown
## 対応内容の概要

## 対応内容の詳細

### 編集対象ファイル

### 完了条件

### 備考
- 適当な粒度でコミットすること。
```

## 注意事項

- `tmp/todo`フォルダが存在しない場合は自動的に作成されます。
- GitHub CLI (`gh`) が必要です。
- 未解決のコメントのみが対象となります。
- タスクの粒度は、issueまたはPRの内容に応じて適切に調整してください。

## 関連スキル

- **github**: GitHub操作の統合スキル（スレッド一覧取得、詳細取得、返信、解決）

## 関連ドキュメント

- [コントリビューションガイド](../../../docs/04_contributing.md) - プルリクエストの作成方法
- [テストルール](../../../docs/03_testing_rules.md) - TDDの実践方法