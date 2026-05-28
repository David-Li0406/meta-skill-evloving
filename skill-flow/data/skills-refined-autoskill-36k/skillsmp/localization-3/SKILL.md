---
name: localization
description: "WHAT: Internationalization with useT9n hook for namespace-based translations. WHEN: displaying user-facing text, accessibility labels, toast messages. KEYWORDS: i18n, localization, translations, useT9n, translateRaw, namespace, altText, accessibility."
---

# Localization

## Core Principles

**Always use useT9n hook with feature namespace.** Every component displaying user-facing text must use useT9n('feature-name') to access translations. Never hardcode strings directly in JSX. Feature namespace organizes translations and prevents key collisions across the app.

**Always use hierarchical translation keys.** Translation keys must follow the pattern `namespace.context.element.property` (e.g., 'social-recipe-bridge.screen.header.title'). Hierarchical structure makes translations easy to find, maintain, and prevents ambiguous keys.

**Always provide translations for accessibility properties.** Icon altText, TouchableOpacity accessibilityLabel, and other accessibility properties must use translateRaw for screen reader support. Accessibility is not optional - every interactive element needs translated labels.

**Always test translations with mocked useT9n.** Tests must mock useT9n to return keys as-is (translateRaw: (key) => key). This removes external dependencies, makes tests fast, and verifies correct translation keys are used without requiring translation files.

**Why**: Internationalization enables global reach, provides consistent translation patterns, ensures accessibility for all users, and makes the app maintainable across multiple languages through namespace-based organization.

## When to Use This Skill

Use these patterns when:

- Displaying any user-facing text (titles, labels, descriptions, messages)
- Providing Icon altText for screen reader accessibility
- Setting accessibilityLabel on TouchableOpacity or buttons
- Showing error messages or validation feedback
- Rendering placeholder text in InputField components
- Displaying toast notifications (success, error, info)
- Building empty states with titles and descriptions
- Creating form labels and helper text
- Showing confirmation dialogs or modals
- Implementing multi-language support for global users

## useT9n Hook

### Basic Usage with translateRaw

Use useT9n with feature namespace and translateRaw for simple string translations.

```typescript
import { useT9n } from '@libs/localization';
import { Text } from '@zest/react-native';

const RecipeDetailsScreen = () => {
  const { translateRaw } = useT9n('recipe-details');

  return (
    <View>
      <Text type="headline-lg">
        {translateRaw('recipe-details.screen.title')}
      </Text>
      <Text type="body-md-regular">
        {translateRaw('recipe-details.screen.description')}
      </Text>
    </View>
  );
};
```

**Why**: useT9n provides type-safe translations with automatic namespace handling. translateRaw returns translated string for the given key. Feature namespace ('recipe-details') organizes translations logically.

**Production Example**: `modules/social-recipe-bridge/screens/social-recipe-bridge/SocialRecipeBridgeScreen.tsx:49`

### Feature-Based Namespaces

Use feature name as translation namespace to organize translations by domain.

```typescript
// Social recipe feature
const { translateRaw } = useT9n('social-recipe-bridge');

// Cart feature
const { translateRaw } = useT9n('cart');

// Cookbook FAQ feature
const { translateRaw } = useT9n('cookbook-faq');

// Reactivation banner feature
const { translateRaw } = useT9n('reactivation-banner');
```

**Why**: Feature-based namespaces prevent key collisions, organize translations logically by feature, make it easy to find translations for a specific feature, and enable lazy loading of translation namespaces on demand.

### Namespace Constants

Define namespace constants for reusability across feature.

```typescript
// modules/store/screens/cart/constants/index.ts
export const applangaKeys = {
  cart: 'cart',
  store: 'store',
  checkout: 'checkout',
} as const;

// Usage in components
import { applangaKeys } from '@modules/store/screens/cart/constants';

const CartScreen = () => {
  const { translateRaw } = useT9n(applangaKeys.cart);

  return (
    <Text>
      {translateRaw(`${applangaKeys.cart}.revamp.header.title`)}
    </Text>
  );
};
```

**Why**: Constants prevent typos in namespace strings, enable IDE autocomplete, make refactoring easier, and provide single source of truth for feature namespace names.

**Production Example**: `modules/store/screens/cart/external/error-message/ErrorMessage.tsx:17`

## Translation Key Conventions

### Hierarchical Key Structure

Use dot notation with pattern: `namespace.context.element.property`

