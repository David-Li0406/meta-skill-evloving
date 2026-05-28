# Skill Creator 例集

## 例1: シンプルなスキルの作成（コマンドリファレンス系）

### 目的
特定のコマンド群のリファレンスを提供するスキルを作成する。

### ステップ1: ディレクトリ作成
```bash
mkdir -p .claude/skills/my-commands
```

### ステップ2: SKILL.md作成
```markdown
---
name: my-commands
description: MyApp用のコマンドリファレンスを提供します。ユーザーがアプリの実行、テスト、デプロイ方法を尋ねた時にアクティベートされます。
---

# MyApp Commands

## 目的
MyAppの各種コマンドのクイックリファレンスを提供します。

## いつアクティベートするか
- ユーザーが「アプリの起動方法」「テスト実行方法」を尋ねた時
- 「コマンド」「実行」「起動」などのキーワードを含む質問時

## クイックリファレンス

### 基本コマンド
```bash
# アプリ起動
npm start

# テスト実行
npm test

# ビルド
npm run build
```

## 詳細リファレンス
[reference.md](reference.md) を参照してください。
```

### ステップ3: reference.md作成（詳細なコマンド一覧）
```markdown
# MyApp Commands リファレンス

## 開発コマンド

### 起動
```bash
npm start
# または
npm run dev
```

### テスト
```bash
# 全テスト
npm test

# 特定ファイル
npm test -- path/to/test.js
```

## デプロイコマンド
...
```

### 結果
- シンプルで明確なコマンドリファレンススキル
- 必要に応じてreference.mdで詳細を提供
- テンプレートやexamplesは不要（コマンドリファレンスのため）

---

## 例2: チェッカー系スキルの作成（コード品質チェック）

### 目的
特定のコーディング規約やパターンに従っているかチェックするスキルを作成する。

### ステップ1: ディレクトリとファイル作成
```bash
mkdir -p .claude/skills/api-design-checker/templates
```

### ステップ2: SKILL.md作成
```markdown
---
name: api-design-checker
description: RESTful API設計のベストプラクティスをチェックします。src/api/ディレクトリ内のファイル作成・修正時にアクティベートされ、エンドポイント命名、HTTPメソッド使用、エラーハンドリングを検証します。
---

# API Design Checker

## 目的
RESTful APIの設計がベストプラクティスに従っているか検証します。

## いつアクティベートするか
- `src/api/` または `src/routes/` ディレクトリ内のファイルを作成・修正する時
- ユーザーが「API」「エンドポイント」「REST」と言った時
- API設計のレビュー時

## クイックチェックリスト

作成前に確認：
- [ ] **リソース名は複数形か** (例: `/users`, `/posts`)
- [ ] **HTTPメソッドが適切か** (GET=取得, POST=作成, PUT/PATCH=更新, DELETE=削除)
- [ ] **ステータスコードが正しいか** (200, 201, 400, 404, 500など)
- [ ] **エラーレスポンスが統一されているか**
- [ ] **認証・認可が実装されているか**
- [ ] **APIバージョニングが考慮されているか**

## ベストプラクティス

### 1. エンドポイント命名

#### ✅ 良い例
```javascript
GET    /api/v1/users          // ユーザー一覧
GET    /api/v1/users/:id      // 特定ユーザー
POST   /api/v1/users          // ユーザー作成
PUT    /api/v1/users/:id      // ユーザー更新
DELETE /api/v1/users/:id      // ユーザー削除
```

#### ❌ 悪い例
```javascript
GET  /api/getUsers            // 動詞を含む
POST /api/user/create         // 単数形 + 動詞
GET  /api/users/delete/:id    // GETで削除
```

### 2. HTTPステータスコード

#### ✅ 良い例
```javascript
// 成功時
res.status(200).json({ data: users });        // GET成功
res.status(201).json({ data: newUser });      // POST成功（作成）
res.status(204).send();                       // DELETE成功（内容なし）

