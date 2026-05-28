---
name: zest-components
description: "WHAT: Zest design system components for React Native including Button, Text, Icon, Card, Badge, InputField. WHEN: building UI with buttons, forms, icons, cards, status indicators, loading states, inline messages. KEYWORDS: Button, Text, Icon, IconButton, Card, Badge, InputField, InlineMessage, Tag, Spinner, testID, altText."
---

# Zest Design System Components

## Core Principles

**Always use Zest components instead of custom implementations.** Zest provides pre-built, accessible components with consistent styling, behavior, and theme integration. Creating custom components duplicates work and breaks design consistency.

**Always provide testID for all interactive components.** testID enables reliable UI testing with @testing-library/react-native. Every button, input, card, and interactive element requires a unique testID.

**Always provide altText for icons for accessibility.** Icons need descriptive alt text for screen readers. Without altText, visually impaired users cannot understand icon meaning.

**Use correct component variants for semantic meaning.** Button variants (primary/secondary/text), Card variants (static/navigational/selectable), and InlineMessage variants (success/error/warning/info) provide semantic meaning and consistent styling.

**Why**: Zest components ensure design consistency, built-in accessibility, automatic theme support, and reduce custom code maintenance.

## When to Use This Skill

Use these patterns when:

- Building any UI component in the app
- Creating forms with inputs, checkboxes, switches
- Displaying content in cards or containers
- Showing buttons for user actions
- Providing feedback with messages or alerts
- Displaying loading states with spinners
- Showing icons for visual communication
- Creating navigational elements
- Implementing selectable or filterable lists
- Displaying status with badges or tags

## Button Component

### Button Variants and Sizes

Use Button component with variants for different button styles and semantic meaning.

```typescript
import { Button } from '@zest/react-native';

// Primary button (main actions)
<Button
  variant="primary"
  size="lg"
  appearance="brand"
  onPress={handleSubmit}
  testID="submit-button"
>
  Submit
</Button>

// Secondary button (secondary actions)
<Button
  variant="secondary"
  size="md"
  appearance="neutral"
  onPress={handleCancel}
  testID="cancel-button"
>
  Cancel
</Button>

// Text button (subtle actions)
<Button
  variant="text"
  size="sm"
  onPress={handleMore}
  testID="learn-more-button"
>
  Learn More
</Button>

// Disabled button
<Button
  variant="primary"
  disabled={!isFormValid}
  onPress={handleSubmit}
  testID="submit-button"
>
  Submit
</Button>

// Loading button
<Button
  variant="primary"
  loading={isSubmitting}
  disabled={isSubmitting}
  onPress={handleSubmit}
  testID="submit-button"
>
  Submit
</Button>
```

**Variants:**
- `primary` - Filled button with solid background (main actions)
- `secondary` - Outlined button with border (secondary actions)
- `text` - Text-only button without background (subtle actions)

**Sizes:**
- `sm` - Small (32px height)
- `md` - Medium (40px height, default)
- `lg` - Large (48px height)

**Appearances:**
- `brand` - Brand color (primary actions, default)
- `neutral` - Neutral color (secondary actions)
- `critical` / `negative` - Error/destructive actions

**Why**: Button variants provide semantic meaning (primary vs secondary), sizes ensure consistent touch targets, appearances communicate action importance.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/store/components/floating-store-button/FloatingStoreButton.tsx:82`

## Text Component

### Text Types for Typography Hierarchy

Use Text component with type prop for consistent typography styles.

```typescript
import { Text } from '@zest/react-native';

// Headlines (titles, headings)
<Text type="headline-xl">{recipe.name}</Text>
<Text type="headline-lg">{section.title}</Text>
<Text type="headline-md">{card.title}</Text>

// Body text (content, descriptions)
<Text type="body-lg-regular">{content.description}</Text>
<Text type="body-md-regular">{content.body}</Text>
<Text type="body-sm-regular">{content.caption}</Text>

