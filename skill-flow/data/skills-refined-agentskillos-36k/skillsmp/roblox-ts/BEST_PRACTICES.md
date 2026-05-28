# Roblox-TS Best Practices

Project structure, performance, and debugging recommendations.

## Project Structure

**Feature-based organization:**
```
src/
├── server/
│   ├── features/
│   │   ├── combat/
│   │   ├── inventory/
│   │   └── progression/
│   └── services/
├── client/
│   ├── features/
│   │   ├── ui/
│   │   └── input/
│   └── controllers/
└── shared/
    ├── types/
    ├── constants/
    └── utils/
```

## Type Safety

1. **Enable strict mode** in tsconfig.json
2. **Avoid `any`** - use `unknown` and type guards
3. **Type function parameters and returns**
4. **Use interfaces for data structures**
5. **Leverage union types** for state

## Performance

1. **Use Maps over objects** for dictionaries
2. **Prefer const over let** when possible
3. **Avoid unnecessary promises** for sync operations
4. **Use production builds** for deployment
5. **Profile with microprofiler**

## Code Organization

1. **One export per file** for clarity
2. **Group related code** in features
3. **Separate server/client/shared** strictly
4. **Use barrel exports** (index.ts) sparingly
5. **Keep functions small** and focused

## Error Handling

```typescript
// Always catch promise rejections
fetchData().catch(err => warn("Error:", err));

// Use pcall for Roblox API calls
const [success, result] = pcall(() => {
    return dataStore.GetAsync(key);
});

// Type error results
type Result<T> = { success: true; value: T } | { success: false; error: string };
```

## Debugging

1. **Use `print()` for basic logging**
2. **Leverage TypeScript source maps**
3. **Test incrementally** with watch mode
4. **Use verbose mode** for compiler issues
5. **Check browser console** for client errors

## Common Pitfalls

**Array indexing:**
```typescript
// ❌ Lua style (1-indexed)
const first = arr[1];

// ✅ TypeScript style (0-indexed)
const first = arr[0];
```

**Dictionaries:**
```typescript
// ❌ Don't use objects for dynamic keys
const scores: { [key: string]: number } = {};

// ✅ Use Map
const scores = new Map<string, number>();
```

**Type assertions:**
```typescript
// ❌ Unsafe casting
const part = workspace.FindFirstChild("Part") as Part;

// ✅ Type guard
const part = workspace.FindFirstChild("Part");
if (part && classIs(part, "Part")) {
    // Safe to use
}
```

## Testing Recommendations

1. Test in Studio frequently
2. Test with multiple players
3. Test client and server separately
4. Use print statements liberally
5. Check output for warnings

## Git Workflow

1. Commit package-lock.json
2. Gitignore out/ directory
3. Gitignore *.lua files
4. Use meaningful commit messages
5. Branch for features
