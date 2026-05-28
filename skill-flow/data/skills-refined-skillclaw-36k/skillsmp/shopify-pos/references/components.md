# POS UI Components

Complete reference for all available POS UI components.

## Import Pattern

```tsx
import {
  Screen, Navigator, Button, Text, Section,
  // ... other components
} from '@shopify/ui-extensions-react/point-of-sale';
```

## Layout & Structure

### Screen

Navigation screen container with title, loading state, and actions.

```tsx
<Screen
  name="Main"                    // Required: unique screen identifier
  title="My Screen"              // Screen title in navigation bar
  isLoading={false}              // Show loading indicator
  presentation="modal"           // 'modal' | 'card' | 'fullScreen'
  onNavigateBack={() => {}}      // Back button handler
  primaryAction={{               // Primary action button
    title: 'Save',
    onPress: handleSave,
    disabled: false
  }}
  secondaryAction={{             // Secondary action button
    title: 'Cancel',
    onPress: handleCancel
  }}
>
  {/* Screen content */}
</Screen>
```

### Navigator

Container for screen navigation stack.

```tsx
<Navigator initialScreen="Home">
  <Screen name="Home" title="Home">
    <Button title="Go to Details" onPress={() => navigation.navigate('Details')} />
  </Screen>
  <Screen name="Details" title="Details">
    <Text>Detail content</Text>
  </Screen>
</Navigator>
```

### ScrollView

Scrollable content container.

```tsx
<ScrollView>
  {/* Long content that may overflow */}
</ScrollView>
```

### Section

Card-like container with optional title.

```tsx
<Section title="Customer Info">
  <Text>Name: John Doe</Text>
  <Text>Email: john@example.com</Text>
</Section>
```

### Stack

Flex container for horizontal or vertical layouts.

```tsx
<Stack direction="horizontal" spacing={2} alignment="center">
  <Icon name="customer" />
  <Text>Customer Name</Text>
</Stack>

<Stack direction="vertical" spacing={4}>
  <Button title="Option 1" />
  <Button title="Option 2" />
</Stack>
```

**Props**:
- `direction`: `'horizontal'` | `'vertical'`
- `spacing`: number (spacing units)
- `alignment`: `'start'` | `'center'` | `'end'`

### List

Structured data rows with rich content.

```tsx
<List
  data={items}
  renderItem={(item) => (
    <List.Item
      title={item.name}
      subtitle={item.description}
      leftSide={{ image: { source: item.imageUrl } }}
      rightSide={{ label: item.price }}
      onPress={() => handleSelect(item)}
    />
  )}
/>
```

### Box

Generic container with styling props.

```tsx
<Box padding={4} background="surface">
  <Text>Boxed content</Text>
</Box>
```

### SectionHeader

Header for grouping content sections.

```tsx
<SectionHeader title="Recent Orders" />
```

### Spacing

Add vertical spacing between elements.

```tsx
<Spacing height={4} />
```

## Actions

### Button

Tappable action button.

```tsx
<Button
  title="Add to Cart"
  type="primary"              // 'primary' | 'basic' | 'destructive'
  onPress={handlePress}
  disabled={false}
  loading={false}
/>
```

### Tile

Smart grid tile (only for `pos.home.tile.render`).

```tsx
<Tile
  title="Loyalty"
  subtitle="Check points"
  enabled={true}
  badge={{ text: '5', status: 'warning' }}
/>
```

**Props**:
- `title`: string (required)
- `subtitle`: string
- `enabled`: boolean
- `badge`: `{ text: string, status: 'info' | 'success' | 'warning' | 'critical' }`

### Selectable

Make any component tappable.

```tsx
<Selectable onPress={handlePress}>
  <Section>
    <Text>Tap this section</Text>
  </Section>
</Selectable>
```

## Forms

### TextField

Single-line text input.

```tsx
<TextField
  label="Name"
  value={name}
  onChange={setName}
  placeholder="Enter name"
  disabled={false}
  error="Name is required"      // Error message
/>
```

### TextArea

Multi-line text input.

```tsx
<TextArea
  label="Notes"
  value={notes}
  onChange={setNotes}
  placeholder="Add notes..."
  rows={4}
/>
```

### NumberField

Numeric input with validation.

```tsx
<NumberField
  label="Quantity"
  value={quantity}
  onChange={setQuantity}
  min={1}
  max={100}
/>
```

### EmailField

Email input with built-in validation.

```tsx
<EmailField
  label="Email"
  value={email}
  onChange={setEmail}
  error={emailError}
/>
```

### DateField / DatePicker

Date selection components.

```tsx
<DateField
  label="Date of Birth"
  value={date}
  onChange={setDate}
/>

<DatePicker
  selected={selectedDate}
  onSelect={setSelectedDate}
  minDate={new Date()}
/>
```

### TimeField / TimePicker

Time selection components.

