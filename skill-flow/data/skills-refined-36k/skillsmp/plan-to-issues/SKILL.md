---
name: plan-to-issues
description: 実装計画からGitHub Issuesを作成するスキル。実装計画テンプレートをエピックと子Issueに分解してGitHub Issuesとして起票する。「Issueを作りたい」「実装計画をIssue化したい」「エピックを作成したい」などのリクエスト時に使用。
---

# Plan to Issues

実装計画をGitHub Issuesに変換するスキル。

## ワークフロー

```
1. 実装計画の確認
   ↓
2. エピックIssue作成
   ↓
3. 子Issue分解・起票
   ↓
4. 親子リンク設定
```

## 前提・準備

### ラベル作成

リポジトリにラベルがない場合、`scripts/create-github-labels.sh`で一括作成:

```bash
# カレントリポジトリに作成
./scripts/create-github-labels.sh

# 特定リポジトリに作成
REPO=owner/repo ./scripts/create-github-labels.sh

# ドライラン（実行内容のみ表示）
DRY_RUN=1 ./scripts/create-github-labels.sh

# 既存ラベルも上書き更新
FORCE_UPDATE=1 ./scripts/create-github-labels.sh
```

### ラベル指針
- 種別: `type:epic` / `type:feature` / `type:migration` / `type:chore` / `type:test` / `type:docs`
- 領域: `area:frontend` / `area:server` / `area:shared`
- 優先度: `priority:P1` / `priority:P2` / `priority:P3`
- 規模: `size:S` / `size:M` / `size:L`

### マイルストーン
該当スプリント/マイルストーンを用意

## Issue種類

### 1. エピック（親Issue）

テンプレート: `assets/templates/epic.template.md`

**タイトル形式**: `[Epic] 機能名: 実装計画と進行管理`

**内容**:
- 背景/目的
- スコープ
- サブIssue（Tasklist）
- 受け入れ条件（DoD）

### 2. Feature Issue

テンプレート: `assets/templates/feature.template.md`

**タイトル形式**: `[Feature][Model] ComponentA: create/parseを実装`

**内容**:
- 目的
- 仕様（入力/出力/エラーモード）
- タスク
- 完了条件

### 3. Migration Issue

テンプレート: `assets/templates/migration.template.md`

**タイトル形式**: `[Migration] Phase 1: 基本実装`

**内容**:
- 目的
- 範囲（対象/非対象）
- タスク
- リスク/ロールバック

### 4. Test Issue

テンプレート: `assets/templates/test.template.md`

**タイトル形式**: `[Test] ComponentA/Bの単体・結合テスト整備`

### 5. Docs Issue

テンプレート: `assets/templates/docs.template.md`

**タイトル形式**: `[Docs] 使用例/設計ドキュメント更新`

### 6. Chore Issue

テンプレート: `assets/templates/chore.template.md`

**タイトル形式**: `[Chore] CI/CD改善`

## 分解ヒント

実装計画の章から分解:

| セクション | Issue種類 |
|:-|:-|
| 主要コンポーネントの設計 | Feature Issue |
| 未実装リスト | Feature Issue |
| 移行計画（Phase 1〜4） | Migration Issue |
| 技術的な詳細（エラーハンドリング/パフォーマンス） | Test/Chore Issue |

## 作成手順

### 1. エピックIssue作成

```bash
EPIC_NUM=$(gh issue create \
  --title "[Epic] 機能名: 実装計画と進行管理" \
  --body-file epic.md \
  --label "type:epic" \
  --label "priority:P2" \
  | grep -oE '[0-9]+$')
echo "Created Epic: #${EPIC_NUM}"
```

### 2. 子Issue作成 + Sub-issue紐付け

子Issueを作成し、`gh api`でSub-issueとして親に紐付ける:

```bash
# 子Issue作成
CHILD_NUM=$(gh issue create \
  --title "[Feature][Model] ComponentA: create/parseを実装" \
  --body-file feature.md \
  --label "type:feature" \
  | grep -oE '[0-9]+$')

# Sub-issueとして紐付け（GitHub GraphQL API）
gh api graphql -f query='
  mutation {
    addSubIssue(input: {
      issueId: "<EPIC_NODE_ID>"
      subIssueId: "<CHILD_NODE_ID>"
    }) {
      issue { number }
      subIssue { number }
    }
  }
'
```

### 3. Node ID取得方法

```bash
# Issue番号からNode IDを取得
gh api graphql -f query='
  query {
    repository(owner: "OWNER", name: "REPO") {
      issue(number: 123) {
        id
      }
    }
  }
'
```

### 簡易フロー（推奨）

1. エピックIssue作成（Tasklist形式で子タスクを列挙）
2. 各子Issueを作成
3. GraphQL APIで`addSubIssue`を実行して紐付け
4. ラベル/マイルストーン設定

## 完了チェックリスト

- [ ] エピック1件＋子Issue（実装/移行/品質/Docs）が作成済み
- [ ] すべての子Issueがエピックに相互参照されている
- [ ] ラベル/マイルストーン/担当/優先度が設定済み
- [ ] 子Issueの完了条件がテスト/ドキュメントまで含む
