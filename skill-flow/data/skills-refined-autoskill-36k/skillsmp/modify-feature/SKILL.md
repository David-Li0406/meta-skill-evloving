---
name: modify-feature
description: 既存機能修正の変更要求・影響分析・タスクリスト作成まで行うコマンド
---

# Modify Feature Command

既存機能の修正・改善に向けて、対話形式で以下を行うコマンドです:

1. **変更要求**: ユーザーとの対話で変更内容を明確化
2. **影響分析**: 既存コードへの影響範囲を分析
3. **タスクリスト作成**: 実装のためのタスク一覧を作成

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
docs/steering/{YYYYMMDD}-modify-{feature-name}/
├── progress.md          # プロセス進捗（Step 3で作成）
├── change-request.md    # 変更要求（Step 3で作成）
├── impact-analysis.md   # 影響分析（Step 7で作成）
└── tasklist.md          # タスクリスト（Step 9で作成）
```

命名例: `docs/steering/20260113-modify-user-profile/`

---

## スキップ条件

CLAUDE.md の「実装ワークフロー」セクションに記載の例外条件に従う。

---

## 開始前の準備

main ブランチが最新であることを確認:

```bash
git checkout main && git pull origin main
```

---

## Phase 1: 変更要求確認

### Step 1: 初期入力の受け取り

ユーザーが自由形式で入力できるように促す:

```
既存機能の修正を始めましょう！

どの機能をどう変更したいですか？
自由に教えてください。「〇〇の動作を△△に変えたい」「□□がうまく動かない」など、何でもOKです。
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

**対象機能**: {AIが解釈した対象機能}
**変更内容**: {AIが解釈した変更内容を1-2文で要約}

---

では、詳しく教えてください。

{不足情報への質問（例: 変更理由、現在の動作、期待する動作など）}
```

確認すべき項目（不足していれば質問）:
- 対象機能
- 変更理由
- 現在の動作
- 変更後の動作

### Step 3: ステアリングディレクトリの作成

ユーザーの回答をもとに:

1. 日付取得（`date +%Y%m%d`）、機能名をkebab-caseに変換
2. `docs/steering/{YYYYMMDD}-modify-{feature-name}/` ディレクトリを作成
3. テンプレートからファイル作成:
   - `progress.md`（テンプレート: `.claude/skills/modify-feature/templates/progress-template.md`）
   - `change-request.md`（テンプレート: `.claude/skills/modify-feature/templates/change-request-template.md`）
4. 変更概要・理由・内容を記入

### Step 4: 後方互換性・成功指標の確認

```
次に、後方互換性と成功指標を確認します。

**後方互換性**: 既存の動作が変わりますか？移行対応は必要ですか？
**成功指標**: 何が改善され、どう測定しますか？

それぞれ教えてください。
```

回答を得たら、`change-request.md` を更新。

### Step 5: change-request.md のレビュー

`change-request.md` の内容をユーザーに提示してレビューを依頼:

```
変更要求ドキュメントを作成しました。

📄 **ファイル**: `docs/steering/{YYYYMMDD}-modify-{feature-name}/change-request.md`

内容を確認してください。修正が必要な場合はお知らせください。
問題なければ「承認」と入力してください。
```

ユーザーが「承認」と回答したら、影響分析に進む。

---

## Phase 2: 影響分析

### Step 6: コードベース調査（file-finder エージェント）

```
影響分析に入ります。関連する既存コードを調査します。
🔍 **file-finder エージェントを実行します（独立コンテキスト）**
```

→ file-finder エージェントへの入力:
  - 機能名/キーワード: {変更対象の機能名}
  - 検索範囲: src/app/api/, src/components/, src/hooks/, src/types/
  - 検索目的: 変更影響の調査

調査結果をユーザーに報告。

### Step 7: 影響範囲分析（impact-analyzer エージェント）

```
関連コードを調査しました。次に、変更の影響範囲を分析します。
🔍 **impact-analyzer エージェントを実行します（独立コンテキスト）**
```

→ impact-analyzer エージェントへの入力:
  - 変更内容: {変更概要}
  - 変更対象ファイル: {変更予定のファイルパス}
  - 分析観点: 破壊的変更、関連機能への影響

分析結果を `impact-analysis.md` に記録（テンプレート: `.claude/skills/modify-feature/templates/impact-analysis-template.md`）

記入セクション:
- 影響を受けるコンポーネント
- リスク評価
- テスト戦略

### Step 8: impact-analysis.md のレビュー

`impact-analysis.md` の内容をユーザーに提示してレビューを依頼:

```
影響分析ドキュメントを作成しました。

