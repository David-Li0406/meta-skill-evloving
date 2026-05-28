---
name: feature-modification-and-bug-fixing
description: Use this skill when you need to define requirements, analyze impacts, and create task lists for new features, modifications, or bug fixes.
---

# Feature Modification and Bug Fixing Command

このコマンドは、新機能の要件定義、既存機能の修正、バグ修正に向けて、対話形式で以下を行います:

1. **要件定義 / 変更要求 / バグ情報収集**: ユーザーとの対話で要件や変更内容、バグの症状を明確化
2. **技術設計 / 影響分析 / 原因調査**: DB・API・UI の設計を決定し、既存コードへの影響範囲を分析
3. **タスクリスト作成**: TDD実装のためのタスク一覧を作成

**このコマンドは設計まで。実装は `/implement-feature` で行います。**

## 実行条件

**Planモードでは実行不可**

このスキルはファイル作成・Git操作を伴うため、Planモードでは実行できません。
Planモード中に実行された場合は、以下のメッセージを表示して終了:

```
このコマンドはPlanモードでは実行できません。
Planモードを終了してから再度実行してください。
```

---

## 出力ファイル

```
docs/steering/{YYYYMMDD}-{action}-{feature-name}/
├── progress.md          # プロセス進捗（各ステップで作成）
├── requirements.md      # 要件定義または変更要求（Phase 1で作成）
├── design.md            # 技術設計（Phase 2で作成）
├── impact-analysis.md    # 影響分析（Phase 2で作成）
├── investigation.md      # 調査結果（Phase 1で作成）
├── fix-plan.md          # 修正計画（Phase 2で作成）
└── tasklist.md          # タスクリスト（Phase 3で作成）
```

命名例: `docs/steering/20260113-modify-user-profile/`

---

## 開始前の準備

main ブランチが最新であることを確認:

```bash
git checkout main && git pull origin main
```

---

## Phase 1: 要件定義 / 変更要求 / バグ情報収集

### Step 1: 初期入力の受け取り

ユーザーが自由形式で入力できるように促す:

```
新機能の実装、既存機能の修正、またはバグ修正を始めましょう！

どのような機能を作りたいですか？または、どの機能をどう変更したいですか？バグが発生している場合は、その症状を教えてください。
```

### Step 2: 初期入力の解釈と確認

ユーザーの回答を受け取ったら:

1. AIが内容を解釈・整理
2. 理解内容を要約して提示
3. 不足情報があれば質問

```
ありがとうございます！いくつか確認させてください。

---
### 現時点での理解

**やりたいこと / 対象機能**: {AIが解釈した内容を1-2文で要約}

---

では、詳しく教えてください。

{不足情報への質問}
```

### Step 3: ステアリングディレクトリの作成

ユーザーの回答をもとに:

1. 日付取得（`date +%Y%m%d`）、機能名をkebab-caseに変換
2. `docs/steering/{YYYYMMDD}-{action}-{feature-name}/` ディレクトリを作成
3. テンプレートからファイル作成:
   - `progress.md`（テンプレート: `.claude/skills/{action}/templates/progress-template.md`）
   - `requirements.md` または `change-request.md`（テンプレート: `.claude/skills/{action}/templates/requirements-template.md`）
   - `investigation.md`（バグ修正の場合）
4. 収集した情報を各ファイルに記入

### Step 4: 影響度と環境の確認（バグ修正の場合）

```
次に、バグの影響度と発生環境を確認します。

**影響度**:
- Critical: サービス停止、データ損失
- High: 主要機能が使用不可
- Medium: 機能の一部が使用不可、回避策あり
- Low: 軽微な不具合

**発生環境**:
- ブラウザ / OS は何ですか？
- 本番環境 / 開発環境 / 両方で発生しますか？

それぞれ教えてください。
```

回答を得たら、`investigation.md` の「4. 発生環境」セクションを更新。

### Step 5: 各ドキュメントのレビュー

`requirements.md` または `investigation.md` の内容をユーザーに提示してレビューを依頼:

```
要件定義ドキュメントを作成しました。

📄 **ファイル**: `docs/steering/{YYYYMMDD}-{action}-{feature-name}/requirements.md`

内容を確認してください。修正が必要な場合はお知らせください。
問題なければ「承認」と入力してください。
```

ユーザーが「承認」と回答したら、次のフェーズに進む。

---

## Phase 2: 技術設計 / 影響分析 / 原因調査

### Step 6: コードベース調査（file-finder エージェント）

```
技術設計または原因調査に入ります。関連する既存コードを調査します。
🔍 **file-finder エージェントを実行します（独立コンテキスト）**
```

→ file-finder エージェントへの入力:
  - 機能名/キーワード: {対象の機能名}
  - 検索範囲: src/app/api/, src/components/, src/hooks/, src/types/
  - 検索目的: 技術設計またはバグ原因調査

