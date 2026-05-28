---
name: Accessibility Patterns
description: WCAG 2.2 Level AA compliance patterns for Flutter applications including Semantics widgets, screen reader support, keyboard navigation, and color contrast requirements
version: 1.0.0
---

# Accessibility Patterns for Flutter

Complete guide to building accessible Flutter applications that comply with WCAG 2.2 Level AA standards.

## WCAG 2.2 Level AA Requirements

### Perceivable
- **Text Alternatives**: Provide alt text for non-text content
- **Contrast**: 4.5:1 for normal text, 3:1 for large text
- **Resize Text**: Support 200% zoom
- **Non-text Contrast**: 3:1 for UI components

### Operable
- **Keyboard Accessible**: All functionality via keyboard
- **Focus Visible**: Clear focus indicators
- **Target Size**: Minimum 44x44 logical pixels
- **No Keyboard Trap**: Users can navigate away

### Understandable
- **Language**: Declare content language
- **Predictable**: Consistent navigation and identification
- **Input Assistance**: Labels, error identification, suggestions

### Robust
- **Compatible**: Works with assistive technologies
- **Status Messages**: Announce changes to screen readers

## Semantic Widgets

### Basic Semantics

```dart
// ❌ BAD - No semantic information
IconButton(
  icon: Icon(Icons.favorite),
  onPressed: () => likePage(),
)

// ✅ GOOD - Semantic label provided
Semantics(
  label: 'Like this page',
  hint: 'Double tap to like',
  button: true,
  enabled: true,
  child: IconButton(
    icon: Icon(Icons.favorite),
    onPressed: () => likePage(),
  ),
)

// ✅ GOOD - Using Tooltip provides semantic label
Tooltip(
  message: 'Like this page',
  child: IconButton(
    icon: Icon(Icons.favorite),
    onPressed: () => likePage(),
  ),
)
```

### Semantic Properties

```dart
Semantics(
  // Identification
  label: 'Submit button',           // What it is
  hint: 'Double tap to submit form', // How to use it
  value: 'Form is incomplete',       // Current state

  // Role
  button: true,
  header: false,
  image: false,
  link: false,
  textField: false,
  slider: false,

  // State
  enabled: isFormValid,
  checked: isChecked,
  selected: isSelected,
  toggled: isToggled,
  expanded: isExpanded,
  hidden: isHidden,

  // Actions
  onTap: () => submitForm(),
  onLongPress: () => showOptions(),
  onScrollUp: () => scrollUp(),
  onScrollDown: () => scrollDown(),
  onIncrease: () => increase(),
  onDecrease: () => decrease(),

  child: ElevatedButton(
    onPressed: isFormValid ? submitForm : null,
    child: Text('Submit'),
  ),
)
```

### Merging Semantics

```dart
// Combine multiple widgets into single semantic node
MergeSemantics(
  child: Row(
    children: [
      Icon(Icons.star, color: Colors.yellow),
      SizedBox(width: 4),
      Text('4.5'),
      SizedBox(width: 4),
      Text('(120 reviews)'),
    ],
  ),
)
// Screen reader announces: "4.5 star rating, 120 reviews"

// Exclude decorative elements
ExcludeSemantics(
  child: Container(
    decoration: BoxDecoration(
      border: Border.all(color: Colors.grey),
    ),
    child: Text('Content'),
  ),
)
```

## Screen Reader Support

### Text Fields with Labels

```dart
// ✅ GOOD - Implicit label from decoration
TextField(
  decoration: InputDecoration(
    labelText: 'Email',
    hintText: 'name@example.com',
  ),
)

// ✅ GOOD - Explicit semantic label
Semantics(
  label: 'Email address',
  hint: 'Enter your email address',
  textField: true,
  child: TextField(
    decoration: InputDecoration(
      border: OutlineInputBorder(),
    ),
  ),
)

// ✅ GOOD - Form field with validation
TextFormField(
  decoration: InputDecoration(
    labelText: 'Password',
    helperText: 'Must be at least 8 characters',
    errorText: hasError ? 'Password is too short' : null,
  ),
  obscureText: true,
  validator: (value) {
    if (value == null || value.length < 8) {
      return 'Password must be at least 8 characters';
    }
    return null;
  },
)
```

### Announce Status Changes

```dart
class FormController extends GetxController {
  final isSubmitting = false.obs;
  final submitSuccess = false.obs;

  Future<void> submitForm() async {
    isSubmitting.value = true;

    // Announce loading state
    SemanticsService.announce(
      'Submitting form',
      TextDirection.ltr,
    );

    final result = await repository.submit();

    result.fold(
      (failure) {
        SemanticsService.announce(
          'Error: ${failure.message}',
          TextDirection.ltr,
        );
      },
      (success) {
        submitSuccess.value = true;
        SemanticsService.announce(
          'Form submitted successfully',
          TextDirection.ltr,
        );
      },
    );

    isSubmitting.value = false;
  }
}
```

### Live Regions

```dart
// Announce dynamic content changes
Obx(() => Semantics(
  liveRegion: true,
  child: Text('${controller.itemCount} items in cart'),
))
```

