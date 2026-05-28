# Localization - Production Examples

This document contains real production code examples from the YourCompany React Native codebase demonstrating localization patterns with useT9n hook.

## Example 1: Basic useT9n with Feature Namespace

**File**: `modules/social-recipe-bridge/screens/social-recipe-bridge/SocialRecipeBridgeScreen.tsx:49`

This example shows basic useT9n usage with feature namespace for screen translations.

```typescript
import { useT9n } from '@libs/localization';
import { useZestStyles, Icon, Text } from '@zest/react-native';

export const SocialRecipeBridgeScreen = () => {
  const styles = useZestStyles(stylesConfig);
  const { translateRaw } = useT9n('social-recipe-bridge');
  const { trackAnalyticsEvent } = useAnalyticsTracker();
  const screenName = 'SocialRecipeBridgeScreen';

  const {
    data: infiniteData,
    isLoading,
    refetch,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useGetExternalRecipesInfinite({});

  // Flatten all pages into a single array of recipes
  const recipes = infiniteData?.pages.flatMap((page) => page.data) || [];

  // ... component logic
};
```

**Key patterns demonstrated:**
- useT9n hook with feature namespace ('social-recipe-bridge')
- translateRaw destructured from useT9n return value
- Namespace matches feature name for logical organization
- Hook called at component top level (following Hooks rules)
- Feature namespace prevents key collisions with other features
- Single useT9n call per component for efficiency

## Example 2: Namespace Constants Pattern

**File**: `modules/store/screens/cart/external/price-summary/components/error-message/ErrorMessage.tsx:17`

This example shows using namespace constants for consistency across components.

```typescript
import { View } from 'react-native';
import { useT9n } from '@libs/localization';
import { applangaKeys } from '@modules/store/screens/cart/constants';
import { Text, Icon, Link, useZestStyles } from '@zest/react-native';

interface ErrorMessageProps {
  onTryAgain: () => void;
}

export const ErrorMessage = ({ onTryAgain }: ErrorMessageProps) => {
  const styles = useZestStyles(stylesConfig);
  const { translateRaw } = useT9n(applangaKeys.cart);

  return (
    <View style={styles.container} testID="error-message">
      <Icon
        icon="CircleExclamationMarkOutline24"
        altText="Error"
        testID="error-message-icon"
      />
      <Text style={styles.text} testID="error-message-text">
        {translateRaw(`${applangaKeys.cart}.revamp.pricing-info.pricing-error`)}
      </Text>
      <Link
        type="body-md-bold"
        testID="error-message-link"
        onPress={onTryAgain}
      >
        {translateRaw(`${applangaKeys.cart}.revamp.pricing-info.retry`)}
      </Link>
    </View>
  );
};
```

**Key patterns demonstrated:**
- Import namespace constants from centralized location (applangaKeys)
- Use constants with useT9n(applangaKeys.cart) instead of string
- Template literal for full key: `${applangaKeys.cart}.revamp.pricing-info.pricing-error`
- Error message and retry action use separate translation keys
- Icon with hardcoded altText "Error" (acceptable for error icons)
- testID on all elements for testing
- Link component for clickable text (retry action)
- Constants prevent typos and enable refactoring

## Example 3: Toast Notifications with Translations

**File**: `operations/social-recipe-deletion/useDeleteRecipe.ts:37`

This example shows translating toast notification titles and descriptions.

```typescript
import { useCallback } from 'react';
import { useDeleteExternalRecipe } from '@data-access/query/external-recipes';
import { useToast } from '@features/toast-feature/useToast';
import { useAnalyticsTracker } from '@libs/analytics';
import { useT9n } from '@libs/localization';

interface UseDeleteRecipeOptions {
  screenName: string;
  onDeleteSuccess?: (recipe: DeletableRecipe) => void;
  showToasts?: boolean;
  refetch?: () => void;
}

export const useDeleteRecipe = (
  options: UseDeleteRecipeOptions
): DeleteRecipeCallbacks => {
  const { onDeleteSuccess, showToasts = true, refetch, screenName } = options;
  const { trackAnalyticsEvent } = useAnalyticsTracker();
  const { showToast } = useToast();
  const { translateRaw } = useT9n('social-recipe-bridge');
  const deleteRecipeMutation = useDeleteExternalRecipe({});

  const onConfirm = useCallback(
    async (recipe: DeletableRecipe) => {
      // Track confirm analytics
      trackAnalyticsEvent(
        CookbookRecipeDeleteConfirmEvent({
          screenName,
          recipeId: recipe.id,
          recipeTitle: recipe.title,
        }).createAnalyticsEvent()
      );

      try {
        // Execute API call
        await deleteRecipeMutation.mutateAsync({ id: recipe.id });

        // Handle success callbacks
        onDeleteSuccess?.(recipe);
        refetch?.();

        // Show success toast
        if (showToasts) {
          showToast({
            id: 'recipe-deleted',
            title: translateRaw(
              'social-recipe-bridge.toast.delete_success.title'
            ),
            description: translateRaw(
              'social-recipe-bridge.toast.delete_success.description'
            ),
            variant: 'success',
            autoHide: true,
            duration: 3000,
          });
        }
      } catch (error) {
        // Show error toast
        if (showToasts) {
          showToast({
            id: 'recipe-delete-error',
            title: translateRaw(
              'social-recipe-bridge.toast.delete_error.title'
            ),
            description: translateRaw(
              'social-recipe-bridge.toast.delete_error.description'
            ),
            variant: 'error',
            autoHide: true,
            duration: 5000,
          });
        }
      }
    },
    [
      trackAnalyticsEvent,
      screenName,
      deleteRecipeMutation,
      onDeleteSuccess,
      refetch,
      showToasts,
      showToast,
      translateRaw,
    ]
  );

  // ... other callbacks
};
```

