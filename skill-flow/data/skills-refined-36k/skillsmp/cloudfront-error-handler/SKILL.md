---
name: cloudfront-error-handler
description: CloudFront配下のAPI/フロントエンドのエラーに対応し、アクセス検証、原因特定、対処、検証を体系的に行います。CloudFront経由のアクセスでエラーが発生した場合に使用してください。
---

# CloudFrontエラー対応スキル

このスキルは、CloudFront経由で発生するエラーに対して体系的に対応し、問題を解決します。

## 利用可能なツール

- **web_fetch**: CloudFront経由のHTTPレスポンス確認
- **playwright-browser**: ブラウザ操作（User-Agent偽装含む）
- **bash**: curlやnodeスクリプトによる検証
- **view**: 関連コードの確認
- **rg**: ログやコードの検索
- **edit**: 必要な修正の実施

## 使用すべきタイミング

- CloudFront配下の `/api/*` が 4xx/5xx を返す場合
- CloudFront配下でフロントが読み込まれない場合
- API GatewayやLambdaの統合エラーが疑われる場合

## 実行手順

### 1. CloudFront経由での疎通確認

```bash
curl -i https://<cloudfront-domain>/
curl -i https://<cloudfront-domain>/api/health
```

### 2. User-Agent偽装の検証

```bash
curl -i -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36" https://<cloudfront-domain>/
```

Playwrightで検証する場合はTLSエラー無視を有効にする:

```ts
const context = await browser.newContext({
  userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
  ignoreHTTPSErrors: true,
});
```

### 3. CloudFrontのオリジン確認

- `infrastructure/deploy/lib/constructs/frontend.ts` の `additionalBehaviors` を確認
- `/api/*` のオリジンが API Gateway か確認

### 4. Lambda配布物の確認

- `infrastructure/deploy/lib/constructs/backend.ts` の Lambdaバンドル方法を確認
- バンドルに依存関係が含まれるか検証

### 5. 依頼者への説明テンプレート

```
## エラー概要

**CloudFront URL**: <cloudfront-url>
**エラー内容**: <ステータスコードとメッセージ>

## 原因

<原因の説明>

## 対応内容

- <修正内容>

## 検証結果

- ✅ curl / Playwright で再確認
```
