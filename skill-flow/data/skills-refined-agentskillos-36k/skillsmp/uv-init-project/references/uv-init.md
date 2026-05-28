# uv プロジェクト初期化

`uv init` を使って Python プロジェクトを初期化する手順をまとめます。

## 事前確認

- uv コマンドが見つからない場合はユーザーに確認する。

## 1. 新規プロジェクトを作成する

初期化したいディレクトリに移動して以下のコマンドを実行する

```shell
uv init .
```

- `uv init . --python 3.14` のように、pythonのバージョンを指定することも可能

## 2. 生成物の確認

初期化が完了すると、`pyproject.toml` や `.python-version`、などがが作成されます。想定どおりのファイルが生成されているか確認してください。

## 3. pyproject.toml の初期設定

依存パッケージを追加するときにバージョンの上限を自動付与したいので`pyproject.toml` に次の設定を追記します。

```toml
[tool.uv]
add-bounds = "major"
```

## パッケージ管理方法をプロジェクトのAGENTS.mdに追記

`uv-manage-dependencies` スキルの `references/uv-manage-dependencies.md` の内容をプロジェクトのAGENTS.mdに追記する