// エラー時
res.status(400).json({ error: "Invalid input" });    // クライアントエラー
res.status(404).json({ error: "User not found" });   // リソースなし
res.status(500).json({ error: "Server error" });     // サーバーエラー
```

#### ❌ 悪い例
```javascript
// すべて200を返す
res.status(200).json({ error: "User not found" });   // エラーなのに200
res.status(200).json({ success: false });            // 失敗なのに200
```

### 3. エラーハンドリング

#### ✅ 良い例
```javascript
app.post('/api/v1/users', async (req, res) => {
  try {
    // バリデーション
    if (!req.body.email) {
      return res.status(400).json({
        error: "Validation failed",
        details: { email: "Email is required" }
      });
    }

    const user = await createUser(req.body);
    res.status(201).json({ data: user });
  } catch (error) {
    console.error(error);
    res.status(500).json({
      error: "Internal server error",
      message: error.message
    });
  }
});
```

#### ❌ 悪い例
```javascript
app.post('/api/v1/users', async (req, res) => {
  // エラーハンドリングなし
  const user = await createUser(req.body);
  res.json(user);
});
```

## テンプレート
`templates/` ディレクトリに以下のテンプレートがあります：
- `crud_endpoint_template.js`: CRUD操作の完全な実装例

## 詳細リファレンス
[reference.md](reference.md) を参照してください。

## 例
[examples.md](examples.md) にさらに多くの例があります。
```

### ステップ3: examples.md作成
```markdown
# API Design Checker 例集

## 例1: ユーザー管理API

### 悪い実装 ❌
```javascript
// ❌ 動詞を含むエンドポイント
app.get('/getUserById/:id', (req, res) => {
  const user = users.find(u => u.id === req.params.id);
  // ❌ 常に200を返す
  res.status(200).json(user || { error: "Not found" });
});

app.post('/createUser', (req, res) => {
  const newUser = { ...req.body, id: Date.now() };
  users.push(newUser);
  // ❌ 201ではなく200
  res.status(200).json(newUser);
});
```

**問題点:**
- エンドポイントに動詞が含まれている
- HTTPステータスコードが不適切
- エラーハンドリングがない
- バリデーションがない

### 良い実装 ✅
```javascript
// ✅ リソースベースのエンドポイント
app.get('/api/v1/users/:id', async (req, res) => {
  try {
    const user = await User.findById(req.params.id);

    if (!user) {
      // ✅ 適切な404
      return res.status(404).json({
        error: "User not found",
        details: { id: req.params.id }
      });
    }

    // ✅ 200で成功
    res.status(200).json({ data: user });
  } catch (error) {
    console.error(error);
    // ✅ 500でサーバーエラー
    res.status(500).json({
      error: "Internal server error"
    });
  }
});

app.post('/api/v1/users', async (req, res) => {
  try {
    // ✅ バリデーション
    const errors = validateUser(req.body);
    if (errors.length > 0) {
      return res.status(400).json({
        error: "Validation failed",
        details: errors
      });
    }

    const newUser = await User.create(req.body);
    // ✅ 201で作成成功
    res.status(201).json({ data: newUser });
  } catch (error) {
    console.error(error);
    res.status(500).json({
      error: "Internal server error"
    });
  }
});
```

**改善点:**
- RESTfulなエンドポイント設計
- 適切なHTTPステータスコード
- 包括的なエラーハンドリング
- バリデーションの実装
```

### ステップ4: templates/crud_endpoint_template.js作成
```javascript
/**
 * {Resource} CRUD API Endpoints
 *
 * このテンプレートを使用して、RESTful APIエンドポイントを作成します。
 * {Resource}を実際のリソース名（User, Post など）に置き換えてください。
 */

const express = require('express');
const router = express.Router();

// GET /api/v1/{resources} - 一覧取得
router.get('/', async (req, res) => {
  try {
    const items = await {Resource}.findAll();
    res.status(200).json({ data: items });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Internal server error" });
  }
});

// GET /api/v1/{resources}/:id - 個別取得
router.get('/:id', async (req, res) => {
  try {
    const item = await {Resource}.findById(req.params.id);

    if (!item) {
      return res.status(404).json({
        error: "{Resource} not found",
        details: { id: req.params.id }
      });
    }

    res.status(200).json({ data: item });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Internal server error" });
  }
});

// POST /api/v1/{resources} - 作成
router.post('/', async (req, res) => {
  try {
    // バリデーション
    const errors = validate{Resource}(req.body);
    if (errors.length > 0) {
      return res.status(400).json({
        error: "Validation failed",
        details: errors
      });
    }

    const newItem = await {Resource}.create(req.body);
    res.status(201).json({ data: newItem });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Internal server error" });
  }
});

// PUT /api/v1/{resources}/:id - 更新
router.put('/:id', async (req, res) => {
  try {
    const errors = validate{Resource}(req.body);
    if (errors.length > 0) {
      return res.status(400).json({
        error: "Validation failed",
        details: errors
      });
    }

    const updatedItem = await {Resource}.update(req.params.id, req.body);

    if (!updatedItem) {
      return res.status(404).json({
        error: "{Resource} not found",
        details: { id: req.params.id }
      });
    }

    res.status(200).json({ data: updatedItem });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Internal server error" });
  }
});

// DELETE /api/v1/{resources}/:id - 削除
router.delete('/:id', async (req, res) => {
  try {
    const deleted = await {Resource}.delete(req.params.id);

    if (!deleted) {
      return res.status(404).json({
        error: "{Resource} not found",
        details: { id: req.params.id }
      });
    }

    res.status(204).send();
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Internal server error" });
  }
});

module.exports = router;
```

