# Semantic Commit - 実装リファレンス

分割ロジックの詳細と判断基準を記載しています。

---

## 変更分析で使用する Git コマンド

| 目的 | コマンド |
|------|---------|
| 変更ファイル一覧 | `git diff HEAD --name-only` |
| 変更種別付き一覧 | `git diff HEAD --name-status` |
| 変更統計 | `git diff HEAD --stat` |
| 特定ファイルの差分 | `git diff HEAD -- <file>` |
| 最近のコミット履歴 | `git log --oneline -20` |

---

## 行単位（hunk単位）分割の実装

### パッチファイルの構造

```diff
diff --git a/src/example.ts b/src/example.ts
--- a/src/example.ts
+++ b/src/example.ts
@@ -10,6 +10,8 @@ function existingFunction() {
   // 既存コード
+  // 追加行1 (fix用)
+  // 追加行2 (fix用)
 }
@@ -25,4 +27,10 @@ function anotherFunction() {
   // 既存コード
+// 新しい関数 (feat用)
+function newFeature() {
+  return true;
+}
```

### パッチ分割の手順

1. **一時ディレクトリを作成**
   ```
   TMPDIR=$(mktemp -d)
   ```

2. **全体の差分を取得**
   ```
   git diff HEAD -- <file> > "$TMPDIR/full.patch"
   ```

3. **hunk を論理単位に分割**
   - 各 `@@` で始まるブロックが1つの hunk
   - 関連する hunk をグループ化して別ファイルに保存
   - ヘッダー部分 (`diff --git`, `---`, `+++`) は各パッチに必要

4. **パッチを適用してステージング**
   ```
   git apply --cached "$TMPDIR/fix.patch"
   git commit -m "fix: ..."

   git apply --cached "$TMPDIR/feat.patch"
   git commit -m "feat: ..."
   ```

5. **一時ディレクトリを削除**
   ```
   rm -rf "$TMPDIR"
   ```

### パッチファイルの最小構成

```diff
diff --git a/path/to/file b/path/to/file
--- a/path/to/file
+++ b/path/to/file
@@ -開始行,行数 +開始行,行数 @@ コンテキスト
 コンテキスト行（変更なし）
-削除行
+追加行
 コンテキスト行（変更なし）
```

### 行単位分割の判断基準

| 状況 | 分割方法 |
|------|---------|
| 同一ファイルに fix + feat | hunk 単位で分割 |
| import 追加 + 本体変更 | 通常は同一コミット（依存関係） |
| 複数関数の独立した変更 | 関数単位で hunk を分割 |
| コメント追加 + ロジック変更 | 目的が異なれば分割検討 |

### 注意点

- パッチのコンテキスト行（変更なし行）が一致しないと適用失敗
- 行番号は元ファイルの状態と一致している必要がある
- 複雑な分割は `git stash` でバックアップ後に実施

---

## 分割判断のロジック

### 1. 変更規模の判定

| 条件 | 閾値 | アクション |
|------|------|-----------|
| 変更ファイル数 | ≥ 5 | 分割を推奨 |
| 変更行数 | ≥ 100 | 分割を推奨 |
| 機能領域 | ≥ 2 | 機能単位で分割 |
| 混在タイプ | feat + fix + docs | タイプ別に分割 |

### 2. グループ化の優先順位

1. **機能単位** (最優先)
   - 同一ディレクトリ配下のファイル
   - 例: `src/auth/*` → 認証機能として1グループ

2. **変更種別**
   - A (追加) / M (修正) / D (削除) で分類
   - テストファイル (`*test*`, `*spec*`) は別グループ

3. **依存関係**
   - import/export の関係があるファイルは同一グループ
   - 型定義と実装は同一グループ

4. **コミットタイプ**
   - feat / fix / docs / test / refactor / chore

### 3. コミットサイズの最適化

- **推奨**: 1コミットあたり 3〜8 ファイル
- **上限**: 10 ファイル (超える場合はさらに分割)
- **下限**: 意味のある単位であれば1ファイルでも可

---

## 変更種別の判定基準

| パターン | タイプ | 判定根拠 |
|---------|--------|---------|
| 新規ファイル + 新規関数/クラス | `feat` | 機能追加 |
| 既存ファイルの条件分岐修正 | `fix` | バグ修正 |
| ファイル移動・リネームのみ | `refactor` | 構造変更 |
| `*test*`, `*spec*` ファイル | `test` | テスト |
| `*.md`, `docs/*` | `docs` | ドキュメント |
| `package.json`, 設定ファイル | `chore` | メンテナンス |

---

## CommitLint 設定の検出

### 検索対象ファイル (優先順)

1. `commitlint.config.mjs`
2. `commitlint.config.js`
3. `commitlint.config.cjs`
4. `commitlint.config.ts`
5. `.commitlintrc.json`
6. `.commitlintrc.yml`
7. `package.json` の `commitlint` セクション

### 抽出する設定項目

| 項目 | 用途 |
|------|------|
| `type-enum` | 使用可能なコミットタイプ |
| `scope-enum` | 使用可能なスコープ |
| `subject-max-length` | メッセージ長制限 |

---

## 順次コミットの実行フロー

```
1. git reset HEAD (ステージングをクリア)
     ↓
2. グループ1のファイルを git add
     ↓
3. コミットメッセージを生成・提案
     ↓
4. ユーザー確認 → git commit
     ↓
5. 次のグループへ (2に戻る)
     ↓
6. 完了確認 (残りの変更がないか確認)
```

### エラー時の対応

| エラー | 対応 |
|--------|------|
| pre-commit hook 失敗 | 自動修正を取り込み再コミット (最大2回) |
| ファイルが存在しない | スキップして警告表示 |
| 空のステージング | そのグループをスキップ |

---

## スコープ推測のヒント

| プロジェクト構造 | スコープ候補 |
|-----------------|-------------|
| `packages/*` | 各パッケージ名 |
| `src/components/*` | `ui`, `components` |
| `src/api/*` | `api` |
| `src/utils/*` | `utils`, `core` |
| `tests/*` | 不要 (type が `test` で十分) |
