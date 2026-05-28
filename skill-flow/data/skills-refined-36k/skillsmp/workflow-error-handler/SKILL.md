---
name: workflow-error-handler
description: ワークフローのエラーに対応するスキルです。エラーの確認、再現、原因特定、対処、検証を体系的に行い、依頼者に説明します。ワークフローの失敗やCI/CDエラーへの対応を依頼された場合に使用してください。
---

# ワークフローエラー対応スキル

このスキルは、GitHub Actionsワークフローのエラーに対して体系的に対応し、問題を解決します。

## 利用可能なツール

このスキルでは以下のツールを使用します:

- **github-mcp-server-actions_list**: ワークフロー実行履歴の取得
- **github-mcp-server-actions_get**: ワークフロー実行の詳細取得
- **github-mcp-server-get_job_logs**: ジョブログの取得
- **view**: ワークフローYMLファイルの確認
- **bash**: コマンド実行、エラー再現、検証
- **edit**: コードやワークフローの修正
- **grep**: エラー関連コードの検索

## 使用すべきタイミング

以下の場合にこのスキルを使用してください:

- GitHub Actionsワークフローが失敗した場合
- CI/CDパイプラインでエラーが発生した場合
- ワークフローのトラブルシューティングを依頼された場合

## 実行手順

### 1. エラー内容の確認

#### 1.1 ワークフロー実行履歴の取得

**効率的な調査のための優先順位**:

1. **URLが直接指定されている場合**: そのワークフロー実行のみを確認する
2. **PRベースの調査**:
   - PRが明示的に指定されている場合: そのPRがトリガーとなっているワークフローのみを調査対象
   - PRが指定されていない場合: エージェントが作業するブランチに紐づくPRがトリガーとなっているワークフローのみを調査対象
   - 直近のワークフロー実行から確認
   - 同一ジョブ名の重複は調査対象としない（最新のもののみ）
   - **最大5件まで**とする

**実行例**:

```
# 1. URLが指定されている場合（最優先）
# URLからrun_idを抽出して直接取得
get_workflow_run --method=get_workflow_run --owner=<owner> --repo=<repo> --resource_id=<run_id>

# 2. PRベースの調査
# PRが明示的に指定されている場合（例: PR #123）
# まずPR情報からブランチ名を取得し、そのブランチのワークフロー実行を検索
# GitHub MCP Serverでブランチ名を使用してフィルタリング
list_workflow_runs --owner=<owner> --repo=<repo> --workflow_runs_filter='{"event": "pull_request", "branch": "<pr-branch-name>"}' --per_page=5

# PRが指定されていない場合は作業ブランチからPR番号を特定
# Step 1: 作業ブランチ名を取得
# git branch --show-current
# Step 2: そのブランチ名でフィルタリング
list_workflow_runs --owner=<owner> --repo=<repo> --workflow_runs_filter='{"event": "pull_request", "branch": "<current-branch-name>"}' --per_page=5
```

**注**: 
- `<owner>`と`<repo>`は実際のリポジトリのオーナー名とリポジトリ名に置き換えてください
- `<run_id>`はワークフローURLから抽出（例: `https://github.com/owner/repo/actions/runs/12345` → `12345`）
- `<pr-branch-name>`は指定されたPRのブランチ名に置き換えてください
- `<current-branch-name>`は`git branch --show-current`で取得した現在のブランチ名に置き換えてください

エラーとなったワークフロー実行を特定し、以下の情報を記録:
- ワークフロー名
- 実行ID（run_id）
- 失敗したジョブ名
- エラー発生時刻

**調査対象の絞り込み**:
- 失敗ステータス（`conclusion: failure`）のみを対象
- 既に調査したジョブ名は重複調査を避ける
- 最大5件までに制限して調査時間を短縮

#### 1.2 エラーログの取得

```
# 失敗したジョブのログを取得
get_job_logs --owner=<owner> --repo=<repo> --run_id=<run_id> --failed_only=true --return_content=true
```

エラーログから以下を抽出:
- エラーメッセージ
- スタックトレース
- 失敗したステップ名
- エラーコード

#### 1.3 エラーの分類

エラーを以下のカテゴリに分類:
- **依存関係エラー**: パッケージインストールの失敗
- **ビルドエラー**: コンパイル、トランスパイルの失敗
- **テストエラー**: テストケースの失敗
- **Lintエラー**: コードスタイル、型チェックの失敗
- **環境エラー**: Node.jsバージョン、権限、証明書の問題
- **設定エラー**: ワークフローYML、パッケージ設定の問題

### 2. ワークフローYMLでの再現手順確認

#### 2.1 ワークフローファイルの確認

```bash
# ワークフローファイルを確認
view .github/workflows/<workflow-name>.yml
```

以下の項目を確認:
- トリガー条件（on:）
- 実行環境（runs-on:）
- Node.jsバージョン（node-version:）
- 失敗したステップのコマンド
- 環境変数の設定

#### 2.2 再現手順の特定

失敗したステップのコマンドを特定:

```yaml
# 例: Lintステップの場合
- name: Run lint
  run: npm run lint
```

