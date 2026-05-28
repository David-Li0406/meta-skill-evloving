# Atomic Design iOS — Complete Design System

> **Loading Trigger**: Load when building component library from scratch, implementing design token system, or organizing large-scale design systems.

---

## Complete Token System

```swift
// MARK: - Tokens/Spacing.swift

import SwiftUI

enum Spacing {
    /// 4pt
    static let xxs: CGFloat = 4
    /// 8pt
    static let xs: CGFloat = 8
    /// 12pt
    static let sm: CGFloat = 12
    /// 16pt
    static let md: CGFloat = 16
    /// 24pt
    static let lg: CGFloat = 24
    /// 32pt
    static let xl: CGFloat = 32
    /// 48pt
    static let xxl: CGFloat = 48
    /// 64pt
    static let xxxl: CGFloat = 64
}

// MARK: - Tokens/Radius.swift

enum Radius {
    /// 4pt
    static let sm: CGFloat = 4
    /// 8pt
    static let md: CGFloat = 8
    /// 12pt
    static let lg: CGFloat = 12
    /// 16pt
    static let xl: CGFloat = 16
    /// Full rounding (pill shape)
    static let full: CGFloat = 9999
}

// MARK: - Tokens/Shadows.swift

enum Shadow {
    static let subtle = ShadowStyle(
        color: .black.opacity(0.05),
        radius: 2,
        x: 0,
        y: 1
    )

    static let elevated = ShadowStyle(
        color: .black.opacity(0.1),
        radius: 8,
        x: 0,
        y: 4
    )

    static let prominent = ShadowStyle(
        color: .black.opacity(0.15),
        radius: 16,
        x: 0,
        y: 8
    )
}

struct ShadowStyle {
    let color: Color
    let radius: CGFloat
    let x: CGFloat
    let y: CGFloat
}

extension View {
    func shadow(_ style: ShadowStyle) -> some View {
        shadow(color: style.color, radius: style.radius, x: style.x, y: style.y)
    }
}

// MARK: - Tokens/Colors.swift

extension Color {
    // MARK: - Semantic Colors

    /// Primary text color
    static let textPrimary = Color("TextPrimary")
    /// Secondary text color
    static let textSecondary = Color("TextSecondary")
    /// Tertiary/disabled text
    static let textTertiary = Color("TextTertiary")
    /// Inverse text (on dark backgrounds)
    static let textInverse = Color("TextInverse")

    // MARK: - Surfaces

    /// Main background
    static let surface = Color("Surface")
    /// Elevated surface (cards, modals)
    static let surfaceElevated = Color("SurfaceElevated")
    /// Secondary surface
    static let surfaceSecondary = Color("SurfaceSecondary")

    // MARK: - Brand

    /// Primary brand color
    static let brandPrimary = Color("BrandPrimary")
    /// Secondary brand color
    static let brandSecondary = Color("BrandSecondary")
    /// Accent color for highlights
    static let brandAccent = Color("BrandAccent")

    // MARK: - Semantic Feedback

    /// Success state
    static let success = Color("Success")
    /// Success background
    static let successBackground = Color("SuccessBackground")
    /// Warning state
    static let warning = Color("Warning")
    /// Warning background
    static let warningBackground = Color("WarningBackground")
    /// Error/Destructive state
    static let error = Color("Error")
    /// Error background
    static let errorBackground = Color("ErrorBackground")
    /// Info state
    static let info = Color("Info")
    /// Info background
    static let infoBackground = Color("InfoBackground")

    // MARK: - Interactive

    /// Interactive elements (buttons, links)
    static let interactive = Color("Interactive")
    /// Hover/focused state
    static let interactiveHover = Color("InteractiveHover")
    /// Pressed state
    static let interactivePressed = Color("InteractivePressed")
    /// Disabled state
    static let interactiveDisabled = Color("InteractiveDisabled")

    // MARK: - Border

    /// Default border
    static let border = Color("Border")
    /// Focused border
    static let borderFocused = Color("BorderFocused")
    /// Error border
    static let borderError = Color("BorderError")
}

// MARK: - Tokens/Typography.swift

extension Font {
    // MARK: - Display

    /// 34pt Bold - Hero titles
    static let displayLarge = Font.system(size: 34, weight: .bold)
    /// 28pt Bold - Page titles
    static let displayMedium = Font.system(size: 28, weight: .bold)
    /// 22pt Semibold - Section titles
    static let displaySmall = Font.system(size: 22, weight: .semibold)

    // MARK: - Headings

    /// 20pt Semibold
    static let heading1 = Font.system(size: 20, weight: .semibold)
    /// 18pt Semibold
    static let heading2 = Font.system(size: 18, weight: .semibold)
    /// 16pt Medium
    static let heading3 = Font.system(size: 16, weight: .medium)

    // MARK: - Body

    /// 17pt Regular - Primary body text
    static let bodyLarge = Font.system(size: 17)
    /// 15pt Regular - Secondary body text
    static let bodyMedium = Font.system(size: 15)
    /// 13pt Regular - Small body text
    static let bodySmall = Font.system(size: 13)

    // MARK: - Labels

    /// 14pt Medium - Button labels
    static let labelLarge = Font.system(size: 14, weight: .medium)
    /// 12pt Medium - Small labels
    static let labelMedium = Font.system(size: 12, weight: .medium)
    /// 11pt Medium - Tiny labels
    static let labelSmall = Font.system(size: 11, weight: .medium)

    // MARK: - Caption

    /// 12pt Regular
    static let caption = Font.system(size: 12)
    /// 11pt Regular
    static let captionSmall = Font.system(size: 11)
}
```

