# Android Localization

> strings.xml + Resource Qualifiers + ViewModel integration

---

## Recommended Approach

| Aspect | Choice |
|--------|--------|
| Library | Native strings.xml (built-in) |
| Code Generation | Auto `R.string.*` |
| State Management | `StateFlow<String>` trong ViewModel |
| Persistence | SharedPreferences |

---

## Folder Structure

```
app/src/main/res/
├── values/
│   └── strings.xml         # Default (English)
├── values-vi/
│   └── strings.xml         # Vietnamese
├── values-ja/
│   └── strings.xml         # Japanese
└── values-zh-rCN/
    └── strings.xml         # Chinese (Simplified)
```

### Resource Qualifiers

| Qualifier | Example |
|-----------|---------|
| Language only | `values-vi`, `values-ja` |
| Language + Region | `values-zh-rCN`, `values-zh-rTW` |

---

## strings.xml Format

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <!-- App name -->
    <string name="app_name">My App</string>
    
    <!-- Common -->
    <string name="common_ok">OK</string>
    <string name="common_cancel">Cancel</string>
    
    <!-- Login Screen -->
    <string name="login_title">Login</string>
    <string name="login_email_placeholder">Email</string>
    <string name="login_button_sign_in">Sign In</string>
    
    <!-- With placeholder -->
    <string name="login_greeting">Hello %s</string>
</resources>
```

### Special Characters

| Character | Escape |
|-----------|--------|
| Apostrophe | `Don\'t` |
| Quotes | `He said \"Hello\"` |
| Newline | `Line 1\nLine 2` |
| HTML | `<b>Bold</b> text` |

---

## MVVM Integration

### AppViewModel

```kotlin
class AppViewModel(private val localeStorage: LocaleStorage) : ViewModel() {
  private val _currentLocale = MutableStateFlow("en")
  val currentLocale: StateFlow<String> = _currentLocale.asStateFlow()
  
  init {
    viewModelScope.launch {
      _currentLocale.value = localeStorage.loadLocale() ?: "en"
    }
  }
  
  fun changeLocale(context: Context, locale: String) {
    _currentLocale.value = locale
    localeStorage.saveLocale(locale)
    updateConfiguration(context, locale)
    (context as? Activity)?.recreate()
  }
  
  private fun updateConfiguration(context: Context, locale: String) {
    val localeObj = Locale(locale)
    Locale.setDefault(localeObj)
    val config = Configuration(context.resources.configuration)
    config.setLocale(localeObj)
    context.createConfigurationContext(config)
  }
}
```

### LocaleStorage

```kotlin
interface LocaleStorage {
  fun saveLocale(locale: String)
  fun loadLocale(): String?
}

class SharedPreferencesLocaleStorage(context: Context) : LocaleStorage {
  private val prefs = context.getSharedPreferences("app_prefs", Context.MODE_PRIVATE)
  private val key = "app_locale"
  
  override fun saveLocale(locale: String) {
    prefs.edit().putString(key, locale).apply()
  }
  
  override fun loadLocale(): String? {
    return prefs.getString(key, null)
  }
}
```

### LocaleContextWrapper

```kotlin
class LocaleContextWrapper(base: Context) : ContextWrapper(base) {
  companion object {
    fun wrap(context: Context, language: String): ContextWrapper {
      var ctx = context
      val config = ctx.resources.configuration
      val locale = Locale(language)
      Locale.setDefault(locale)
      config.setLocale(locale)
      ctx = ctx.createConfigurationContext(config)
      return LocaleContextWrapper(ctx)
    }
  }
}
```

### BaseActivity

```kotlin
abstract class BaseActivity : AppCompatActivity() {
  override fun attachBaseContext(newBase: Context) {
    val locale = SharedPreferencesLocaleStorage(newBase).loadLocale() ?: "en"
    super.attachBaseContext(LocaleContextWrapper.wrap(newBase, locale))
  }
}
```

---

## Usage

### In Code

```kotlin
// Simple
binding.titleText.text = getString(R.string.login_title)

// With placeholder
val greeting = getString(R.string.login_greeting, userName)
binding.greetingText.text = greeting
```

### In XML

```xml
<TextView
    android:text="@string/login_title"
    ... />

<Button
    android:text="@string/login_button_sign_in"
    ... />
```

---

## Language Switcher UI

```kotlin
class SettingsFragment : Fragment() {
  private val viewModel: AppViewModel by activityViewModels()
  
  override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
    val languages = arrayOf("English", "Tiếng Việt", "日本語")
    val locales = arrayOf("en", "vi", "ja")
    
    binding.languageSpinner.adapter = ArrayAdapter(
      requireContext(),
      android.R.layout.simple_spinner_dropdown_item,
      languages
    )
    
    // Set current selection
    lifecycleScope.launch {
      viewModel.currentLocale.collect { locale ->
        val index = locales.indexOf(locale)
        if (index >= 0) {
          binding.languageSpinner.setSelection(index)
        }
      }
    }
    
    binding.languageSpinner.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
      override fun onItemSelected(parent: AdapterView<*>, view: View, position: Int, id: Long) {
        val locale = locales[position]
        if (locale != viewModel.currentLocale.value) {
          viewModel.changeLocale(requireContext(), locale)
        }
      }
      override fun onNothingSelected(parent: AdapterView<*>) {}
    }
  }
}
```

---

## Pluralization

### strings.xml

```xml
<plurals name="items_count">
    <item quantity="zero">No items</item>
    <item quantity="one">1 item</item>
    <item quantity="other">%d items</item>
</plurals>
```

### Quantities

| Category | Languages |
|----------|-----------|
| zero | Arabic |
| one | English, Vietnamese |
| two | Arabic, Welsh |
| few | Russian, Polish |
| many | Russian, Polish |
| other | All (required) |

### Usage

```kotlin
val text = resources.getQuantityString(R.plurals.items_count, count, count)
```

---

## String Arrays

```xml
<string-array name="languages">
    <item>English</item>
    <item>Tiếng Việt</item>
    <item>日本語</item>
</string-array>
```

```kotlin
val languages = resources.getStringArray(R.array.languages)
```

---

## Best Practices

- ✅ Use resource qualifiers (values-vi, values-ja)
- ✅ Store locale in ViewModel StateFlow
- ✅ Persist with SharedPreferences
- ✅ Override `attachBaseContext` in BaseActivity
- ✅ Call `recreate()` after locale change
- ✅ Use `getString(R.string.key)` in code
- ✅ Use `@string/key` in XML layouts
- ✅ Handle RTL with `start`/`end` thay vì `left`/`right`
- ✅ Use `<plurals>` for pluralization
- ✅ Escape special characters properly

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Translations not updating | Call `Activity.recreate()` |
| Wrong language on startup | Check `attachBaseContext` in BaseActivity |
| Missing translations | Verify strings.xml exists in values-XX folder |

---

## Related Files

- **Shared Architecture**: [../shared/architecture.md](../shared/architecture.md)
- **Best Practices**: [../shared/best_practices.md](../shared/best_practices.md)
