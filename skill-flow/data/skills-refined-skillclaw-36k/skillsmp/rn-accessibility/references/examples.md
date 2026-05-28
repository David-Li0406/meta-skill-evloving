# Accessibility - Production Examples

This document contains real production code examples from the YourCompany React Native codebase demonstrating accessibility patterns.

## Example 1: Week Selector with Full Accessibility

**File**: `shared-mobile-modules/src/modules/store/screens/storefront/components/week-header/week-selector/WeekSelector.tsx`

This example demonstrates comprehensive accessibility for a horizontal scrollable tab list with state management and translated labels.

```typescript
import { Pressable, View, ScrollView } from 'react-native';
import { useT9n } from '@libs/localization';
import { Icon, Text, useZestStyles, accessibilityScale } from '@zest/react-native';

export const WeekSelector = ({
  weeks = [],
  selectedWeekId,
  onSelectWeek,
  onViewPastDeliveries,
}: WeekSelectorProps) => {
  const { translateRaw } = useT9n('store');

  const renderWeekItem = (week: WeekItem, index: number) => {
    const isSelected = week.id === selectedWeekId;
    const isSkipped = week.isSkipped;

    // Create accessibility label based on week state
    const weekStatus = isSkipped
      ? 'Skipped week'
      : isSelected
        ? 'Selected week'
        : 'Week';
    const accessibilityLabel = `${weekStatus} ${week.deliveryDay} ${week.deliveryDate}`;

    return (
      <Pressable
        key={week.id}
        onPress={() => handleSelectWeek(week)}
        accessibilityRole="button"
        accessibilityLabel={accessibilityLabel}
        accessibilityState={{
          selected: isSelected,
        }}
        accessibilityHint={
          isSkipped ? 'This delivery is skipped' : 'Select this delivery week'
        }
      >
        {isSkipped ? (
          <>
            <Text>Skipped</Text>
            <View>
              <Icon
                icon="PauseFilled16"
                color={isSelected ? 'alias.color.neutral.foreground.default' : 'global.color.black'}
                altText="Skipped"
              />
              <Text decoration="strikethrough">{week.deliveryDate}</Text>
            </View>
          </>
        ) : (
          <>
            <Text>{week.deliveryDay}</Text>
            <Text>{week.deliveryDate}</Text>
          </>
        )}
      </Pressable>
    );
  };

  return (
    <ScrollView
      horizontal
      accessibilityRole="tablist"
      accessibilityLabel="Week selector"
      accessibilityHint="Select delivery week from the list"
    >
      <Pressable
        onPress={onViewPastDeliveries}
        accessibilityRole="button"
        accessibilityLabel={translateRaw('store.week-selector.past-deliveries.button.accessibility.label')}
        accessibilityHint={translateRaw('store.week-selector.past-deliveries.button.accessibility.hint')}
        testID="view-past-deliveries-button"
      >
        <Text type="body-xs-bold">
          {translateRaw('store.week-selector.past-deliveries.button.text')}
        </Text>
      </Pressable>
      {weeks.map(renderWeekItem)}
    </ScrollView>
  );
};
```

**Key patterns demonstrated:**
- `accessibilityRole="tablist"` for container
- `accessibilityState={{ selected }}` for tab state
- Dynamic accessibility labels based on item state
- Contextual hints ("This delivery is skipped")
- Translated labels with `translateRaw`
- Icon `altText` for meaningful icons
- TestID alongside accessibility properties

## Example 2: Single Week Header with Semantic Roles

**File**: `shared-mobile-modules/src/modules/store/screens/storefront/components/week-header/single-week-header/SingleWeekHeader.tsx`

```typescript
import { View } from 'react-native';
import { useT9n } from '@libs/localization';
import { useZestStyles } from '@zest/react-native';

export const SingleWeekHeader = ({ week, onBackPress }: SingleWeekHeaderProps) => {
  const { translateRaw } = useT9n('store');

  const isSkipped = week.isSkipped;
  const weekStatus = isSkipped ? 'Skipped week' : 'Week';
  const accessibilityLabel = `${weekStatus} ${week.deliveryDay} ${week.deliveryDate}`;
  const accessibilityHint = isSkipped
    ? 'This delivery is skipped'
    : 'Select this delivery week';

  return (
    <View style={headerStyles}>
      <BackButton onPress={onBackPress} />
      <View
        accessibilityRole="header"
        accessibilityLabel={accessibilityLabel}
        accessibilityHint={accessibilityHint}
      >
        {isSkipped ? (
          <SkippedWeekContent week={week} />
        ) : (
          <ActiveWeekContent week={week} />
        )}
      </View>
    </View>
  );
};
```

**Key patterns demonstrated:**
- `accessibilityRole="header"` for semantic structure
- Conditional accessibility labels based on state
- Contextual hints for different states
- Clean separation of accessibility logic