---

## Atoms

```swift
// MARK: - Atoms/PrimaryButton.swift

import SwiftUI

struct PrimaryButton: View {
    let title: String
    let action: () -> Void
    var isLoading: Bool = false
    var isEnabled: Bool = true
    var size: Size = .regular
    var isFullWidth: Bool = false

    enum Size {
        case small, regular, large

        var verticalPadding: CGFloat {
            switch self {
            case .small: return Spacing.xs
            case .regular: return Spacing.sm
            case .large: return Spacing.md
            }
        }

        var horizontalPadding: CGFloat {
            switch self {
            case .small: return Spacing.sm
            case .regular: return Spacing.md
            case .large: return Spacing.lg
            }
        }

        var font: Font {
            switch self {
            case .small: return .labelMedium
            case .regular: return .labelLarge
            case .large: return .heading3
            }
        }
    }

    var body: some View {
        Button(action: action) {
            HStack(spacing: Spacing.xs) {
                if isLoading {
                    ProgressView()
                        .progressViewStyle(CircularProgressViewStyle(tint: .textInverse))
                        .scaleEffect(size == .small ? 0.8 : 1.0)
                } else {
                    Text(title)
                        .font(size.font)
                }
            }
            .frame(maxWidth: isFullWidth ? .infinity : nil)
            .padding(.vertical, size.verticalPadding)
            .padding(.horizontal, size.horizontalPadding)
            .background(isEnabled ? Color.brandPrimary : Color.interactiveDisabled)
            .foregroundColor(.textInverse)
            .cornerRadius(Radius.md)
        }
        .disabled(!isEnabled || isLoading)
    }
}

// MARK: - Atoms/SecondaryButton.swift

struct SecondaryButton: View {
    let title: String
    let action: () -> Void
    var isEnabled: Bool = true
    var size: PrimaryButton.Size = .regular

    var body: some View {
        Button(action: action) {
            Text(title)
                .font(size.font)
                .padding(.vertical, size.verticalPadding)
                .padding(.horizontal, size.horizontalPadding)
                .background(Color.surfaceSecondary)
                .foregroundColor(isEnabled ? .brandPrimary : .textTertiary)
                .cornerRadius(Radius.md)
                .overlay(
                    RoundedRectangle(cornerRadius: Radius.md)
                        .stroke(isEnabled ? Color.brandPrimary : Color.border, lineWidth: 1)
                )
        }
        .disabled(!isEnabled)
    }
}

// MARK: - Atoms/IconButton.swift

struct IconButton: View {
    let icon: String
    let action: () -> Void
    var size: Size = .regular
    var style: Style = .default

    enum Size {
        case small, regular, large

        var dimension: CGFloat {
            switch self {
            case .small: return 32
            case .regular: return 44
            case .large: return 56
            }
        }

        var iconSize: CGFloat {
            switch self {
            case .small: return 14
            case .regular: return 20
            case .large: return 24
            }
        }
    }

    enum Style {
        case `default`
        case filled
        case tinted

        func background(isPressed: Bool) -> Color {
            switch self {
            case .default:
                return isPressed ? .surfaceSecondary : .clear
            case .filled:
                return isPressed ? .interactivePressed : .brandPrimary
            case .tinted:
                return isPressed ? .brandPrimary.opacity(0.2) : .brandPrimary.opacity(0.1)
            }
        }

        var foregroundColor: Color {
            switch self {
            case .default, .tinted: return .brandPrimary
            case .filled: return .textInverse
            }
        }
    }

    @State private var isPressed = false

    var body: some View {
        Button(action: action) {
            Image(systemName: icon)
                .font(.system(size: size.iconSize, weight: .medium))
                .foregroundColor(style.foregroundColor)
                .frame(width: size.dimension, height: size.dimension)
                .background(style.background(isPressed: isPressed))
                .cornerRadius(Radius.md)
        }
        .buttonStyle(PressableButtonStyle(isPressed: $isPressed))
    }
}

// MARK: - Atoms/Badge.swift

struct Badge: View {
    let text: String
    var style: Style = .default

    enum Style {
        case `default`, success, warning, error, info

        var backgroundColor: Color {
            switch self {
            case .default: return .surfaceSecondary
            case .success: return .successBackground
            case .warning: return .warningBackground
            case .error: return .errorBackground
            case .info: return .infoBackground
            }
        }

        var foregroundColor: Color {
            switch self {
            case .default: return .textSecondary
            case .success: return .success
            case .warning: return .warning
            case .error: return .error
            case .info: return .info
            }
        }
    }

    var body: some View {
        Text(text)
            .font(.labelSmall)
            .padding(.horizontal, Spacing.xs)
            .padding(.vertical, Spacing.xxs)
            .background(style.backgroundColor)
            .foregroundColor(style.foregroundColor)
            .cornerRadius(Radius.sm)
    }
}

// MARK: - Atoms/TextInput.swift

struct TextInput: View {
    let placeholder: String
    @Binding var text: String
    var error: String? = nil
    var isSecure: Bool = false

    @FocusState private var isFocused: Bool

    var body: some View {
        VStack(alignment: .leading, spacing: Spacing.xxs) {
            Group {
                if isSecure {
                    SecureField(placeholder, text: $text)
                } else {
                    TextField(placeholder, text: $text)
                }
            }
            .font(.bodyMedium)
            .padding(Spacing.sm)
            .background(Color.surface)
            .cornerRadius(Radius.md)
            .overlay(
                RoundedRectangle(cornerRadius: Radius.md)
                    .stroke(borderColor, lineWidth: 1)
            )
            .focused($isFocused)

            if let error = error {
                Text(error)
                    .font(.captionSmall)
                    .foregroundColor(.error)
            }
        }
    }

    private var borderColor: Color {
        if error != nil { return .borderError }
        if isFocused { return .borderFocused }
        return .border
    }
}
```

