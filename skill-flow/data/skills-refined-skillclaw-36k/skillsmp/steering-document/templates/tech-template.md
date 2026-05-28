# tech.md テンプレート

技術スタック、アーキテクチャ、開発標準を定義する。

```markdown
# Technology Stack

## Architecture

[システムアーキテクチャの概要]
- モノリス/マイクロサービス/JAMstack など

## Core Technologies

### Primary Language(s)
- **Language**: [言語]
- **Runtime**: [ランタイム]
- **Framework**: [フレームワーク]

### Key Dependencies/Libraries

[主要ライブラリ一覧]

## Development Standards

### Type Safety
[型安全性に関する方針]
- TypeScript strict mode の使用状況
- 型定義の要求レベル

### Code Quality
[コード品質ツール]
- ESLint, Prettier, Biome などの設定状況

### Testing
[テスト戦略]
- テストフレームワーク
- カバレッジ要求

## Development Environment

### Required Tools
[必要なツールとバージョン]

### Common Commands
\`\`\`bash
# Dev: [開発サーバー起動コマンド]
# Build: [ビルドコマンド]
# Test: [テストコマンド]
\`\`\`

## Key Technical Decisions

[重要な技術的決定とその理由]

1. **[決定事項1]**:
   - **理由**: [理由]
   - **代替案**: [検討した代替案]
   - **トレードオフ**: [トレードオフ]
```

## 記載のポイント

- **Architecture**: 図を使わず文章で説明
- **Key Technical Decisions**: ADR（Architecture Decision Records）的な記録
- 具体的なコマンドは抽象化しすぎない（開発者が実行できるレベル）
