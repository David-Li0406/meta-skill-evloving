# Pipeline: New Project Localization

> Step-by-step setup localization cho dự án CHƯA có localization

---

## When to Use

- Project chưa có localization
- Bắt đầu từ zero
- Cần scan hardcoded strings và thay thế
- Setup localization tools lần đầu

---

## Overview

| Step | Task | Time |
|------|------|------|
| 1 | Choose languages | 5 min |
| 2 | Choose library | 10 min |
| 3 | Install dependencies | 15 min |
| 4 | Create folder structure | 10 min |
| 5 | Create base translation file | 15 min |
| 6 | Scan hardcoded strings | 30-60 min |
| 7 | Add strings to translation file | 30 min |
| 8 | Replace hardcoded strings | 30-60 min |
| 9 | Setup locale management | 20 min |
| 10 | Add language switcher | 15 min |

**Total:** 2-4 hours

---

## Step 1: Choose Languages

**Base Language:** English (en) - recommended cho keys và fallback

**Target Languages (common):**
- `vi` - Vietnamese
- `ja` - Japanese
- `zh` - Chinese
- `ko` - Korean
- `es` - Spanish

> **Tip:** Start với 2-3 languages, add more later

---

## Step 2: Choose Library

### iOS
**Recommended:** SwiftGen + Localizable.strings
- Native approach
- Type-safe (L10n enum)
- No external dependencies

### Android
**Recommended:** Native strings.xml
- Built-in
- Auto generates R.string.*

### Flutter
**Recommended:** intl + ARB files
- Official approach
- ICU MessageFormat
- Code generation

---

## Step 3: Install Dependencies

### iOS (SwiftGen)
```bash
# Homebrew
brew install swiftgen

# Or SPM (Package.swift)
.package(url: "https://github.com/SwiftGen/SwiftGen", from: "6.6.0")
```

**swiftgen.yml:**
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

### Android
No installation needed - built-in!

### Flutter
```yaml
# pubspec.yaml
dependencies:
  flutter_localizations:
    sdk: flutter
  intl: ^0.18.0
  shared_preferences: ^2.0.0
```

**l10n.yaml:**
```yaml
arb-dir: lib/l10n
template-arb-file: app_en.arb
output-localization-file: app_localizations.dart
output-class: AppLocalizations
```

---

## Step 4: Create Folder Structure

### iOS
```
Resources/Localization/
├── en.lproj/
│   └── Localizable.strings
├── vi.lproj/
│   └── Localizable.strings
└── ja.lproj/
    └── Localizable.strings
```

### Android
```
res/
├── values/
│   └── strings.xml
├── values-vi/
│   └── strings.xml
└── values-ja/
    └── strings.xml
```

### Flutter
```
lib/l10n/
├── app_en.arb
├── app_vi.arb
└── app_ja.arb
```

---

## Step 5: Create Base Translation File

### iOS (Localizable.strings)
```
/* Common */
"common.ok" = "OK";
"common.cancel" = "Cancel";

/* Login Screen */
"login.title" = "Login";
"login.email.placeholder" = "Email";
"login.button.sign_in" = "Sign In";
```

### Android (strings.xml)
```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <!-- Common -->
    <string name="common_ok">OK</string>
    <string name="common_cancel">Cancel</string>
    
    <!-- Login Screen -->
    <string name="login_title">Login</string>
    <string name="login_email_placeholder">Email</string>
    <string name="login_button_sign_in">Sign In</string>
</resources>
```

### Flutter (app_en.arb)
```json
{
  "commonOk": "OK",
  "commonCancel": "Cancel",
  "loginTitle": "Login",
  "loginEmailPlaceholder": "Email",
  "loginButtonSignIn": "Sign In"
}
```

---

## Step 6: Scan Hardcoded Strings

### Search Patterns

