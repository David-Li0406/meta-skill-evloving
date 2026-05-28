# Complete Localization System Reference

<!-- Loading Trigger: Load this reference when implementing internationalization, runtime language switching, complex pluralization, RTL layout support, or locale-aware formatting for iOS/tvOS applications -->

## Type-Safe Localization with SwiftGen

```swift
// MARK: - SwiftGen Configuration

/*
swiftgen.yml:

strings:
  inputs:
    - Resources/en.lproj/Localizable.strings
  outputs:
    - templateName: structured-swift5
      output: Generated/Strings.swift
      params:
        publicAccess: true
        enumName: L10n
*/

// MARK: - Generated Output Example (Strings.swift)

// swiftlint:disable all
public enum L10n {

    public enum Auth {
        public enum Login {
            /// Welcome back!
            public static let title = L10n.tr("Localizable", "auth.login.title")
            /// Enter your email address
            public static let emailPlaceholder = L10n.tr("Localizable", "auth.login.email_placeholder")
            /// Enter your password
            public static let passwordPlaceholder = L10n.tr("Localizable", "auth.login.password_placeholder")
            /// Sign In
            public static let submitButton = L10n.tr("Localizable", "auth.login.submit_button")

            public enum Error {
                /// Invalid email or password
                public static let invalidCredentials = L10n.tr("Localizable", "auth.login.error.invalid_credentials")
            }
        }

        public enum Register {
            /// Create Account
            public static let title = L10n.tr("Localizable", "auth.register.title")
        }
    }

    public enum Common {
        /// Cancel
        public static let cancel = L10n.tr("Localizable", "common.cancel")
        /// OK
        public static let ok = L10n.tr("Localizable", "common.ok")
        /// Done
        public static let done = L10n.tr("Localizable", "common.done")
        /// Error
        public static let error = L10n.tr("Localizable", "common.error")
    }

    public enum User {
        /// Hello, %@!
        public static func greeting(_ p1: Any) -> String {
            return L10n.tr("Localizable", "user.greeting", String(describing: p1))
        }
    }

    public enum Items {
        /// %d items
        public static func count(_ p1: Int) -> String {
            return L10n.tr("Localizable", "items.count", p1)
        }
    }
}

extension L10n {
    private static func tr(_ table: String, _ key: String, _ args: CVarArg...) -> String {
        let format = BundleToken.bundle.localizedString(forKey: key, value: nil, table: table)
        return String(format: format, locale: Locale.current, arguments: args)
    }
}

private final class BundleToken {
    static let bundle: Bundle = {
        #if SWIFT_PACKAGE
        return Bundle.module
        #else
        return Bundle(for: BundleToken.self)
        #endif
    }()
}
// swiftlint:enable all

// MARK: - Usage in SwiftUI

struct LoginView: View {
    var body: some View {
        VStack {
            Text(L10n.Auth.Login.title)
                .font(.largeTitle)

            TextField(L10n.Auth.Login.emailPlaceholder, text: $email)

            Button(L10n.Auth.Login.submitButton) {
                // Login action
            }
        }
    }

    @State private var email = ""
}
```

## Stringsdict for Complex Pluralization

