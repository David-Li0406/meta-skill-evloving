# MoonBit FFI パターン集

MoonBitからJavaScriptを呼び出すFFI（Foreign Function Interface）のパターン。

---

## FFI削減ガイド（推奨）

**原則**: MoonBitで実装できるものはMoonBitで書く。FFIは最小限に。

### 削減実績

| カテゴリ | 削減前 | 削減後 | 削減率 |
|---------|--------|--------|--------|
| データアクセス | 5 FFI | 0 FFI | 100% |
| 文字列操作 | 2 FFI | 0 FFI | 100% |
| JSON処理 | 2 FFI | 0 FFI | 100% |
| フォーム処理 | 2 FFI | 0 FFI | 100% |
| フレームワーク連携 | 2 FFI | 0 FFI | 100% |
| クライアントヘルパー | 3 FFI | 0 FFI | 100% |
| **合計** | **26 FFI** | **10 FFI** | **62%** |

### 削減パターン

#### 1. データアクセスヘルパー → `@core.Any` API

```moonbit
// ❌ Before: FFI
extern "js" fn get_str(obj, field) -> String = #| (obj, field) => obj?.[field] ?? ""

// ✅ After: MoonBit native
pub fn get_str(obj : @core.Any, field : String) -> String {
  if @core.is_nullish(obj) { return "" }
  let val = obj._get(field)
  if @core.is_nullish(val) { "" } else { val.to_string() }
}

// ❌ Before: FFI
extern "js" fn get_int(obj, field) -> Int = #| (obj, field) => Number(obj?.[field]) || 0

// ✅ After: MoonBit native
pub fn get_int(obj : @core.Any, field : String) -> Int {
  if @core.is_nullish(obj) { return 0 }
  let val = obj._get(field)
  if @core.is_nullish(val) { 0 } else { val.cast() }
}

// ❌ Before: FFI
extern "js" fn is_null(obj) -> Bool = #| (obj) => obj == null

// ✅ After: MoonBit native
pub fn is_null(obj : @core.Any) -> Bool {
  @core.is_nullish(obj)
}

// ❌ Before: FFI
extern "js" fn array_len(arr) -> Int = #| (arr) => arr?.length || 0

// ✅ After: MoonBit native
pub fn array_len(arr : @core.Any) -> Int {
  if @core.is_nullish(arr) { 0 }
  else { arr._get("length").cast() }
}

// ❌ Before: FFI
extern "js" fn array_get(arr, idx) -> @core.Any = #| (arr, idx) => arr[idx]

// ✅ After: MoonBit native
pub fn array_get(arr : @core.Any, idx : Int) -> @core.Any {
  arr._get_by_index(idx)
}
```

#### 2. 文字列操作 → MoonBit String API

```moonbit
// ❌ Before: FFI
extern "js" fn normalize_newlines(s) -> String = #| (s) => s.replace(/\\n/g, '\n')

// ✅ After: MoonBit native
fn normalize_newlines(s : String) -> String {
  let result = StringBuilder::new()
  let chars = s.to_array()
  let len = chars.length()
  let mut i = 0
  while i < len {
    if i + 1 < len && chars[i] == '\\' && chars[i + 1] == 'n' {
      result.write_char('\n')
      i = i + 2
    } else {
      result.write_char(chars[i])
      i = i + 1
    }
  }
  result.to_string()
}

// ❌ Before: FFI
extern "js" fn safe_excerpt(content, maxLen) -> String = #| ...

// ✅ After: MoonBit native
fn safe_excerpt(content : String, max_len : Int) -> String {
  let chars = content.to_array()
  if chars.length() <= max_len { content }
  else {
    let result = StringBuilder::new()
    for i = 0; i < max_len; i = i + 1 { result.write_char(chars[i]) }
    result.write_string("...")
    result.to_string()
  }
}

// ❌ Before: FFI (slug生成)
extern "js" fn generate_slug(title) -> String = #| (title) => title.toLowerCase()...

// ✅ After: MoonBit native
fn generate_slug(title : String) -> String {
  let result = StringBuilder::new()
  let mut prev_hyphen = true
  for c in title {
    let lower = if c >= 'A' && c <= 'Z' {
      (c.to_int() + 32).unsafe_to_char()
    } else { c }
    let is_alnum = (lower >= 'a' && lower <= 'z') || (lower >= '0' && lower <= '9')
    if is_alnum {
      result.write_char(lower)
      prev_hyphen = false
    } else if not(prev_hyphen) {
      result.write_char('-')
      prev_hyphen = true
    }
  }
  // Trim trailing hyphen...
  result.to_string()
}
```

