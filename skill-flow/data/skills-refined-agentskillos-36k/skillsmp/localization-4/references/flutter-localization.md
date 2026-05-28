# Flutter Localization

> intl + ARB files + Provider/Riverpod integration

---

## Recommended Approach

| Aspect | Choice |
|--------|--------|
| Library | intl + ARB files + l10n.yaml |
| Code Generation | `flutter gen-l10n` → `AppLocalizations` |
| State Management | Provider/Riverpod |
| Persistence | SharedPreferences |

---

## Setup

### pubspec.yaml

```yaml
dependencies:
  flutter:
    sdk: flutter
  flutter_localizations:
    sdk: flutter
  intl: ^0.18.0
  shared_preferences: ^2.0.0
  # Choose one:
  provider: ^6.0.0
  # OR
  flutter_riverpod: ^2.0.0
```

### l10n.yaml (project root)

```yaml
arb-dir: lib/l10n
template-arb-file: app_en.arb
output-localization-file: app_localizations.dart
output-class: AppLocalizations
```

---

## Folder Structure

```
lib/
├── l10n/
│   ├── app_en.arb          # English (base)
│   ├── app_vi.arb          # Vietnamese
│   └── app_ja.arb          # Japanese
└── providers/
    └── locale_provider.dart

.dart_tool/flutter_gen/gen_l10n/
└── app_localizations*.dart # Generated
```

---

## ARB File Format

### app_en.arb

```json
{
  "loginTitle": "Login",
  "@loginTitle": {
    "description": "Login screen title"
  },
  "loginEmailPlaceholder": "Email",
  "loginButtonSignIn": "Sign In",
  
  "loginGreeting": "Hello {name}",
  "@loginGreeting": {
    "description": "Greeting message",
    "placeholders": {
      "name": {
        "type": "String",
        "example": "John"
      }
    }
  },
  
  "itemsCount": "{count, plural, zero{No items} one{1 item} other{{count} items}}",
  "@itemsCount": {
    "placeholders": {
      "count": { "type": "int" }
    }
  }
}
```

---

## State Management

### Provider

```dart
class LocaleProvider extends ChangeNotifier {
  Locale _locale = const Locale('en');
  final SharedPreferences _prefs;
  
  LocaleProvider(this._prefs) {
    _loadSavedLocale();
  }
  
  Locale get locale => _locale;
  
  Future<void> _loadSavedLocale() async {
    final saved = _prefs.getString('app_locale');
    if (saved != null) {
      _locale = Locale(saved);
      notifyListeners();
    }
  }
  
  Future<void> changeLocale(Locale newLocale) async {
    _locale = newLocale;
    await _prefs.setString('app_locale', newLocale.languageCode);
    notifyListeners();
  }
}
```

### Riverpod

```dart
final sharedPreferencesProvider = Provider<SharedPreferences>((ref) {
  throw UnimplementedError();
});

final localeProvider = StateNotifierProvider<LocaleNotifier, Locale>((ref) {
  final prefs = ref.watch(sharedPreferencesProvider);
  return LocaleNotifier(prefs);
});

class LocaleNotifier extends StateNotifier<Locale> {
  final SharedPreferences _prefs;
  
  LocaleNotifier(this._prefs) : super(const Locale('en')) {
    _loadSavedLocale();
  }
  
  Future<void> _loadSavedLocale() async {
    final saved = _prefs.getString('app_locale');
    if (saved != null) {
      state = Locale(saved);
    }
  }
  
  Future<void> changeLocale(Locale newLocale) async {
    state = newLocale;
    await _prefs.setString('app_locale', newLocale.languageCode);
  }
}
```

---

## main.dart Integration

### Provider

```dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final prefs = await SharedPreferences.getInstance();
  
  runApp(
    ChangeNotifierProvider(
      create: (_) => LocaleProvider(prefs),
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final locale = context.watch<LocaleProvider>().locale;
    
    return MaterialApp(
      locale: locale,
      localizationsDelegates: AppLocalizations.localizationsDelegates,
      supportedLocales: AppLocalizations.supportedLocales,
      home: const HomeScreen(),
    );
  }
}
```

