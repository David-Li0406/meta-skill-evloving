---
name: build-tanstack-app
description: Build and enhance React applications using the TanStack ecosystem. Use this skill when working with TanStack libraries such as Router, Query, Form, or Table—whether starting a new project or integrating into existing code.
---

# SKILL.md

## Tech Stack

- TanStack Start（React）
- TanStack React Query
- Hono（API バックエンド）
- Drizzle ORM

## Key Patterns

- hc クライアントで型安全な API 呼び出し
- refetch で更新（invalidateQueries は使わない）
- Suspense + use() でデータフェッチ
- Skeleton でローディング表示
- query を子コンポーネントに渡す

## Hono API

API の基盤となる factory パターンとルート定義。

→ [references/hono-api.md](references/hono-api.md)

## hc クライアント

Hono の型安全な RPC クライアント。フロントエンドから API を呼び出す。

→ [references/hc-client.md](references/hc-client.md)

## 認証

JWT + Cookie ベースの認証。authMiddleware でルートを保護。

→ [references/auth.md](references/auth.md)

## セッション管理

React Context + React Query でセッション状態を管理。useSession フックで取得。

→ [references/session-context.md](references/session-context.md)

## データフェッチ

Suspense + use() パターン。親で useQuery、子で use() でデータ取得。

→ [references/suspense-use.md](references/suspense-use.md)

## Cloudflare

Cloudflare Workers + D1 を使う場合の設定。HonoEnv、databaseMiddleware、drizzle.config.ts。

→ [references/cloudflare.md](references/cloudflare.md)

## TanStack Start 固有

### BASIC 認証

サーバーミドルウェアで BASIC 認証を実装する場合。

→ [references/tanstack-start/basic-auth.md](references/tanstack-start/basic-auth.md)