#### 3. JSON処理 → `@core` API

```moonbit
// ❌ Before: FFI
extern "js" fn api_json_success(msg, slug) -> @core.Any = #| (msg, slug) => ({ success: true, message: msg, slug })

// ✅ After: MoonBit native
fn action_json_response(success : Bool, message : String, slug : String) -> @core.Any {
  @core.from_entries([
    ("success", @core.any(success)),
    ("message", @core.any(message)),
    ("slug", @core.any(slug)),
  ])
}

// ❌ Before: FFI
extern "js" fn parse_json(s) -> @core.Any = #| (s) => JSON.parse(s)

// ✅ After: MoonBit native with error handling
fn parse_json(s : String) -> @core.Any {
  try { @core.try_sync(fn() { @core.json_parse(s) }) }
  catch { @core.JsError(_) => @core.new_object() }
}
```

#### 4. フォーム処理 → Pure MoonBit

```moonbit
// ❌ Before: FFI
extern "js" fn parse_form_urlencoded(s) -> @core.Any = #| (s) => ...

// ✅ After: MoonBit native (ヘルパー関数と組み合わせ)
fn parse_form_urlencoded(s : String) -> @core.Any {
  let result = @core.new_object()
  if s == "" { return result }
  let pairs = split_by_char(s, '&')
  for pair in pairs {
    if pair == "" { continue }
    // key=value を分解
    let chars = pair.to_array()
    let mut eq_idx = -1
    for i, c in chars {
      if c == '=' { eq_idx = i; break }
    }
    if eq_idx >= 0 {
      let key = safe_decode_uri(extract_substring(chars, 0, eq_idx))
      let value = safe_decode_uri(extract_substring(chars, eq_idx + 1, chars.length()))
      result._set(key, @core.any(value))
    }
  }
  result
}

// ヘルパー: 文字で分割
fn split_by_char(s : String, sep : Char) -> Array[String] { ... }

// ヘルパー: 部分文字列抽出
fn extract_substring(chars : Array[Char], start : Int, end : Int) -> String { ... }
```

#### 5. フレームワーク連携 → Sol Framework API

```moonbit
// ❌ Before: FFI
extern "js" fn get_form_body_promise(props) -> @core.Promise[@core.Any] = #| async (props) => await props.ctx.req.parseBody()

// ✅ After: Sol Framework native API
async fn api_handler(props : @router.PageProps) -> @core.Any {
  let body = props.ctx.req.parseBody()  // 直接呼び出し可能
  // ...
}

// ❌ Before: FFI
extern "js" fn hono_redirect(props, url) -> @core.Any = #| (props, url) => new Response(null, { status: 302, headers: { Location: url } })

// ✅ After: Sol Framework native API
async fn api_delete(props : @router.PageProps) -> @core.Any {
  @core.any(props.ctx.redirect("/admin"))  // 直接呼び出し可能
}
```

#### 6. クライアントヘルパー → `@js.Any` API

```moonbit
// ❌ Before: FFI
extern "js" fn get_message(data) -> String = #| (data) => data?.message || "成功"

// ✅ After: MoonBit native (クライアント側は @js を使用)
fn get_message(data : @js.Any) -> String {
  let val = data._get("message")
  if @js.is_nullish(val) { "成功" } else { val.to_string() }
}

// ❌ Before: FFI
extern "js" fn get_slug(data) -> String = #| (data) => data?.slug || ""

// ✅ After: MoonBit native
fn get_slug(data : @js.Any) -> String {
  let val = data._get("slug")
  if @js.is_nullish(val) { "" } else { val.to_string() }
}
```

