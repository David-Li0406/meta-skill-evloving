---
name: git-commit
description: "適切な粒度でコミット作成スキル。変更内容を機能・目的ごとに分割し、複数の小さなコミットを作成。Use when: コミット作成、変更のコミット、適切な粒度でのコミットを依頼された時。"
---

# 適切な粒度でのコミット作成

変更内容を分析し、機能や目的ごとに適切な粒度で分割して複数のコミットを作成します。各コミットはConventional Commits形式の日本語メッセージで作成されます。

## コミット粒度の原則

### 良いコミット粒度の特徴

| 特徴         | 説明                                     |
| ------------ | ---------------------------------------- |
| 単一目的     | 1つのコミットは1つの目的を持つ           |
| 機能的独立性 | 独立してレビュー・revert可能             |
| テスト可能   | コミット時点でテストが通る               |
| 適切なサイズ | 通常は数十～数百行程度                   |
| 自己完結     | コミットメッセージで変更内容が理解できる |

### 避けるべきコミット

| タイプ         | 問題点                               |
| -------------- | ------------------------------------ |
| 巨大コミット   | レビューが困難、問題特定が難しい     |
| 混合コミット   | 複数の無関係な変更が含まれる         |
| 不完全コミット | テストが失敗する、ビルドエラーがある |
| 曖昧コミット   | 何をしたのか不明確                   |

## コミット分割の判断基準

### 分割すべき変更

以下の異なる種類の変更は**別々のコミット**に分割します：

1. **機能追加** vs **バグ修正** vs **リファクタリング**
2. **ドキュメント** vs **実装コード**
3. **テストコード** vs **プロダクションコード**（機能が複雑な場合）
4. **設定ファイル** vs **アプリケーションコード**
5. **異なる機能・モジュール**の変更
6. **依存関係追加** vs **コード変更**

### まとめて良い変更

以下は**同じコミット**にまとめます：

1. **関連するテストとコード**（単純な機能の場合）
2. **同じ機能の関連ファイル**（モデル、ビュー、コントローラーなど）
3. **同時に必要な変更**（APIとそのクライアント）
4. **型定義とその使用箇所**
5. **リネームとその参照更新**

## コミット作成手順

### 1. 変更内容の分析

```bash
# 現在の変更を確認
git status

# 詳細な差分を確認
git diff

# ステージングされた変更を確認
git diff --cached
```

### 2. セルフレビュー（ブランチ差分チェック）

**コミット前の必須プロセス**として、変更内容を客観的に確認します。

```bash
# self-review スキルを使用
"コミット前にセルフレビューをお願いします"
```

詳細な手順とチェックリストは [self-review/SKILL.md](../self-review/SKILL.md) を参照してください。

### 3. 変更の分類

変更されたファイルを以下のカテゴリに分類：

- **機能追加**: 新しい機能の実装
- **バグ修正**: 既存の不具合修正
- **リファクタリング**: 動作を変えない改善
- **ドキュメント**: READMEやコメントの更新
- **テスト**: テストコードの追加・修正
- **設定**: 設定ファイル、環境変数の変更
- **依存関係**: ライブラリの追加・更新

### 4. コミット順序の決定

以下の順序でコミットを作成すると理解しやすい：

1. **基盤・設定**: 依存関係追加、設定ファイル変更
2. **リファクタリング**: コード構造の改善
3. **バグ修正**: 既存の問題修正
4. **機能追加**: 新機能の実装
5. **テスト追加**: 新しいテストの追加
6. **ドキュメント**: 説明文書の更新

### 5. 部分的なステージングとコミット

```bash
# ファイル単位でステージング
git add path/to/file1.py path/to/file2.py

# ファイルの一部をインタラクティブにステージング
git add -p path/to/file.py

# コミット実行
git commit -m "$(cat <<'EOF'
feat: 機能の要約

詳細な説明...

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

## コミットメッセージ形式

各コミットは**commit-message**スキルの形式に従います：

```
<type>: <subject>

<body>

<footer>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

詳細は [commit-message/SKILL.md](../commit-message/SKILL.md) を参照。

## 実践例

### 例1: 複数の独立した変更を分割

**変更内容**:

- Docker環境の構築（Dockerfile, docker-compose.yml）
- FastAPIアプリケーションの実装（app/main.py）
- テストコードの追加（tests/test_api.py）
- ドキュメントの作成（README.md）

**コミット分割**:

