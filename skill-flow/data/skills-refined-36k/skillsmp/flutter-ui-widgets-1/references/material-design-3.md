# Material Design 3 in Flutter

A comprehensive guide to Material Design 3 (M3) in Flutter, covering components, theming, color systems, typography, and migration strategies. Material 3 is Flutter's default design language as of Flutter 3.16.

## Overview

Material Design 3 is Google's open-source design system that enables personal, adaptive, and expressive experiences. It builds on Material Design's foundation with enhanced features including dynamic color, improved accessibility, and refined components.

### Key Features

- **Dynamic Color** - Generate custom color schemes from seed colors or images
- **Enhanced Accessibility** - Improved contrast ratios and touch target sizes
- **Design Tokens** - Systematic design values for consistency
- **Expressive Components** - More customization options and visual refinement
- **Large Screen Support** - Foundations for responsive tablet and desktop layouts
- **Personal and Adaptive** - Adapt to user preferences and contexts

### Default Status

Since Flutter 3.16, Material 3 is **enabled by default**. You can opt out by setting `useMaterial3: false` in your `ThemeData`, but this property will eventually be deprecated as Material 2 is phased out.

```dart
MaterialApp(
  theme: ThemeData(
    colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
    useMaterial3: true, // This is now the default
  ),
  home: MyHomePage(),
)
```

## Color System

Material 3 introduces a sophisticated color system based on tonal palettes and roles.

### Color Roles

Instead of defining colors directly, M3 uses semantic color roles:

- **Primary** - Main brand color, used for prominent UI elements
- **Secondary** - Accent color for less prominent elements
- **Tertiary** - Contrasting accent for highlights and variety
- **Error** - Error states and destructive actions
- **Surface** - Background colors for cards, sheets, menus
- **Background** - App background color
- **Outline** - Borders and dividers

Each role has variants: `onPrimary`, `primaryContainer`, `onPrimaryContainer`, etc.

### Creating Color Schemes

```dart
import 'package:flutter/material.dart';

// From seed color (recommended)
final lightColorScheme = ColorScheme.fromSeed(
  seedColor: Colors.blue,
  brightness: Brightness.light,
);

final darkColorScheme = ColorScheme.fromSeed(
  seedColor: Colors.blue,
  brightness: Brightness.dark,
);

// Custom color scheme
final customColorScheme = ColorScheme(
  brightness: Brightness.light,
  primary: Color(0xFF6750A4),
  onPrimary: Color(0xFFFFFFFF),
  primaryContainer: Color(0xFFEADDFF),
  onPrimaryContainer: Color(0xFF21005D),
  secondary: Color(0xFF625B71),
  onSecondary: Color(0xFFFFFFFF),
  secondaryContainer: Color(0xFFE8DEF8),
  onSecondaryContainer: Color(0xFF1D192B),
  tertiary: Color(0xFF7D5260),
  onTertiary: Color(0xFFFFFFFF),
  tertiaryContainer: Color(0xFFFFD8E4),
  onTertiaryContainer: Color(0xFF31111D),
  error: Color(0xFFB3261E),
  onError: Color(0xFFFFFFFF),
  errorContainer: Color(0xFFF9DEDC),
  onErrorContainer: Color(0xFF410E0B),
  background: Color(0xFFFFFBFE),
  onBackground: Color(0xFF1C1B1F),
  surface: Color(0xFFFFFBFE),
  onSurface: Color(0xFF1C1B1F),
  surfaceVariant: Color(0xFFE7E0EC),
  onSurfaceVariant: Color(0xFF49454F),
  outline: Color(0xFF79747E),
  outlineVariant: Color(0xFFCAC4D0),
  shadow: Color(0xFF000000),
  scrim: Color(0xFF000000),
  inverseSurface: Color(0xFF313033),
  onInverseSurface: Color(0xFFF4EFF4),
  inversePrimary: Color(0xFFD0BCFF),
  surfaceTint: Color(0xFF6750A4),
);
```

### Using Color Scheme in Theme

```dart
MaterialApp(
  theme: ThemeData(
    colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
    useMaterial3: true,
  ),
  darkTheme: ThemeData(
    colorScheme: ColorScheme.fromSeed(
      seedColor: Colors.deepPurple,
      brightness: Brightness.dark,
    ),
    useMaterial3: true,
  ),
  themeMode: ThemeMode.system,
  home: MyHomePage(),
)
```

