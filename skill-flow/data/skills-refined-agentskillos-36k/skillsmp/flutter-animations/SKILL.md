---
name: flutter-animations
description: Master Flutter's animation system with implicit and explicit animations, hero transitions, physics-based motion, and custom transitions. Use when adding animations, creating transitions, implementing hero effects, or building interactive animated experiences.
version: 1.0.0
---

# Flutter Animations

Master Flutter's animation system to create smooth, performant, and delightful user experiences through implicit animations, explicit control, hero transitions, and physics-based motion.

## Overview

Flutter's animation framework is built on a fundamental principle: well-designed animations make UIs feel more intuitive, contribute to a polished experience, and provide visual feedback that guides users through your application. The framework offers a comprehensive toolkit ranging from simple, pre-packaged implicit animations to fully customizable explicit animations with physics simulations.

Understanding when and how to use each type of animation is crucial for building modern Flutter applications. This skill provides comprehensive guidance on Flutter's animation capabilities, performance optimization techniques, and best practices for creating smooth, responsive animations.

## Animation Philosophy in Flutter

Flutter approaches animations through a layered architecture that balances ease of use with powerful control:

**Progressive Complexity**: Start with the simplest solution that meets your needs. Flutter encourages using implicit animations for straightforward transitions, explicit animations when you need coordination, and custom implementations only when necessary. This progressive approach ensures you're not adding unnecessary complexity to your codebase.

**Declarative Animation**: Unlike imperative animation systems where you manually calculate and set values frame-by-frame, Flutter's declarative approach lets you specify what should change and the framework handles the interpolation. You describe the start and end states, and Flutter smoothly transitions between them.

**Composition Over Inheritance**: Flutter's animation classes are designed to compose together. A `CurvedAnimation` wraps an `AnimationController`, a `Tween` transforms values, and these pieces combine to create sophisticated effects without deep inheritance hierarchies.

**Performance First**: The animation system is optimized for 60fps (or 120fps on capable devices) by default. The framework provides tools like `RepaintBoundary` and `AnimatedBuilder` to minimize unnecessary rebuilds and ensure smooth performance even on lower-end devices.

## Implicit vs Explicit Animations

The choice between implicit and explicit animations is one of the first decisions you'll make when adding motion to your Flutter app.

### Implicit Animations

Implicit animations are Flutter widgets that automatically animate property changes over a specified duration. They derive from `ImplicitlyAnimatedWidget` and handle all animation controller management internally.

**When to Use Implicit Animations**:
- Animating simple property changes (opacity, size, color, position)
- One-off transitions triggered by user interaction or state changes
- Prototyping animation ideas quickly
- When you don't need to coordinate multiple animations together

**Common Implicit Animated Widgets**:
- `AnimatedContainer` - Animates container properties like size, color, padding, and borders
- `AnimatedOpacity` - Fades widgets in and out
- `AnimatedPositioned` - Animates position changes within a Stack
- `AnimatedAlign` - Animates alignment changes
- `AnimatedPadding` - Animates padding transitions
- `AnimatedSwitcher` - Cross-fades between different widgets
- `TweenAnimationBuilder` - Creates custom implicit animations for any property

**Key Advantages**:
- Minimal boilerplate code
- No need to manage AnimationController lifecycle
- Automatic cleanup when widget is disposed
- Perfect for UI polish and subtle transitions

**Example Use Case**: A button that changes color when pressed, a container that expands when selected, or a widget that fades in when data loads.

### Explicit Animations

Explicit animations give you full control over the animation lifecycle through `AnimationController`. You manage when animations start, stop, reverse, and repeat.

**When to Use Explicit Animations**:
- Coordinating multiple simultaneous animations (staggered effects)
- Creating looping or repeating animations
- Responding to user gestures in real-time (drag, fling)
- Building complex animation choreography
- When you need precise control over animation timing

**Core Components**:
- `AnimationController` - The animation timeline controller
- `Tween` - Maps animation values to custom ranges
- `CurvedAnimation` - Applies easing curves
- `AnimatedBuilder` - Efficiently rebuilds only animated parts
- `AnimatedWidget` - Base class for reusable animated widgets

**Key Advantages**:
- Fine-grained control over timing and playback
- Ability to coordinate multiple animations
- Support for custom animation curves
- Integration with gestures and physics simulations

**Example Use Case**: A loading spinner that continuously rotates, a card that flips over with coordinated opacity and rotation changes, or an interactive animation that follows user drag gestures.

## Hero Animations

Hero animations, also known as shared element transitions, create visual continuity between screens by animating a widget from one route to another. This pattern is ubiquitous in modern mobile apps - think of tapping a photo thumbnail that smoothly expands into a full-screen view.

**How Hero Animations Work**:

