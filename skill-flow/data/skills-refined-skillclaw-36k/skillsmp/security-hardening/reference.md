# OWASP Top 10 Security Reference Guide

このドキュメントは、OWASP Top 10 2021に基づいた体系的なセキュリティチェックリストを提供します。

## A01:2021 – Broken Access Control (アクセス制御の不備)

### 概要
アクセス制御の不備により、ユーザーが権限外のデータやリソースにアクセスできる脆弱性。

### チェック項目

#### 認証・認可の実装
- [ ] すべての機密リソースに認証が必要か
- [ ] 認証バイパスの可能性がないか
- [ ] ロールベースアクセス制御（RBAC）が適切に実装されているか
- [ ] 権限チェックがサーバー側で行われているか（クライアント側のみではない）

#### リソースアクセス制御
- [ ] URLの直接入力による不正アクセスが防がれているか
- [ ] APIエンドポイントに適切な認可チェックがあるか
- [ ] ファイルパスの検証が行われているか（パストラバーサル対策）
- [ ] 他ユーザーのIDを使ったアクセスが防がれているか（IDOR対策）

#### CORS設定
- [ ] CORS設定が適切か（`*`を使用していないか）
- [ ] 信頼できるオリジンのみ許可しているか
- [ ] Credentials付きリクエストの設定が適切か

### 脆弱なコード例

```python
# ❌ 脆弱: IDを直接使用
@app.route('/user/<user_id>/profile')
def get_profile(user_id):
    # 認可チェックなし
    profile = db.get_user_profile(user_id)
    return jsonify(profile)

# ✅ 安全: 認可チェック
@app.route('/user/<user_id>/profile')
@login_required
def get_profile(user_id):
    if current_user.id != user_id and not current_user.is_admin:
        abort(403)
    profile = db.get_user_profile(user_id)
    return jsonify(profile)
```

### 対策

1. **デフォルト拒否**: すべてのリソースはデフォルトでアクセス拒否
2. **最小権限**: 必要最小限の権限のみ付与
3. **サーバー側検証**: すべての認可チェックはサーバー側で実施
4. **セッション無効化**: ログアウト時は確実にセッションを無効化
5. **ログ記録**: アクセス制御失敗をログに記録

---

## A02:2021 – Cryptographic Failures (暗号化の失敗)

### 概要
機密データの不適切な保護による情報漏洩の脆弱性。

### チェック項目

#### データ保護
- [ ] 機密データが平文で保存されていないか
- [ ] データベースの暗号化が有効か
- [ ] バックアップデータも暗号化されているか
- [ ] ログファイルに機密情報が記録されていないか

#### 通信の暗号化
- [ ] すべての通信がHTTPS/TLSで暗号化されているか
- [ ] TLS 1.2以上を使用しているか
- [ ] 証明書の検証が適切に行われているか
- [ ] HTTP Strict Transport Security (HSTS)が有効か

#### 暗号化アルゴリズム
- [ ] 弱い暗号化アルゴリズム（MD5、SHA1、DES）を使用していないか
- [ ] 適切な鍵長を使用しているか（AES-256、RSA-2048以上）
- [ ] ソルトとイテレーション数が適切か（パスワードハッシュ）
- [ ] 乱数生成が暗号学的に安全か

#### 鍵管理
- [ ] 暗号化鍵がハードコードされていないか
- [ ] 鍵の定期的なローテーションが行われているか
- [ ] 鍵へのアクセスが適切に制限されているか

### 脆弱なコード例

```python
# ❌ 脆弱: 弱いハッシュ化
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()

# ✅ 安全: bcrypt使用
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))

# ❌ 脆弱: 平文保存
config = {
    'api_key': 'sk-1234567890abcdef',
    'db_password': 'password123'
}

# ✅ 安全: 環境変数使用
import os
api_key = os.environ.get('API_KEY')
if not api_key:
    raise ValueError('API_KEY environment variable is required')
```

