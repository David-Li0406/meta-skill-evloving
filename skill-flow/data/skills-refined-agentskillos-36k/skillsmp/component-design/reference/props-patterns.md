# Props設計パターン

## 型定義

### Props インターフェース

```typescript
interface ButtonProps {
  children: React.ReactNode;
  variant?: "primary" | "secondary" | "danger";
  size?: "sm" | "md" | "lg";
  disabled?: boolean;
  onClick?: () => void;
}
```

### デフォルトProps

```typescript
const defaultProps: Partial<ButtonProps> = {
  variant: "primary",
  size: "md",
  disabled: false,
};
```

## イベントハンドリング

### 命名規則
- `on` + 動詞の命名規則を使用
- 例: `onClick`, `onSubmit`, `onChange`

### 型定義

```typescript
interface FormProps {
  onSubmit: (data: FormData) => void;
  onChange: (field: string, value: string) => void;
}
```

## 状態管理

### ローカル状態
- `useState` でローカル状態を管理
- 複雑な状態は `useReducer` を検討

```typescript
const [isOpen, setIsOpen] = useState(false);

// 複雑な状態の場合
const [state, dispatch] = useReducer(reducer, initialState);
```

## エラーハンドリング

### Error Boundary
- 予期しないエラーをキャッチ
- ユーザーフレンドリーなエラー表示

### バリデーション
- フォーム入力のバリデーション
- 適切なエラーメッセージの表示

## 実装例

### 基本的なButtonコンポーネント

```typescript
// index.tsx
export interface ButtonProps {
  children: React.ReactNode;
  variant?: "primary" | "secondary" | "danger";
  size?: "sm" | "md" | "lg";
  disabled?: boolean;
  onClick?: () => void;
}

import { button } from "styled-system/recipes";
import type { ButtonProps } from "./types";

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = "primary",
  size = "md",
  disabled = false,
  onClick,
}) => {
  return (
    <button
      className={button({ variant, size })}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  );
};
```

## パフォーマンス

### メモ化
- `React.memo` で不要な再レンダリングを防止
- `useMemo`, `useCallback` で計算結果をキャッシュ

```typescript
const MemoizedComponent = React.memo(({ data, onClick }) => {
  return <div onClick={onClick}>{data.name}</div>;
});

// useCallbackでコールバックをメモ化
const handleClick = useCallback(() => {
  // 処理
}, [dependency]);
```

### 遅延読み込み
- `React.lazy` で大きなコンポーネントの遅延読み込み
- `Suspense` で読み込み状態を表示

```typescript
const HeavyComponent = React.lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <HeavyComponent />
    </Suspense>
  );
}
```

## アクセシビリティ

### セマンティックHTML
- 適切なHTMLタグを使用
- `aria-*` 属性の適切な使用

```typescript
<button
  aria-label="メニューを開く"
  aria-expanded={isOpen}
>
  <MenuIcon />
</button>
```

### キーボード操作
- キーボードのみでの操作を可能にする
- フォーカス管理の実装

```typescript
const handleKeyDown = (e: React.KeyboardEvent) => {
  if (e.key === 'Enter' || e.key === ' ') {
    handleClick();
  }
};
```
