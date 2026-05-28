# TypeScript Patterns

## Component Props
```tsx
interface ButtonProps {
  title: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}

export default function Button({ 
  title, 
  onPress, 
  variant = 'primary',
  disabled = false 
}: ButtonProps) {
  return (
    <TouchableOpacity 
      onPress={onPress} 
      disabled={disabled}
      className={variant === 'primary' ? 'bg-blue-500' : 'bg-gray-500'}
    >
      <Text className="text-white">{title}</Text>
    </TouchableOpacity>
  );
}
```

## API Types
```tsx
interface User {
  id: string;
  email: string;
  name: string;
}

interface ApiResponse<T> {
  data: T;
  message: string;
  success: boolean;
}

async function fetchUser(id: string): Promise<ApiResponse<User>> {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}
```

## Path Aliases
```json
// tsconfig.json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": { "@/*": ["src/*"] }
  }
}
```

## Best Practices
- Use `interface` for objects, `type` for unions/primitives
- Avoid `any`—use `unknown` when type is uncertain
- Define API response types
- Use generics for reusable utilities
