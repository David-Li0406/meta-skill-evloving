---
name: TypeScript 規範
description: TypeScript 編碼規範與最佳實踐
---

# TypeScript 規範

## 基本設定

### tsconfig.json
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022", "DOM"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "skipLibCheck": true
  }
}
```

---

## 類型定義

### 基本類型
```typescript
// 明確類型
const name: string = 'John';
const age: number = 30;
const isActive: boolean = true;

// 陣列
const items: string[] = ['a', 'b'];
const numbers: Array<number> = [1, 2, 3];

// 元組
const tuple: [string, number] = ['hello', 42];
```

### Interface vs Type
```typescript
// Interface - 物件結構、可擴展
interface User {
  id: number;
  name: string;
  email: string;
}

interface Admin extends User {
  role: 'admin';
  permissions: string[];
}

// Type - 聯合類型、複雜類型
type Status = 'pending' | 'active' | 'inactive';
type Callback = (data: User) => void;
type Maybe<T> = T | null | undefined;
```

### 泛型
```typescript
// 函式泛型
function getFirst<T>(arr: T[]): T | undefined {
  return arr[0];
}

// Interface 泛型
interface ApiResponse<T> {
  success: boolean;
  data: T;
  error?: string;
}

// 約束泛型
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
```

---

## 函式

```typescript
// 參數和回傳類型
function greet(name: string, age?: number): string {
  return `Hello, ${name}`;
}

// 箭頭函式
const add = (a: number, b: number): number => a + b;

// 非同步函式
async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}

// 函式重載
function format(value: string): string;
function format(value: number): string;
function format(value: string | number): string {
  return String(value);
}
```

---

## 型別守衛

```typescript
// typeof
function process(value: string | number) {
  if (typeof value === 'string') {
    return value.toUpperCase();
  }
  return value * 2;
}

// in
function handleEvent(event: MouseEvent | KeyboardEvent) {
  if ('key' in event) {
    console.log(event.key);
  }
}

// 自訂型別守衛
function isUser(obj: unknown): obj is User {
  return typeof obj === 'object' && obj !== null && 'id' in obj;
}
```

---

## 最佳實踐

1. **啟用 strict 模式**
2. **避免 any，使用 unknown**
3. **優先使用 interface**
4. **使用類型推斷**
5. **明確回傳類型**
6. **使用 readonly 保護資料**
