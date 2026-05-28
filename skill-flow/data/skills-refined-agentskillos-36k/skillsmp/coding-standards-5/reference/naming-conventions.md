# 命名規則

## ファイル・ディレクトリ命名

### 基本的な命名原則

- **Reactコンポーネント**: PascalCase（例: `UserProfile.tsx`）
- **ユーティリティファイル**: camelCase（例: `authConfig.ts`）
- **Next.jsファイル**: lowercase（例: `page.tsx`, `layout.tsx`）

**注意**: shadcn/uiで生成されたコンポーネントはkebab-caseファイル名（例: `button.tsx`, `input.tsx`）を使用しており、この命名規則の例外となります。

## 変数・関数命名

### 変数名

```typescript
// ✅ camelCase
const userName = 'john';
const isLoggedIn = true;
const userList = [];

// ✅ boolean値は is/has/can などで開始
const isVisible = true;
const hasPermission = false;
const canEdit = true;

// ✅ 定数はSCREAMING_SNAKE_CASE
const API_ENDPOINT = 'https://api.example.com';
const MAX_RETRY_COUNT = 3;
```

### 関数名

```typescript
// ✅ 動詞で開始
function getUserById(id: string): User | null { }
function validateEmail(email: string): boolean { }
function handleSubmit(): void { }

// ✅ イベントハンドラーは "handle" または "on" で開始
function handleClick(): void { }
function onUserSelect(user: User): void { }

// ✅ 戻り値がbooleanの場合は is/has/can で開始
function isValidUser(user: User): boolean { }
function hasPermission(user: User, action: string): boolean { }
```

### インターフェース・型名

```typescript
// ✅ PascalCase
interface User {
  id: string;
  name: string;
}

// ✅ Props は "Props" サフィックス
interface UserCardProps {
  user: User;
  onEdit?: () => void;
}

// ✅ 型は Type サフィックス（必要に応じて）
type ApiResponseType<T> = {
  data: T;
  status: string;
};

// ✅ Union型は具体的な名前
type ButtonVariant = 'primary' | 'secondary' | 'danger';
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';
```

## コメント規約

### JSDoc の使用

```typescript
/**
 * ユーザー情報を取得する
 * @param id - ユーザーID
 * @returns ユーザー情報、見つからない場合はnull
 * @throws {ApiError} API呼び出しが失敗した場合
 */
async function getUserById(id: string): Promise<User | null> {
  // 実装
}
```

### インラインコメント

```typescript
// ✅ 「なぜ」を説明するコメント
// Safari では transform-origin が正しく動作しないため、明示的に設定
element.style.transformOrigin = 'center center';

// ✅ 複雑なビジネスロジックの説明
// 管理者は全てのデータにアクセス可能、
// 一般ユーザーは自分のデータのみアクセス可能
const hasAccess = user.role === 'admin' || user.id === resourceOwnerId;

// ❌ 「何を」するかのコメント（不要）
// ユーザー名を取得
const userName = user.name;
```
