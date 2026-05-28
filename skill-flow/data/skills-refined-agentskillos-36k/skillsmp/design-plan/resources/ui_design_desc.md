# 画面開発（Web/フロントエンド）: UI/UX仕様設計

Web/フロントエンド開発における設計ドキュメントの作成ガイドです。

## 作成する設計ドキュメント

`docs/design/ui-specification.md` を作成:

- **画面構成**: ページレイアウトとセクション
- **コンポーネント構造**: UIコンポーネントの階層
- **状態管理**: アプリケーション状態とデータフロー
- **ユーザーインタラクション**: クリック、入力などのイベント
- **レスポンシブデザイン**: ブレークポイントとレイアウト変更
- **アクセシビリティ**: ARIA属性、キーボード操作

## 補助ツール（基本: Storybook）

- **Storybook**: コンポーネントカタログとUI開発環境（基本）
- **Figma / Adobe XD**: デザインモックアップとプロトタイプ
- **Chromatic**: ビジュアルレグレッションテスト
- **Zeplin**: デザインとコードの橋渡し
- **Histoire**: Vite向けの軽量Storybook代替

## Storybookのセットアップ

### インストール

```bash
# 自動セットアップ
npx storybook@latest init

# 起動
npm run storybook
```

### コンポーネントストーリー例（React + TypeScript）

`src/components/Button/Button.stories.tsx`:

```typescript
import type { Meta, StoryObj } from "@storybook/react";
import { Button } from "./Button";

const meta: Meta<typeof Button> = {
  title: "Components/Button",
  component: Button,
  parameters: {
    layout: "centered",
  },
  tags: ["autodocs"],
  argTypes: {
    variant: {
      control: "select",
      options: ["primary", "secondary", "danger"],
    },
    size: {
      control: "select",
      options: ["small", "medium", "large"],
    },
  },
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    variant: "primary",
    children: "Primary Button",
  },
};

export const Secondary: Story = {
  args: {
    variant: "secondary",
    children: "Secondary Button",
  },
};

export const Danger: Story = {
  args: {
    variant: "danger",
    children: "Danger Button",
  },
};

export const Small: Story = {
  args: {
    size: "small",
    children: "Small Button",
  },
};

export const Large: Story = {
  args: {
    size: "large",
    children: "Large Button",
  },
};

export const Disabled: Story = {
  args: {
    disabled: true,
    children: "Disabled Button",
  },
};

export const WithIcon: Story = {
  args: {
    children: (
      <>
        <Icon name="plus" /> Add Item
      </>
    ),
  },
};
```

### Vue 3 での例

`src/components/Button/Button.stories.ts`:

```typescript
import type { Meta, StoryObj } from "@storybook/vue3";
import Button from "./Button.vue";

const meta: Meta<typeof Button> = {
  title: "Components/Button",
  component: Button,
  tags: ["autodocs"],
  argTypes: {
    variant: {
      control: "select",
      options: ["primary", "secondary", "danger"],
    },
  },
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    variant: "primary",
    label: "Primary Button",
  },
};
```

## UI仕様書テンプレート

`docs/design/ui-specification.md`:

```markdown
# UI仕様: [画面名]

## 概要

[画面の目的と主要機能の説明]

## デザインモックアップ

[Figmaリンクや画像を挿入]

## 画面構成

### レイアウト構造
```

Page
├── Header
│ ├── Logo
│ ├── Navigation
│ └── UserMenu
├── MainContent
│ ├── Sidebar
│ │ ├── FilterPanel
│ │ └── QuickActions
│ └── ContentArea
│ ├── SearchBar
│ ├── DataTable
│ └── Pagination
└── Footer
├── Links
└── Copyright

```

### コンポーネント一覧

| コンポーネント | 説明                   | 状態             | Props                    |
| -------------- | ---------------------- | ---------------- | ------------------------ |
| Header         | ページヘッダー         | ログイン状態     | user, onLogout           |
| Navigation     | ナビゲーションメニュー | アクティブページ | items, activePath        |
| DataTable      | データ表示テーブル     | ソート、選択     | data, columns, onSort    |
| SearchBar      | 検索バー               | 検索クエリ       | onSearch, placeholder    |
| Pagination     | ページネーション       | 現在ページ       | total, current, onChange |

## コンポーネント詳細

### Button コンポーネント
```