### 結果
- 包括的なAPI設計チェックスキル
- 良い例・悪い例の対比
- 実用的なテンプレート
- 明確なチェックリスト

---

## 例3: ヘルパー系スキルの作成（開発補助）

### 目的
特定の作業（例: データベース移行）を支援するスキルを作成する。

### SKILL.md（migration-helperの例）
```markdown
---
name: migration-helper
description: データベース移行ファイルの作成を支援します。database/migrations/ディレクトリでファイル作成時にアクティベートされ、連番管理、命名規則、02_run_migrations.sqlへの登録を確認します。
---

# Migration Helper

## 目的
データベーススキーマ変更の際の移行ファイル作成を支援します。

## いつアクティベートするか
- `database/migrations/` ディレクトリ内でファイルを作成する時
- ユーザーが「マイグレーション」「スキーマ変更」と言った時
- データベーステーブルやカラムの追加・変更時

## クイックチェックリスト

移行ファイル作成前に：
- [ ] **連番が正しいか** (最新の番号 + 1)
- [ ] **命名規則に従っているか** (`XXX_descriptive_name.sql`)
- [ ] **ファイルが `database/migrations/` にあるか**
- [ ] **`02_run_migrations.sql` に追加されているか**

## 手順

### ステップ1: 最新の移行番号を確認
```bash
ls database/migrations/ | sort -n | tail -1
# 例: 015_add_column_to_users.sql
# → 次は 016
```

### ステップ2: 移行ファイル作成
```sql
-- 016_add_email_to_politicians.sql
ALTER TABLE politicians ADD COLUMN email VARCHAR(255);
```

### ステップ3: 02_run_migrations.sqlに追加
```sql
-- database/02_run_migrations.sql に追加
\i database/migrations/016_add_email_to_politicians.sql
```

## テンプレート
[templates/migration_template.sql](templates/migration_template.sql) を参照してください。
```

### templates/migration_template.sql
```sql
-- {番号}_{ descriptive_name}.sql
--
-- 目的: {この移行で何を行うか簡潔に説明}
-- 作成日: {YYYY-MM-DD}

-- テーブル作成の例
CREATE TABLE IF NOT EXISTS {table_name} (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- カラム追加の例
-- ALTER TABLE {existing_table} ADD COLUMN {column_name} {data_type};

-- インデックス作成の例
-- CREATE INDEX IF NOT EXISTS idx_{table}_{column} ON {table}({column});

-- ⚠️ この移行ファイルを作成したら、必ず以下を実行：
-- 1. database/02_run_migrations.sql に \i database/migrations/{番号}_{descriptive_name}.sql を追加
-- 2. ./reset-database.sh を実行して動作確認
```

### 結果
- 明確な手順が示されたヘルパースキル
- チェックリストで必須事項を確認
- テンプレートで作業を効率化

---

## まとめ

### スキルタイプ別の構成

| スキルタイプ | SKILL.md | reference.md | examples.md | templates/ |
|--------------|----------|--------------|-------------|------------|
| コマンドリファレンス | 必須 | 任意（詳細） | 不要 | 不要 |
| コードチェッカー | 必須 | 任意（詳細パターン） | 推奨（良い例・悪い例） | 任意 |
| ヘルパー/ガイド | 必須 | 任意（トラブルシューティング） | 推奨（ステップバイステップ） | 推奨 |

### すべてのスキルに共通
- SKILL.mdは必須
- フロントマター（name, description）は必須
- 目的とアクティベーション条件は必須
- クイックチェックリストを含める
- 日本語で記述する