// Bold variants (labels, emphasis)
<Text type="body-md-bold">{label}</Text>
<Text type="body-sm-bold">{badge}</Text>

// Text with props
<Text
  type="body-md-regular"
  numberOfLines={2}
  ellipsizeMode="tail"
  testID="description-text"
>
  {longDescription}
</Text>
```

**Type Variants:**
- `headline-xl` - Extra large headline (32px)
- `headline-lg` - Large headline (24px)
- `headline-md` - Medium headline (20px)
- `body-lg-regular` - Large body text (18px)
- `body-md-regular` - Medium body text (16px, default)
- `body-sm-regular` - Small body text (14px)
- `body-md-bold` - Medium bold text (16px, 700 weight)
- `body-sm-bold` - Small bold text (14px, 700 weight)

**Common Props:**
- `numberOfLines` - Truncate text after N lines
- `ellipsizeMode` - Where to truncate ('head', 'middle', 'tail')
- `testID` - Test identifier

**Why**: Text types ensure consistent typography hierarchy and automatic theme integration (font family, size, line height, color from theme).

**Production Example**: `git-resources/shared-mobile-modules/src/modules/social-recipe-bridge/screens/social-recipe-bridge/components/recipe-card/RecipeCard.tsx:77`

## Icon Component

### Icon Naming Convention

Use Icon component with consistent naming convention: `{Name}{Variant}{Size}`.

```typescript
import { Icon } from '@zest/react-native';

// Basic icon
<Icon icon="HeartOutline24" altText="Favorite" />

// Icon with color (use theme tokens)
<Icon
  icon="CheckmarkOutline24"
  color="alias.color.semantic.success.foreground.default"
  altText="Success"
/>

// Icon with custom size
<Icon
  icon="InfoOutline24"
  size={32}
  color="alias.color.brand.foreground.default"
  altText="Information"
/>

// Decorative icon (no alt text)
<Icon icon="ImageOutline24" altText="" />
```

**Icon Naming Convention:**
- Format: `{Name}{Variant}{Size}`
- Examples: `HeartOutline24`, `CheckmarkFilled32`, `CartOutline24`
- Variants: `Outline` (outlined), `Filled` (solid)
- Sizes: `16`, `24` (most common), `32`, `40`, `48`

**Props:**
- `icon` - Icon name (required)
- `altText` - Accessibility label (required, empty string for decorative)
- `color` - Theme token string
- `size` - Custom size override

**Why**: Consistent naming makes icons discoverable, altText ensures accessibility, size flexibility adapts to different contexts.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/store/components/floating-store-button/FloatingStoreButton.tsx:110`

## IconButton and IconButtonToggle

### Clickable Icon Buttons

Use IconButton for clickable icons, IconButtonToggle for toggle states.

```typescript
import { IconButton, IconButtonToggle } from '@zest/react-native';

// Simple icon button
<IconButton
  icon="ShareOutline24"
  onPress={handleShare}
  size="md"
  appearance="neutral"
  testID="share-button"
/>

// Icon button with accessibility
<IconButton
  icon="BookmarkFilled16"
  appearance="neutral"
  shape="square"
  onPress={handleDelete}
  accessibilityHint="Remove from saved recipes"
  accessibilityLabel="Remove recipe"
  altText="Remove recipe"
  size="sm"
  testID="delete-button"
/>

// Toggle button (favorites, likes, bookmarks)
<IconButtonToggle
  activeIcon="HeartFilled24"
  inactiveIcon="HeartOutline24"
  isActive={isFavorited}
  onToggle={handleToggleFavorite}
  altText={isFavorited ? 'Remove from favorites' : 'Add to favorites'}
  size="sm"
  testID="favorite-button"
/>
```

**IconButton Props:**
- `icon` - Icon name
- `onPress` - Click handler
- `size` - Button size (sm/md/lg)
- `shape` - Button shape (circle/square)
- `appearance` - Color appearance (brand/neutral/critical)
- `testID` - Test identifier
- `accessibilityLabel` / `accessibilityHint` / `altText` - Accessibility