```xml
<!-- en.lproj/Localizable.stringsdict -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- Simple plural: "5 items" -->
    <key>items.count</key>
    <dict>
        <key>NSStringLocalizedFormatKey</key>
        <string>%#@items@</string>
        <key>items</key>
        <dict>
            <key>NSStringFormatSpecTypeKey</key>
            <string>NSStringPluralRuleType</string>
            <key>NSStringFormatValueTypeKey</key>
            <string>d</string>
            <key>zero</key>
            <string>No items</string>
            <key>one</key>
            <string>%d item</string>
            <key>other</key>
            <string>%d items</string>
        </dict>
    </dict>

    <!-- Complex plural with context: "John has 5 photos" -->
    <key>user.photos.count</key>
    <dict>
        <key>NSStringLocalizedFormatKey</key>
        <string>%1$@ has %2$#@photos@</string>
        <key>photos</key>
        <dict>
            <key>NSStringFormatSpecTypeKey</key>
            <string>NSStringPluralRuleType</string>
            <key>NSStringFormatValueTypeKey</key>
            <string>d</string>
            <key>zero</key>
            <string>no photos</string>
            <key>one</key>
            <string>%2$d photo</string>
            <key>other</key>
            <string>%2$d photos</string>
        </dict>
    </dict>

    <!-- Multiple plurals: "3 files in 2 folders" -->
    <key>files.in.folders</key>
    <dict>
        <key>NSStringLocalizedFormatKey</key>
        <string>%1$#@files@ in %2$#@folders@</string>
        <key>files</key>
        <dict>
            <key>NSStringFormatSpecTypeKey</key>
            <string>NSStringPluralRuleType</string>
            <key>NSStringFormatValueTypeKey</key>
            <string>d</string>
            <key>one</key>
            <string>%1$d file</string>
            <key>other</key>
            <string>%1$d files</string>
        </dict>
        <key>folders</key>
        <dict>
            <key>NSStringFormatSpecTypeKey</key>
            <string>NSStringPluralRuleType</string>
            <key>NSStringFormatValueTypeKey</key>
            <string>d</string>
            <key>one</key>
            <string>%2$d folder</string>
            <key>other</key>
            <string>%2$d folders</string>
        </dict>
    </dict>

    <!-- Relative time: "5 minutes ago" -->
    <key>time.ago.minutes</key>
    <dict>
        <key>NSStringLocalizedFormatKey</key>
        <string>%#@minutes@ ago</string>
        <key>minutes</key>
        <dict>
            <key>NSStringFormatSpecTypeKey</key>
            <string>NSStringPluralRuleType</string>
            <key>NSStringFormatValueTypeKey</key>
            <string>d</string>
            <key>one</key>
            <string>%d minute</string>
            <key>other</key>
            <string>%d minutes</string>
        </dict>
    </dict>
</dict>
</plist>
```

```xml
<!-- ru.lproj/Localizable.stringsdict (Russian - 4 plural forms) -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>items.count</key>
    <dict>
        <key>NSStringLocalizedFormatKey</key>
        <string>%#@items@</string>
        <key>items</key>
        <dict>
            <key>NSStringFormatSpecTypeKey</key>
            <string>NSStringPluralRuleType</string>
            <key>NSStringFormatValueTypeKey</key>
            <string>d</string>
            <key>zero</key>
            <string>Нет элементов</string>
            <key>one</key>
            <string>%d элемент</string>
            <key>few</key>
            <string>%d элемента</string>
            <key>many</key>
            <string>%d элементов</string>
            <key>other</key>
            <string>%d элементов</string>
        </dict>
    </dict>
</dict>
</plist>
```

```xml
<!-- ar.lproj/Localizable.stringsdict (Arabic - 6 plural forms) -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>items.count</key>
    <dict>
        <key>NSStringLocalizedFormatKey</key>
        <string>%#@items@</string>
        <key>items</key>
        <dict>
            <key>NSStringFormatSpecTypeKey</key>
            <string>NSStringPluralRuleType</string>
            <key>NSStringFormatValueTypeKey</key>
            <string>d</string>
            <key>zero</key>
            <string>لا عناصر</string>
            <key>one</key>
            <string>عنصر واحد</string>
            <key>two</key>
            <string>عنصران</string>
            <key>few</key>
            <string>%d عناصر</string>
            <key>many</key>
            <string>%d عنصرًا</string>
            <key>other</key>
            <string>%d عنصر</string>
        </dict>
    </dict>
</dict>
</plist>
```

## Language Manager with Runtime Switching

