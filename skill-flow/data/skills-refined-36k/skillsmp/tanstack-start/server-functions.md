# Server Functions Reference

## Environment Functions

Functions that adapt behavior based on runtime environment.

### Isomorphic Functions

Execute different logic on client vs server:

```tsx
import { createIsomorphicFn } from '@tanstack/react-start';

const getStorageValue = createIsomorphicFn()
  .server(() => {
    // Server: read from database or env
    return process.env.FEATURE_FLAG;
  })
  .client(() => {
    // Client: read from localStorage
    return localStorage.getItem('featureFlag');
  });

const value = getStorageValue(); // Works in both environments
```

### Server-Only Functions

Throw an error if called on the client:

```tsx
import { createServerOnlyFn } from '@tanstack/react-start';

const readSecretConfig = createServerOnlyFn(() => {
  return process.env.SECRET_API_KEY;
});
```

### Client-Only Functions

Throw an error if called on the server:

```tsx
import { createClientOnlyFn } from '@tanstack/react-start';

const getGeolocation = createClientOnlyFn(() => {
  return navigator.geolocation.getCurrentPosition();
});
```

**Tree shaking:** Code inside `.client()` blocks is removed from server bundles and vice versa.

## Middleware Chain

```tsx
import { createServerFn, createMiddleware } from '@tanstack/react-start';

const authMiddleware = createMiddleware().server(async ({ next, request }) => {
  const session = await auth.api.getSession({ headers: request.headers });

  if (!session) {
    throw new Error('Unauthorized');
  }

  return next({ context: { user: session.user } });
});

const logMiddleware = createMiddleware().server(async ({ next, request }) => {
  const start = Date.now();
  const result = await next();
  console.log(`${request.method} ${request.url} - ${Date.now() - start}ms`);
  return result;
});

const getProtectedData = createServerFn({ method: 'GET' })
  .middleware([logMiddleware, authMiddleware])
  .handler(async ({ context }) => {
    // context.user available from authMiddleware
    return await fetchUserData(context.user.id);
  });
```

## Middleware Composition

Chain middleware together using the `.middleware()` method:

```tsx
import { createMiddleware } from '@tanstack/react-start';

const authMiddleware = createMiddleware().server(async ({ next, request }) => {
  const session = await auth.api.getSession({ headers: request.headers });
  if (!session) throw new Error('Unauthorized');
  return next({ context: { user: session.user } });
});

const adminMiddleware = createMiddleware()
  .middleware([authMiddleware])
  .server(async ({ next, context }) => {
    if (context.user.role !== 'admin') {
      throw new Error('Admin access required');
    }
    return next({ context: { isAdmin: true } });
  });

const adminAction = createServerFn({ method: 'POST' })
  .middleware([adminMiddleware])
  .handler(async ({ context }) => {
    // context.user and context.isAdmin available from middleware chain
    return await performAdminAction(context.user.id);
  });
```

## beforeLoad Alternative

For client-side auth checks (runs before route loads):

```tsx
export const Route = createFileRoute('/_app')({
  component: AppLayout,
  beforeLoad: async () => {
    const session = await getSession();
    if (!session) throw redirect({ to: '/login' });
    return { user: session.user };
  },
});
```

## Function-Level Middleware Type

Use `type: 'function'` for middleware specific to server functions:

```tsx
import { createMiddleware } from '@tanstack/react-start';
import { zodValidator } from '@tanstack/zod-adapter';

const workspaceMiddleware = createMiddleware({ type: 'function' })
  .inputValidator(zodValidator(z.object({ workspaceId: z.string() })))
  .server(async ({ next, data }) => {
    const workspace = await db.query.workspaces.findFirst({
      where: eq(workspaces.id, data.workspaceId),
    });

    if (!workspace) throw new Error('Workspace not found');

    return next({ context: { workspace } });
  });

const getWorkspaceData = createServerFn({ method: 'GET' })
  .middleware([authMiddleware, workspaceMiddleware])
  .handler(async ({ context }) => {
    return await fetchWorkspaceData(context.workspace.id);
  });
```

## Error Handling

```tsx
import { createServerFn } from '@tanstack/react-start';

class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public status: number = 400,
  ) {
    super(message);
    this.name = 'AppError';
  }
}

const createPost = createServerFn({ method: 'POST' })
  .inputValidator(
    z.object({
      title: z.string().min(1),
      body: z.string().min(10),
    }),
  )
  .handler(async ({ data }) => {
    try {
      const [post] = await db.insert(posts).values(data).returning();
      return { success: true, post };
    } catch (error) {
      if (error instanceof AppError) {
        throw error;
      }
      console.error('Failed to create post:', error);
      throw new AppError('Failed to create post', 'CREATE_FAILED', 500);
    }
  });

function CreatePostForm() {
  const handleSubmit = async (data: FormData) => {
    try {
      const result = await createPost({ data });
      toast.success('Post created!');
    } catch (error) {
      if (error instanceof Error) {
        toast.error(error.message);
      }
    }
  };
}
```

## Response Headers and Cookies

```tsx
const setTheme = createServerFn({ method: 'POST' })
  .inputValidator(z.object({ theme: z.enum(['light', 'dark']) }))
  .handler(async ({ data, request }) => {
    const response = new Response(JSON.stringify({ success: true }), {
      headers: {
        'Set-Cookie': `theme=${data.theme}; Path=/; HttpOnly; SameSite=Lax`,
        'Content-Type': 'application/json',
      },
    });

    return response;
  });

const getTheme = createServerFn({ method: 'GET' }).handler(
  async ({ request }) => {
    const cookies = request.headers.get('cookie') || '';
    const theme = cookies.match(/theme=(\w+)/)?.[1] || 'light';
    return { theme };
  },
);
```

## File Uploads

```tsx
const uploadFile = createServerFn({ method: 'POST' }).handler(
  async ({ request }) => {
    const formData = await request.formData();
    const file = formData.get('file') as File;

    if (!file) {
      throw new Error('No file provided');
    }

    const maxSize = 5 * 1024 * 1024;
    if (file.size > maxSize) {
      throw new Error('File too large');
    }

    const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
    if (!allowedTypes.includes(file.type)) {
      throw new Error('Invalid file type');
    }

    const buffer = await file.arrayBuffer();
    const filename = `${Date.now()}-${file.name}`;

    await writeFile(`./uploads/${filename}`, Buffer.from(buffer));

    return { filename, size: file.size };
  },
);

function UploadForm() {
  const handleUpload = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);

    const result = await uploadFile({ data: formData });
    console.log('Uploaded:', result.filename);
  };

  return (
    <form onSubmit={handleUpload}>
      <input type="file" name="file" accept="image/*" />
      <button type="submit">Upload</button>
    </form>
  );
}
```
