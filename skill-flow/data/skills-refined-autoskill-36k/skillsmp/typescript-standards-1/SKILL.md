---
name: typescript-standards
description: TypeScript 代码规范和最佳实践。用于编写、审查和优化 TypeScript 代码，确保类型安全和代码质量。
allowed-tools: Read, Grep, Glob, Edit
---

# TypeScript 代码规范

## 类型系统

### 避免 any
```typescript
// ❌ 不好
function process(data: any) {
  return data.value;
}

// ✅ 好
interface Data {
  value: string;
}
function process(data: Data): string {
  return data.value;
}

// ✅ 如果类型真的未知，使用 unknown
function process(data: unknown) {
  if (typeof data === 'object' && data !== null && 'value' in data) {
    return (data as Data).value;
  }
}
```

### 使用严格模式
在 `tsconfig.json` 中启用：
```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true
  }
}
```

### 类型定义

#### Interface vs Type
```typescript
// Interface - 用于对象形状
interface User {
  id: string;
  name: string;
  email: string;
}

// Type - 用于联合类型、交叉类型、工具类型
type Status = 'pending' | 'active' | 'inactive';
type UserWithStatus = User & { status: Status };
```

#### 泛型
```typescript
// ✅ 好的泛型使用
function getFirstItem<T>(items: T[]): T | undefined {
  return items[0];
}

// ✅ 约束泛型
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// ✅ 默认泛型参数
interface Response<T = unknown> {
  data: T;
  status: number;
}
```

### 类型推断
```typescript
// ✅ 让 TypeScript 推断简单类型
const count = 0; // number
const name = 'John'; // string
const items = [1, 2, 3]; // number[]

// ✅ 显式声明复杂类型
const user: User = {
  id: '1',
  name: 'John',
  email: 'john@example.com'
};
```

### 联合类型和类型守卫
```typescript
type Result =
  | { success: true; data: string }
  | { success: false; error: string };

function handleResult(result: Result) {
  if (result.success) {
    console.log(result.data); // TypeScript 知道这里有 data
  } else {
    console.log(result.error); // TypeScript 知道这里有 error
  }
}

// 自定义类型守卫
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'name' in value
  );
}
```

## 函数

### 函数签名
```typescript
// ✅ 明确的参数和返回类型
function calculateTotal(
  items: CartItem[],
  discount: number = 0
): number {
  const subtotal = items.reduce((sum, item) => sum + item.price, 0);
  return subtotal * (1 - discount);
}

// ✅ 可选参数
function greet(name: string, title?: string): string {
  return title ? `${title} ${name}` : name;
}

// ✅ 剩余参数
function sum(...numbers: number[]): number {
  return numbers.reduce((a, b) => a + b, 0);
}
```

### 函数重载
```typescript
function format(value: string): string;
function format(value: number): string;
function format(value: Date): string;
function format(value: string | number | Date): string {
  if (value instanceof Date) {
    return value.toISOString();
  }
  return String(value);
}
```

## 类和接口

### 类定义
```typescript
class UserService {
  // 私有属性
  private readonly apiUrl: string;

  // 公共属性
  public users: User[] = [];

  constructor(apiUrl: string) {
    this.apiUrl = apiUrl;
  }

  // 异步方法
  async fetchUsers(): Promise<User[]> {
    const response = await fetch(this.apiUrl);
    this.users = await response.json();
    return this.users;
  }

  // 私有方法
  private validateUser(user: User): boolean {
    return !!user.id && !!user.name;
  }
}
```

### 抽象类和接口
```typescript
// 接口定义契约
interface Repository<T> {
  findById(id: string): Promise<T | null>;
  save(entity: T): Promise<T>;
  delete(id: string): Promise<void>;
}

// 抽象类提供基础实现
abstract class BaseRepository<T> implements Repository<T> {
  abstract findById(id: string): Promise<T | null>;

  async save(entity: T): Promise<T> {
    // 通用保存逻辑
    return entity;
  }

  async delete(id: string): Promise<void> {
    // 通用删除逻辑
  }
}
```

## 工具类型

### 内置工具类型
```typescript
interface User {
  id: string;
  name: string;
  email: string;
  age: number;
}

// Partial - 所有属性可选
type PartialUser = Partial<User>;

// Required - 所有属性必需
type RequiredUser = Required<PartialUser>;

// Pick - 选择部分属性
type UserPreview = Pick<User, 'id' | 'name'>;

// Omit - 排除部分属性
type UserWithoutEmail = Omit<User, 'email'>;

// Record - 创建对象类型
type UserMap = Record<string, User>;

// Readonly - 只读
type ReadonlyUser = Readonly<User>;
```

