---
name: react-best-practices
description: React best practices e frameworks modernos
triggers: [react, nextjs, vite, typescript, jsx, component]
sources:
  - https://github.com/vitejs/vite
  - https://github.com/vercel/next.js
  - https://github.com/react-boilerplate/react-boilerplate
---

# React Best Practices

**Convenções para React com frameworks modernos.**

---

## Framework Recomendado

### Next.js (Fullstack com SSR/SSG)

**Para projetos que precisam de SEO, SSR ou roteamento:**

```typescript
// pages/users/[id].tsx
import { GetServerSideProps } from 'next';

export default function UserPage({ user }) {
  return <div>{user.name}</div>;
}

export const getServerSideProps: GetServerSideProps = async (context) => {
  const user = await getUser(context.params.id);
  return { props: { user } };
};
```

### Vite + React (SPA Rápida)

**Para aplicações SPA modernas:**

```typescript
// src/App.tsx
import { useState } from 'react';

function App() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

---

## Estrutura de Projeto

### Next.js

```
project/
├── pages/
│   ├── api/
│   ├── _app.tsx
│   └── index.tsx
├── components/
├── lib/
├── styles/
└── public/
```

### Vite + React

```
project/
├── src/
│   ├── components/
│   ├── hooks/
│   ├── utils/
│   ├── App.tsx
│   └── main.tsx
└── public/
```

---

## Componentes

### TypeScript

```typescript
interface UserCardProps {
  name: string;
  email: string;
  avatar?: string;
}

export const UserCard: React.FC<UserCardProps> = ({ name, email, avatar }) => {
  return (
    <div>
      {avatar && <img src={avatar} alt={name} />}
      <h3>{name}</h3>
      <p>{email}</p>
    </div>
  );
};
```

---

## Hooks Customizados

```typescript
function useUser(userId: string) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUser(userId).then(setUser).finally(() => setLoading(false));
  }, [userId]);

  return { user, loading };
}
```

---

## Checklist

- [ ] TypeScript configurado
- [ ] Componentes funcionais com hooks
- [ ] Estrutura de projeto organizada
- [ ] Next.js para SSR/SSG (quando necessário)
- [ ] Vite para SPA rápida (quando necessário)

