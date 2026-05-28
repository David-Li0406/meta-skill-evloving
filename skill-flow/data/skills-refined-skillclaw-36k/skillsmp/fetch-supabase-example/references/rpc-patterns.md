# RPC Patterns

## Parameter Handling

```typescript
// Optional parameters require special handling
p_optional_param: value ?? (null as unknown as undefined);

// Required parameters
p_required_param: value;
```

## Type Assertions

```typescript
// Always use "as unknown as" for type casting
data as unknown as Type[];

// For single items
data[0] as unknown as Type;
```

## Error Handling

```typescript
// Standard error handling pattern
if (error) {
  throw new Error(`Operation failed: ${error.message}`);
}
```

## Full Example

```typescript
// Example for posts_read RPC function

// 1. RPC Function Call
const { data, error } = await supabase.rpc("posts_read", {
  p_limit: params.limit ?? 20,
  p_offset: params.offset ?? 0,
  p_user_id: params.userId ?? (null as unknown as undefined),
});

// 2. Error Handling
if (error) {
  throw new Error(`Failed to fetch posts: ${error.message}`);
}

// 3. Type Assertion
return {
  posts: data as unknown as Post[],
  total: data.length,
};

// 4. Parameter Notes
// - p_limit: number (default: 20)
// - p_offset: number (default: 0)
// - p_user_id: string | undefined (use null as unknown as undefined for optional)

// 5. Type Definitions Needed
import type { Post } from "@/models/post.model";
```

## Available Domains

Core-supabase provides examples for:

- `posts` - Post CRUD operations
- `comments` - Comment operations
- `users` - User profile operations
- `activities` - User activity tracking
- (Check `document/test/` for full list)

## GitHub CLI Commands

```bash
# List available test examples
gh api repos/semicolon-devteam/core-supabase/contents/document/test

# Fetch specific domain example
gh api repos/semicolon-devteam/core-supabase/contents/document/test/posts/createPost.ts \
  --jq '.content' | base64 -d

# Fetch RPC function definition
gh api repos/semicolon-devteam/core-supabase/contents/docker/volumes/db/init/functions/05-posts
```

## Critical Rules

1. **Always use RPC functions**: Never write raw SQL in Repository
2. **Follow parameter naming**: Use `p_` prefix for all RPC parameters
3. **Type assertion pattern**: Always `as unknown as Type`
4. **Error handling**: Always check error before using data
5. **Optional parameters**: Use `null as unknown as undefined`
