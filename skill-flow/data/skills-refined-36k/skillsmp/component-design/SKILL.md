---
name: component-design
description: "Reactコンポーネントの設計原則と実装ガイドライン"
---

# Component Design Skill

## 概要

このSkillは、プロジェクトにおけるReactコンポーネントの設計原則と実装ガイドラインを提供します。

## 基本原則

### 1. 単一責任の原則
- 各コンポーネントは単一の機能・責任を持つ
- 複数の機能が必要な場合は、複数のコンポーネントに分割する

### 2. 再利用可能性
- プロジェクト全体で再利用可能なコンポーネントを作成する
- プロパティ（props）による柔軟なカスタマイズを可能にする

### 3. 型安全性
- TypeScriptの型定義を必須とする
- プロパティ、状態、イベントハンドラーは全て型定義する

### 4. Co-location（共存配置）
- 機能固有のコンポーネントは関連するページの近くに配置する
- `_components` ディレクトリを使用してページ固有のコンポーネントを管理する
- 複数のページで共有されるコンポーネントのみ `src/components/` に配置する

## 詳細ドキュメント

各カテゴリの詳細な規約は以下を参照してください：

- [ディレクトリ構造](./reference/directory-structure.md) - ファイル配置とディレクトリ設計
- [Props設計パターン](./reference/props-patterns.md) - Props設計とイベントハンドリング
- [スタイリングガイド](./reference/styling-guide.md) - Panda CSSを使用したスタイリング規約

## クイックリファレンス

### ディレクトリ構造

```
src/
├── components/
│   ├── ui/                 # 基本的なUIコンポーネント
│   │   ├── Button/
│   │   ├── Input/
│   │   └── ...
│   └── shared/             # 共通コンポーネント（レイアウト含む）
│       ├── Header/
│       ├── Footer/
│       └── ...
└── app/
    ├── dashboard/
    │   ├── page.tsx
    │   └── _components/    # ページ固有のコンポーネント
    │       ├── DashboardChart/
    │       └── StatsCard/
    └── ...
```

### コンポーネント命名規則

- **ファイル名**: PascalCase（例: `Button.tsx`, `UserProfile.tsx`）
- **例外**: shadcn/uiコンポーネントはkebab-case（例: `button.tsx`）

### コンポーネントディレクトリ構造

```
ComponentName/
├── index.tsx           # コンポーネント本体
└── styles.ts          # Panda CSS スタイル定義（必要に応じて）
```

### 基本的な型定義

```typescript
interface ButtonProps {
  children: React.ReactNode;
  variant?: "primary" | "secondary" | "danger";
  size?: "sm" | "md" | "lg";
  disabled?: boolean;
  onClick?: () => void;
}
```

## チェックリスト

新しいコンポーネントを作成する際の確認事項：

- [ ] 適切なディレクトリに配置されている
- [ ] TypeScript の型定義が完全
- [ ] Panda CSS でスタイリングされている
- [ ] プロパティのデフォルト値が設定されている
- [ ] アクセシビリティが考慮されている
- [ ] 単体テストが実装されている

## 関連Skill・ドキュメント

- [coding-standards](../einja-coding-standards/SKILL.md) - コーディング規約
- `docs/einja/steering/development/testing-strategy.md` - テスト戦略
- `docs/einja/steering/development/frontend-development.md` - フロントエンド開発ガイド

## 参考資料

- [React 公式ドキュメント](https://react.dev)
- [TypeScript 公式ドキュメント](https://www.typescriptlang.org)
- [Panda CSS ドキュメント](https://panda-css.com)