### 対策

1. **強力な暗号化**: AES-256、RSA-2048以上を使用
2. **パスワードハッシュ**: bcrypt、argon2、scrypt等を使用
3. **TLS強制**: すべての通信をHTTPS化
4. **鍵管理**: 環境変数または専用の鍵管理サービス使用
5. **データ分類**: 機密度に応じた適切な保護措置

---

## A03:2021 – Injection (インジェクション)

### 概要
信頼できないデータがコマンドやクエリの一部として実行される脆弱性。

### チェック項目

#### SQLインジェクション
- [ ] パラメータ化クエリを使用しているか
- [ ] ORM/クエリビルダーを使用しているか
- [ ] ユーザー入力を直接SQL文に埋め込んでいないか
- [ ] ストアドプロシージャを使用する場合も安全か

#### NoSQLインジェクション
- [ ] NoSQLクエリに入力検証があるか
- [ ] オブジェクト展開を安全に行っているか
- [ ] MongoDB等のクエリ演算子が適切にエスケープされているか

#### OSコマンドインジェクション
- [ ] システムコマンド実行を避けているか
- [ ] コマンド実行が必要な場合、入力を厳密に検証しているか
- [ ] シェルを経由しない実行方法を使っているか
- [ ] ホワイトリストで許可されたコマンドのみ実行しているか

#### LDAPインジェクション
- [ ] LDAP クエリが適切にエスケープされているか
- [ ] 特殊文字（*, (, ), \, NUL）が処理されているか

#### XMLインジェクション
- [ ] XML外部エンティティ（XXE）攻撃への対策があるか
- [ ] XMLパーサーが外部エンティティを無効化しているか
- [ ] DTD処理が無効化されているか

### 脆弱なコード例

```python
# ❌ 脆弱: SQLインジェクション
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)

# ✅ 安全: パラメータ化クエリ
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))

# ❌ 脆弱: OSコマンドインジェクション
import os
os.system(f"cat {filename}")

# ✅ 安全: 安全なAPI使用
with open(filename, 'r') as f:
    content = f.read()

# ❌ 脆弱: NoSQLインジェクション
db.users.find({ username: req.body.username })

# ✅ 安全: 入力検証
if (typeof req.body.username !== 'string') {
    throw new Error('Invalid username');
}
db.users.find({ username: req.body.username })
```

### 対策

1. **パラメータ化**: プリペアドステートメント/パラメータ化クエリ使用
2. **ORM使用**: ORM/クエリビルダーの活用
3. **入力検証**: すべての入力をホワイトリストで検証
4. **最小権限**: データベースユーザーに最小限の権限のみ付与
5. **エスケープ**: 特殊文字を適切にエスケープ

---

## A04:2021 – Insecure Design (安全でない設計)

### 概要
設計段階でのセキュリティ考慮不足による脆弱性。

### チェック項目

#### セキュリティ要件
- [ ] セキュリティ要件が明確に定義されているか
- [ ] 脅威モデリングが実施されているか
- [ ] リスク評価が行われているか
- [ ] セキュリティレビューが設計段階で行われているか

#### セキュアなデザインパターン
- [ ] 多層防御が実装されているか
- [ ] フェイルセーフな設計か
- [ ] 分離の原則が適用されているか
- [ ] 完全な媒介の原則が守られているか

#### ビジネスロジック
- [ ] ビジネスロジックの脆弱性がないか
- [ ] レート制限が適切に実装されているか
- [ ] リソース枯渇攻撃への対策があるか
- [ ] ワークフロー操作への対策があるか

### 脆弱な設計例

```python
# ❌ 脆弱: レート制限なし
@app.route('/api/expensive-operation', methods=['POST'])
def expensive_operation():
    # 重い処理
    result = perform_expensive_calculation()
    return jsonify(result)

# ✅ 安全: レート制限あり
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/expensive-operation', methods=['POST'])
@limiter.limit("5 per minute")
def expensive_operation():
    result = perform_expensive_calculation()
    return jsonify(result)
```