```bash
# コミット1: Docker環境構築
git add Dockerfile docker-compose.yml .dockerignore
git commit -m "$(cat <<'EOF'
chore: Docker Composeによる開発環境をセットアップ

FastAPIアプリケーション用のDocker環境を構築。

主な変更内容:
- Python 3.11ベースのDockerfileを作成
- docker-compose.ymlでサービスを定義
- ホットリロード対応のボリュームマウント設定

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"

# コミット2: FastAPIアプリケーション実装
git add app/main.py app/__init__.py requirements.txt
git commit -m "$(cat <<'EOF'
feat: FastAPIで基本的なAPIエンドポイントを実装

ヘルスチェックとユーザー管理の基本APIを追加。

主な変更内容:
- FastAPIアプリケーションの初期化
- /health エンドポイントの実装
- /users エンドポイントの実装
- 必要なパッケージをrequirements.txtに追加

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"

# コミット3: テストコード追加
git add tests/test_api.py tests/__init__.py
git commit -m "$(cat <<'EOF'
test: APIエンドポイントのテストを追加

FastAPIアプリケーションの主要なエンドポイントに対するテストを実装。

主な変更内容:
- ヘルスチェックエンドポイントのテスト
- ユーザー管理APIのテスト
- pytestのフィクスチャ設定

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"

# コミット4: ドキュメント作成
git add README.md
git commit -m "$(cat <<'EOF'
docs: セットアップ手順とAPI仕様をREADMEに追加

開発環境のセットアップ方法とAPIの使用方法を文書化。

主な変更内容:
- Docker環境のセットアップ手順
- API エンドポイントの説明
- 開発ワークフローのガイド

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

### 例2: バグ修正と関連するテスト

**変更内容**:

- 認証ロジックのバグ修正（auth.py）
- 既存テストの修正（test_auth.py）

**コミット分割**:

```bash
# 1つのコミットにまとめる（バグ修正とそのテストは密接に関連）
git add app/auth.py tests/test_auth.py
git commit -m "$(cat <<'EOF'
fix: 認証トークンの有効期限チェックを修正

トークンの有効期限が切れた後も認証が通ってしまう問題を修正。
有効期限のチェックロジックを改善し、適切にエラーを返すようにした。

主な変更内容:
- トークン検証ロジックの修正（auth.py）
- 有効期限切れトークンのテストケース追加（test_auth.py）

Closes #45

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

### 例3: リファクタリングと機能追加を分離

**変更内容**:

- 既存コードのリファクタリング
- 新機能の追加

**コミット分割**:

```bash
# コミット1: リファクタリング（まず既存コードを改善）
git add app/services/user_service.py
git commit -m "$(cat <<'EOF'
refactor: ユーザーサービスのコードを整理

ユーザー管理ロジックを複数のメソッドに分割し、可読性を向上。
既存の機能には影響なし。

主な変更内容:
- create_user メソッドをヘルパーメソッドに分割
- バリデーションロジックを独立した関数に抽出
- エラーハンドリングを統一

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"

# コミット2: 新機能追加（リファクタリング後の綺麗なコードに追加）
git add app/services/user_service.py app/routes/user_routes.py tests/test_user_service.py
git commit -m "$(cat <<'EOF'
feat: ユーザープロフィール画像のアップロード機能を追加

ユーザーがプロフィール画像をアップロードできる機能を実装。

主な変更内容:
- 画像アップロードエンドポイントの実装
- 画像ファイルのバリデーション
- ストレージへの保存処理
- 画像アップロードのテスト追加

Closes #56

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

## 各コミットでのテスト実行

各コミット作成後、テストが通ることを確認：

```bash
# テスト実行
npm test  # または pytest, cargo test など

# ビルド確認
npm run build  # または必要に応じて

# リンター実行
npm run lint  # または必要に応じて
```

エラーが発生した場合は、コミットを修正（amend）するか、追加の修正コミットを作成します。

## コミット粒度のチェックリスト

各コミット作成前に以下を確認：

- [ ] コミットは単一の目的を持っているか？
- [ ] 他のコミットと独立してレビューできるか？
- [ ] コミット時点でテストが通るか？
- [ ] 差分サイズは適切か（通常は数十～数百行）？
- [ ] コミットメッセージで変更内容が明確に理解できるか？
- [ ] 無関係な変更が混ざっていないか？
- [ ] このコミットだけでrevertしても問題ないか？

## 重要な注意事項

1. **テスト可能性**: 各コミットは単独でテストが通る状態を保つ
2. **段階的な変更**: 大きな変更は複数の小さなコミットに分割
3. **レビュー容易性**: レビュアーが理解しやすい粒度を心がける
4. **履歴の明確性**: git logやgit blameで変更理由が追跡できるようにする
5. **安全なrevert**: 問題があった場合に特定のコミットだけrevertできるようにする
6. **commit-message形式**: 全てのコミットでConventional Commits形式を使用
