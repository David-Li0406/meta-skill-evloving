---
name: "Rails Localization (i18n) - English & Arabic"
description: "Chief Content Copywriter with comprehensive internationalization skill for Ruby on Rails applications with proper English, Arabic, French and Spanish translations, RTL support, pluralization rules, date/time formatting, and culturally appropriate content adaptation. Use when: (1) Setting up i18n in Rails, (2) Adding RTL/Arabic support, (3) Implementing pluralization, (4) Formatting dates/currency, (5) Creating locale files. Trigger keywords: i18n, translations, localization, internationalization, locale, RTL, Arabic, multilingual, localize, translate"
version: 1.1.0
---

# Rails Localization Skill

Comprehensive guidance for implementing i18n in Ruby on Rails with English/Arabic support.

## Localization Decision Tree

```
What localization task?
│
├─ Setting up i18n from scratch?
│   └─ See "Project Setup" below
│
├─ Adding Arabic/RTL support?
│   └─ See references/rtl-css.md + references/helpers.md
│
├─ Need locale YAML files?
│   └─ See references/locale-files.md
│
├─ Implementing pluralization?
│   └─ See "Arabic Pluralization" below
│
├─ Creating views/forms?
│   └─ See references/view-components.md
│
├─ Writing i18n tests?
│   └─ See references/testing.md
│
└─ Currency/number formatting?
    └─ See "Formatting Quick Reference" below
```

---

## NEVER Do This

**NEVER** use direct translation for Arabic:
```ruby
# WRONG - Google Translate output
ar:
  items:
    one: "عنصر"
    other: "عناصر"

# RIGHT - Proper Arabic 6 plural forms
ar:
  items:
    zero: "عناصر"
    one: "عنصر"
    two: "عنصران"
    few: "عناصر"      # 3-10
    many: "عنصرًا"     # 11-99
    other: "عنصر"     # 100+
```

**NEVER** hardcode user-facing strings:
```ruby
# WRONG
flash[:notice] = "User created successfully"

# RIGHT
flash[:notice] = t('users.created_successfully')
```

**NEVER** use physical CSS properties for layout:
```css
/* WRONG - Breaks in RTL */
margin-left: 1rem;
text-align: left;

/* RIGHT - Works in both directions */
margin-inline-start: 1rem;
text-align: start;
```

**NEVER** let numbers break in RTL:
```erb
<%# WRONG - Numbers display incorrectly %>
<span><%= amount %></span>

<%# RIGHT - Keep numbers LTR %>
<span dir="ltr"><%= amount %></span>
```

**NEVER** concatenate translated strings:
```ruby
# WRONG - Word order differs between languages
"Hello " + name + ", welcome!"

# RIGHT - Use interpolation
t('greetings.welcome', name: name)
# en: "Hello %{name}, welcome!"
# ar: "مرحبًا %{name}، أهلاً بك!"
```

---

## Project Setup

### 1. Configure Application

```ruby
# config/application.rb
config.i18n.available_locales = [:en, :ar]
config.i18n.default_locale = :en
config.i18n.fallbacks = { ar: [:ar, :en], en: [:en] }
config.i18n.load_path += Dir[Rails.root.join('config', 'locales', '**', '*.{rb,yml}')]
```

### 2. Application Controller

```ruby
class ApplicationController < ActionController::Base
  around_action :switch_locale

  private

  def switch_locale(&action)
    locale = params[:locale] || cookies[:locale] || I18n.default_locale
    I18n.with_locale(locale, &action)
  end

  def default_url_options
    { locale: I18n.locale }
  end
end
```

### 3. Route Configuration

```ruby
# config/routes.rb
scope "(:locale)", locale: /en|ar/ do
  resources :users
  root "home#index"
end

get "locale/:locale", to: "locales#switch", as: :switch_locale
```

---

## Arabic Localization Principles

Arabic localization requires **cultural and linguistic adaptation**, not direct translation:

| Aspect | Requirement |
|--------|-------------|
| Direction | RTL (right-to-left) layout |
| Pluralization | 6 forms: zero, one, two, few (3-10), many (11-99), other (100+) |
| Gender | Nouns and adjectives have grammatical gender |
| Numbers | Eastern Arabic (٠١٢٣٤٥٦٧٨٩) or Western (0123456789) |
| Calendar | Hijri calendar support may be needed |
| Formality | Different greeting/formality levels |

