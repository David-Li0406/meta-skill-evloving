---
name: rn-accessibility
description: "WHAT: React Native accessibility with accessibilityLabel, accessibilityRole, and Icon altText. WHEN: interactive elements, form inputs, images, lists, modals, testing with VoiceOver/TalkBack. KEYWORDS: accessibilityLabel, accessibilityRole, accessibilityHint, altText, VoiceOver, TalkBack, screen reader, WCAG."
---

# Accessibility Patterns for React Native

## Documentation

This skill has comprehensive documentation:

- **[Production Examples](./references/examples.md)** - Real-world code examples from the codebase
- **[API Reference](./references/api-docs.md)** - Complete API documentation with official links
- **[Implementation Patterns](./references/patterns.md)** - Best practices and anti-patterns


## Core Principles

**Provide accessibility labels, roles, hints, and alt text for all interactive elements.** Use translated strings for labels and test with screen readers.

**Why**: Accessibility ensures the app is usable by everyone, including users with visual, auditory, motor, or cognitive disabilities. It's both ethical and required by law in many jurisdictions (WCAG 2.1 AA compliance).

## When to Use This Skill

Use these patterns when:

- Creating any interactive element (buttons, links, inputs)
- Adding icons or images to the UI
- Building forms with input fields
- Implementing lists, carousels, or dynamic content
- Creating modals, dialogs, or overlays
- Testing components with screen readers
- Ensuring WCAG 2.1 Level AA compliance

## Icon Accessibility

### Icon altText (REQUIRED)

**Always** provide `altText` for Zest Icon components. This prop is **required**, not optional:

```typescript
import { Icon } from '@zest/react-native';
import { useT9n } from '@libs/localization';

const HeaderButton = () => {
  const { translateRaw } = useT9n('feature');

  return (
    <TouchableOpacity
      onPress={handleClose}
      accessibilityLabel={translateRaw('feature.screen.header.close.label')}
      accessibilityRole="button"
      testID="close-button"
    >
      <Icon
        icon="CloseOutline24"
        color="alias.color.neutral.foreground.inverse"
        altText={translateRaw('feature.screen.header.close.alt_text')}
      />
    </TouchableOpacity>
  );
};
```

**Why**: The `altText` prop on Zest `Icon` is **required** and enables screen readers to describe icons. This is Zest-specific and differs from standard React Native `accessibilityLabel`. The component will not compile without it.

### Decorative Icons

Mark decorative icons with empty `altText`:

```typescript
<TouchableOpacity
  accessibilityLabel="Add recipe to cart"
  accessibilityRole="button"
>
  <Icon icon="PlusOutline24" altText="" />
  <Text>Add to Cart</Text>
</TouchableOpacity>
```

**Why**: Empty `altText=""` tells screen readers to skip decorative icons. The button's `accessibilityLabel` already describes the action, so the icon doesn't need additional description.

### Meaningful vs Decorative Icons

```typescript
// ✅ Meaningful icon (stands alone)
<Icon
  icon="ChevronRightOutline24"
  altText="Navigate forward"
/>

// ✅ Decorative icon (in button with text)
<TouchableOpacity accessibilityLabel="Save recipe">
  <Icon icon="BookmarkOutline24" altText="" />
  <Text>Save</Text>
</TouchableOpacity>

// ✅ Decorative icon (parent has label)
<Pressable
  accessibilityLabel="View past deliveries"
  accessibilityRole="button"
>
  <Icon icon="HistoryOutline24" altText="" />
</Pressable>
```

**Rule**: Use `altText=""` when the icon is decorative or the parent element already has a descriptive label. Use descriptive `altText` when the icon stands alone and conveys meaning.

## Interactive Element Accessibility

### accessibilityLabel

Provide clear, descriptive labels for all interactive elements:

```typescript
import { useT9n } from '@libs/localization';

const AddToCartButton = () => {
  const { translateRaw } = useT9n('recipe');

  return (
    <TouchableOpacity
      onPress={handleAddToCart}
      accessibilityLabel={translateRaw('recipe.action.add_to_cart')}
      accessibilityRole="button"
      testID="add-to-cart-button"
    >
      <Icon icon="PlusOutline24" altText="" />
      <Text>Add to Cart</Text>
    </TouchableOpacity>
  );
};

// Translation: "Add recipe to cart"
```

**Why**: `accessibilityLabel` provides a clear description of what the element does, overriding default behavior for screen readers.

**Important**: Always use translated strings from localization, never hardcode labels.

### accessibilityRole

Specify semantic roles for elements:

