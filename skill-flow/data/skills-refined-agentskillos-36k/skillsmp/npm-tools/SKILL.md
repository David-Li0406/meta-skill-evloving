---
name: npm-tools
description: NPM tools and package management using mise including commitizen, cz-git, and global package configuration
---

# npm tools

[Install npm tools](#install-npm-tools)

## Create directory for global npm packages

```sh
mkdir -p ~/.npm-global
npm config set prefix ~/.npm-global
```

## Install npm tools

### 方法1: mise タスクを使用（推奨）

```sh
# commitizen + cz-git をグローバルにインストール
make mise-install-npm-commitizen

# または直接 mise を使用
mise run npm-commitizen

# mise で管理している全ツールをインストール
make mise-install-all
```

### 方法2: 従来のnpmコマンド

```sh
# 非推奨: 代わりに上記の mise タスクを使用
make npm-tools
```

## mise で管理されているツール

### ツール一覧の確認

```sh
# インストールされているツール一覧
make mise-list

# mise の設定確認
make mise-config
```

### 管理対象ツール

- **Node.js**: `lts`
- **Go**: `1.23.4`
- **NPMパッケージ（mise管理）**:
  - `@redocly/cli`
  - `corepack`
  - `@anthropic-ai/claude-code`
  - `@google/gemini-cli`
- **NPMパッケージ（グローバルインストール）**:
  - `commitizen`
  - `cz-git`

## commitizen & cz-git

### Usage

```sh
git cz
```

または

```sh
cz
```