**IconButtonToggle Props:**
- `activeIcon` - Icon when active (e.g., HeartFilled24)
- `inactiveIcon` - Icon when inactive (e.g., HeartOutline24)
- `isActive` - Current toggle state
- `onToggle` - Toggle handler
- `altText` - Dynamic accessibility label

**Why**: IconButton provides consistent touch targets and feedback, IconButtonToggle shows clear toggle state visually (filled vs outline).

**Production Example**: `git-resources/shared-mobile-modules/src/modules/social-recipe-bridge/screens/social-recipe-bridge/components/recipe-card/RecipeCard.tsx:53`

## Form Components

### InputField for Text Input

Use InputField for all text input with built-in validation styling.

```typescript
import { InputField } from '@zest/react-native';

// Basic input
<InputField
  label="Email"
  value={email}
  onChangeText={setEmail}
  placeholder="Enter your email"
  testID="email-input"
/>

// Input with error
<InputField
  label="Password"
  value={password}
  onChangeText={setPassword}
  placeholder="Enter password"
  secureTextEntry
  error="Password must be at least 8 characters"
  testID="password-input"
/>

// Input with helper text
<InputField
  label="Recipe Name"
  value={recipeName}
  onChangeText={setRecipeName}
  helperText="Give your recipe a memorable name"
  maxLength={100}
  testID="recipe-name-input"
/>

// Disabled input
<InputField
  label="Order ID"
  value={orderId}
  editable={false}
  testID="order-id-input"
/>

// Input with ref
const inputRef = useRef<InputFieldRef>(null);

<InputField
  label="Username"
  value={username}
  ref={inputRef}
  onChangeText={setUsername}
  autoCapitalize="none"
  testID="username-input"
/>
```

**Props:**
- `label` - Field label (required)
- `value` / `onChangeText` - Controlled input
- `placeholder` - Placeholder text
- `error` - Error message (shows red border)
- `helperText` - Helper text below input
- `secureTextEntry` - Hide text for passwords
- `editable` - Enable/disable editing
- `ref` - Input ref (InputFieldRef type)
- `testID` - Test identifier

**Why**: InputField provides consistent form inputs with automatic validation styling (error states), built-in label/helper text, and theme integration.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/test-playground/screens/sign-in/components/authentication-form/AuthenticationForm.tsx:66`

### TextArea for Multi-line Input

Use TextArea for multi-line text input.

```typescript
import { TextArea } from '@zest/react-native';

<TextArea
  label="Description"
  value={description}
  onChangeText={setDescription}
  placeholder="Enter description"
  helperText="Maximum 500 characters"
  maxLength={500}
  testID="description-textarea"
/>
```

**Why**: TextArea provides multi-line text input with consistent styling and character count support.

## Card Component

### Card Variants for Different Interactions

Use Card with variants for different interaction patterns.

```typescript
import { Card } from '@zest/react-native';

// Static card (default, non-interactive)
<Card testID="info-card">
  <Text type="headline-md">{title}</Text>
  <Text type="body-md-regular">{description}</Text>
</Card>

// Navigational card (clickable)
<Card
  variant="navigational"
  onPress={handleNavigate}
  testID="recipe-card"
>
  <Text type="headline-md">{recipe.name}</Text>
</Card>

// Selectable card (with selection state)
<Card.Selectable
  style={styles.container}
  padding="none"
  variant="transparent"
  onPress={handleSelect}
  accessibilityLabel="Recipe card"
  accessibilityHint="Tap to open recipe"
  testID="recipe-card"
>
  <Image source={{ uri: imageUrl }} style={styles.image} />
  <Text type="body-md-bold">{title}</Text>
</Card.Selectable>

// Card with custom padding
<Card padding="lg" testID="content-card">
  {/* content */}