---

## Arabic Pluralization Rules

| Count | Form | Arabic Example (days) |
|-------|------|----------------------|
| 0 | zero | صفر أيام |
| 1 | one | يوم واحد |
| 2 | two | يومان |
| 3-10 | few | ٣ أيام |
| 11-99 | many | ٢٠ يومًا |
| 100+ | other | ١٠٠ يوم |

```yaml
# Correct Arabic pluralization
ar:
  datetime:
    distance_in_words:
      x_days:
        zero: "صفر أيام"
        one: "يوم واحد"
        two: "يومان"
        few: "%{count} أيام"
        many: "%{count} يومًا"
        other: "%{count} يوم"
```

---

## Formatting Quick Reference

### Currency

```ruby
# Helper method
def localized_currency(amount, currency: 'SAR')
  if I18n.locale == :ar
    "#{number_with_precision(amount, precision: 2)} ر.س"
  else
    "SAR #{number_with_precision(amount, precision: 2)}"
  end
end
```

### Eastern Arabic Numerals

```ruby
EASTERN_ARABIC = { '0'=>'٠', '1'=>'١', '2'=>'٢', '3'=>'٣', '4'=>'٤',
                   '5'=>'٥', '6'=>'٦', '7'=>'٧', '8'=>'٨', '9'=>'٩' }

def to_eastern_arabic(number)
  number.to_s.gsub(/[0-9]/, EASTERN_ARABIC)
end
```

### Direction Helpers

```ruby
def rtl? = I18n.t('direction', default: 'ltr') == 'rtl'
def direction_class = rtl? ? 'rtl' : 'ltr'
def start_align = rtl? ? 'right' : 'left'
def end_align = rtl? ? 'left' : 'right'
```

---

## Locale File Structure

```
config/locales/
├── en/
│   ├── activerecord.en.yml
│   ├── views.en.yml
│   └── controllers.en.yml
├── ar/
│   ├── activerecord.ar.yml
│   ├── views.ar.yml
│   └── controllers.ar.yml
├── defaults/
│   ├── en.yml    # Rails defaults
│   └── ar.yml
└── shared/
    ├── errors.en.yml
    └── errors.ar.yml
```

---

## RTL Layout Essentials

### HTML Structure

```erb
<html lang="<%= I18n.locale %>" dir="<%= rtl? ? 'rtl' : 'ltr' %>">
<body class="<%= direction_class %>">
```

### Form Field Directions

| Field Type | Direction |
|------------|-----------|
| Email | Always `dir="ltr"` |
| Phone | Always `dir="ltr"` |
| URL | Always `dir="ltr"` |
| Numbers | Always `dir="ltr"` |
| Names | `dir="auto"` |
| Text content | `dir="auto"` |

### CSS Logical Properties

| Physical | Logical |
|----------|---------|
| `margin-left` | `margin-inline-start` |
| `margin-right` | `margin-inline-end` |
| `padding-left` | `padding-inline-start` |
| `text-align: left` | `text-align: start` |

---

## Best Practices Checklist

- [ ] Use lazy lookup: `t('.title')` instead of `t('users.show.title')`
- [ ] Namespace by feature: `users.index.title`, `users.show.title`
- [ ] Provide all 6 Arabic plural forms
- [ ] Use CSS logical properties for layout
- [ ] Keep numbers/emails/URLs as LTR
- [ ] Use `dir="auto"` for user-generated content
- [ ] Test both locales in system specs
- [ ] Hire native Arabic speakers for translations

---

## Quick Commands

```bash
# Check for missing translations
rails i18n:missing

# List all translation keys
rails i18n:keys

# Generate locale file from existing
rails i18n:export LOCALE=ar
```

---

## References

Detailed patterns and examples in `references/`:
- `locale-files.md` - Complete English/Arabic YAML locale files
- `helpers.md` - LocalizationHelper and ArabicHelper with all methods
- `rtl-css.md` - RTL stylesheet and Tailwind logical properties
- `view-components.md` - Layout, forms, language switcher templates
- `testing.md` - RSpec helpers and i18n test patterns

## External Resources

- [Rails I18n Guide](https://guides.rubyonrails.org/i18n.html)
- [Unicode CLDR Plural Rules](https://cldr.unicode.org/index/cldr-spec/plural-rules)
- [RTL Styling Guide](https://rtlstyling.com/)
