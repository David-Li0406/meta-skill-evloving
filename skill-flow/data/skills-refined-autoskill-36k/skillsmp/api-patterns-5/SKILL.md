---
name: api-patterns
description: REST API設計とセキュリティのベストプラクティス。認証、バリデーション、エラーハンドリングに使用。
triggers:
  - API
  - authentication
  - auth
  - REST
  - endpoint
allowed-tools: Read, Write, Edit, Grep, Bash, mcp__fetch
version: 1.0
---

# API Best Practices

## 原則（仕様は既存コードから調査すること）

- OWASP準拠: Secure cookies, rate limiting, no hard-coded secrets
- Input validation: Zodスキーマ必須
- Error handling: 適切なHTTPステータス、エラーメッセージ
- 認証: 環境変数から秘密鍵取得

## 発動時のワークフロー

### 1. 調査（実装前に必ず実行）
```bash
# 既存APIの確認
find app/api -name "*.ts" | head -20

# 認証パターンの確認
grep -r "auth" app/api/ --include="*.ts"

# 既存スキーマの確認
grep -r "z.object" src/ --include="*.ts"

# 環境変数の使用確認
grep -r "process.env" src/lib/ --include="*.ts"
```

### 2. セキュリティチェック（必須）
```bash
# ハードコードされた秘密鍵の検出
grep -r "secret\|password\|key" src/ --include="*.ts" | grep -v "process.env"

# 認証なしエンドポイントの確認
grep -L "auth" app/api/**/route.ts
```

### 3. 実装
- 既存パターンに従う
- Zodでinput validation
- 適切なエラーハンドリング

### 4. 検証（必須）
```bash
# 静的解析
npm run type-check
npm run lint

# ビルド確認
npm run build

# APIテスト（curl or fetch MCP）
curl -X GET http://localhost:3000/api/endpoint
```

### 5. API動作確認（fetch MCP使用）
- 正常系: 期待するレスポンス
- 異常系: 不正入力、認証エラー
- エッジケース: レート制限、タイムアウト

## 報告形式

```
## API実装レポート

### セキュリティチェック結果
- [ ] ハードコードされた秘密鍵なし
- [ ] 認証が必要なエンドポイントは保護済み
- [ ] Input validation実装済み

### 変更内容
- ファイル: 変更概要

### API検証結果
- エンドポイント: URL
- 正常系: ステータス、レスポンス
- 異常系: ステータス、エラーメッセージ
```
