---
id: internationalization
name: "Internationalization"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Internationalization

## Overview

Internationalization (i18n) prepares software to support multiple languages and locales without code changes. This includes text translation, date/number formatting, right-to-left languages, and cultural adaptations.

## When to Use

- Building products for global markets
- Supporting multilingual users
- Legal requirements for specific regions
- Expanding to new geographic markets
- Creating white-label products

## Key Principles

- **Externalize strings**: No hardcoded text in code
- **Use ICU format**: Industry standard for plurals, gender, context
- **Design for expansion**: Text in other languages may be 30% longer
- **Consider RTL**: Right-to-left language support from the start
- **Locale awareness**: Beyond translation - formats, units, conventions

## Best Practices

### Python i18n with Babel

```python
# Configuration
from babel import Locale, numbers, dates
from babel.support import Translations
import gettext
from functools import lru_cache
from pathlib import Path

LOCALES_DIR = Path(__file__).parent / "locales"
SUPPORTED_LOCALES = ["en", "uk", "de", "fr", "ja", "ar"]
DEFAULT_LOCALE = "en"


@lru_cache(maxsize=None)
def get_translations(locale: str) -> Translations:
    """Load translations for a locale."""
    try:
        return Translations.load(LOCALES_DIR, [locale])
    except FileNotFoundError:
        return Translations.load(LOCALES_DIR, [DEFAULT_LOCALE])


def gettext_lazy(message: str, locale: str = DEFAULT_LOCALE) -> str:
    """Translate a message."""
    translations = get_translations(locale)
    return translations.gettext(message)


def ngettext_lazy(singular: str, plural: str, n: int, locale: str = DEFAULT_LOCALE) -> str:
    """Translate with plural forms."""
    translations = get_translations(locale)
    return translations.ngettext(singular, plural, n)


# Shorthand functions
_ = gettext_lazy
_n = ngettext_lazy


# Usage
print(_("Welcome to our application", "uk"))
# "Ласкаво просимо до нашого додатку"

print(_n("%(count)d item", "%(count)d items", count, "de") % {"count": count})
# "5 Artikel"
```

### Message Extraction and Compilation

```bash
# Extract messages from Python files
pybabel extract -F babel.cfg -o locales/messages.pot .

# Initialize new language
pybabel init -i locales/messages.pot -d locales -l uk

# Update existing translations
pybabel update -i locales/messages.pot -d locales

# Compile translations
pybabel compile -d locales
```

```ini
# babel.cfg
[python: **.py]
encoding = utf-8

[jinja2: **/templates/**.html]
encoding = utf-8
extensions = jinja2.ext.autoescape,jinja2.ext.with_
```

### FastAPI Internationalization

```python
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextvars import ContextVar
from typing import Optional

# Context variable for current locale
current_locale: ContextVar[str] = ContextVar("locale", default=DEFAULT_LOCALE)

app = FastAPI()


def get_locale_from_request(request: Request) -> str:
    """Determine locale from request."""
    # 1. Check query parameter
    if locale := request.query_params.get("lang"):
        if locale in SUPPORTED_LOCALES:
            return locale

    # 2. Check Accept-Language header
    accept_language = request.headers.get("Accept-Language", "")
    for lang in accept_language.split(","):
        lang = lang.split(";")[0].strip()[:2]
        if lang in SUPPORTED_LOCALES:
            return lang

    # 3. Check user preference (if authenticated)
    if hasattr(request.state, "user") and request.state.user:
        if request.state.user.preferred_locale in SUPPORTED_LOCALES:
            return request.state.user.preferred_locale

    return DEFAULT_LOCALE


@app.middleware("http")
async def locale_middleware(request: Request, call_next):
    """Set locale context for request."""
    locale = get_locale_from_request(request)
    token = current_locale.set(locale)
    try:
        response = await call_next(request)
        response.headers["Content-Language"] = locale
        return response
    finally:
        current_locale.reset(token)


# Helper for endpoints
def get_current_locale() -> str:
    return current_locale.get()


def _(message: str) -> str:
    """Translate using current locale."""
    return gettext_lazy(message, current_locale.get())


# Usage in endpoints
@app.get("/api/products/{product_id}")
async def get_product(product_id: str, locale: str = Depends(get_current_locale)):
    product = await product_repo.get(product_id)
    return {
        "id": product.id,
        "name": product.get_name(locale),
        "description": product.get_description(locale),
        "price": format_price(product.price, locale),
    }


@app.post("/api/orders")
async def create_order(order_data: OrderCreate):
    order = await order_service.create(order_data)
    return {
        "message": _("Order created successfully"),
        "order_id": order.id,
    }
```

