---
name: security-error-review
description: セキュリティ・エラーハンドリングレビュー - OWASP Top 10、エラー処理、ログ管理を統合評価
requires-guidelines:
  - common
---

# セキュリティ・エラーハンドリングレビュー（統合版）

## 統合スコープ

1. **セキュリティ** - OWASP Top 10、インジェクション対策、認証・セッション管理
2. **エラーハンドリング** - エラー握りつぶし、適切なログ、エラー伝播

## 使用タイミング

- API実装時 / 認証・認可機能実装時 / 本番エラー調査 / セキュリティレビュー時

---

## レビュー観点

### 🔴 Critical（修正必須）

| 観点 | 検出パターン | 対策 |
|------|-------------|------|
| SQLインジェクション | 文字列結合でクエリ構築 | パラメータ化クエリ使用 |
| XSS | innerHTML直接代入 | textContent or DOMPurify |
| 認証不備 | パスワード平文保存 | bcrypt等でハッシュ化 |
| セッション漏洩 | URLにセッションID | HttpOnly/Secure Cookie |
| 情報露出 | エラーにDB情報含む | 一般的メッセージのみ返却 |
| エラー握りつぶし | 空catch/err無視 | ログ+適切な例外伝播 |
| 機密情報ログ | password/tokenログ出力 | センシティブ情報除外 |

### 🟡 Warning（要改善）

| 観点 | 検出パターン | 対策 |
|------|-------------|------|
| ヘッダー不足 | CSP/HSTS未設定 | セキュリティヘッダー追加 |
| レート制限なし | 認証APIに制限なし | express-rate-limit等 |
| 汎用catch | "Something went wrong" | エラー種別で分岐 |
| リトライなし | 外部API1回呼び出し | exponential backoff |

**コード例が必要な場合**: Context7で「OWASP secure coding」「error handling best practices」を検索

---

## OWASP Top 10 (2021)

| ランク | カテゴリ | 主な対策 |
|--------|----------|----------|
| A01 | Broken Access Control | 認可チェック、最小権限 |
| A02 | Cryptographic Failures | HTTPS、bcrypt |
| A03 | Injection | パラメータ化クエリ |
| A04 | Insecure Design | 脅威モデリング |
| A05 | Security Misconfiguration | セキュリティヘッダー |
| A06 | Vulnerable Components | 依存パッケージ更新 |
| A07 | Auth Failures | MFA、セッション管理 |
| A08 | Data Integrity | 署名検証 |
| A09 | Logging Failures | 構造化ログ |
| A10 | SSRF | URLホワイトリスト |

---

## チェックリスト

**セキュリティ**: パラメータ化クエリ / 入力検証 / パスワードハッシュ / HttpOnly Cookie / セキュリティヘッダー / レート制限

**エラーハンドリング**: 全エラー処理 / コンテキスト付加 / 機密情報除外 / エラーラップ（Go: %w）

---

## 出力形式

```
## セキュリティ・エラーハンドリングレビュー結果

### セキュリティ
🔴 Critical: `ファイル:行` - 問題 - 修正案

### エラーハンドリング
🔴 Critical: `ファイル:行` - 問題 - 修正案

📊 Summary: Critical X件 / Warning Y件
```

---

## 外部リソース

- **Context7**: OWASP Top 10、CWE、セキュアコーディングガイド
- **Serena memory**: プロジェクト固有の認証方式・ログ戦略