### Accessing Colors in Widgets

```dart
Widget build(BuildContext context) {
  final colorScheme = Theme.of(context).colorScheme;

  return Container(
    color: colorScheme.primaryContainer,
    child: Text(
      'Themed text',
      style: TextStyle(color: colorScheme.onPrimaryContainer),
    ),
  );
}
```

## Typography

Material 3 provides a comprehensive type scale with five categories.

### Type Scale Roles

- **Display** - Large, high-impact text (display-large, display-medium, display-small)
- **Headline** - High-emphasis section headers (headline-large, headline-medium, headline-small)
- **Title** - Medium-emphasis text (title-large, title-medium, title-small)
- **Body** - Default text (body-large, body-medium, body-small)
- **Label** - Smaller utility text (label-large, label-medium, label-small)

### Default Type Scales

```dart
// Display styles
TextStyle displayLarge;   // 57px, light weight
TextStyle displayMedium;  // 45px, regular weight
TextStyle displaySmall;   // 36px, regular weight

// Headline styles
TextStyle headlineLarge;  // 32px, regular weight
TextStyle headlineMedium; // 28px, regular weight
TextStyle headlineSmall;  // 24px, regular weight

// Title styles
TextStyle titleLarge;     // 22px, medium weight
TextStyle titleMedium;    // 16px, medium weight
TextStyle titleSmall;     // 14px, medium weight

// Body styles
TextStyle bodyLarge;      // 16px, regular weight
TextStyle bodyMedium;     // 14px, regular weight
TextStyle bodySmall;      // 12px, regular weight

// Label styles
TextStyle labelLarge;     // 14px, medium weight
TextStyle labelMedium;    // 12px, medium weight
TextStyle labelSmall;     // 11px, medium weight
```

### Using Text Styles

```dart
Widget build(BuildContext context) {
  final textTheme = Theme.of(context).textTheme;

  return Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      Text('Display Large', style: textTheme.displayLarge),
      Text('Headline Medium', style: textTheme.headlineMedium),
      Text('Title Large', style: textTheme.titleLarge),
      Text('Body Medium', style: textTheme.bodyMedium),
      Text('Label Small', style: textTheme.labelSmall),
    ],
  );
}
```

### Custom Typography

```dart
MaterialApp(
  theme: ThemeData(
    colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
    textTheme: TextTheme(
      displayLarge: TextStyle(
        fontSize: 57,
        fontWeight: FontWeight.w400,
        fontFamily: 'CustomFont',
      ),
      bodyMedium: TextStyle(
        fontSize: 14,
        fontWeight: FontWeight.w400,
        letterSpacing: 0.25,
      ),
    ),
    useMaterial3: true,
  ),
)
```

## Material 3 Components

### Buttons

Material 3 provides five button types with distinct visual hierarchies.

```dart
import 'package:flutter/material.dart';

class ButtonShowcase extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        // Filled Button - Highest emphasis
        FilledButton(
          onPressed: () {},
          child: Text('Filled Button'),
        ),
        SizedBox(height: 8),

        // Filled Tonal Button - Medium emphasis
        FilledButton.tonal(
          onPressed: () {},
          child: Text('Filled Tonal'),
        ),
        SizedBox(height: 8),

        // Elevated Button - Medium emphasis with elevation
        ElevatedButton(
          onPressed: () {},
          child: Text('Elevated Button'),
        ),
        SizedBox(height: 8),

        // Outlined Button - Medium emphasis with border
        OutlinedButton(
          onPressed: () {},
          child: Text('Outlined Button'),
        ),
        SizedBox(height: 8),

        // Text Button - Lowest emphasis
        TextButton(
          onPressed: () {},
          child: Text('Text Button'),
        ),
        SizedBox(height: 16),

        // Buttons with icons
        FilledButton.icon(
          onPressed: () {},
          icon: Icon(Icons.add),
          label: Text('Add Item'),
        ),
        SizedBox(height: 8),

        // Icon Button
        IconButton(
          onPressed: () {},
          icon: Icon(Icons.favorite),
        ),
        SizedBox(height: 8),

        // Filled Icon Button
        IconButton.filled(
          onPressed: () {},
          icon: Icon(Icons.favorite),
        ),
        SizedBox(height: 8),

        // Filled Tonal Icon Button
        IconButton.filledTonal(
          onPressed: () {},
          icon: Icon(Icons.favorite),
        ),
        SizedBox(height: 8),

        // Outlined Icon Button
        IconButton.outlined(
          onPressed: () {},
          icon: Icon(Icons.favorite),
        ),
      ],
    );
  }
}
```

