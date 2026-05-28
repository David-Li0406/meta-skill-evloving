---
name: frontend-development-guidelines
description: Use this skill when defining frontend development rules, including environment setup, component design, data flow, and state management for React applications.
---

# フロントエンド開発ガイドライン

このスキルは、Reactアプリケーションのフロントエンド開発における環境設定、コンポーネント設計、データフロー、状態管理のルールを定義します。

## 技術スタックの基本方針
TypeScriptベースのReactアプリケーションを実装し、アーキテクチャパターンはプロジェクトの要件と規模に応じて選択します。

## 環境変数管理とセキュリティ

### 環境変数管理
- ビルドツールの環境変数システムを使用し、`process.env`はブラウザ環境で動作しないため、設定レイヤーを通じて環境変数を一元管理します。
- TypeScriptによる型安全性を実装し、デフォルト値設定と必須チェックを行います。

```typescript
const config = {
  apiUrl: import.meta.env.API_URL || 'http://localhost:3000',
  appName: import.meta.env.APP_NAME || 'My App'
}
```

### セキュリティ
- すべてのフロントエンドコードは公開され、ブラウザで見えるため、クライアントサイドに秘密情報を保存しないことが重要です。
- `.env`ファイルをGitに含めず、機密情報のログ出力を禁止します。

## コンポーネント設計

### 基本ルール
- 関数コンポーネントを使用し、再描画コストが高い場合は `React.memo` を使用します。
- Propsは同ファイル内で `type Props` として定義し、単一責任の原則を守ります。

### 命名規則
- コンポーネント名は `PascalCase`、props/変数名は `camelCase` で命名します。

### 条件付きレンダリング
```tsx
{isLoading ? <Spinner /> : <Content />}
```

### アクセシビリティ
- aria属性を適切に設定し、セマンティックHTMLを使用します。

## データフロー統一原則

### クライアントサイドのデータフロー
- Single Source of Truthを維持し、データはPropsを通じて上から下へ流れます。
- State更新には不変パターンを使用します。

```typescript
setUsers(prev => [...prev, newUser])
```

### 型安全性
- Props/State（型保証済み）からAPIリクエスト（シリアライゼーション）を行い、APIレスポンスを型ガードで確認します。

## 状態管理パターン

### Zustand（推奨）
```typescript
import { create } from 'zustand';

const useAuthStore = create<AuthState>()((set) => ({
  user: null,
  isAuthenticated: false,
  login: (user) => set({ user, isAuthenticated: true }),
  logout: () => set({ user: null, isAuthenticated: false }),
}));
```

### Context API
- 状態をコンポーネントツリー全体で共有するためにContext APIを使用します。

## フォーム処理

### React Hook Form + Zod
```typescript
const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
  resolver: zodResolver(schema),
});
```

## データフェッチング

### TanStack Query
```typescript
import { useQuery } from '@tanstack/react-query';

function useUser(userId: string) {
  return useQuery(['user', userId], () => fetchUser(userId));
}
```

## 品質チェック要件
実装完了時に品質チェックは必須です。すべてのコンポーネントはテスト可能であり、アクセシビリティ要件を満たす必要があります。

---

このガイドラインに従って、フロントエンドの実装を行い、プロトタイプを本番品質のユーザーインターフェースに変換します。