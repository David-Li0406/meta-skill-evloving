# Polaris Icons Migration Guide

This guide helps you migrate from older versions of Polaris Icons to the latest version.

## From @shopify/polaris-icons v8.x to v9.x

### Key Changes

1. **Renamed Icons**: Some icons have been renamed for clarity and consistency
2. **Removed Icons**: Deprecated icons have been removed
3. **New Icons**: New commerce and AI-related icons added

### Icon Renames

| Old Name (v8) | New Name (v9) |
|---------------|---------------|
| `MobileCancelMajor` | `XIcon` |
| `MobileChevronMajor` | `ChevronDownIcon` |
| `CirclePlusMajor` | `PlusCircleIcon` |
| `CircleMinusMajor` | `MinusCircleIcon` |
| `CircleCheckMajor` | `CheckCircleIcon` |
| `CircleAlertMajor` | `AlertCircleIcon` |
| `CircleCancelMajor` | `XCircleIcon` |
| `CircleInfoMajor` | `InfoIcon` |
| `CircleQuestionMajor` | `QuestionCircleIcon` |
| `DeleteMajor` | `DeleteIcon` |
| `EditMajor` | `EditIcon` |
| `AddMajor` | `PlusIcon` |
| `ViewMajor` | `EyeIcon` |
| `HideMajor` | `HideIcon` |
| `HomeMajor` | `HomeIcon` |
| `OrdersMajor` | `OrderIcon` |
| `ProductsMajor` | `ProductIcon` |
| `CustomersMajor` | `CustomerIcon` |
| `SettingsMajor` | `SettingsIcon` |
| `AnalyticsMajor` | `AnalyticsIcon` |
| `ContentMajor` | `FileIcon` |
| `ImageMajor` | `ImageIcon` |
| `PriceLookupMajor` | `PriceTagIcon` |
| `DiscountsMajor` | `DiscountIcon` |
| `GiftCardMajor` | `GiftCardIcon` |
| `TransferMajor` | `TransferIcon` |
| `InventoryMajor` | `InventoryIcon` |

### Migration Script

You can use this regex-based find-and-replace pattern to update imports:

```bash
# Example sed command for common renames
sed -i '' 's/CirclePlusMajor/PlusCircleIcon/g' **/*.tsx
sed -i '' 's/CircleMinusMajor/MinusCircleIcon/g' **/*.tsx
sed -i '' 's/CircleCheckMajor/CheckCircleIcon/g' **/*.tsx
sed -i '' 's/CircleAlertMajor/AlertCircleIcon/g' **/*.tsx
```

### Code Changes

#### Before (v8)
```jsx
import { CirclePlusMajor, DeleteMajor, HomeMajor } from '@shopify/polaris-icons';
import { Icon } from '@shopify/polaris';

<Icon source={CirclePlusMajor} color="success" />
<Icon source={DeleteMajor} color="critical" />
<Icon source={HomeMajor} color="base" />
```

#### After (v9)
```jsx
import { PlusCircleIcon, DeleteIcon, HomeIcon } from '@shopify/polaris-icons';
import { Icon } from '@shopify/polaris';

<Icon source={PlusCircleIcon} tone="success" />
<Icon source={DeleteIcon} tone="critical" />
<Icon source={HomeIcon} tone="base" />
```

### Breaking Changes

1. **`color` prop renamed to `tone`**: The Icon component now uses `tone` instead of `color`
   ```jsx
   // Before
   <Icon source={HomeIcon} color="success" />

   // After
   <Icon source={HomeIcon} tone="success" />
   ```

2. **Major/Minor suffix removed**: Icon names no longer have `Major` or `Minor` suffixes
   ```jsx
   // Before
   import { HomeMajor, HomeMinor } from '@shopify/polaris-icons';

   // After
   import { HomeIcon } from '@shopify/polaris-icons';
   ```

3. **Filled variants**: Some icons now have explicit `Filled` variants
   ```jsx
   import { StarIcon, StarFilledIcon } from '@shopify/polaris-icons';
   ```

## From Inline SVG to Polaris Icons

If you're migrating from custom inline SVGs to Polaris Icons:

### Before
```jsx
function MyComponent() {
  return (
    <svg viewBox="0 0 20 20" fill="currentColor">
      <path d="M10 2a8 8 0 100 16 8 8 0 000-16zm1 11H9v-2h2v2zm0-4H9V5h2v4z"/>
    </svg>
  );
}
```

### After
```jsx
import { Icon } from '@shopify/polaris';
import { InfoIcon } from '@shopify/polaris-icons';

function MyComponent() {
  return <Icon source={InfoIcon} />;
}
```

### Benefits of Migration

1. **Consistency**: All icons follow the same design language
2. **Accessibility**: Built-in accessibility support
3. **Maintainability**: Automatic updates with Polaris upgrades
4. **Theming**: Icons respond to theme changes automatically
5. **Bundle Size**: Tree-shakeable imports

## Troubleshooting

### Icon not found

If you get an error that an icon doesn't exist:

1. Check the [Icons Browser](https://polaris.shopify.com/icons) for the correct name
2. Icon names are case-sensitive and follow `PascalCaseIcon` format
3. Some icons may have been renamed - check this migration guide

### Icon not displaying

1. Ensure you're importing from `@shopify/polaris-icons`
2. Use the `Icon` component from `@shopify/polaris`, not a custom wrapper
3. Check that the `source` prop is receiving the icon function, not a string

```jsx
// Correct
import { HomeIcon } from '@shopify/polaris-icons';
<Icon source={HomeIcon} />

// Incorrect
<Icon source="HomeIcon" />
<Icon source={<HomeIcon />} />
```

### Wrong icon size

Polaris Icons are designed for a 20x20 viewport. Don't resize them manually:

```jsx
// Incorrect - avoid manual sizing
<Icon source={HomeIcon} style={{ width: 40, height: 40 }} />

// Correct - use the icon as-is or use a larger component
<Icon source={HomeIcon} />
```

If you need larger icons, consider using the icon in a larger button or container, or contact design about the use case.