</Card>
```

**Variants:**
- `Card` (default) - Static card, non-interactive
- `Card.Navigational` - Clickable card for navigation
- `Card.Selectable` - Card with selection state

**Padding:**
- `none` - No padding
- `sm` / `md` / `lg` - Small/medium/large padding

**Props:**
- `variant` - Card style variant
- `padding` - Internal padding
- `onPress` - Press handler (for navigational/selectable)
- `style` - Additional styles
- `testID` - Test identifier

**Why**: Card variants communicate interaction type visually and semantically. Static cards contain content, navigational cards show press states, selectable cards show selection state.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/social-recipe-bridge/screens/social-recipe-bridge/components/recipe-card/RecipeCard.tsx:142`

## Status and Loading Components

### Badge for Status Indicators

Use Badge for status indicators and count displays.

```typescript
import { Badge, withBadge } from '@zest/react-native';

// Status badge
<Badge
  label="New"
  variant="brand"
  size="sm"
  testID="new-badge"
/>

// Count badge
<Badge
  content={String(cartCount)}
  size="xs"
  variant="positive"
  testID="cart-count-badge"
/>

// Badge with icon using withBadge HOC
const IconWithBadge = withBadge(Icon, {
  placement: 'top-right',
  badgeContent: '5',
});

<IconWithBadge icon="NotificationOutline24" />
```

**Variants:**
- `brand` - Brand color
- `neutral` - Neutral/default
- `critical` / `negative` - Error/warning
- `success` / `positive` - Success/confirmed

**Sizes:**
- `xs` - Extra small (count badges)
- `sm` - Small (status badges)
- `md` - Medium

**Why**: Badges draw attention to status or counts, with color variants providing semantic meaning.

**Production Example**: `git-resources/shared-mobile-modules/src/modules/store/components/floating-store-button/FloatingStoreButton.tsx:113`

### Spinner for Loading States

Use Spinner for loading indicators.

```typescript
import { Spinner } from '@zest/react-native';

// Loading state
{isLoading && <Spinner size="lg" testID="loading-spinner" />}

// Inline spinner with text
<View style={styles.row}>
  <Spinner size="sm" />
  <Text type="body-md-regular">Loading recipes...</Text>
</View>

// In Button (automatic)
<Button
  variant="primary"
  loading={isSubmitting}
  disabled={isSubmitting}
  onPress={handleSubmit}
>
  Submit
</Button>
```

**Sizes:**
- `sm` - Small (16px) - inline with text
- `md` - Medium (24px) - default
- `lg` - Large (32px) - full-screen loading

**Why**: Spinner provides visual feedback during async operations, with sizes appropriate for context (inline vs full-screen).

## Feedback Components

### InlineMessage for Contextual Feedback

Use InlineMessage for contextual feedback without disrupting flow.

```typescript
import { InlineMessage } from '@zest/react-native';

// Success message
<InlineMessage
  variant="success"
  message="Recipe added to your cookbook"
  testID="success-message"
/>

// Error message with action
<InlineMessage
  variant="error"
  message="Failed to load recipes. Please try again."
  onActionPress={handleRetry}
  actionLabel="Retry"
  testID="error-message"
/>

// Warning message
<InlineMessage
  variant="warning"
  message="Some ingredients may not be available"
  testID="warning-message"
/>

// Info message
<InlineMessage
  variant="info"
  message="Delivery scheduled for tomorrow"
  testID="info-message"
/>
```

**Variants:**
- `success` - Success confirmation (green)
- `error` - Error notification (red)
- `warning` - Warning alert (yellow)
- `info` - Informational message (blue)

**Props:**
- `variant` - Message type
- `message` - Message text
- `onActionPress` - Optional action handler
- `actionLabel` - Optional action button text
- `testID` - Test identifier

**Why**: InlineMessage provides contextual feedback with semantic color coding without modal interruption.

## Layout Components

### Divider for Visual Separation

Use Divider for visual separation between content sections.

```typescript
import { Divider } from '@zest/react-native';

<View>
  <Text>Section 1</Text>
  <Divider />
  <Text>Section 2</Text>
</View>
```

**Why**: Divider creates clear visual boundaries with consistent styling from theme.

## Selection Components

