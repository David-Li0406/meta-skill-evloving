---
name: react-component-patterns
description: Use this skill when building scalable and maintainable React components using modern patterns and composition techniques.
---

# React Component Patterns

## **Priority: P0 (CRITICAL)**

Standards for building scalable, maintainable React components.

## Implementation Guidelines

- **Function Components**: Only hooks. No class components.
- **Composition**: Use `children` prop. Avoid inheritance and prop drilling.
- **Props**: Explicit TypeScript interfaces. Destructure in parameters.
- **Boolean Props**: Use shorthand `<Cmp isVisible />` instead of `isVisible={true}`.
- **Imports**: Group imports as follows: Built-in → External → Internal → Styles.
- **Error Boundaries**: Wrap app/features with `react-error-boundary`.
- **Size**: Keep components small (< 250 lines). One component per file.
- **Naming**: Use `PascalCase` for components and `use*` for hooks.
- **Exports**: Use named exports only.
- **Conditionals**: Prefer ternary (`Cond ? <A/> : <B/>`) over `&&` for rendering consistency.
- **Hoisting**: Extract static JSX/Objects outside components to prevent recreation.

## Anti-Patterns

- **No Classes**: Use hooks instead.
- **No Nested Definitions**: Define components at the top level.
- **No Inline Handlers**: Define event handlers before the return statement.
- **No Index Keys**: Use stable IDs for list items.
- **No Deep Nesting**: Limit nesting to a maximum of 3 levels.

## Code Examples

```tsx
// Composition Example
export function Layout({ children, aside }: { children: ReactNode; aside: ReactNode }) {
  return (
    <div className='grid'>
      <aside>{aside}</aside>
      <main>{children}</main>
    </div>
  );
}

// Compound Component Example
export function Select({ children }: { children: ReactNode }) {
  return <select>{children}</select>;
}
Select.Option = ({ val, children }: { val: string; children: ReactNode }) => <option value={val}>{children}</option>;
```

## Reference & Examples

For advanced patterns (HOCs, Render Props, Compound Components), see [references/patterns.md](references/patterns.md).

## Related Topics

hooks | state-management | performance | react/hooks | styling