**Props**:

```typescript
interface ButtonProps {
  variant: "primary" | "secondary" | "danger";
  size: "small" | "medium" | "large";
  disabled?: boolean;
  loading?: boolean;
  icon?: ReactNode;
  onClick?: () => void;
  children: ReactNode;
}
```

**使用例**:

```tsx
<Button variant="primary" size="medium" onClick={handleClick}>
  Save
</Button>

<Button variant="danger" loading={isDeleting}>
  Delete
</Button>
```

**状態**:

- Default: 通常状態
- Hover: ホバー時の色変更
- Active: クリック時の状態
- Disabled: 無効化状態
- Loading: 処理中状態（スピナー表示）

### DataTable コンポーネント

**Props**:

```typescript
interface Column<T> {
  key: keyof T;
  header: string;
  sortable?: boolean;
  render?: (value: T[keyof T], row: T) => ReactNode;
}

interface DataTableProps<T> {
  data: T[];
  columns: Column<T>[];
  onSort?: (key: keyof T, direction: "asc" | "desc") => void;
  onRowClick?: (row: T) => void;
  loading?: boolean;
  emptyMessage?: string;
}
```

**使用例**:

```tsx
<DataTable
  data={users}
  columns={[
    { key: "name", header: "Name", sortable: true },
    { key: "email", header: "Email", sortable: true },
    {
      key: "status",
      header: "Status",
      render: (value) => <Badge>{value}</Badge>,
    },
  ]}
  onSort={handleSort}
  onRowClick={handleRowClick}
  loading={isLoading}
/>
```

## 状態管理

### ローカル状態（コンポーネント内）

- フォーム入力値
- モーダルの開閉状態
- ドロップダウンの展開状態

### グローバル状態（Redux/Zustand/Context）

- ユーザー認証情報
- アプリケーション設定
- 共有データ（ユーザー一覧、商品一覧など）

### 状態フロー図

```
User Action (クリック)
↓
Event Handler
↓
State Update (setState/dispatch)
↓
Re-render
↓
UI Update
```

## ユーザーインタラクション

### 主要な操作フロー

#### 1. ユーザー検索

1. SearchBar にキーワードを入力
2. 入力中は debounce（300ms）
3. 検索APIを呼び出し
4. DataTable を更新
5. 結果が0件の場合、EmptyState を表示

#### 2. データソート

1. テーブルヘッダーのソートアイコンをクリック
2. ソート方向を切り替え（asc → desc → none）
3. データを再取得またはクライアントソート
4. テーブルを更新

#### 3. アイテム削除

1. 削除ボタンをクリック
2. 確認モーダルを表示
3. 「削除」をクリック
4. 削除APIを呼び出し
5. 成功時: トースト通知、リスト更新
6. 失敗時: エラーメッセージ表示

### イベント一覧

| イベント | トリガー       | アクション                   |
| -------- | -------------- | ---------------------------- |
| onClick  | ボタンクリック | フォーム送信、モーダル表示   |
| onChange | 入力値変更     | 状態更新、バリデーション     |
| onSubmit | フォーム送信   | APIリクエスト                |
| onScroll | スクロール     | 無限スクロール、ヘッダー固定 |

## レスポンシブデザイン

### ブレークポイント

```css
/* Mobile */
@media (max-width: 767px) {
  /* モバイル専用スタイル */
}

/* Tablet */
@media (min-width: 768px) and (max-width: 1023px) {
  /* タブレット専用スタイル */
}

/* Desktop */
@media (min-width: 1024px) {
  /* デスクトップ専用スタイル */
}
```

### レイアウト変更

| デバイス                    | レイアウト     | 特徴                                   |
| --------------------------- | -------------- | -------------------------------------- |
| モバイル (< 768px)          | シングルカラム | サイドバー非表示、ハンバーガーメニュー |
| タブレット (768px - 1024px) | 2カラム        | サイドバー折りたたみ可能               |
| デスクトップ (> 1024px)     | 3カラム        | サイドバー常時表示                     |

### レスポンシブコンポーネント例