### Tag, TagStatic, TagFilter

Use Tag components for labels, selections, and filters.

```typescript
import { Tag, TagStatic, TagFilter } from '@zest/react-native';

// Selectable tag (interactive)
<Tag
  label="Vegetarian"
  selected={isSelected}
  onPress={handleToggle}
  variant="selectable"
  size="md"
  testID="vegetarian-tag"
/>

// Static tag (non-interactive label)
<TagStatic
  label="New"
  variant="brand"
  size="sm"
  testID="new-tag"
/>

// Filter tag (with remove button)
<TagFilter
  label="Gluten Free"
  selected={isSelected}
  onPress={handleToggle}
  onRemove={handleRemove}
  testID="gluten-free-filter"
/>
```

**When to Use:**
- **Tag** - Interactive selections (dietary preferences, categories)
- **TagStatic** - Non-interactive labels (badges, status indicators)
- **TagFilter** - Filter chips with remove functionality

**Why**: Different Tag components provide appropriate interaction patterns for different contexts (selection vs labeling vs filtering).

## Common Mistakes to Avoid

❌ **Don't create custom button components when Zest Button exists**:

```typescript
// ❌ Wrong - custom button
import { TouchableOpacity, Text } from 'react-native';

<TouchableOpacity style={styles.button} onPress={handlePress}>
  <Text style={styles.buttonText}>Submit</Text>
</TouchableOpacity>
```

**Why**: Custom buttons lack theme integration, accessibility features, loading states, and consistent styling.

✅ **Do use Zest Button**:

```typescript
// ✅ Correct - Zest button
import { Button } from '@zest/react-native';

<Button
  variant="primary"
  onPress={handlePress}
  testID="submit-button"
>
  Submit
</Button>
```

**Why**: Zest Button provides built-in theme support, loading states, disabled states, accessibility, and consistent styling.

❌ **Don't forget testID prop**:

```typescript
// ❌ Wrong - missing testID
<Button variant="primary" onPress={handlePress}>
  Submit
</Button>
```

**Why**: Without testID, UI tests cannot reliably find and interact with components.

✅ **Do always provide testID**:

```typescript
// ✅ Correct - testID provided
<Button
  variant="primary"
  onPress={handlePress}
  testID="submit-button"
>
  Submit
</Button>
```

**Why**: testID enables reliable UI testing with @testing-library/react-native.

❌ **Don't skip altText for icons (REQUIRED)**:

```typescript
// ❌ Wrong - missing altText (will cause accessibility issues)
<Icon icon="HeartOutline24" />
```

**Why**: `altText` is a REQUIRED prop on Icon components. Screen readers cannot describe icons without alt text, creating accessibility barriers.

✅ **Do ALWAYS provide altText**:

```typescript
// ✅ Correct - altText provided (REQUIRED)
<Icon icon="HeartOutline24" altText="Favorite" />

// ✅ Correct - empty altText for decorative icons
<Icon icon="ImageOutline24" altText="" />
```

**Why**: Alt text enables screen readers to describe icon meaning, improving accessibility for visually impaired users.

❌ **Don't use wrong card variant**:

```typescript
// ❌ Wrong - static card for navigation
<Card testID="recipe-card">
  <TouchableOpacity onPress={handleNavigate}>
    <Text>{recipe.name}</Text>
  </TouchableOpacity>
</Card>
```

**Why**: Static card doesn't show press states, wrapping content in TouchableOpacity creates nested press areas.

✅ **Do use correct card variant**:

```typescript
// ✅ Correct - navigational card
<Card
  variant="navigational"
  onPress={handleNavigate}
  testID="recipe-card"
>
  <Text>{recipe.name}</Text>
</Card>
```

**Why**: Navigational card provides built-in press states, proper accessibility, and consistent interaction feedback.

❌ **Don't use TagStatic for selections**:

```typescript
// ❌ Wrong - static tag for selection
<TagStatic
  label="Vegetarian"
  onPress={handleToggle} // onPress doesn't exist on TagStatic
/>
```