### 対策

1. **設計段階からセキュリティを組み込む**: Security by Design
2. **脅威モデリング**: STRIDE等のフレームワーク使用
3. **セキュアな開発ライフサイクル**: SDLC全体でセキュリティを考慮
4. **ピアレビュー**: 設計をチームでレビュー
5. **セキュリティパターン**: 実績のあるセキュアなパターンを使用

---

## A05:2021 – Security Misconfiguration (セキュリティ設定ミス)

### 概要
不適切なセキュリティ設定による脆弱性。

### チェック項目

#### デフォルト設定
- [ ] デフォルトアカウントが無効化されているか
- [ ] デフォルトパスワードが変更されているか
- [ ] 不要なサービスが無効化されているか
- [ ] サンプルアプリケーションが削除されているか

#### エラーハンドリング
- [ ] エラーメッセージに詳細情報が含まれていないか
- [ ] スタックトレースが本番環境で表示されないか
- [ ] デバッグモードが本番環境で無効か
- [ ] エラーログが適切に保護されているか

#### セキュリティヘッダー
- [ ] Content-Security-Policy が設定されているか
- [ ] X-Frame-Options が設定されているか
- [ ] X-Content-Type-Options が設定されているか
- [ ] Strict-Transport-Security (HSTS) が設定されているか
- [ ] Referrer-Policy が適切に設定されているか

#### パッチ管理
- [ ] すべてのソフトウェアが最新版か
- [ ] セキュリティパッチが適用されているか
- [ ] EOLソフトウェアを使用していないか

### 脆弱な設定例

```python
# ❌ 脆弱: 詳細なエラー表示
from flask import Flask
app = Flask(__name__)
app.config['DEBUG'] = True  # 本番環境でこれはNG

@app.errorhandler(500)
def internal_error(error):
    return str(error), 500  # スタックトレース露出

# ✅ 安全: 最小限のエラー情報
app.config['DEBUG'] = False

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {error}")
    return "An error occurred", 500
```

### 対策

1. **最小構成**: 必要最小限の機能のみ有効化
2. **セキュリティヘッダー**: 適切なHTTPヘッダーを設定
3. **定期的なパッチ適用**: 脆弱性修正を迅速に適用
4. **設定管理**: Infrastructure as Codeで設定を管理
5. **セキュリティスキャン**: 定期的な脆弱性スキャン実施

---

## A06:2021 – Vulnerable and Outdated Components (脆弱で古いコンポーネント)

### 概要
既知の脆弱性を持つライブラリやフレームワークの使用。

### チェック項目

#### 依存関係管理
- [ ] すべての依存関係のバージョンを把握しているか
- [ ] 依存関係の脆弱性スキャンを定期的に実施しているか
- [ ] 不要な依存関係がないか
- [ ] 推移的依存関係も管理されているか

#### バージョン管理
- [ ] サポート終了（EOL）のソフトウェアを使用していないか
- [ ] 最新の安定版を使用しているか
- [ ] セキュリティアップデートが適時適用されているか

#### ライセンス管理
- [ ] 使用しているライブラリのライセンスを確認しているか
- [ ] ライセンス違反がないか

### 脆弱性スキャン例

```bash
# Node.js
npm audit
npm audit fix

# Python
pip-audit
safety check

# Ruby
bundle audit
bundle update

# Go
go list -m all | nancy sleuth

# Rust
cargo audit

# Java
dependency-check --scan .
```

### 対策

1. **継続的な監視**: 依存関係の脆弱性を継続的に監視
2. **自動更新**: Dependabot等で自動的に更新
3. **最小化**: 不要な依存関係を削除
4. **信頼できるソース**: 公式リポジトリからのみ取得
5. **SBOMの作成**: Software Bill of Materialsを管理

---

## A07:2021 – Identification and Authentication Failures (識別と認証の失敗)