調査結果を `investigation.md` または `impact-analysis.md` に反映。

### Step 7: 影響範囲分析（impact-analyzer エージェント）

```
関連コードを調査しました。次に、変更の影響範囲を分析します。
🔍 **impact-analyzer エージェントを実行します（独立コンテキスト）**
```

→ impact-analyzer エージェントへの入力:
  - 変更内容: {変更概要}
  - 変更対象ファイル: {変更予定のファイルパス}
  - 分析観点: 破壊的変更、関連機能への影響

分析結果を `impact-analysis.md` に記録。

### Step 8: 修正計画の策定（バグ修正の場合）

```
原因と影響範囲が明確になりました。修正計画を策定しましょう。

**修正方針の検討**:
考慮事項:
- 最小限の変更で修正できるか
- 同様のバグを防ぐための対策が必要か
- ロールバックが必要になった場合の対応
```

対話を通じて以下を決定:

- 修正方針
- テスト計画
- ロールバック計画

決定後、`fix-plan.md` を作成。

### Step 9: 各ドキュメントのレビュー

`design.md` または `fix-plan.md` の内容をユーザーに提示してレビューを依頼:

```
技術設計ドキュメントを作成しました。

📄 **ファイル**: `docs/steering/{YYYYMMDD}-{action}-{feature-name}/design.md`

内容を確認してください。修正が必要な場合はお知らせください。
問題なければ「承認」と入力してください。
```

ユーザーが「承認」と回答したら、実装計画に進む。

---

## Phase 3: 実装計画

### Step 10: タスクリスト作成

```
実装計画を策定しましょう。

**変更タイプの確認**:
この修正はどのタイプに該当しますか？

A. **フロントエンドのみ**: UIコンポーネント、表示変更
B. **バックエンドのみ**: APIエンドポイント変更、ロジック修正
C. **フルスタック**: API + UI の両方に影響
D. **複合変更**: 複数機能にまたがる変更
```

変更タイプが決まったら、該当するテンプレートで `tasklist.md` を作成。

### Step 11: 最終確認と実装開始案内

すべてのファイルが揃ったら:

```
ステアリングファイルが完成しました！

📁 **ステアリングディレクトリ**: `docs/steering/{YYYYMMDD}-{action}-{feature-name}/`

| ファイル | 内容 |
|----------|------|
| requirements.md | 要件定義または変更要求 |
| design.md | 技術設計 |
| impact-analysis.md | 影響分析 |
| fix-plan.md | 修正計画 |
| tasklist.md | タスクリスト |

---

## サマリー

- **対象機能**: {機能名}
- **影響度**: {Critical/High/Medium/Low}
- **変更ファイル数**: {概算}

### 推奨エージェントフロー
file-finder → impact-analyzer → [実装] → test-runner → code-reviewer

---

```

### Step 12: ブランチ作成とコミット

設計ドキュメントをバージョン管理に登録:

1. フィーチャーブランチを作成:
   ```bash
   git checkout -b {action}/{YYYYMMDD}-{feature-name}
   ```

2. ステアリングディレクトリをコミット:
   ```bash
   git add docs/steering/{YYYYMMDD}-{action}-{feature-name}/
   git commit -m "docs: add steering documents for {action}-{feature-name}"
   ```

3. 完了メッセージを表示:
   ```
   ✅ 設計フェーズが完了しました！

   📁 **ブランチ**: `{action}/{YYYYMMDD}-{feature-name}`
   📄 **コミット済み**: ステアリングドキュメント一式

   実装を開始する場合は `/implement-feature` を実行してください。
   ```

---

## ステータス遷移

| ファイル | 初期値 | 主な遷移 |
|----------|--------|----------|
| progress.md | Phase 1 | Phase 1 → 2（Step 5承認後）→ 3（Step 11承認後）→ 完了（Step 12） |
| requirements.md | 作成中 | → 要件確定（Step 5承認後） |
| design.md | 設計中 | → 設計確定（Step 9承認後） |
| impact-analysis.md | 分析中 | → 分析完了（Step 8承認後） |
| investigation.md | 調査中 | → 原因特定済み（Step 7） |
| fix-plan.md | 計画中 | → 確定（Step 9承認後） |
| tasklist.md | 計画中 | → 計画確定（Step 12） |

---

## 注意事項

- ディレクトリは Step 3 で即座に作成し、以降のファイルは随時追加・更新する
- 各ステップでユーザーの回答を待ってから次に進む
- 既存のコードパターンに従った設計を提案する
- 技術的な判断が必要な場合は、CLAUDE.md を参照する
- 対話が中断されても、途中まで入力した内容はファイルに保存されている
- 設計完了後、実装は `/implement-feature` で行う
- 完了後、`mv docs/steering/{dir} docs/steering/archive/` でアーカイブ