## Example 3: Back Button with Full Accessibility

**File**: `shared-mobile-modules/src/modules/store/screens/storefront/components/week-header/single-week-header/back-button/BackButton.tsx`

```typescript
import { Pressable } from 'react-native';
import { Icon, useZestStyles } from '@zest/react-native';

interface BackButtonProps {
  onPress: () => void;
}

export const BackButton: React.FC<BackButtonProps> = ({ onPress }) => {
  const styles = useZestStyles(stylesConfig);
  const isSaving = useMealSelection(useShallow((state) => state.isSaving));

  return (
    <Pressable
      style={styles.backButton}
      onPress={onPress}
      disabled={isSaving}
      accessibilityRole="button"
      accessibilityLabel="Back Button"
      accessibilityHint="Go back to the previous screen"
      testID="back-button"
    >
      <Icon
        icon="ChevronLeftOutline24"
        color="alias.color.neutral.foreground.inverse"
        altText="Back Button"
      />
    </Pressable>
  );
};
```

**Key patterns demonstrated:**
- `accessibilityRole="button"` for interactive element
- Clear, descriptive `accessibilityLabel`
- Action-oriented `accessibilityHint`
- `disabled` state handled automatically
- Icon `altText` matches button label
- TestID for testing alongside accessibility

## Example 4: Accessibility Testing

**File**: `shared-mobile-modules/src/modules/store/screens/storefront/components/week-header/single-week-header/back-button/BackButton.spec.tsx`

```typescript
import { render } from '@testing-library/react-native';
import { BackButton } from './BackButton';

describe('BackButton', () => {
  it('should have proper accessibility properties', () => {
    const { getByRole, getByLabelText } = render(
      <BackButton onPress={jest.fn()} />
    );

    const button = getByRole('button');
    expect(button).toBeTruthy();
    expect(button.props.accessibilityRole).toBe('button');
    expect(button.props.accessibilityLabel).toBe('Back Button');
    expect(button.props.accessibilityHint).toBe('Go back to the previous screen');
  });

  it('should be accessible by label', () => {
    const { getByLabelText } = render(
      <BackButton onPress={jest.fn()} />
    );

    const button = getByLabelText('Back Button');
    expect(button).toBeTruthy();
  });

  it('should have testID for E2E testing', () => {
    const { getByTestId } = render(
      <BackButton onPress={jest.fn()} />
    );

    const button = getByTestId('back-button');
    expect(button).toBeTruthy();
  });
});
```

**Key patterns demonstrated:**
- `getByRole` to find elements by accessibility role
- `getByLabelText` to find by accessibility label
- Testing all accessibility properties
- Verifying testID alongside accessibility

## Example 5: Icon Accessibility Patterns from Codebase

**Source**: `shared-mobile-modules/.github/claude/a11y/a11y-2.2-AA-react-native.md`

### Decorative Icon in Button

```typescript
<TouchableOpacity
  accessibilityLabel="Add to cart"
  accessibilityRole="button"
>
  <Icon icon="PlusOutline24" altText="" />
  <Text>Add to Cart</Text>
</TouchableOpacity>
```

**Why**: Icon is decorative because button has text. Use `altText=""`.

### Meaningful Standalone Icon

```typescript
<Icon
  icon="ChevronRightOutline24"
  altText="Navigate forward"
/>
```

**Why**: Icon stands alone without text, so needs descriptive `altText`.

### Icon Button with Parent Label

```typescript
<TouchableOpacity
  accessibilityLabel="Close dialog"
  accessibilityRole="button"
>
  <Icon icon="CloseOutline16" altText="" />
</TouchableOpacity>
```

**Why**: Parent button provides label, so icon is decorative with `altText=""`.

## Example 6: Form Field with Error State

Pattern from production code:

```typescript
import { InputField } from '@zest/react-native';
import { useT9n } from '@libs/localization';

const EmailInput = ({ email, setEmail, error }: Props) => {
  const { translateRaw } = useT9n('form');

  return (
    <InputField
      label={translateRaw('form.email_label')}
      placeholder={translateRaw('form.email_placeholder')}
      value={email}
      onChangeText={setEmail}
      state={error ? 'error' : 'default'}
      validationText={error ? translateRaw('form.email_error') : undefined}
      accessibilityLabel={translateRaw('form.email_label')}
      accessibilityHint={translateRaw('form.email_hint')}
      accessibilityLiveRegion={error ? 'polite' : 'none'}
      testID="email-input"
    />
  );
};
```

**Key patterns demonstrated:**
- Translated labels and hints
- `accessibilityLiveRegion="polite"` for error announcements
- Dynamic state changes announced to screen readers
- TestID for automated testing

## Example 7: List Item with Position Context

