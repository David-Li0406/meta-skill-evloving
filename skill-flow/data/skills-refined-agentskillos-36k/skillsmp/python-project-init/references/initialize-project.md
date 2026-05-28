# Python プロジェクト初期化

## 目的

uv を使って Python プロジェクトのひな型を作成し、Ruff を導入してコードスタイルと静的解析を一括管理できる状態にする。

## 前提条件

- Python と uv がインストール済みであること。uv のコマンドが見つからない場合は、ユーザーに確認する。
- プロジェクト用の Git リポジトリを初期化済みであること、または初期化する権限があること。

## 手順

### 1. uv でプロジェクトを初期化する

- `uv-init-project` スキルの `references/uv-init.md` を参照し、`uv init` の実行から生成物の確認、`add-bounds` など初期設定の反映までを完了させる。

### 2. Ruff を開発依存に追加して設定する

- `ruff-setup` スキルの `references/ruff-setup.md` を参照し、Ruff のインストールと `ruff.toml` の設定を行う。
- docstring は Google スタイルで書く旨を、プロジェクトの AGENTS.md に追記する。

### 3. 初期フォーマットと静的解析を確認する

- Ruff の初回実行手順と検証ポイントは `ruff-operations` スキルの `references/ruff-operations.md` を参照する。

### 4. 初期コミットを作成する

- Git 運用に関するチームルールに従って初期コミットを作成する。規約が未整備の場合はプロジェクトの `AGENTS.md` に従う。

## 参考ドキュメント

- `uv-init-project` スキルの `references/uv-init.md`: uv の初期化コマンドとオプションの詳細
- `ruff-setup` スキルの `references/ruff-setup.md`: Ruff の導入手順と推奨設定
- `uv-manage-dependencies` スキルの `references/uv-manage-dependencies.md`: `uv add` 以外の依存関係管理コマンド
