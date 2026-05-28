---
name: nextjs-patterns
description: Next.js App Routerのベストプラクティス適用。Server Components, data fetching, server actionsに使用。
triggers:
  - Next.js
  - React
  - routing
  - components
  - server actions
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, mcp__playwright
version: 1.0
---

# Next.js Best Practices (App Router)

## 原則（仕様は既存コードから調査すること）

- Server Componentsをデフォルト、'use client'は必要な場合のみ
- データ取得はServer Component内でasync/await
- MutationsはServer Actions優先
- パフォーマンス: Suspense, revalidatePath, cache()

## 発動時のワークフロー

### 1. 調査（実装前に必ず実行）

```bash
# 既存構造の確認
find app -name "*.tsx" | head -20

# Client Componentの使用状況
grep -r "use client" app/ --include="*.tsx"

# 既存のUIコンポーネント
ls src/components/ui/

# package.jsonでバージョン確認
cat package.json | grep -E "next|react"
```

### 2. 実装

- 既存パターンに従う（調査結果を基に判断）
- 既存UIコンポーネントを再利用
- 変更は最小限に

### 3. 検証（必須）

```bash
# 静的解析
npm run type-check
npm run lint

# ビルド確認
npm run build

# 動作確認
npm run dev
```

### 4. ブラウザ検証（Playwright使用）

- 該当ページにアクセス
- コンソールエラーがないことを確認
- 意図した表示・動作を確認
- レスポンシブ確認（viewport切り替え）

## 報告形式

```
## Next.js実装レポート

### 調査結果
- 既存パターン: Server/Client比率、使用コンポーネント
- package.jsonバージョン: next@X.X.X

### 変更内容
- ファイル: 変更概要

### 検証結果
- type-check: OK/NG
- lint: OK/NG
- build: OK/NG
- ブラウザ確認: OK/NG（URL、確認項目）
```
