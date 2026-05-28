---
name: testing-patterns
description: Jest testing patterns, React Testing Library best practices, and API testing with Supertest. Use for writing tests, improving coverage, and test architecture decisions.
allowed-tools: Read, Write, Edit, Bash(pnpm:*)
---

# Testing Patterns for PMS

## Test Organization

```
tests/
├── setup/
│   ├── jest.setup.ts           # Global setup
│   ├── test-utils.tsx          # Custom render utilities
│   └── mocks/
│       ├── handlers.ts         # MSW handlers
│       └── server.ts           # MSW server
├── factories/
│   ├── user.factory.ts
│   ├── project.factory.ts
│   └── task.factory.ts
├── fixtures/
│   ├── users.json
│   └── projects.json
└── helpers/
    ├── auth.helper.ts
    └── db.helper.ts
```

## Test Utilities

### Custom Render with Providers
```tsx
// tests/setup/test-utils.tsx
import { render, RenderOptions } from '@testing-library/react';
import { Provider } from 'react-redux';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';
import { configureStore } from '@reduxjs/toolkit';
import { rootReducer } from '../../src/store';

interface ExtendedRenderOptions extends Omit<RenderOptions, 'wrapper'> {
  preloadedState?: Partial<RootState>;
  store?: ReturnType<typeof configureStore>;
}

export function renderWithProviders(
  ui: React.ReactElement,
  {
    preloadedState = {},
    store = configureStore({
      reducer: rootReducer,
      preloadedState,
    }),
    ...renderOptions
  }: ExtendedRenderOptions = {}
) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });

  function Wrapper({ children }: { children: React.ReactNode }) {
    return (
      <Provider store={store}>
        <QueryClientProvider client={queryClient}>
          <BrowserRouter>{children}</BrowserRouter>
        </QueryClientProvider>
      </Provider>
    );
  }

  return {
    store,
    queryClient,
    ...render(ui, { wrapper: Wrapper, ...renderOptions }),
  };
}

export * from '@testing-library/react';
export { renderWithProviders as render };
```

### Test Factories
```typescript
// tests/factories/project.factory.ts
import { faker } from '@faker-js/faker';
import { IProject } from '../../src/types';

export const createProject = (overrides: Partial<IProject> = {}): IProject => ({
  _id: faker.database.mongodbObjectId(),
  name: faker.company.name(),
  description: faker.lorem.paragraph(),
  key: faker.string.alpha({ length: 4, casing: 'upper' }),
  ownerId: faker.database.mongodbObjectId(),
  members: [],
  status: 'active',
  visibility: 'team',
  settings: {
    defaultTaskStatus: 'todo',
    allowSubtasks: true,
    timeTrackingEnabled: false,
  },
  metadata: {
    taskCount: 0,
    completedTaskCount: 0,
    memberCount: 1,
  },
  createdAt: faker.date.recent(),
  updatedAt: faker.date.recent(),
  ...overrides,
});

export const createProjects = (count: number): IProject[] =>
  Array.from({ length: count }, () => createProject());
```

### MSW Handlers
```typescript
// tests/setup/mocks/handlers.ts
import { rest } from 'msw';
import { createProject } from '../../factories/project.factory';

export const handlers = [
  // List projects
  rest.get('/api/v1/projects', (req, res, ctx) => {
    const projects = createProjects(5);
    return res(
      ctx.json({
        success: true,
        data: projects,
        meta: { page: 1, limit: 20, total: 5 },
      })
    );
  }),

  // Get single project
  rest.get('/api/v1/projects/:id', (req, res, ctx) => {
    const project = createProject({ _id: req.params.id as string });
    return res(ctx.json({ success: true, data: project }));
  }),

  // Error scenario
  rest.get('/api/v1/projects/error', (req, res, ctx) => {
    return res(
      ctx.status(500),
      ctx.json({
        success: false,
        error: { code: 'INTERNAL_ERROR', message: 'Server error' },
      })
    );
  }),
];
```

## Component Testing Examples

### Testing User Interactions
```tsx
import { render, screen, waitFor } from '../setup/test-utils';
import userEvent from '@testing-library/user-event';
import { CreateTaskForm } from '../../src/components/CreateTaskForm';

describe('CreateTaskForm', () => {
  const user = userEvent.setup();
  const mockOnSubmit = jest.fn();

  beforeEach(() => {
    mockOnSubmit.mockClear();
  });

  it('submits form with valid data', async () => {
    render(<CreateTaskForm onSubmit={mockOnSubmit} projectId="123" />);

    // Fill form
    await user.type(screen.getByLabelText(/title/i), 'New Task');
    await user.type(screen.getByLabelText(/description/i), 'Task description');
    await user.selectOptions(screen.getByLabelText(/priority/i), 'high');

    // Submit
    await user.click(screen.getByRole('button', { name: /create/i }));

    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith({
        title: 'New Task',
        description: 'Task description',
        priority: 'high',
        projectId: '123',
      });
    });
  });

  it('shows validation errors for empty title', async () => {
    render(<CreateTaskForm onSubmit={mockOnSubmit} projectId="123" />);

    await user.click(screen.getByRole('button', { name: /create/i }));

    expect(await screen.findByText(/title is required/i)).toBeInTheDocument();
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });
});
```

## API Testing Examples

### Testing Endpoints
```typescript
import request from 'supertest';
import { app } from '../../src/app';
import { Project } from '../../src/models/project.model';
import { User } from '../../src/models/user.model';
import { generateToken } from '../helpers/auth.helper';
import { connectDB, clearDB, closeDB } from '../helpers/db.helper';

describe('Project API', () => {
  let authToken: string;
  let testUser: any;

  beforeAll(async () => {
    await connectDB();
  });

  afterAll(async () => {
    await closeDB();
  });

  beforeEach(async () => {
    await clearDB();
    testUser = await User.create({
      name: 'Test User',
      email: 'test@example.com',
      password: 'hashedpassword',
    });
    authToken = generateToken(testUser._id);
  });

  describe('POST /api/v1/projects', () => {
    const validProject = {
      name: 'Test Project',
      key: 'TEST',
      description: 'A test project',
    };

    it('creates project with valid data', async () => {
      const res = await request(app)
        .post('/api/v1/projects')
        .set('Authorization', `Bearer ${authToken}`)
        .send(validProject)
        .expect(201);

      expect(res.body.success).toBe(true);
      expect(res.body.data.name).toBe(validProject.name);
      expect(res.body.data.ownerId).toBe(testUser._id.toString());
    });

    it('returns 401 without auth token', async () => {
      await request(app)
        .post('/api/v1/projects')
        .send(validProject)
        .expect(401);
    });
  });
});
```
