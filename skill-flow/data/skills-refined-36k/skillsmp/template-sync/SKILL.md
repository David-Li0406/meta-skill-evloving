---
name: template-sync
description: "テンプレート同期スキル。yellow-seed/template の更新を他のリポジトリに反映。Use when: テンプレート更新の反映、template同期、既存リポジトリへの変更適用を依頼された時。"
---

# テンプレート同期

yellow-seed/template の更新内容を、このテンプレートを基に作成された他のリポジトリに反映するためのスキルです。

## 背景

- yellow-seed/template はテンプレート用途で、新しいリポジトリ作成時のベースとして使用される
- yellow-seed/template を更新した際、これを基にした既存リポジトリにも変更を追随させたい
- 多くのリポジトリが yellow-seed/template をベースにしているため、効率的な同期メカニズムが必要

## 同期原則

1. **非破壊的**: 参照先リポジトリの既存設定を尊重
2. **選択的適用**: 必要な変更のみを適用
3. **カスタマイズ保持**: プロジェクト固有のカスタマイズを保護
4. **透明性**: 適用される変更を明確に説明
5. **安全性**: 適用前に確認プロセスを提供
6. **パターンベース**: ファイルの性質や役割に基づいた分類と同期

## パターンベースの同期戦略

このスキルは、具体的なファイルパスではなく、ファイルの**性質**や**役割**に基づいた分類を使用します。これにより、将来追加されるファイルやディレクトリにも自動的に対応できます。

### A. GitHub設定ファイル群（`.github/` 配下）

**対象パターン**:

```bash
.github/**/*
```

**同期戦略**:

- `.github/workflows/`: 新規ファイルは追加、既存ファイルは構造比較後に更新提案
- `.github/ISSUE_TEMPLATE/`: 新規テンプレートを追加
- `.github/PULL_REQUEST_TEMPLATE.md`: 新規追加または内容比較
- `.github/actions/`: 新規カスタムアクションを追加
- `.github/configs/`, `.github/skills/`: 将来追加される任意のディレクトリに自動対応

### B. AIエージェント設定ファイル群

**対象パターン**:

```bash
# 既知のAIエージェント設定ディレクトリ
.claude/**/*
.codex/**/*
.cursor/**/*
.aider/**/*
.codeium/**/*
.copilot/**/*
```

**自動検出ロジック**:
テンプレート側でドット始まりの新しいディレクトリを検出した場合、以下の条件でAIエージェント設定と判定：

- ディレクトリ名が `.{claude,codex,cursor,aider,codeium,copilot}` のパターンに一致
- `skills/`, `prompts/`, `config/`, `hooks/` などのサブディレクトリを含む

**同期戦略**:

- **skills/**: 新規スキル追加、既存スキルは更新確認
- **hooks/**: 新規フック追加、既存フックは内容比較後に更新提案
- **config/**, **prompts/**: 新規ファイル追加、既存ファイルは内容比較

### C. 開発環境設定ファイル群

**対象パターン**:

```bash
# エディタ・フォーマッタ設定
.editorconfig
.prettierrc*
.eslintrc*
.markdownlint*
.shellcheckrc

# CI/CD設定
.codecov.yml
.renovate.json
.dependabot/**/*
```

**同期戦略**:

- 新規ファイル: そのまま追加
- 既存ファイル: 内容差分を表示し、マージ方法を提案
- 設定値: テンプレート値を基準に（詳細は「設定ファイル値の基準化」セクション参照）

### D. Git設定ファイル群

**対象パターン**:

```bash
.gitignore
.gitattributes
.gitmodules
```

**同期戦略**:

- 行単位でマージ（重複を避けて新規エントリを追加）
- コメントブロック単位で整理

### E. ドキュメントファイル（構造同期を含む）

**対象パターン**:

```markdown
README.md
AGENTS.md
CLAUDE.md
CONTRIBUTING.md
```

**同期戦略**:

- `README.md`: バッジセクション（先頭の `<!-- ... -->` コメントで囲まれた範囲）を同期
- `AGENTS.md`, `CLAUDE.md`: セクション構造をテンプレートに合わせてリファクタリング提案
- **構造同期の重要性**: skillsへの適切な委譲は、ドキュメント構造の質に依存するため、テンプレートのお手本構造を維持

## 同期ルールの明確化

| 同期タイプ     | 対象ファイル                                                                   | 動作                               |
| -------------- | ------------------------------------------------------------------------------ | ---------------------------------- |
| **完全同期**   | `.github/workflows/` (新規), `.github/ISSUE_TEMPLATE/`, `.github/actions/`     | テンプレートから完全コピー         |
| **構造同期**   | README.md, AGENTS.md, CLAUDE.md, `.github/workflows/` (既存)                   | 構造をテンプレートに合わせる       |
| **マージ同期** | `.gitignore`, `.gitattributes`                                                 | 既存内容を保持しつつ新規内容を追加 |
| **値同期**     | `.codecov.yml`, `.renovate.json`, `.editorconfig`                              | テンプレート値を基準に             |
| **選択的同期** | README.md (バッジセクションのみ)                                               | 特定セクションのみを置換           |
| **スキップ**   | プロジェクト固有ファイル (`package.json`, `Cargo.toml`, `pyproject.toml` など) | 同期対象外                         |

## ドキュメント構造同期

### 目的

テンプレートのお手本構造を維持し、AIエージェントが理解しやすいドキュメントを保つことで、skillsへの適切な委譲精度を向上させます。

### ドキュメント構造の比較

```bash
# 見出し構造を抽出
grep "^#" template/README.md > /tmp/template_structure.txt
grep "^#" target/README.md > /tmp/target_structure.txt
diff -u /tmp/target_structure.txt /tmp/template_structure.txt
```

### テンプレート推奨構造

**README.md**:

1. タイトルとバッジ
2. 概要・説明
3. 特徴（Features）
4. 前提条件（Prerequisites）
5. インストール（Installation）
6. 使い方（Usage）
7. 設定（Configuration）
8. テスト（Testing）
9. 貢献（Contributing）
10. ライセンス（License）

**AGENTS.md**:

1. プロジェクト概要
2. 技術スタック
3. ディレクトリ構造
4. 開発環境のセットアップ
5. コーディング規約
6. コミットメッセージ規約
7. コミット粒度
8. テスト戦略
9. Pull Request 作成
10. デプロイメント
11. その他の重要な情報

### リファクタリング提案の生成

構造比較結果から、ターゲットリポジトリのドキュメント構造をテンプレートに合わせるための提案を生成します。

```diff
- ## セットアップ
- ## 使い方
+ ## インストール方法
+   ### 前提条件
+   ### 手順
+ ## 使い方

→ 提案: セクション「セットアップ」を「インストール方法」に統合し、
         「前提条件」「手順」のサブセクションに再編成
```

## ワークフロー構造同期

### 目的

テンプレートの整理されたワークフロー構造は、適切なCI/CDのベストプラクティスを反映しています。トリガー条件、ジョブの分離、依存関係、ステップ順序などの構造パターンは、技術スタックに依存せず共通化できます。

### 同期する要素と同期しない要素

**同期する要素**:

| 要素             | 同期方法             | 理由                                 |
| ---------------- | -------------------- | ------------------------------------ |
| **トリガー条件** | テンプレート値を採用 | CI/CD戦略の統一                      |
| **ブランチ条件** | テンプレート値を採用 | `branches: [main]`                   |
| **パス条件**     | テンプレート値を採用 | `paths-ignore: ['**.md']` でCI最適化 |
| **ジョブ分離**   | 構造パターンを採用   | lint → test → coverage の分離        |
| **依存関係**     | 構造パターンを採用   | `needs: lint`                        |
| **ステップ順序** | 構造パターンを採用   | checkout → setup → action            |

**同期しない要素**:

| 要素                 | 理由                                                       |
| -------------------- | ---------------------------------------------------------- |
| **具体的なコマンド** | 技術スタック依存（`npm test` vs `pytest` vs `cargo test`） |
| **環境変数値**       | プロジェクト固有（`NODE_VERSION`, `PYTHON_VERSION` など）  |

### テンプレート推奨トリガー条件

```yaml
on:
  push:
    branches: [main]
    paths-ignore: ["**.md", "docs/**"]
  pull_request:
    branches: [main]
    paths-ignore: ["**.md", "docs/**"]
  workflow_dispatch: # 手動実行を許可
```

### ワークフロー構造パターン

**パターンA: 基本CI（lint → test）**

```yaml
jobs:
  lint:
    steps: [checkout, setup-tools, run-linter]

  test:
    needs: lint
    steps: [checkout, setup-env, run-tests]
