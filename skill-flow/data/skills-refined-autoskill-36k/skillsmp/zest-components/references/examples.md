# Zest Components - Production Examples

This document contains real production code examples from the YourCompany React Native codebase demonstrating Zest component usage patterns.

## Example 1: Button with Loading and Disabled States

**File**: `modules/store/components/floating-store-button/FloatingStoreButton.tsx:82`

This example shows Button with variant, appearance, loading, and disabled props for primary CTAs.

```typescript
import { Badge, Button, Icon, Text, useZestStyles } from '@zest/react-native';

const renderPrimaryCTA = () => (
  <Button
    style={styles.primaryCTA}
    fullWidth
    disabled={isCTADisabled || isExecutingPrimaryCTAOnPress}
    loading={isExecutingPrimaryCTAOnPress}
    onPress={handlePrimaryCTAPress}
    variant={isSkippedWeek ? 'primary' : screenConfig.ctaVariant}
    appearance={isSkippedWeek ? 'negative' : 'brand'}
    testID="primary-cta"
  >
    {ctaText}
  </Button>
);
```

**Key patterns demonstrated:**
- `variant` prop switches between 'primary' and other variants dynamically
- `appearance` prop switches between 'negative' (critical) and 'brand' (primary)
- `loading` prop shows spinner during async operations
- `disabled` prop prevents interaction when loading or invalid state
- `fullWidth` prop makes button span full container width
- `testID` for testing
- Conditional variant/appearance based on business logic (isSkippedWeek)

## Example 2: IconButton for Navigation Actions

**File**: `modules/store/screens/cart/components/header/Header.tsx:55`

This example shows IconButton with dynamic icon selection, altText for accessibility, and variant prop.

```typescript
import {
  IconButton,
  Text,
  useZestStyles,
  type IconsType24,
} from '@zest/react-native';

export const Header = () => {
  const styles = useZestStyles(stylesConfig);
  const navigation = useNavigation();
  const brandCategory = useBrandCategory();
  const { trackCartClose } = useCartAnalytics();

  const { buttonIcon, buttonId } = useMemo(() => {
    const isRTE = brandCategory === BrandCategory.RTE;
    return {
      buttonIcon: isRTE ? 'ChevronLeftOutline24' : 'CloseOutline24',
      buttonId: isRTE ? 'back-button' : 'close-button',
    };
  }, [brandCategory]);

  return (
    <View style={styles.container}>
      <View style={styles.innerContainer}>
        <IconButton
          icon={buttonIcon as IconsType24}
          altText="Close Cart"
          testID={buttonId}
          variant="tertiary"
          style={styles.backButton}
          onPress={() => {
            trackCartClose();
            navigation.goBack();
          }}
        />
        <View style={styles.titleContainer} testID="title">
          <SectionTitle title={title} badge={totalQuantity} />
          {cutoffDate && (
            <Text testID="cutoff-date">
              {translateRaw('cart.revamp.header.cutoff-date', {
                cutoffDate: formatDate(cutoffDate, DATE_FORMATS.SHORT),
              })}
            </Text>
          )}
        </View>
        <View style={styles.backButton} />
      </View>
    </View>
  );
};
```

**Key patterns demonstrated:**
- IconButton with dynamic icon based on brand category
- `variant="tertiary"` for subtle icon buttons in headers
- `altText` for accessibility (required for screen readers)
- `testID` with dynamic value based on icon type
- useMemo for icon selection logic to prevent recalculation
- Type casting `as IconsType24` for icon name type safety
- Icon names follow convention: ChevronLeftOutline24, CloseOutline24

## Example 3: Icon with Badge for Cart Counter

**File**: `modules/store/components/floating-store-button/FloatingStoreButton.tsx:110`

This example shows Icon with Badge overlay for cart item count.

```typescript
import { Badge, Icon } from '@zest/react-native';

const renderCartCTA = () => (
  <Pressable style={styles.cartCtaContainer} onPress={handleCartPress}>
    <View style={styles.cartIconContainer}>
      <Icon icon="CartOutline24" altText="Cart" />
      {totalItemsInCart > 0 && (
        <View style={styles.cartBadge}>
          <Badge
            content={String(totalItemsInCart)}
            size="xs"
            variant="positive"
          />
        </View>
      )}
    </View>
  </Pressable>
);
```

**Key patterns demonstrated:**
- Icon with altText ("Cart") for accessibility
- Badge with `content` prop showing numeric count
- Badge with `size="xs"` for small counter badges
- Badge with `variant="positive"` for success/confirmation color
- Conditional rendering (only show badge when count > 0)
- String conversion for numeric content (String(totalItemsInCart))
- Absolute positioning pattern (styles.cartBadge overlay)