### Cards

Material 3 cards have refined elevation and shapes.

```dart
// Elevated Card
Card(
  elevation: 1,
  child: Padding(
    padding: EdgeInsets.all(16),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Card Title', style: Theme.of(context).textTheme.titleLarge),
        SizedBox(height: 8),
        Text('Card content goes here'),
      ],
    ),
  ),
)

// Filled Card
Card(
  elevation: 0,
  color: Theme.of(context).colorScheme.surfaceVariant,
  child: Padding(
    padding: EdgeInsets.all(16),
    child: Text('Filled Card'),
  ),
)

// Outlined Card
Card(
  elevation: 0,
  shape: RoundedRectangleBorder(
    side: BorderSide(
      color: Theme.of(context).colorScheme.outline,
    ),
    borderRadius: BorderRadius.circular(12),
  ),
  child: Padding(
    padding: EdgeInsets.all(16),
    child: Text('Outlined Card'),
  ),
)
```

### FloatingActionButton

```dart
// Regular FAB
FloatingActionButton(
  onPressed: () {},
  child: Icon(Icons.add),
)

// Small FAB
FloatingActionButton.small(
  onPressed: () {},
  child: Icon(Icons.add),
)

// Large FAB
FloatingActionButton.large(
  onPressed: () {},
  child: Icon(Icons.add),
)

// Extended FAB
FloatingActionButton.extended(
  onPressed: () {},
  icon: Icon(Icons.add),
  label: Text('Create'),
)
```

### Navigation

#### NavigationBar (Bottom Navigation)

```dart
class NavigationExample extends StatefulWidget {
  @override
  State<NavigationExample> createState() => _NavigationExampleState();
}

class _NavigationExampleState extends State<NavigationExample> {
  int _selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _pages[_selectedIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _selectedIndex,
        onDestinationSelected: (index) {
          setState(() {
            _selectedIndex = index;
          });
        },
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.home_outlined),
            selectedIcon: Icon(Icons.home),
            label: 'Home',
          ),
          NavigationDestination(
            icon: Icon(Icons.search_outlined),
            selectedIcon: Icon(Icons.search),
            label: 'Search',
          ),
          NavigationDestination(
            icon: Icon(Icons.person_outline),
            selectedIcon: Icon(Icons.person),
            label: 'Profile',
          ),
        ],
      ),
    );
  }

  final List<Widget> _pages = [
    Center(child: Text('Home')),
    Center(child: Text('Search')),
    Center(child: Text('Profile')),
  ];
}
```

#### NavigationRail (Side Navigation)

```dart
class NavigationRailExample extends StatefulWidget {
  @override
  State<NavigationRailExample> createState() => _NavigationRailExampleState();
}

class _NavigationRailExampleState extends State<NavigationRailExample> {
  int _selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          NavigationRail(
            selectedIndex: _selectedIndex,
            onDestinationSelected: (index) {
              setState(() {
                _selectedIndex = index;
              });
            },
            labelType: NavigationRailLabelType.all,
            destinations: const [
              NavigationRailDestination(
                icon: Icon(Icons.home_outlined),
                selectedIcon: Icon(Icons.home),
                label: Text('Home'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.search_outlined),
                selectedIcon: Icon(Icons.search),
                label: Text('Search'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.settings_outlined),
                selectedIcon: Icon(Icons.settings),
                label: Text('Settings'),
              ),
            ],
          ),
          VerticalDivider(thickness: 1, width: 1),
          Expanded(
            child: _pages[_selectedIndex],
          ),
        ],
      ),
    );
  }

  final List<Widget> _pages = [
    Center(child: Text('Home')),
    Center(child: Text('Search')),
    Center(child: Text('Settings')),
  ];
}
```

#### NavigationDrawer

