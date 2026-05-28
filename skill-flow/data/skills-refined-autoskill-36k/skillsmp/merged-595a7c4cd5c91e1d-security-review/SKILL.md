---
name: security-review
description: Use this skill when conducting security reviews based on the OWASP Top 10, focusing on vulnerabilities such as SQL injection, XSS, authentication, and data protection.
---

# Security Review

## Purpose

このスキルは、OWASP Top 10に基づいたセキュリティ脆弱性のチェックを提供します。以下の観点でコードをレビューします:

- 入力検証とサニタイゼーション
- 認証・認可の適切な実装
- セキュアなエラーハンドリング
- インジェクション攻撃対策（SQL、NoSQL、コマンド等）
- XSS（クロスサイトスクリプティング）対策
- CSRF（クロスサイトリクエストフォージェリ）対策
- 機密データの保護
- セキュアな暗号化実装
- セキュリティ設定のミス検出
- 既知の脆弱性を持つコンポーネントの特定

## When to Use

以下の場合にこのスキルを使用:

- 認証・認可コードを実装する際
- ユーザー入力を処理する際
- 機密データを取り扱う際
- セキュリティレビューを実施する際
- OWASP Top 10準拠の確認

## Instructions

### 1. Understand the Context

セキュリティ強化対象を明確化:

```bash
# 対象ファイルの確認
git status
git diff --name-only
```

### 2. Identify Security Requirements

プロジェクトのセキュリティ要件を特定:

- **公開WebアプリケーションAPI**: すべてのOWASP Top 10対策
- **内部ツール・CLI**: インジェクション対策、機密情報保護
- **データ処理バッチ**: ログインインジェクション、ファイルパストラバーサル

### 3. Conduct OWASP Top 10 Security Scan

以下の観点で体系的にスキャン:

- **A01: Broken Access Control**: 認可チェックの実装
- **A02: Cryptographic Failures**: 機密データの暗号化
- **A03: Injection**: SQLインジェクション対策
- **A04: Insecure Design**: 脅威モデリングの実施
- **A05: Security Misconfiguration**: デフォルト資格情報の変更
- **A06: Vulnerable Components**: 依存関係の最新化
- **A07: Authentication Failures**: 強力なパスワードポリシー
- **A08: Software Integrity Failures**: CI/CDパイプラインの安全性
- **A09: Security Logging Failures**: セキュリティイベントのログ記録
- **A10: Server-Side Request Forgery**: URL検証の実装

### 4. Implement Security Controls

検出された問題に対する対策を実装:

- **入力検証**: すべての外部入力を検証
- **インジェクション対策**: パラメータ化クエリの使用
- **認証情報の保護**: 環境変数での管理
- **セキュアな暗号化**: 強力なアルゴリズムの使用

### 5. Add Security Tests

セキュリティテストを追加:

- **入力検証テスト**: 不正な入力の拒否確認
- **認証テスト**: 未認証アクセスの拒否確認
- **インジェクション対策テスト**: SQLインジェクション等の防御確認

### 6. Security Logging

セキュリティイベントの適切なログ記録:

- ログイン試行（成功・失敗）
- 認可失敗
- 入力検証エラー

### 7. Dependency Security Audit

依存関係の脆弱性スキャン:

```bash
# 言語/ツール別
npm audit          # Node.js
pip-audit          # Python
bundle audit       # Ruby
go list -m all | nancy  # Go
cargo audit        # Rust
```

### 8. Provide Security Report

セキュリティ強化の結果をレポート形式で提供:

```markdown
## セキュリティ強化レポート

### 🔴 Critical Vulnerabilities
- [問題の説明]
- [修正方法]

### 🟡 High Risk Issues
- [問題の説明]
- [推奨される対策]

### 🟢 Security Best Practices Implemented
- [実装されている良いセキュリティ対策]
```

## Key Principles

1. **Defense in Depth**: 複数の層でセキュリティを確保
2. **Least Privilege**: 必要最小限の権限のみを付与
3. **Fail Securely**: エラー時にセキュアな状態を維持
4. **Security by Design**: 最初からセキュリティを組み込む
5. **Don't Trust User Input**: すべての外部入力を検証・サニタイズ

## Secure Coding Guidelines

### DO
- ✅ すべての外部入力を検証する
- ✅ パラメータ化クエリを使用する
- ✅ 機密データを暗号化する

### DON'T
- ❌ 認証情報をハードコードしない
- ❌ MD5、SHA1などの弱い暗号化を使用しない
- ❌ 平文でパスワードを保存しない

## Reference Documents

- [OWASP Top 10詳細チェックリスト](reference.md)

## Integration with Other Skills

このスキルは他のスキルと組み合わせて使用できます:

- **code-review**: コードレビュー時にセキュリティ観点を追加
- **tdd-***: テスト駆動開発でセキュリティテストを含める
- **rev-***: 設計レビュー段階でセキュリティ要件を組み込む

## Notes

- セキュリティは継続的なプロセスです。一度の対策で終わりではありません
- 新しい脆弱性は日々発見されるため、定期的な見直しが必要です