1. **Tagging**: Wrap widgets on both the source and destination screens with `Hero` widgets sharing the same `tag`
2. **Detection**: When you push a new route, Flutter's Navigator detects matching hero tags
3. **Animation**: The hero widget flies from its position on the first screen to its position on the second screen
4. **Morphing**: The hero can change size, shape, and position during the transition

**Behind the Scenes**:

Flutter doesn't actually move the widget between screens. Instead, it:
- Creates a copy in an overlay above both routes
- Animates the overlay widget's bounds using `RectTween`
- Uses `MaterialRectArcTween` for curved motion paths
- Removes the overlay and reveals the destination widget when complete

**Standard Hero Pattern**:
The most common pattern involves an image or card that appears on a list screen and expands to fill the detail screen. The hero tag uniquely identifies which elements should animate together.

**Radial Hero Animations**:
A variant where the hero transforms from circular to rectangular (or vice versa) while flying between screens. This requires using `MaterialRectCenterArcTween` and `RadialExpansion` to maintain the circular clipping during the animation.

**Best Practices**:
- Use meaningful, unique tags that won't accidentally match other heroes
- Keep the widget tree structure similar between source and destination
- Wrap image heroes in `Material(color: Colors.transparent)` for smooth transitions
- Use `timeDilation` to slow animations during development and debugging
- Ensure heroes have defined sizes on both screens

## Performance Considerations

Creating smooth animations requires understanding Flutter's rendering pipeline and avoiding common performance pitfalls.

### The 60fps Target

Flutter aims to render frames in 16ms or less (60 frames per second). On devices with 120Hz displays, this target drops to 8ms. Each frame consists of:
- **Build phase** (8ms budget): Constructing the widget tree
- **Layout/Paint phase** (8ms budget): Measuring and rendering

If either phase exceeds its budget, you'll experience jank - visible stuttering or dropped frames.

### Critical Performance Rules

**1. Avoid Opacity Widget in Animations**

The `Opacity` widget is expensive because it requires rendering the child into an intermediate buffer before applying opacity. For animations:
- Use `AnimatedOpacity` instead of wrapping widgets in `Opacity`
- Use `FadeInImage` for image fade transitions
- Apply opacity directly to decoration colors when possible

**2. Optimize AnimatedBuilder Usage**

`AnimatedBuilder` rebuilds its subtree on every animation frame. To minimize work:
- Pass static widgets as the `child` parameter, not inside the `builder`
- Only rebuild widgets that actually change with the animation
- Use `RepaintBoundary` to isolate repainting to specific subtrees

**3. Avoid Clipping During Animation**

Clipping operations (ClipRect, ClipRRect, ClipPath) are expensive because they create new layers. When animating:
- Pre-clip images before animation starts
- Use `ClipRect` (fastest) instead of `ClipRRect` or `ClipPath` when possible
- Consider whether clipping is necessary or if visual effects can achieve the same result

**4. Use vsync Properly**

The `vsync` parameter in `AnimationController` prevents offscreen animations from consuming resources. Always:
- Add `SingleTickerProviderStateMixin` or `TickerProviderStateMixin` to your State class
- Pass `this` as the vsync parameter
- This ensures animations pause when the widget is not visible

**5. Leverage RepaintBoundary**

`RepaintBoundary` creates a separate display list that can be cached and reused. Use it to:
- Isolate complex, static parts of your UI from animating parts
- Prevent unnecessary repaints of expensive widgets
- Create performance boundaries in lists with animated items

### Measuring Performance

Use Flutter DevTools Performance View to:
- Track frame rendering times
- Identify expensive rebuilds
- Monitor layout passes
- Profile animation smoothness
- Check for shader compilation jank

Enable performance overlays during development:
```dart
MaterialApp(
  showPerformanceOverlay: true,  // Shows GPU/UI thread times
  debugShowCheckedModeBanner: false,
)
```

## Animation Curves and Timing

The timing and easing of animations dramatically affects how they feel. Flutter provides a rich set of curves through the `Curves` class.

**Common Curves**:
- `Curves.linear` - No easing, constant speed (rarely used)
- `Curves.easeIn` - Slow start, fast finish
- `Curves.easeOut` - Fast start, slow finish (most common)
- `Curves.easeInOut` - Slow start and finish, fast middle
- `Curves.elasticOut` - Bouncy overshoot effect
- `Curves.bounceOut` - Multiple bounces at end
- `Curves.fastOutSlowIn` - Material Design standard curve

**Platform Conventions**:
- **Material Design** (Android): Typically uses `Curves.fastOutSlowIn` or `Curves.easeOut`
- **iOS**: Often uses `Curves.easeInOut` or custom curves matching UIKit animations

**Custom Curves**:
You can create custom curves by extending the `Curve` class or using `Cubic` for cubic Bézier curves. This is useful for matching designer specifications or creating unique animation feels.

## Physics-Based Animations

Physics simulations make animations feel natural by modeling real-world behavior like springs, gravity, and friction.