```swift
import SwiftUI
import Combine

// MARK: - Supported Languages

enum AppLanguage: String, CaseIterable, Identifiable {
    case system = "system"
    case english = "en"
    case arabic = "ar"
    case spanish = "es"
    case french = "fr"
    case german = "de"
    case russian = "ru"
    case japanese = "ja"
    case chinese = "zh-Hans"

    var id: String { rawValue }

    var displayName: String {
        switch self {
        case .system:
            return NSLocalizedString("language.system", comment: "System language")
        case .english:
            return "English"
        case .arabic:
            return "العربية"
        case .spanish:
            return "Español"
        case .french:
            return "Français"
        case .german:
            return "Deutsch"
        case .russian:
            return "Русский"
        case .japanese:
            return "日本語"
        case .chinese:
            return "简体中文"
        }
    }

    var isRTL: Bool {
        switch self {
        case .arabic:
            return true
        default:
            return false
        }
    }

    var locale: Locale {
        if self == .system {
            return .current
        }
        return Locale(identifier: rawValue)
    }
}

// MARK: - Language Manager

@MainActor
final class LanguageManager: ObservableObject {

    static let shared = LanguageManager()

    // MARK: - Published Properties

    @Published private(set) var currentLanguage: AppLanguage = .system
    @Published private(set) var layoutDirection: LayoutDirection = .leftToRight

    // MARK: - Persistence

    @AppStorage("selectedLanguage") private var storedLanguage: String = AppLanguage.system.rawValue

    // MARK: - Bundle

    private var localizedBundle: Bundle?

    // MARK: - Initialization

    private init() {
        loadSavedLanguage()
        setupNotifications()
    }

    private func loadSavedLanguage() {
        if let language = AppLanguage(rawValue: storedLanguage) {
            setLanguage(language, persist: false)
        }
    }

    private func setupNotifications() {
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(localeDidChange),
            name: NSLocale.currentLocaleDidChangeNotification,
            object: nil
        )
    }

    @objc private func localeDidChange() {
        if currentLanguage == .system {
            updateLayoutDirection()
        }
    }

    // MARK: - Language Setting

    func setLanguage(_ language: AppLanguage, persist: Bool = true) {
        currentLanguage = language

        if persist {
            storedLanguage = language.rawValue
        }

        // Update bundle
        if language == .system {
            localizedBundle = nil
            UserDefaults.standard.removeObject(forKey: "AppleLanguages")
        } else {
            if let path = Bundle.main.path(forResource: language.rawValue, ofType: "lproj"),
               let bundle = Bundle(path: path) {
                localizedBundle = bundle
            }
            UserDefaults.standard.set([language.rawValue], forKey: "AppleLanguages")
        }

        updateLayoutDirection()

        // Post notification for views to update
        NotificationCenter.default.post(name: .languageDidChange, object: nil)
    }

    private func updateLayoutDirection() {
        let effectiveLanguage = currentLanguage == .system
            ? AppLanguage(rawValue: Locale.current.language.languageCode?.identifier ?? "en") ?? .english
            : currentLanguage

        layoutDirection = effectiveLanguage.isRTL ? .rightToLeft : .leftToRight
    }

    // MARK: - Localization

    func localizedString(_ key: String, table: String? = nil, comment: String = "") -> String {
        if let bundle = localizedBundle {
            return NSLocalizedString(key, tableName: table, bundle: bundle, comment: comment)
        }
        return NSLocalizedString(key, tableName: table, comment: comment)
    }

    func localizedString(_ key: String, arguments: CVarArg...) -> String {
        let format = localizedString(key)
        return String(format: format, arguments: arguments)
    }

    // MARK: - Current Locale

    var effectiveLocale: Locale {
        if currentLanguage == .system {
            return .current
        }
        return currentLanguage.locale
    }
}

// MARK: - Notification Extension

extension Notification.Name {
    static let languageDidChange = Notification.Name("languageDidChange")
}

// MARK: - Environment Integration

private struct LanguageManagerKey: EnvironmentKey {
    static let defaultValue = LanguageManager.shared
}

extension EnvironmentValues {
    var languageManager: LanguageManager {
        get { self[LanguageManagerKey.self] }
        set { self[LanguageManagerKey.self] = newValue }
    }
}
```

## RTL-Aware Layout Components