### 概要
認証メカニズムの不備による不正アクセス。

### チェック項目

#### パスワードポリシー
- [ ] 弱いパスワードが拒否されるか
- [ ] パスワードの複雑性要件があるか
- [ ] パスワードの最小長が適切か（12文字以上推奨）
- [ ] よく使われるパスワードのブラックリストがあるか

#### パスワード保存
- [ ] パスワードが平文で保存されていないか
- [ ] 適切なハッシュアルゴリズム（bcrypt、argon2等）を使用しているか
- [ ] ソルトが使用されているか
- [ ] 十分なイテレーション数か（bcryptで12以上）

#### 認証プロセス
- [ ] クレデンシャルスタッフィング対策があるか
- [ ] ブルートフォース攻撃対策があるか
- [ ] レート制限が実装されているか
- [ ] アカウントロックアウトメカニズムがあるか

#### セッション管理
- [ ] セッションIDが予測困難か
- [ ] セッションタイムアウトが適切に設定されているか
- [ ] ログアウト時にセッションが無効化されるか
- [ ] セッション固定攻撃への対策があるか

#### 多要素認証
- [ ] 機密性の高い操作にMFAが要求されるか
- [ ] TOTPやWebAuthnなど安全な方式を使用しているか

### 脆弱なコード例

```python
# ❌ 脆弱: 平文パスワード保存
user.password = password

# ✅ 安全: bcryptでハッシュ化
import bcrypt
user.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))

# ❌ 脆弱: 弱いセッションID
import random
session_id = str(random.randint(100000, 999999))

# ✅ 安全: 暗号学的に安全な乱数
import secrets
session_id = secrets.token_urlsafe(32)

# ❌ 脆弱: レート制限なし
@app.route('/login', methods=['POST'])
def login():
    # ログイン処理
    pass

# ✅ 安全: レート制限あり
from flask_limiter import Limiter
limiter = Limiter(app)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # ログイン処理
    pass
```

### 対策

1. **強力なパスワードポリシー**: NIST SP 800-63Bに準拠
2. **MFA実装**: すべての重要なアカウントでMFA必須
3. **セキュアなセッション管理**: 予測困難なID、適切なタイムアウト
4. **レート制限**: ログイン試行回数を制限
5. **監視とアラート**: 異常なログイン試行を検出

---

## A08:2021 – Software and Data Integrity Failures (ソフトウェアとデータの整合性の不備)

### 概要
整合性検証の欠如によるデータ改ざんや不正なコード実行。

### チェック項目

#### CI/CDセキュリティ
- [ ] CI/CDパイプラインが適切に保護されているか
- [ ] ビルド環境が隔離されているか
- [ ] シークレットが安全に管理されているか
- [ ] ビルド成果物の署名があるか

#### ソフトウェア更新
- [ ] ソフトウェア更新に署名検証があるか
- [ ] HTTPS経由で更新を取得しているか
- [ ] 更新の整合性チェックがあるか

#### デシリアライゼーション
- [ ] 信頼できないデータをデシリアライズしていないか
- [ ] デシリアライゼーション前に検証しているか
- [ ] 型チェックが行われているか

#### サプライチェーン
- [ ] 依存関係の取得元が信頼できるか
- [ ] 依存関係に署名検証があるか
- [ ] lockファイルが使用されているか

### 脆弱なコード例

```python
# ❌ 脆弱: 安全でないデシリアライゼーション
import pickle
data = pickle.loads(untrusted_data)  # RCEの危険

# ✅ 安全: 安全なフォーマット使用
import json
data = json.loads(untrusted_data)

# ❌ 脆弱: 署名検証なし
response = requests.get('http://example.com/update.zip')
with open('update.zip', 'wb') as f:
    f.write(response.content)

# ✅ 安全: 署名検証
import hashlib
response = requests.get('https://example.com/update.zip')
expected_hash = 'abc123...'
actual_hash = hashlib.sha256(response.content).hexdigest()
if actual_hash != expected_hash:
    raise ValueError('Hash mismatch')
```

