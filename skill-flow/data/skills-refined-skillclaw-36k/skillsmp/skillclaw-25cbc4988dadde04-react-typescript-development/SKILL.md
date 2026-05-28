---
name: react-typescript-development
description: Use this skill when developing React components, managing state, or optimizing performance with TypeScript, Ant Design, and Tauri.
---

# Skill body

## Overview
This skill provides guidance for developing React components using TypeScript, Ant Design, and Tauri, focusing on best practices for performance and type safety.

## Applicable Areas
- React component and Hooks development
- Ant Design forms and interactions
- Tauri frontend command calls and error handling

## Critical Rules
- Use only the `commands` from `frontend/src/bindings.ts`.
- Avoid `console.*`; use `message.info/warning/error` instead.
- Do not use `as any`; prefer type guards or precise types.
- Call Hooks only at the top level with complete dependencies.
- Maintain consistent table row heights: default th/td padding 6px 10px, line-height 1.2; compact tags within tables.

## Quick Templates

### Command Call (Result + ApiResponse)
```typescript
import { commands } from '../bindings';
import { message } from 'antd';

export async function loadFactories(keyword: string | null) {
  const res = await commands.getAllFactories(keyword, null);
  if (res.status === 'error') {
    message.error(String(res.error));
    return [] as const;
  }
  const { success, data, error } = res.data;
  if (!success || !data) {
    message.error(error ?? '加载失败');
    return [] as const;
  }
  return data;
}
```

### Hook Pattern
```typescript
import { useEffect, useState } from 'react';
import type { Factory } from '../bindings';

export function useFactoryList(keyword: string | null) {
  const [items, setItems] = useState<Factory[]>([]);
  useEffect(() => {
    void loadFactories(keyword).then(setItems);
  }, [keyword]);
  return items;
}
```

## Performance Recommendations
- Use `useMemo` for complex calculations.
- Use `useCallback` to maintain stable references for callbacks.
- Implement virtual scrolling for large lists using `react-window`.

## Form Validation
- Use AntD `Form.Item` rules and custom validation functions.
- Provide immediate feedback for errors to users.

## Checklist
- [ ] No `console.*` or `as any`.
- [ ] Command calls utilize `commands`.
- [ ] Hooks rules and dependencies are correct.
- [ ] Large lists consider virtual scrolling.
- [ ] Table row heights and padding are consistent.