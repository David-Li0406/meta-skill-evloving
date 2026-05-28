---
name: react
description: React開発ルール。コンポーネント（関数コンポーネント、Props、条件付きレンダリング）、カスタムフック（use*命名、状態管理）、Storybook（CSF3.0）の規約を定義。React実装時に参照。
---

# React開発ルール

Reactコンポーネント、カスタムフック、Storybookの規約を定義するスキル。

## コンポーネント

### 基本ルール

- 関数コンポーネントを使用（`React.FC` は使用しない）
- 再描画コストが高い場合は `React.memo` を使用
- Propsは同ファイル内で `type Props` として定義
- 単一責任の原則（1コンポーネント = 1責任）
- ビジネスロジックはcustom hooksに抽出

### 命名規則

- コンポーネント名: `PascalCase`
- props/変数名: `camelCase`

### 条件付きレンダリング

```tsx
// ✅ 推奨: 三項演算子
{isLoading ? <Spinner /> : <Content />}

// ❌ 非推奨: 論理演算子（falsy値の問題）
{count && <Badge count={count} />}
```

### アクセシビリティ

- aria属性を適切に設定
- セマンティックHTMLを使用
- キーボード操作を考慮

## カスタムフック

### 基本ルール

- **命名規則**: 必ず `use` で始める（例: `useUserData`）
- **単一責任**: 1フック = 1機能
- **戻り値**: 配列またはオブジェクトで統一
- **型定義**: 戻り値の型を明示的に定義
- **エラーハンドリング**: エラー状態も戻り値に含める

### 推奨パターン

```typescript
type UseUserDataResult = {
  user: User | null;
  isLoading: boolean;
  error: Error | null;
  refetch: () => void;
};

export const useUserData = (userId: string): UseUserDataResult => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  // ...
  return { user, isLoading, error, refetch };
};
```

### テスト

```typescript
import { renderHook, act } from "@testing-library/react";

test("初期値が0である", () => {
  const { result } = renderHook(() => useCounter());
  expect(result.current.count).toBe(0);
});
```

## Storybook

### 基本ルール

- **ファイル名**: `ComponentName.stories.tsx`
- **CSF3.0**: Component Story Format 3.0 を使用
- **型定義**: `Meta<typeof Component>` と `StoryObj<typeof Component>`
- **Title設定**: Metaに title は設定しない（自動生成）

### Story種類

| Story | 内容 |
|:-|:-|
| Default | 基本的な使用例 |
| AllProps | 全props設定状態 |
| EdgeCases | 境界値・特殊状態 |

### 基本例

```tsx
import type { Meta, StoryObj } from "@storybook/react";
import { fn } from "@storybook/test";
import { Button } from "./Button";

const meta: Meta<typeof Button> = {
  component: Button,
  args: { onClick: fn() },
};
export default meta;

type Story = StoryObj<typeof Button>;

export const Default: Story = {
  args: { label: "Click me" },
};
```

### 禁止事項

- Story内でビジネスロジックを実装しない
- API呼び出しや外部サービスへの直接依存を避ける
