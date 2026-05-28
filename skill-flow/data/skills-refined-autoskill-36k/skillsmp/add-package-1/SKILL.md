---
name: add-package
description: |
  **[src/web専用]** フロントエンド（React/TypeScript）にnpmパッケージを追加する際に使用します。
  開発用と、プロダクト用途問わずこれを使います。shadcnはnpxのため本スキルでは扱いません。
---

# パッケージ追加スキル

このスキルは、pnpmを使ってプロジェクトにパッケージを追加する正しい方法を提供します。

## Instructions

1. まず、カレントディレクトリがsrc/webであることを確認します。
2. `pnpm add <package-name>` コマンドでパッケージを追加する
   - 通常の依存パッケージ: `pnpm add <package-name>`
   - 開発用依存パッケージ: `pnpm add -D <package-name>`
3. パッケージ追加後、`package.json` にパッケージが追加されていることを確認する
4. `pnpm-lock.yaml` が更新されていることを確認する

## 注意事項

⚠️ **package.jsonを直接編集しないでください**

パッケージを追加する際は、必ず `pnpm add` コマンドを使用してください。package.jsonを直接編集すると、pnpm-lock.yamlが更新されず、依存関係の整合性が失われます。