### 自定义工具类型
```typescript
// 深度只读
type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object
    ? DeepReadonly<T[P]>
    : T[P];
};

// 可空类型
type Nullable<T> = T | null;

// 提取 Promise 类型
type Awaited<T> = T extends Promise<infer U> ? U : T;
```

## 枚举

### 使用 const enum
```typescript
// ✅ 好 - const enum 编译后会被内联
const enum Status {
  Pending = 'PENDING',
  Active = 'ACTIVE',
  Inactive = 'INACTIVE'
}

// ✅ 或使用联合类型（更推荐）
type Status = 'PENDING' | 'ACTIVE' | 'INACTIVE';

// ❌ 避免普通 enum（会生成额外代码）
enum Status {
  Pending,
  Active,
  Inactive
}
```

## 模块和导入

### 导入导出
```typescript
// ✅ 命名导出（推荐）
export interface User { }
export function createUser() { }

// ✅ 默认导出（适用于单一导出）
export default class UserService { }

// ✅ 类型导入
import type { User } from './types';

// ✅ 重新导出
export { User, type UserRole } from './types';
```

### 路径别名
```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@components/*": ["src/components/*"],
      "@utils/*": ["src/utils/*"]
    }
  }
}
```

```typescript
// 使用别名
import { Button } from '@components/Button';
import { formatDate } from '@utils/date';
```

## React 与 TypeScript

### 组件类型
```typescript
// 函数组件
interface ButtonProps {
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}

const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  disabled = false,
  onClick,
  children
}) => {
  return (
    <button
      className={variant}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  );
};
```

### Hooks 类型
```typescript
// useState
const [count, setCount] = useState<number>(0);
const [user, setUser] = useState<User | null>(null);

// useRef
const inputRef = useRef<HTMLInputElement>(null);

// useReducer
type State = { count: number };
type Action =
  | { type: 'increment' }
  | { type: 'decrement' }
  | { type: 'set'; value: number };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'increment':
      return { count: state.count + 1 };
    case 'decrement':
      return { count: state.count - 1 };
    case 'set':
      return { count: action.value };
  }
}

const [state, dispatch] = useReducer(reducer, { count: 0 });
```

### 事件处理
```typescript
// 表单事件
const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
  e.preventDefault();
};

// 输入事件
const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  console.log(e.target.value);
};

// 点击事件
const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
  console.log(e.currentTarget);
};
```

## 错误处理

### 自定义错误类型
```typescript
class ValidationError extends Error {
  constructor(
    message: string,
    public field: string
  ) {
    super(message);
    this.name = 'ValidationError';
  }
}

// 使用
function validateEmail(email: string): void {
  if (!email.includes('@')) {
    throw new ValidationError('Invalid email', 'email');
  }
}
```

### Result 类型
```typescript
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

function divide(a: number, b: number): Result<number> {
  if (b === 0) {
    return { ok: false, error: new Error('Division by zero') };
  }
  return { ok: true, value: a / b };
}
```

## 最佳实践

### 1. 优先使用类型推断
- 简单类型让 TypeScript 推断
- 复杂类型显式声明

### 2. 使用严格模式
- 启用所有严格检查
- 避免类型断言（as）

### 3. 避免类型断言
```typescript
// ❌ 不好
const user = data as User;

// ✅ 好 - 使用类型守卫
if (isUser(data)) {
  const user = data;
}
```

### 4. 使用 const assertions
```typescript
// ✅ 字面量类型
const config = {
  apiUrl: 'https://api.example.com',
  timeout: 5000
} as const;

// config.apiUrl 类型是 'https://api.example.com'，不是 string
```

### 5. 文档注释
```typescript
/**
 * 计算两个数的和
 * @param a - 第一个数
 * @param b - 第二个数
 * @returns 两数之和
 * @example
 * ```ts
 * add(1, 2) // 3
 * ```
 */
function add(a: number, b: number): number {
  return a + b;
}
```

## 常见问题

### 问题：类型 'X' 不能赋值给类型 'Y'
- 检查类型定义是否匹配
- 使用类型守卫验证
- 考虑使用联合类型

### 问题：对象可能为 null
- 使用可选链：`obj?.property`
- 使用空值合并：`value ?? defaultValue`
- 添加类型守卫

### 问题：类型过于宽泛
- 使用更具体的类型
- 使用字面量类型
- 使用 const assertions