```typescript
// Buttons
<TouchableOpacity
  onPress={handlePress}
  accessibilityRole="button"
  accessibilityLabel="Save recipe"
>
  <Text>Save</Text>
</TouchableOpacity>

// Headers
<View accessibilityRole="header">
  <Text type="headline-lg">My Recipes</Text>
</View>

// Search inputs
<TextInput
  accessibilityRole="search"
  accessibilityLabel="Search recipes"
  placeholder="Search..."
/>

// Links
<TouchableOpacity
  onPress={handleNavigate}
  accessibilityRole="link"
  accessibilityLabel="View all recipes"
>
  <Text decoration="link">View All</Text>
</TouchableOpacity>

// Tab lists
<ScrollView
  horizontal
  accessibilityRole="tablist"
  accessibilityLabel="Week selector"
>
  {weeks.map(renderWeekTab)}
</ScrollView>

// Individual tabs
<Pressable
  accessibilityRole="button"
  accessibilityLabel={`Week ${week.deliveryDay} ${week.deliveryDate}`}
  accessibilityState={{ selected: isSelected }}
>
  <Text>{week.deliveryDay}</Text>
</Pressable>
```

**Available roles:**
- `button` - Interactive buttons
- `header` - Section headers
- `search` - Search inputs
- `link` - Navigation links
- `text` - Static text
- `image` - Images
- `imagebutton` - Image buttons
- `tablist` - Tab containers
- `none` - Explicitly no role (for layout elements)

**Why**: Roles help screen readers understand element purpose, behavior, and how to interact with them.

### accessibilityHint

Provide hints for complex or non-obvious interactions:

```typescript
<Pressable
  onPress={handleSelectWeek}
  accessibilityLabel="Week Monday January 15"
  accessibilityRole="button"
  accessibilityHint="Select this delivery week"
  accessibilityState={{ selected: isSelected }}
>
  <WeekContent week={week} />
</Pressable>

<TouchableOpacity
  onPress={handleViewPastDeliveries}
  accessibilityRole="button"
  accessibilityLabel="View past deliveries"
  accessibilityHint="Navigate to past delivery history"
>
  <Text>Past Deliveries</Text>
</TouchableOpacity>
```

**Why**: Hints explain what will happen when the user interacts with an element. Use for actions that aren't obvious from the label alone.

**Best practice**: Keep hints concise and action-oriented (e.g., "Select this week", "Navigate to details").

### accessibilityState

Indicate element state for screen readers:

```typescript
<Pressable
  accessibilityLabel={`Week ${week.deliveryDay} ${week.deliveryDate}`}
  accessibilityRole="button"
  accessibilityState={{
    selected: isSelected,
    disabled: week.isPast,
  }}
>
  <WeekCard week={week} />
</Pressable>

<Checkbox
  checked={isChecked}
  onValueChange={setIsChecked}
  accessibilityLabel="Agree to terms"
  accessibilityState={{
    checked: isChecked,
  }}
/>
```

**Available states:**
- `selected` - Element is selected (tabs, list items)
- `disabled` - Element cannot be interacted with
- `checked` - Checkbox/toggle is checked
- `busy` - Element is loading or processing

**Why**: State information helps screen reader users understand the current status of interactive elements.

## Form Accessibility

### Label Input Fields

Always provide labels and hints for form inputs:

```typescript
import { InputField } from '@zest/react-native';
import { useT9n } from '@libs/localization';

const EmailInput = () => {
  const { translateRaw } = useT9n('form');

  return (
    <InputField
      label={translateRaw('form.email_label')}
      placeholder={translateRaw('form.email_placeholder')}
      value={email}
      onChangeText={setEmail}
      accessibilityLabel={translateRaw('form.email_label')}
      accessibilityHint={translateRaw('form.email_hint')}
      testID="email-input"
    />
  );
};

// Translations:
// form.email_label: "Email address"
// form.email_placeholder: "you@example.com"
// form.email_hint: "Enter your email address"
```

**Why**: Labeled inputs are accessible and easier to use. The label is read by screen readers when the input receives focus.

### Error Messages with Live Regions

Make error messages accessible with live regions:

```typescript
<InputField
  label="Email"
  value={email}
  onChangeText={setEmail}
  state="error"
  validationText="Please enter a valid email address"
  accessibilityLabel="Email input"
  accessibilityLiveRegion="polite"
  accessibilityRole="none"
  testID="email-input-error"
/>
```

**Live region values:**
- `polite` - Announce after current speech completes (preferred for errors)
- `assertive` - Interrupt current speech immediately (use sparingly)
- `none` - Don't announce automatically

**Why**: Live regions announce dynamic content changes (like validation errors) to screen readers without requiring user interaction.

### Form Field Groups

Group related form fields:

```typescript
<View
  accessibilityRole="none"
  accessibilityLabel="Shipping address"
>
  <InputField
    label="Street address"
    accessibilityLabel="Street address"
  />
  <InputField
    label="City"
    accessibilityLabel="City"
  />
  <InputField
    label="Postal code"
    accessibilityLabel="Postal code"
  />
</View>
```