### 対策

1. **デジタル署名**: すべての更新とアーティファクトに署名
2. **整合性チェック**: ハッシュ値の検証
3. **安全なデシリアライゼーション**: JSON等の安全な形式を使用
4. **CI/CD強化**: パイプラインへのアクセス制限、監査ログ
5. **SBOMの活用**: 依存関係の完全な可視化

---

## A09:2021 – Security Logging and Monitoring Failures (セキュリティログとモニタリングの失敗)

### 概要
不十分なログ記録や監視による攻撃の見逃し。

### チェック項目

#### ログ記録
- [ ] ログイン試行（成功・失敗）を記録しているか
- [ ] 認可失敗を記録しているか
- [ ] 入力検証エラーを記録しているか
- [ ] 重要な設定変更を記録しているか
- [ ] 機密データアクセスを記録しているか

#### ログ保護
- [ ] ログファイルが改ざんから保護されているか
- [ ] ログに機密情報が含まれていないか
- [ ] ログファイルへのアクセスが制限されているか
- [ ] ログインジェクション対策があるか

#### 監視とアラート
- [ ] セキュリティイベントの監視があるか
- [ ] 異常検知メカニズムがあるか
- [ ] アラート通知が適切に設定されているか
- [ ] インシデント対応プロセスがあるか

#### ログ保持
- [ ] ログの保持期間が適切に設定されているか
- [ ] 監査証跡として利用可能か
- [ ] ログのバックアップがあるか

### ログ記録例

```python
import logging
import json
from datetime import datetime

# ✅ 構造化ログ
logger = logging.getLogger(__name__)

def log_security_event(event_type, user_id, details):
    logger.warning(json.dumps({
        'timestamp': datetime.utcnow().isoformat(),
        'event_type': event_type,
        'user_id': user_id,
        'ip_address': request.remote_addr,
        'details': details
    }))

# ログイン失敗の記録
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = authenticate(username, password)
    if not user:
        log_security_event('LOGIN_FAILED', username, 'Invalid credentials')
        return 'Login failed', 401

    log_security_event('LOGIN_SUCCESS', user.id, 'User logged in')
    return 'Login successful', 200

# ❌ 脆弱: ログインジェクション
logger.info(f"User input: {user_input}")  # user_input に改行が含まれる可能性

# ✅ 安全: エスケープ処理
logger.info("User input: %s", user_input.replace('\n', '\\n'))
```

### 対策

1. **包括的なログ記録**: すべてのセキュリティイベントを記録
2. **集中ログ管理**: SIEM等で集中管理
3. **リアルタイム監視**: 異常を即座に検出
4. **ログの保護**: 改ざん防止、アクセス制限
5. **インシデント対応**: 明確なプロセスと責任者

---

## A10:2021 – Server-Side Request Forgery (SSRF)

### 概要
サーバーから意図しないリソースへのリクエストが可能になる脆弱性。

### チェック項目

#### URL検証
- [ ] ユーザー提供のURLを検証しているか
- [ ] URLスキームをホワイトリストで制限しているか（http/httpsのみ等）
- [ ] IPアドレスの直接指定を許可していないか
- [ ] プライベートIPアドレスへのアクセスをブロックしているか

#### 内部リソース保護
- [ ] 内部サービスへのアクセスが制限されているか
- [ ] メタデータAPIへのアクセスが制限されているか（AWS EC2等）
- [ ] localhostへのアクセスが制限されているか
- [ ] DNSリバインディング対策があるか

#### リダイレクト制御
- [ ] オープンリダイレクトの脆弱性がないか
- [ ] リダイレクト先のURLを検証しているか
- [ ] リダイレクト回数を制限しているか

### 脆弱なコード例