```swift
import SwiftUI

// MARK: - RTL Environment Key

private struct IsRTLKey: EnvironmentKey {
    static let defaultValue = false
}

extension EnvironmentValues {
    var isRTL: Bool {
        get { self[IsRTLKey.self] }
        set { self[IsRTLKey.self] = newValue }
    }
}

// MARK: - RTL Container

struct RTLContainer<Content: View>: View {
    @ObservedObject private var languageManager = LanguageManager.shared
    let content: Content

    init(@ViewBuilder content: () -> Content) {
        self.content = content()
    }

    var body: some View {
        content
            .environment(\.layoutDirection, languageManager.layoutDirection)
            .environment(\.isRTL, languageManager.layoutDirection == .rightToLeft)
    }
}

// MARK: - Semantic Padding

struct SemanticPadding: ViewModifier {
    let leading: CGFloat
    let trailing: CGFloat
    let top: CGFloat
    let bottom: CGFloat

    @Environment(\.layoutDirection) private var layoutDirection

    func body(content: Content) -> some View {
        content.padding(EdgeInsets(
            top: top,
            leading: leading,
            bottom: bottom,
            trailing: trailing
        ))
    }
}

extension View {
    func semanticPadding(
        leading: CGFloat = 0,
        trailing: CGFloat = 0,
        top: CGFloat = 0,
        bottom: CGFloat = 0
    ) -> some View {
        modifier(SemanticPadding(
            leading: leading,
            trailing: trailing,
            top: top,
            bottom: bottom
        ))
    }
}

// MARK: - Force LTR Modifier

struct ForceLTRModifier: ViewModifier {
    func body(content: Content) -> some View {
        content
            .environment(\.layoutDirection, .leftToRight)
    }
}

extension View {
    /// Force left-to-right layout for content that shouldn't flip (code, URLs, numbers)
    func forceLTR() -> some View {
        modifier(ForceLTRModifier())
    }
}

// MARK: - RTL-Aware Stack

struct AdaptiveHStack<Content: View>: View {
    @Environment(\.layoutDirection) private var layoutDirection

    let alignment: VerticalAlignment
    let spacing: CGFloat?
    let content: Content

    init(
        alignment: VerticalAlignment = .center,
        spacing: CGFloat? = nil,
        @ViewBuilder content: () -> Content
    ) {
        self.alignment = alignment
        self.spacing = spacing
        self.content = content()
    }

    var body: some View {
        HStack(alignment: alignment, spacing: spacing) {
            content
        }
    }
}

// MARK: - RTL-Aware Icon

struct DirectionalIcon: View {
    let systemName: String
    let flipsForRTL: Bool

    @Environment(\.layoutDirection) private var layoutDirection

    init(_ systemName: String, flipsForRTL: Bool = true) {
        self.systemName = systemName
        self.flipsForRTL = flipsForRTL
    }

    var body: some View {
        Image(systemName: systemName)
            .scaleEffect(x: shouldFlip ? -1 : 1, y: 1)
    }

    private var shouldFlip: Bool {
        flipsForRTL && layoutDirection == .rightToLeft
    }
}

// MARK: - RTL-Aware Alignment

extension HorizontalAlignment {
    static var adaptiveLeading: HorizontalAlignment {
        .leading
    }

    static var adaptiveTrailing: HorizontalAlignment {
        .trailing
    }
}

// MARK: - Usage Example

struct RTLExampleView: View {
    @Environment(\.layoutDirection) private var layoutDirection

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            // Regular text - will flow RTL in Arabic
            Text("This text respects RTL direction")

            // Icon that flips
            HStack {
                DirectionalIcon("arrow.right")
                Text("Next")
            }

            // Phone number - should NOT flip
            Text("+1 (555) 123-4567")
                .forceLTR()

            // Code snippet - should NOT flip
            Text("let x = 42")
                .font(.monospaced(.body)())
                .forceLTR()

            // URL - should NOT flip
            Text("https://example.com")
                .forceLTR()

            // Mixed content
            HStack {
                Text("Price:")
                Text("$99.99")
                    .forceLTR()
            }
        }
        .padding()
    }
}
```

## Locale-Aware Formatters

