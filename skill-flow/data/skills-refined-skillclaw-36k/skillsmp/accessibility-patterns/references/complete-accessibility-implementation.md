# Complete Accessibility Implementation

<!-- Loading Trigger: Agent reads this file when implementing VoiceOver support, Dynamic Type, reduce motion, keyboard navigation, or WCAG compliance -->

## VoiceOver Support

```swift
import SwiftUI

// MARK: - Accessible Custom Controls

struct AccessibleRatingControl: View {
    @Binding var rating: Int
    let maximumRating: Int

    var body: some View {
        HStack(spacing: 8) {
            ForEach(1...maximumRating, id: \.self) { index in
                Image(systemName: index <= rating ? "star.fill" : "star")
                    .foregroundStyle(index <= rating ? .yellow : .gray)
                    .onTapGesture {
                        rating = index
                    }
            }
        }
        // Group as single accessible element
        .accessibilityElement(children: .ignore)
        .accessibilityLabel("Rating")
        .accessibilityValue("\(rating) out of \(maximumRating) stars")
        .accessibilityHint("Double tap and hold, then drag to adjust rating")
        .accessibilityAdjustableAction { direction in
            switch direction {
            case .increment:
                if rating < maximumRating { rating += 1 }
            case .decrement:
                if rating > 1 { rating -= 1 }
            @unknown default:
                break
            }
        }
    }
}

// MARK: - Accessible Custom Slider

struct AccessibleCustomSlider: View {
    @Binding var value: Double
    let range: ClosedRange<Double>
    let step: Double
    let label: String
    let valueFormatter: (Double) -> String

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(label)
                .font(.headline)

            GeometryReader { geometry in
                ZStack(alignment: .leading) {
                    // Track
                    Rectangle()
                        .fill(Color.gray.opacity(0.3))
                        .frame(height: 8)
                        .cornerRadius(4)

                    // Filled portion
                    Rectangle()
                        .fill(Color.accentColor)
                        .frame(width: thumbPosition(in: geometry.size.width), height: 8)
                        .cornerRadius(4)

                    // Thumb
                    Circle()
                        .fill(Color.white)
                        .frame(width: 24, height: 24)
                        .shadow(radius: 2)
                        .offset(x: thumbPosition(in: geometry.size.width) - 12)
                        .gesture(
                            DragGesture()
                                .onChanged { gesture in
                                    updateValue(from: gesture.location.x, in: geometry.size.width)
                                }
                        )
                }
            }
            .frame(height: 24)
        }
        .accessibilityElement(children: .ignore)
        .accessibilityLabel(label)
        .accessibilityValue(valueFormatter(value))
        .accessibilityAdjustableAction { direction in
            switch direction {
            case .increment:
                value = min(value + step, range.upperBound)
            case .decrement:
                value = max(value - step, range.lowerBound)
            @unknown default:
                break
            }
        }
    }

    private func thumbPosition(in width: CGFloat) -> CGFloat {
        let percentage = (value - range.lowerBound) / (range.upperBound - range.lowerBound)
        return CGFloat(percentage) * width
    }

    private func updateValue(from x: CGFloat, in width: CGFloat) {
        let percentage = max(0, min(1, x / width))
        let newValue = range.lowerBound + Double(percentage) * (range.upperBound - range.lowerBound)
        value = (newValue / step).rounded() * step
    }
}

// MARK: - Accessible Data Visualization

struct AccessibleBarChart: View {
    let data: [(label: String, value: Double)]
    let maxValue: Double

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            ForEach(Array(data.enumerated()), id: \.offset) { index, item in
                HStack {
                    Text(item.label)
                        .frame(width: 80, alignment: .leading)

                    GeometryReader { geometry in
                        Rectangle()
                            .fill(Color.accentColor)
                            .frame(width: barWidth(for: item.value, in: geometry.size.width))
                    }
                    .frame(height: 24)

                    Text(String(format: "%.1f", item.value))
                        .frame(width: 50, alignment: .trailing)
                }
                .accessibilityElement(children: .ignore)
                .accessibilityLabel("\(item.label)")
                .accessibilityValue("\(String(format: "%.1f", item.value)), \(percentageDescription(for: item.value))")
            }
        }
        .accessibilityElement(children: .contain)
        .accessibilityLabel("Bar chart with \(data.count) items")
        .accessibilityHint("Swipe right to navigate through each bar")
    }

    private func barWidth(for value: Double, in totalWidth: CGFloat) -> CGFloat {
        CGFloat(value / maxValue) * totalWidth
    }

    private func percentageDescription(for value: Double) -> String {
        let percentage = (value / maxValue) * 100
        return "\(Int(percentage)) percent of maximum"
    }
}

// MARK: - Accessible Image with Description

struct AccessibleImage: View {
    let image: Image
    let label: String
    let description: String?
    let isDecorative: Bool

    init(
        _ image: Image,
        label: String,
        description: String? = nil,
        isDecorative: Bool = false
    ) {
        self.image = image
        self.label = label
        self.description = description
        self.isDecorative = isDecorative
    }

    var body: some View {
        image
            .resizable()
            .aspectRatio(contentMode: .fit)
            .accessibilityLabel(isDecorative ? "" : label)
            .accessibilityHint(description ?? "")
            .accessibilityHidden(isDecorative)
    }
}

// MARK: - Rotor Actions

struct ArticleView: View {
    let article: Article
    @State private var isSaved = false
    @State private var isSharing = false

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                Text(article.title)
                    .font(.title)
                    .accessibilityAddTraits(.isHeader)

                Text(article.author)
                    .font(.subheadline)
                    .foregroundStyle(.secondary)

                Text(article.content)
                    .font(.body)
            }
            .padding()
        }
        .accessibilityRotor("Headings") {
            AccessibilityRotorEntry(article.title, id: "title")
        }
        .accessibilityAction(named: "Save Article") {
            isSaved.toggle()
        }
        .accessibilityAction(named: "Share") {
            isSharing = true
        }
    }
}

struct Article {
    let title: String
    let author: String
    let content: String
}
```