```dart
Scaffold(
  appBar: AppBar(title: Text('App')),
  drawer: NavigationDrawer(
    selectedIndex: _selectedIndex,
    onDestinationSelected: (index) {
      setState(() {
        _selectedIndex = index;
      });
      Navigator.pop(context);
    },
    children: [
      Padding(
        padding: EdgeInsets.fromLTRB(28, 16, 16, 10),
        child: Text(
          'Menu',
          style: Theme.of(context).textTheme.titleSmall,
        ),
      ),
      NavigationDrawerDestination(
        icon: Icon(Icons.home_outlined),
        selectedIcon: Icon(Icons.home),
        label: Text('Home'),
      ),
      NavigationDrawerDestination(
        icon: Icon(Icons.search_outlined),
        selectedIcon: Icon(Icons.search),
        label: Text('Search'),
      ),
      Divider(),
      Padding(
        padding: EdgeInsets.fromLTRB(28, 16, 16, 10),
        child: Text(
          'Settings',
          style: Theme.of(context).textTheme.titleSmall,
        ),
      ),
      NavigationDrawerDestination(
        icon: Icon(Icons.settings_outlined),
        selectedIcon: Icon(Icons.settings),
        label: Text('Settings'),
      ),
    ],
  ),
  body: _pages[_selectedIndex],
)
```

### Dialogs

```dart
// Alert Dialog
showDialog(
  context: context,
  builder: (context) => AlertDialog(
    icon: Icon(Icons.warning_amber_rounded),
    title: Text('Alert Title'),
    content: Text('This is an alert dialog with Material 3 styling.'),
    actions: [
      TextButton(
        onPressed: () => Navigator.pop(context),
        child: Text('Cancel'),
      ),
      FilledButton(
        onPressed: () {
          Navigator.pop(context);
        },
        child: Text('OK'),
      ),
    ],
  ),
);

// Full-screen Dialog
Navigator.push(
  context,
  MaterialPageRoute(
    fullscreenDialog: true,
    builder: (context) => Scaffold(
      appBar: AppBar(
        title: Text('Full Screen Dialog'),
        leading: IconButton(
          icon: Icon(Icons.close),
          onPressed: () => Navigator.pop(context),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('Save'),
          ),
        ],
      ),
      body: Center(child: Text('Dialog content')),
    ),
  ),
);
```

### Bottom Sheets

```dart
// Modal Bottom Sheet
showModalBottomSheet(
  context: context,
  builder: (context) => Container(
    padding: EdgeInsets.all(16),
    child: Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        ListTile(
          leading: Icon(Icons.share),
          title: Text('Share'),
          onTap: () {
            Navigator.pop(context);
          },
        ),
        ListTile(
          leading: Icon(Icons.link),
          title: Text('Get link'),
          onTap: () {
            Navigator.pop(context);
          },
        ),
        ListTile(
          leading: Icon(Icons.edit),
          title: Text('Edit'),
          onTap: () {
            Navigator.pop(context);
          },
        ),
      ],
    ),
  ),
);
```

### Chips

```dart
// Input Chip
InputChip(
  label: Text('Input Chip'),
  onPressed: () {},
  onDeleted: () {},
)

// Filter Chip
FilterChip(
  label: Text('Filter'),
  selected: _isSelected,
  onSelected: (bool value) {
    setState(() {
      _isSelected = value;
    });
  },
)

// Choice Chip
ChoiceChip(
  label: Text('Choice'),
  selected: _isSelected,
  onSelected: (bool value) {
    setState(() {
      _isSelected = value;
    });
  },
)

// Action Chip
ActionChip(
  label: Text('Action'),
  onPressed: () {},
  avatar: Icon(Icons.add, size: 18),
)
```

### Badges

```dart
// Badge on Icon
Badge(
  label: Text('3'),
  child: Icon(Icons.notifications),
)

// Small Badge (dot)
Badge(
  smallSize: 8,
  child: Icon(Icons.message),
)

// Badge on NavigationBar
NavigationDestination(
  icon: Badge(
    label: Text('12'),
    child: Icon(Icons.mail_outlined),
  ),
  selectedIcon: Badge(
    label: Text('12'),
    child: Icon(Icons.mail),
  ),
  label: 'Messages',
)
```

### Progress Indicators

```dart
// Circular Progress Indicator
CircularProgressIndicator()

// Linear Progress Indicator
LinearProgressIndicator()

// With specific value
LinearProgressIndicator(value: 0.7)
```

### Lists