### React i18n with react-intl

```typescript
// i18n/messages.ts
export const messages = {
  en: {
    'app.welcome': 'Welcome, {name}!',
    'app.items': '{count, plural, =0 {No items} one {# item} other {# items}}',
    'order.total': 'Total: {amount, number, currency}',
    'order.date': 'Order date: {date, date, long}',
  },
  uk: {
    'app.welcome': 'Ласкаво просимо, {name}!',
    'app.items': '{count, plural, =0 {Немає елементів} one {# елемент} few {# елементи} many {# елементів} other {# елементів}}',
    'order.total': 'Всього: {amount, number, currency}',
    'order.date': 'Дата замовлення: {date, date, long}',
  },
  de: {
    'app.welcome': 'Willkommen, {name}!',
    'app.items': '{count, plural, =0 {Keine Artikel} one {# Artikel} other {# Artikel}}',
    'order.total': 'Gesamt: {amount, number, currency}',
    'order.date': 'Bestelldatum: {date, date, long}',
  },
};

// App.tsx
import { IntlProvider, FormattedMessage, FormattedNumber, FormattedDate } from 'react-intl';
import { messages } from './i18n/messages';

function App() {
  const [locale, setLocale] = useState('en');

  return (
    <IntlProvider locale={locale} messages={messages[locale]}>
      <Router>
        <LocaleSelector value={locale} onChange={setLocale} />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/order/:id" element={<OrderDetails />} />
        </Routes>
      </Router>
    </IntlProvider>
  );
}

// Components using translations
function Home({ user }: { user: User }) {
  return (
    <div>
      <h1>
        <FormattedMessage
          id="app.welcome"
          values={{ name: user.name }}
        />
      </h1>
      <p>
        <FormattedMessage
          id="app.items"
          values={{ count: user.cartItems.length }}
        />
      </p>
    </div>
  );
}

function OrderDetails({ order }: { order: Order }) {
  return (
    <div>
      <p>
        <FormattedMessage
          id="order.date"
          values={{ date: new Date(order.createdAt) }}
        />
      </p>
      <p>
        <FormattedMessage
          id="order.total"
          values={{ amount: order.total }}
        />
      </p>
      <p>
        <FormattedNumber
          value={order.total}
          style="currency"
          currency={order.currency}
        />
      </p>
    </div>
  );
}
```

### Database-Driven Translations

```python
from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True)
    sku = Column(String, unique=True)
    price = Column(Numeric(10, 2))

    translations = relationship("ProductTranslation", back_populates="product")

    def get_name(self, locale: str) -> str:
        return self._get_translation(locale, "name")

    def get_description(self, locale: str) -> str:
        return self._get_translation(locale, "description")

    def _get_translation(self, locale: str, field: str) -> str:
        # Try exact match
        for t in self.translations:
            if t.locale == locale:
                return getattr(t, field)

        # Fallback to base language (e.g., "uk" for "uk-UA")
        base_locale = locale.split("-")[0]
        for t in self.translations:
            if t.locale == base_locale:
                return getattr(t, field)

        # Fallback to default locale
        for t in self.translations:
            if t.locale == DEFAULT_LOCALE:
                return getattr(t, field)

        return ""


class ProductTranslation(Base):
    __tablename__ = "product_translations"

    id = Column(String, primary_key=True)
    product_id = Column(String, ForeignKey("products.id"))
    locale = Column(String(10))
    name = Column(String(255))
    description = Column(Text)

    product = relationship("Product", back_populates="translations")


# Query with eager loading
def get_product_localized(product_id: str, locale: str) -> Product:
    return (
        db.query(Product)
        .options(selectinload(Product.translations))
        .filter(Product.id == product_id)
        .first()
    )
```

### Date, Number, and Currency Formatting