### Riverpod

```dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final prefs = await SharedPreferences.getInstance();
  
  runApp(
    ProviderScope(
      overrides: [
        sharedPreferencesProvider.overrideWithValue(prefs),
      ],
      child: const MyApp(),
    ),
  );
}

class MyApp extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final locale = ref.watch(localeProvider);
    
    return MaterialApp(
      locale: locale,
      localizationsDelegates: AppLocalizations.localizationsDelegates,
      supportedLocales: AppLocalizations.supportedLocales,
      home: const HomeScreen(),
    );
  }
}
```

---

## Usage in Widgets

```dart
final l10n = AppLocalizations.of(context)!;

// Simple
Text(l10n.loginTitle)
ElevatedButton(
  child: Text(l10n.loginButtonSignIn),
  onPressed: () {},
)

// With placeholder
Text(l10n.loginGreeting(userName))

// Plurals
Text(l10n.itemsCount(count))
```

---

## Language Switcher UI

### Provider

```dart
class SettingsScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final localeProvider = context.read<LocaleProvider>();
    final currentLocale = context.watch<LocaleProvider>().locale;
    final l10n = AppLocalizations.of(context)!;
    
    return Scaffold(
      appBar: AppBar(title: Text(l10n.settingsTitle)),
      body: ListView(
        children: [
          ListTile(
            title: Text(l10n.settingsLanguage),
            trailing: DropdownButton<Locale>(
              value: currentLocale,
              onChanged: (newLocale) {
                if (newLocale != null) {
                  localeProvider.changeLocale(newLocale);
                }
              },
              items: const [
                DropdownMenuItem(value: Locale('en'), child: Text('English')),
                DropdownMenuItem(value: Locale('vi'), child: Text('Tiếng Việt')),
                DropdownMenuItem(value: Locale('ja'), child: Text('日本語')),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
```

### Riverpod

```dart
class SettingsScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final locale = ref.watch(localeProvider);
    final l10n = AppLocalizations.of(context)!;
    
    return Scaffold(
      appBar: AppBar(title: Text(l10n.settingsTitle)),
      body: DropdownButton<Locale>(
        value: locale,
        onChanged: (newLocale) {
          if (newLocale != null) {
            ref.read(localeProvider.notifier).changeLocale(newLocale);
          }
        },
        items: const [
          DropdownMenuItem(value: Locale('en'), child: Text('English')),
          DropdownMenuItem(value: Locale('vi'), child: Text('Tiếng Việt')),
        ],
      ),
    );
  }
}
```

---

## Code Generation

```bash
flutter gen-l10n
```

Hoặc chạy tự động với `flutter run` / `flutter pub get` nếu đã config l10n.yaml.

---

## ICU MessageFormat

### Plurals

```json
{
  "itemsCount": "{count, plural, zero{No items} one{1 item} other{{count} items}}"
}
```

### Gender

```json
{
  "likedPost": "{gender, select, male{He} female{She} other{They}} liked your post"
}
```

### Combined

```json
{
  "userItems": "{count, plural, one{{gender, select, male{He has} female{She has} other{They have}} 1 item} other{{gender, select, male{He has} female{She has} other{They have}} {count} items}}"
}
```

---

## Best Practices

- ✅ Use intl + ARB files (official approach)
- ✅ Store locale in Provider/Riverpod
- ✅ Persist locale với SharedPreferences
- ✅ Use `AppLocalizations.of(context)!`
- ✅ Run `flutter gen-l10n` after adding keys
- ✅ Use ICU MessageFormat for plurals/gender
- ✅ Test với all supported languages
- ✅ Handle RTL với Directionality widget

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| AppLocalizations not found | Run `flutter gen-l10n` hoặc `flutter pub get` |
| Translations not updating | Restart app (hot reload may not work) |
| Missing translations | Verify key exists in all .arb files |

---

## Related Files

- **Shared Architecture**: [../shared/architecture.md](../shared/architecture.md)
- **Best Practices**: [../shared/best_practices.md](../shared/best_practices.md)