```

**パターンB: カバレッジ付きCI（lint → test → coverage）**

```yaml
jobs:
  lint:
    steps: [checkout, setup-tools, run-linter]

  test:
    needs: lint
    steps: [checkout, setup-env, run-tests]

  coverage:
    needs: test
    steps: [checkout, setup-coverage, generate, upload]
```

### 構造リファクタリング提案の例

```markdown
# ci-macos.yml 構造リファクタリング提案

## 1. トリガー条件の修正

現在: `on: [push, pull_request]`
修正後: テンプレート推奨条件（branches指定、paths-ignore、workflow_dispatch追加）

## 2. ジョブ構成の修正

現在: test ジョブのみ（lint と test が混在）
修正後: lint と test を分離、依存関係を明示（`test: needs: lint`）

## 3. ステップ順序の整理

各ジョブで checkout → setup → action の順序を維持
```

## 設定ファイル値の基準化

### 対象ファイル

`.codecov.yml`, `.renovate.json`, `.editorconfig`, `.prettierrc` など

### 同期ルール

**codecov.yml の例**:

```yaml
# テンプレート基準値
coverage:
  status:
    project:
      default:
        target: 80% # ← この値を基準に
        threshold: 5% # ← この値を基準に
```

**適用方法**:

- カバレッジ目標値: テンプレート値を採用（プロジェクト全体で統一）
- 除外パス: マージ（テンプレート + プロジェクト固有）

**renovate.json の例**:

```json
{
  "extends": ["config:base"],
  "schedule": ["after 10pm every weekday"],
  "automerge": true
}
```

**適用方法**:

- スケジュール設定: テンプレート値を採用
- automerge設定: テンプレート値を採用
- パッケージ固有ルール: マージ

## READMEバッジセクションの同期

### 目的

テンプレート側でワークフローを追加した場合、対応するバッジもターゲットリポジトリのREADMEに反映します。

### 実装方法

1. テンプレート側のREADME先頭のコメントブロック（`<!-- ... -->`）で囲まれたバッジセクションを識別

```markdown
<!-- CI/CD & Code Quality -->

