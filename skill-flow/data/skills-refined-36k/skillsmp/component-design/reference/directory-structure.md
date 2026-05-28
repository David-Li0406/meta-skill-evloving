# ディレクトリ構造

## プロジェクト全体のコンポーネント配置

```
src/
├── components/
│   ├── ui/                 # 基本的なUIコンポーネント
│   │   ├── Button/
│   │   ├── Input/
│   │   ├── Dialog/
│   │   └── ...
│   └── shared/             # 共通コンポーネント（レイアウト含む）
│       ├── Header/
│       ├── Footer/
│       ├── Sidebar/
│       ├── LoadingSpinner/
│       ├── ErrorBoundary/
│       └── ...
└── app/
    ├── dashboard/
    │   ├── page.tsx
    │   └── _components/    # ページ固有のコンポーネント (co-location)
    │       ├── DashboardChart/
    │       ├── StatsCard/
    │       └── ...
    ├── auth/
    │   ├── login/
    │   │   ├── page.tsx
    │   │   └── _components/
    │   │       ├── LoginForm/
    │   │       └── ...
    │   └── register/
    │       ├── page.tsx
    │       └── _components/
    │           ├── RegisterForm/
    │           └── ...
    └── ...
```

## コンポーネント配置のルール

### `src/components/ui/`
- shadcn/uiなどの基本的なUIコンポーネント
- 複数ページで使用される汎用コンポーネント
- Button、Input、Dialog、Cardなど

### `src/components/shared/`
- レイアウトコンポーネント（Header、Footer、Sidebar）
- 共通のユーティリティコンポーネント（LoadingSpinner、ErrorBoundary）
- 複数の機能領域で共有されるコンポーネント

### `app/*/page/_components/`
- ページ固有のコンポーネント
- Co-locationパターンに従った配置
- 他のページでは使用しないコンポーネント

## コンポーネントディレクトリ構造

### 基本構造

```
ComponentName/
├── index.tsx           # コンポーネント本体
└── styles.ts          # Panda CSS スタイル定義（必要に応じて）
```

### 複雑なコンポーネントの場合

```
ComponentName/
├── index.tsx           # メインエクスポート
├── ComponentName.tsx   # コンポーネント本体
├── styles.ts           # Panda CSS スタイル定義
├── types.ts            # 型定義
├── hooks.ts            # カスタムフック
└── ComponentName.test.tsx  # テスト（co-location）
```

## 命名規則

### ファイル名
- **PascalCase を使用**: `Button.tsx`, `UserProfile.tsx`
- **コンポーネント名とファイル名を一致させる**

### 例外：shadcn/ui
- shadcn/uiで生成されたコンポーネントはkebab-caseファイル名
- 例: `button.tsx`, `input.tsx`
- これらはそのまま使用し、新規作成するカスタムコンポーネントのみPascalCaseを適用

## Co-location パターン

### メリット
- 関連するコードが近くにある
- ファイルの検索が容易
- 機能削除時のクリーンアップが簡単

### 実践例

```
app/
└── users/
    ├── page.tsx
    ├── loading.tsx
    ├── error.tsx
    └── _components/
        ├── UserList/
        │   ├── index.tsx
        │   └── UserListItem.tsx
        └── UserSearchForm/
            └── index.tsx
```

### `_components` の役割
- アンダースコアプレフィックスはNext.jsのルーティングから除外される
- ページ固有のコンポーネントを整理する場所
- 他のページでは使用しないコンポーネントを格納
