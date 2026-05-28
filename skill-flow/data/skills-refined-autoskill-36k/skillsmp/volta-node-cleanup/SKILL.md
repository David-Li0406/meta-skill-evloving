---
name: volta-node-cleanup
description: Volta で不要になった Node.js バージョンを手動で削除するときに使う。`volta uninstall node@<version>` が存在しないため、`~/.volta` 配下の実体を削除する作業を行う（macOS 前提）。
---

# Volta の古い Node.js を手動で削除する（macOS）

## 概要

Volta で管理している不要な Node.js バージョンを、`~/.volta` 配下の実体削除で掃除する手順をまとめる。

## 前提

- `volta uninstall node@<version>` というコマンドは存在しない。

## 削除手順

1. 現状を確認する。
```bash
volta list all
```

2. 削除バージョンを特定し、ユーザーに確認する。
   - 対象は `~/.volta` 配下の「ディレクトリ 1つ + ファイル 2つ」。
   - ディレクトリ: `tools/image/node/<version>`
   - ファイル: `tools/inventory/node/node-v<version>-darwin-*.tar.gz`
   - ファイル: `tools/inventory/node/node-v<version>-npm`

3. 削除を実行する。

```bash
rm -rf "$HOME/.volta/tools/image/node/<version>"
rm -f "$HOME/.volta/tools/inventory/node/node-v<version>-darwin-"*.tar.gz
rm -f "$HOME/.volta/tools/inventory/node/node-v<version>-npm"
```

4. 現状を確認する。
```bash
volta list all
```