ローカルで実行可能なコマンドに変換:
- `npm ci` → 依存関係のインストール
- `npm run lint` → Lintの実行
- `npm test` → テストの実行
- `npm run build` → ビルドの実行

### 3. エラーの再現

#### 3.1 環境の準備

```bash
# 現在のブランチとクリーンな状態を確認
git status
git --no-pager log -1 --oneline
```

#### 3.2 依存関係のインストール

```bash
# package-lock.jsonの存在確認
ls -la package-lock.json

# 依存関係をクリーンインストール
npm ci
```

エラーが発生した場合:
- package-lock.jsonの問題
- Node.jsバージョンの不一致
- ネットワークやレジストリの問題

#### 3.3 失敗したステップの実行

```bash
# 失敗したコマンドを実行
npm run <command>
```

エラーの再現を確認:
- エラーメッセージが一致するか
- エラーの発生箇所が同じか
- スタックトレースが同じか

#### 3.4 詳細なログの取得

```bash
# より詳細なログで実行
npm run <command> --verbose

# または特定のファイル/テストのみ実行
npm run lint -- <specific-file>
npm test -- <specific-test-file>
```

### 4. 原因の特定と対処

#### 4.1 原因の分析

エラーログとコードを分析し、根本原因を特定:

**依存関係エラーの場合**:
- パッケージバージョンの不一致
- 依存関係の欠落
- package.jsonとpackage-lock.jsonの不整合

**ビルドエラーの場合**:
- 型エラー（TypeScript）
- 構文エラー
- インポートエラー
- 設定ファイルの問題（tsconfig.json等）

**テストエラーの場合**:
- テストロジックの問題
- モックの設定ミス
- 非同期処理のハンドリングミス

**Lintエラーの場合**:
- コードスタイルの問題
- 未使用変数・インポート
- 型定義の不足

**環境エラーの場合**:
- Node.jsバージョンの不一致
- 環境変数の欠落
- 権限やパスの問題

#### 4.2 対処の実施

##### コード修正の場合

```bash
# 問題のあるファイルを確認
view <file-path>

# エラー箇所を修正
edit <file-path>
```

##### 依存関係の修正の場合

```bash
# パッケージの追加
npm install <package-name>

# パッケージの更新
npm update <package-name>

# package-lock.jsonの再生成
rm package-lock.json
npm install
```

##### 設定ファイルの修正の場合

```bash
# 設定ファイルを確認
view tsconfig.json
# または
view .eslintrc.js

# 設定を修正
edit <config-file>
```

##### ワークフローの修正の場合

```bash
# ワークフローファイルを確認
view .github/workflows/<workflow-name>.yml

# ワークフローを修正
edit .github/workflows/<workflow-name>.yml
```

### 5. エラーが再現しない事を確認

#### 5.1 修正後の再実行

```bash
# 失敗したコマンドを再実行
npm run <command>
```

確認項目:
- ✅ エラーが発生しないこと
- ✅ 正常に完了すること
- ✅ 期待される出力が得られること

#### 5.2 複数回の実行

```bash
# 偶発的な成功ではないことを確認
npm run <command>
npm run <command>
```

安定して成功することを確認。

### 6. 他のステップの成功確認

#### 6.1 ローカルで検証可能なステップの実行

ワークフローの他のステップも実行し、全体が正常に動作することを確認:

```bash
# Lint
npm run lint

# Test
npm test

# Build
npm run build
```

各ステップの結果を記録:
- ✅ 成功: 問題なし
- ⚠️ 警告あり: 内容を確認
- ❌ 失敗: 追加対応が必要

#### 6.2 プレマージチェック（推奨）

可能であれば、プレマージワークフローをローカルで実行:

```bash
# actツールがインストールされている場合
npm run premerge:local
```

または、個別に各ステップを実行:

```bash
# 依存関係のクリーンインストール
npm ci

# Lint実行
npm run lint

# テスト実行
npm test

# ビルド実行
npm run build
```

### 7. 依頼者への説明

以下の形式で報告を作成:

#### 7.1 エラー概要

```
## エラー概要

**ワークフロー**: <ワークフロー名>
**失敗したジョブ**: <ジョブ名>
**失敗したステップ**: <ステップ名>
**エラー発生時刻**: <時刻>

**エラーメッセージ**:
```
<エラーメッセージを引用>
```
```

#### 7.2 原因の説明

```
## 原因

<エラーの根本原因を説明>

**分類**: <依存関係/ビルド/テスト/Lint/環境/設定>

**詳細**:
- <原因の詳細1>
- <原因の詳細2>
- <原因の詳細3>
```

#### 7.3 対応内容

```
## 対応内容

以下の修正を実施しました:

### 修正1: <修正内容のタイトル>
**ファイル**: `<ファイルパス>`
**変更内容**:
- <変更内容1>
- <変更内容2>

### 修正2: <修正内容のタイトル>
**ファイル**: `<ファイルパス>`
**変更内容**:
- <変更内容1>
- <変更内容2>
```

#### 7.4 検証結果

