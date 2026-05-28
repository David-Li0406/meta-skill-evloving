# Liquid Glass (iOS 26+)

> Apple's new translucent material với fluid morphing animations.

---

## 🎯 Overview

**Platform**: iOS 26+, iPadOS 26+, macOS Tahoe 26+  
**Purpose**: Tạo distinct functional layer cho controls và navigation

**Đặc điểm**:
- Translucent với optical properties như glass thật
- Reflects và refracts content xung quanh
- Fluid morphing animations
- Auto-adapts to light/dark và accessibility settings

---

## ✨ Automatic Adoption

Build với Xcode mới nhất, các components tự động có Liquid Glass:

| Component | Liquid Glass |
|-----------|--------------|
| `NavigationStack`, `NavigationSplitView` | ✅ |
| `Toolbar`, `TabView` | ✅ |
| `Button`, `Toggle`, `Slider`, `Picker` | ✅ |
| `Sheet`, `Popover` | ✅ |
| `TextField` | ✅ |

---

## 🎨 Button Styles

```swift
// Standard Liquid Glass
Button("Submit") { }
    .buttonStyle(.glass)

// Prominent (primary CTA)
Button("Get Started") { }
    .buttonStyle(.glassProminent)

// Tinted với custom color
Button("Custom") { }
    .buttonStyle(.glass(.blue))
```

---

## 📦 Custom Glass Effect

```swift
// Apply sparingly - overuse distracts
RoundedRectangle(cornerRadius: 12)
    .fill(.clear)
    .glassEffect(.regularMaterial, in: RoundedRectangle(cornerRadius: 12))
```

### Performance - GlassEffectContainer

```swift
// Combine multiple effects trong container để optimize
GlassEffectContainer {
    VStack {
        ForEach(items) { item in
            ItemView(item)
                .glassEffect(.regularMaterial, in: RoundedRectangle(cornerRadius: 12))
        }
    }
}
```

---

## 🎬 Animation Rules

**CRITICAL**: Animation state vẫn phải ở `@State`, không phải ViewModel

```swift
// ViewModel
class MyViewModel: ObservableObject {
    @Published var showMenu: Bool = false  // Business state
}

// View
struct MyView: View {
    @StateObject var viewModel: MyViewModel
    @State private var morphProgress: Double = 0.0  // Animation state
    
    var body: some View {
        Button("Options") { viewModel.showMenu = true }
            .buttonStyle(.glass)
        
        .onChange(of: viewModel.showMenu) { showing in
            withAnimation(.spring(response: 0.3)) {
                morphProgress = showing ? 1.0 : 0.0
            }
        }
    }
}
```

---

## 📱 Tab Bar Minimize

```swift
TabView {
    HomeView()
        .tabItem { Label("Home", systemImage: "house") }
    
    ProfileView()
        .tabItem { Label("Profile", systemImage: "person") }
}
.tabBarMinimizeBehavior(.onScrollDown)
// System auto-handles animation
```

---

## 🔲 Sidebar với Background Extension

```swift
NavigationSplitView {
    SidebarView()
} detail: {
    DetailView()
        .backgroundExtensionEffect()
}
```

---

## ♿ Accessibility

System tự động adapts khi user enable:

| Setting | Effect |
|---------|--------|
| **Reduce Transparency** | Glass opacity giảm/tắt |
| **Reduce Motion** | Morphing animations đơn giản hóa |

```swift
@Environment(\.accessibilityReduceMotion) var reduceMotion
@Environment(\.accessibilityReduceTransparency) var reduceTransparency

var body: some View {
    Button("Submit") { }
        .buttonStyle(reduceTransparency ? .bordered : .glass)
        .onChange(of: viewModel.isLoading) { loading in
            if reduceMotion {
                buttonScale = loading ? 0.95 : 1.0  // Instant
            } else {
                withAnimation { buttonScale = loading ? 0.95 : 1.0 }
            }
        }
}
```

---

## ✅ Best Practices

| ✅ Do | ❌ Don't |
|-------|---------|
| Dùng standard components | Overuse custom glass effects |
| Remove custom backgrounds | Backgrounds che system effects |
| Dùng `GlassEffectContainer` | Nhiều glass effects không grouped |
| Test accessibility settings | Ignore reduce transparency |
| Animation trong `@State` | Animation trong ViewModel |

---

## 🔗 Related

- [animation-guidelines.md](animation-guidelines.md) - Animation rules
- [theme-system.md](theme-system.md) - Theme integration