## Touch Target Sizing

### Minimum Size Requirements

```dart
// ❌ BAD - Touch target too small
IconButton(
  iconSize: 16,
  icon: Icon(Icons.close),
  onPressed: () => close(),
)

// ✅ GOOD - Minimum 44x44 logical pixels
IconButton(
  iconSize: 24,
  padding: EdgeInsets.all(10), // Total: 24 + 20 = 44
  icon: Icon(Icons.close),
  onPressed: () => close(),
)

// ✅ GOOD - Wrap small widgets in larger touch target
GestureDetector(
  onTap: () => toggle(),
  child: Container(
    width: 44,
    height: 44,
    alignment: Alignment.center,
    child: Icon(Icons.check, size: 16),
  ),
)

// ✅ GOOD - Adequate spacing between targets
Row(
  spacing: 16, // Minimum 8px recommended
  children: [
    IconButton(icon: Icon(Icons.edit), onPressed: () => edit()),
    IconButton(icon: Icon(Icons.delete), onPressed: () => delete()),
  ],
)
```

## Color Contrast

### Text Contrast Requirements

```dart
// ✅ GOOD - High contrast text
Text(
  'Normal text',
  style: TextStyle(
    color: Color(0xFF212121), // #212121 on white = 16.1:1 ✓
    fontSize: 16,
  ),
)

Text(
  'Large text',
  style: TextStyle(
    color: Color(0xFF767676), // #767676 on white = 4.6:1 ✓
    fontSize: 24,
    fontWeight: FontWeight.bold,
  ),
)

// ❌ BAD - Insufficient contrast
Text(
  'Low contrast text',
  style: TextStyle(
    color: Color(0xFFCCCCCC), // #CCCCCC on white = 1.6:1 ✗
  ),
)
```

### UI Component Contrast

```dart
// ✅ GOOD - Focus indicators with sufficient contrast
OutlinedButton(
  style: OutlinedButton.styleFrom(
    side: BorderSide(
      color: Color(0xFF0066CC), // 3:1 contrast minimum
      width: 2,
    ),
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(8),
    ),
  ),
  onPressed: () {},
  child: Text('Button'),
)

// ✅ GOOD - Form borders
TextField(
  decoration: InputDecoration(
    border: OutlineInputBorder(
      borderSide: BorderSide(
        color: Color(0xFF757575), // 3:1 contrast
      ),
    ),
    focusedBorder: OutlineInputBorder(
      borderSide: BorderSide(
        color: Color(0xFF0066CC),
        width: 2,
      ),
    ),
  ),
)
```

## Focus Management

### Focus Visibility

```dart
// ✅ GOOD - Default focus ring
ElevatedButton(
  onPressed: () {},
  child: Text('Button'),
) // Flutter provides default focus indicator

// ✅ GOOD - Custom focus indicator
Focus(
  child: Builder(
    builder: (context) {
      final isFocused = Focus.of(context).hasFocus;
      return Container(
        decoration: BoxDecoration(
          border: isFocused
              ? Border.all(color: Colors.blue, width: 3)
              : null,
          borderRadius: BorderRadius.circular(8),
        ),
        child: ElevatedButton(
          onPressed: () {},
          child: Text('Button'),
        ),
      );
    },
  ),
)
```

### Focus Order

```dart
// ✅ GOOD - Explicit focus order with FocusTraversalGroup
FocusTraversalGroup(
  policy: OrderedTraversalPolicy(),
  child: Column(
    children: [
      FocusTraversalOrder(
        order: NumericFocusOrder(1.0),
        child: TextField(decoration: InputDecoration(labelText: 'First')),
      ),
      FocusTraversalOrder(
        order: NumericFocusOrder(2.0),
        child: TextField(decoration: InputDecoration(labelText: 'Second')),
      ),
      FocusTraversalOrder(
        order: NumericFocusOrder(3.0),
        child: ElevatedButton(
          onPressed: () {},
          child: Text('Submit'),
        ),
      ),
    ],
  ),
)
```

### Focus Trapping for Modals

```dart
class AccessibleDialog extends StatefulWidget {
  @override
  State<AccessibleDialog> createState() => _AccessibleDialogState();
}

class _AccessibleDialogState extends State<AccessibleDialog> {
  final FocusScopeNode _focusScopeNode = FocusScopeNode();

  @override
  void initState() {
    super.initState();
    // Focus first element when dialog opens
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _focusScopeNode.requestFocus();
    });
  }

  @override
  void dispose() {
    _focusScopeNode.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FocusScope(
      node: _focusScopeNode,
      child: AlertDialog(
        title: Text('Confirm Action'),
        content: Text('Are you sure?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('Cancel'),
          ),
          ElevatedButton(
            autofocus: true, // Focus first action
            onPressed: () {
              // Perform action
              Navigator.pop(context);
            },
            child: Text('Confirm'),
          ),
        ],
      ),
    );
  }
}
```

## Keyboard Navigation

### Standard Keyboard Shortcuts