```typescript
const { translateRaw } = useT9n('social-recipe-bridge');

// namespace.context.element.property
translateRaw('social-recipe-bridge.screen.header.title');
translateRaw('social-recipe-bridge.screen.header.close.alt_text');
translateRaw('social-recipe-bridge.screen.empty_state.title');
translateRaw('social-recipe-bridge.screen.empty_state.description');
translateRaw('social-recipe-bridge.dialog.confirm_delete.message');
translateRaw('social-recipe-bridge.toast.delete_success.title');
```

**Key parts:**
- `namespace`: Feature name (social-recipe-bridge, cart, checkout)
- `context`: Screen, dialog, toast, banner, form
- `element`: Specific UI element (header, button, title, message)
- `property`: Text type (title, description, label, alt_text, placeholder)

**Why**: Hierarchical structure makes translations easy to find, prevents ambiguous keys, mirrors UI hierarchy, and enables logical organization in translation JSON files.

### Common Context Types

Standard context values for consistent key organization.

```typescript
// Screens
translateRaw('feature.screen.title');
translateRaw('feature.screen.subtitle');

// Dialogs/Modals
translateRaw('feature.dialog.title');
translateRaw('feature.dialog.message');
translateRaw('feature.dialog.confirm_button');
translateRaw('feature.dialog.cancel_button');

// Toasts/Notifications
translateRaw('feature.toast.success.title');
translateRaw('feature.toast.success.description');
translateRaw('feature.toast.error.title');
translateRaw('feature.toast.error.description');

// Forms
translateRaw('feature.form.field_label');
translateRaw('feature.form.placeholder');
translateRaw('feature.form.error_message');
translateRaw('feature.form.helper_text');

// Empty States
translateRaw('feature.empty_state.title');
translateRaw('feature.empty_state.description');
translateRaw('feature.empty_state.action_button');

// Error States
translateRaw('feature.error.network_error');
translateRaw('feature.error.validation_failed');
translateRaw('feature.error.retry');
```

**Why**: Consistent context types make translations predictable and easy to find. Standard patterns reduce cognitive load when adding new translations.

## Parameterized Translations

### With Interpolation

Use t() function with parameters for dynamic translations.

```typescript
import { useT9n } from '@libs/localization';
import { useFormatDate, DATE_FORMATS } from '@libs/date';

const CartHeader = ({ cutoffDate }) => {
  const { translateRaw } = useT9n('cart');
  const formatDate = useFormatDate();

  return (
    <Text>
      {translateRaw('cart.revamp.header.cutoff-date', {
        cutoffDate: formatDate(cutoffDate, DATE_FORMATS.SHORT),
      })}
    </Text>
  );
};

// Translation file:
// "cart.revamp.header.cutoff-date": "Order by {{cutoffDate}}"
```

**Why**: Parameters enable dynamic translations with variable values (dates, names, counts). Interpolation with {{variable}} syntax keeps translations readable and translatable.

**Production Example**: `modules/store/screens/cart/components/header/Header.tsx:75`

### Multiple Parameters

Pass multiple parameters to translations for complex strings.

```typescript
const { translateRaw } = useT9n('recipe-details');

const message = translateRaw('recipe-details.screen.serving_info', {
  servings: recipe.servings,
  prepTime: recipe.prepTimeMinutes,
  cookTime: recipe.cookTimeMinutes,
});

// Translation file:
// "recipe-details.screen.serving_info": "Serves {{servings}} | Prep: {{prepTime}}min | Cook: {{cookTime}}min"
```

**Why**: Multiple parameters enable complex dynamic strings. Translation file shows full context with all placeholders, making it easier for translators.

### Pluralization

Use count parameter for automatic pluralization.

```typescript
const { t } = useT9n('recipe-list');

const itemCount = t('recipe-list.screen.item_count', {
  count: recipes.length,
});

// Translation file:
// "recipe-list.screen.item_count": "{{count}} recipe"
// "recipe-list.screen.item_count_plural": "{{count}} recipes"
```

**Why**: i18next automatically selects singular or plural form based on count parameter. Different languages have different pluralization rules (some have 2 forms, some have 6), handled automatically.

## Accessibility Labels

### altText for Icons

Always provide translated altText for Icon components.

```typescript
import { Icon } from '@zest/react-native';
import { useT9n } from '@libs/localization';

const ErrorMessage = ({ onTryAgain }) => {
  const { translateRaw } = useT9n('cart');

  return (
    <View>
      <Icon
        icon="CircleExclamationMarkOutline24"
        altText={translateRaw('cart.revamp.pricing-info.error-icon-alt')}
        testID="error-message-icon"
      />
      <Text>
        {translateRaw('cart.revamp.pricing-info.pricing-error')}
      </Text>
    </View>
  );
};
```

