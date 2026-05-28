# スタイリングガイド（Panda CSS）

## 基本的な使い方

### Panda CSS の使用
- Panda CSS を使用してスタイルを定義
- デザイントークンとレシピを活用
- 型安全なスタイル定義

```typescript
import { css } from "styled-system/css";
import { button } from "styled-system/recipes";

const buttonStyles = button({
  variant: "primary",
  size: "md",
});
```

## レシピの使用

### 基本的なレシピ

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
```

## css関数の使用

### インラインスタイル

```typescript
import { css } from 'styled-system/css';

const customStyles = css({
  padding: '1rem',
  backgroundColor: 'blue.500',
  _hover: {
    backgroundColor: 'blue.600'
  }
});
```

### 複雑なスタイル定義

```typescript
const cardStyles = css({
  display: 'flex',
  flexDirection: 'column',
  padding: '4',
  borderRadius: 'lg',
  boxShadow: 'md',
  backgroundColor: 'white',
  _dark: {
    backgroundColor: 'gray.800',
  },
  '& > h2': {
    fontSize: 'xl',
    fontWeight: 'bold',
    marginBottom: '2',
  },
});
```

## スタイルの分離

### 別ファイルへの分離

```typescript
// styles.ts
import { css } from 'styled-system/css';

export const containerStyles = css({
  maxWidth: 'container.lg',
  marginX: 'auto',
  paddingX: '4',
});

export const headerStyles = css({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  height: '16',
});
```

```typescript
// Component.tsx
import { containerStyles, headerStyles } from './styles';

export function Layout({ children }) {
  return (
    <div className={containerStyles}>
      <header className={headerStyles}>
        {/* ... */}
      </header>
      {children}
    </div>
  );
}
```

## クラス名の結合

### cn（className）ユーティリティの使用

```typescript
import { cn } from '@/lib/utils';

export function Card({ className, children }: CardProps) {
  return (
    <div className={cn('border rounded-lg p-4', className)}>
      {children}
    </div>
  );
}
```

### 条件付きスタイル

```typescript
import { css } from 'styled-system/css';
import { cn } from '@/lib/utils';

export function Button({ isActive, className }) {
  return (
    <button
      className={cn(
        css({ padding: '2', borderRadius: 'md' }),
        isActive && css({ backgroundColor: 'blue.500', color: 'white' }),
        className
      )}
    >
      Click me
    </button>
  );
}
```

## レスポンシブデザイン

### ブレークポイント

```typescript
const responsiveStyles = css({
  fontSize: 'sm',
  padding: '2',
  md: {
    fontSize: 'base',
    padding: '4',
  },
  lg: {
    fontSize: 'lg',
    padding: '6',
  },
});
```

### カスタムブレークポイント
- sm: 640px
- md: 768px
- lg: 1024px
- xl: 1280px
- 2xl: 1440px

## ダークモード対応

```typescript
const themedStyles = css({
  backgroundColor: 'white',
  color: 'gray.900',
  _dark: {
    backgroundColor: 'gray.900',
    color: 'gray.100',
  },
});
```

## ベストプラクティス

### 1. デザイントークンの活用
- 直接の数値ではなくトークンを使用
- `padding: 4` は `padding: 1rem` に相当

### 2. レシピを優先
- 再利用可能なスタイルはレシピとして定義
- コンポーネント固有のスタイルのみcss()を使用

### 3. スタイルの一貫性
- プロジェクト全体で同じトークンを使用
- カラーパレット、スペーシングの統一
