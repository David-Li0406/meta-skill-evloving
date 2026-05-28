# Localization Best Practices

> Key naming, placeholders, plurals, ICU MessageFormat

---

## 1. Key Naming Conventions

### Platform Casing

| Platform | Convention | Examples |
|----------|------------|----------|
| **iOS** | dot.notation.snake_case | `login.title`, `login.button.sign_in` |
| **Android** | snake_case | `login_title`, `login_button_sign_in` |
| **Flutter** | camelCase | `loginTitle`, `loginButtonSignIn` |

### Hierarchy Patterns

#### Screen-based
```
{screen}.{element}.{variant}

home.title
login.email.placeholder
login.button.sign_in
login.error.invalid_credentials
```

#### Feature-based
```
{feature}.{screen}.{element}

auth.login.title
auth.signup.title
portfolio.list.title
```

#### Shared Strings
```
common.{element}

common.ok
common.cancel
common.save
common.delete
common.error.network
```

### Contextual Keys

**Problem:** `close` có thể là close button, close window, close account?

**Solution:** Add context
```
dialog.button.close
account.action.close
window.button.close
```

### Anti-Patterns

| ❌ Bad | Reason | ✅ Good |
|--------|--------|---------|
| `label1`, `text2` | Non-descriptive | `login.email.label` |
| `loginScreenWelcomeMessageForNewUsers` | Too long | `login.welcome.new_user` |
| `btn_login`, `txt_email` | Unnecessary abbreviations | `login.button`, `login.email` |

---

## 2. Placeholders & Interpolation

### iOS Format
```swift
// Localizable.strings
"greeting.hello" = "Hello %@";
"inbox.message_count" = "You have %d new messages";

// Usage
let text = String(format: NSLocalizedString("greeting.hello", comment: ""), name)
```

### Android Format
```xml
<!-- strings.xml -->
<string name="greeting_hello">Hello %s</string>
<string name="inbox_message_count">You have %d new messages</string>

// Usage
getString(R.string.greeting_hello, name)
```

### Flutter Format (ICU)
```json
{
  "greetingHello": "Hello {name}",
  "@greetingHello": {
    "placeholders": {
      "name": { "type": "String" }
    }
  }
}
```

```dart
// Usage
AppLocalizations.of(context)!.greetingHello(name)
```

### Placeholder Rules

- ✅ Use named placeholders cho clarity
- ✅ Document placeholders trong metadata
- ❌ KHÔNG concatenate translated strings
- ❌ KHÔNG embed HTML trong translations

---

## 3. Pluralization

### iOS (.stringsdict)
```xml
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
```

### Android (plurals)
```xml
<plurals name="items_count">
    <item quantity="zero">No items</item>
    <item quantity="one">1 item</item>
    <item quantity="other">%d items</item>
</plurals>
```
```kotlin
resources.getQuantityString(R.plurals.items_count, count, count)
```

### Flutter (ICU)
```json
{
  "itemsCount": "{count, plural, zero{No items} one{1 item} other{{count} items}}"
}
```
```dart
AppLocalizations.of(context)!.itemsCount(count)
```

### Plural Categories

| Category | Description | Example Languages |
|----------|-------------|-------------------|
| zero | Zero quantity | Arabic |
| one | Singular | English, Vietnamese |
| two | Dual | Arabic, Welsh |
| few | Small numbers | Russian, Polish |
| many | Large numbers | Russian, Polish |
| other | Default (REQUIRED) | All |

> **Note:** English chỉ dùng `one` và `other`

---

## 4. ICU MessageFormat (Flutter)

### Gender Selection
```json
{
  "likedPost": "{gender, select, male{He} female{She} other{They}} liked your post"
}
```

### Combined (Plural + Gender)
```json
{
  "userItems": "{count, plural, one{{gender, select, male{He has} female{She has} other{They have}} 1 item} other{{gender, select, male{He has} female{She has} other{They have}} {count} items}}"
}
```

---

## 5. Common Mistakes

### ❌ Concatenating Strings
```swift
// WRONG
let text = NSLocalizedString("hello", comment: "") + " " + name

// RIGHT
let text = String(format: NSLocalizedString("greeting.hello", comment: ""), name)
```

### ❌ Logic in Translations
```
// WRONG
"greeting" = "Hello {if premium}Premium {endif}User"

// RIGHT - Use separate keys
"greeting.regular" = "Hello User"
"greeting.premium" = "Hello Premium User"
```

### ❌ Hardcoded Strings
```swift
// WRONG
Text("Welcome")

// RIGHT
Text(L10n.Home.welcome)
```

---

## 6. RTL Language Support

### Affected Languages
Arabic, Hebrew, Persian, Urdu

### Best Practices

| ❌ Avoid | ✅ Use |
|---------|-------|
| `left` / `right` | `leading` / `trailing` |
| Fixed padding left | `leadingPadding` |
| Text alignment left | `.natural` alignment |

### Testing
- Enable RTL in simulator
- Test all screens with Arabic/Hebrew
- Check icon mirroring

---

## Summary Checklist

- [ ] Keys follow platform convention (dot/snake/camel)
- [ ] Keys are descriptive and contextual
- [ ] Placeholders documented
- [ ] Plurals use proper format
- [ ] No string concatenation
- [ ] No hardcoded strings
- [ ] RTL languages supported

---

## Related Files

- **Architecture**: [architecture.md](architecture.md)
- **New Project Pipeline**: [pipeline_new_project.md](pipeline_new_project.md)
