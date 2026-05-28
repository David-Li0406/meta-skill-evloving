---
name: flutter-performance
description: Use this skill when optimizing performance or profiling code in Flutter applications.
---

# Skill body

This skill provides guidelines and best practices for enhancing the performance of Flutter applications. Follow these steps to effectively optimize your code:

1. **Profile Your Application**: Use the Flutter DevTools to identify performance bottlenecks. Focus on areas with high CPU usage or long frame rendering times.
2. **Optimize Widget Builds**: Minimize the number of widgets rebuilt during state changes. Use `const` constructors where possible and consider using `ValueListenableBuilder` or `StreamBuilder` for efficient updates.
3. **Reduce Overdraw**: Use the Flutter performance overlay to identify and reduce overdraw in your application. Ensure that widgets are not unnecessarily layered on top of each other.
4. **Use Efficient Images**: Optimize image sizes and formats. Use `AssetImage` for local images and `NetworkImage` for remote images, ensuring they are appropriately sized for the display.
5. **Leverage Isolates**: For heavy computations, consider using isolates to run code in a separate thread, preventing UI jank.
6. **Minimize Build Context Usage**: Avoid passing the `BuildContext` unnecessarily, as it can lead to performance issues during widget rebuilds.
7. **Test on Real Devices**: Always test performance on real devices, as emulators may not accurately reflect performance characteristics.

For detailed documentation, refer to the performance guidelines in the Flutter documentation.