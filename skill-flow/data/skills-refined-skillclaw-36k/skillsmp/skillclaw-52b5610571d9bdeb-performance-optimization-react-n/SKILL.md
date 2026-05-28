---
name: performance-optimization-react-native
description: Use this skill when optimizing performance or profiling code in React Native applications.
---

# Performance Optimization - React Native

This skill provides guidelines and best practices for optimizing performance in React Native applications. Follow these steps to ensure your app runs efficiently:

1. **Profile Your Application**: Use tools like the React Native Performance Monitor to identify bottlenecks.
2. **Optimize Rendering**: Minimize unnecessary re-renders by using `shouldComponentUpdate` or `React.memo`.
3. **Use FlatList for Large Lists**: Implement `FlatList` instead of `ScrollView` for rendering large lists to improve performance.
4. **Reduce Overdraw**: Use the `Debug` mode to visualize overdraw and optimize your component hierarchy.
5. **Optimize Images**: Use appropriate image sizes and formats to reduce load times.
6. **Leverage Native Modules**: Offload heavy computations to native code when necessary.
7. **Avoid Inline Functions in Render**: Define functions outside of the render method to prevent unnecessary re-renders.

For detailed documentation, refer to the performance optimization guidelines.