### 削減不可能なFFI（必須）

以下はブラウザ/ランタイムAPIの制約により残す必要がある：

| FFI | 理由 |
|-----|------|
| `get_global_db()` | D1バインディング取得 - 1 FFIのみ |
| `get_timestamp()` | Date API - JSのみ |
| `redirect_to(url)` | `window.location.href` - DOM API |
| `get_form_data_from_form()` | FormData API - DOM API |
| `safe_decode_uri()` | `decodeURIComponent()` - 例外処理含むためFFI推奨 |

---

## mizchi/cloudflare パッケージ（推奨）

**`mizchi/cloudflare` パッケージを使用することで、D1/KV/R2/Durable Objectsへのアクセスを型安全に行える。**

### インストール

```bash
moon add mizchi/cloudflare
```

### moon.pkg.json への追加

```json
{
  "import": [
    { "path": "mizchi/cloudflare", "alias": "cloudflare" }
  ]
}
```

### D1データベースアクセス

```moonbit
///| D1データベース取得（最小FFI - バインディング取得のみ）
fn get_db() -> @cloudflare.D1Database {
  let db_js : @core.Any = get_global_db()
  @core.identity(db_js)
}

extern "js" fn get_global_db() -> @core.Any =
  #| () => {
  #|   const db = globalThis.__D1_DB;
  #|   if (!db) throw new Error('D1 database not initialized');
  #|   return db;
  #| }

///| 全記事取得 - 本家パッケージのAPIを使用
pub async fn db_get_all_posts() -> @core.Any {
  let db = get_db()
  let result = db
    .prepare("SELECT * FROM posts ORDER BY updated_at DESC")
    .all()
  result.results_raw()
}

///| 条件付き取得 - bind()でパラメータバインド
pub async fn db_get_post_by_slug(slug : String) -> @core.Any {
  let db = get_db()
  let row = db
    .prepare("SELECT * FROM posts WHERE slug = ?")
    .bind1(@core.any(slug))
    .first()
  match row {
    Some(r) => r
    None => @core.null()
  }
}

///| INSERT/UPDATE/DELETE - run()を使用
pub async fn db_delete_post(id : String) -> @cloudflare.D1Result {
  let db = get_db()
  db.prepare("DELETE FROM posts WHERE id = ?")
    .bind1(@core.any(id))
    .run()
}

///| 複数パラメータのバインド - bind()で配列を渡す
pub async fn db_create_post(
  title : String,
  slug : String,
  content : String
) -> @core.Any {
  let db = get_db()
  let row = db
    .prepare("INSERT INTO posts (title, slug, content) VALUES (?, ?, ?) RETURNING *")
    .bind([
      @core.any(title),
      @core.any(slug),
      @core.any(content),
    ])
    .first()
  match row {
    Some(r) => r
    None => @core.null()
  }
}
```

### @cloudflare.D1Database API

| メソッド | 説明 |
|---------|------|
| `prepare(query: String)` | D1PreparedStatementを作成 |

### @cloudflare.D1PreparedStatement API

| メソッド | 説明 |
|---------|------|
| `bind(params: Array[@core.Any])` | 複数パラメータをバインド |
| `bind1(param: @core.Any)` | 1パラメータをバインド |
| `bind2(p1, p2)` | 2パラメータをバインド |
| `first()` | 1行取得 (Option[@core.Any]) |
| `all()` | 全行取得 (D1Result) |
| `run()` | INSERT/UPDATE/DELETE実行 (D1Result) |

### @cloudflare.D1Result API

| メソッド | 説明 |
|---------|------|
| `results_raw()` | 結果配列を取得 |
| `success()` | 成功チェック |
| `meta()` | メタ情報取得 |