**Key patterns demonstrated:**
- useT9n hook in custom operation hook (not just components)
- Toast success with translateRaw for title and description
- Toast error with separate translateRaw calls for title and description
- Separate translation keys for success vs error toasts
- Keys follow hierarchical pattern: feature.toast.variant.property
- Conditional toast display (if showToasts)
- Different durations for success (3000ms) and error (5000ms) toasts
- translateRaw in useCallback dependencies array
- Success toast: 'social-recipe-bridge.toast.delete_success.title'
- Error toast: 'social-recipe-bridge.toast.delete_error.title'

## Example 4: Parameterized Translation with Date Formatting

**File**: `modules/store/screens/cart/components/header/Header.tsx:75`

This example shows parameterized translation with formatted date parameter.

```typescript
import { useNavigation } from '@react-navigation/native';
import { useMemo } from 'react';
import { View } from 'react-native';
import { DATE_FORMATS, useFormatDate } from '@libs/date';
import { useT9n } from '@libs/localization';
import { IconButton, Text, useZestStyles } from '@zest/react-native';
import { applangaKeys } from '../../constants';

export const Header = () => {
  const styles = useZestStyles(stylesConfig);
  const navigation = useNavigation();
  const formatDate = useFormatDate();
  const { translateRaw } = useT9n(applangaKeys.cart);

  const { delivery } = useDataContext();
  const cutoffDate = delivery?.dates.cutOffDate;
  const totalQuantity = useMealSelection(useShallow(totalQuantitySelector));

  return (
    <View style={styles.container}>
      <View style={styles.innerContainer}>
        <IconButton
          icon="CloseOutline24"
          altText="Close Cart"
          testID="close-button"
          variant="tertiary"
          style={styles.backButton}
          onPress={() => {
            trackCartClose();
            navigation.goBack();
          }}
        />
        <View style={styles.titleContainer} testID="title">
          <SectionTitle
            title={translateRaw(
              `${applangaKeys.cart}.eos.main-header.your-order`
            )}
            badge={totalQuantity}
          />
          {cutoffDate && (
            <Text testID="cutoff-date">
              {translateRaw(`${applangaKeys.cart}.revamp.header.cutoff-date`, {
                cutoffDate: formatDate(cutoffDate, DATE_FORMATS.SHORT),
              })}
            </Text>
          )}
        </View>
        <View style={styles.backButton} />
      </View>
      <CartFeedbackBar />
    </View>
  );
};
```

**Key patterns demonstrated:**
- Parameterized translation with translateRaw second argument (object with parameters)
- Date formatting before passing to translation: formatDate(cutoffDate, DATE_FORMATS.SHORT)
- Translation key with parameters: `${applangaKeys.cart}.revamp.header.cutoff-date`
- Parameter object: { cutoffDate: formattedDateString }
- Conditional rendering with cutoffDate && (only show if date exists)
- Template literal for namespace prefix: `${applangaKeys.cart}.revamp.header.cutoff-date`
- Simple translation without parameters: `${applangaKeys.cart}.eos.main-header.your-order`
- testID on Text for testing cutoff date display
- Translation file would have: "Order by {{cutoffDate}}"

## Summary

The YourCompany codebase consistently follows these localization patterns:

1. **useT9n Hook** - Import from @libs/localization, destructure translateRaw
2. **Feature Namespaces** - Use feature name as namespace (social-recipe-bridge, cart)
3. **Namespace Constants** - Define applangaKeys constants for reusability across components
4. **Hierarchical Keys** - Follow namespace.context.element.property pattern
5. **translateRaw** - Use for simple string translations without parameters
6. **Parameterized Translations** - Pass object as second argument with variables
7. **Toast Notifications** - Separate keys for title and description, success vs error
8. **Error Messages** - Translate error text and retry action separately
9. **Date Formatting** - Format dates before passing to translations as parameters
10. **Template Literals** - Use `${applangaKeys.cart}.key.path` for namespace prefix
11. **Conditional Rendering** - Check value exists before rendering translations with parameters
12. **testID** - Always add testID to elements with translated text for testing

These patterns enable multi-language support, ensure accessibility for all users, provide consistent translation organization through namespaces, and make translations maintainable across the entire app.
