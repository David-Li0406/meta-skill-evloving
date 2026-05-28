---
name: tanstack-types
description: Use this skill when you need guidance on achieving type safety with TanStack Query, including type-safe query options, runtime validation with Zod, and TypeScript best practices.
---

# TanStack Query Type Safety Patterns

This skill provides guidance for achieving type safety in TanStack Query, covering query options, runtime validation with Zod, and TypeScript best practices based on TKDodo's recommendations.

## Core Principle: Trust in Types

The foundation of type safety is **trust in type definitions**. Without trust, TypeScript becomes just a linter that can be silenced.

> "To truly leverage the power of TypeScript, there is one thing that you need above all: Trust."

## The Anti-Pattern: Manual Generics

Avoid passing type parameters directly to `useQuery`:

```typescript
// BAD: Manual generics
const { data } = useQuery<Todo>({
  queryKey: ['todos', id],
  queryFn: () => fetchTodo(id),
});
// data is Todo | undefined, but is it really?
// The generic is just a type assertion in disguise
```

This violates the "golden rule of generics": **For a generic to be useful, it must appear at least twice.**

## The Pattern: Type the Data Source

Instead of typing the consumer, type the source:

```typescript
// GOOD: Type the queryFn return
const fetchTodo = async (id: string): Promise<Todo> => {
  const response = await axios.get(`/todos/${id}`);
  return response.data;
};

// Types flow through automatically
const { data } = useQuery({
  queryKey: ['todos', id],
  queryFn: () => fetchTodo(id),
});
// data is Todo | undefined, and we can trust it
```

## The queryOptions Helper

The `queryOptions()` helper provides compile-time type safety:

```typescript
import { queryOptions, useQuery } from '@tanstack/react-query';

const todoQueryOptions = (id: string) => queryOptions({
  queryKey: ['todos', id] as const,
  queryFn: async (): Promise<Todo> => {
    const response = await api.get(`/todos/${id}`);
    return response.data;
  },
  staleTime: 5 * 60 * 1000,
});

// Usage - types are inferred correctly
const { data } = useQuery(todoQueryOptions(id));
// data: Todo | undefined

// TypeScript catches property typos
const bad = queryOptions({
  queryKey: ['todos'],
  queryFn: fetchTodos,
  stallTime: 5000, // Error! Did you mean 'staleTime'?
});
```