---

## Molecules

```swift
// MARK: - Molecules/Card.swift

struct Card<Content: View>: View {
    let content: Content
    var padding: CGFloat = Spacing.md

    init(
        padding: CGFloat = Spacing.md,
        @ViewBuilder content: () -> Content
    ) {
        self.padding = padding
        self.content = content()
    }

    var body: some View {
        content
            .padding(padding)
            .background(Color.surfaceElevated)
            .cornerRadius(Radius.lg)
            .shadow(Shadow.subtle)
    }
}

// MARK: - Molecules/SearchBar.swift

struct SearchBar: View {
    @Binding var text: String
    var placeholder: String = "Search"
    var onSubmit: (() -> Void)? = nil

    @FocusState private var isFocused: Bool

    var body: some View {
        HStack(spacing: Spacing.xs) {
            Image(systemName: "magnifyingglass")
                .foregroundColor(.textTertiary)
                .font(.bodyMedium)

            TextField(placeholder, text: $text)
                .font(.bodyMedium)
                .focused($isFocused)
                .onSubmit { onSubmit?() }

            if !text.isEmpty {
                Button {
                    text = ""
                } label: {
                    Image(systemName: "xmark.circle.fill")
                        .foregroundColor(.textTertiary)
                        .font(.bodyMedium)
                }
            }
        }
        .padding(.horizontal, Spacing.sm)
        .padding(.vertical, Spacing.xs)
        .background(Color.surfaceSecondary)
        .cornerRadius(Radius.md)
    }
}

// MARK: - Molecules/ListItem.swift

struct ListItem<Leading: View, Trailing: View>: View {
    let title: String
    var subtitle: String? = nil
    let leading: Leading
    let trailing: Trailing
    var action: (() -> Void)? = nil

    init(
        title: String,
        subtitle: String? = nil,
        @ViewBuilder leading: () -> Leading = { EmptyView() },
        @ViewBuilder trailing: () -> Trailing = { EmptyView() },
        action: (() -> Void)? = nil
    ) {
        self.title = title
        self.subtitle = subtitle
        self.leading = leading()
        self.trailing = trailing()
        self.action = action
    }

    var body: some View {
        Button {
            action?()
        } label: {
            HStack(spacing: Spacing.sm) {
                leading

                VStack(alignment: .leading, spacing: Spacing.xxs) {
                    Text(title)
                        .font(.bodyMedium)
                        .foregroundColor(.textPrimary)

                    if let subtitle = subtitle {
                        Text(subtitle)
                            .font(.caption)
                            .foregroundColor(.textSecondary)
                    }
                }

                Spacer()

                trailing
            }
            .padding(.vertical, Spacing.sm)
            .contentShape(Rectangle())
        }
        .buttonStyle(.plain)
        .disabled(action == nil)
    }
}

// MARK: - Molecules/EmptyState.swift

struct EmptyState: View {
    let icon: String
    let title: String
    var message: String? = nil
    var action: (() -> Void)? = nil
    var actionTitle: String = "Try Again"

    var body: some View {
        VStack(spacing: Spacing.md) {
            Image(systemName: icon)
                .font(.system(size: 48))
                .foregroundColor(.textTertiary)

            VStack(spacing: Spacing.xs) {
                Text(title)
                    .font(.heading2)
                    .foregroundColor(.textPrimary)

                if let message = message {
                    Text(message)
                        .font(.bodyMedium)
                        .foregroundColor(.textSecondary)
                        .multilineTextAlignment(.center)
                }
            }

            if let action = action {
                PrimaryButton(title: actionTitle, action: action)
            }
        }
        .padding(Spacing.xl)
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}
```