```dart
class KeyboardNavigableWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Shortcuts(
      shortcuts: {
        LogicalKeySet(LogicalKeyboardKey.space): ActivateIntent(),
        LogicalKeySet(LogicalKeyboardKey.enter): ActivateIntent(),
        LogicalKeySet(LogicalKeyboardKey.escape): DismissIntent(),
      },
      child: Actions(
        actions: {
          ActivateIntent: CallbackAction<ActivateIntent>(
            onInvoke: (intent) => onActivate(),
          ),
          DismissIntent: CallbackAction<DismissIntent>(
            onInvoke: (intent) => onDismiss(),
          ),
        },
        child: Focus(
          autofocus: true,
          child: YourWidget(),
        ),
      ),
    );
  }
}
```

## Accessibility Testing

### Semantic Debugger

```dart
void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      showSemanticsDebugger: true, // Enable semantic tree overlay
      home: HomePage(),
    );
  }
}
```

### Automated Accessibility Tests

```dart
testWidgets('Button has semantic label', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        body: Semantics(
          label: 'Submit form',
          button: true,
          child: ElevatedButton(
            onPressed: () {},
            child: Text('Submit'),
          ),
        ),
      ),
    ),
  );

  // Verify semantic label
  expect(
    tester.getSemantics(find.byType(ElevatedButton)),
    matchesSemantics(
      label: 'Submit form',
      isButton: true,
    ),
  );
});

testWidgets('Touch target meets minimum size', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      home: IconButton(
        icon: Icon(Icons.close),
        onPressed: () {},
      ),
    ),
  );

  final size = tester.getSize(find.byType(IconButton));
  expect(size.width, greaterThanOrEqualTo(44));
  expect(size.height, greaterThanOrEqualTo(44));
});
```

## Best Practices Checklist

### Semantics
- [ ] All interactive widgets have semantic labels
- [ ] Decorative images are excluded from semantics
- [ ] Complex widgets use `MergeSemantics`
- [ ] Status changes are announced to screen readers
- [ ] Form errors are announced

### Touch Targets
- [ ] All interactive elements ≥ 44x44 logical pixels
- [ ] Adequate spacing between touch targets (≥ 8px)
- [ ] Small icons wrapped in larger touch areas

### Color and Contrast
- [ ] Text contrast ≥ 4.5:1 (normal), ≥ 3:1 (large)
- [ ] UI component contrast ≥ 3:1
- [ ] Don't rely on color alone for information
- [ ] Test with color blindness simulators

### Focus Management
- [ ] Clear focus indicators on all interactive elements
- [ ] Logical focus order (top to bottom, left to right)
- [ ] No keyboard traps
- [ ] Modals trap focus within dialog
- [ ] First element auto-focused when appropriate

### Keyboard Navigation
- [ ] All functionality accessible via keyboard
- [ ] Standard shortcuts (Enter, Space, Escape)
- [ ] Arrow keys for directional navigation
- [ ] Tab order matches visual order

### Testing
- [ ] Test with screen readers (TalkBack, VoiceOver)
- [ ] Test with semantic debugger enabled
- [ ] Write automated accessibility tests
- [ ] Test with keyboard only
- [ ] Test at 200% zoom

## Platform-Specific Considerations

### Android TalkBack

```dart
// Announce changes
SemanticsService.announce(
  'Item added to cart',
  TextDirection.ltr,
  assertiveness: Assertiveness.polite,
);
```

### iOS VoiceOver

```dart
// Same API works on iOS
SemanticsService.announce(
  'Item added to cart',
  TextDirection.ltr,
);
```

## Common Accessibility Anti-Patterns

### Anti-Pattern 1: Missing Semantic Labels

```dart
// ❌ BAD
IconButton(
  icon: Icon(Icons.favorite),
  onPressed: () => like(),
)

// ✅ GOOD
Tooltip(
  message: 'Like',
  child: IconButton(
    icon: Icon(Icons.favorite),
    onPressed: () => like(),
  ),
)
```

### Anti-Pattern 2: Insufficient Touch Targets

```dart
// ❌ BAD - 24x24 too small
Icon(Icons.close, size: 24)

// ✅ GOOD - Wrapped in 44x44 button
IconButton(
  icon: Icon(Icons.close),
  onPressed: () => close(),
)
```

### Anti-Pattern 3: Poor Color Contrast

```dart
// ❌ BAD - Gray on white (2:1)
Text('Low contrast', style: TextStyle(color: Color(0xFFAAAAAA)))

// ✅ GOOD - Dark gray on white (7:1)
Text('Good contrast', style: TextStyle(color: Color(0xFF555555)))
```

### Anti-Pattern 4: Not Announcing Changes

```dart
// ❌ BAD - Silent update
void addToCart(Product product) {
  cart.add(product);
  cartCount.value++;
}

// ✅ GOOD - Announce update
void addToCart(Product product) {
  cart.add(product);
  cartCount.value++;
  SemanticsService.announce(
    '${product.name} added to cart',
    TextDirection.ltr,
  );
}
```