**Why**: Grouping provides context for related fields, helping screen reader users understand the form structure.

## Image Accessibility

### Meaningful Images

Provide descriptive alt text for meaningful images:

```typescript
import { Image } from 'react-native';
import { useT9n } from '@libs/localization';

const RecipeImage = ({ recipe }: Props) => {
  const { translateRaw } = useT9n('recipe');

  return (
    <Image
      source={{ uri: recipe.imageUrl }}
      accessible={true}
      accessibilityLabel={translateRaw('recipe.image_alt', { name: recipe.name })}
      style={styles.image}
    />
  );
};

// Translation: "Photo of {{name}}"
// Result: "Photo of Chicken Pasta"
```

**Why**: Alt text describes images to users who cannot see them. Be specific and descriptive.

### Decorative Images

Mark decorative images as not accessible:

```typescript
<Image
  source={require('./decorative-pattern.png')}
  accessible={false}
  style={styles.decoration}
/>
```

**Why**: Decorative images don't convey meaning, so screen readers should skip them to reduce noise.

## List Accessibility

### List Items with Position Context

Provide position information for list items:

```typescript
import { FlatList } from 'react-native';
import { useT9n } from '@libs/localization';

const RecipeList = ({ recipes }: Props) => {
  const { translateRaw } = useT9n('recipe');

  return (
    <FlatList
      data={recipes}
      accessibilityRole="list"
      renderItem={({ item, index }) => (
        <TouchableOpacity
          onPress={() => handlePress(item)}
          accessibilityLabel={translateRaw('recipe.list_item', {
            name: item.name,
            position: index + 1,
            total: recipes.length,
          })}
          accessibilityRole="button"
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

**Why**: Position context helps users navigate long lists and understand where they are.

### Horizontal Scrollable Lists

Provide clear labels and hints for horizontal scrollable content:

```typescript
<ScrollView
  horizontal
  accessibilityRole="tablist"
  accessibilityLabel="Week selector"
  accessibilityHint="Select delivery week from the list"
  showsHorizontalScrollIndicator={false}
>
  {weeks.map(renderWeek)}
</ScrollView>
```

**Why**: Horizontal scrolling isn't always obvious. Clear labels and hints help users understand the interaction.

## Modal and Dialog Accessibility

### Modal Focus Trapping

Set proper accessibility properties for modals:

```typescript
import { Dialog } from '@zest/react-native';
import { useT9n } from '@libs/localization';

const ConfirmDialog = ({ visible, onDismiss }: Props) => {
  const { translateRaw } = useT9n('dialog');

  return (
    <Dialog
      visible={visible}
      onDismiss={onDismiss}
      title={translateRaw('dialog.confirm.title')}
      description={translateRaw('dialog.confirm.description')}
      accessible={true}
      accessibilityLabel={translateRaw('dialog.confirm.title')}
      accessibilityRole="alert"
      accessibilityViewIsModal={true}
      testID="confirm-dialog"
      buttons={[
        {
          title: translateRaw('dialog.confirm.cancel'),
          onPress: onDismiss,
          testID: 'cancel-button',
        },
        {
          title: translateRaw('dialog.confirm.confirm'),
          onPress: handleConfirm,
          testID: 'confirm-button',
        },
      ]}
    />
  );
};
```

**Key properties:**
- `accessibilityRole="alert"` - Announces modal opening
- `accessibilityViewIsModal={true}` - Traps focus within modal
- `accessible={true}` - Makes modal accessible to screen readers

**Why**: `accessibilityViewIsModal` prevents screen readers from navigating outside the modal, ensuring users focus on the modal content.

## Accessibility Scaling

### maxFontSizeMultiplier for Text

Zest Text component includes `maxFontSizeMultiplier={2}` by default for accessibility scaling:

```typescript
import { Text } from '@zest/react-native';

// Default: maxFontSizeMultiplier={2} is applied
<Text type="body-md-regular">{content}</Text>

// Disable scaling for fixed-size UI (use sparingly)
<Text type="body-md-regular" maxFontSizeMultiplier={1}>
  Fixed size text
</Text>
```

**Why**: `maxFontSizeMultiplier` limits how much text can scale when users increase system font size, preventing layout breaking while still supporting accessibility.

### allowAccessibilityScaling for Components

Some Zest components support `allowAccessibilityScaling` prop:

```typescript
import { Spinner } from '@zest/react-native';

// Allow spinner to scale with system font settings
<Spinner size="lg" allowAccessibilityScaling={true} />
```

**Why**: Components like Spinner can scale with user font preferences to remain visible for users who need larger UI elements.

## Testing Accessibility

### Screen Reader Testing

Test with platform screen readers:

**iOS - VoiceOver:**
1. Settings → Accessibility → VoiceOver → On
2. Triple-click home/side button to toggle
3. Swipe right/left to navigate
4. Double-tap to activate

**Android - TalkBack:**
1. Settings → Accessibility → TalkBack → On
2. Volume keys to toggle
3. Swipe right/left to navigate
4. Double-tap to activate

### Automated Testing

Test accessibility properties in unit tests:

```typescript
import { render } from '@testing-library/react-native';

