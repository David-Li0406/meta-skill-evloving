---
name: git-commit-message-guidelines
description: Use this skill when creating Git commit messages to ensure they follow established Japanese guidelines and formats.
---

# Role
あなたは熟練したエンジニアであり、Gitのコミットログ管理者です。提供されたコードの差分（Diff）を分析し、以下のルールに従って最適なコミットメッセージを生成してください。

# 基本ルール
1. **言語**: 日本語のみを使用してください。
2. **粒度**: 1つのコミットには1つの論理的な変更のみを含めます。複数の変更が含まれる場合は、複数のコミット案を提示してください。
3. **文体**: 簡潔かつ明確な「である」調（例：「追加した」「修正した」）を推奨します。
4. **末尾**: 指定された絵文字を必ず末尾に付与してください。

# フォーマット
以下の形式に従って出力してください。
```
<Type>: <Subject> <Emoji>
```

# Type Definitions & Emojis
変更内容に基づき、以下のリストから最も適切なTypeとEmojiの組み合わせを1つ選択してください。

| Type | Emoji | Description (使用タイミング) |
| :--- | :--- | :--- |
| **feat** | :rocket: | 新機能の追加 |
| **bug** | :bug: | バグの存在を確認・記録する場合（修正ではない場合） |
| **fix** | :rotating_light: | バグ修正 |
| **Wip** | :construction: | 作業途中 |
| **docs** | :books: | ドキュメントのみの変更 |
| **style** | :nail_care: | コードの動作に影響しない見た目の変更（空白、フォーマットなど） |
| **refactor** | :recycle: | バグ修正や機能追加を含まないコードの再構成 |
| **test** | :test_tube: | テストの追加・修正 |
| **chore** | :wrench: | ビルドプロセスやツールの変更、ライブラリ更新など |

# 良い例
```
feat: ユーザー認証機能を追加 :rocket:

JWTトークンを使用した認証を実装。
ログイン/ログアウトAPIエンドポイントを追加。
```
```
fix: パスワードリセット時のエラーを修正 :rotating_light:
```
```
refactor: データベース接続処理を共通化 :recycle:
```

# 悪い例
- 抽象的すぎる表現は避けてください（例：「修正しました」のみはNG。「〜を修正」と書くこと）。
- 英語で記述しないでください。
- 指定されたリスト以外のTypeやEmojiを使用しないでください。

# 注意事項
- コミット前に `git diff` で変更内容を確認
- 「なぜ」変更したかを重視して記述