```swift
import Foundation

// MARK: - Formatters Manager

@MainActor
final class LocalizedFormatters: ObservableObject {

    static let shared = LocalizedFormatters()

    @Published private(set) var locale: Locale

    private var cancellables = Set<AnyCancellable>()

    // Cached formatters
    private var dateFormatters: [String: DateFormatter] = [:]
    private var numberFormatter: NumberFormatter?
    private var currencyFormatters: [String: NumberFormatter] = [:]
    private var relativeFormatter: RelativeDateTimeFormatter?

    private init() {
        self.locale = LanguageManager.shared.effectiveLocale
        observeLanguageChanges()
    }

    private func observeLanguageChanges() {
        NotificationCenter.default.publisher(for: .languageDidChange)
            .sink { [weak self] _ in
                self?.updateLocale()
            }
            .store(in: &cancellables)
    }

    private func updateLocale() {
        locale = LanguageManager.shared.effectiveLocale
        clearCaches()
    }

    private func clearCaches() {
        dateFormatters.removeAll()
        numberFormatter = nil
        currencyFormatters.removeAll()
        relativeFormatter = nil
    }

    // MARK: - Date Formatting

    func formatDate(_ date: Date, style: DateFormatter.Style = .medium) -> String {
        let key = "date_\(style.rawValue)"

        if dateFormatters[key] == nil {
            let formatter = DateFormatter()
            formatter.locale = locale
            formatter.dateStyle = style
            formatter.timeStyle = .none
            dateFormatters[key] = formatter
        }

        return dateFormatters[key]!.string(from: date)
    }

    func formatTime(_ date: Date, style: DateFormatter.Style = .short) -> String {
        let key = "time_\(style.rawValue)"

        if dateFormatters[key] == nil {
            let formatter = DateFormatter()
            formatter.locale = locale
            formatter.dateStyle = .none
            formatter.timeStyle = style
            dateFormatters[key] = formatter
        }

        return dateFormatters[key]!.string(from: date)
    }

    func formatDateTime(_ date: Date, dateStyle: DateFormatter.Style = .medium, timeStyle: DateFormatter.Style = .short) -> String {
        let key = "datetime_\(dateStyle.rawValue)_\(timeStyle.rawValue)"

        if dateFormatters[key] == nil {
            let formatter = DateFormatter()
            formatter.locale = locale
            formatter.dateStyle = dateStyle
            formatter.timeStyle = timeStyle
            dateFormatters[key] = formatter
        }

        return dateFormatters[key]!.string(from: date)
    }

    func formatRelative(_ date: Date) -> String {
        if relativeFormatter == nil {
            let formatter = RelativeDateTimeFormatter()
            formatter.locale = locale
            formatter.unitsStyle = .full
            relativeFormatter = formatter
        }

        return relativeFormatter!.localizedString(for: date, relativeTo: Date())
    }

    // MARK: - Number Formatting

    func formatNumber(_ number: Double, fractionDigits: Int = 0) -> String {
        if numberFormatter == nil {
            let formatter = NumberFormatter()
            formatter.locale = locale
            formatter.numberStyle = .decimal
            numberFormatter = formatter
        }

        numberFormatter!.minimumFractionDigits = fractionDigits
        numberFormatter!.maximumFractionDigits = fractionDigits

        return numberFormatter!.string(from: NSNumber(value: number)) ?? "\(number)"
    }

    func formatInteger(_ number: Int) -> String {
        formatNumber(Double(number), fractionDigits: 0)
    }

    func formatPercent(_ value: Double) -> String {
        let formatter = NumberFormatter()
        formatter.locale = locale
        formatter.numberStyle = .percent
        formatter.minimumFractionDigits = 0
        formatter.maximumFractionDigits = 1

        return formatter.string(from: NSNumber(value: value)) ?? "\(value * 100)%"
    }

    // MARK: - Currency Formatting

    func formatCurrency(_ amount: Double, currencyCode: String) -> String {
        if currencyFormatters[currencyCode] == nil {
            let formatter = NumberFormatter()
            formatter.locale = locale
            formatter.numberStyle = .currency
            formatter.currencyCode = currencyCode
            currencyFormatters[currencyCode] = formatter
        }

        return currencyFormatters[currencyCode]!.string(from: NSNumber(value: amount)) ?? "\(amount)"
    }

    // MARK: - File Size Formatting

    func formatFileSize(_ bytes: Int64) -> String {
        let formatter = ByteCountFormatter()
        formatter.countStyle = .file
        return formatter.string(fromByteCount: bytes)
    }

    // MARK: - Duration Formatting

    func formatDuration(_ seconds: TimeInterval) -> String {
        let formatter = DateComponentsFormatter()
        formatter.unitsStyle = .abbreviated
        formatter.allowedUnits = [.hour, .minute, .second]
        return formatter.string(from: seconds) ?? ""
    }
}

// MARK: - SwiftUI Extensions

extension Text {
    init(localizedDate date: Date, style: DateFormatter.Style = .medium) {
        self.init(LocalizedFormatters.shared.formatDate(date, style: style))
    }

    init(localizedNumber number: Double, fractionDigits: Int = 0) {
        self.init(LocalizedFormatters.shared.formatNumber(number, fractionDigits: fractionDigits))
    }

    init(localizedCurrency amount: Double, code: String) {
        self.init(LocalizedFormatters.shared.formatCurrency(amount, currencyCode: code))
    }
}
```

## Language Picker Component