---

## Organisms

```swift
// MARK: - Organisms/ProductCard.swift

struct ProductCard: View {
    let product: Product
    let onTap: () -> Void
    let onAddToCart: () -> Void

    var body: some View {
        Card {
            VStack(alignment: .leading, spacing: Spacing.sm) {
                // Image
                AsyncImage(url: product.imageURL) { image in
                    image
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                } placeholder: {
                    Color.surfaceSecondary
                }
                .frame(height: 160)
                .clipped()
                .cornerRadius(Radius.md)

                // Content
                VStack(alignment: .leading, spacing: Spacing.xs) {
                    Text(product.name)
                        .font(.heading3)
                        .foregroundColor(.textPrimary)
                        .lineLimit(2)

                    Text(product.price.formatted)
                        .font(.bodyLarge)
                        .fontWeight(.semibold)
                        .foregroundColor(.brandPrimary)

                    if let originalPrice = product.originalPrice {
                        Text(originalPrice.formatted)
                            .font(.bodySmall)
                            .foregroundColor(.textTertiary)
                            .strikethrough()
                    }
                }

                // Actions
                HStack(spacing: Spacing.xs) {
                    SecondaryButton(title: "Details", action: onTap, size: .small)
                    PrimaryButton(title: "Add", action: onAddToCart, size: .small, isFullWidth: true)
                }
            }
        }
    }
}

// MARK: - Organisms/UserCard.swift

struct UserCard: View {
    let user: User
    let onTap: () -> Void

    var body: some View {
        Card {
            HStack(spacing: Spacing.md) {
                // Avatar
                AsyncImage(url: user.avatarURL) { image in
                    image
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                } placeholder: {
                    Circle()
                        .fill(Color.surfaceSecondary)
                        .overlay(
                            Text(user.initials)
                                .font(.heading2)
                                .foregroundColor(.textSecondary)
                        )
                }
                .frame(width: 64, height: 64)
                .clipShape(Circle())

                // Info
                VStack(alignment: .leading, spacing: Spacing.xxs) {
                    Text(user.fullName)
                        .font(.heading3)
                        .foregroundColor(.textPrimary)

                    Text(user.email.value)
                        .font(.bodySmall)
                        .foregroundColor(.textSecondary)

                    Badge(text: user.role.displayName, style: user.role == .admin ? .info : .default)
                }

                Spacer()

                Image(systemName: "chevron.right")
                    .foregroundColor(.textTertiary)
            }
        }
        .onTapGesture(perform: onTap)
    }
}

// MARK: - Organisms/OrderSummary.swift

struct OrderSummary: View {
    let order: Order

    var body: some View {
        Card {
            VStack(alignment: .leading, spacing: Spacing.md) {
                // Header
                HStack {
                    VStack(alignment: .leading, spacing: Spacing.xxs) {
                        Text("Order #\(order.id.prefix(8))")
                            .font(.heading3)
                            .foregroundColor(.textPrimary)

                        Text(order.createdAt.formatted(date: .abbreviated, time: .shortened))
                            .font(.caption)
                            .foregroundColor(.textSecondary)
                    }

                    Spacer()

                    Badge(text: order.status.displayName, style: badgeStyle(for: order.status))
                }

                Divider()

                // Items
                VStack(spacing: Spacing.xs) {
                    ForEach(order.items) { item in
                        HStack {
                            Text("\(item.quantity)x \(item.productName)")
                                .font(.bodySmall)
                                .foregroundColor(.textSecondary)

                            Spacer()

                            Text(item.totalPrice.formatted)
                                .font(.bodySmall)
                                .foregroundColor(.textSecondary)
                        }
                    }
                }

                Divider()

                // Total
                HStack {
                    Text("Total")
                        .font(.heading3)
                        .foregroundColor(.textPrimary)

                    Spacer()

                    Text(order.pricing.total.formatted)
                        .font(.heading2)
                        .foregroundColor(.brandPrimary)
                }
            }
        }
    }

    private func badgeStyle(for status: Order.Status) -> Badge.Style {
        switch status {
        case .pending: return .warning
        case .confirmed, .processing, .shipped: return .info
        case .delivered: return .success
        case .cancelled, .refunded: return .error
        }
    }
}
```

