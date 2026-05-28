# structure.md テンプレート

プロジェクト構造、命名規則、コード組織原則を定義する。

```markdown
# Project Structure

## Directory Organization

\`\`\`
[プロジェクト名]/
├── [ディレクトリ構造]
├── specs/
│   └── _steering/          # ステアリングドキュメント
└── ...
\`\`\`

**組織化の原則**:
- **[原則1]**: [説明]
- **[原則2]**: [説明]

## Naming Conventions

### ファイル名
- **[パターン1]**: [説明]（例: kebab-case.ts）
- **[パターン2]**: [説明]（例: PascalCase.tsx）

### ディレクトリ名
- **[パターン]**: [説明]

## Code Organization Principles

1. **単一責任**: [プロジェクト固有の適用方法]
2. **モジュール性**: [モジュール分割の基準]
3. **再利用性**: [共通コンポーネントの配置]

## Module Boundaries

[モジュール間の境界定義]

## File Size Guidelines

- **推奨サイズ**: [行数]
- **最大サイズ**: [行数]

## Documentation Standards

### プロジェクトレベル
- **README.md**: [役割]

### コードレベル
- **コメント**: [コメント規約]
- **型定義**: [型定義の要求]
```

## 記載のポイント

- **Directory Organization**: 実際のディレクトリ構造を反映
- **Naming Conventions**: 一貫性を保つためのルール
- **Module Boundaries**: 循環参照を防ぐための境界定義
