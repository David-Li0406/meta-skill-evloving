---
name: github-project-creation
description: Use when user says 'gh project create', 'GitHub Project 作成', 'プロジェクト作成', 'create project', or discusses creating a new GitHub Project. Ensures projects have proper short description and README.
allowed-tools: [Bash, Read]
---

# GitHub Project 作成ガイド

## 目的

GitHub Project 作成時に、必要な情報（Short Description, README, デフォルトリポジトリ）が適切に設定されることを担保する。

## トリガー条件

以下の操作について議論・作業する際に自動的に実行:

- `gh project create` コマンドの実行
- GitHub Project の新規作成に関する議論
- プロジェクト管理の初期設定

## 必須項目

GitHub Project 作成時には、以下の項目を**必ず**設定すること:

| 項目 | 説明 | 必須 |
|------|------|------|
| Title | プロジェクト名 | 必須 |
| Short Description | プロジェクトの概要（1行） | **必須** |
| README | プロジェクトの詳細説明 | **必須** |
| Default Repository | 対象リポジトリ（Issue 追加時のデフォルト） | **必須** |

## Short Description ガイドライン

### 目的

プロジェクト一覧で表示される短い説明文。一目でプロジェクトの目的がわかるようにする。

### フォーマット

```
<動詞> + <対象> + <目的/範囲>
```

### 例

```
# Good
Track feature development for v2.0 release
Manage bug fixes and hotfixes for production
Coordinate documentation updates across repositories

# Bad
Project for stuff (曖昧すぎる)
（空欄）
```

### 文字数

- 推奨: 50〜100文字
- 最大: 280文字

## README ガイドライン

### 目的

プロジェクトの詳細情報を記載し、チームメンバーがプロジェクトの目的・運用方法を理解できるようにする。

### 必須セクション

```markdown
# プロジェクト名

## 概要
このプロジェクトの目的と範囲を説明。

## 対象
- どのリポジトリ/Issue が対象か
- どの期間/マイルストーンが対象か

## ステータス定義
| ステータス | 意味 |
|-----------|------|
| Todo | 未着手 |
| In Progress | 作業中 |
| Done | 完了 |

## 運用ルール
- Issue の追加方法
- ステータス更新のタイミング
- レビュー/完了の基準
```

### 推奨セクション（任意）

```markdown
## 関連リンク
- [リポジトリ](URL)
- [ドキュメント](URL)

## チーム
- Owner: @username
- Members: @team
```

## Default Repository ガイドライン

### 目的

プロジェクトに対象リポジトリをリンクし、Issue 追加時のデフォルトリポジトリを設定する。

### 設定方法

1. **Web UI から設定**:
   - Project Settings → Manage access → Link a repository
   - リポジトリを選択してリンク

2. **gh CLI から設定**:
   ```bash
   # プロジェクトにリポジトリをリンク
   gh project link <project-number> --owner @me --repo <owner>/<repo>
   ```

### 複数リポジトリの場合

```bash
# 複数リポジトリをリンク可能
gh project link <project-number> --owner @me --repo owner/repo1
gh project link <project-number> --owner @me --repo owner/repo2
```

### リンク済みリポジトリの確認

```bash
# Web UI の Project Settings → Manage access で確認
# または gh project view で確認
gh project view <project-number> --owner @me
```

## 作成手順

### 1. gh CLI でプロジェクト作成

```bash
# プロジェクト作成（対話形式）
gh project create

# または、オプション指定
gh project create --owner @me --title "Project Title"
```

### 2. Short Description 設定

```bash
# プロジェクト番号を確認
gh project list

# Short Description 編集
gh project edit <project-number> --description "Track feature development for v2.0 release"
```

### 3. README 設定

```bash
# README 編集（対話形式でエディタが開く）
gh project edit <project-number> --readme
```

または Web UI から:
1. Project Settings を開く
2. README セクションで編集

### 4. Default Repository 設定

```bash
# 対象リポジトリをリンク（必須）
gh project link <project-number> --owner @me --repo <owner>/<repo>

# リンク確認
gh project view <project-number> --owner @me
```

**重要**: Issue 追加時のデフォルトリポジトリとなるため、必ず設定すること。

## チェックリスト

プロジェクト作成時の確認事項:

```
[ ] Title が適切に設定されている
[ ] Short Description が記載されている
[ ] Short Description がプロジェクトの目的を明確に示している
[ ] README が作成されている
[ ] README に概要セクションがある
[ ] README に対象セクションがある
[ ] README にステータス定義がある
[ ] Default Repository がリンクされている
[ ] リンクされたリポジトリが正しいか確認済み
```

## クイックリファレンス

```
プロジェクト作成:
  gh project create --title "Project Title"

Short Description 設定:
  gh project edit <number> --description "説明文"

README 設定:
  gh project edit <number> --readme

リポジトリリンク:
  gh project link <number> --owner @me --repo <owner>/<repo>

プロジェクト一覧:
  gh project list

プロジェクト詳細:
  gh project view <number>
```

## 警告パターン

以下の状態を検知した場合は警告:

| 状態 | 警告メッセージ |
|------|---------------|
| Short Description 未設定 | Short Description が空です。プロジェクトの概要を記載してください。 |
| README 未設定 | README が空です。プロジェクトの詳細説明を記載してください。 |
| 曖昧な Description | Short Description が具体的ではありません。プロジェクトの目的を明確に記載してください。 |
| Repository 未リンク | リポジトリがリンクされていません。`gh project link` でデフォルトリポジトリを設定してください。 |