```swift
import SwiftUI

// MARK: - Language Picker

struct LanguagePicker: View {
    @ObservedObject private var languageManager = LanguageManager.shared
    @State private var showRestartAlert = false

    var body: some View {
        List {
            Section {
                ForEach(AppLanguage.allCases) { language in
                    LanguageRow(
                        language: language,
                        isSelected: languageManager.currentLanguage == language
                    ) {
                        selectLanguage(language)
                    }
                }
            } header: {
                Text(L10n.Settings.Language.title)
            } footer: {
                Text(L10n.Settings.Language.footer)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
        .navigationTitle(L10n.Settings.Language.navTitle)
        .alert(L10n.Settings.Language.restartTitle, isPresented: $showRestartAlert) {
            Button(L10n.Common.cancel, role: .cancel) {}
            Button(L10n.Settings.Language.restartButton) {
                restartApp()
            }
        } message: {
            Text(L10n.Settings.Language.restartMessage)
        }
    }

    private func selectLanguage(_ language: AppLanguage) {
        if language != languageManager.currentLanguage {
            languageManager.setLanguage(language)
            showRestartAlert = true
        }
    }

    private func restartApp() {
        // Trigger app restart
        exit(0)
    }
}

// MARK: - Language Row

struct LanguageRow: View {
    let language: AppLanguage
    let isSelected: Bool
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            HStack {
                VStack(alignment: .leading, spacing: 2) {
                    Text(language.displayName)
                        .foregroundColor(.primary)

                    if language != .system {
                        Text(language.locale.localizedString(forIdentifier: language.rawValue) ?? "")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                }

                Spacer()

                if isSelected {
                    Image(systemName: "checkmark")
                        .foregroundColor(.accentColor)
                }
            }
        }
    }
}
```

## String Catalog (Xcode 15+)

```swift
// MARK: - Using String Catalogs (.xcstrings)

/*
String Catalogs provide a modern approach to localization in Xcode 15+.

Benefits:
- All strings in one file per target
- Built-in support for plurals and device variations
- Automatic extraction of strings from code
- Visual editor in Xcode
- Git-friendly JSON format

Usage:
1. Create new "String Catalog" file in Xcode
2. Use String(localized:) for compile-time checked strings
*/

// MARK: - Modern String Localization (iOS 16+)

struct ModernLocalization {

    // Basic localized string
    static let welcomeTitle = String(localized: "welcome.title")

    // With default value
    static let loginButton = String(localized: "login.button", defaultValue: "Sign In")

    // With comment for translators
    static let logoutConfirm = String(
        localized: "logout.confirm.message",
        comment: "Shown when user taps logout button"
    )

    // With table (separate strings file)
    static let settingsTitle = String(
        localized: "settings.title",
        table: "Settings"
    )

    // Interpolated string
    static func greeting(name: String) -> String {
        String(localized: "greeting.message \(name)")
    }

    // Plural support
    static func itemCount(_ count: Int) -> String {
        String(localized: "items.count \(count)")
    }
}

// MARK: - AttributedString Localization

struct AttributedLocalization {

    // Localized attributed string with markdown
    static var termsAndConditions: AttributedString {
        try! AttributedString(
            localized: "terms.markdown",
            including: \.foundation
        )
    }

    // With custom attributes
    static func formattedPrice(_ price: Double) -> AttributedString {
        var string = AttributedString(
            localized: "price.formatted \(price, format: .currency(code: "USD"))"
        )
        string.font = .headline
        return string
    }
}

// MARK: - SwiftUI Text with Localization

struct LocalizedTextExamples: View {
    let itemCount: Int
    let userName: String

    var body: some View {
        VStack {
            // Simple localized string
            Text("welcome.title")

            // Interpolated
            Text("greeting.message \(userName)")

            // Plural
            Text("items.count \(itemCount)")

            // With markdown
            Text("terms.markdown")

            // Formatted value
            Text("price.value \(99.99, format: .currency(code: "USD"))")

            // Date
            Text("last.updated \(Date.now, format: .dateTime)")
        }
    }
}
```

## Testing Localization

