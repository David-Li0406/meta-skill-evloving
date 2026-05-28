# Development Utilities

Commands, tools, and debugging guides.

## Essential Commands

### Development
```bash
# Start dev server
npm run dev

# Run linter
npm run lint

# Fix lint issues
npm run lint -- --fix

# Type check (without building)
npm run prebuild

# Build production
npm run build

# Clear Next.js cache
rm -rf .next
```

### Git
```bash
# Check status
git status

# View changes
git diff

# View staged changes
git diff --staged

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Stash changes
git stash
git stash pop
```

### Database
```bash
# Connect to MongoDB
mongosh "$DATABASE_URL"

# Quick query
mongosh "$DATABASE_URL" --eval "
db['collection'].find({}).limit(5).forEach(printjson);
"

# Count documents
mongosh "$DATABASE_URL" --eval "
print(db['collection'].countDocuments());
"
```

## Debugging Tools

### 1. React DevTools
- Install browser extension
- Inspect component tree
- View props and state
- Profile performance

### 2. React Query DevTools
- Included in dev mode automatically
- View cache state
- Inspect queries and mutations
- Manual refetch/invalidate

### 3. Network Tab
- Monitor API calls
- Check request/response payloads
- Identify slow requests

### 4. MongoDB Compass
- Visual database explorer
- Run queries with GUI
- View indexes and schema

### 5. VS Code Debugger
- Set breakpoints in code
- Step through execution
- Inspect variables

## Common Debug Scenarios

### Server Action Not Working

1. **Check the action is called**
   ```typescript
   console.log("Action called with:", input);
   ```

2. **Check database connection**
   ```typescript
   return withDbConnection(async () => {
     console.log("DB connected");
     // ...
   });
   ```

3. **Check the response**
   ```typescript
   const result = await myAction(input);
   console.log("Result:", result);
   ```

### React Query Not Updating

1. **Check query key matches**
   ```typescript
   // These must match exactly
   queryKey: ["myFeature", id]
   invalidateQueries({ queryKey: ["myFeature", id] })
   ```

2. **Check enabled condition**
   ```typescript
   enabled: !!id && !!userId  // Must be true to run
   ```

3. **Force refetch**
   ```typescript
   const { refetch } = useMyQuery(id);
   await refetch();
   ```

### Component Not Re-rendering

1. **Check state is actually changing**
   ```typescript
   useEffect(() => {
     console.log("State changed:", value);
   }, [value]);
   ```

2. **Check for reference equality issues**
   ```typescript
   // Bad - creates new object each render
   const options = { foo: "bar" };

   // Good - memoized
   const options = useMemo(() => ({ foo: "bar" }), []);
   ```

### TypeScript Errors

1. **Check imports**
   - Ensure path aliases are correct
   - Check for typos in import paths

2. **Check types match**
   ```typescript
   // Zod infers type
   type MyType = z.infer<typeof MySchema>;
   ```

3. **Use type assertions sparingly**
   ```typescript
   const data = result as MyType;  // Only when necessary
   ```

## Performance Tips

### 1. Memoize Expensive Components
```typescript
const MemoizedComponent = React.memo(ExpensiveComponent);
```

### 2. Use React Query Caching
```typescript
useQuery({
  queryKey: ["data", id],
  queryFn: fetchData,
  staleTime: 5 * 60 * 1000, // 5 minutes
});
```

### 3. Lazy Load Components
```typescript
const HeavyComponent = dynamic(() => import("./HeavyComponent"), {
  loading: () => <Skeleton />,
});
```

### 4. Optimize Database Queries
```typescript
// Only fetch needed fields
const result = await Model.find({}).select("name email").lean();
```

## Code Quality Checklist

Before pushing code:

- [ ] `npm run lint` passes
- [ ] `npm run prebuild` passes
- [ ] No `console.log` statements
- [ ] No `any` types (use `unknown` + type guards)
- [ ] Error states handled
- [ ] Loading states handled
- [ ] Responsive design checked
