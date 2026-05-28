# iOS Localization

> SwiftGen + Localizable.strings + MVVM integration

---

## Recommended Approach

| Aspect | Choice |
|--------|--------|
| Library | SwiftGen + Localizable.strings |
| Code Generation | SwiftGen → `L10n` enum |
| State Management | `@Published currentLocale` trong AppViewModel |
| Persistence | UserDefaults |

---

## Setup SwiftGen

### Installation

**Homebrew (recommended):**
```bash
brew install swiftgen
```

**SPM:**
```swift
.package(url: "https://github.com/SwiftGen/SwiftGen", from: "6.6.0")
```

### Configuration (swiftgen.yml)

```yaml
strings:
  inputs:
    - Resources/Localization/en.lproj
    - Resources/Localization/vi.lproj
  outputs:
    - templateName: structured-swift5
      output: Generated/Strings.swift
      params:
        enumName: L10n
```

### Xcode Build Phase

```bash
if which swiftgen >/dev/null; then
  swiftgen
else
  echo "warning: SwiftGen not installed"
fi
```

---

## Folder Structure

```
Resources/Localization/
├── en.lproj/
│   └── Localizable.strings
├── vi.lproj/
│   └── Localizable.strings
└── ja.lproj/
    └── Localizable.strings

Generated/
└── Strings.swift (SwiftGen output)
```

---

## Localizable.strings Format

```
/* Comment for translators */
"key" = "Value";

/* Common */
"common.ok" = "OK";
"common.cancel" = "Cancel";

/* Login Screen */
"login.title" = "Login";
"login.email.placeholder" = "Email";
"login.button.sign_in" = "Sign In";

/* With placeholder */
"login.greeting" = "Hello %@";
```

---

## MVVM Integration

### AppViewModel

```swift
class AppViewModel: ObservableObject {
  @Published var currentLocale: String = "en"
  
  private let localeStorage: LocaleStorageProtocol
  
  init(localeStorage: LocaleStorageProtocol = UserDefaultsLocaleStorage()) {
    self.localeStorage = localeStorage
  }
  
  func loadSavedLocale() {
    if let saved = localeStorage.loadLocale() {
      currentLocale = saved
      Bundle.setLanguage(saved)
    }
  }
  
  func changeLocale(_ locale: String) {
    currentLocale = locale
    localeStorage.saveLocale(locale)
    Bundle.setLanguage(locale)
    objectWillChange.send()
  }
}
```

### LocaleStorage

```swift
protocol LocaleStorageProtocol {
  func saveLocale(_ locale: String)
  func loadLocale() -> String?
}

class UserDefaultsLocaleStorage: LocaleStorageProtocol {
  private let key = "app_locale"
  
  func saveLocale(_ locale: String) {
    UserDefaults.standard.set(locale, forKey: key)
  }
  
  func loadLocale() -> String? {
    UserDefaults.standard.string(forKey: key)
  }
}
```

### Bundle Extension (Runtime Switching)

```swift
private var bundleKey: UInt8 = 0

extension Bundle {
  static func setLanguage(_ language: String) {
    defer {
      object_setClass(Bundle.main, CustomBundle.self)
    }
    
    objc_setAssociatedObject(
      Bundle.main,
      &bundleKey,
      Bundle.main.path(forResource: language, ofType: "lproj").flatMap(Bundle.init),
      .OBJC_ASSOCIATION_RETAIN_NONATOMIC
    )
  }
}

private class CustomBundle: Bundle {
  override func localizedString(forKey key: String, value: String?, table tableName: String?) -> String {
    guard let bundle = objc_getAssociatedObject(self, &bundleKey) as? Bundle else {
      return super.localizedString(forKey: key, value: value, table: tableName)
    }
    return bundle.localizedString(forKey: key, value: value, table: tableName)
  }
}
```

---

## Usage in Views

### With SwiftGen (Type-safe)

```swift
Text(L10n.Login.title)
Button(L10n.Login.Button.signIn) { viewModel.login() }

// With placeholder
let greeting = L10n.Login.greeting(userName)
Text(greeting)
```

### Without SwiftGen

```swift
Text(NSLocalizedString("login.title", comment: ""))

// With placeholder
let greeting = String(format: NSLocalizedString("login.greeting", comment: ""), userName)
```

---

## Language Switcher UI

```swift
struct SettingsView: View {
  @EnvironmentObject var appViewModel: AppViewModel
  
  var body: some View {
    Form {
      Section(header: Text(L10n.Settings.language)) {
        Picker(L10n.Settings.language, selection: $appViewModel.currentLocale) {
          Text("English").tag("en")
          Text("Tiếng Việt").tag("vi")
          Text("日本語").tag("ja")
        }
        .pickerStyle(.menu)
        .onChange(of: appViewModel.currentLocale) { newLocale in
          appViewModel.changeLocale(newLocale)
        }
      }
    }
  }
}
```

---

## Pluralization

### Localizable.stringsdict

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "...">
<plist version="1.0">
<dict>
  <key>items_count</key>
  <dict>
    <key>NSStringLocalizedFormatKey</key>
    <string>%#@item_count@</string>
    <key>item_count</key>
    <dict>
      <key>NSStringFormatSpecTypeKey</key>
      <string>NSStringPluralRuleType</string>
      <key>NSStringFormatValueTypeKey</key>
      <string>d</string>
      <key>zero</key><string>No items</string>
      <key>one</key><string>1 item</string>
      <key>other</key><string>%d items</string>
    </dict>
  </dict>
</dict>
</plist>
```

### Usage

```swift
let text = String.localizedStringWithFormat(
  NSLocalizedString("items_count", comment: ""),
  count
)
```

---

## Best Practices

- ✅ Use SwiftGen for type-safety
- ✅ Store locale in AppViewModel `@Published`
- ✅ Persist locale with UserDefaults
- ✅ Use Bundle extension for runtime switching
- ✅ Test with all supported languages
- ✅ Handle RTL with leading/trailing
- ✅ Use .stringsdict for plurals
- ✅ Provide context comments

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Translations not updating | Ensure `Bundle.setLanguage` called + `objectWillChange.send()` |
| SwiftGen not generating | Check swiftgen.yml, verify .strings location |
| Missing translations | Verify key exists in all .lproj folders |

---

## Related Files

- **Shared Architecture**: [../shared/architecture.md](../shared/architecture.md)
- **Best Practices**: [../shared/best_practices.md](../shared/best_practices.md)
