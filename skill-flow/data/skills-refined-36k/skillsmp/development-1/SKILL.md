---
name: development
description: Set up the development environment, understand code conventions, and implement type-safe patterns. Use when starting development work, writing new components, or following project-specific coding guidelines.
metadata:
  author: Bingify
  version: "1.0"
---

# Development Setup & Code Conventions

このスキルは、Bingifyプロジェクトの開発環境構築とコード規約をカバーします。

## 概要

BingifyはNext.js+AppRouter、Tailwind CSS、shadcn/ui、Supabaseを使用したプロジェクトです。エージェントが効率的に開発できるよう、プロジェクト固有のルールと実装パターンを提供します。

## セットアップ手順

### リポジトリのクローン

```bash
git clone https://github.com/ykzts/bingify.git
cd bingify
```

### 環境構築

```bash
pnpm install          # パッケージのインストール
pnpm local:setup      # Supabaseとデータベース初期化
pnpm dev              # 開発サーバー起動
```

Supabaseへのアクセス情報や設定詳細は [supabase-setup スキル](../supabase-setup/SKILL.md) を参照してください。

## コード規約

### TypeScript & Next.js

- **Next.js 型安全な Props**：
  - レイアウトコンポーネントには `LayoutProps<Route>` を使用
  - ページコンポーネントには `PageProps<Route>` を使用
  - これらの型は `pnpm typegen` で自動生成（`.next/types/routes.d.ts`）
  - `params` と `searchParams` は `Promise` として扱い、`await` で解決

### UIコンポーネント

- shadcn/uiコンポーネントは `@/components/ui` に配置 (自動生成、手動編集禁止)
- カスタムコンポーネントは `@/components` に配置
- `cn` ユーティリティ (`lib/utils.ts`) でクラス結合

**shadcn/ui 管理**:

```bash
# 新規追加
pnpm dlx shadcn@latest add <component-name>

# 既存コンポーネントの更新（上書き）
pnpm dlx shadcn@latest add --yes --overwrite <component-name>
```

### スタイリング

Tailwind CSSを使用 (CSS-first)：

- デザイントークンは `messages/` から参照
- Theme Color: Purple (Primary: `#a78bfa`)
- Icons: Lucide React
- メインアクションボタンには `primary` バリアント（デフォルト）を使用

```tsx
import { cn } from "@/lib/utils";

export function Button({ variant, className, ...props }) {
  return (
    <button
      className={cn(
        "px-4 py-2 rounded-lg font-medium",
        variant === "primary" && "bg-purple-500 text-white",
        className,
      )}
      {...props}
    />
  );
}
```

### 型安全性

Zodスキーマから型推論：

```tsx
import { z } from "zod";

const userSchema = z.object({
  id: z.string(),
  email: z.string().email(),
});

type User = z.infer<typeof userSchema>;
```

### バリデーション・フォーム処理

TanStack Form + Server Actions + Zod：

- `formOptions` で共有フォームオプション定義
- `createServerValidate` でサーバー側バリデーション実装
- `useForm` + `useActionState` + `mergeForm` で状態統合
- `form.Field` でフィールドレベルバリデーション
- エラーは `field.state.meta.errors` から取得

```tsx
"use client";

import { useForm } from "@tanstack/react-form";
import { updateUser } from "./actions";

export function UserForm() {
  const form = useForm({
    defaultValues: { email: "" },
    onSubmit: async ({ value }) => {
      await updateUser(value);
    },
  });

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        form.handleSubmit();
      }}
    >
      <form.Field name="email" />
      <button type="submit">Save</button>
    </form>
  );
}
```

### Server Actions

フォーム処理・データ操作はサーバーサイド：

```tsx
"use server";

import { db } from "@/lib/supabase/server";

export async function createUser(data: unknown) {
  const validData = userSchema.parse(data);

  const { data: user, error } = await db
    .from("users")
    .insert([validData])
    .select()
    .single();

  if (error) throw error;
  return user;
}
```

### エラー・成功フィードバック

- **エラー表示**: shadcn/ui `Alert` コンポーネント（`destructive` variant）+ `AlertCircle` アイコン
- **成功通知**: Sonner `toast.success()` を使用

### コメント・コード規約

- コメントは最小限、必要な箇所のみ（日本語）
- JSON/JSオブジェクトキーはアルファベット順に並べる
- 複雑なロジックには必ずテストを追加（日本語で記述）

## コード品質チェック

```bash
pnpm check       # Biome: Lint + Format
pnpm type-check  # TypeScript 型チェック
pnpm test        # Vitest によるテスト実行
```

詳細は [testing スキル](../testing/SKILL.md) と [github-workflow スキル](../github-workflow/SKILL.md) を参照してください。

## 参考

- [AGENTS.md](../../../AGENTS.md) - 開発ガイドライン全体
- [CONTRIBUTING.md](../../../CONTRIBUTING.md) - 貢献ガイドライン
