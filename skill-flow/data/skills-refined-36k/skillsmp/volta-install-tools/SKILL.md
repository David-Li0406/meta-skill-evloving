---
name: volta-install-tools
description: Volta で Node.js / npm のバージョンを追加・切替し、npm のグローバル CLI をインストールするときに使う。例 `volta install node@lts`、`volta install @google/gemini-cli` など。
---

# Volta で Node/npm とグローバル CLI を追加する

## 概要

Node.js / npm のバージョン追加や切替、npm のグローバル CLI の導入を Volta 経由で行うための手順をまとめる。

## 手順

1. 現状を確認する。

```bash
volta list all
```

2. 追加するバージョンとツールを特定し、ユーザーに確認する。

3. インストールを実行する。

```bash
volta install node@lts
volta install node@<version>
volta install <package>
volta install @google/gemini-cli
```

4. 追加後の状態を確認する。

```bash
volta list all
```
