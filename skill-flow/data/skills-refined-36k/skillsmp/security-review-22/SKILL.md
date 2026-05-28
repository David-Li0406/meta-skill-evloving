---
name: security-review
description: |
  このスキルは、ユーザーが「セキュリティ」「脆弱性」「OWASP」「XSS」「SQLインジェクション」「認証」「認可」「機密情報」について質問したとき、またはセキュリティレビューが必要なときに使用する。
---

# Security Review

## OWASP Top 10 チェックリスト

### A01: Broken Access Control

- [ ] 認可チェックが全エンドポイントに実装されている
- [ ] 水平権限昇格が防止されている
- [ ] CORS が適切に設定されている

### A02: Cryptographic Failures

- [ ] 機密データが暗号化されている
- [ ] HTTPS が強制されている
- [ ] 安全な暗号アルゴリズムを使用している

### A03: Injection

- [ ] SQL インジェクション対策（ORM 使用）
- [ ] XSS 対策（自動エスケープ）
- [ ] コマンドインジェクション対策

### A04: Insecure Design

- [ ] 脅威モデリングが実施されている
- [ ] セキュリティ要件が定義されている
- [ ] 防御の深さが実装されている

### A05: Security Misconfiguration

- [ ] デフォルト資格情報が変更されている
- [ ] 不要な機能が無効化されている
- [ ] エラーメッセージが適切

### A06: Vulnerable Components

- [ ] 依存関係が最新
- [ ] npm audit がクリーン
- [ ] 既知の脆弱性なし

### A07: Authentication Failures

- [ ] 強力なパスワードポリシー
- [ ] MFA が利用可能
- [ ] セッション管理が安全

### A08: Software Integrity Failures

- [ ] CI/CD パイプラインが安全
- [ ] 依存関係の整合性チェック
- [ ] コード署名

### A09: Security Logging Failures

- [ ] セキュリティイベントがログ記録される
- [ ] ログが改ざん防止されている
- [ ] 監視アラートが設定されている

### A10: Server-Side Request Forgery

- [ ] URL 検証が実装されている
- [ ] 内部ネットワークへのアクセスが制限されている

## 入力検証

```typescript
import { z } from "zod";

// スキーマベースのバリデーション
const UserInput = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(50),
  age: z.number().int().positive().max(150),
});

// 使用
const result = UserInput.safeParse(input);
if (!result.success) {
  // エラーハンドリング
}
```

## 機密情報の保護

### 環境変数

```bash
# .env.local（gitignore に追加）
DATABASE_URL=postgresql://...
API_SECRET=...

# .env.example（コミット可能）
DATABASE_URL=your_database_url
API_SECRET=your_api_secret
```

### 検出パターン

```bash
# 機密情報の検出
grep -r "password\|secret\|api_key\|token" --include="*.ts"
grep -r "https\?://" --include="*.ts" --include="*.tsx"
```

## 金融システム追加チェック

- [ ] トランザクションの原子性
- [ ] 二重支払い防止
- [ ] 監査ログの実装
- [ ] レート制限
- [ ] ウォレット署名検証（Web3）
