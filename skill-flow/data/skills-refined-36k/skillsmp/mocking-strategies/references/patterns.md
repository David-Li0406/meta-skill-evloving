# Mocking Strategies - Implementation Patterns

Implementation patterns for mocking in React web tests.

## Pattern: Mock React Query

Mock queries and mutations.

✅ **Good:**
\`\`\`typescript
import { useQuery } from 'react-query';

jest.mock('react-query');

(useQuery as jest.Mock).mockReturnValue({
  data: mockData,
  isLoading: false,
  error: null,
});
\`\`\`

❌ **Bad:**
\`\`\`typescript
// No mocking - real API calls in tests
\`\`\`

**Why:** Mocking:
- Predictable tests
- No API dependencies
- Faster tests
- Test error states

## Pattern: Use MockedProvider for Apollo

Mock GraphQL queries.

✅ **Good:**
\`\`\`typescript
const mocks = [
  {
    request: { query: GET_USER, variables: { id: '1' } },
    result: { data: { user: { name: 'John' } } },
  },
];

<MockedProvider mocks={mocks}>
  <Component />
</MockedProvider>
\`\`\`

**Why:** MockedProvider:
- Test GraphQL components
- Mock responses
- Test loading states
- Test errors

## Pattern: Mock Router

Mock navigation.

✅ **Good:**
\`\`\`typescript
const mockPush = jest.fn();

jest.mock('@/libs/router', () => ({
  useRouter: () => ({
    push: mockPush,
    pathname: '/test',
  }),
}));
\`\`\`

**Why:** Router mocking:
- Test navigation
- Verify redirects
- No actual navigation

## Summary

**Key Patterns:**
- Mock React Query
- Use MockedProvider for Apollo
- Mock router
- Mock fetch/axios
- Mock custom hooks

**Anti-Patterns to Avoid:**
- Real API calls in tests
- No mocking
- Incomplete mocks