### FFI削減効果

```
Before (独自FFI):  7 FFI (db_get_*, db_create_*, db_update_*, db_delete_*)
After (本家使用):  1 FFI (get_global_db のみ)
削減率: 86%
```

### なぜ1つのFFIが必要か？

Cloudflare Workers の D1 バインディングは `env.DB` から取得する必要がある。
Sol Framework の PageProps からは直接 env にアクセスできないため、
worker.ts で `globalThis.__D1_DB = env.DB` を設定し、MoonBit側で取得する。

```typescript
// src/worker.ts
export default {
  fetch: async (request: Request, env: Env, ctx: ExecutionContext) => {
    (globalThis as any).__D1_DB = env.DB;
    // ...
  }
}
```

---

## 基本構文

```moonbit
extern "js" fn function_name(arg1 : Type1, arg2 : Type2) -> ReturnType =
  #| (arg1, arg2) => {
  #|   // JavaScript code
  #|   return result;
  #| }
```

## 型マッピング

| MoonBit型 | JavaScript型 |
|----------|-------------|
| `String` | `string` |
| `Int` | `number` |
| `Bool` | `boolean` |
| `@core.Any` | `any` |
| `@core.Promise[T]` | `Promise<T>` |
| `@js.Any` | `any` (client) |
| `Unit` | `undefined` |

## 同期関数

### 文字列操作

```moonbit
extern "js" fn generate_slug(title : String) -> String =
  #| (title) => title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')

extern "js" fn safe_excerpt(content : String, max_len : Int) -> String =
  #| (content, maxLen) => {
  #|   if (content.length <= maxLen) return content;
  #|   return content.slice(0, maxLen) + "...";
  #| }

extern "js" fn normalize_newlines(s : String) -> String =
  #| (s) => s.replace(/\\n/g, '\n')
```

### オブジェクト操作

```moonbit
///| 文字列フィールド取得
extern "js" fn get_str(obj : @core.Any, field : String) -> String =
  #| (obj, field) => obj && obj[field] != null ? String(obj[field]) : ""

///| 数値フィールド取得
extern "js" fn get_int(obj : @core.Any, field : String) -> Int =
  #| (obj, field) => obj && obj[field] != null ? Number(obj[field]) : 0

///| null/undefinedチェック
extern "js" fn is_null(obj : @core.Any) -> Bool =
  #| (obj) => obj == null
```

### 配列操作

```moonbit
extern "js" fn array_len(arr : @core.Any) -> Int =
  #| (arr) => Array.isArray(arr) ? arr.length : 0

extern "js" fn array_get(arr : @core.Any, idx : Int) -> @core.Any =
  #| (arr, idx) => arr[idx]
```

### タイムスタンプ

```moonbit
extern "js" fn get_timestamp() -> String =
  #| () => new Date().toISOString()
```

## 非同期関数（Promise）

### D1データベース

```moonbit
extern "js" fn db_get_all_posts() -> @core.Promise[@core.Any] =
  #| async () => {
  #|   const db = globalThis.__D1_DB;
  #|   if (!db) throw new Error('D1 database not initialized');
  #|   const r = await db.prepare("SELECT * FROM posts ORDER BY updated_at DESC").all();
  #|   return r.results;
  #| }

extern "js" fn db_get_post_by_slug(slug : String) -> @core.Promise[@core.Any] =
  #| async (slug) => {
  #|   const db = globalThis.__D1_DB;
  #|   if (!db) throw new Error('D1 database not initialized');
  #|   return await db.prepare("SELECT * FROM posts WHERE slug = ?").bind(slug).first();
  #| }

extern "js" fn db_create_post(
  title : String,
  slug : String,
  content : String,
  content_html : String,
  excerpt : String,
  status : String
) -> @core.Promise[@core.Any] =
  #| async (title, slug, content, content_html, excerpt, status) => {
  #|   const db = globalThis.__D1_DB;
  #|   const published_at = status === 'published' ? new Date().toISOString() : null;
  #|   return await db.prepare(
  #|     "INSERT INTO posts (title, slug, content, content_html, excerpt, status, published_at) VALUES (?, ?, ?, ?, ?, ?, ?) RETURNING *"
  #|   ).bind(title, slug, content, content_html, excerpt, status, published_at).first();
  #| }
```

