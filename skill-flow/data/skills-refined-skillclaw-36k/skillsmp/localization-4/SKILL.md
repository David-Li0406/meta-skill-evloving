---
name: localization
description: 'Multi-platform localization (iOS, Android, Flutter). Sử dụng skill này khi setup localization mới, thêm text, hoặc cần best practices về đa ngôn ngữ.'
---

# Localization Skill

> Multi-platform localization guide cho iOS, Android và Flutter

---

## 🎯 Khi Nào Sử Dụng Skill Này

| User Request | Action |
|--------------|--------|
| Setup localization mới | Đọc [references/pipeline-new-project.md](references/pipeline-new-project.md) |
| Thêm text mới | Đọc [references/pipeline-add-text.md](references/pipeline-add-text.md) |
| Best practices | Đọc [references/best-practices.md](references/best-practices.md) |
| iOS localization | Đọc [references/ios-localization.md](references/ios-localization.md) |
| Android localization | Đọc [references/android-localization.md](references/android-localization.md) |
| Flutter localization | Đọc [references/flutter-localization.md](references/flutter-localization.md) |

---

## 📐 Architecture Overview

```
┌─────────────────────────────────────────────────┐
│  Presentation Layer                             │
│  ├── View (hiển thị L10n.key)                   │
│  └── ViewModel (@Published currentLocale)        │
├─────────────────────────────────────────────────┤
│  Data Layer                                     │
│  └── LocaleStorage (UserDefaults/SharedPrefs)   │
└─────────────────────────────────────────────────┘
```

### Core Principles

1. **Separation of Concerns** - Locale state trong ViewModel/Provider
2. **Type Safety** - Code generation (SwiftGen, R.string, AppLocalizations)
3. **Dynamic Switching** - Runtime language change
4. **Persistence** - Save user preference
5. **Fallback** - Luôn có base language (English)

---

## 📱 Platform Quick Reference

| Platform | File Format | Key Convention | Code Gen |
|----------|-------------|----------------|----------|
| **iOS** | `.strings` | `login.title` (dot.notation) | SwiftGen → `L10n` |
| **Android** | `.xml` | `login_title` (snake_case) | Auto `R.string` |
| **Flutter** | `.arb` | `loginTitle` (camelCase) | `flutter gen-l10n` |

---

## 📋 Key Naming Convention

### iOS (dot.notation)
```
login.title
login.email.placeholder
login.button.sign_in
login.error.invalid_credentials
```

### Android (snake_case)
```xml
<string name="login_title">Đăng nhập</string>
<string name="login_email_placeholder">Email</string>
<string name="login_button_sign_in">Đăng nhập</string>
```

### Flutter (camelCase)
```json
{
  "loginTitle": "Đăng nhập",
  "loginEmailPlaceholder": "Email",
  "loginButtonSignIn": "Đăng nhập"
}
```

---

## 🚀 Quick Workflows

### 1. Setup Localization (Dự án mới)

**iOS:**
```bash
# 1. Install SwiftGen
brew install swiftgen

# 2. Create Localizable.strings
mkdir -p Resources/en.lproj
touch Resources/en.lproj/Localizable.strings

# 3. Configure swiftgen.yml
# 4. Run: swiftgen
```

**Android:**
```bash
# 1. Create strings.xml
mkdir -p app/src/main/res/values
touch app/src/main/res/values/strings.xml

# 2. Add base strings
# 3. Android Studio auto-generates R.string
```

**Flutter:**
```bash
# 1. Add to pubspec.yaml
flutter:
  generate: true

# 2. Create l10n.yaml
# 3. Create lib/l10n/app_en.arb
# 4. Run: flutter gen-l10n
```

### 2. Thêm Text Mới

```
1. Xác định key name theo convention
2. Thêm vào base language file
3. Run code generation
4. Sử dụng trong code
5. Thêm translations cho các ngôn ngữ khác
```

---

## ✅ Best Practices Checklist

- [ ] Key names descriptive và hierarchical
- [ ] Base language (EN) luôn complete
- [ ] Plurals sử dụng proper rules (ICU format)
- [ ] Date/number formatting theo locale
- [ ] RTL support nếu cần (Arabic, Hebrew)
- [ ] String interpolation với named parameters
- [ ] No hardcoded strings trong code

---

## 📁 Reference Files

| File | Nội dung |
|------|----------|
| [pipeline-new-project.md](references/pipeline-new-project.md) | Setup từ đầu |
| [pipeline-add-text.md](references/pipeline-add-text.md) | Thêm text mới |
| [best-practices.md](references/best-practices.md) | Best practices |
| [ios-localization.md](references/ios-localization.md) | iOS với SwiftGen |
| [android-localization.md](references/android-localization.md) | Android strings.xml |
| [flutter-localization.md](references/flutter-localization.md) | Flutter ARB |

