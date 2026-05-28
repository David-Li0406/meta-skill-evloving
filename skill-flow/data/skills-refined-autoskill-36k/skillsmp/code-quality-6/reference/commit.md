# コミットメッセージ規約

## 目次
- Conventional Commits
- コミットメッセージの構造
- タイプ一覧
- 良い例・悪い例
- 自動生成

## Conventional Commits

### 基本形式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 例

```
feat(auth): JWT認証を実装

- ログインエンドポイントを追加
- トークン検証ミドルウェアを実装
- リフレッシュトークン機能を追加

Closes #123
```

## タイプ一覧

| タイプ | 説明 | 例 |
|--------|------|-----|
| feat | 新機能 | 新しいAPI追加 |
| fix | バグ修正 | NPE修正 |
| docs | ドキュメント | README更新 |
| style | フォーマット | インデント修正 |
| refactor | リファクタリング | 関数分割 |
| perf | パフォーマンス改善 | クエリ最適化 |
| test | テスト | ユニットテスト追加 |
| chore | ビルド・ツール | 依存関係更新 |
| ci | CI設定 | GitHub Actions修正 |

## スコープ

プロジェクトに応じて定義：

```
auth     - 認証関連
api      - API関連
db       - データベース
ui       - ユーザーインターフェース
config   - 設定
deps     - 依存関係
```

## サブジェクト

### ルール

- 命令形で書く（「追加した」ではなく「追加」）
- 最初の文字は小文字（英語の場合）
- 末尾にピリオドを付けない
- 50文字以内

### 良い例

```
feat(api): ユーザー検索エンドポイントを追加
fix(auth): トークン有効期限の計算を修正
refactor(db): クエリビルダーを共通化
```

### 悪い例

```
❌ fix: バグを修正。          # ピリオド不要、内容が曖昧
❌ Fixed the bug             # 過去形、小文字で始めるべき
❌ feat: 色々な機能を追加     # 複数の変更を1コミットに
```

## ボディ

変更の理由や詳細を説明：

```
fix(payment): 決済処理のタイムアウトを修正

外部決済APIのレスポンスが遅い場合にタイムアウトエラーが
発生していた問題を修正。

- タイムアウト値を30秒から60秒に延長
- リトライ処理を追加（最大3回）
- エラー時のログ出力を改善
```

## フッター

### Breaking Changes

```
feat(api): レスポンス形式をJSONに統一

BREAKING CHANGE: XML形式のレスポンスは廃止されました。
すべてのエンドポイントがJSON形式で応答します。
```

### Issue参照

```
fix(auth): ログインエラーメッセージを改善

Fixes #456
Closes #789
Refs #123
```

## 自動生成スクリプト

```python
#!/usr/bin/env python3
"""
git diffからコミットメッセージを生成する

使用方法:
    git diff --staged | python generate_commit.py
"""

import sys
from anthropic import Anthropic

def generate_commit_message(diff: str) -> str:
    client = Anthropic()
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f"""以下のgit diffからConventional Commits形式のコミットメッセージを生成してください。

形式:
<type>(<scope>): <subject>

<body>

タイプ: feat, fix, docs, style, refactor, perf, test, chore, ci
スコープ: 変更対象のモジュール/機能
サブジェクト: 50文字以内、命令形
ボディ: 変更内容の詳細（箇条書き可）

diff:
```
{diff[:3000]}
```

コミットメッセージのみを出力してください。"""
        }]
    )
    
    return response.content[0].text.strip()

if __name__ == "__main__":
    diff = sys.stdin.read()
    if not diff.strip():
        print("Usage: git diff --staged | python generate_commit.py")
        sys.exit(1)
    
    message = generate_commit_message(diff)
    print(message)
```

## コミット分割のガイドライン

### 1コミット = 1つの論理的変更

```bash
# ❌ 悪い例: 複数の変更を1コミットに
git commit -m "fix: バグ修正とリファクタリングと新機能追加"

# ✅ 良い例: 分割してコミット
git add src/auth.py
git commit -m "fix(auth): トークン検証のバグを修正"

git add src/utils.py
git commit -m "refactor(utils): ヘルパー関数を共通化"

git add src/api.py tests/test_api.py
git commit -m "feat(api): 新しいエンドポイントを追加"
```

### インタラクティブリベース

```bash
# 直近3コミットを整理
git rebase -i HEAD~3

# エディタで操作を選択
pick abc1234 feat: 機能A
squash def5678 fix: 機能Aの修正  # 前のコミットに統合
reword ghi9012 docs: ドキュメント  # メッセージ変更
```
