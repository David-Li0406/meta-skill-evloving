---
name: python-command-and-quality-check
description: Use this skill when you need to determine the appropriate Python command for your environment and perform quality checks on Python code.
---

# Python コマンド判別とコード品質チェック

このワークフローでは、現在の環境で使用すべき適切なPythonコマンドを判別し、Pythonコードの品質チェックを行います。

## Python コード品質チェック

Pythonファイルを編集した後、以下の手順を実行して品質チェックとレビューを行います：

### 1. フォーマット適用

```bash
uv run ruff format .
```

### 2. リンタ実行と自動修正

```bash
uv run ruff check --fix .
```

### 3. 残りのリンタエラー確認

```bash
uv run ruff check .
```

エラーがあれば手動で修正します。

### 4. コードレビュー

変更したコードを確認し、以下の観点でレビューします：

- **可読性**: 変数名・関数名は適切か
- **ロジック**: バグや edge case の見落としはないか
- **セキュリティ**: インジェクション等の脆弱性はないか
- **パフォーマンス**: 非効率な処理はないか
- **テスト**: テストが必要な変更か

問題があれば修正し、再度 1〜3 を実行します。

## Python コマンド判別・実行

現在の環境で使用すべき適切なPythonコマンドを判別し、スクリプトを実行します。プロジェクトの設定（pyproject.toml、.venv、uv）を確認し、最適な方法で実行します。

### 使用方法

#### 方法1: ラッパースクリプトで実行（推奨）

`run-python.sh` を使用して、Pythonスクリプトを直接実行します：

```bash
.skills/detect-python-command/scripts/run-python.sh script.py [args...]
```

#### 方法2: コマンドの確認のみ

使用されるPythonコマンドを確認したい場合：

```bash
.skills/detect-python-command/scripts/detect-python.sh
```

### 判別ロジック

以下の優先順位で判別します：

| 優先度 | 条件 | 使用するコマンド |
|--------|------|-----------------|
| 1 | `pyproject.toml` が存在 かつ `uv` がインストール済み | `uv run python` |
| 2 | `.venv/bin/python` が存在 | `.venv/bin/python` |
| 3 | `python` コマンドが存在 | `python` |
| 4 | `python3` コマンドが存在 | `python3` |
| 5 | いずれも該当しない | エラー終了 |

## コマンドリファレンス

| コマンド | 用途 |
|---------|------|
| `uv run ruff format .` | フォーマット適用 |
| `uv run ruff check .` | リンタ実行 |
| `uv run ruff check --fix .` | リンタ + 自動修正 |

## トラブルシューティング

### Pythonが見つからない

```
Error: No Python interpreter found
```

**解決方法**:
1. Python をインストール
2. または `uv sync` を実行して仮想環境を作成

### スクリプトが見つからない

```
Error: Script not found: script.py
```

**解決方法**:
1. スクリプトのパスが正しいか確認
2. 相対パスの場合、カレントディレクトリを確認

### uv が見つからない

uv がインストールされていない場合、フォールバックとして `.venv/bin/python` または システムの `python3` を使用します。

## 関連スキル

このスキルは以下のスキルから参照されます：

- `mixseek-config-validate` - 設定ファイルの検証