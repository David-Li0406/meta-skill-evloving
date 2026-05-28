# cga-review 詳細ガイド

サブエージェントを使って並列でコードレビューを実施。人間がマージ判断。

## 基本ルール

- **読み取り専用**: コードの変更は行わない
- **4並列構成**: 自動チェックとLLMレビュー3観点を同時実行
- **人間が判断**: マージ可否は人間が決定

## 実行フロー

```
/cga-review <target>
    │
    ▼ 4タスク並列実行
    │
    ├─ Task(自動チェック: npm run review:json) ──┐
    ├─ Task(観点1: ビジネスロジック)           ──┤
    ├─ Task(観点2: 設計・命名)                 ──┼─→ 結果マージ
    └─ Task(観点3: セキュリティ)               ──┘
```

**重要**: 4タスクを同時に並列起動し、全完了後に結果をマージする。

## タスク1: 自動チェック（Task: Bash）

Taskツール（subagent_type="Bash"）で以下のコマンドを実行し、結果を返す:

```bash
npm run review:json ${TARGET}
```

### チェック項目

| チェック | ツール | 判定基準 |
|----------|--------|----------|
| 依存関係ルール | dependency-cruiser | .dependency-cruiser.cjs のルール違反 |
| 循環依存 | madge | 循環パスの存在 |
| 循環複雑度 | ESLint | complexity > 15 でエラー |
| 関数行数 | ESLint | max-lines-per-function > 50 で警告 |
| ファイル行数 | ESLint | max-lines > 400 で警告 |
| ネスト深度 | ESLint | max-depth > 4 で警告 |
| 型エラー | tsc | コンパイルエラー |
| カバレッジ | vitest | 80% 未満で警告 |
| Branded Type | tsc | テストでの生文字列代入エラー |
| Repository Mock | tsc | インターフェースのメソッド不足エラー |

## タスク2〜4: LLMレビュー（Task: Explore）

自動チェックとは独立に、3つの観点でTaskツールを使い並列レビュー:

### 並列起動

4つのTaskを単一メッセージ内で同時に起動する:

```
Task(subagent_type="Bash", prompt="npm run review:json ${TARGET} を実行し、結果を返して")
Task(subagent_type="Explore", prompt="観点1: ビジネスロジックの正しさをレビュー。対象: ${TARGET}")
Task(subagent_type="Explore", prompt="観点2: 設計・命名をレビュー。対象: ${TARGET}")
Task(subagent_type="Explore", prompt="観点3: セキュリティをレビュー。対象: ${TARGET}")
```

LLMレビューは自動チェック結果を待たず、コードを直接読んでレビューする。

### 観点1: ビジネスロジックの正しさ

**レビュー内容:**
- ドメインルール（glossary.md）への準拠
- 状態遷移の妥当性
- エッジケースの考慮
- Result型のエラーハンドリング漏れ

**チェックリスト:**
- [ ] doc/decisions/DDR-*.md の意思決定と一貫性が保たれているか
- [ ] ドメイン用語が正しく使われているか
- [ ] 状態遷移が glossary.md のルールに従っているか
- [ ] 全ての分岐パスが正しく処理されているか
- [ ] エラーケースが適切にResult型で返されているか
- [ ] **集約の状態遷移・状態変更が集約ルートを経由しているか**
- [ ] **配送状態チェックで全ステータス（SHIPPED, IN_TRANSIT, DELIVERED, FAILED）を考慮しているか**

### 観点2: 設計・命名

**レビュー内容:**
- レイヤー構造の適切さ
- 責務の分離
- 命名の適切さ（CLAUDE.md の命名規約）
- インターフェースの設計

**チェックリスト:**
- [ ] doc/decisions/ADR-*.md の意思決定と一貫性が保たれているか
- [ ] 1つの関数/クラスが1つの責務を持っているか
- [ ] 命名が意図を明確に表現しているか
- [ ] publicメソッドにJSDocがあるか
- [ ] **Command型の定義が`type`と`interface`で統一されているか**
- [ ] **インライン定義されたサービス（ProductService等）が別ファイルに分離されているか**

### 観点3: セキュリティ

**レビュー内容:**
- 認証・認可チェックの漏れ
- 機密情報の取り扱い
- 入力検証の十分性

**チェックリスト:**
- [ ] エンドポイントで認証が必要か確認
- [ ] リソースアクセス時に所有者チェックがあるか
- [ ] Zodスキーマで入力検証されているか
- [ ] 機密情報がログに出力されていないか

## 結果マージ

4タスクの結果を統合してレポートを作成:

```
1. 全4タスクの完了を待機
2. 自動チェック結果とLLMレビュー結果を統合
3. 自動チェックとLLMで重複する指摘は自動チェック側を優先し、LLM側を除去する
4. 重要度順にソート（Critical → Warning → Info）
5. レポート形式で出力
```

### レポート形式

```markdown
## コードレビュー結果

### 自動チェック結果

| チェック | 結果 | Issue数 |
|----------|------|---------|
| 依存関係 | ✅ | 0 |
| 循環依存 | ✅ | 0 |
| 複雑度 | ❌ | 2 |
| 型チェック | ✅ | 0 |
| カバレッジ | ⚠️ | 1 |

### 詳細Issue（自動検出）

#### 🔴 Critical

##### [src/ordering/usecases/create-order.ts:45](src/ordering/usecases/create-order.ts#L45)
**ルール:** complexity
**問題:** 循環複雑度が16（上限15）

### LLMレビュー

#### ビジネスロジック
- 🟠 `createOrder` で在庫チェックが不足
- 🟡 状態遷移のコメントがあると理解しやすい

#### 設計・命名
- 🟡 `handleOrder` より `processOrderCreation` の方が意図が明確

#### セキュリティ
- 問題なし

---

## 総合評価

- **自動チェック:** 4/5 パス
- **重大Issue:** 1件（複雑度超過）
- **要対応:** 複雑度の高い関数を分割
```

## 使用例

```bash
# 特定ディレクトリをレビュー
/cga-review src/ordering/usecases/

# 特定ファイルをレビュー
/cga-review src/ordering/usecases/create-order.ts
```