## Dynamic Type Support

```swift
import SwiftUI

// MARK: - Scaled Metric for Custom Values

struct DynamicTypeView: View {
    @ScaledMetric(relativeTo: .body) private var iconSize: CGFloat = 24
    @ScaledMetric(relativeTo: .body) private var spacing: CGFloat = 8
    @ScaledMetric(relativeTo: .body) private var padding: CGFloat = 16

    var body: some View {
        HStack(spacing: spacing) {
            Image(systemName: "star.fill")
                .frame(width: iconSize, height: iconSize)

            Text("Featured Item")
                .font(.body)
        }
        .padding(padding)
    }
}

// MARK: - Adaptive Layout for Large Text

struct AdaptiveListItem: View {
    let title: String
    let subtitle: String
    let icon: String

    @Environment(\.dynamicTypeSize) private var dynamicTypeSize

    var body: some View {
        Group {
            if dynamicTypeSize.isAccessibilitySize {
                // Stack vertically for accessibility sizes
                VStack(alignment: .leading, spacing: 8) {
                    Image(systemName: icon)
                        .font(.title)

                    VStack(alignment: .leading, spacing: 4) {
                        Text(title)
                            .font(.headline)
                        Text(subtitle)
                            .font(.subheadline)
                            .foregroundStyle(.secondary)
                    }
                }
            } else {
                // Horizontal layout for standard sizes
                HStack(spacing: 12) {
                    Image(systemName: icon)
                        .font(.title2)
                        .frame(width: 44, height: 44)

                    VStack(alignment: .leading, spacing: 2) {
                        Text(title)
                            .font(.headline)
                        Text(subtitle)
                            .font(.subheadline)
                            .foregroundStyle(.secondary)
                    }

                    Spacer()
                }
            }
        }
        .padding()
    }
}

// MARK: - Text Truncation Prevention

struct FlexibleTextLayout: View {
    let items: [String]

    @Environment(\.dynamicTypeSize) private var dynamicTypeSize

    var body: some View {
        if dynamicTypeSize.isAccessibilitySize {
            // Use scrollable list for very large text
            ScrollView {
                VStack(alignment: .leading, spacing: 8) {
                    ForEach(items, id: \.self) { item in
                        Text(item)
                            .fixedSize(horizontal: false, vertical: true)
                    }
                }
            }
        } else {
            // Wrap in flow layout for standard sizes
            FlowLayout(spacing: 8) {
                ForEach(items, id: \.self) { item in
                    Text(item)
                        .padding(.horizontal, 12)
                        .padding(.vertical, 6)
                        .background(Color.accentColor.opacity(0.2))
                        .cornerRadius(8)
                }
            }
        }
    }
}

// MARK: - Flow Layout for Tags

struct FlowLayout: Layout {
    var spacing: CGFloat = 8

    func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) -> CGSize {
        let result = FlowLayoutResult(
            in: proposal.width ?? 0,
            subviews: subviews,
            spacing: spacing
        )
        return result.size
    }

    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) {
        let result = FlowLayoutResult(
            in: bounds.width,
            subviews: subviews,
            spacing: spacing
        )

        for (index, subview) in subviews.enumerated() {
            let position = result.positions[index]
            subview.place(
                at: CGPoint(x: bounds.minX + position.x, y: bounds.minY + position.y),
                proposal: .unspecified
            )
        }
    }

    struct FlowLayoutResult {
        var positions: [CGPoint] = []
        var size: CGSize = .zero

        init(in width: CGFloat, subviews: Subviews, spacing: CGFloat) {
            var currentX: CGFloat = 0
            var currentY: CGFloat = 0
            var lineHeight: CGFloat = 0
            var maxWidth: CGFloat = 0

            for subview in subviews {
                let size = subview.sizeThatFits(.unspecified)

                if currentX + size.width > width && currentX > 0 {
                    currentX = 0
                    currentY += lineHeight + spacing
                    lineHeight = 0
                }

                positions.append(CGPoint(x: currentX, y: currentY))

                currentX += size.width + spacing
                lineHeight = max(lineHeight, size.height)
                maxWidth = max(maxWidth, currentX)
            }

            self.size = CGSize(width: maxWidth, height: currentY + lineHeight)
        }
    }
}

// MARK: - Minimum Touch Target

struct AccessibleButton: View {
    let title: String
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Text(title)
                .padding(.horizontal, 16)
                .padding(.vertical, 8)
        }
        .frame(minWidth: 44, minHeight: 44) // Minimum touch target
        .contentShape(Rectangle()) // Expand tap area
    }
}
```