**Why**: altText improves accessibility for screen readers. Translated altText ensures all users understand icon meaning in their language. Empty altText for decorative icons is acceptable.

**Production Example**: `modules/store/screens/cart/external/price-summary/components/error-message/ErrorMessage.tsx:22`

### accessibilityLabel for Buttons

Provide translated accessibility labels for TouchableOpacity and interactive elements.

```typescript
const { translateRaw } = useT9n('social-recipe-bridge');

const AddButton = ({ onPress }) => {
  return (
    <TouchableOpacity
      onPress={onPress}
      accessibilityLabel={translateRaw(
        'social-recipe-bridge.action.add_recipe.accessibility_label'
      )}
      accessibilityHint={translateRaw(
        'social-recipe-bridge.action.add_recipe.accessibility_hint'
      )}
      accessibilityRole="button"
      testID="add-recipe-button"
    >
      <Icon icon="PlusOutline24" altText="" />
    </TouchableOpacity>
  );
};
```

**Why**: accessibilityLabel ensures screen readers announce button purpose. accessibilityHint provides additional context about what happens when pressed. Both must be translated for accessibility in all languages.

### IconButton with Translated altText

IconButton requires altText for accessibility.

```typescript
import { IconButton } from '@zest/react-native';
import { useT9n } from '@libs/localization';

const CartHeader = ({ onClose }) => {
  const { translateRaw } = useT9n('cart');

  return (
    <IconButton
      icon="CloseOutline24"
      altText={translateRaw('cart.screen.header.close.alt_text')}
      variant="tertiary"
      testID="close-button"
      onPress={onClose}
    />
  );
};
```

**Why**: IconButton altText provides accessible label for screen readers. Always translate altText - different languages may use different words (Close, Cerrar, Fermer, Schließen).

**Production Example**: `modules/store/screens/cart/components/header/Header.tsx:56`

## Toast Notifications

### Success and Error Toasts

Use translations for toast messages with title and description.

```typescript
import { useToast } from '@features/toast-feature/useToast';
import { useT9n } from '@libs/localization';

const useDeleteRecipe = () => {
  const { showToast } = useToast();
  const { translateRaw } = useT9n('social-recipe-bridge');

  const onDeleteSuccess = () => {
    showToast({
      id: 'recipe-deleted',
      title: translateRaw('social-recipe-bridge.toast.delete_success.title'),
      description: translateRaw(
        'social-recipe-bridge.toast.delete_success.description'
      ),
      variant: 'success',
      autoHide: true,
      duration: 3000,
    });
  };

  const onDeleteError = (error: Error) => {
    showToast({
      id: 'recipe-delete-error',
      title: translateRaw('social-recipe-bridge.toast.delete_error.title'),
      description: translateRaw(
        'social-recipe-bridge.toast.delete_error.description'
      ),
      variant: 'error',
      autoHide: true,
      duration: 5000,
    });
  };

  return { onDeleteSuccess, onDeleteError };
};
```

**Why**: Toast notifications are user-facing messages that must be translated. Separate title and description keys enable better translations. Success and error toasts have different contexts requiring different translations.

**Production Example**: `operations/social-recipe-deletion/useDeleteRecipe.ts:75`

## Error Messages

### Error Message Components

Display translated error messages with retry action.

```typescript
import { useT9n } from '@libs/localization';
import { Text, Icon, Link } from '@zest/react-native';

const ErrorMessage = ({ onTryAgain }) => {
  const { translateRaw } = useT9n('cart');

  return (
    <View testID="error-message">
      <Icon
        icon="CircleExclamationMarkOutline24"
        altText="Error"
        testID="error-message-icon"
      />
      <Text testID="error-message-text">
        {translateRaw('cart.revamp.pricing-info.pricing-error')}
      </Text>
      <Link type="body-md-bold" testID="error-message-link" onPress={onTryAgain}>
        {translateRaw('cart.revamp.pricing-info.retry')}
      </Link>
    </View>
  );
};
```

**Why**: Error messages explain what went wrong in user's language. Retry action label must be translated. Error message and action are separate keys for flexibility.

**Production Example**: `modules/store/screens/cart/external/price-summary/components/error-message/ErrorMessage.tsx:15`

## Testing Translations

### Mock useT9n in Tests

Mock useT9n to return keys as-is for testing.