```tsx
const ResponsiveLayout = () => {
  const isMobile = useMediaQuery("(max-width: 767px)");

  return (
    <div className="layout">
      {!isMobile && <Sidebar />}
      <MainContent />
      {isMobile && <MobileNavigation />}
    </div>
  );
};
```

## アクセシビリティ

### ARIA属性

```tsx
<button
  aria-label="ユーザーを削除"
  aria-describedby="delete-description"
  aria-pressed={isActive}
>
  削除
</button>

<div id="delete-description" role="tooltip">
  このアクションは取り消せません
</div>
```

### キーボード操作

| キー       | 操作                                  |
| ---------- | ------------------------------------- |
| Tab        | フォーカス移動                        |
| Enter      | ボタンクリック、リンク遷移            |
| Space      | チェックボックス/ラジオボタン切り替え |
| Escape     | モーダル/ドロップダウンを閉じる       |
| Arrow Keys | リスト内の移動                        |

### フォーカス管理

```tsx
// モーダル表示時にフォーカスをトラップ
const Modal = ({ isOpen, onClose }) => {
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isOpen && modalRef.current) {
      modalRef.current.focus();
    }
  }, [isOpen]);

  return (
    <div ref={modalRef} role="dialog" aria-modal="true" tabIndex={-1}>
      {/* モーダルコンテンツ */}
    </div>
  );
};
```

### カラーコントラスト

WCAG AA基準を満たすコントラスト比:

- 通常テキスト: 4.5:1 以上
- 大きなテキスト: 3:1 以上

## スタイリング

### CSS-in-JS（styled-components）

```tsx
import styled from "styled-components";

const Button = styled.button<{ variant: "primary" | "secondary" }>`
  padding: 0.75rem 1.5rem;
  border-radius: 0.25rem;
  font-weight: 600;
  transition: all 0.2s;

  ${({ variant }) =>
    variant === "primary" &&
    `
      background-color: #3b82f6;
      color: white;

      &:hover {
        background-color: #2563eb;
      }
    `}

  ${({ variant }) =>
    variant === "secondary" &&
    `
      background-color: #6b7280;
      color: white;

      &:hover {
        background-color: #4b5563;
      }
    `}

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;
```

### Tailwind CSS

```tsx
<button className="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded transition-colors disabled:opacity-50">
  Submit
</button>
```

## パフォーマンス最適化

### 1. コード分割

```tsx
import { lazy, Suspense } from "react";

const HeavyComponent = lazy(() => import("./HeavyComponent"));

<Suspense fallback={<Loading />}>
  <HeavyComponent />
</Suspense>;
```

### 2. メモ化

```tsx
import { memo, useMemo, useCallback } from "react";

const ExpensiveComponent = memo(({ data }) => {
  const processedData = useMemo(() => {
    return data.map((item) => heavyCalculation(item));
  }, [data]);

  const handleClick = useCallback(() => {
    // 処理
  }, []);

  return <div>{/* ... */}</div>;
});
```

### 3. 画像最適化

```tsx
<img
  src="image.jpg"
  srcSet="image-320w.jpg 320w, image-640w.jpg 640w, image-1280w.jpg 1280w"
  sizes="(max-width: 768px) 100vw, 50vw"
  loading="lazy"
  alt="Description"
/>
```

## テスト設計の考慮事項

1. **ユニットテスト**

   - コンポーネントが正しくレンダリングされる
   - Props が正しく渡される
   - イベントハンドラーが呼ばれる

2. **統合テスト**

   - ユーザーフローが正常に動作する
   - 状態管理が正しく機能する

3. **ビジュアルレグレッションテスト**

   - UI の見た目が意図通りである
   - レスポンシブデザインが正しく機能する

4. **アクセシビリティテスト**
   - キーボード操作が可能
   - スクリーンリーダー対応

## 設計チェックリスト

- [ ] コンポーネントが適切に分割されているか
- [ ] Props の型定義が明確か
- [ ] 状態管理の責任が明確か
- [ ] レスポンシブデザインが考慮されているか
- [ ] アクセシビリティ対応がされているか
- [ ] パフォーマンスが最適化されているか
- [ ] エラー状態が適切に処理されているか
- [ ] ローディング状態が表示されるか
- [ ] 空状態（データなし）が表示されるか
- [ ] デザインシステムに準拠しているか
