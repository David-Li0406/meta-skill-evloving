# Mocking Strategies - Production Examples

Real-world mocking examples for React web testing.

## Example 1: Mock React Query

\`\`\`typescript
// __mocks__/react-query.ts
export const useQuery = jest.fn();
export const useMutation = jest.fn();
export const QueryClient = jest.fn(() => ({
  clear: jest.fn(),
}));

// In test
import { useQuery } from 'react-query';

(useQuery as jest.Mock).mockReturnValue({
  data: { user: { id: '1', name: 'John' } },
  isLoading: false,
  error: null,
});
\`\`\`

## Example 2: Mock Apollo Client

\`\`\`typescript
import { MockedProvider } from '@apollo/client/testing';

const mocks = [
  {
    request: {
      query: GET_USER,
      variables: { id: '1' },
    },
    result: {
      data: {
        user: { id: '1', name: 'John' },
      },
    },
  },
];

render(
  <MockedProvider mocks={mocks} addTypename={false}>
    <UserComponent />
  </MockedProvider>
);
\`\`\`

## Example 3: Mock Next.js Router

\`\`\`typescript
// __mocks__/@/libs/router.ts
export const useRouter = jest.fn(() => ({
  push: jest.fn(),
  replace: jest.fn(),
  pathname: '/',
  query: {},
  asPath: '/',
}));
\`\`\`

## Example 4: Mock Fetch

\`\`\`typescript
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    json: async () => ({ data: 'test' }),
  })
) as jest.Mock;
\`\`\`