## Example 4: Card.Selectable for Interactive Product Cards

**File**: `features/customization/components/product-card/ProductCard.tsx:204`

This example shows Card.Selectable with outlined variant, selected state, and dynamic styling.

```typescript
import { Card, Checkbox, useZestStyles } from '@zest/react-native';

export const ProductCard = (props: ProductCardProps) => {
  const {
    type,
    name,
    id,
    isSelected,
    image,
    price,
    orientation = 'VERTICAL',
    horizontalCardWidth,
  } = props;

  const styles = useZestStyles(
    stylesConfig({ orientation, horizontalCardWidth }),
    [orientation, horizontalCardWidth]
  );

  const handlePress = () => {
    if (type === 'CUSTOMIZATION') {
      trackCustomizationCarouselClick(id);
      if (shouldSaveAction) {
        onSwapCourse(selectedCustomization, id);
      } else {
        props.setSelectedCustomization(id);
      }
    }
  };

  if (type === 'CUSTOMIZATION') {
    return (
      <Card.Selectable
        variant={'outlined'}
        onPress={handlePress}
        disabled={isDisabled}
        selected={isSelected}
        style={[
          styles.container,
          styles.verticalCard,
          isRTECustomization && styles.verticalCardRTE,
        ]}
      >
        {isRTECustomization ? null : imageComponent}
        {innerContainer}
      </Card.Selectable>
    );
  }
};
```

**Key patterns demonstrated:**
- Card.Selectable for cards with selection state
- `variant="outlined"` for outlined card style
- `selected` prop controls visual selection state
- `disabled` prop prevents interaction when isDisabled
- `onPress` handler for card selection
- Style array with conditional styles (isRTECustomization condition)
- useZestStyles with dependencies array [orientation, horizontalCardWidth]
- Dynamic stylesConfig based on props (orientation, horizontalCardWidth)

## Example 5: Card.Selectable with IconButton

**File**: `modules/social-recipe-bridge/screens/social-recipe-bridge/components/recipe-card/RecipeCard.tsx:53`

This example shows Card.Selectable with nested IconButton for delete action.

```typescript
import { Icon, IconButton, Text, useZestStyles } from '@zest/react-native';
import { Card } from '@zest/react-native';

const RecipeImage = ({ imageUrl, onDelete, recipe }) => {
  const handleDelete = () => {
    onDelete?.(recipe);
  };

  return (
    <View style={styles.imageContainer}>
      {imageUrl ? (
        <Image source={{ uri: imageUrl }} style={styles.imageStyle} />
      ) : (
        <View style={styles.imagePlaceholder}>
          <Icon icon="ImageOutline24" altText="" />
        </View>
      )}
      {onDelete && (
        <IconButton
          icon="BookmarkFilled16"
          appearance="neutral"
          shape="square"
          onPress={handleDelete}
          accessibilityHint="Remove from saved recipes"
          accessibilityLabel="Remove recipe"
          altText="Remove recipe"
          size="sm"
        />
      )}
    </View>
  );
};

const RecipeTitle = ({ title }) => (
  <Text type="body-md-bold" numberOfLines={2}>
    {title}
  </Text>
);

export const RecipeCard = ({ recipe, onPress, onDelete }) => {
  const handlePress = () => {
    onPress?.(recipe);
  };

  return (
    <Card.Selectable
      style={styles.container}
      padding="none"
      variant="transparent"
      onPress={handlePress}
      accessibilityLabel="Recipe card"
      accessibilityHint="Tap to open recipe"
    >
      <RecipeImage
        imageUrl={recipe.thumbnail_url}
        onDelete={onDelete}
        recipe={recipe}
      />
      <RecipeContent title={recipe.title} />
    </Card.Selectable>
  );
};
```

**Key patterns demonstrated:**
- Card.Selectable with `padding="none"` for custom internal layout
- Card.Selectable with `variant="transparent"` for no background
- IconButton with `size="sm"` for small action buttons
- IconButton with `shape="square"` instead of default circle
- IconButton with `appearance="neutral"` for neutral color
- Icon with empty altText (`altText=""`) for decorative images
- Text with `type="body-md-bold"` for emphasized text
- Text with `numberOfLines={2}` to truncate long titles
- accessibilityLabel and accessibilityHint for screen readers
- Conditional IconButton rendering (only show if onDelete exists)
- Optional chaining for callbacks (onPress?.(recipe), onDelete?.(recipe))

## Example 6: InputField with Form Validation

**File**: `modules/test-playground/screens/sign-in/components/authentication-form/AuthenticationForm.tsx:66`

This example shows InputField with refs, validation, and controlled state.

