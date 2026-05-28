# Animation Guidelines

> ⚠️ **CRITICAL**: Đọc file này TRƯỚC KHI implement bất kỳ animation nào.

---

## 🎯 Core Rule

```
Animation state → @State (View)
Business state → @Published (ViewModel)

KHÔNG BAO GIỜ đặt animation values trong ViewModel @Published
```

**Lý do**:
- `@Published` updates tốn performance, animations cần 60fps
- Animation là UI concern, không phải business logic
- ViewModel tests không cần biết về animations

---

## ✅ Correct Pattern

```swift
// ViewModel - Business state only
class MyViewModel: ObservableObject {
    @Published var status: Status = .idle
    
    enum Status { case idle, loading, success, error }
}

// View - Animation state
struct MyView: View {
    @StateObject var viewModel: MyViewModel
    @State private var buttonScale: CGFloat = 1.0  // ✅ Animation
    @State private var isShaking = false           // ✅ Animation
    
    var body: some View {
        Button("Submit") { }
            .scaleEffect(buttonScale)
            .onChange(of: viewModel.status) { status in
                // Business state → trigger animation
                switch status {
                case .loading:
                    withAnimation { buttonScale = 0.95 }
                case .error:
                    withAnimation { isShaking = true }
                default:
                    buttonScale = 1.0
                }
            }
    }
}
```

---

## ❌ Forbidden Pattern

```swift
// ❌ WRONG - Animation trong ViewModel
class MyViewModel: ObservableObject {
    @Published var buttonScale: CGFloat = 1.0  // ❌ NO!
    @Published var shakeOffset: Double = 0     // ❌ NO!
    @Published var pulseOpacity: Double = 1.0  // ❌ NO!
}
```

---

## 🎨 Common Animation Patterns

### 1. Button Scale on Loading

```swift
@State private var buttonScale: CGFloat = 1.0

.onChange(of: viewModel.status) { status in
    withAnimation(.easeInOut(duration: 0.15)) {
        buttonScale = status == .loading ? 0.95 : 1.0
    }
}
```

### 2. Shake on Error

```swift
@State private var shakeCount: Int = 0

.modifier(ShakeEffect(shakes: shakeCount))
.onChange(of: viewModel.errorMessage) { error in
    if error != nil {
        withAnimation { shakeCount += 1 }
    }
}
```

### 3. Pulse on Active

```swift
@State private var pulseScale: CGFloat = 1.0

.onChange(of: viewModel.isActive) { active in
    if active {
        withAnimation(.easeInOut.repeatForever()) {
            pulseScale = 1.2
        }
    } else {
        withAnimation { pulseScale = 1.0 }
    }
}
```

### 4. Fade Transition

```swift
@State private var opacity: Double = 0

.opacity(opacity)
.onAppear {
    withAnimation(.easeIn(duration: 0.3)) {
        opacity = 1.0
    }
}
```

---

## 📱 Liquid Glass Animations (iOS 26+)

### Button Morph

```swift
// ViewModel
@Published var showMenu: Bool = false

// View
@State private var morphProgress: Double = 0.0

Button("Options") { viewModel.showMenu = true }
    .buttonStyle(.glass)
    
.onChange(of: viewModel.showMenu) { showing in
    withAnimation(.spring(response: 0.3)) {
        morphProgress = showing ? 1.0 : 0.0
    }
}
```

### Tab Bar Minimize

```swift
TabView { }
    .tabBarMinimizeBehavior(.onScrollDown)
// System tự handle animation
```

### Accessibility

```swift
@Environment(\.accessibilityReduceMotion) var reduceMotion

// Respect reduce motion setting
if reduceMotion {
    opacity = targetValue  // Instant
} else {
    withAnimation { opacity = targetValue }
}
```

---

## 🔍 Property Wrappers Guide

| Wrapper | Dùng cho | Animation? |
|---------|----------|------------|
| `@State` | Animation values, transient UI | ✅ Yes |
| `@Published` | Business state trong ViewModel | ❌ No animation |
| `@FocusState` | TextField focus | UI state |
| `@GestureState` | Drag, pinch gestures | ✅ Yes |

---

## ✅ Validation Checklist

- [ ] Animation values dùng `@State` trong View
- [ ] Business state triggers animation via `.onChange()`
- [ ] `withAnimation` wrap `@State` updates
- [ ] Không có animation values trong ViewModel `@Published`
- [ ] Respect `accessibilityReduceMotion` setting

---

## ⚠️ Common Mistakes

| Mistake | Fix |
|---------|-----|
| `@Published var scale: CGFloat` | `@State private var scale: CGFloat` |
| `.animation()` modifier everywhere | Dùng `withAnimation` explicitly |
| Animation trong ViewModel | Animation trong View `@State` |

