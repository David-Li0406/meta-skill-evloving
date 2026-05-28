---
name: authentication
description: Implement authentication with Supabase, OAuth providers, and session management. Use when adding login, OAuth flows, or protecting routes.
metadata:
  author: Bingify
  version: "1.0"
---

# Authentication & Session Management

このスキルは、Bingifyの認証実装とセッション管理をカバーします。

## 概要

BingifyはSupabaseAuth (メールOTP/Magic Link、OAuth) を使用し、認証は [proxy.ts](../../../proxy.ts) およびミドルウェア ([lib/middleware/auth-handlers.ts](../../../lib/middleware/auth-handlers.ts)) で保護されます。

## ログインフロー

### 1. ログインページ

[app/[locale]/login/page.tsx](../../../app/%5Blocale%5D/login/page.tsx) で以下を処理：

- ユーザーがメールアドレスを入力
- OAuthプロバイダー (Google、Twitchなど) のボタンをクリック
- `redirect` クエリパラメータで認証後の遷移先を指定

### 2. OAuthフロー (例：Google OAuth)

```tsx
// 実装例: app/[locale]/login/_components/login-form.tsx
"use client";

export function LoginForm() {
  // signInWithOAuth呼び出し → プロバイダーのログインページへリダイレクト
  return (
    <button
      onClick={async () => {
        await signInWithGoogle(redirect);
      }}
    >
      Sign in with Google
    </button>
  );
}
```

**実装詳細**:

- `signInWithGoogle()` などのServer Actionsは [app/[locale]/login/\_actions/](../../../app/%5Blocale%5D/login/_actions/) に配置
- `supabase.auth.signInWithOAuth()` でプロバイダーのログインページにリダイレクト
- ユーザー認可後、`redirectTo` で指定したコールバックURLへリダイレクト
  - 例: `https://example.com/auth/google/callback`

### 3. コールバック処理 (コード→セッション交換)

- プロバイダーからリダイレクトされた `/auth/[provider]/callback` で `code` パラメータを受け取ります
- [app/auth/[provider]/callback/route.ts](../../../app/auth/%5Bprovider%5D/callback/route.ts) が処理：
  1. **リトライロジック**: `exchangeCodeForSession()` を最大2回まで実行(ネットワークエラー時は再試行)
  2. **セッション取得**: 交換後に `getSession()` でセッション情報を取得
  3. **トークン保存**: OAuthトークン(`provider_token`, `provider_refresh_token`)をRPC関数 `upsert_oauth_token` / `get_oauth_token` 経由で保存。暗号化・復号はSupabase Vault側(RPC層)で自動的に処理される
  4. **メタデータ設定**: 言語情報を `user_metadata.language` に設定
  5. **リダイレクト**: 認証成功後、`redirect` パラメータで指定した遷移先(またはダッシュボード)へリダイレクト

**エラーハンドリング**:

- OAuthトークン交換失敗時: `/login?error=auth_failed` へリダイレクト
- セッション取得失敗時: `/login?error=auth_failed` へリダイレクト

**参考実装**:

- [app/auth/[provider]/callback/route.ts](../../../app/auth/%5Bprovider%5D/callback/route.ts) - OAuthコールバック処理
- [app/auth/callback/route.ts](../../../app/auth/callback/route.ts) - メールOTPコールバック処理

## ミドルウェア保護

### 実装位置

- [proxy.ts](../../../proxy.ts) - 統一エントリーポイント
- [lib/middleware/auth-handlers.ts](../../../lib/middleware/auth-handlers.ts) - 認証ハンドラー

### 保護ルート

**ダッシュボード保護** (`/dashboard/*`):

- `handleAuthenticatedRoute()` で認証ユーザーのみ許可
- 未認証の場合、`/login` へリダイレクト(`redirect` パラメータで元のパスを指定)

**管理画面保護** (`/admin/*`):