📄 **ファイル**: `docs/steering/{YYYYMMDD}-modify-{feature-name}/impact-analysis.md`

内容を確認してください。修正が必要な場合はお知らせください。
問題なければ「承認」と入力してください。
```

ユーザーが「承認」と回答したら、実装計画に進む。

---

## Phase 3: 実装計画

### Step 9: タスクリスト作成

```
実装計画を策定しましょう。

**変更タイプの確認**:
この修正はどのタイプに該当しますか？

A. **フロントエンドのみ**: UIコンポーネント、表示変更
B. **バックエンドのみ**: APIエンドポイント変更、ロジック修正
C. **フルスタック**: API + UI の両方に影響
D. **複合変更**: 複数機能にまたがる変更
```

変更タイプが決まったら、該当するテンプレートで `tasklist.md` を作成:
- テンプレート: `.claude/skills/modify-feature/templates/tasklist.md`

### Step 10: 最終確認と実装開始案内

すべてのファイルが揃ったら:

```
ステアリングファイルが完成しました！

📁 **ステアリングディレクトリ**: `docs/steering/{YYYYMMDD}-modify-{feature-name}/`

| ファイル | 内容 |
|----------|------|
| change-request.md | 変更要求（対象、理由、変更内容） |
| impact-analysis.md | 影響分析（破壊的変更、リスク） |
| tasklist.md | タスクリスト |

---

## サマリー

- **対象機能**: {機能名}
- **破壊的変更**: {あり/なし}
- **リスクレベル**: {低/中/高}

### 推奨エージェントフロー
file-finder → impact-analyzer → [実装] → test-runner → code-reviewer

---

```

### Step 11: ブランチ作成とコミット

設計ドキュメントをバージョン管理に登録:

1. モディファイブランチを作成:
   ```bash
   git checkout -b modify/{YYYYMMDD}-{feature-name}
   ```

2. ステアリングディレクトリをコミット:
   ```bash
   git add docs/steering/{YYYYMMDD}-modify-{feature-name}/
   git commit -m "docs: add steering documents for modify-{feature-name}"
   ```

3. 完了メッセージを表示:
   ```
   ✅ 設計フェーズが完了しました！

   📁 **ブランチ**: `modify/{YYYYMMDD}-{feature-name}`
   📄 **コミット済み**: ステアリングドキュメント一式

   実装を開始する場合は `/implement-feature` を実行してください。
   ```

---

## ステータス遷移

| ファイル | 初期値 | 主な遷移 |
|----------|--------|----------|
| progress.md | Phase 1 | Phase 1 → 2（Step 5承認後）→ 3（Step 8承認後）→ 完了（Step 11） |
| change-request.md | ヒアリング中 | → 要求確定（Step 5承認後） |
| impact-analysis.md | 分析中 | → 分析完了（Step 8承認後） |
| tasklist.md | 計画中 | → 計画確定（Step 11） |

---

## 注意事項

- ディレクトリは Step 3 で即座に作成し、以降のファイルは随時追加・更新する
- 各ステップでユーザーの回答を待ってから次に進む
- 後方互換性を最大限維持することを優先する
- 技術的な判断が必要な場合は、CLAUDE.md を参照する
- 対話が中断されても、途中まで入力した内容はファイルに保存されている
- 設計完了後、実装は `/implement-feature` で行う
- 完了後、`mv docs/steering/{dir} docs/steering/archive/` でアーカイブ
