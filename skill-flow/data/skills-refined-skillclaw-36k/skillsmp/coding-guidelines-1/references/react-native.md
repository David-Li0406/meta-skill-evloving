# React Native Patterns

Principles and research guidance for projects using React Native.

## Core Principles

### Native Components
React Native uses native components instead of DOM elements. Research current component names and props:

| Web | React Native |
|-----|--------------|
| `<div>` | `<View>` |
| `<span>`, `<p>` | `<Text>` |
| `<input>` | `<TextInput>` |
| `<button>` | `<Pressable>`, `<TouchableOpacity>` |
| `<img>` | `<Image>` |
| `<ul>`, `<li>` | `<FlatList>`, `<ScrollView>` |

### Research Before Implementation
React Native APIs evolve. Always verify current syntax:
- Use context7 to query React Native documentation
- Search for: component props, platform-specific behavior, styling

## Component Patterns

### Props Extension
Extend base component props for proper typing:

```tsx
import { Pressable, type PressableProps, Text } from "react-native";

type Props = PressableProps & {
  children?: React.ReactNode;
  loading?: boolean;
};

const Button = ({ children, disabled, loading, ...props }: Props) => (
  <Pressable disabled={disabled || loading} {...props}>
    <Text>{children}</Text>
  </Pressable>
);
```

### Text Must Be Wrapped
All text content must be inside `<Text>` components:

```tsx
// Correct
<View>
  <Text>Hello world</Text>
</View>

// Error - text outside Text component
<View>Hello world</View>
```

### Conditional Styling
Use array join or conditional expressions:

```tsx
<TextInput
  className={[
    "h-12 rounded-lg border",
    error ? "border-red-500" : "border-slate-300",
  ].join(" ")}
/>
```

## Platform Considerations

### Platform-Specific Code
Research `Platform` API for platform-specific behavior:

```tsx
import { Platform } from "react-native";

<KeyboardAvoidingView
  behavior={Platform.OS === "ios" ? "padding" : "height"}
>
```

### Safe Areas
Use SafeAreaView for notches and system UI. Research current safe area patterns.

## Research Checklist

Before implementing, query documentation for:
- [ ] Correct component for the use case (View, Text, Pressable, etc.)
- [ ] Available props and their types
- [ ] Platform-specific behavior differences (iOS vs Android)
- [ ] Styling approach (StyleSheet vs className with NativeWind)
- [ ] Any deprecated components or props in current version
