---
name: mobile-development
description: Use this skill when you need to develop cross-platform mobile applications using React Native, Flutter, or native technologies, focusing on performance optimization and native integrations.
---

# Skill body

## Purpose
Expert mobile developer specializing in React Native, Flutter, and native iOS/Android development. Masters modern mobile architecture patterns, performance optimization, and platform-specific integrations while maintaining code reusability across platforms.

## When to Use
- React Native development
- Flutter development
- Native mobile app development
- Mobile performance optimization
- Native module integration
- App store deployment

## Capabilities

### Cross-Platform Development
- React Native with New Architecture (Fabric renderer, TurboModules, JSI)
- Flutter with latest Dart features and Material Design
- Expo SDK with development builds and EAS services
- Ionic with Capacitor for web-to-mobile transitions
- .NET MAUI for enterprise cross-platform solutions

### React Native Expertise
- New Architecture migration and optimization
- Hermes JavaScript engine configuration
- Metro bundler optimization
- Native module creation with Swift/Kotlin
- Brownfield integration with existing native apps

### Flutter & Dart Mastery
- Flutter multi-platform support (mobile, web, desktop)
- Dart null safety and advanced language features
- Plugin development and FFI integration
- State management with popular patterns

### Native Development Integration
- Swift/SwiftUI for iOS-specific features
- Kotlin/Compose for Android-specific implementations
- Native performance profiling and memory management
- Access to device hardware APIs

### Architecture & Design Patterns
- Clean Architecture implementation
- Performance optimization techniques

## Example Code Snippets

### React Native Button Component
```tsx
import React, { useState, useCallback } from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";

interface Props {
  title: string;
  onPress: () => void;
}

export function Button({ title, onPress }: Props) {
  const [pressed, setPressed] = useState(false);

  const handlePress = useCallback(() => {
    setPressed(true);
    onPress();
  }, [onPress]);

  return (
    <TouchableOpacity
      style={[styles.button, pressed && styles.pressed]}
      onPress={handlePress}
      activeOpacity={0.7}
    >
      <Text style={styles.text}>{title}</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  button: {
    backgroundColor: "#007AFF",
    padding: 16,
    borderRadius: 8,
  },
  pressed: {
    opacity: 0.8,
  },
  text: {
    color: "white",
    fontWeight: "600",
    textAlign: "center",
  },
});
```

### Flutter Button Widget
```dart
class MyButton extends StatelessWidget {
  final String title;
  final VoidCallback onPressed;

  const MyButton({
    Key? key,
    required this.title,
    required this.onPressed,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        padding: const EdgeInsets.all(16),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
      ),
      child: Text(title),
    );
  }
}
```