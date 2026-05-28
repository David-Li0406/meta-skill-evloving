# Ruffの運用

## プロジェクトのAGENTS.mdに追記

プロジェクトのAGENTS.mdに Ruff の使用方法がない場合は、以下の内容をそのプロジェクトのAGENTS.mdに追記する。

````markdown
## 3. 実行コマンド

### lint

```bash
# ソースを変更しない
ruff check .

# 変更内容を確認する
ruff check . --fix --diff

# ソースを変更する
ruff check . --fix
```

### format

```bash
# ソースを変更しない
ruff format . --check

# 変更内容を確認する
ruff format . --diff

# ソースを変更する
ruff format .
```

## 4. よく使う追加オプション

コミット前に一度実行してください。

### 未使用import / 未使用変数の削除

```bash
# 未使用 import と未使用変数を削除する
ruff check . --fix --unsafe-fixes --config "lint.fixable = ['F401', 'F841']"

# 未使用 import を削除する
ruff check . --fix --config "lint.fixable = ['F401']"

# 未使用変数を削除する（unsafe のため --unsafe-fixes が必要）
ruff check . --fix --unsafe-fixes --config "lint.fixable = ['F841']"
```
````

## 補足

- Ruff の実行方法はプロジェクトのパッケージ管理ツールに合わせて調整する。
- auto fix で治らないルール違反が出た場合は、`ruff rule F401` のようにしてルールの詳細を確認してから修正を開始する。
