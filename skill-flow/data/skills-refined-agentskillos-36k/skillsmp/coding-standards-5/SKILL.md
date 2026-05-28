---
name: coding-standards
description: "TypeScript/React/Next.jsのコーディング規約とベストプラクティス"
---

# Coding Standards Skill

## 概要

このSkillは、プロジェクトのコーディング規約を提供します。一貫性のある高品質なコードを維持し、チーム全体の開発効率を向上させることを目的とします。

## 基本原則

### 1. 可読性の重視
- コードは書くよりも読まれることが多い
- 明確で理解しやすいコードを書く
- 適切な命名と構造化を心がける

### 2. 一貫性の保持
- プロジェクト全体で統一されたスタイルを維持
- 既存のコードパターンに従う
- ツールによる自動化を活用

### 3. 保守性の向上
- 変更に強いコード設計
- 適切な分離と抽象化
- テスタブルなコード構造

## 詳細ドキュメント

各カテゴリの詳細な規約は以下を参照してください：

- [TypeScript規約](./reference/typescript-rules.md) - 型安全性、型定義、禁止事項
- [命名規則](./reference/naming-conventions.md) - 変数・関数・型の命名規則
- [禁止事項](./reference/prohibited-patterns.md) - 絶対に使用禁止のパターン

## クイックリファレンス

### 必須チェック項目

- [ ] **any型を使用していない**（最重要）
- [ ] 適切な型定義がされている
- [ ] 命名規約に従っている
- [ ] early return パターンを使用している
- [ ] エラーハンドリングが適切に実装されている
- [ ] 禁止事項に該当するコードがない

### インポート順序

```typescript
// 1. Node.js標準ライブラリ
import { readFile } from 'fs/promises';

// 2. 外部ライブラリ
import React from 'react';
import { NextRequest } from 'next/server';

// 3. 内部ライブラリ（@/から始まる）
import { Button } from '@/components/ui/button';
import { auth } from '@/lib/auth';

// 4. 相対インポート
import './styles.css';
import { localUtil } from '../utils';
```

### スタイリング（Panda CSS）

```typescript
// ✅ Panda CSS レシピの使用
import { button } from 'styled-system/recipes';

export function Button({ variant, size, children }: ButtonProps) {
  return (
    <button className={button({ variant, size })}>
      {children}
    </button>
  );
}

// ✅ css関数の使用
import { css } from 'styled-system/css';

const customStyles = css({
  padding: '1rem',
  backgroundColor: 'blue.500',
  _hover: {
    backgroundColor: 'blue.600'
  }
});
```

## ツール設定

### 必須ツール
1. **Biome**: linting と formatting
2. **TypeScript**: 型チェック
3. **Husky**: Git hooks
4. **lint-staged**: ステージングファイルのチェック

### VS Code 推奨設定

```json
{
  "editor.codeActionsOnSave": {
    "source.organizeImports": true,
    "source.fixAll": true
  },
  "editor.formatOnSave": true,
  "typescript.preferences.noSemicolons": false,
  "typescript.preferences.quoteStyle": "double"
}
```

## 関連Skill・ドキュメント

- [component-design](../einja-component-design/SKILL.md) - コンポーネント設計ガイドライン
- `docs/einja/steering/development/testing-strategy.md` - テスト戦略
- `docs/einja/steering/development/review-guidelines.md` - コードレビューガイドライン
- `docs/einja/steering/commit-rules.md` - コミットルール