**Why**: TagStatic has no onPress prop and doesn't show selection state, it's only for non-interactive labels.

✅ **Do use Tag for selections, TagStatic for labels**:

```typescript
// ✅ Correct - Tag for selection
<Tag
  label="Vegetarian"
  selected={isSelected}
  onPress={handleToggle}
  variant="selectable"
/>

// ✅ Correct - TagStatic for label
<TagStatic
  label="New"
  variant="brand"
/>
```

**Why**: Tag provides selection state and press handling, TagStatic is for non-interactive labels only.

❌ **Don't mix custom components with Zest inconsistently**:

```typescript
// ❌ Wrong - mixing custom and Zest
<View>
  <Button variant="primary" onPress={handleSubmit}>Submit</Button>
  <TouchableOpacity style={styles.cancelButton} onPress={handleCancel}>
    <Text>Cancel</Text>
  </TouchableOpacity>
</View>
```

**Why**: Inconsistent components break design system consistency and create different interaction patterns.

✅ **Do use Zest components consistently**:

```typescript
// ✅ Correct - consistent Zest components
<View>
  <Button variant="primary" onPress={handleSubmit}>
    Submit
  </Button>
  <Button variant="secondary" onPress={handleCancel}>
    Cancel
  </Button>
</View>
```

**Why**: Consistent use of Zest components ensures uniform styling, interaction patterns, and accessibility across the app.

## Quick Reference

**Button**:
```typescript
<Button
  variant="primary" // primary/secondary/text
  size="lg" // sm/md/lg
  appearance="brand" // brand/neutral/critical
  onPress={handlePress}
  testID="button"
>
  Submit
</Button>
```

**Text**:
```typescript
<Text type="headline-md">{title}</Text> // headline-xl/lg/md, body-lg/md/sm-regular/bold
<Text type="body-md-regular" numberOfLines={2}>{content}</Text>
```

**Icon**:
```typescript
<Icon
  icon="HeartOutline24" // {Name}{Variant}{Size}
  altText="Favorite"
  color="alias.color.brand.foreground.default"
/>
```

**IconButton**:
```typescript
<IconButton
  icon="ShareOutline24"
  onPress={handleShare}
  size="md"
  testID="share-button"
/>
```

**InputField**:
```typescript
<InputField
  label="Email"
  value={email}
  onChangeText={setEmail}
  placeholder="Enter email"
  error={errorMessage}
  testID="email-input"
/>
```

**Card**:
```typescript
// Static
<Card>{content}</Card>

// Navigational
<Card variant="navigational" onPress={handleNavigate}>
  {content}
</Card>

// Selectable
<Card.Selectable onPress={handleSelect}>
  {content}
</Card.Selectable>
```

**Badge**:
```typescript
<Badge
  content="5"
  variant="positive"
  size="xs"
/>
```

**InlineMessage**:
```typescript
<InlineMessage
  variant="success" // success/error/warning/info
  message="Operation successful"
/>
```

**Tag/TagStatic/TagFilter**:
```typescript
// Interactive selection
<Tag label="Vegetarian" selected={isSelected} onPress={handleToggle} />

// Non-interactive label
<TagStatic label="New" variant="brand" />

// Filter chip
<TagFilter label="Gluten Free" onRemove={handleRemove} />
```

**Key Libraries:**
- @zest/react-native 1.5.3
- React Native 0.76+

**Available Components (42 total):**
Button, Text, Icon, IconButton, IconButtonToggle, Card, Badge, InputField, TextArea, InlineMessage, Divider, Tag, TagStatic, TagFilter, Spinner, Checkbox, Switch, Radio, Select, Modal, BottomSheet, Toast, Tooltip, Avatar, Chip, List, ListItem, Accordion, Tabs, ProgressBar, Skeleton, DatePicker, TimePicker, SearchInput, NumberInput, Slider, Rating, Stepper, Banner, Alert, Notification, EmptyState

For production examples, see [references/examples.md](references/examples.md).