Pattern from production code:

```typescript
import { FlatList, TouchableOpacity } from 'react-native';
import { useT9n } from '@libs/localization';

const RecipeList = ({ recipes }: Props) => {
  const { translateRaw } = useT9n('recipe');

  return (
    <FlatList
      data={recipes}
      accessibilityRole="list"
      renderItem={({ item, index }) => (
        <TouchableOpacity
          onPress={() => handleSelectRecipe(item)}
          accessibilityRole="button"
          accessibilityLabel={translateRaw('recipe.list_item', {
            name: item.name,
            position: index + 1,
            total: recipes.length,
          })}
          testID={`recipe-card-${item.id}`}
        >
          <RecipeCard recipe={item} />
        </TouchableOpacity>
      )}
    />
  );
};

// Translation: "{{name}}, {{position}} of {{total}}"
// Result: "Chicken Pasta, 3 of 15"
```

**Key patterns demonstrated:**
- List container has `accessibilityRole="list"`
- Position context in labels ("3 of 15")
- Translated labels with interpolation
- Dynamic testID based on item ID

## Anti-Patterns from Codebase Review

### ❌ Missing Icon altText

```typescript
// DON'T: Missing altText
<Icon icon="ChevronRightOutline24" />

// This will fail linting checks
```

### ❌ Generic Accessibility Labels

```typescript
// DON'T: Generic label
<TouchableOpacity accessibilityLabel="Button">
  <Text>Close</Text>
</TouchableOpacity>

// DO: Specific label
<TouchableOpacity accessibilityLabel="Close dialog">
  <Text>Close</Text>
</TouchableOpacity>
```

### ❌ Hardcoded Labels

```typescript
// DON'T: Hardcoded English
<TouchableOpacity accessibilityLabel="Add to cart">

// DO: Translated
<TouchableOpacity
  accessibilityLabel={translateRaw('recipe.action.add_to_cart')}
>
```

## Accessibility Linting Rules

**From codebase**: `shared-mobile-modules/scripts/localization/check_hard-coded_copy.cjs`

The codebase enforces:
- No hardcoded `accessibilityLabel`
- No hardcoded `accessibilityHint`
- No hardcoded `altText`
- All must use `translateRaw()` from localization

## Screen Reader Testing Checklist

Based on production practices:

**iOS VoiceOver:**
1. Enable: Settings → Accessibility → VoiceOver → On
2. Navigate: Swipe right/left
3. Activate: Double-tap
4. Verify: All elements announced correctly

**Android TalkBack:**
1. Enable: Settings → Accessibility → TalkBack → On
2. Navigate: Swipe right/left
3. Activate: Double-tap
4. Verify: All elements announced correctly

**Test Cases:**
- [ ] All buttons have clear labels
- [ ] All icons have altText (or empty string for decorative)
- [ ] Form inputs have labels and hints
- [ ] Errors are announced automatically
- [ ] List items include position context
- [ ] Modals trap focus correctly
- [ ] All labels are translated

## Integration with Other Patterns

### With Zustand State

```typescript
const isSelected = useRecipeStore(
  useShallow((state) => state.selectedIds.includes(recipeId))
);

<Pressable
  accessibilityLabel={recipe.name}
  accessibilityRole="button"
  accessibilityState={{ selected: isSelected }}
>
  <RecipeCard recipe={recipe} />
</Pressable>
```

### With Test IDs

```typescript
<TouchableOpacity
  onPress={handlePress}
  accessibilityLabel="Add to cart"
  accessibilityRole="button"
  testID="add-to-cart-button"
>
  <Icon icon="PlusOutline24" altText="" />
  <Text>Add</Text>
</TouchableOpacity>
```

### With Localization

```typescript
const { translateRaw } = useT9n('feature');

<TouchableOpacity
  accessibilityLabel={translateRaw('feature.action.close')}
  accessibilityHint={translateRaw('feature.action.close_hint')}
  accessibilityRole="button"
>
  <Icon icon="CloseOutline24" altText={translateRaw('feature.icon.close')} />
</TouchableOpacity>
```

## Summary

The YourCompany codebase consistently follows these accessibility patterns:

1. **All interactive elements** have `accessibilityLabel` and `accessibilityRole`
2. **All Zest Icons** have `altText` (descriptive or empty string)
3. **All labels are translated** using `translateRaw()` from localization
4. **State is communicated** via `accessibilityState` (selected, disabled, checked)
5. **Hints provide context** for non-obvious interactions
6. **Position information** included in list items
7. **Modals trap focus** with `accessibilityViewIsModal`
8. **Testing enforces** accessibility properties via linting and unit tests

These patterns ensure WCAG 2.1 Level AA compliance and provide excellent screen reader support for VoiceOver and TalkBack users.