```dart
// ListTile
ListTile(
  leading: CircleAvatar(child: Icon(Icons.person)),
  title: Text('Title'),
  subtitle: Text('Subtitle'),
  trailing: Icon(Icons.arrow_forward_ios),
  onTap: () {},
)

// Three-line ListTile
ListTile(
  leading: Icon(Icons.album),
  title: Text('Song Title'),
  subtitle: Text('Artist Name\nAlbum Name'),
  isThreeLine: true,
  trailing: IconButton(
    icon: Icon(Icons.more_vert),
    onPressed: () {},
  ),
)
```

## Complete Theme Example

```dart
import 'package:flutter/material.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Material 3 Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.deepPurple,
          brightness: Brightness.light,
        ),
        useMaterial3: true,
        cardTheme: CardTheme(
          elevation: 2,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
        ),
        appBarTheme: AppBarTheme(
          centerTitle: false,
          elevation: 0,
        ),
        inputDecorationTheme: InputDecorationTheme(
          border: OutlineInputBorder(),
          filled: true,
        ),
      ),
      darkTheme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.deepPurple,
          brightness: Brightness.dark,
        ),
        useMaterial3: true,
      ),
      themeMode: ThemeMode.system,
      home: HomePage(),
    );
  }
}

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Material 3'),
        actions: [
          IconButton(icon: Icon(Icons.search), onPressed: () {}),
          IconButton(icon: Icon(Icons.more_vert), onPressed: () {}),
        ],
      ),
      body: ListView(
        padding: EdgeInsets.all(16),
        children: [
          Card(
            child: Padding(
              padding: EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Welcome to Material 3',
                    style: Theme.of(context).textTheme.headlineSmall,
                  ),
                  SizedBox(height: 8),
                  Text('Experience the new design system'),
                  SizedBox(height: 16),
                  FilledButton(
                    onPressed: () {},
                    child: Text('Get Started'),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {},
        child: Icon(Icons.add),
      ),
    );
  }
}
```

## Migration from Material 2

### Breaking Changes

Some widgets required entirely new implementations and cannot be automatically updated:

- `NavigationBar` - Replaces `BottomNavigationBar` with M3 styling
- `NavigationDrawer` - New drawer implementation
- `NavigationRail` - Enhanced for M3

### Migration Steps

1. **Enable Material 3** in your theme:
```dart
ThemeData(
  colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
  useMaterial3: true,
)
```

2. **Update color references** to use `ColorScheme` roles:
```dart
// Old
Container(color: Colors.blue)

// New
Container(color: Theme.of(context).colorScheme.primary)
```

3. **Replace deprecated widgets**:
- `BottomNavigationBar` → `NavigationBar`
- Custom drawer → `NavigationDrawer`

4. **Update button usage** to use M3 variants:
```dart
// Use new button types
FilledButton(onPressed: () {}, child: Text('Primary'))
FilledButton.tonal(onPressed: () {}, child: Text('Secondary'))
```

5. **Test visual appearance** - M3 components have different shapes and elevations

### Compatibility

Most Material widgets work in both M2 and M3 modes. Test your app with `useMaterial3: true` and fix any visual inconsistencies.

## Best Practices

1. **Use ColorScheme** - Reference colors through `Theme.of(context).colorScheme` instead of hard-coding
2. **Use semantic colors** - Use `primary`, `secondary`, etc., not specific colors
3. **Leverage TextTheme** - Use predefined text styles for consistency
4. **Test in dark mode** - Ensure your UI works in both light and dark themes
5. **Use appropriate button types** - Choose button emphasis based on action importance
6. **Follow elevation guidelines** - M3 uses less elevation than M2
7. **Embrace dynamic color** - Let users personalize your app with seed colors
8. **Test accessibility** - M3 improves contrast but still needs testing
9. **Use NavigationBar** - For bottom navigation on mobile
10. **Use NavigationRail** - For side navigation on tablets/desktop

## Resources

- [Material 3 Official Documentation](https://m3.material.io/)
- [Flutter Material 3 Demo](https://flutter.github.io/samples/web/material_3_demo/)
- [Migration Guide](https://docs.flutter.dev/release/breaking-changes/material-3-migration)
- [Affected Widgets List](https://api.flutter.dev/flutter/material/ThemeData/useMaterial3.html)

## Further Reading

- [Widget Catalog](widget-catalog.md)
- [Layout Patterns](layout-patterns.md)
- [Cupertino Widgets](cupertino-widgets.md)
