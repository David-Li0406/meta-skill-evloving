# [Repository Name]

## Purpose

Brief description of what this repository does and why it exists in the workspace.

## Architecture

### Tech Stack
- Framework/Language: [e.g., React 18, Node.js 20]
- State Management: [e.g., Zustand, Redux, Context API]
- Styling: [e.g., TailwindCSS, styled-components]
- Build Tool: [e.g., Vite, Webpack, esbuild]

### Key Patterns
- [Pattern 1]: Description
- [Pattern 2]: Description

### Directory Structure
```
src/
├── components/     # Reusable UI components
├── features/       # Feature-based modules
├── hooks/          # Custom React hooks
├── utils/          # Utility functions
└── types/          # TypeScript type definitions
```

## Dependencies

### Internal Dependencies
- **@workspace/shared-ui**: Shared component library
- **@workspace/api-client**: API client for backend communication

### External Critical Dependencies
- **react**: UI framework
- **react-router**: Client-side routing
- **axios**: HTTP client

## Development Guidelines

### Code Style
- Follow [Airbnb/Google/Standard] style guide
- Use [ESLint/Prettier] for formatting
- Prefer functional components with hooks

### Testing Strategy
- Unit tests: [Jest/Vitest]
- Integration tests: [Testing Library]
- E2E tests: [Playwright/Cypress]
- Target coverage: 80%+

### Common Patterns

#### Component Structure
```typescript
// Preferred pattern for components
export const MyComponent = ({ prop1, prop2 }: Props) => {
  // hooks
  // handlers
  // render
};
```

#### API Calls
```typescript
// Preferred pattern for API calls
const { data, error, isLoading } = useQuery(['key'], fetchFn);
```

## Integration Points

### Consumes From
- **backend-api**: REST API at `/api/v1`
- **auth-service**: Authentication endpoints

### Provides To
- **admin-dashboard**: Shared components via `@workspace/shared-ui`

## Known Issues & Technical Debt

- [ ] Issue 1: Description and plan to address
- [ ] Issue 2: Description and plan to address

## Recent Decisions

### [Date] - Decision Title
**Context**: Why this decision was needed
**Decision**: What was decided
**Consequences**: Impact on the codebase

## Performance Considerations

- Lazy load routes for code splitting
- Memoize expensive computations
- Use virtual scrolling for large lists

## Security Considerations

- Sanitize user inputs
- Use HTTPS only
- Implement CSRF protection
- Follow OWASP guidelines

## Future Improvements

- [ ] Improvement 1
- [ ] Improvement 2
