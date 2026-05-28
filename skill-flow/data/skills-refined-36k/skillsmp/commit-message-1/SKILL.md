---
name: commit-message
description: "コミットメッセージ作成スキル。Conventional Commits形式の日本語メッセージを作成。Use when: コミット作成、変更内容のコミット、git commitを依頼された時。"
---

# コミットメッセージ作成

Conventional Commits形式の**日本語メッセージ**でコミットを作成します。

## コミットメッセージ形式

```
<type>: <subject>

<body>

<footer>
```

## メッセージ構成要素

| 要素    | 必須/任意 | 説明                          |
| ------- | --------- | ----------------------------- |
| type    | 必須      | 変更の種類（英語）            |
| subject | 必須      | 変更の要約（日本語）          |
| body    | 任意      | 変更の詳細説明（日本語）      |
| footer  | 任意      | Issue参照、破壊的変更（英語） |
| 署名    | 必須      | Claude Code生成署名           |

## Type一覧

| Type       | 用途                                                         |
| ---------- | ------------------------------------------------------------ |
| `feat`     | 新機能の追加                                                 |
| `fix`      | バグ修正                                                     |
| `docs`     | ドキュメントのみの変更                                       |
| `style`    | コードの動作に影響しない変更（フォーマット、セミコロンなど） |
| `refactor` | バグ修正や機能追加ではないコード変更                         |
| `perf`     | パフォーマンス改善                                           |
| `test`     | テストの追加や修正                                           |
| `chore`    | ビルドプロセスやツールの変更                                 |

## 記述ルール

### Subject（必須）

- **日本語で記述**
- 50文字以内
- 命令形で記述（例: "追加する" ではなく "追加"）
- 最初の文字は小文字
- 末尾にピリオドや句点を付けない

### Body（任意）

- **日本語で記述**
- 変更の理由や方法を説明
- 72文字で折り返す
- 複数行に分けて詳細を記述可能
- 箇条書きで主な変更内容を列挙

### Footer（任意）

- Issue番号を参照する場合: `Closes #123`
- 破壊的変更がある場合: `BREAKING CHANGE:` を記載（日本語で説明）

### Claude Code署名（必須）

全てのコミットメッセージの末尾に以下を追加:

```
🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## コミットメッセージ例

### 例1: 新機能追加

```
feat: Docker Composeとuvによる開発環境をセットアップ

FastAPI + MetaTrader5プロジェクトのDocker ComposeとuvベースのPython開発環境を構築。

主な変更内容:
- pyproject.toml でプロジェクト依存関係と設定を定義
- Python 3.11とuvを含むDockerfileを作成
- docker-compose.yml でサービスオーケストレーションを設定
- app/ディレクトリにFastAPIアプリケーション構造を作成
- tests/ディレクトリにテスト構造を作成
- .env.example で環境変数の設定例を提供
- AGENTS.md に包括的なプロジェクトドキュメントを記載

MetaTrader5パッケージはWindows専用のため、オプショナル依存関係(mt5)として設定。
macOS/Linuxでの開発はMT5なしでサポートし、完全なMT5統合はWindows Dockerコンテナでテスト可能。

Closes #1

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### 例2: バグ修正

```
fix: 認証トークンの有効期限チェックを修正

トークンの有効期限が切れた後も認証が通ってしまう問題を修正。
有効期限のチェックロジックを改善し、適切にエラーを返すようにした。

Closes #456

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### 例3: ドキュメント更新

```
docs: READMEにセットアップ手順を追加

初めて利用するユーザー向けに、より詳細なセットアップ手順をREADMEに追加。
環境変数の設定方法とトラブルシューティングのセクションを含む。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### 例4: リファクタリング

```
refactor: 認証ロジックを独立したモジュールに分離

認証関連のコードを app/auth.py に分離し、コードの可読性と保守性を向上。
既存の機能には影響なし。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

## コミット作成手順

1. **変更内容の分析**: `git status` と `git diff` で変更内容を確認
2. **Type選択**: 変更の性質に応じて適切なtypeを選択
3. **Subject作成**: 変更内容を簡潔に日本語で要約
4. **Body作成**: 詳細な変更内容を箇条書きで記述
5. **Footer追加**: Issue番号や破壊的変更を記載
6. **署名追加**: Claude Code署名を追加
7. **コミット実行**: HEREDOCを使用してコミット

## コミットコマンド形式

```bash
git commit -m "$(cat <<'EOF'
feat: 機能の要約

詳細な説明をここに記述します。
複数行にわたって説明できます。

主な変更内容:
- 変更1
- 変更2
- 変更3

Closes #123

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

## 重要な注意事項

1. **日本語メッセージ**: typeは英語、subject/bodyは日本語で記述
2. **簡潔なsubject**: 50文字以内で変更内容を要約
3. **詳細なbody**: 必要に応じて変更の理由と方法を説明
4. **Issue参照**: 関連するIssue番号は必ず記載
5. **HEREDOC使用**: コミットメッセージの整形にHEREDOCを使用
6. **署名必須**: 全てのコミットにClaude Code署名を追加