```python
# ❌ 脆弱: URL検証なし
import requests

@app.route('/fetch')
def fetch_url():
    url = request.args.get('url')
    response = requests.get(url)  # SSRF脆弱性
    return response.content

# ✅ 安全: URL検証あり
from urllib.parse import urlparse
import ipaddress

ALLOWED_SCHEMES = ['http', 'https']
BLOCKED_NETWORKS = [
    ipaddress.ip_network('10.0.0.0/8'),
    ipaddress.ip_network('172.16.0.0/12'),
    ipaddress.ip_network('192.168.0.0/16'),
    ipaddress.ip_network('127.0.0.0/8'),
]

@app.route('/fetch')
def fetch_url():
    url = request.args.get('url')

    # URLパース
    parsed = urlparse(url)

    # スキーム検証
    if parsed.scheme not in ALLOWED_SCHEMES:
        return 'Invalid scheme', 400

    # ホスト名からIPアドレス取得
    try:
        ip = ipaddress.ip_address(socket.gethostbyname(parsed.hostname))
    except Exception:
        return 'Invalid hostname', 400

    # プライベートIPブロック
    for network in BLOCKED_NETWORKS:
        if ip in network:
            return 'Access to private IP is forbidden', 403

    # 安全にリクエスト
    response = requests.get(url, timeout=5)
    return response.content
```

### 対策

1. **入力検証**: URLのスキーム、ホスト、ポートを検証
2. **ホワイトリスト**: 許可されたドメインのみアクセス可能に
3. **ネットワーク分離**: アプリケーションサーバーと内部サービスを分離
4. **プライベートIP拒否**: 10.0.0.0/8、172.16.0.0/12、192.168.0.0/16をブロック
5. **DNS検証**: DNSレスポンスの再検証

---

## 言語別セキュリティチェックリスト

### Python

- [ ] `pickle`の使用を避ける（または信頼できるデータのみ）
- [ ] `eval()`、`exec()`の使用を避ける
- [ ] `os.system()`ではなく`subprocess`を使用
- [ ] `bandit`でセキュリティスキャン実施
- [ ] `pip-audit`で依存関係の脆弱性確認

### JavaScript/Node.js

- [ ] `eval()`の使用を避ける
- [ ] `innerHTML`ではなく`textContent`を使用
- [ ] `npm audit`で依存関係の脆弱性確認
- [ ] ESLintに`eslint-plugin-security`を追加
- [ ] `helmet`でセキュリティヘッダー設定

### Java

- [ ] デシリアライゼーションに注意
- [ ] PreparedStatementを使用（Statement避ける）
- [ ] `dependency-check`で脆弱性スキャン
- [ ] SpotBugsでセキュリティバグ検出

### Go

- [ ] `gosec`でセキュリティスキャン
- [ ] `nancy`で依存関係の脆弱性確認
- [ ] SQLインジェクション対策（パラメータ化クエリ）
- [ ] コマンドインジェクション対策

### Ruby

- [ ] `bundle audit`で依存関係確認
- [ ] `brakeman`で静的解析
- [ ] Strong Parametersの使用（Rails）
- [ ] 生のSQLを避ける

---

## セキュリティテストチェックリスト

### 単体テスト
- [ ] 入力検証のテスト（境界値、不正値）
- [ ] 認証・認可のテスト
- [ ] 暗号化処理のテスト
- [ ] エラーハンドリングのテスト

### 統合テスト
- [ ] セキュリティヘッダーの検証
- [ ] CSRF保護の検証
- [ ] セッション管理の検証
- [ ] APIセキュリティの検証

### 脆弱性テスト
- [ ] SQLインジェクションテスト
- [ ] XSSテスト
- [ ] CSRF テスト
- [ ] SSRFテスト
- [ ] 認証バイパステスト
- [ ] 権限昇格テスト

---

## 参考リソース

- [OWASP Top 10 2021](https://owasp.org/Top10/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [SANS Top 25 Software Errors](https://www.sans.org/top25-software-errors/)