```
## 検証結果

### エラーの再現テスト
- ✅ エラーが再現しないことを確認

### 全ステップの検証
- ✅ `npm run lint`: 成功
- ✅ `npm test`: 成功
- ✅ `npm run build`: 成功

### 実行ログ
```
<主要な実行結果のログを抜粋>
```
```

#### 7.5 コミットへのリンク

```
## コミット

Commit: [<短縮SHA>](https://github.com/<owner>/<repo>/commit/<完全SHA>)
```

**注**: `<owner>`、`<repo>`、`<短縮SHA>`、`<完全SHA>`は実際の値に置き換えてください。

## エラー別対応例

### 例1: 依存関係インストールエラー

**エラーメッセージ**:
```
npm error code ERESOLVE
npm error ERESOLVE unable to resolve dependency tree
```

**原因**: パッケージバージョンの競合

**対処**:
1. package-lock.jsonを削除
2. `npm install`で再生成
3. 必要に応じてpackage.jsonのバージョン指定を調整

### 例2: TypeScript型エラー

**エラーメッセージ**:
```
error TS2345: Argument of type 'string' is not assignable to parameter of type 'number'.
```

**原因**: 型の不一致

**対処**:
1. エラー箇所のコードを確認
2. 型定義を修正または型アサーションを追加
3. `npm run build`で再検証

### 例3: テスト失敗

**エラーメッセージ**:
```
Expected: 5
Received: 4
```

**原因**: テストの期待値とロジックの不一致

**対処**:
1. テストコードとプロダクションコードを確認
2. ロジックが正しい場合はテストを修正
3. テストが正しい場合はロジックを修正
4. `npm test`で再検証

### 例4: ESLintエラー

**エラーメッセージ**:
```
error  'unusedVar' is defined but never used  no-unused-vars
```

**原因**: 未使用変数の存在

**対処**:
1. 未使用変数を削除
2. または変数名を`_unusedVar`に変更（意図的な未使用）
3. `npm run lint`で再検証

### 例5: Node.jsバージョン不一致

**エラーメッセージ**:
```
The engine "node" is incompatible with this module.
Expected version ">=24.0.0". Got "18.0.0"
```

**原因**: Node.jsバージョンの不一致（ワークフローがNode.js 24を要求しているが、ローカル環境が18を使用）

**対処**:
1. `.nvmrc`やpackage.jsonの`engines`フィールドを確認
2. ワークフローの`node-version`を確認
3. 必要に応じてバージョンを統一
4. ローカル環境でNode.jsバージョンを切り替え

## ベストプラクティス

### エラー対応の原則

1. **体系的なアプローチ**
   - 手順に従って順番に対応
   - 推測ではなく、ログとコードで確認

2. **最小限の変更**
   - 問題の原因のみを修正
   - 無関係なコードは変更しない

3. **完全な検証**
   - エラーの解消だけでなく、他への影響も確認
   - 複数回の実行で安定性を確認

4. **明確な説明**
   - エラー、原因、対処、検証を明確に記録
   - 再現可能な形で説明

### トラブルシューティング

#### ログが不十分な場合

```bash
# より詳細なログを出力
npm run <command> --verbose
# または
DEBUG=* npm run <command>
```

#### ローカルで再現しない場合

- ワークフローの環境変数を確認
- Node.jsバージョンを確認
- OSの違いを確認（Ubuntu vs macOS vs Windows）
- キャッシュの影響を確認

#### 複数のエラーがある場合

1. まず最初に発生したエラーに対応
2. 1つずつ順番に解決
3. 各修正後に全体を検証

## GitHub MCP Server ツールの使用

### ワークフロー情報の取得

```javascript
// ワークフロー一覧の取得
list_workflows({
  method: "list_workflows",
  owner: "<owner>",
  repo: "<repo>"
})

// ワークフロー実行履歴の取得
list_workflow_runs({
  method: "list_workflow_runs",
  owner: "<owner>",
  repo: "<repo>",
  resource_id: "premerge.yml", // ワークフローファイル名
  per_page: 10
})

// 特定の実行の詳細取得
get_workflow_run({
  method: "get_workflow_run",
  owner: "<owner>",
  repo: "<repo>",
  resource_id: "<run_id>"
})
```

### ジョブログの取得

```javascript
// 失敗したジョブのログを取得
get_job_logs({
  owner: "<owner>",
  repo: "<repo>",
  run_id: <run_id>,
  failed_only: true,
  return_content: true,
  tail_lines: 500
})

// 特定ジョブのログを取得
get_job_logs({
  owner: "<owner>",
  repo: "<repo>",
  job_id: <job_id>,
  return_content: true,
  tail_lines: 1000
})
```

## 注意事項

- **セキュリティ**: シークレットやクレデンシャルをログに出力しない
- **最小変更**: 問題の原因のみを修正し、無関係な変更は避ける
- **既存の問題**: タスクと無関係な既存のエラーは修正しない
- **バージョン管理**: 変更は適切にコミットし、説明を残す

## 参考資料

- ワークフロー定義: `.github/workflows/`
- プレマージチェックスキル: `premerge-check/SKILL.md`
- GitHub Actions ドキュメント: https://docs.github.com/en/actions
- Copilotインストラクション: `.github/copilot-instructions.md`