---

## Templates

```swift
// MARK: - Templates/ListPageTemplate.swift

struct ListPageTemplate<Item: Identifiable, Row: View>: View {
    let title: String
    let items: [Item]
    let isLoading: Bool
    let error: String?
    let emptyIcon: String
    let emptyTitle: String
    let emptyMessage: String
    let onRefresh: () async -> Void
    let onLoadMore: (() async -> Void)?
    let rowContent: (Item) -> Row

    @State private var searchText = ""

    var body: some View {
        NavigationStack {
            Group {
                if isLoading && items.isEmpty {
                    loadingView
                } else if let error = error, items.isEmpty {
                    errorView(error)
                } else if items.isEmpty {
                    emptyView
                } else {
                    listView
                }
            }
            .navigationTitle(title)
            .searchable(text: $searchText)
            .refreshable {
                await onRefresh()
            }
        }
    }

    private var loadingView: some View {
        VStack(spacing: Spacing.md) {
            ProgressView()
            Text("Loading...")
                .font(.bodyMedium)
                .foregroundColor(.textSecondary)
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }

    private func errorView(_ message: String) -> some View {
        EmptyState(
            icon: "exclamationmark.triangle",
            title: "Something went wrong",
            message: message,
            action: { Task { await onRefresh() } }
        )
    }

    private var emptyView: some View {
        EmptyState(
            icon: emptyIcon,
            title: emptyTitle,
            message: emptyMessage
        )
    }

    private var listView: some View {
        List {
            ForEach(items) { item in
                rowContent(item)
                    .onAppear {
                        if item.id == items.last?.id {
                            Task { await onLoadMore?() }
                        }
                    }
            }
        }
        .listStyle(.plain)
    }
}
```
