---
name: fix-bug
description: バグ調査・原因特定・修正計画の作成まで行うコマンド
---

# Fix Bug Command

バグ修正に向けて、対話形式で以下を行うコマンドです:

1. **バグ情報収集**: ユーザーとの対話でバグの症状を明確化
2. **原因調査**: コードベース調査と影響範囲分析
3. **修正計画作成**: 修正方針とタスクリストを作成

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
docs/steering/{YYYYMMDD}-fix-{bug-name}/
├── progress.md        # プロセス進捗（Step 3 で作成）
├── investigation.md   # 調査結果（Step 3 で作成、Step 4-7 で更新）
├── fix-plan.md        # 修正計画（Step 8 で作成）
└── tasklist.md        # タスクリスト（Step 10 で作成）
```

命名例: `docs/steering/20260113-fix-login-error/`

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

## Phase 1: バグ情報収集

### Step 1: 初期入力の受け取り

ユーザーが自由形式で入力できるように促す:

```
バグ修正を始めましょう！

どんな問題が発生していますか？
自由に教えてください。「〇〇すると△△になる」「□□が動かない」など、何でもOKです。
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

**症状**: {AIが解釈したバグの症状}
**発生条件**: {AIが解釈した発生条件を1-2文で要約}

---

では、詳しく教えてください。

{不足情報への質問（例: 再現手順、期待動作、実際の動作など）}
```

確認すべき項目（不足していれば質問）:
- バグの症状
- 再現手順
- 期待動作
- 実際の動作

### Step 3: ステアリングディレクトリの作成

ユーザーの回答をもとに:

1. 日付取得（`date +%Y%m%d`）、バグ名をkebab-caseに変換
2. `docs/steering/{YYYYMMDD}-fix-{bug-name}/` ディレクトリを作成
3. テンプレートからファイル作成:
   - `progress.md`（テンプレート: `.claude/skills/fix-bug/templates/progress-template.md`）
   - `investigation.md`（テンプレート: `.claude/skills/fix-bug/templates/investigation-template.md`）
4. 「1. バグ概要」「2. 再現手順」「3. 期待動作 vs 実際の動作」セクションを埋める

### Step 4: 影響度と環境の確認

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

### Step 5: investigation.md のレビュー（Phase 1 完了時）

`investigation.md` の内容をユーザーに提示してレビューを依頼:

```
バグ情報をまとめました。

📄 **ファイル**: `docs/steering/{YYYYMMDD}-fix-{bug-name}/investigation.md`

内容を確認してください。修正が必要な場合はお知らせください。
問題なければ「承認」と入力してください。
```

ユーザーが「承認」と回答したら、原因調査に進む。

---

## Phase 2: 原因調査

### Step 6: コードベース調査（file-finder エージェント）

```
原因調査に入ります。関連する既存コードを調査します。
🔍 **file-finder エージェントを実行します（独立コンテキスト）**
```

→ file-finder エージェントへの入力:
  - 機能名/キーワード: {バグに関連する機能名}
  - 検索範囲: src/app/api/, src/components/, src/hooks/, src/types/
  - 検索目的: バグ原因調査

調査結果を `investigation.md` の「5. 原因分析」セクションに反映。

### Step 7: 影響範囲分析（impact-analyzer エージェント）

```
原因が特定できました。次に、修正の影響範囲を分析します。
🔍 **impact-analyzer エージェントを実行します（独立コンテキスト）**
```

→ impact-analyzer エージェントへの入力:
  - 変更内容: {修正予定の変更概要}
  - 変更対象ファイル: {修正予定のファイルパス}
  - 分析観点: 修正による副作用、関連機能への影響

分析結果を `investigation.md` の「6. 影響範囲」セクションに反映。
ステータスを `原因特定済み` に変更。

### Step 8: 修正計画の策定

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

決定後、`fix-plan.md` を作成（テンプレート: `.claude/skills/fix-bug/templates/fix-plan-template.md`）

### Step 9: fix-plan.md のレビュー

`fix-plan.md` の内容をユーザーに提示してレビューを依頼:

```
修正計画ドキュメントを作成しました。

📄 **ファイル**: `docs/steering/{YYYYMMDD}-fix-{bug-name}/fix-plan.md`

内容を確認してください。修正が必要な場合はお知らせください。
問題なければ「承認」と入力してください。
```

ユーザーが「承認」と回答したら、実装計画に進む。

---

## Phase 3: 実装計画

### Step 10: タスクリストの作成

バグ修正専用テンプレートで `tasklist.md` を作成:
- テンプレート: `.claude/skills/fix-bug/templates/tasklist.md`

### Step 11: 最終確認と実装開始案内

すべてのファイルが揃ったら:

```
ステアリングファイルが完成しました！

📁 **ステアリングディレクトリ**: `docs/steering/{YYYYMMDD}-fix-{bug-name}/`

| ファイル | 内容 |
|----------|------|
| investigation.md | 調査結果（症状、再現手順、原因） |
| fix-plan.md | 修正計画（方針、テスト計画） |
| tasklist.md | タスクリスト |

---

## サマリー

- **バグ名**: {バグ名}
- **影響度**: {Critical/High/Medium/Low}
- **変更ファイル数**: {概算}

### 推奨エージェントフロー
file-finder → impact-analyzer → [修正] → test-runner → code-reviewer

---

```

### Step 12: ブランチ作成とコミット

設計ドキュメントをバージョン管理に登録:

1. フィックスブランチを作成:
   ```bash
   git checkout -b fix/{YYYYMMDD}-{bug-name}
   ```

2. ステアリングディレクトリをコミット:
   ```bash
   git add docs/steering/{YYYYMMDD}-fix-{bug-name}/
   git commit -m "docs: add steering documents for fix-{bug-name}"
   ```

3. 完了メッセージを表示:
   ```
   ✅ 設計フェーズが完了しました！

   📁 **ブランチ**: `fix/{YYYYMMDD}-{bug-name}`
   📄 **コミット済み**: ステアリングドキュメント一式

   修正を開始する場合は `/implement-feature` を実行してください。
   ```

---

## ステータス遷移

| ファイル | 初期値 | 主な遷移 |
|----------|--------|----------|
| progress.md | Phase 1 | Phase 1 → 2（Step 5承認後）→ 3（Step 9承認後）→ 完了（Step 12） |
| investigation.md | 調査中 | → 原因特定済み（Step 7） |
| fix-plan.md | 計画中 | → 確定（Step 9承認後） |
| tasklist.md | 計画中 | → 計画確定（Step 12） |

---

## 注意事項

- ディレクトリは Step 3 で即座に作成し、以降のファイルは随時追加・更新する
- 各ステップでユーザーの回答を待ってから次に進む
- 最小限の修正で問題を解決することを優先する
- 技術的な判断が必要な場合は、CLAUDE.md を参照する
- 対話が中断されても、途中まで入力した内容はファイルに保存されている
- 設計完了後、実装は `/implement-feature` で行う
- 完了後、`mv docs/steering/{dir} docs/steering/archive/` でアーカイブ