### Promiseの使用

```moonbit
async fn my_handler(props : @router.PageProps) -> @server_dom.ServerNode {
  @server_dom.ServerNode::async_(async fn() {
    // .wait()でPromiseを待機
    let posts = db_get_all_posts().wait()
    let len = array_len(posts)

    // 結果を使用
    @luna.fragment([...])
  })
}
```

## Hono連携

### フォームボディ取得

```moonbit
extern "js" fn get_form_body_promise(props : @router.PageProps) -> @core.Promise[@core.Any] =
  #| async (props) => {
  #|   const ctx = props.ctx;
  #|   if (!ctx?.req) return {};
  #|   try {
  #|     return await ctx.req.parseBody();
  #|   } catch (e) {
  #|     console.error('Error parsing form:', e);
  #|     return {};
  #|   }
  #| }
```

### リダイレクト

```moonbit
extern "js" fn hono_redirect(_props : @router.PageProps, url : String) -> @core.Any =
  #| (props, url) => new Response(null, {
  #|   status: 302,
  #|   headers: { 'Location': url }
  #| })
```

### JSONレスポンス

```moonbit
extern "js" fn api_json_success(message : String, slug : String) -> @core.Any =
  #| (message, slug) => ({ success: true, message, slug })
```

## クライアント側FFI（Island Component用）

### DOM操作

```moonbit
extern "js" fn redirect_to(url : String) -> Unit =
  #| (url) => { window.location.href = url; }
```

### フォームデータ取得

```moonbit
extern "js" fn get_form_data_from_form(e : @js_dom.FormEvent, post_id : String) -> @js.Any =
  #| (e, postId) => {
  #|   const form = e.target;
  #|   const formData = new FormData(form);
  #|   const data = {};
  #|   formData.forEach((value, key) => { data[key] = value; });
  #|   if (postId) { data.id = postId; }
  #|   return data;
  #| }
```

### レスポンスデータ取得

```moonbit
extern "js" fn get_message(data : @js.Any) -> String =
  #| (data) => data?.message || "成功"

extern "js" fn get_slug(data : @js.Any) -> String =
  #| (data) => data?.slug || ""
```

## globalThis経由のデータ共有

Cloudflare Workers環境でD1データベースをMoonBitコードから使用する場合、
`worker.ts` で `globalThis` に設定。

```typescript
// src/worker.ts
export default {
  fetch: async (request: Request, env: Env, ctx: ExecutionContext) => {
    (globalThis as any).__D1_DB = env.DB;
    // ...
  }
}
```

MoonBitからアクセス：
```moonbit
extern "js" fn db_query() -> @core.Promise[@core.Any] =
  #| async () => {
  #|   const db = globalThis.__D1_DB;
  #|   // ...
  #| }
```

## サーバー vs クライアント

| 場所 | 戻り値型 | 用途 |
|-----|---------|------|
| `app/server/*.mbt` | `@core.Any`, `@core.Promise[T]` | D1, Hono連携 |
| `app/client/*.mbt` | `@js.Any`, `Unit` | DOM操作, イベント |

## よくある問題

### undefined関数エラー

FFI関数はビルド時にJSに変換される。
定義場所（server/client）を確認。

### Promiseが解決されない

`async fn` 内で `.wait()` を忘れずに。

```moonbit
// ❌ NG
let posts = db_get_all_posts()  // Promise未解決

// ✅ OK
let posts = db_get_all_posts().wait()
```

### 型不一致

`@core.Any` と `@js.Any` は異なる型。
サーバーでは `@core`、クライアントでは `@js` を使用。
