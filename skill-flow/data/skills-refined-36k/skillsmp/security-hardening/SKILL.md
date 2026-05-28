---
name: security-hardening
description: |
  OWASP Top 10に準拠したセキュアなコード実装を支援。入力検証、認証・認可、
  セキュアなエラーハンドリング、SQL/XSS/CSRF対策などのセキュリティ強化を実施。
  「セキュリティチェック」「脆弱性スキャン」「OWASP準拠」などの指示で起動。
---

# Security Hardening Skill

## Purpose

このスキルは、OWASP Top 10に基づいた包括的なセキュリティ強化を提供します:

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

- 新機能実装前のセキュリティ設計レビュー
- 「セキュリティ強化して」という明示的な指示
- OWASP Top 10準拠の確認
- 脆弱性診断・スキャンの実施
- 認証・認可機能の実装時
- 外部入力を扱うコードの実装時
- セキュリティインシデント後の再発防止

## Instructions

### 1. Understand the Context

セキュリティ強化対象を明確化:

```bash
# 対象ファイルの確認
git status
git diff --name-only

# または特定のファイル/ディレクトリが指定されている場合
# PRの場合は差分を確認
gh pr diff
```

**確認事項**:
- アプリケーションのタイプ（Web API、フロントエンド、CLIツール等）
- 扱うデータの機密性レベル
- 外部入力の有無（ユーザー入力、API、ファイル等）
- 認証・認可の実装状況
- 現在のセキュリティ対策レベル

### 2. Identify Security Requirements

プロジェクトのセキュリティ要件を特定:

**プロジェクトタイプ別の重要度**:

- **公開WebアプリケーションAPI**:
  - 🔴 Critical: すべてのOWASP Top 10対策
  - 認証・認可、入力検証、XSS/CSRF対策必須

- **内部ツール・CLI**:
  - 🟡 High: インジェクション対策、機密情報保護
  - 入力検証、コマンドインジェクション対策必須

- **データ処理バッチ**:
  - 🟡 High: ログインジェクション、ファイルパストラバーサル
  - 安全なファイル操作、ログの適切な処理

### 3. Conduct OWASP Top 10 Security Scan

以下の観点で体系的にスキャン（詳細は[reference.md](reference.md)参照）:

#### A01:2021 – Broken Access Control (アクセス制御の不備)
- 認証なしでアクセス可能な機密リソース
- 権限昇格の可能性
- 不適切なCORS設定
- 強制的ブラウジング（予測可能なURL）

#### A02:2021 – Cryptographic Failures (暗号化の失敗)
- 平文での機密データ保存・送信
- 弱い暗号化アルゴリズム（MD5、SHA1等）
- 不適切な鍵管理
- HTTPSの未使用

#### A03:2021 – Injection (インジェクション)
- SQLインジェクション
- NoSQLインジェクション
- OSコマンドインジェクション
- LDAPインジェクション
- XPath/XMLインジェクション

#### A04:2021 – Insecure Design (安全でない設計)
- セキュリティ要件の欠如
- 脅威モデリングの未実施
- セキュアなデザインパターンの未適用
- ビジネスロジックの脆弱性

#### A05:2021 – Security Misconfiguration (セキュリティ設定ミス)
- デフォルト認証情報の使用
- 不要な機能の有効化
- 詳細すぎるエラーメッセージ
- セキュリティヘッダーの欠如

#### A06:2021 – Vulnerable and Outdated Components (脆弱で古いコンポーネント)
- 既知の脆弱性を持つライブラリ
- サポート終了のソフトウェア
- 未パッチの依存関係

#### A07:2021 – Identification and Authentication Failures (識別と認証の失敗)
- 弱いパスワードポリシー
- クレデンシャルスタッフィング対策の欠如
- セッション管理の不備
- 不適切なパスワード保存

#### A08:2021 – Software and Data Integrity Failures (ソフトウェアとデータの整合性の不備)
- 署名なしのアップデート
- CI/CDパイプラインの脆弱性
- 信頼できないソースからのデシリアライゼーション
- 整合性検証の欠如

#### A09:2021 – Security Logging and Monitoring Failures (セキュリティログとモニタリングの失敗)
- 重要イベントのログ記録漏れ
- ログの不適切な保護
- 監視・アラートの欠如
- インシデント対応計画の不在

#### A10:2021 – Server-Side Request Forgery (SSRF) (サーバーサイドリクエストフォージェリ)
- 未検証のユーザー提供URL
- 内部リソースへのアクセス
- クラウドメタデータAPIへのアクセス

### 4. Implement Security Controls

検出された問題に対する対策を実装:

#### 入力検証
- すべての外部入力を検証
- 型チェック、範囲チェック、フォーマット検証
- ホワイトリスト方式の採用
- サニタイゼーション処理

#### インジェクション対策
- パラメータ化クエリ/プリペアドステートメント使用
- ORM/クエリビルダーの活用
- 入力のエスケープ処理
- 最小権限でのDB接続

#### 認証情報の保護
- 環境変数での管理
- ハードコードの禁止
- 秘密情報のバージョン管理除外
- 暗号化された設定ファイルの使用

#### セキュアな暗号化
- 強力なアルゴリズム使用（AES-256、SHA-256以上）
- 暗号学的に安全な乱数生成器
- 適切な鍵管理
- パスワードハッシュ化（bcrypt、argon2等）

