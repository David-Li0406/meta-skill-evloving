# Lint Fix Patterns

## Common Biome Issues

### 1. Template Literals (useTemplate)
```javascript
// Before
alert('Error: ' + err.message);

// After
alert(`Error: ${err.message}`);
```

### 2. Const Declarations (useConst)
```javascript
// Before
let value = 10;

// After
const value = 10;
```

### 3. Unused Variables (noUnusedVariables)
```typescript
// Remove or prefix with _
const _intentionallyUnused = value;
```

### 4. Console Statements (noConsole)
```typescript
// Development only
if (import.meta.env.DEV) {
  console.log('Debug:', data);
}
```

### 5. Any Type (noExplicitAny)
```typescript
// Use specific types or unknown
function process(data: unknown) {
  if (isData(data)) return data.value;
}
```

### 6. Non-Null Assertions (noNonNullAssertion)
```typescript
// Before
const el = document.getElementById('app')!;

// After
const el = document.getElementById('app');
if (!el) throw new Error('Element not found');
```

## File Type Patterns

### React Components (.tsx)
```typescript
interface Props {
  data: DataType;
  onUpdate: (value: string) => void;
}

export const Component = ({ data, onUpdate }: Props) => {
  return <div>...</div>;
};
```

### Edge Functions (.ts)
```typescript
interface RequestBody { field: string; }
interface ResponseData { success: boolean; data: ResultType; }

serve(async (req: Request) => {
  try {
    const body: RequestBody = await req.json();
    return new Response(JSON.stringify({ success: true, data }), { headers: corsHeaders });
  } catch (error) {
    return new Response(
      JSON.stringify({ success: false, error: error instanceof Error ? error.message : 'Unknown' }),
      { status: 500, headers: corsHeaders }
    );
  }
});
```

## Ignoring Rules

```javascript
// biome-ignore lint/style/useTemplate: Legacy code
const message = 'Error: ' + error;

// biome-ignore lint/suspicious/noExplicitAny: Third-party types
const data: any = externalLibrary.getData();
```

## Quick Reference

| Issue | Auto-fix? | Manual Review? |
|-------|-----------|----------------|
| Template literals | Yes | No |
| Const declarations | Yes | No |
| Formatting | Yes | No |
| Unused variables | Yes | Verify not needed |
| Any types | No | Add proper types |
| Console statements | No | Keep errors only |
| Non-null assertions | No | Add null checks |