## Reduce Motion Support

```swift
import SwiftUI

// MARK: - Motion-Aware Animations

struct MotionAwareAnimation: View {
    @State private var isExpanded = false
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    var body: some View {
        VStack {
            Button("Toggle") {
                if reduceMotion {
                    // Instant change without animation
                    isExpanded.toggle()
                } else {
                    // Animated change
                    withAnimation(.spring(response: 0.3, dampingFraction: 0.7)) {
                        isExpanded.toggle()
                    }
                }
            }

            Rectangle()
                .fill(Color.blue)
                .frame(width: isExpanded ? 200 : 100, height: isExpanded ? 200 : 100)
        }
    }
}

// MARK: - Reduced Motion View Modifier

extension View {
    func reducedMotionAnimation<V: Equatable>(
        _ animation: Animation? = .default,
        value: V
    ) -> some View {
        modifier(ReducedMotionAnimationModifier(animation: animation, value: value))
    }
}

struct ReducedMotionAnimationModifier<V: Equatable>: ViewModifier {
    let animation: Animation?
    let value: V
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    func body(content: Content) -> some View {
        content
            .animation(reduceMotion ? nil : animation, value: value)
    }
}

// MARK: - Motion-Aware Loading Indicator

struct AccessibleLoadingIndicator: View {
    @State private var isAnimating = false
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    var body: some View {
        Group {
            if reduceMotion {
                // Static loading indicator
                Text("Loading...")
                    .foregroundStyle(.secondary)
            } else {
                // Animated spinner
                Circle()
                    .trim(from: 0, to: 0.7)
                    .stroke(Color.accentColor, lineWidth: 3)
                    .frame(width: 24, height: 24)
                    .rotationEffect(Angle(degrees: isAnimating ? 360 : 0))
                    .onAppear {
                        withAnimation(.linear(duration: 1).repeatForever(autoreverses: false)) {
                            isAnimating = true
                        }
                    }
            }
        }
        .accessibilityLabel("Loading")
    }
}

// MARK: - Crossfade Transition

struct MotionAwareCrossfade<Content: View>: View {
    let condition: Bool
    @ViewBuilder let content: (Bool) -> Content
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    var body: some View {
        if reduceMotion {
            content(condition)
        } else {
            content(condition)
                .animation(.easeInOut(duration: 0.2), value: condition)
        }
    }
}
```

