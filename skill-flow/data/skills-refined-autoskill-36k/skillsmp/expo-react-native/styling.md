# NativeWind Styling

## Basic Usage
```tsx
import { View, Text } from 'react-native';

export function Card({ title }: { title: string }) {
  return (
    <View className="bg-white rounded-lg p-4 shadow-md">
      <Text className="text-lg font-bold text-gray-900">{title}</Text>
    </View>
  );
}
```

## Conditional Styles
```tsx
<View className={`p-4 rounded-lg ${isActive ? 'bg-blue-500' : 'bg-gray-200'}`}>
  <Text className={isActive ? 'text-white' : 'text-gray-700'}>
    {label}
  </Text>
</View>
```

## Styling Third-Party Components
```tsx
import { cssInterop } from 'nativewind';
import { SomeComponent } from 'some-library';

const StyledComponent = cssInterop(SomeComponent, {
  className: { target: 'style' },
});

<StyledComponent className="bg-blue-500 p-4" />
```

## Best Practices
- Use Tailwind classes over inline styles
- Create reusable styled components for consistency
- Use `@layer components` in `global.css` for repeated patterns
- Leverage responsive prefixes: `sm:`, `md:`, `lg:`