- `handleAdminAuth()` でAdminロールのみ許可
- 未認証の場合、`/login` へリダイレクト
- 認証済みだがAdminロールがない場合、ホームへリダイレクト

### 実装例

```typescript
// proxy.ts から抽出
export function proxy(request: NextRequest) {
  // 1. Basic Auth チェック(最優先)
  const authResponse = checkBasicAuth(request);
  if (authResponse) {
    return authResponse;
  }

  // 2. ダッシュボード保護
  if (isDashboardPath(pathname)) {
    return handleAuthenticatedRoute(request, pathname);
  }

  // 3. 管理画面保護
  if (isAdminPath(pathname)) {
    return handleAdminAuth(request, pathname);
  }

  // 4. その他のルーティング
  return intlMiddleware(request);
}
```

## コーディングエージェント向け：ログイン方法

### 開発環境でのテスト

開発環境でのログイン動作確認は以下のいずれかで行えます。

#### 方法 1: Magic Link (メール OTP) を使用

メールOTPによるログインはMailpitを使用して確認できます。

**前提条件**:

- Supabaseが起動している: `pnpm run local:setup`
- Mailpitが起動している(Supabaseの一部)

**ステップ**:

1. [http://localhost:3000/login](http://localhost:3000/login) にアクセス
2. メールアドレスを入力して「Send Magic Link」をクリック
3. Mailpit UI ([http://localhost:54324](http://localhost:54324)) でメールを確認
4. メール内のマジックリンクをクリックでログイン完了

**ブラウザー自動化での実装例**:

```typescript
// テストでのシミュレーション
// 注: mcp_next は別途初期化が必要な場合は await で取得
const browser = await devtools_browser_eval.start();
await browser.navigate("http://localhost:3000/login");
await browser.fill_form([
  { selector: 'input[type="email"]', value: "user@example.com" },
]);
await browser.click('button[type="submit"]');
// Mailpit からトークンを取得してコールバックをシミュレート
```

#### 方法 2: OAuth プロバイダーをモック

OAuthフローのテストは、Supabaseのテスト設定やスタブ化を使用します。

**参考**:

- [app/auth/[provider]/callback/**tests**/route.test.ts](../../../app/auth/%5Bprovider%5D/callback/__tests__/route.test.ts) - OAuthコールバックテスト例
- OAuthトークン交換のリトライロジック、エラーハンドリングをカバー

#### 方法 3: データベースダイレクトアクセス

開発環境では `supabase` CLIでデータベースに直接アクセス可能：

```bash
pnpm exec supabase db push  # マイグレーション実行
pnpm exec supabase status   # Supabase ステータス確認
```

詳細は [supabase-setup スキル](../supabase-setup/SKILL.md) を参照してください。

### セッション検証

ログイン後のセッション状態は以下で確認：

```typescript
// クライアント側
const {
  data: { user },
  error,
} = await supabase.auth.getUser();
if (user) {
  console.log("Logged in as:", user.email);
}

// サーバー側(Server Actions)
const supabase = await createClient();
const {
  data: { user },
  error,
} = await supabase.auth.getUser();
```

### デバッグ方法

1. **ブラウザー開発者ツール**: ApplicationタブのCookiesセクションまたはNetworkタブでSupabaseセッションクッキー(例: `sb-<project-ref>-auth-token`)を確認。このリポジトリは `@supabase/ssr` の `createServerClient` とクッキーアダプターを使用したクッキーベースのセッション管理を採用([lib/supabase/server.ts](../../../lib/supabase/server.ts) 参照)
2. **Supabase ダッシュボード**: [console.supabase.com](https://console.supabase.com) で認証状態を確認
3. **Server Actions ログ**: `pnpm dev` の出力でサーバー側エラーを確認

## 参考

- [Supabase Auth](https://supabase.com/docs/guides/auth)
- [mailpit-testing スキル](../mailpit-testing/SKILL.md) - メールのローカルテスト
- [supabase-setup スキル](../supabase-setup/SKILL.md) - データベース初期化