## Focus Management

```swift
import SwiftUI

// MARK: - Focus State Management

struct AccessibleForm: View {
    @State private var username = ""
    @State private var email = ""
    @State private var password = ""
    @State private var confirmPassword = ""

    @FocusState private var focusedField: FormField?
    @State private var validationErrors: [FormField: String] = [:]

    enum FormField: Hashable, CaseIterable {
        case username, email, password, confirmPassword
    }

    var body: some View {
        Form {
            Section {
                TextField("Username", text: $username)
                    .focused($focusedField, equals: .username)
                    .accessibilityLabel("Username")
                    .accessibilityHint(validationErrors[.username] ?? "Enter your username")

                TextField("Email", text: $email)
                    .focused($focusedField, equals: .email)
                    .keyboardType(.emailAddress)
                    .accessibilityLabel("Email")
                    .accessibilityHint(validationErrors[.email] ?? "Enter your email address")

                SecureField("Password", text: $password)
                    .focused($focusedField, equals: .password)
                    .accessibilityLabel("Password")
                    .accessibilityHint(validationErrors[.password] ?? "Enter your password")

                SecureField("Confirm Password", text: $confirmPassword)
                    .focused($focusedField, equals: .confirmPassword)
                    .accessibilityLabel("Confirm Password")
                    .accessibilityHint(validationErrors[.confirmPassword] ?? "Re-enter your password")
            }

            Section {
                Button("Create Account") {
                    validateAndSubmit()
                }
            }
        }
        .onSubmit {
            advanceToNextField()
        }
    }

    private func advanceToNextField() {
        guard let current = focusedField,
              let currentIndex = FormField.allCases.firstIndex(of: current) else {
            return
        }

        let nextIndex = FormField.allCases.index(after: currentIndex)
        if nextIndex < FormField.allCases.endIndex {
            focusedField = FormField.allCases[nextIndex]
        } else {
            focusedField = nil
            validateAndSubmit()
        }
    }

    private func validateAndSubmit() {
        validationErrors.removeAll()

        if username.isEmpty {
            validationErrors[.username] = "Username is required"
        }

        if !email.contains("@") {
            validationErrors[.email] = "Please enter a valid email"
        }

        if password.count < 8 {
            validationErrors[.password] = "Password must be at least 8 characters"
        }

        if password != confirmPassword {
            validationErrors[.confirmPassword] = "Passwords do not match"
        }

        // Focus on first error field
        if let firstError = FormField.allCases.first(where: { validationErrors[$0] != nil }) {
            focusedField = firstError

            // Announce error to VoiceOver
            UIAccessibility.post(
                notification: .announcement,
                argument: validationErrors[firstError]
            )
        }
    }
}

// MARK: - Accessibility Focus Notification

struct AccessibilityAnnouncement {
    static func announce(_ message: String) {
        UIAccessibility.post(notification: .announcement, argument: message)
    }

    static func announceScreenChange(_ message: String? = nil) {
        UIAccessibility.post(notification: .screenChanged, argument: message)
    }

    static func announceLayoutChange(_ message: String? = nil) {
        UIAccessibility.post(notification: .layoutChanged, argument: message)
    }
}
```

## Color and Contrast