```tsx
<TimeField
  label="Appointment Time"
  value={time}
  onChange={setTime}
/>
```

### RadioButtonList

Single selection from list.

```tsx
<RadioButtonList
  items={[
    { id: 'small', label: 'Small' },
    { id: 'medium', label: 'Medium' },
    { id: 'large', label: 'Large' }
  ]}
  selected={selectedSize}
  onSelect={setSelectedSize}
/>
```

### Stepper

Increment/decrement numeric control.

```tsx
<Stepper
  label="Quantity"
  value={quantity}
  onChange={setQuantity}
  min={1}
  max={10}
/>
```

### PinPad

Secure PIN entry.

```tsx
<PinPad
  title="Enter PIN"
  onSubmit={handlePinSubmit}
  maxLength={4}
/>
```

## Feedback & Status

### Banner

Highlight important information.

```tsx
<Banner
  status="info"               // 'info' | 'success' | 'warning' | 'critical'
  title="Low Stock"
  message="Only 3 items remaining"
  action={{
    label: 'Reorder',
    onPress: handleReorder
  }}
/>
```

### Dialog

Confirmation modal requiring user response.

```tsx
const { dialog } = useApi<'pos.home.modal.render'>();

// Show dialog
const result = await dialog.show({
  title: 'Confirm Action',
  message: 'Are you sure you want to proceed?',
  primaryAction: { label: 'Confirm' },
  secondaryAction: { label: 'Cancel' }
});

if (result.primaryActionPressed) {
  // User confirmed
}
```

### Badge

Status indicator tag.

```tsx
<Badge status="success">Paid</Badge>
<Badge status="warning">Pending</Badge>
<Badge status="critical">Overdue</Badge>
```

## Text

### Text

Display text with various styles.

```tsx
<Text>Regular text</Text>
<Text variant="headingLarge">Large Heading</Text>
<Text variant="headingSmall">Small Heading</Text>
<Text variant="body">Body text</Text>
<Text variant="caption">Caption text</Text>
<Text color="subdued">Subdued text</Text>
<Text color="critical">Error text</Text>
```

**Variants**: `'headingLarge'` | `'headingSmall'` | `'body'` | `'caption'`

**Colors**: `'default'` | `'subdued'` | `'success'` | `'warning'` | `'critical'`

## Media

### Icon

Display icons from POS catalog.

```tsx
<Icon name="cart" size="large" />
<Icon name="customer" />
<Icon name="search" />
<Icon name="checkmark" />
```

**Common icons**: `cart`, `customer`, `product`, `search`, `settings`, `checkmark`, `close`, `plus`, `minus`, `edit`, `delete`, `print`, `scan`

### Image

Display images.

```tsx
<Image
  source={{ uri: 'https://example.com/image.jpg' }}
  width={100}
  height={100}
  resizeMode="cover"          // 'cover' | 'contain' | 'stretch'
/>
```

### CameraScanner

Barcode/QR code scanner.

```tsx
<CameraScanner
  onScan={(result) => handleScan(result.data)}
  bannerMessage="Scan product barcode"
/>
```

### QRCode (Beta)

Display QR codes.

```tsx
<QRCode
  value="https://example.com/receipt/123"
  size={200}
/>
```

**Requirements**: POS UI extensions 2025-04+, invite-only preview

## Navigation

### SearchBar

Search input with suggestions.

```tsx
<SearchBar
  placeholder="Search products..."
  value={query}
  onChange={setQuery}
  onSubmit={handleSearch}
/>
```

### SegmentedControl

Tab-like selection control.

```tsx
<SegmentedControl
  segments={[
    { id: 'all', label: 'All' },
    { id: 'active', label: 'Active' },
    { id: 'archived', label: 'Archived' }
  ]}
  selected={selectedSegment}
  onSelect={setSelectedSegment}
/>
```

## Receipt Components (Beta)

### POSReceiptBlock

Container for receipt content.

```tsx
<POSReceiptBlock>
  <Text>Thank you for shopping with us!</Text>
  <QRCode value="https://feedback.example.com" size={80} />
</POSReceiptBlock>
```

### PrintPreview

Preview printable documents.

```tsx
<PrintPreview
  content={receiptContent}
  onPrint={handlePrint}
/>
```

## Component Availability by Target

Not all components are available in all targets due to interface constraints.

| Component | Tile | Modal | Block | Menu Item |
|-----------|------|-------|-------|-----------|
| Tile | ✓ | - | - | - |
| Screen | - | ✓ | - | - |
| Navigator | - | ✓ | - | - |
| Button | - | ✓ | ✓ | ✓ |
| Text | ✓ | ✓ | ✓ | ✓ |
| Section | - | ✓ | ✓ | - |
| List | - | ✓ | ✓ | - |
| Form inputs | - | ✓ | - | - |
| Banner | - | ✓ | ✓ | - |
| CameraScanner | - | ✓ | - | - |