### 5. Add Security Tests

セキュリティテストを追加:

- **入力検証テスト**: 不正な入力の拒否確認
- **認証テスト**: 未認証アクセスの拒否確認
- **認可テスト**: 権限外アクセスの拒否確認
- **インジェクション対策テスト**: SQLインジェクション等の防御確認
- **暗号化テスト**: データの適切な暗号化確認

### 6. Security Logging

セキュリティイベントの適切なログ記録:

- ログイン試行（成功・失敗）
- 認可失敗
- 入力検証エラー
- セキュリティ例外
- 設定変更
- データアクセス（機密情報）

**注意事項**:
- 機密情報（パスワード、トークン等）をログに記録しない
- ログの改ざん防止
- ログの安全な保存と管理

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

### 🔴 Critical Vulnerabilities (即座に修正が必要)
- [OWASP分類] [問題の説明]
- [場所とコード例]
- [修正方法]
- [CVE番号（該当する場合）]

### 🟡 High Risk Issues (修正を強く推奨)
- [問題の説明]
- [潜在的な影響]
- [推奨される対策]

### 🟠 Medium Risk Issues (修正を推奨)
- [問題の説明]
- [改善提案]

### 🟢 Security Best Practices Implemented
- [実装されている良いセキュリティ対策]

### 💡 Additional Recommendations
- [さらなるセキュリティ向上のための提案]

### 📊 OWASP Top 10 Compliance Status
- A01 Broken Access Control: ✅/⚠️/❌
- A02 Cryptographic Failures: ✅/⚠️/❌
- A03 Injection: ✅/⚠️/❌
- A04 Insecure Design: ✅/⚠️/❌
- A05 Security Misconfiguration: ✅/⚠️/❌
- A06 Vulnerable Components: ✅/⚠️/❌
- A07 Authentication Failures: ✅/⚠️/❌
- A08 Integrity Failures: ✅/⚠️/❌
- A09 Logging Failures: ✅/⚠️/❌
- A10 SSRF: ✅/⚠️/❌

### 🔧 Remediation Priority
1. [最優先で修正すべき項目]
2. [次に修正すべき項目]
3. [時間があれば修正する項目]
```

## Key Principles

1. **Defense in Depth（多層防御）**: 単一の防御策に依存せず、複数の層でセキュリティを確保
2. **Least Privilege（最小権限の原則）**: 必要最小限の権限のみを付与
3. **Fail Securely（安全な失敗）**: エラー時にセキュアな状態を維持
4. **Security by Design（設計段階からのセキュリティ）**: 後付けではなく最初から組み込む
5. **Don't Trust User Input（ユーザー入力を信用しない）**: すべての外部入力を検証・サニタイズ

## Secure Coding Guidelines

### DO (実施すべきこと)
- ✅ すべての外部入力を検証する
- ✅ パラメータ化クエリを使用する
- ✅ 機密データを暗号化する
- ✅ セキュアな乱数生成器を使用する（`crypto.randomBytes()`）
- ✅ HTTPSを強制する
- ✅ セキュリティヘッダーを設定する
- ✅ 最小権限の原則を適用する
- ✅ セキュリティイベントをログに記録する
- ✅ 依存関係を定期的に更新する
- ✅ エラーメッセージで詳細情報を漏らさない

### DON'T (避けるべきこと)
- ❌ 認証情報をハードコードしない
- ❌ MD5、SHA1などの弱い暗号化を使用しない
- ❌ 平文でパスワードを保存しない
- ❌ クエリに直接ユーザー入力を埋め込まない
- ❌ `eval()`や同等の機能を使用しない
- ❌ デフォルト認証情報を使用しない
- ❌ エラーでスタックトレースを露出しない
- ❌ セキュリティ対策を「後で」に先延ばししない

## Reference Documents

- [OWASP Top 10詳細チェックリスト](reference.md)

## Dependencies

### Required
- Git (変更差分の確認用)
- プロジェクトのソースコード（読み取り・書き込み）
- 依存関係マニフェスト（言語固有）

### Recommended
- 言語別セキュリティ監査ツール:
  - Node.js: `npm audit`, `snyk`
  - Python: `pip-audit`, `safety`
  - Ruby: `bundle audit`, `brakeman`
  - Go: `nancy`, `gosec`
  - Rust: `cargo audit`
  - Java: `dependency-check`
- SAST（Static Application Security Testing）ツール
  - SonarQube
  - Snyk
  - GitHub Advanced Security / CodeQL
  - Semgrep
- Linter with security plugins
  - ESLint + eslint-plugin-security
  - Pylint + bandit
  - RuboCop
  - golangci-lint

## Integration with Other Skills

このスキルは他のスキルと組み合わせて使用できます:

- **code-review**: コードレビュー時にセキュリティ観点を追加
- **tdd-***: テスト駆動開発でセキュリティテストを含める
- **rev-***: 設計レビュー段階でセキュリティ要件を組み込む

## Notes

- セキュリティは継続的なプロセスです。一度の対策で終わりではありません
- 新しい脆弱性は日々発見されるため、定期的な見直しが必要です
- セキュリティとユーザビリティのバランスを考慮してください
- コンプライアンス要件（GDPR、HIPAA等）も確認してください
