---
name: project-guidelines
description: |
  このスキルは、ユーザーが「プロジェクト設定」「ガイドライン」「テンプレート」「プロジェクト固有」について質問したとき、またはプロジェクト固有の設定を管理する必要があるときに使用する。
---

# Project Guidelines

## プロジェクト設定ファイル

### .claude/dev-core.local.md

プロジェクト固有の設定を管理するファイル：

```markdown
---
package-manager: pnpm
test-command: pnpm test
lint-command: pnpm lint
build-command: pnpm build
typecheck-command: pnpm typecheck
---

# プロジェクト固有の設定

## 技術スタック

- Framework: Next.js 14 (App Router)
- UI: shadcn/ui + Tailwind CSS
- State: Zustand
- Form: react-hook-form + zod
- Database: PostgreSQL + Prisma
- Auth: Auth.js

## ディレクトリ構造

FSD (Feature-Sliced Design) を採用：

\`\`\`
src/
├── app/       # Next.js App Router
├── widgets/   # ページ構成要素
├── features/  # ユーザー向け機能
├── entities/  # ビジネスエンティティ
└── shared/    # 共通コンポーネント
\`\`\`

## コーディング規約

- ハードコーディング禁止
- useEffect の使用制限
- TypeScript strict mode
```

## プロジェクトテンプレート

### Next.js + FSD

```
project/
├── .claude/
│   └── dev-core.local.md
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── widgets/
│   ├── features/
│   │   └── auth/
│   │       ├── api/
│   │       ├── model/
│   │       ├── ui/
│   │       └── index.ts
│   ├── entities/
│   │   └── user/
│   │       ├── model/
│   │       ├── ui/
│   │       └── index.ts
│   └── shared/
│       ├── ui/
│       ├── lib/
│       └── config/
├── prisma/
│   └── schema.prisma
└── package.json
```

## 環境変数テンプレート

### .env.example

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/db

# Auth
AUTH_SECRET=your_auth_secret

# API
NEXT_PUBLIC_API_URL=http://localhost:3000/api
```

## CI/CD 設定

### GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "pnpm"
      - run: pnpm install
      - run: pnpm typecheck
      - run: pnpm lint
      - run: pnpm test
```

## 推奨パッケージ

### 必須

- `typescript`: 型安全性
- `eslint`: コード品質
- `prettier`: フォーマット
- `vitest` / `jest`: テスト

### 推奨

- `zod`: スキーマバリデーション
- `react-hook-form`: フォーム管理
- `zustand`: 状態管理
- `prisma`: ORM

## ドキュメント構造

```
docs/
├── plans/           # 実装計画
│   └── issue-123.md
├── api/             # API ドキュメント
│   └── users.md
└── architecture/    # アーキテクチャ決定
    └── adr-001.md
```
