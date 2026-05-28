---
name: frontend-patterns
description: |
  このスキルは、ユーザーが「React」「コンポーネント」「フック」「状態管理」「フロントエンド」「UI」について質問したとき、またはフロントエンドパターンを実装する必要があるときに使用する。
---

# Frontend Patterns

## コンポーネント設計

### コンポジションパターン

```typescript
// 合成可能なコンポーネント
function Card({ children }: { children: React.ReactNode }) {
  return <div className="card">{children}</div>;
}

function CardHeader({ children }: { children: React.ReactNode }) {
  return <div className="card-header">{children}</div>;
}

function CardBody({ children }: { children: React.ReactNode }) {
  return <div className="card-body">{children}</div>;
}

// 使用例
<Card>
  <CardHeader>タイトル</CardHeader>
  <CardBody>コンテンツ</CardBody>
</Card>;
```

### Props 設計

```typescript
// 明確な Props 型定義
interface ButtonProps {
  variant: "primary" | "secondary" | "danger";
  size: "sm" | "md" | "lg";
  disabled?: boolean;
  loading?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}
```

## カスタムフック

### データフェッチフック

```typescript
function useQuery<T>(fetcher: () => Promise<T>) {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    fetcher()
      .then((result) => {
        if (!cancelled) setData(result);
      })
      .catch((err) => {
        if (!cancelled) setError(err);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, []);

  return { data, error, loading };
}
```

### フォームフック

```typescript
function useForm<T>(initialValues: T) {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});

  const handleChange = (name: keyof T, value: T[keyof T]) => {
    setValues((prev) => ({ ...prev, [name]: value }));
  };

  const reset = () => setValues(initialValues);

  return { values, errors, handleChange, setErrors, reset };
}
```

## useEffect の代替

### Server Components（推奨）

```typescript
// app/users/page.tsx
async function UsersPage() {
  const users = await fetchUsers(); // サーバーサイドで実行

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

### イベントハンドラー

```typescript
// useEffect の代わりにイベントハンドラーを使用
function SearchForm() {
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    const results = await search(query);
    setResults(results);
  };

  return <form onSubmit={handleSubmit}>...</form>;
}
```

### データフェッチライブラリ

```typescript
// useSWR
import useSWR from "swr";

function UserProfile({ id }: { id: string }) {
  const { data, error, isLoading } = useSWR(`/api/users/${id}`, fetcher);

  if (isLoading) return <Loading />;
  if (error) return <Error error={error} />;
  return <Profile user={data} />;
}
```

## 状態管理

### Zustand（推奨）

```typescript
import { create } from "zustand";

interface AuthState {
  user: User | null;
  login: (user: User) => void;
  logout: () => void;
}

const useAuthStore = create<AuthState>((set) => ({
  user: null,
  login: (user) => set({ user }),
  logout: () => set({ user: null }),
}));
```

## パフォーマンス最適化

### React.memo

```typescript
const ExpensiveComponent = React.memo(function ExpensiveComponent({
  data,
}: {
  data: Data;
}) {
  return <div>{/* 重い処理 */}</div>;
});
```

### useMemo / useCallback

```typescript
// 計算結果のメモ化
const sortedItems = useMemo(() => items.sort((a, b) => a.name.localeCompare(b.name)), [items]);

// コールバックのメモ化
const handleClick = useCallback(() => {
  doSomething(id);
}, [id]);
```

## フォーム実装

### react-hook-form + zod

```typescript
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(schema),
  });

  return <form onSubmit={handleSubmit(onSubmit)}>...</form>;
}
```
