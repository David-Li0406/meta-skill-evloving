# Transloco

## What is this?

One-UI i18n translation tool, replacing ngx-translate.

## When to use

When displaying translated text.

## Import

```typescript
import { TranslocoModule, TranslocoService } from '@jsverse/transloco';
```

---

## Basic Usage

### In Template

```html
<div *transloco="let t">
  <h1>{{ t('features.user.page_title') }}</h1>
  <button>{{ t('general.button.create') }}</button>
</div>
```

### In Component

```typescript
readonly #transloco = inject(TranslocoService);

getMessage() {
  return this.#transloco.translate('features.xxx.success_message');
}
```

---

## Key Conventions

| Prefix | Use | Example |
|--------|-----|---------|
| `general.common.*` | Common terms | `general.common.name`, `general.common.status` |
| `general.button.*` | Button text | `general.button.create`, `general.button.delete` |
| `general.tooltip.*` | Tooltips | `general.tooltip.refresh` |
| `features.{feature}.*` | Feature-specific | `features.user.page_title` |

---

## Common Keys

```typescript
// Buttons
t('general.button.create')
t('general.button.delete')
t('general.button.cancel')
t('general.button.submit')
t('general.button.apply')
t('general.button.save')

// Common terms
t('general.common.name')
t('general.common.description')
t('general.common.status')
t('general.common.enable')
t('general.common.disable')
t('general.common.optional')

// Table
t('general.tooltip.refresh')
t('general.table_function.limit_count')
```

---

## Table Column Translation

```typescript
readonly columns = computed(() => [
  { key: 'name', header: this.#transloco.translate('general.common.name') },
  { key: 'status', header: this.#transloco.translate('general.common.status') }
]);
```

---

## Common Mistakes

```html
<!-- ❌ WRONG: Using old syntax -->
<h1>{{ 'features.user.page_title' | translate }}</h1>

<!-- ✅ CORRECT: Using *transloco -->
<div *transloco="let t">
  <h1>{{ t('features.user.page_title') }}</h1>
</div>
```

```typescript
// ❌ WRONG: Creating new translation key
t('features.user.my_custom_label')  // This key doesn't exist!

// ✅ CORRECT: Only use keys that exist in Legacy
t('features.user.page_title')  // Verify exists in assets/i18n/en.json
```

---

## Migration Key Points

1. **Do NOT create new translation keys**
2. **Do NOT modify existing translation keys**
3. **Copy EXACT keys from Legacy**
4. **Verify key exists in `assets/i18n/en.json`**

### Finding Legacy Keys

```bash
# Search Legacy i18n files
grep -r "page_title" ~/moxa/f2e-networking/apps/*/src/assets/i18n/en.json

# Search Legacy template usage
grep -r "'features.user" ~/moxa/f2e-networking/apps/*/src/app/
```

---

## Related Tools

- [common-table.md](./common-table.md) - Table header translation
- [dialogs.md](./ui/dialogs.md) - Dialog title translation
