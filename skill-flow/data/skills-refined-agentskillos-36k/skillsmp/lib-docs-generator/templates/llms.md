# llms.txt形式テンプレート

llms.txtがないサイトからスキルを生成する際に、このテンプレートを参照して`llms.md`を生成する。

## テンプレート

```markdown
# [LIBRARY_NAME]

> [DESCRIPTION - ライブラリの概要を1-2文で]

## Getting Started

- [Installation](URL): インストール方法
- [Quick Start](URL): 基本的な使い方

## Core Concepts

- [PAGE_TITLE](URL): [SHORT_DESCRIPTION]

## API Reference

- [PAGE_TITLE](URL): [SHORT_DESCRIPTION]

## Guides

- [PAGE_TITLE](URL): [SHORT_DESCRIPTION]

## Examples

- [PAGE_TITLE](URL): [SHORT_DESCRIPTION]

## Optional

- [PAGE_TITLE](URL): [SHORT_DESCRIPTION]
```

## 記載ルール

### 必須項目

| セクション | 説明 |
|------------|------|
| Library名 | `# {Library}` 形式で記載 |
| Description | `> ` で始まる引用形式。1-2文で概要を説明 |
| Getting Started | インストール・セットアップ関連 |

### オプション項目

必要に応じてセクションを追加:

- **Core Concepts**: 基本概念・アーキテクチャ
- **API Reference**: 関数・コンポーネント・フック等
- **Guides**: ハウツーガイド
- **Examples**: サンプルコード
- **Optional**: 高度な設定・トラブルシューティング等

### リンク形式

```markdown
- [PAGE_TITLE](URL): SHORT_DESCRIPTION
```

- **PAGE_TITLE**: ページのタイトル（簡潔に）
- **URL**: 完全なURL
- **SHORT_DESCRIPTION**: 1文以内の説明（ページの最初の1-2文を抜粋）

## 例: Tamaguiの場合

```markdown
# Tamagui

> Universal UI components for React Native and Web. A styling library, design system, and optimizing compiler.

## Getting Started

- [Introduction](https://tamagui.dev/docs/intro/introduction): Overview of Tamagui's features and philosophy
- [Installation](https://tamagui.dev/docs/intro/installation): How to install Tamagui in your project

## Core Concepts

- [Configuration](https://tamagui.dev/docs/core/configuration): Setting up tamagui.config.ts
- [Styled](https://tamagui.dev/docs/core/styled): Creating styled components with createStyledContext

## Components

- [Stacks](https://tamagui.dev/docs/components/stacks): XStack, YStack, ZStack layout components
- [Button](https://tamagui.dev/docs/components/button): Accessible button component
- [Text](https://tamagui.dev/docs/components/text): Typography components

## Guides

- [Themes](https://tamagui.dev/docs/guides/themes): Creating and using themes
- [Animations](https://tamagui.dev/docs/guides/animations): Animation drivers and usage

## Optional

- [Compiler](https://tamagui.dev/docs/compiler/install): Static extraction and optimization
```

## 生成時の注意点

1. **URLは実際にアクセス可能なものを使用**
2. **SHORT_DESCRIPTIONはページから実際に抽出した内容を使う**
3. **セクション名は実際のドキュメント構造に合わせて調整可能**
4. **不要なセクションは省略してよい**
