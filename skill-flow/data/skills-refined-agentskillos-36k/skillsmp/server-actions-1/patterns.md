# Server Action Patterns & Best Practices

## Table of Contents

1. [File Organization](#file-organization)
2. [Error Handling Patterns](#error-handling-patterns)
3. [Database Operation Patterns](#database-operation-patterns)
4. [Logging Patterns](#logging-patterns)
5. [Cache Revalidation](#cache-revalidation)
6. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
7. [Security Best Practices](#security-best-practices)
8. [Performance Considerations](#performance-considerations)

---

## File Organization

### Recommended Structure

```text
features/
  users/
    server/
      actions/           # Server actions
        create-user.ts
        update-user.ts
        delete-user.ts
        index.ts         # Re-exports
      db/                # Database queries
        users.ts
    schemas/             # Zod validation schemas
      user.ts
    types/               # TypeScript types
      user.ts
    components/          # UI components
      user-form.tsx
```

### Action File Naming

- Use kebab-case: `create-user.ts`, `update-profile.ts`
- Name should describe the action: `submit-preferences.ts`, `complete-onboarding.ts`
- Group related actions: `manage-users.ts` for admin operations

### Index Re-exports

```typescript
// features/users/server/actions/index.ts
export { createUser } from "./create-user";
export { updateUser } from "./update-user";
export { deleteUser } from "./delete-user";

// Usage in components
import { createUser, updateUser } from "~/features/users/server/actions";
```

---

## Error Handling Patterns

### Tuple Pattern for Database Operations

The tuple pattern `[error, data]` provides explicit error handling:

```typescript
// Database function
export async function getUserById(id: string): Promise<[DbError | null, User | null]> {
  try {
    const user = await db.collection("users").doc(id).get();
    if (!user.exists) {
      return [DbError.notFound("User"), null];
    }
    return [null, transformUser(user)];
  } catch (error) {
    return [categorizeDbError(error, "User"), null];
  }
}

// Server action usage
export async function getUser(id: string): ActionResponse<User> {
  const [error, user] = await getUserById(id);

  if (error) {
    if (error.isNotFound) {
      return { success: false, error: "User not found" };
    }
    if (error.isRetryable) {
      // Log and let client retry
      return { success: false, error: "Service temporarily unavailable" };
    }
    return { success: false, error: "Failed to fetch user" };
  }

  return { success: true, data: user };
}
```

### Error Categories

Handle different error types appropriately:

```typescript
const [error, data] = await dbOperation();

if (error) {
  // Not found - expected case, user-friendly message
  if (error.isNotFound) {
    return { success: false, error: "Resource not found" };
  }

  // Retryable - transient error, suggest retry
  if (error.isRetryable) {
    logger.warn({ error }, "Transient error, client should retry");
    return { success: false, error: "Please try again in a moment" };
  }

  // Permission denied - auth issue
  if (error.isPermissionDenied) {
    return { success: false, error: "Access denied" };
  }

  // Already exists - conflict
  if (error.isAlreadyExists) {
    return { success: false, error: "Resource already exists" };
  }

  // Unknown - log and return generic message
  logger.error({ error }, "Unexpected database error");
  return { success: false, error: "An unexpected error occurred" };
}
```

### Never Expose Internal Errors

```typescript
// ❌ Bad: Exposes internal details
return { success: false, error: error.message };
return { success: false, error: `Firestore error: ${error.code}` };

// ✅ Good: User-friendly messages
return { success: false, error: "Failed to save changes" };
return { success: false, error: "Service temporarily unavailable" };
```

---

## Database Operation Patterns

### Standard CRUD Return Types

```typescript
// CREATE - returns created entity
async function createUser(data: CreateUserDto): Promise<[DbError | null, User | null]>

// READ - returns entity or null
async function getUserById(id: string): Promise<[DbError | null, User | null]>

// UPDATE - returns updated entity
async function updateUser(id: string, data: UpdateUserDto): Promise<[DbError | null, User | null]>

// DELETE - returns void (null for data)
async function deleteUser(id: string): Promise<[DbError | null, null]>

// LIST - returns array
async function listUsers(filters?: UserFilters): Promise<[DbError | null, User[] | null]>
```

### Input Validation in Database Layer

```typescript
export async function getUserById(userId: string): Promise<[DbError | null, User | null]> {
  // Validate input before database call
  if (!userId?.trim()) {
    const error = DbError.validation("Invalid userId provided");
    logger.warn({ userId, errorCode: error.code }, "Invalid userId");
    return [error, null];
  }

  try {
    // ... database operation
  } catch (error) {
    return [categorizeDbError(error, "User"), null];
  }
}
```

### Transaction Pattern

```typescript
export async function transferFunds(
  fromAccountId: string,
  toAccountId: string,
  amount: number
): Promise<[DbError | null, TransferResult | null]> {
  const batch = db.batch();

  try {
    // Validate both accounts exist
    const [fromRef, toRef] = await Promise.all([
      db.collection("accounts").doc(fromAccountId).get(),
      db.collection("accounts").doc(toAccountId).get()
    ]);

    if (!fromRef.exists || !toRef.exists) {
      return [DbError.notFound("Account"), null];
    }

    const fromBalance = fromRef.data()!.balance;
    if (fromBalance < amount) {
      return [DbError.validation("Insufficient funds"), null];
    }

    // Batch updates
    batch.update(fromRef.ref, { balance: fromBalance - amount });
    batch.update(toRef.ref, { balance: toRef.data()!.balance + amount });

    await batch.commit();

    return [null, { fromAccountId, toAccountId, amount }];
  } catch (error) {
    return [categorizeDbError(error, "Transfer"), null];
  }
}
```

---

## Logging Patterns

### Structured Logging

Always include relevant context in logs:

```typescript
const logger = createLogger({ module: "users-actions" });

export async function createUser(data: CreateUserDto): ActionResponse<User> {
  const { userId: currentUserId } = await auth();

  // Log action start with context
  logger.info({ currentUserId, email: data.email }, "Creating user");

  const [error, user] = await createUserInDb(data);

  if (error) {
    // Log error with full context
    logger.error(
      {
        currentUserId,
        email: data.email,
        errorCode: error.code,
        isRetryable: error.isRetryable
      },
      "Failed to create user"
    );
    return { success: false, error: "Failed to create user" };
  }

  // Log success
  logger.info({ currentUserId, newUserId: user.id }, "User created successfully");

  return { success: true, data: user };
}
```

### Log Levels Guide

```typescript
// INFO: Normal operations, audit trail
logger.info({ userId, action: "login" }, "User logged in");

// WARN: Expected errors, recoverable issues
logger.warn({ userId, errorCode: "not-found" }, "User not found during lookup");

// ERROR: Unexpected failures, requires attention
logger.error({ userId, error }, "Database connection failed");

// DEBUG: Development details (not in production)
logger.debug({ query, params }, "Executing database query");
```

### Sensitive Data

Never log sensitive information:

```typescript
// ❌ Bad: Logging sensitive data
logger.info({ password, creditCard }, "Processing payment");

// ✅ Good: Redact or omit sensitive fields
logger.info({ userId, last4: creditCard.slice(-4) }, "Processing payment");
```

---

## Cache Revalidation

### Path-Based Revalidation

```typescript
import { revalidatePath } from "next/cache";

export async function updatePost(postId: string, data: UpdatePostDto): ActionResponse<Post> {
  const [error, post] = await updatePostInDb(postId, data);
  if (error) return { success: false, error: error.message };

  // Revalidate specific paths
  revalidatePath("/posts");           // List page
  revalidatePath(`/posts/${postId}`); // Detail page

  return { success: true, data: post };
}
```

### Tag-Based Revalidation

```typescript
import { revalidateTag } from "next/cache";

export async function createPost(data: CreatePostDto): ActionResponse<Post> {
  const [error, post] = await createPostInDb(data);
  if (error) return { success: false, error: error.message };

  // Revalidate all data tagged with "posts"
  revalidateTag("posts");

  return { success: true, data: post };
}
```

### Combined Revalidation

```typescript
export async function deleteCategory(categoryId: string): ActionResponse<void> {
  const [error] = await deleteCategoryFromDb(categoryId);
  if (error) return { success: false, error: error.message };

  // Revalidate multiple concerns
  revalidatePath("/categories");      // Category list
  revalidatePath("/products");        // Products may reference category
  revalidateTag("categories");        // All cached category data

  return { success: true, data: undefined };
}
```

---

## Anti-Patterns to Avoid

### 1. Missing "use server" Directive

```typescript
// ❌ Bad: No directive - won't work as server action
export async function myAction() { /* ... */ }

// ✅ Good: File-level directive
"use server";
export async function myAction() { /* ... */ }

// ✅ Good: Function-level directive (inline actions)
export async function Page() {
  async function myAction() {
    "use server";
    // ...
  }
}
```

### 2. Inconsistent Return Types

```typescript
// ❌ Bad: Inconsistent structure
if (error) return { error: error.message };
return user; // Returns raw data

// ✅ Good: Consistent ActionResponse
if (error) return { success: false, error: error.message };
return { success: true, data: user };
```

### 3. Missing Authentication

```typescript
// ❌ Bad: No auth check
export async function deleteUser(userId: string): ActionResponse<void> {
  await deleteUserFromDb(userId);
  return { success: true, data: undefined };
}

// ✅ Good: Always verify authentication
export async function deleteUser(userId: string): ActionResponse<void> {
  const { userId: currentUserId } = await auth();
  if (!currentUserId) {
    return { success: false, error: "Authentication required" };
  }
  // ... proceed with operation
}
```

### 4. Trusting Client Data

```typescript
// ❌ Bad: Using client data directly
export async function updateProfile(data: ProfileData): ActionResponse<Profile> {
  const [error, profile] = await updateProfileInDb(data);
  // ...
}

// ✅ Good: Always validate
export async function updateProfile(data: ProfileData): ActionResponse<Profile> {
  const parsed = profileSchema.safeParse(data);
  if (!parsed.success) {
    return {
      success: false,
      error: "Validation failed",
      fieldErrors: parsed.error.flatten().fieldErrors
    };
  }
  const [error, profile] = await updateProfileInDb(parsed.data);
  // ...
}
```

### 5. Forgetting to Revalidate

```typescript
// ❌ Bad: Data changes but cache is stale
export async function createPost(data: CreatePostDto): ActionResponse<Post> {
  const [error, post] = await createPostInDb(data);
  if (error) return { success: false, error: error.message };
  return { success: true, data: post }; // Cache not updated!
}

// ✅ Good: Revalidate affected paths/tags
export async function createPost(data: CreatePostDto): ActionResponse<Post> {
  const [error, post] = await createPostInDb(data);
  if (error) return { success: false, error: error.message };

  revalidatePath("/posts");
  revalidateTag("posts");

  return { success: true, data: post };
}
```

### 6. Blocking Redirects with Toast

```typescript
// ❌ Bad: Toast after redirect won't work
export async function submitForm(data: FormData): RedirectAction {
  await saveData(data);
  redirect("/success");
  await setToastCookie("Success!"); // Never reached!
}

// ✅ Good: Toast before redirect
export async function submitForm(data: FormData): RedirectAction {
  await saveData(data);
  await setToastCookie("Success!");
  redirect("/success");
}
```

---

## Security Best Practices

### 1. Always Verify Ownership

```typescript
export async function updatePost(postId: string, data: UpdatePostDto): ActionResponse<Post> {
  const { userId } = await auth();
  if (!userId) {
    return { success: false, error: "Authentication required" };
  }

  // Verify ownership before update
  const [fetchError, post] = await getPostById(postId);
  if (fetchError) {
    return { success: false, error: "Post not found" };
  }

  if (post.authorId !== userId) {
    logger.warn({ userId, postId }, "Unauthorized update attempt");
    return { success: false, error: "Not authorized to edit this post" };
  }

  // Proceed with update...
}
```

### 2. Rate Limiting

```typescript
import { rateLimit } from "~/lib/rate-limit";

export async function sendVerificationEmail(email: string): ActionResponse<void> {
  const { userId } = await auth();

  // Rate limit: 3 requests per hour per user
  const { success: allowed } = await rateLimit.check(`verify-email:${userId}`, {
    limit: 3,
    window: "1h"
  });

  if (!allowed) {
    return { success: false, error: "Too many requests. Please try again later." };
  }

  // Send email...
}
```

### 3. Input Sanitization

```typescript
import DOMPurify from "isomorphic-dompurify";

export async function createComment(data: CreateCommentDto): ActionResponse<Comment> {
  // Sanitize HTML content
  const sanitizedContent = DOMPurify.sanitize(data.content, {
    ALLOWED_TAGS: ["b", "i", "em", "strong", "a"],
    ALLOWED_ATTR: ["href"]
  });

  const [error, comment] = await createCommentInDb({
    ...data,
    content: sanitizedContent
  });

  // ...
}
```

---

## Performance Considerations

### 1. Minimize Database Calls

```typescript
// ❌ Bad: Multiple sequential calls
export async function getPostWithAuthor(postId: string) {
  const [postError, post] = await getPostById(postId);
  if (postError) return [postError, null];

  const [authorError, author] = await getUserById(post.authorId);
  if (authorError) return [authorError, null];

  return [null, { ...post, author }];
}

// ✅ Good: Single query with join or batch
export async function getPostWithAuthor(postId: string) {
  // Use database-level join or embedded data
  const [error, post] = await getPostWithAuthorById(postId);
  return [error, post];
}
```

### 2. Use Parallel Operations

```typescript
// ❌ Bad: Sequential when parallel is possible
const [userError, user] = await getUser(userId);
const [postsError, posts] = await getUserPosts(userId);
const [statsError, stats] = await getUserStats(userId);

// ✅ Good: Parallel fetching
const [userResult, postsResult, statsResult] = await Promise.all([
  getUser(userId),
  getUserPosts(userId),
  getUserStats(userId)
]);
```

### 3. Avoid Unnecessary Revalidation

```typescript
// ❌ Bad: Revalidating everything
revalidatePath("/");

// ✅ Good: Revalidate only affected paths
revalidatePath(`/posts/${postId}`);
revalidateTag(`post-${postId}`);
```

### 4. Batch Operations

```typescript
// ❌ Bad: Individual deletes
for (const id of postIds) {
  await deletePost(id);
}

// ✅ Good: Batch delete
export async function batchDeletePosts(postIds: string[]): ActionResponse<void> {
  const batch = db.batch();
  postIds.forEach(id => {
    batch.delete(db.collection("posts").doc(id));
  });
  await batch.commit();
  return { success: true, data: undefined };
}
```
