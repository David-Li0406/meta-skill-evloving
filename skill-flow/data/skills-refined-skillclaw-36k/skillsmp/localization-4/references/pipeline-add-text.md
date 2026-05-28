# Pipeline: Add New Localization Text

> Step-by-step thêm text mới vào dự án ĐÃ có localization setup

---

## When to Use

- Project **đã có** localization setup
- Cần thêm translation key cho feature/screen mới
- Adding new UI text cần localize

**Time:** 10-30 minutes

---

## Quick Steps

| Step | Task | Time |
|------|------|------|
| 1 | Identify text cần localize | 5 min |
| 2 | Choose key name | 2 min |
| 3 | Add to base language file | 3 min |
| 4 | Add translations | 5-15 min |
| 5 | Regenerate code (if needed) | 1 min |
| 6 | Use key in code | 2 min |

---

## Step 1: Identify Text

### Example Scenarios

**New Screen (HomeView):**
- "Welcome to Dashboard" (title)
- "Refresh" (button)
- "Load More" (button)
- "No data available" (empty state)

**New Feature (Biometric):**
- "Enable Biometric Login" (toggle)
- "Authenticate with Face ID" (button)
- "Biometric authentication failed" (error)

**New Error:**
- "Please enter a valid phone number"
- "Phone number is required"

### Checklist

- [ ] All visible UI text
- [ ] Error messages
- [ ] Placeholder text
- [ ] Confirmation dialogs
- [ ] Plurals (1 item vs 2 items)
- [ ] Dynamic text với placeholders

---

## Step 2: Choose Key Name

### Platform Conventions

| Platform | Convention | Example |
|----------|------------|---------|
| iOS | dot.notation | `home.title` |
| Android | snake_case | `home_title` |
| Flutter | camelCase | `homeTitle` |

### Key Patterns

| Type | iOS | Android | Flutter |
|------|-----|---------|---------|
| Title | `home.title` | `home_title` | `homeTitle` |
| Button | `home.button.refresh` | `home_button_refresh` | `homeButtonRefresh` |
| Placeholder | `home.search.placeholder` | `home_search_placeholder` | `homeSearchPlaceholder` |
| Error | `home.error.load_failed` | `home_error_load_failed` | `homeErrorLoadFailed` |
| Empty state | `home.empty_state.message` | `home_empty_state_message` | `homeEmptyStateMessage` |

---

## Step 3: Add to Base Language File

### iOS (Localizable.strings)
```
/* Home Screen */
"home.title" = "Welcome to Dashboard";
"home.button.refresh" = "Refresh";
"home.button.load_more" = "Load More";
"home.empty_state.message" = "No data available";
```

**Location:** `Resources/Localization/en.lproj/Localizable.strings`

### Android (strings.xml)
```xml
<!-- Home Screen -->
<string name="home_title">Welcome to Dashboard</string>
<string name="home_button_refresh">Refresh</string>
<string name="home_button_load_more">Load More</string>
<string name="home_empty_state_message">No data available</string>
```

**Location:** `res/values/strings.xml`

### Flutter (app_en.arb)
```json
{
  "homeTitle": "Welcome to Dashboard",
  "@homeTitle": { "description": "Home screen title" },
  "homeButtonRefresh": "Refresh",
  "homeButtonLoadMore": "Load More",
  "homeEmptyStateMessage": "No data available"
}
```

**Location:** `lib/l10n/app_en.arb`

---

## Step 4: Add Translations

### iOS (vi.lproj/Localizable.strings)
```
"home.title" = "Chào mừng đến Dashboard";
"home.button.refresh" = "Làm mới";
"home.button.load_more" = "Tải thêm";
"home.empty_state.message" = "Không có dữ liệu";
```

### Android (values-vi/strings.xml)
```xml
<string name="home_title">Chào mừng đến Dashboard</string>
<string name="home_button_refresh">Làm mới</string>
<string name="home_button_load_more">Tải thêm</string>
<string name="home_empty_state_message">Không có dữ liệu</string>
```

### Flutter (app_vi.arb)
```json
{
  "homeTitle": "Chào mừng đến Dashboard",
  "homeButtonRefresh": "Làm mới",
  "homeButtonLoadMore": "Tải thêm",
  "homeEmptyStateMessage": "Không có dữ liệu"
}
```

---

## Step 5: Regenerate Code

### iOS (SwiftGen)
```bash
swiftgen
# Or build project in Xcode (if Build Phase configured)
```

### Android
Automatic on build - no action needed!

### Flutter
```bash
flutter gen-l10n
# Or run flutter pub get
```

---

## Step 6: Use Key in Code

### iOS (SwiftGen)
```swift
struct HomeView: View {
  var body: some View {
    VStack {
      Text(L10n.Home.title)
      
      Button(L10n.Home.Button.refresh) { refresh() }
      
      Button(L10n.Home.Button.loadMore) { loadMore() }
      
      if items.isEmpty {
        Text(L10n.Home.EmptyState.message)
      }
    }
  }
}
```

### Android
```kotlin
// In code
binding.titleText.text = getString(R.string.home_title)

// In XML
android:text="@string/home_title"
```

### Flutter
```dart
final l10n = AppLocalizations.of(context)!;

Text(l10n.homeTitle)
ElevatedButton(
  child: Text(l10n.homeButtonRefresh),
  onPressed: () { refresh(); },
)
```

---

## Special Cases

### Placeholders

**iOS:**
```
"home.greeting" = "Hello %@";
```
```swift
let text = String(format: L10n.Home.greeting, userName)
```

**Android:**
```xml
<string name="home_greeting">Hello %s</string>
```
```kotlin
getString(R.string.home_greeting, userName)
```

**Flutter:**
```json
{
  "homeGreeting": "Hello {name}",
  "@homeGreeting": {
    "placeholders": { "name": { "type": "String" } }
  }
}
```
```dart
l10n.homeGreeting(userName)
```

### Plurals

**Flutter:**
```json
{
  "itemsCount": "{count, plural, zero{No items} one{1 item} other{{count} items}}"
}
```

---

## Checklist

- [ ] Key follows platform naming convention
- [ ] Added to base language file
- [ ] Added to ALL target language files
- [ ] Code regenerated (SwiftGen/intl)
- [ ] Used in code correctly
- [ ] Tested in all languages

---

## Related Files

- **Best Practices**: [best_practices.md](best_practices.md)
- **Architecture**: [architecture.md](architecture.md)
