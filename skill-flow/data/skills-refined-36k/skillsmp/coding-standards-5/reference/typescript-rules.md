# TypeScript 規約

## 型安全性

### ❌ any型の使用禁止

```typescript
// ❌ 禁止
function processData(data: any) {
  return data.someProperty;
}

const user: any = getUser();

// ✅ 推奨
interface User {
  id: string;
  name: string;
  email: string;
}

function processData(data: User) {
  return data.name;
}

const user: User = getUser();
```

**any型が絶対に禁止される理由:**
- TypeScriptの型チェック機能を無効化
- ランタイムエラーの原因となる
- IDEの自動補完・リファクタリング機能が働かない
- コードの可読性・保守性が著しく低下

### 型定義のベストプラクティス

```typescript
// ✅ 明確な型定義
interface ApiResponse<T> {
  data: T;
  status: 'success' | 'error';
  message?: string;
}

// ✅ Union型の活用
type ButtonVariant = 'primary' | 'secondary' | 'danger';

// ✅ Generic型の活用
function createApiCall<T>(endpoint: string): Promise<ApiResponse<T>> {
  // 実装
}

// ✅ 型ガードの使用
function isUser(obj: unknown): obj is User {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    typeof (obj as User).id === 'string'
  );
}
```

### unknown型の活用

```typescript
// ✅ anyの代わりにunknownを使用
function parseJson(json: string): unknown {
  return JSON.parse(json);
}

// ✅ 型ガードと組み合わせて安全に使用
const data = parseJson(jsonString);
if (isUser(data)) {
  console.log(data.name); // 型安全
}
```

## 厳格な型チェック設定

`tsconfig.json`で以下の設定を必須とする：

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "noImplicitReturns": true,
    "noImplicitThis": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true
  }
}
```

## React / Next.js での型安全性

### Props型定義

```typescript
// ✅ 明確なProps型定義（any型禁止）
interface ComponentProps {
  data: UserData; // 具体的な型を指定
  onAction: (id: string) => void; // 関数型も明確に
}

// ❌ any型の使用禁止
interface BadProps {
  data: any; // 絶対禁止
  callback: any; // 絶対禁止
}
```

## コード構造・パターン

### エクスポート規約

```typescript
// ✅ 名前付きエクスポート（推奨）
export function Button() { }
export { Button };

// ✅ デフォルトエクスポート（Pageコンポーネントのみ）
export default function HomePage() { }

// ❌ 混在は避ける
export function Button() { }
export default Button; // 避ける
```

### 条件分岐

#### 早期リターン

```typescript
// ✅ 早期リターンパターン
function processUser(user: User | null): string {
  if (!user) {
    return 'User not found';
  }

  if (!user.isActive) {
    return 'User is inactive';
  }

  return `Welcome, ${user.name}!`;
}

// ❌ ネストの深い条件分岐
function processUser(user: User | null): string {
  if (user) {
    if (user.isActive) {
      return `Welcome, ${user.name}!`;
    } else {
      return 'User is inactive';
    }
  } else {
    return 'User not found';
  }
}
```

#### Optional Chaining の活用

```typescript
// ✅ Optional Chaining
const userName = user?.profile?.name ?? 'Anonymous';
const hasAdminRole = user?.roles?.includes('admin') ?? false;

// ✅ Nullish Coalescing
const config = userConfig ?? defaultConfig;
const port = process.env.PORT ?? 3000;
```

## エラーハンドリング

### エラー型の定義

```typescript
// ✅ カスタムエラークラス
class ApiError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public code: string
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

// ✅ Result型パターン
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

function safeApiCall<T>(fn: () => Promise<T>): Promise<Result<T>> {
  return fn()
    .then(data => ({ success: true as const, data }))
    .catch(error => ({ success: false as const, error }));
}
```

### エラーハンドリングパターン

```typescript
// ✅ try-catch の適切な使用
async function fetchUser(id: string): Promise<User | null> {
  try {
    const response = await api.get(`/users/${id}`);
    return response.data;
  } catch (error) {
    if (error instanceof ApiError && error.statusCode === 404) {
      return null;
    }
    throw error; // 予期しないエラーは再スロー
  }
}

// ✅ Error Boundary での エラーキャッチ
export function ErrorBoundary({ children }: { children: React.ReactNode }) {
  return (
    <ErrorBoundaryComponent
      fallback={<ErrorFallback />}
      onError={(error, errorInfo) => {
        console.error('Error caught by boundary:', error, errorInfo);
      }}
    >
      {children}
    </ErrorBoundaryComponent>
  );
}
```

## テストでの型安全性

```typescript
// ✅ テストでもany型禁止
interface MockUser {
  id: string;
  name: string;
}

const mockUser: MockUser = { id: '1', name: 'Test User' };

// ❌ テストでもany型は使用禁止
const badMockData: any = { /* データ */ }; // 禁止
```
