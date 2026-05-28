# React Best Practices
- React 18+: prefer function components with hooks; avoid legacy lifecycles.
- Data fetching: use react-query or SWR for server state; keep fetch logic in hooks/services.
- State: keep local UI state in components; lift shared state; avoid prop drilling via context or state library when needed.
- Components: PascalCase; colocate component with styles/tests; avoid default exports when component naming matters.
- Props: destructure props; document required vs optional; avoid spreading untrusted props.
- Error boundaries: place at feature or page level; provide user-friendly fallback.
- Routing: lazy-load large routes; code-split where beneficial.
- Testing: use React Testing Library; prefer user-centric assertions; mock network with msw.