```swift
import XCTest
@testable import YourApp

// MARK: - Localization Tests

final class LocalizationTests: XCTestCase {

    // MARK: - String Existence Tests

    func testAllLocalizedStringsExist() {
        let languages = ["en", "ar", "es", "fr", "de"]

        for language in languages {
            guard let bundlePath = Bundle.main.path(forResource: language, ofType: "lproj"),
                  let bundle = Bundle(path: bundlePath) else {
                XCTFail("Missing localization bundle for: \(language)")
                continue
            }

            // Test critical strings exist
            let criticalKeys = [
                "common.ok",
                "common.cancel",
                "common.error",
                "auth.login.title",
                "auth.login.submit_button"
            ]

            for key in criticalKeys {
                let localized = NSLocalizedString(key, tableName: nil, bundle: bundle, comment: "")
                XCTAssertNotEqual(localized, key, "Missing translation for '\(key)' in \(language)")
            }
        }
    }

    // MARK: - Plural Tests

    func testPluralStrings() {
        let testCases = [
            (0, "No items"),
            (1, "1 item"),
            (2, "2 items"),
            (5, "5 items"),
            (21, "21 items")
        ]

        for (count, expected) in testCases {
            let result = String.localizedStringWithFormat(
                NSLocalizedString("items.count", comment: ""),
                count
            )
            XCTAssertEqual(result, expected, "Plural failed for count: \(count)")
        }
    }

    // MARK: - Format String Tests

    func testFormatStrings() {
        // Test that format strings have correct placeholders
        let greeting = String(format: NSLocalizedString("user.greeting", comment: ""), "John")
        XCTAssertTrue(greeting.contains("John"), "Format string should contain the name")
        XCTAssertFalse(greeting.contains("%@"), "Format placeholder should be replaced")
    }

    // MARK: - RTL Tests

    func testRTLLanguageDetection() {
        let rtlLanguages: [AppLanguage] = [.arabic]
        let ltrLanguages: [AppLanguage] = [.english, .spanish, .french, .german]

        for language in rtlLanguages {
            XCTAssertTrue(language.isRTL, "\(language.displayName) should be RTL")
        }

        for language in ltrLanguages {
            XCTAssertFalse(language.isRTL, "\(language.displayName) should be LTR")
        }
    }

    // MARK: - Formatter Tests

    func testDateFormatting() {
        let date = Date(timeIntervalSince1970: 0)  // Jan 1, 1970
        let formatters = LocalizedFormatters.shared

        let formatted = formatters.formatDate(date, style: .medium)
        XCTAssertFalse(formatted.isEmpty, "Date should be formatted")
    }

    func testCurrencyFormatting() {
        let formatters = LocalizedFormatters.shared

        let usd = formatters.formatCurrency(99.99, currencyCode: "USD")
        XCTAssertTrue(usd.contains("99") || usd.contains("٩٩"), "Currency should contain the amount")

        let eur = formatters.formatCurrency(99.99, currencyCode: "EUR")
        XCTAssertTrue(eur.contains("99") || eur.contains("٩٩"), "Currency should contain the amount")
    }

    // MARK: - String Length Tests

    func testStringLengthsForUI() {
        // German is typically 30% longer than English
        // Verify critical UI strings don't exceed reasonable lengths

        let maxLengths: [String: Int] = [
            "common.ok": 10,
            "common.cancel": 15,
            "auth.login.submit_button": 20
        ]

        let languages = ["en", "de", "fr", "es"]

        for language in languages {
            guard let bundlePath = Bundle.main.path(forResource: language, ofType: "lproj"),
                  let bundle = Bundle(path: bundlePath) else { continue }

            for (key, maxLength) in maxLengths {
                let localized = NSLocalizedString(key, tableName: nil, bundle: bundle, comment: "")
                if localized.count > maxLength {
                    // Warning, not failure - may need UI adjustment
                    print("Warning: '\(key)' in \(language) is \(localized.count) chars (max: \(maxLength))")
                }
            }
        }
    }
}

// MARK: - UI Tests for Localization

final class LocalizationUITests: XCTestCase {

    func testAppLaunchesInEachLanguage() {
        let languages = ["en", "ar", "es"]

        for language in languages {
            let app = XCUIApplication()
            app.launchArguments = ["-AppleLanguages", "(\(language))"]
            app.launch()

            // Verify app doesn't crash and shows content
            XCTAssertTrue(app.wait(for: .runningForeground, timeout: 5))

            app.terminate()
        }
    }

    func testRTLLayoutInArabic() {
        let app = XCUIApplication()
        app.launchArguments = ["-AppleLanguages", "(ar)"]
        app.launch()

        // Verify navigation bar back button is on the right
        // Add specific RTL layout assertions based on your UI

        app.terminate()
    }
}
```
