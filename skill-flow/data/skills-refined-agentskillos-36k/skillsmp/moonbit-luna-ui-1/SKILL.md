---
name: moonbit-luna-ui
description: MoonBit + Luna UI (Sol Framework) でのWebアプリ開発。MoonBitコード、Solルーティング、Island Components、Server Actions、D1データベース、Cloudflare Workersデプロイに使用
---

# MoonBit + Luna UI 開発ガイド

MoonBitとLuna UI (Sol Framework) を使用したCloudflare Workers向けWebアプリケーション開発のノウハウ。

## 技術スタック概要

| 技術 | 役割 |
|-----|------|
| MoonBit | メイン言語（WASMターゲット、JSターゲット両対応） |
| Luna UI | UIフレームワーク（Island Architecture） |
| Sol Framework | ルーティング・SSR・Server Actions |
| Cloudflare Workers | ランタイム |
| D1 | SQLiteベースのデータベース |
| Hono | HTTPミドルウェア（認証等） |

## プロジェクト構成

```
project/
├── app/
│   ├── server/
│   │   ├── routes.mbt      # ルーティング・ページ・API定義
│   │   ├── db.mbt          # D1 FFIバインディング
│   │   └── _using.mbt      # 共通インポート
│   ├── client/
│   │   ├── *.mbt           # Island Components
│   │   └── _using.mbt
│   └── __gen__/            # 自動生成（.gitignore推奨）
├── src/
│   └── worker.ts           # Cloudflare Workerエントリーポイント
├── static/
│   └── loader.js           # Luna UIハイドレーションローダー
├── scripts/
│   ├── patch-for-cloudflare.js  # CF Workers用パッチ
│   └── bundle-client.js         # クライアントバンドル
├── moon.mod.json           # MoonBit設定
├── wrangler.json           # Cloudflare設定
└── .sol/                   # Sol生成物（.gitignore推奨）
```

## ビルドプロセス

```bash
# 完全ビルド
pnpm build
# 内部で実行される処理:
# 1. sol generate        - __gen__と.solを生成
# 2. moon build --target js  - MoonBitをJSにコンパイル
# 3. patch-for-cloudflare.js - CF Workers用にパッチ
# 4. bundle-client.js    - Island Componentsをバンドル
```

### wrangler.jsonでの自動ビルド設定

```json
{
  "build": {
    "command": "pnpm build",
    "watch_dir": ["src", "app"]
  }
}
```

## 詳細リファレンス

- ルーティングとページ定義 → [SOL-ROUTING.md](SOL-ROUTING.md)
- Island Components → [ISLAND-COMPONENTS.md](ISLAND-COMPONENTS.md)
- Server Actions → [SERVER-ACTIONS.md](SERVER-ACTIONS.md)
- MoonBit FFIパターン → [MOONBIT-FFI.md](MOONBIT-FFI.md)
- Cloudflare Workersデプロイ → [CLOUDFLARE-DEPLOY.md](CLOUDFLARE-DEPLOY.md)

## クイックリファレンス

### ルート定義（routes.mbt）

```moonbit
pub fn routes() -> Array[@router.SolRoutes] {
  [
    @router.SolRoutes::Page(
      path="/",
      handler=@router.PageHandler(home_page),
      title="Home",
      meta=[], revalidate=None, cache=None,
    ),
    @router.SolRoutes::Post(
      path="/api/posts",
      handler=@router.ApiHandler(api_create_post),
    ),
  ]
}
```

### Island Component（クライアント）

```moonbit
pub fn my_component(props : MyProps) -> DomNode {
  let count = @signal.signal(0)

  div(class="container", [
    button(
      on=events().click(fn(_) { count.set(count.get() + 1) }),
      [text_of(count)]
    )
  ])
}
```

### Server Action

```moonbit
let create_action : @action.ActionHandler = @action.ActionHandler(async fn(ctx) {
  let body = ctx.body
  let data = parse_json(body)
  // 処理...
  @action.ActionResult::ok({ message: "Success" })
})

pub fn action_registry() -> @action.ActionRegistry {
  @action.ActionRegistry::new(allowed_origins=[
    "http://localhost:8787",
    "https://your-app.workers.dev",
  ]).register(
    @action.ActionDef::new("create", create_action)
  )
}
```

### D1 FFI

```moonbit
extern "js" fn db_query(sql : String) -> @core.Promise[@core.Any] =
  #| async (sql) => {
  #|   const db = globalThis.__D1_DB;
  #|   return await db.prepare(sql).all();
  #| }
```

## よくある問題と解決策

### 403エラー（Server Actions）
→ `action_registry()`の`allowed_origins`に本番ドメインを追加

### CSSが適用されない（Island Component）
→ CSSクラス名がroutes.mbtのスタイル定義と一致しているか確認

### ビルド後にモジュールエラー
→ `scripts/patch-for-cloudflare.js`でCF Workers非互換コードをパッチ

### デプロイ時にビルドされない
→ `wrangler.json`に`build.command`を設定
