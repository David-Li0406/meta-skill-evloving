# Ruffのセットアップ

## Ruffのインストール

開発用の依存に Ruff をインストールします。

```shell
# 例)
uv add --group dev ruff
```

## 設定

Python プロジェクトのルート（通常は `pyproject.toml` がある場所）に `ruff.toml` を配置します。設定内容は `assets/ruff.toml` をコピーし、必要に応じて調整してください。

## Git管理対象外ディレクトリの設定

Ruff を実行すると `.ruff_cache` ディレクトリが作成されるため、プロジェクトの `.gitignore` に `**/.ruff_cache/` を追記する。