```typescript
jest.mock('@libs/localization', () => ({
  useT9n: () => ({
    translateRaw: (key: string) => key, // Returns key as-is
    t: (key: string) => key,
  }),
}));

describe('<RecipeDetailsScreen />', () => {
  it('renders title with correct translation key', () => {
    render(<RecipeDetailsScreen />);

    expect(
      screen.getByText('recipe-details.screen.title')
    ).toBeTruthy();
  });

  it('renders description with correct translation key', () => {
    render(<RecipeDetailsScreen />);

    expect(
      screen.getByText('recipe-details.screen.description')
    ).toBeTruthy();
  });
});
```

**Why**: Mocking translations removes external dependencies (translation files), makes tests fast, and verifies correct translation keys are used. Tests check key correctness, not translated content.

### Verify Translation Keys

Test that correct translation keys are called with expected parameters.

```typescript
const mockTranslateRaw = jest.fn((key: string, params?: object) => key);

jest.mock('@libs/localization', () => ({
  useT9n: () => ({
    translateRaw: mockTranslateRaw,
  }),
}));

describe('<CartHeader />', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('calls translateRaw with cutoffDate parameter', () => {
    const cutoffDate = new Date('2024-01-15');

    render(<CartHeader cutoffDate={cutoffDate} />);

    expect(mockTranslateRaw).toHaveBeenCalledWith(
      'cart.revamp.header.cutoff-date',
      expect.objectContaining({
        cutoffDate: expect.any(String),
      })
    );
  });
});
```

**Why**: Testing translation key calls verifies correct keys are used with correct parameters. Ensures parameterized translations receive expected values.

## Translation File Organization

### Feature-Based Files

Organize translation files by feature namespace.

```
locales/
└── en/
    ├── common.json                       # Shared translations
    ├── social-recipe-bridge.json         # Feature-specific
    ├── cart.json                         # Feature-specific
    ├── cookbook-faq.json                 # Feature-specific
    └── store.json                        # Feature-specific
```

**Why**: Feature-based organization keeps translations maintainable, prevents large monolithic files, enables lazy loading per feature, and makes it easy to find translations for a specific feature.

### Translation File Structure

JSON structure mirrors hierarchical key convention.

```json
// locales/en/social-recipe-bridge.json
{
  "social-recipe-bridge": {
    "screen": {
      "header": {
        "title": "My Recipes",
        "close": {
          "alt_text": "Close"
        }
      },
      "empty_state": {
        "title": "No recipes yet",
        "description": "Add your first recipe to get started",
        "action_button": "Add Recipe"
      }
    },
    "toast": {
      "delete_success": {
        "title": "Recipe deleted",
        "description": "Your recipe has been removed"
      },
      "delete_error": {
        "title": "Delete failed",
        "description": "Unable to delete recipe. Please try again."
      }
    }
  }
}
```

**Why**: JSON structure mirrors dot notation keys, making it easy to find translations. Nested structure shows relationships between translations. Clear hierarchy improves maintainability.

## i18next Configuration

### Basic Setup

Configure i18next with fallback language.

```typescript
import i18n from 'i18next';

i18n.init({
  fallbackLng: 'en',
  defaultNS: 'common',
  lng: userLocale || 'en',
  interpolation: {
    escapeValue: false, // React already escapes
  },
  resources: {
    en: {
      common: commonEn,
      'social-recipe-bridge': socialRecipeBridgeEn,
      cart: cartEn,
    },
  },
});
```

**Why**: fallbackLng ensures app works even if translations are missing. defaultNS provides common translations. interpolation.escapeValue false prevents double-escaping in React.

### Lazy Load Namespaces

Load translation namespaces on demand for performance.

```typescript
import { useEffect } from 'react';
import i18n from 'i18next';

const RecipeDetailsScreen = () => {
  useEffect(() => {
    i18n.loadNamespaces('recipe-details');
  }, []);

  const { translateRaw } = useT9n('recipe-details');

  return <View>{/* component */}</View>;
};
```

**Why**: Lazy loading reduces initial bundle size, improves startup performance, and only loads translations when needed. Feature namespaces enable selective loading.

## Common Mistakes to Avoid

❌ **Don't hardcode user-facing strings**:

```typescript
// ❌ Wrong - hardcoded text
<Text type="headline-lg">My Recipes</Text>

// ❌ Wrong - hardcoded altText
<Icon icon="CloseOutline24" altText="Close" />
```

**Why**: Hardcoded strings prevent internationalization. Users in other languages see English text. Screen readers announce English for all users.

✅ **Do use translations for all user-facing text**:

```typescript
// ✅ Correct - translated text
const { translateRaw } = useT9n('social-recipe-bridge');

<Text type="headline-lg">
  {translateRaw('social-recipe-bridge.screen.header.title')}
</Text>

// ✅ Correct - translated altText
<Icon
  icon="CloseOutline24"
  altText={translateRaw('social-recipe-bridge.screen.close.alt_text')}
/>
```

**Why**: Translations enable multi-language support. All text is accessible in user's language. Screen readers announce correctly in all languages.

❌ **Don't use inconsistent key structure**:

```typescript
// ❌ Wrong - inconsistent patterns
translateRaw('RecipeTitle'); // Wrong case
translateRaw('recipe.screen-title'); // Mixed separators
translateRaw('title'); // Missing namespace
translateRaw('recipe_screen_title'); // Wrong separator
```

**Why**: Inconsistent keys make translations hard to find, prevent autocomplete, and cause confusion about key patterns.

✅ **Do use hierarchical keys with namespace**:

```typescript
// ✅ Correct - consistent hierarchical pattern
translateRaw('social-recipe-bridge.screen.header.title');
translateRaw('social-recipe-bridge.dialog.confirm_delete.message');
translateRaw('social-recipe-bridge.toast.success.description');
```

**Why**: Consistent hierarchical keys are predictable, easy to find, and enable logical organization in translation files.

❌ **Don't concatenate translations**:

```typescript
// ❌ Wrong - string concatenation
const text = translateRaw('recipe.serves') + ' ' + servings;

// ❌ Wrong - template literals
const text = `${translateRaw('recipe.serves')} ${servings}`;
```

**Why**: Concatenation doesn't work for all languages. Word order differs across languages. Impossible for translators to understand context.

✅ **Do use parameterized translations**:

```typescript
// ✅ Correct - parameters
const text = translateRaw('recipe.serving_info', { servings });

// Translation file:
// "recipe.serving_info": "Serves {{servings}}"
```

**Why**: Parameters enable proper translation for all languages. Translators see full context with placeholders. Word order can be adjusted per language.

❌ **Don't forget accessibility translations**:

```typescript
// ❌ Wrong - no altText
<Icon icon="CloseOutline24" />

// ❌ Wrong - hardcoded accessibility
<TouchableOpacity accessibilityLabel="Close">
  <Icon icon="CloseOutline24" altText="" />
</TouchableOpacity>
```

**Why**: Missing or hardcoded accessibility labels prevent screen reader users from understanding UI in their language.

✅ **Do translate all accessibility properties**:

```typescript
// ✅ Correct - translated altText
<Icon
  icon="CloseOutline24"
  altText={translateRaw('feature.screen.close.alt_text')}
/>

// ✅ Correct - translated accessibilityLabel
<TouchableOpacity
  accessibilityLabel={translateRaw('feature.action.close.accessibility_label')}
  onPress={onClose}
>
  <Icon icon="CloseOutline24" altText="" />
</TouchableOpacity>
```

**Why**: Translated accessibility labels ensure all users understand UI in their language. Screen readers announce correctly for all languages.

## Quick Reference

**Basic translation**:
```typescript
const { translateRaw } = useT9n('feature-name');

<Text>{translateRaw('feature.screen.title')}</Text>
```

**With parameters**:
```typescript
const { translateRaw } = useT9n('feature');

const text = translateRaw('feature.message', {
  name: user.name,
  count: items.length,
});
```

**Icon altText**:
```typescript
<Icon
  icon="CloseOutline24"
  altText={translateRaw('feature.screen.close.alt_text')}
/>
```

**TouchableOpacity accessibility**:
```typescript
<TouchableOpacity
  accessibilityLabel={translateRaw('feature.action.label')}
  accessibilityHint={translateRaw('feature.action.hint')}
  onPress={onPress}
>
  <Text>{translateRaw('feature.action.text')}</Text>
</TouchableOpacity>
```

**Toast notifications**:
```typescript
showToast({
  title: translateRaw('feature.toast.success.title'),
  description: translateRaw('feature.toast.success.description'),
  variant: 'success',
});
```

**Mock in tests**:
```typescript
jest.mock('@libs/localization', () => ({
  useT9n: () => ({
    translateRaw: (key: string) => key,
    t: (key: string) => key,
  }),
}));
```

**Namespace constants**:
```typescript
export const applangaKeys = {
  cart: 'cart',
  store: 'store',
} as const;

const { translateRaw } = useT9n(applangaKeys.cart);
```

**Key Libraries:**
- i18next 24.2.1
- react-i18next (via @libs/localization)
- React Native 0.75.4

For production examples, see [references/examples.md](references/examples.md).
