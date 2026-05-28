---
name: add-package
description: |
  **[src/api専用]** バックエンド（Python/FastAPI）にパッケージを追加する際に使用します。
  開発用と、プロダクト用途問わずこれを使います。
---

# パッケージ追加スキル

このスキルは、uvを使ってプロジェクトにパッケージを追加する正しい方法を提供します。

## Instructions

1. まず、カレントディレクトリがsrc/apiであることを確認します。
2. `uv add <package-name>` コマンドでパッケージを追加する
   - 通常の依存パッケージ: `uv add <package-name>`
   - 開発用依存パッケージ: `uv add -D <package-name>`
3. パッケージ追加後、`pyproject.toml` にパッケージが追加されていることを確認する
4. `uv.lock` が更新されていることを確認する

## 注意事項

⚠️ **pyproject.tomlを直接編集しないでください**

パッケージを追加する際は、必ず `uv add` コマンドを使用してください。pyproject.tomlを直接編集すると、uv.lockが更新されず、依存関係の整合性が失われます。