**SpringSimulation** is the most common physics-based animation. It uses three parameters:
- **Mass**: Higher values create more inertia and slower response
- **Stiffness**: Higher values make the spring snappier and more responsive
- **Damping**: Higher values reduce oscillation and bouncing

**Use Cases**:
- Scrolling overscroll effects
- Drawer open/close with momentum
- Draggable cards that snap back into place
- Interactive animations that respond to gesture velocity

**Implementation Pattern**:
Instead of specifying a duration and curve, you use `controller.animateWith(simulation)` and the physics engine calculates the motion based on initial velocity and spring properties.

## Common Patterns and Anti-Patterns

### Recommended Patterns

**Start Simple**: Always begin with implicit animations. Only move to explicit animations when you need features implicit animations don't provide.

**Compose Animations**: Build complex effects by composing simple animations rather than creating monolithic animation code.

**Separate Concerns**: Keep animation logic separate from business logic. Use `AnimatedBuilder` or `AnimatedWidget` to isolate rebuilds.

**Provide Feedback**: Use animations to acknowledge user input, show state transitions, and guide attention.

### Anti-Patterns to Avoid

**Over-Animation**: Not everything needs to animate. Too much motion becomes distracting and slows down the user experience.

**Inconsistent Timing**: Mixing different animation durations randomly creates a chaotic feel. Establish a timing scale (fast: 150ms, normal: 300ms, slow: 500ms) and stick to it.

**Ignoring Platform Conventions**: iOS and Android have different animation expectations. Consider using platform-specific curves and timings.

**Animating on Every Frame**: Calling `setState()` in `addListener()` rebuilds your entire widget. Use `AnimatedBuilder` to isolate rebuilds.

**Memory Leaks**: Forgetting to dispose `AnimationController` instances causes memory leaks. Always dispose in the `dispose()` method.

## Integration with State Management

Animations often need to respond to state changes from your chosen state management solution.

**Provider/ChangeNotifier**: Trigger animations in response to notifyListeners calls
**BLoC/Cubit**: Start animations when specific states are emitted
**Riverpod**: Use providers to trigger animation controller methods
**GetX**: Integrate animations with reactive state updates

The key is separating what changes (state) from how it changes (animation). State management determines when to animate; the animation system handles how.

## Testing Animated Widgets

Testing animations requires special consideration:

**Widget Tests**: Use `WidgetTester.pumpAndSettle()` to wait for animations to complete, or `pump(duration)` to advance by a specific time.

**Unit Tests**: Test animation controllers and tweens independently of widgets.

**Integration Tests**: Use `tester.pump()` in a loop to verify animation behavior over time.

**Golden Tests**: Capture snapshots at different animation stages to verify visual appearance.

## When to Use Each Approach

### Use Implicit Animations When:
- Animating a single widget property
- The animation is triggered once and completes
- You want minimal code and quick implementation
- The animation doesn't need to coordinate with others

### Use Explicit Animations When:
- Creating staggered or choreographed animations
- Building repeating or looping animations
- Responding to continuous user input (gestures)
- You need fine control over playback (pause, reverse, seek)

### Use Hero Animations When:
- Transitioning between screens with shared elements
- Creating visual continuity in navigation
- The same conceptual object appears on multiple screens

### Use Physics Simulations When:
- You want natural, realistic motion
- The animation should respond to user gesture velocity
- Creating spring-based or bouncy effects
- Modeling scrolling or flinging behavior

## Learning Path

1. **Start with implicit animations**: Master `AnimatedContainer`, `AnimatedOpacity`, and `TweenAnimationBuilder`
2. **Progress to explicit animations**: Learn `AnimationController`, `Tween`, and `AnimatedBuilder`
3. **Explore hero animations**: Implement shared element transitions
4. **Add physics**: Incorporate `SpringSimulation` for natural motion
5. **Build staggered effects**: Coordinate multiple animations with intervals
6. **Optimize performance**: Profile and optimize using DevTools

## Additional Resources

See the reference documentation for detailed implementation guides:
- **references/implicit-animations.md** - Complete guide to built-in implicit animated widgets
- **references/explicit-animations.md** - Deep dive into AnimationController and explicit animation patterns
- **references/hero-transitions.md** - Implementing shared element transitions
- **references/custom-transitions.md** - Building custom page route transitions
- **references/physics-simulations.md** - Physics-based animation techniques
- **examples/staggered-animations.md** - Creating choreographed animation sequences
- **examples/interactive-animations.md** - Building gesture-driven animations

## Conclusion

Flutter's animation system provides the tools to create everything from subtle UI polish to complex, interactive motion experiences. By understanding the spectrum from implicit to explicit animations, leveraging physics for natural motion, and following performance best practices, you can build applications that feel fluid, responsive, and delightful to use.

Remember: the best animations are often the ones users don't consciously notice - they just make the interface feel right.
