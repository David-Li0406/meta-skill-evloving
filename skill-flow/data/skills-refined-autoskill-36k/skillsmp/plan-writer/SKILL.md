---
name: plan-writer
description: 実装計画を作成する際にtmp/配下にファイルを配置するようガイドします。docs/への不要なドキュメント生成を防ぎ、一時的な計画ファイルを適切に管理します。
---

# Plan Writer（実装計画作成ガイド）

## 目的

実装計画や調査結果などの一時的なドキュメントを作成する際に、`tmp/`ディレクトリに配置するようガイドします。これにより、`docs/`ディレクトリの肥大化を防ぎ、プロジェクトのドキュメント構造を維持します。

## いつアクティベートするか

このスキルは以下の場合に自動的にアクティベートされます：

- 実装計画を作成する時
- 調査結果をドキュメント化する時
- 一時的な分析結果を保存する時
- Issue解決のための計画を立てる時
- 新機能の設計を検討する時

## クイックチェックリスト

計画ファイルを作成する前に：

- [ ] **ファイルは`tmp/`ディレクトリに配置するか確認**
- [ ] **ファイル名は`implementation_plan_{issue_number}.md`または`{task_name}_plan.md`形式**
- [ ] **docs/には絶対に計画ファイルを作成しない**

計画完了後：

- [ ] **実装が完了したら計画ファイルを削除**
- [ ] **永続的に残すべき情報はADRまたは既存ドキュメントに統合**

## ファイル配置ルール

### tmp/に配置するもの（一時ファイル）

```
tmp/
├── implementation_plan_123.md       # Issue #123の実装計画
├── investigation_report_456.md      # Issue #456の調査結果
├── design_proposal_feature_x.md     # 機能Xの設計提案
├── analysis_results_20260108.md     # 日付付きの分析結果
└── refactoring_plan.md              # リファクタリング計画
```

**特徴**:
- 一時的なドキュメント
- 実装完了後に削除される
- gitignoreされている（コミットされない）
- 作業中のみ必要

### docs/に配置するもの（永続ファイル）

```
docs/
├── ADR/                    # アーキテクチャ決定記録
├── architecture/           # 層別実装ガイド
├── diagrams/               # アーキテクチャ図
├── monitoring/             # 監視設定ガイド
├── ARCHITECTURE.md         # システムアーキテクチャ
├── BI_DASHBOARD.md         # BIダッシュボード
├── CLEAN_ARCHITECTURE_MIGRATION.md
├── DEPLOYMENT.md           # デプロイ手順
└── DEVELOPMENT_GUIDE.md    # 開発ガイド
```

**特徴**:
- 永続的なドキュメント
- プロジェクト全体で参照される
- gitで管理される
- 定期的にメンテナンスされる

## ファイル名規則

### 実装計画
```
tmp/implementation_plan_{issue_number}.md
例: tmp/implementation_plan_895.md
```

### 調査結果
```
tmp/investigation_{topic}.md
例: tmp/investigation_performance_issue.md
```

### 設計提案
```
tmp/design_{feature_name}.md
例: tmp/design_new_api_endpoint.md
```

### 分析結果
```
tmp/analysis_{topic}_{date}.md
例: tmp/analysis_database_performance_20260108.md
```

## 禁止事項

### docs/に作成してはいけないもの

- 実装計画 (`IMPLEMENTATION_PLAN_*.md`)
- 調査結果 (`INVESTIGATION_*.md`)
- 一時的な分析 (`ANALYSIS_*.md`)
- 作業中のメモ (`NOTES_*.md`)
- 個人的なドキュメント

### 理由

1. **docs/の肥大化を防ぐ**: 不要なファイルが蓄積される
2. **混乱を防ぐ**: 一時ファイルと永続ファイルが混在する
3. **メンテナンス負荷を減らす**: 不要なファイルの削除作業が発生する
4. **CIチェックをパスする**: 規定外のファイルはCIで検出される

## 計画から永続ドキュメントへの昇格

一時的な計画が永続的なドキュメントになるべき場合：

1. **Architecture Decision Record (ADR)**
   - 重要なアーキテクチャ決定は`docs/ADR/`に追加
   - 形式: `NNNN-kebab-case-title.md`

2. **開発ガイドへの統合**
   - 汎用的な開発プラクティスは`docs/DEVELOPMENT_GUIDE.md`に追加

3. **層別ガイドへの統合**
   - 層固有のガイドは該当する`docs/architecture/*.md`に追加

## テンプレート

### 実装計画テンプレート

```markdown
# Issue #{issue_number} 実装計画

## 背景

[問題の背景を説明]

## 受け入れ基準

[Issueの受け入れ基準を記載]

## 実装タスク

1. タスク1
2. タスク2
3. タスク3

## 技術的決定

[主要な技術的決定を記載]

## リスクと注意点

[潜在的なリスクを記載]
```

## 関連スキル

- `skill-design-principles`: SKILLの設計原則
- `temp-file-management`: 一時ファイル管理
- `project-conventions`: プロジェクト規約