test('button is accessible', () => {
  const { getByLabelText, getByRole } = render(<AddToCartButton />);

  const button = getByLabelText('Add recipe to cart');
  expect(button).toBeTruthy();
  expect(button.props.accessibilityRole).toBe('button');
});

test('icon has proper alt text', () => {
  const { getByA11yHint } = render(<HeaderButton />);

  const button = getByA11yHint('Close screen');
  expect(button).toBeTruthy();
});

test('list item includes position', () => {
  const { getByLabelText } = render(<RecipeList recipes={mockRecipes} />);

  expect(getByLabelText(/1 of 5/)).toBeTruthy();
  expect(getByLabelText(/5 of 5/)).toBeTruthy();
});
```

**Why**: Automated tests catch missing accessibility properties during development.

## Common Mistakes to Avoid

❌ **Don't forget accessibility labels**:

```typescript
// ❌ Bad - No label
<TouchableOpacity onPress={handlePress}>
  <Icon icon="CloseOutline24" />
</TouchableOpacity>
```

❌ **Don't use generic labels**:

```typescript
// ❌ Bad - Generic
<TouchableOpacity accessibilityLabel="Button">
  <Text>Close</Text>
</TouchableOpacity>
```

❌ **Don't hardcode labels**:

```typescript
// ❌ Bad - Hardcoded, not translated
<TouchableOpacity
  accessibilityLabel="Close screen"
  accessibilityRole="button"
>
  <Icon icon="CloseOutline24" altText="Close" />
</TouchableOpacity>
```

❌ **Don't forget Icon altText**:

```typescript
// ❌ Bad - Missing altText
<Icon icon="ChevronRightOutline24" color="brand.primary" />
```

✅ **Do provide descriptive, translated labels**:

```typescript
// ✅ Good - Descriptive, translated
const { translateRaw } = useT9n('feature');

<TouchableOpacity
  onPress={handleClose}
  accessibilityLabel={translateRaw('feature.action.close_screen')}
  accessibilityRole="button"
  testID="close-button"
>
  <Icon
    icon="CloseOutline24"
    altText={translateRaw('feature.action.close')}
  />
</TouchableOpacity>
```

✅ **Do use empty altText for decorative icons**:

```typescript
// ✅ Good - Empty altText for decorative icon
<TouchableOpacity
  accessibilityLabel="Save recipe"
  accessibilityRole="button"
>
  <Icon icon="BookmarkOutline24" altText="" />
  <Text>Save</Text>
</TouchableOpacity>
```

✅ **Do test with screen readers**:

```typescript
// ✅ Good - Test on real devices
// 1. Enable VoiceOver (iOS) or TalkBack (Android)
// 2. Navigate through entire flow
// 3. Verify all elements are announced correctly
// 4. Confirm no missing labels or unclear descriptions
```

## Quick Reference

**Required Accessibility Properties:**

| Element | Required Props | Example |
|---------|---------------|---------|
| Button | `accessibilityLabel`, `accessibilityRole` | `accessibilityLabel="Add to cart"` `accessibilityRole="button"` |
| Icon (Zest) | `altText` | `altText="Close"` or `altText=""` for decorative |
| Image | `accessible`, `accessibilityLabel` | `accessible={true}` `accessibilityLabel="Photo of recipe"` |
| Input | `accessibilityLabel`, `accessibilityHint` | `accessibilityLabel="Email"` `accessibilityHint="Enter your email"` |
| Header | `accessibilityRole` | `accessibilityRole="header"` |
| List | `accessibilityRole` | `accessibilityRole="list"` |
| Modal | `accessibilityViewIsModal`, `accessibilityRole` | `accessibilityViewIsModal={true}` `accessibilityRole="alert"` |

**Key Patterns:**
- ✅ Always translate labels with `useT9n`
- ✅ Use `altText=""` for decorative icons
- ✅ Provide `accessibilityHint` for complex interactions
- ✅ Use `accessibilityState` for selected/disabled/checked states
- ✅ Set `accessibilityViewIsModal={true}` for modals
- ✅ Test with VoiceOver (iOS) and TalkBack (Android)
- ✅ Include position context in list items

**Testing:**
- Manual: VoiceOver (iOS), TalkBack (Android)
- Automated: `getByLabelText`, `getByRole`, `getByA11yHint`

**Key Libraries:**
- React Native 0.76+
- @zest/react-native 1.5.3
- @libs/localization (i18next 24.2.1)

For production examples, see [references/examples.md](references/examples.md).