```python
from babel import Locale
from babel.numbers import format_currency, format_decimal, format_percent
from babel.dates import format_date, format_datetime, format_time
from datetime import datetime, date
from decimal import Decimal

class LocaleFormatter:
    """Format values according to locale conventions."""

    def __init__(self, locale: str):
        self.locale = Locale.parse(locale)

    def format_currency(
        self,
        amount: Decimal,
        currency: str = "USD"
    ) -> str:
        """Format currency value."""
        return format_currency(amount, currency, locale=self.locale)

    def format_number(self, value: float, decimal_places: int = 2) -> str:
        """Format number with locale-specific separators."""
        return format_decimal(value, format=f"#,##0.{'0' * decimal_places}", locale=self.locale)

    def format_percent(self, value: float) -> str:
        """Format percentage."""
        return format_percent(value, locale=self.locale)

    def format_date(self, value: date, format: str = "medium") -> str:
        """Format date (short, medium, long, full)."""
        return format_date(value, format=format, locale=self.locale)

    def format_datetime(self, value: datetime, format: str = "medium") -> str:
        """Format datetime."""
        return format_datetime(value, format=format, locale=self.locale)

    def format_time(self, value: datetime, format: str = "short") -> str:
        """Format time."""
        return format_time(value, format=format, locale=self.locale)


# Usage
formatter_us = LocaleFormatter("en_US")
formatter_de = LocaleFormatter("de_DE")
formatter_uk = LocaleFormatter("uk_UA")

amount = Decimal("1234.56")
print(formatter_us.format_currency(amount, "USD"))  # $1,234.56
print(formatter_de.format_currency(amount, "EUR"))  # 1.234,56 €
print(formatter_uk.format_currency(amount, "UAH"))  # 1 234,56 ₴

dt = datetime(2024, 1, 15, 14, 30)
print(formatter_us.format_date(dt.date()))  # Jan 15, 2024
print(formatter_de.format_date(dt.date()))  # 15.01.2024
print(formatter_uk.format_date(dt.date()))  # 15 січ. 2024 р.
```

### RTL Language Support

```css
/* Base styles with logical properties */
.card {
  /* Use logical properties instead of physical */
  margin-inline-start: 1rem;  /* Instead of margin-left */
  margin-inline-end: 1rem;    /* Instead of margin-right */
  padding-block: 1rem;        /* padding-top and padding-bottom */
  padding-inline: 1.5rem;     /* padding-left and padding-right */

  /* Text alignment */
  text-align: start;          /* Instead of text-align: left */

  /* Borders */
  border-inline-start: 2px solid blue;
}

/* Float with logical values */
.sidebar {
  float: inline-start;        /* left in LTR, right in RTL */
}

/* Flexbox automatically handles RTL */
.flex-container {
  display: flex;
  flex-direction: row;        /* Reverses in RTL */
  gap: 1rem;
}

/* Manual RTL overrides when needed */
[dir="rtl"] .icon-arrow {
  transform: scaleX(-1);      /* Flip horizontal arrows */
}
```

```tsx
// React component with RTL support
import { useIntl } from 'react-intl';

function App() {
  const intl = useIntl();
  const isRTL = ['ar', 'he', 'fa'].includes(intl.locale);

  return (
    <div dir={isRTL ? 'rtl' : 'ltr'}>
      <Navigation />
      <main>
        <Content />
      </main>
    </div>
  );
}

// Tailwind with RTL plugin
// tailwind.config.js
module.exports = {
  plugins: [
    require('tailwindcss-rtl'),
  ],
};

// Usage
<div className="ms-4 me-2 text-start">
  {/* ms = margin-start, me = margin-end */}
</div>
```

### Translation Management Workflow

```markdown
## Translation Workflow

### 1. Development
- Use translation keys in code
- Extract strings with tools
- Provide context for translators

### 2. Translation
- Send to translation service/team
- Provide screenshots for context
- Review machine translations

### 3. Review
- Native speaker review
- Context verification
- Consistency check

### 4. Integration
- Merge translation files
- Test in context
- Visual regression testing

### Tools
- Lokalise, Crowdin, Phrase for management
- Transifex for open source
- POEditor for smaller projects
```

## Anti-patterns

- **Concatenating translated strings**: Breaks grammar in other languages
- **Hardcoded formats**: Dates, numbers, currencies in code
- **Ignoring pluralization**: Languages have complex plural rules
- **Fixed-width layouts**: Don't accommodate text expansion
- **Forgetting RTL**: Layout breaks in RTL languages
- **No context for translators**: Same word, different meanings

## References

- [Unicode ICU Message Format](https://unicode-org.github.io/icu/userguide/format_parse/messages/)
- [Babel Documentation](https://babel.pocoo.org/)
- [react-intl Documentation](https://formatjs.io/docs/react-intl/)
- [W3C Internationalization](https://www.w3.org/International/)