```swift
import SwiftUI
import UIKit

// MARK: - High Contrast Support

struct ContrastAwareText: View {
    let text: String
    let style: TextStyle

    @Environment(\.accessibilityDifferentiateWithoutColor) private var differentiateWithoutColor
    @Environment(\.colorSchemeContrast) private var contrast

    enum TextStyle {
        case primary, secondary, success, error, warning
    }

    var body: some View {
        HStack(spacing: 4) {
            // Add icon when differentiating without color
            if differentiateWithoutColor {
                icon
            }

            Text(text)
                .foregroundStyle(foregroundColor)
        }
    }

    @ViewBuilder
    private var icon: some View {
        switch style {
        case .success:
            Image(systemName: "checkmark.circle.fill")
        case .error:
            Image(systemName: "xmark.circle.fill")
        case .warning:
            Image(systemName: "exclamationmark.triangle.fill")
        default:
            EmptyView()
        }
    }

    private var foregroundColor: Color {
        let isHighContrast = contrast == .increased

        switch style {
        case .primary:
            return .primary
        case .secondary:
            return isHighContrast ? .primary : .secondary
        case .success:
            return isHighContrast ? Color(UIColor.systemGreen) : .green
        case .error:
            return isHighContrast ? Color(UIColor.systemRed) : .red
        case .warning:
            return isHighContrast ? Color(UIColor.systemOrange) : .orange
        }
    }
}

// MARK: - WCAG Contrast Checker

struct WCAGContrastChecker {

    enum Level {
        case aa       // 4.5:1 for normal text, 3:1 for large text
        case aaa      // 7:1 for normal text, 4.5:1 for large text
    }

    static func contrastRatio(between foreground: UIColor, and background: UIColor) -> Double {
        let foregroundLuminance = relativeLuminance(of: foreground)
        let backgroundLuminance = relativeLuminance(of: background)

        let lighter = max(foregroundLuminance, backgroundLuminance)
        let darker = min(foregroundLuminance, backgroundLuminance)

        return (lighter + 0.05) / (darker + 0.05)
    }

    static func meetsLevel(
        _ level: Level,
        foreground: UIColor,
        background: UIColor,
        isLargeText: Bool = false
    ) -> Bool {
        let ratio = contrastRatio(between: foreground, and: background)

        switch (level, isLargeText) {
        case (.aa, true):
            return ratio >= 3.0
        case (.aa, false):
            return ratio >= 4.5
        case (.aaa, true):
            return ratio >= 4.5
        case (.aaa, false):
            return ratio >= 7.0
        }
    }

    private static func relativeLuminance(of color: UIColor) -> Double {
        var red: CGFloat = 0
        var green: CGFloat = 0
        var blue: CGFloat = 0
        var alpha: CGFloat = 0

        color.getRed(&red, green: &green, blue: &blue, alpha: &alpha)

        func adjust(_ component: CGFloat) -> Double {
            let value = Double(component)
            return value <= 0.03928
                ? value / 12.92
                : pow((value + 0.055) / 1.055, 2.4)
        }

        return 0.2126 * adjust(red) + 0.7152 * adjust(green) + 0.0722 * adjust(blue)
    }
}

// MARK: - Smart Invert Support

struct SmartInvertImage: View {
    let image: Image

    var body: some View {
        image
            .accessibilityIgnoresInvertColors(true) // Don't invert this image
    }
}
```

## Keyboard Navigation (Catalyst/iPad)

```swift
import SwiftUI

// MARK: - Keyboard Shortcuts

struct KeyboardNavigableList: View {
    @State private var items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
    @State private var selectedIndex: Int?

    var body: some View {
        List(selection: $selectedIndex) {
            ForEach(Array(items.enumerated()), id: \.offset) { index, item in
                Text(item)
                    .tag(index)
            }
        }
        .focusable()
        .onKeyPress(.upArrow) {
            moveSelection(by: -1)
            return .handled
        }
        .onKeyPress(.downArrow) {
            moveSelection(by: 1)
            return .handled
        }
        .onKeyPress(.return) {
            if let index = selectedIndex {
                activateItem(at: index)
            }
            return .handled
        }
        .keyboardShortcut("n", modifiers: .command) // Cmd+N for new item
    }

    private func moveSelection(by offset: Int) {
        guard !items.isEmpty else { return }

        if let current = selectedIndex {
            selectedIndex = max(0, min(items.count - 1, current + offset))
        } else {
            selectedIndex = offset > 0 ? 0 : items.count - 1
        }
    }

    private func activateItem(at index: Int) {
        // Handle item activation
    }
}

// MARK: - Focus Section Grouping

struct FocusSectionedView: View {
    var body: some View {
        VStack {
            Section("Navigation") {
                HStack {
                    Button("Home") { }
                    Button("Search") { }
                    Button("Profile") { }
                }
            }
            .focusSection()

            Divider()

            Section("Content") {
                ScrollView {
                    LazyVStack {
                        ForEach(0..<20) { index in
                            ContentRow(index: index)
                        }
                    }
                }
            }
            .focusSection()
        }
    }
}

struct ContentRow: View {
    let index: Int

    var body: some View {
        Text("Content Item \(index)")
            .padding()
            .focusable()
    }
}
```