**iOS:**
```bash
# Find hardcoded strings
grep -rn "Text(\"" --include="*.swift"
grep -rn "Button(\"" --include="*.swift"
grep -rn "Label(\"" --include="*.swift"
```

**Android:**
```bash
# Find hardcoded strings
grep -rn "android:text=\"[^@]" --include="*.xml"
grep -rn "setText(\"" --include="*.kt" --include="*.java"
```

**Flutter:**
```bash
# Find hardcoded strings
grep -rn "Text(\"" --include="*.dart"
grep -rn "\"[A-Z].*\"" --include="*.dart"
```

### Document Findings

| Location | Current Text | Proposed Key |
|----------|--------------|--------------|
| LoginView.swift:15 | "Welcome" | login.welcome |
| LoginView.swift:23 | "Sign In" | login.button.sign_in |

---

## Step 7: Add Strings to Translation File

Add tất cả strings đã scan vào base translation file với key naming conventions.

---

## Step 8: Replace Hardcoded Strings

### iOS
```swift
// Before
Text("Welcome")

// After (with SwiftGen)
Text(L10n.Login.welcome)
```

### Android
```kotlin
// Before
binding.titleText.text = "Welcome"

// After
binding.titleText.text = getString(R.string.login_welcome)
```

### Flutter
```dart
// Before
Text("Welcome")

// After
Text(AppLocalizations.of(context)!.loginWelcome)
```

---

## Step 9: Setup Locale Management

### iOS - AppViewModel
```swift
class AppViewModel: ObservableObject {
  @Published var currentLocale: String = "en"
  
  func changeLocale(_ locale: String) {
    currentLocale = locale
    UserDefaults.standard.set(locale, forKey: "app_locale")
    Bundle.setLanguage(locale)
    objectWillChange.send()
  }
}
```

### Android - ViewModel
```kotlin
class AppViewModel(private val storage: LocaleStorage) : ViewModel() {
  private val _currentLocale = MutableStateFlow("en")
  val currentLocale: StateFlow<String> = _currentLocale.asStateFlow()
  
  fun changeLocale(context: Context, locale: String) {
    _currentLocale.value = locale
    storage.saveLocale(locale)
    (context as? Activity)?.recreate()
  }
}
```

### Flutter - Provider
```dart
class LocaleProvider extends ChangeNotifier {
  Locale _locale = const Locale('en');
  
  Future<void> changeLocale(Locale newLocale) async {
    _locale = newLocale;
    await _prefs.setString('app_locale', newLocale.languageCode);
    notifyListeners();
  }
}
```

---

## Step 10: Add Language Switcher

### iOS
```swift
struct SettingsView: View {
  @EnvironmentObject var appViewModel: AppViewModel
  
  var body: some View {
    Picker("Language", selection: $appViewModel.currentLocale) {
      Text("English").tag("en")
      Text("Tiếng Việt").tag("vi")
    }
    .onChange(of: appViewModel.currentLocale) { newLocale in
      appViewModel.changeLocale(newLocale)
    }
  }
}
```

### Flutter
```dart
DropdownButton<Locale>(
  value: locale,
  onChanged: (newLocale) {
    if (newLocale != null) {
      localeProvider.changeLocale(newLocale);
    }
  },
  items: const [
    DropdownMenuItem(value: Locale('en'), child: Text('English')),
    DropdownMenuItem(value: Locale('vi'), child: Text('Tiếng Việt')),
  ],
)
```

---

## Final Checklist

- [ ] Base language file created
- [ ] All target language files created
- [ ] Code generation configured (SwiftGen/intl)
- [ ] All hardcoded strings replaced
- [ ] LocaleStorage implemented
- [ ] ViewModel locale management
- [ ] Language switcher UI
- [ ] Test all languages

---

## Related Files

- **Architecture**: [architecture.md](architecture.md)
- **Best Practices**: [best_practices.md](best_practices.md)
- **Add Text Pipeline**: [pipeline_add_text.md](pipeline_add_text.md)