[![CI - macOS](https://github.com/yellow-seed/template/workflows/CI%20-%20macOS/badge.svg)](...)
[![CI - Ubuntu](https://github.com/yellow-seed/template/workflows/CI%20-%20Ubuntu/badge.svg)](...)

<!-- /CI/CD & Code Quality -->
```

2. ターゲット側のREADMEで同じコメントブロックパターンを検索
3. リポジトリ名を置換して適用（`yellow-seed/template` → `yellow-seed/{target-repo}`）
4. 既存のバッジを保持しつつ、新しいバッジを追加

### 注意事項

- プロジェクト固有のバッジ（言語固有、フレームワーク固有）は保持
- コメントブロックで囲まれていないバッジは変更しない

## ファイル構造の体系的な差分検出

### ディレクトリツリー比較

```bash
# ディレクトリツリー比較
git ls-tree -r --name-only template/main | grep -E "^\.(github|claude|codex)/" | sort > /tmp/template_structure.txt
git ls-tree -r --name-only HEAD | grep -E "^\.(github|claude|codex)/" | sort > /tmp/target_structure.txt
diff /tmp/template_structure.txt /tmp/target_structure.txt
```

### 新規ファイルタイプの自動検出

```bash
# テンプレートの設定ファイルを検出
find template -maxdepth 1 -type f \( -name ".*rc" -o -name ".*ignore" -o -name ".*yml" -o -name ".*json" \) | sort
```

### AIエージェント設定ディレクトリの自動検出

```bash
# ドット始まりのディレクトリを検出
find template -maxdepth 1 -type d -name ".*" | while read dir; do
  # skills/, hooks/, config/, prompts/ のいずれかを含むか確認
  if find "$dir" -maxdepth 1 -type d \( -name "skills" -o -name "hooks" -o -name "config" -o -name "prompts" \) | grep -q .; then
    echo "AIエージェント設定ディレクトリを検出: $dir"
  fi
done
```

## 同期手順

### 1. yellow-seed/template の情報確認

```bash
# yellow-seed/template のURL（デフォルト）
TEMPLATE_REPO="https://github.com/yellow-seed/template.git"

# yellow-seed/template の最新情報を取得
git ls-remote --heads $TEMPLATE_REPO
```

### 2. 現在のリポジトリ設定を分析

**分析項目**:

- プログラミング言語とフレームワーク
- 既存のCI/CD設定
- プロジェクト構造
- カスタマイズされた設定ファイル
- 既存のskillsとhooks

**分析方法**:

```bash
# 言語検出
ls package.json pyproject.toml Cargo.toml go.mod Gemfile pom.xml build.gradle 2>/dev/null

# 既存のskills確認
ls -la .claude/skills/ 2>/dev/null

# 既存の.github/設定確認（全体）
ls -la .github/ 2>/dev/null
find .github/ -type f 2>/dev/null

# 既存のドキュメント確認
ls AGENTS.md CLAUDE.md README.md 2>/dev/null
```

### 3. yellow-seed/template との差分を検出

```bash
# yellow-seed/template をリモートとして追加（一時的）
git remote add template $TEMPLATE_REPO 2>/dev/null || true
git fetch template main

# 差分を確認
git diff HEAD template/main --name-only

# 特定ディレクトリの差分を詳細確認
git diff HEAD template/main -- .claude/skills/
git diff HEAD template/main -- .github/
git diff HEAD template/main -- AGENTS.md
git diff HEAD template/main -- README.md
```

### 4. 適用すべき変更を選択

**自動適用可能な変更**:

- `.claude/skills/`内の新規skillファイル
- `.github/`配下の全ての新規ファイル・ディレクトリ
  - `.github/workflows/`内の新規ワークフローファイル
  - `.github/ISSUE_TEMPLATE/`内の新規テンプレート
  - `.github/skills/`, `.github/configs/`等、将来追加される新規ディレクトリ

**確認が必要な変更**:

- 既存ファイルの更新
- 設定ファイルの変更（`.gitignore`, `.editorconfig`等）
- ドキュメントファイルの更新（`AGENTS.md`, `CLAUDE.md`）

**適用しない変更**:

- カスタマイズされた設定
- プロジェクト固有のworkflows

### 5. 変更内容の微調整

#### 5.1 言語・フレームワーク固有の調整

```bash
# 例: Node.jsプロジェクトの場合
if [ -f "package.json" ]; then
  # Node.js関連のworkflowsのみ適用
  # Python関連のworkflowsはスキップ
fi
```

#### 5.2 既存設定との統合

**戦略**:

- 新規ファイル: そのまま追加
- 既存ファイルの新規セクション: セクション単位で追加
- 既存ファイルの更新: ユーザーに確認を求める

**例: AGENTS.mdの統合**:

```markdown
# 現在のAGENTS.md

## プロジェクト概要

[既存の内容]

# yellow-seed/template からの新規セクション

## 開発環境のセットアップ

### Claude Code での GitHub CLI (gh) のセットアップ

[新規内容を追加]
```

#### 5.3 競合解決

**競合が発生する場合**:

1. 両方の内容を並べて表示
2. 推奨される統合方法を提案
3. ユーザーの確認を待つ
4. ユーザーの選択に基づいて適用

### 6. 変更を適用

```bash
# yellow-seed/template の .github/workflows/new-workflow.yml を追加
git show template/main:.github/workflows/new-workflow.yml > .github/workflows/new-workflow.yml

# yellow-seed/template の .github/skills/ を追加する例
mkdir -p .github/skills
git archive --remote=$TEMPLATE_REPO HEAD:.github/skills/ | tar -x -C .github/skills/

# yellow-seed/template の .claude/skills/new-skill/SKILL.md を追加
git show template/main:.claude/skills/new-skill/SKILL.md > .claude/skills/new-skill/SKILL.md

# ドキュメントの部分更新例（セクション追加）
# 手動でセクションを追加、または既存内容を保持してマージ
```

### 7. 適用結果の確認

```bash
# 変更内容を確認
git status
git diff

# 変更をコミット
git add .
git commit -m "chore: sync updates from yellow-seed/template

Applied changes:
- Added new skill: xxx
- Added new workflow: yyy
- Updated AGENTS.md with new sections

Source: yellow-seed/template@<commit-hash>"
```

### 8. クリーンアップ

```bash
# 一時的に追加したリモートを削除
git remote remove template
```

## 実行例

### シナリオ1: 新規ファイル・ディレクトリの自動追加（完全同期）

```markdown
**検出された変更**:

- `.claude/skills/template-sync/SKILL.md` (新規スキル)
- `.github/workflows/shell-linting.yml` (新規ワークフロー)
- `.codex/` (新規AIエージェント設定ディレクトリ、自動検出)

**自動検出の流れ**:

1. ドット始まりのディレクトリ `.codex/` を検出
2. サブディレクトリ `skills/`, `config/` を確認
3. AIエージェント設定と判定

**適用戦略**:

- パターンベースで自動的に追加対象と判定
- 新規ファイル・ディレクトリをそのままコピー

**実行**:

1. 新規ディレクトリを作成
2. yellow-seed/template からファイルをコピー
3. 動作確認
4. コミット: `git commit -m "chore: add new files and directories from template"`
```

### シナリオ2: .gitignoreのマージ（マージ同期）

```markdown
**検出された変更**:

- yellow-seed/template の `.gitignore`: 複数の新規エントリ

**現在の.gitignore**:
```

node_modules/
.env
dist/

```

**yellow-seed/template の .gitignore**:
```

# Node

node_modules/
.env
dist/

# IDE

.vscode/
.idea/

# OS

.DS_Store
Thumbs.db

# Claude Code

.claude/settings.local.json

```

**適用戦略**:
- 新規セクション（IDE, OS, Claude Code）を追加
- 既存エントリは保持

**実行**:
1. `.gitignore`に新規セクションを追加
2. 既存の内容は変更しない
3. コミット: `git commit -m "chore: update .gitignore from yellow-seed/template"`
```

### シナリオ3: ドキュメント構造のリファクタリング（構造同期）

````markdown
**検出された変更**:

- `AGENTS.md`: 構造の整理と新規セクション追加
- `README.md`: バッジセクションの更新

**AGENTS.md 構造比較結果**:

```diff
# 現在のターゲットリポジトリ
## プロジェクト概要
## 使い方
## セットアップ手順

# yellow-seed/template の推奨構造
## プロジェクト概要
## 技術スタック
## ディレクトリ構造
## 開発環境のセットアップ
## コーディング規約
## コミットメッセージ規約
## コミット粒度
## テスト戦略
## Pull Request 作成
## デプロイメント
## その他の重要な情報
```
````

**README.md バッジセクション**:

- コメントブロック `<!-- CI/CD & Code Quality -->` で囲まれた範囲を同期
- リポジトリ名を自動置換（`yellow-seed/template` → `yellow-seed/target-repo`）

**適用戦略**:

- AGENTS.md: 既存内容を保持しつつ、セクション構造をテンプレートに合わせる
- README.md: バッジセクションのみ選択的に同期

**実行**:

1. 見出し構造を抽出して比較
2. リファクタリング提案を生成
3. ユーザー確認後、構造を再編成
4. コミット: `git commit -m "docs: restructure documents to match template"`

````

### シナリオ4: ワークフロー構造の同期（構造同期）

```markdown
**検出された変更**:
- `.github/workflows/ci.yml`: 構造パターンの改善

**構造比較結果**:
```diff
# 現在のターゲットリポジトリ
on: [push, pull_request]
jobs:
  test:
    steps: [checkout, setup, lint, test]

# yellow-seed/template の推奨構造
on:
  push:
    branches: [main]
    paths-ignore: ['**.md', 'docs/**']
  pull_request:
    branches: [main]
    paths-ignore: ['**.md', 'docs/**']
  workflow_dispatch:
jobs:
  lint:
    steps: [checkout, setup-tools, run-linter]
  test:
    needs: lint
    steps: [checkout, setup-env, run-tests]
````

**適用戦略**:

- トリガー条件をテンプレート値に更新（branches指定、paths-ignore、workflow_dispatch追加）
- ジョブを lint と test に分離、依存関係を明示
- 具体的なコマンド（npm test など）は変更しない

**実行**:

1. ワークフロー構造を比較
2. トリガー条件を更新
3. ジョブ構造をリファクタリング（コマンドは保持）
4. コミット: `git commit -m "ci: refactor workflow structure to match template"`

````

### シナリオ5: 設定ファイル値の基準化（値同期）

```markdown
**検出された変更**:
- `.codecov.yml`: カバレッジ目標値の更新
- `.renovate.json`: スケジュール設定の更新

**codecov.yml 値比較結果**:
```diff
# 現在のターゲットリポジトリ
coverage:
  status:
    project:
      default:
        target: 70%
        threshold: 10%

# yellow-seed/template の基準値
coverage:
  status:
    project:
      default:
        target: 80%
        threshold: 5%
````

**適用戦略**:

- カバレッジ目標値をテンプレート基準値（80%、5%）に更新
- 除外パスはマージ（テンプレート + プロジェクト固有）
- プロジェクト全体で統一された基準を維持

**実行**:

1. 設定値を比較
2. テンプレート基準値を適用
3. 除外パスをマージ
4. コミット: `git commit -m "chore: align config values with template standards"`

````

## 同期時のチェックリスト

- [ ] yellow-seed/template の最新情報を取得した
- [ ] 現在のリポジトリの設定を分析した
- [ ] 差分を確認し、適用すべき変更を選択した
- [ ] プロジェクト固有の設定を保持する戦略を確認した
- [ ] 新規ファイルの追加を実行した
- [ ] 既存ファイルの更新（必要な場合）をユーザーと確認した
- [ ] 変更内容をコミットした
- [ ] 一時的なリモートをクリーンアップした
- [ ] 適用後の動作確認を行った

## 注意事項

1. **バックアップの推奨**: 同期前にブランチを作成することを推奨
   ```bash
   git checkout -b sync-from-template
````

2. **段階的な適用**: 一度に全ての変更を適用せず、段階的に適用することを推奨

3. **テストの実施**: 適用後、必ずCI/CDやローカルテストを実施

4. **ドキュメントの確認**: READMEやAGENTS.mdの内容がプロジェクトに適合しているか確認

5. **カスタマイズの尊重**: プロジェクト固有のカスタマイズは常に尊重

## トラブルシューティング

### 問題: yellow-seed/template にアクセスできない

**解決策**:

```bash
# SSHキーの確認
ssh -T git@github.com

# HTTPSでアクセスを試す
TEMPLATE_REPO="https://github.com/yellow-seed/template.git"
```

### 問題: 差分が大きすぎて適用が困難

**解決策**:

- 優先度の高い変更のみを適用
- 複数のPRに分割して段階的に適用

### 問題: 競合が複雑で自動マージが困難

**解決策**:

- ユーザーに手動マージを依頼
- 競合部分の両方の内容を表示し、選択を促す

## 他のスキルとの連携

### commit-message スキルとの連携

- 同期によるコミットは `chore:` タイプを使用
- コミットメッセージに yellow-seed/template のコミットハッシュを含める

### pull-request スキルとの連携

- 大規模な同期の場合、PRを作成して変更をレビュー
- PR概要で yellow-seed/template からの変更内容を明確に説明

### github-issue スキルとの連携

- 適用できなかった変更や要検討事項をIssueとして記録
- yellow-seed/template 同期の定期実施をtodoとして管理

## ベストプラクティス

1. **定期的な同期**: yellow-seed/template の更新を定期的にチェック
2. **選択的適用**: 全ての変更を盲目的に適用せず、必要なもののみを選択
3. **ドキュメント化**: 適用した変更と理由をドキュメント化
4. **テスト重視**: 適用後は必ずテストを実施
5. **コミュニティ貢献**: yellow-seed/template への改善提案も検討

## 実装の最小化

このskillは以下の最小限のセットアップで動作します：

1. **必須ファイル**: このSKILL.mdファイルのみ
2. **依存関係**: Git、GitHub CLI（gh）
3. **設定**: 環境変数 `TEMPLATE_REPO`（オプション、デフォルト: yellow-seed/template）

**使用方法**:

```bash
# AI Agentに依頼するだけ
"yellow-seed/template の最新の変更を同期してください"
```

AI Agentが自動的に：

1. yellow-seed/template の変更を検出
2. 現在のリポジトリ設定を分析
3. 適用可能な変更を提案
4. ユーザーの確認後、変更を適用
5. 適切なコミットメッセージでコミット

## yellow-seed/template 情報

- **リポジトリ**: `yellow-seed/template`
- **ブランチ**: `main`
- **URL**: `https://github.com/yellow-seed/template.git`

別のテンプレートを使用する場合は、以下のように指定：

```bash
TEMPLATE_REPO="https://github.com/your-org/your-template.git"
```
