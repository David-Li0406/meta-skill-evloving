# コードレビューガイド

## 目次
- レビュープロセス
- 言語別チェックポイント
- よくある問題パターン
- フィードバックの書き方
- 自動化ツール

## レビュープロセス

### 1. 変更概要の把握

```
確認項目:
- PR/MRの説明を読む
- 関連するチケット/Issueを確認
- コミット履歴で変更の流れを把握
- 変更ファイル数と規模を確認
```

### 2. 全体構造の確認

```
確認項目:
- アーキテクチャへの影響
- 新しい依存関係
- ファイル配置の適切さ
- 公開APIの変更
```

### 3. 詳細レビュー

#### 正確性

```python
# ❌ 境界値エラー
for i in range(len(items)):  # off-by-oneの可能性
    process(items[i])

# ✅ イテレータを使用
for item in items:
    process(item)
```

```python
# ❌ Null安全でない
def get_name(user):
    return user.profile.name  # userやprofileがNoneの可能性

# ✅ Null安全
def get_name(user):
    if user and user.profile:
        return user.profile.name
    return None
```

#### エラーハンドリング

```python
# ❌ エラーを握りつぶす
try:
    result = risky_operation()
except:
    pass

# ✅ 適切なエラー処理
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise
```

#### リソース管理

```python
# ❌ リソースリーク
f = open("file.txt")
content = f.read()
# closeされない

# ✅ コンテキストマネージャ
with open("file.txt") as f:
    content = f.read()
```

## 言語別チェックポイント

### Python

```
□ 型ヒントが適切に使用されているか
□ docstringが記述されているか
□ f-stringを使用しているか（%やformatではなく）
□ リスト内包表記が適切に使用されているか
□ asyncの使い方が正しいか
□ 仮想環境/依存関係が適切か
```

### TypeScript/JavaScript

```
□ 型定義が適切か（anyを避ける）
□ nullish coalescingを使用しているか
□ async/awaitのエラーハンドリング
□ メモリリーク（イベントリスナー、タイマー）
□ 依存配列の漏れ（React hooks）
```

### Go

```
□ エラーハンドリングが適切か
□ goroutineリーク
□ deferの使い方
□ インターフェースの設計
□ コンテキストの伝播
```

## よくある問題パターン

### セキュリティ

```python
# ❌ SQLインジェクション
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ パラメータ化クエリ
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

```python
# ❌ パストラバーサル
file_path = f"/uploads/{filename}"

# ✅ パス検証
import os
safe_path = os.path.join("/uploads", os.path.basename(filename))
if not safe_path.startswith("/uploads/"):
    raise SecurityError("Invalid path")
```

### パフォーマンス

```python
# ❌ N+1クエリ
for user in users:
    orders = Order.objects.filter(user_id=user.id)  # N回クエリ

# ✅ 事前ロード
users = User.objects.prefetch_related('orders').all()
for user in users:
    orders = user.orders.all()  # キャッシュから取得
```

```python
# ❌ ループ内での文字列結合
result = ""
for item in items:
    result += str(item)  # O(n²)

# ✅ joinを使用
result = "".join(str(item) for item in items)  # O(n)
```

### 可読性

```python
# ❌ 複雑な条件
if user and user.is_active and user.role == "admin" and user.department in allowed_depts and not user.is_suspended:
    ...

# ✅ 意味のある関数に分割
def can_access_admin_panel(user):
    if not user or not user.is_active:
        return False
    if user.is_suspended:
        return False
    if user.role != "admin":
        return False
    return user.department in allowed_depts

if can_access_admin_panel(user):
    ...
```

## フィードバックの書き方

### 良いフィードバック

```
✅ 具体的で実行可能
「この関数は50行を超えています。process_order()とvalidate_order()に
分割すると、テストが書きやすくなりそうです。」

✅ 理由を説明
「ここでは`isinstance()`より`hasattr()`の方が適切かもしれません。
ダックタイピングを活用でき、テスト時のモック作成も容易になります。」

✅ 提案を含む
「エラーメッセージにuser_idを含めると、デバッグが楽になります：
`raise ValueError(f"Invalid user: {user_id}")`」
```

### 避けるべきフィードバック

```
❌ 曖昧
「このコードは良くない」

❌ 人格攻撃
「こんなコードを書くなんて...」

❌ 理由なし
「これはダメ」
```

### 重要度の明示

```
[must] セキュリティ上の問題があります。修正必須です。
[should] パフォーマンスが改善できます。対応推奨です。
[nit] 細かい指摘ですが、変数名をより明確にできます。
[question] この実装の意図を教えてください。
```

## 自動化ツール

### Python

```bash
# フォーマット
black .
isort .

# リンター
ruff check .
pylint src/

# 型チェック
mypy src/

# セキュリティ
bandit -r src/
```

### TypeScript

```bash
# フォーマット
prettier --write .

# リンター
eslint .

# 型チェック
tsc --noEmit
```

### Git hooks（pre-commit）

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
```