```typescript
import { Button, InputField, Text, useZestStyles } from '@zest/react-native';
import type { InputFieldRef, StylesConfig } from '@zest/react-native';

export const AuthenticationForm = () => {
  const styles = useZestStyles(stylesConfig);
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');

  const usernameInputRef = useRef<InputFieldRef>(null);
  const passwordInputRef = useRef<InputFieldRef>(null);

  const signIn = () => {
    mutation.mutate({ email: username, password });
  };

  return (
    <View style={styles.container}>
      <Text type="body-lg-bold">{content?.title.text}</Text>

      <InputField
        label="Username"
        testID="username-input"
        value={username}
        ref={usernameInputRef}
        placeholder="Enter Email"
        onChangeText={setUsername}
        autoCapitalize="none"
      />

      <InputField
        label="Password"
        testID="password-input"
        value={password}
        ref={passwordInputRef}
        secureTextEntry
        placeholder="Enter Password"
        onChangeText={setPassword}
      />

      {mutation.isError && (
        <Text style={styles.errorText} testID="error-text">
          {mutation.error?.message}
        </Text>
      )}

      <Button
        testID="signin-button"
        disabled={mutation.isPending}
        onPress={signIn}
      >
        Sign In
      </Button>
    </View>
  );
};

const stylesConfig: StylesConfig = {
  container: {
    flex: 1,
    width: '100%',
    gap: 'global.spacing.sm1',
    paddingHorizontal: 'global.spacing.sm2',
  },
  errorText: {
    color: 'alias.color.negative.foreground.default'
  },
};
```

**Key patterns demonstrated:**
- InputField with `label` prop for form labels
- InputField with `value` and `onChangeText` for controlled state
- InputField with `ref` prop typed as InputFieldRef
- InputField with `placeholder` for hint text
- InputField with `secureTextEntry` for password masking
- InputField with `autoCapitalize="none"` for email inputs
- InputField with `testID` for testing
- Button with `disabled={mutation.isPending}` during async operations
- Text with error styling using theme token
- StylesConfig with token strings for spacing and colors
- useRef<InputFieldRef> type for input refs
- Conditional error message rendering (mutation.isError)

## Example 7: Text with Typography Types

**File**: `modules/social-recipe-bridge/screens/social-recipe-bridge/components/recipe-card/RecipeCard.tsx:77`

This example shows Text component with different typography types and truncation.

```typescript
import { Text } from '@zest/react-native';

const RecipeContent = ({ title, subtitle, description }) => (
  <View style={styles.contentContainer}>
    <Text type="headline-md" numberOfLines={1} ellipsizeMode="tail">
      {title}
    </Text>

    <Text type="body-lg-regular" numberOfLines={2}>
      {subtitle}
    </Text>

    <Text type="body-md-regular" numberOfLines={3} style={styles.description}>
      {description}
    </Text>

    <Text type="body-sm-bold" style={styles.label}>
      {label}
    </Text>
  </View>
);
```

**Key patterns demonstrated:**
- Text with `type="headline-md"` for section titles
- Text with `type="body-lg-regular"` for primary content
- Text with `type="body-md-regular"` for secondary content
- Text with `type="body-sm-bold"` for labels and emphasis
- Text with `numberOfLines` prop to limit lines
- Text with `ellipsizeMode="tail"` to truncate with "..." at end
- Text with additional style prop for custom styling
- Multiple Text components with different typography types

## Summary

The YourCompany codebase consistently follows these Zest component patterns:

1. **Button** - variant (primary/secondary/text), appearance (brand/neutral/critical/negative), loading, disabled, fullWidth, testID
2. **IconButton** - icon name with size suffix (24/16), altText required, variant (tertiary for subtle), size (sm/md), shape (circle/square), appearance
3. **Icon** - icon naming convention {Name}{Variant}{Size}, altText required (empty string for decorative)
4. **Badge** - content as string, size (xs for counters), variant (positive/neutral/brand/critical), positioned absolutely over icons
5. **Card.Selectable** - variant (outlined/transparent), selected state, disabled state, padding (none for custom layout), onPress handler
6. **InputField** - label, value/onChangeText (controlled), ref typed as InputFieldRef, placeholder, secureTextEntry for passwords, autoCapitalize, testID
7. **Text** - type for typography (headline-xl/lg/md, body-lg/md/sm-regular/bold), numberOfLines for truncation, ellipsizeMode
8. **useZestStyles** - with stylesConfig and dependencies array for dynamic styles
9. **Accessibility** - testID on all interactive components, altText on all icons, accessibilityLabel/accessibilityHint for context
10. **Conditional Rendering** - components shown/hidden based on state, optional chaining for callbacks (onPress?.(data))

These patterns ensure consistent component usage, built-in accessibility, automatic theme support, and reliable testing throughout the app.
