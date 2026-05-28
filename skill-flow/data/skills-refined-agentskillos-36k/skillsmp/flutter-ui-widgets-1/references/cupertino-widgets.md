# Cupertino Widgets

A comprehensive guide to Flutter's Cupertino widget library, which implements Apple's iOS and macOS design language with high-fidelity widgets that follow Apple's Human Interface Guidelines.

## Overview

Cupertino widgets provide beautiful, iOS-native experiences with pixel-perfect implementations of Apple's design patterns. These widgets feature rounded corners, translucent effects, smooth animations, and the distinctive iOS aesthetic.

### When to Use Cupertino Widgets

- **iOS-exclusive apps** - When building apps only for Apple platforms
- **Native iOS feel** - When you want an authentic iOS experience
- **Platform-adaptive UIs** - Mix with Material widgets for cross-platform apps
- **macOS apps** - For desktop macOS applications
- **Brand consistency** - When your brand aligns with iOS design language

### When to Use Material Instead

- **Cross-platform apps** - Material Design provides consistent look across platforms
- **Android-first apps** - Material is native to Android
- **Web apps** - Material Design is widely recognized on the web
- **Custom branding** - Material widgets are more customizable

## Getting Started

Import the Cupertino library:

```dart
import 'package:flutter/cupertino.dart';
```

For iOS-only apps, use `CupertinoApp` instead of `MaterialApp`:

```dart
import 'package:flutter/cupertino.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return CupertinoApp(
      title: 'Cupertino Demo',
      theme: CupertinoThemeData(
        primaryColor: CupertinoColors.systemBlue,
        brightness: Brightness.light,
      ),
      home: HomePage(),
    );
  }
}
```

## Core Cupertino Widgets

### CupertinoPageScaffold

The basic iOS page structure with navigation bar and content.

```dart
CupertinoPageScaffold(
  navigationBar: CupertinoNavigationBar(
    middle: Text('Page Title'),
    trailing: CupertinoButton(
      padding: EdgeInsets.zero,
      child: Icon(CupertinoIcons.ellipsis),
      onPressed: () {},
    ),
  ),
  child: SafeArea(
    child: Center(
      child: Text('Page content'),
    ),
  ),
)
```

### CupertinoNavigationBar

iOS-style navigation bar with translucent background.

```dart
CupertinoNavigationBar(
  // Left side
  leading: CupertinoNavigationBarBackButton(
    onPressed: () => Navigator.pop(context),
  ),

  // Center
  middle: Text('Navigation Bar'),

  // Right side
  trailing: CupertinoButton(
    padding: EdgeInsets.zero,
    child: Icon(CupertinoIcons.add),
    onPressed: () {},
  ),

  // Remove border
  border: null,

  // Background color
  backgroundColor: CupertinoColors.systemBackground.resolveFrom(context),
)
```

### CupertinoSliverNavigationBar

Large title navigation bar that collapses on scroll (iOS 11+ style).

```dart
CustomScrollView(
  slivers: [
    CupertinoSliverNavigationBar(
      largeTitle: Text('Large Title'),
      leading: CupertinoNavigationBarBackButton(),
      trailing: CupertinoButton(
        padding: EdgeInsets.zero,
        child: Icon(CupertinoIcons.ellipsis),
        onPressed: () {},
      ),
    ),
    SliverList(
      delegate: SliverChildBuilderDelegate(
        (context, index) => Container(
          height: 80,
          child: Center(child: Text('Item $index')),
        ),
        childCount: 50,
      ),
    ),
  ],
)
```

## Buttons

### CupertinoButton

Standard iOS button with various styles.

```dart
// Standard button
CupertinoButton(
  onPressed: () {},
  child: Text('Standard Button'),
)

// Filled button
CupertinoButton.filled(
  onPressed: () {},
  child: Text('Filled Button'),
)

// Tinted button (iOS 15+)
CupertinoButton(
  color: CupertinoColors.systemBlue.resolveFrom(context).withOpacity(0.15),
  onPressed: () {},
  child: Text(
    'Tinted Button',
    style: TextStyle(
      color: CupertinoColors.systemBlue.resolveFrom(context),
    ),
  ),
)

// Disabled button
CupertinoButton(
  onPressed: null,
  child: Text('Disabled'),
)

// Button with icon
CupertinoButton(
  onPressed: () {},
  child: Row(
    mainAxisSize: MainAxisSize.min,
    children: [
      Icon(CupertinoIcons.heart_fill, size: 20),
      SizedBox(width: 6),
      Text('Like'),
    ],
  ),
)

// Custom padding
CupertinoButton(
  padding: EdgeInsets.symmetric(horizontal: 24, vertical: 12),
  onPressed: () {},
  child: Text('Custom Padding'),
)
```

### Important Note on CupertinoButton Padding

When using `CupertinoButton` in a fixed-height parent like `CupertinoNavigationBar`, use smaller padding or `EdgeInsets.zero` to prevent clipping larger child widgets:

```dart
CupertinoNavigationBar(
  trailing: CupertinoButton(
    padding: EdgeInsets.zero,
    child: Icon(CupertinoIcons.settings),
    onPressed: () {},
  ),
)
```

## Input Widgets

### CupertinoTextField

iOS-style text input field.

```dart
CupertinoTextField(
  placeholder: 'Enter text',
  padding: EdgeInsets.all(12),
  decoration: BoxDecoration(
    color: CupertinoColors.systemGrey6,
    borderRadius: BorderRadius.circular(8),
  ),
  onChanged: (value) {
    print('Input: $value');
  },
)

// With prefix icon
CupertinoTextField(
  placeholder: 'Search',
  prefix: Padding(
    padding: EdgeInsets.only(left: 8),
    child: Icon(CupertinoIcons.search, size: 20),
  ),
  padding: EdgeInsets.symmetric(horizontal: 12, vertical: 10),
  decoration: BoxDecoration(
    color: CupertinoColors.systemGrey6,
    borderRadius: BorderRadius.circular(10),
  ),
)

// With clear button
CupertinoTextField(
  controller: _controller,
  placeholder: 'Clearable field',
  clearButtonMode: OverlayVisibilityMode.editing,
  padding: EdgeInsets.all(12),
  decoration: BoxDecoration(
    color: CupertinoColors.systemGrey6,
    borderRadius: BorderRadius.circular(8),
  ),
)

// Password field
CupertinoTextField(
  placeholder: 'Password',
  obscureText: true,
  padding: EdgeInsets.all(12),
  decoration: BoxDecoration(
    color: CupertinoColors.systemGrey6,
    borderRadius: BorderRadius.circular(8),
  ),
)
```

### CupertinoSwitch

iOS-style toggle switch.

```dart
class SwitchExample extends StatefulWidget {
  @override
  State<SwitchExample> createState() => _SwitchExampleState();
}

class _SwitchExampleState extends State<SwitchExample> {
  bool _switchValue = false;

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text('Enable notifications'),
        CupertinoSwitch(
          value: _switchValue,
          onChanged: (bool value) {
            setState(() {
              _switchValue = value;
            });
          },
        ),
      ],
    );
  }
}
```

### CupertinoSlider

iOS-style slider for selecting a value from a range.

```dart
class SliderExample extends StatefulWidget {
  @override
  State<SliderExample> createState() => _SliderExampleState();
}

class _SliderExampleState extends State<SliderExample> {
  double _sliderValue = 0.5;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Value: ${(_sliderValue * 100).round()}%'),
        CupertinoSlider(
          value: _sliderValue,
          onChanged: (double value) {
            setState(() {
              _sliderValue = value;
            });
          },
          min: 0.0,
          max: 1.0,
          divisions: 100,
          activeColor: CupertinoColors.systemBlue,
        ),
      ],
    );
  }
}
```

### CupertinoSegmentedControl

iOS-style segmented control for selecting from multiple options.

```dart
class SegmentedControlExample extends StatefulWidget {
  @override
  State<SegmentedControlExample> createState() => _SegmentedControlExampleState();
}

class _SegmentedControlExampleState extends State<SegmentedControlExample> {
  int _selectedSegment = 0;

  @override
  Widget build(BuildContext context) {
    return CupertinoSegmentedControl<int>(
      children: {
        0: Padding(
          padding: EdgeInsets.symmetric(horizontal: 20, vertical: 10),
          child: Text('First'),
        ),
        1: Padding(
          padding: EdgeInsets.symmetric(horizontal: 20, vertical: 10),
          child: Text('Second'),
        ),
        2: Padding(
          padding: EdgeInsets.symmetric(horizontal: 20, vertical: 10),
          child: Text('Third'),
        ),
      },
      groupValue: _selectedSegment,
      onValueChanged: (int value) {
        setState(() {
          _selectedSegment = value;
        });
      },
    );
  }
}
```

### CupertinoPicker

iOS-style wheel picker.

```dart
class PickerExample extends StatefulWidget {
  @override
  State<PickerExample> createState() => _PickerExampleState();
}

class _PickerExampleState extends State<PickerExample> {
  int _selectedItem = 0;
  final List<String> _items = ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5'];

  void _showPicker() {
    showCupertinoModalPopup(
      context: context,
      builder: (context) => Container(
        height: 250,
        color: CupertinoColors.systemBackground.resolveFrom(context),
        child: Column(
          children: [
            Container(
              height: 50,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  CupertinoButton(
                    child: Text('Cancel'),
                    onPressed: () => Navigator.pop(context),
                  ),
                  CupertinoButton(
                    child: Text('Done'),
                    onPressed: () => Navigator.pop(context),
                  ),
                ],
              ),
            ),
            Expanded(
              child: CupertinoPicker(
                itemExtent: 40,
                scrollController: FixedExtentScrollController(
                  initialItem: _selectedItem,
                ),
                onSelectedItemChanged: (int index) {
                  setState(() {
                    _selectedItem = index;
                  });
                },
                children: _items.map((item) => Center(child: Text(item))).toList(),
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return CupertinoButton(
      onPressed: _showPicker,
      child: Text('Show Picker: ${_items[_selectedItem]}'),
    );
  }
}
```

### CupertinoDatePicker

iOS-style date and time picker.

```dart
class DatePickerExample extends StatefulWidget {
  @override
  State<DatePickerExample> createState() => _DatePickerExampleState();
}

class _DatePickerExampleState extends State<DatePickerExample> {
  DateTime _selectedDate = DateTime.now();

  void _showDatePicker() {
    showCupertinoModalPopup(
      context: context,
      builder: (context) => Container(
        height: 300,
        color: CupertinoColors.systemBackground.resolveFrom(context),
        child: Column(
          children: [
            Container(
              height: 50,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  CupertinoButton(
                    child: Text('Cancel'),
                    onPressed: () => Navigator.pop(context),
                  ),
                  CupertinoButton(
                    child: Text('Done'),
                    onPressed: () => Navigator.pop(context),
                  ),
                ],
              ),
            ),
            Expanded(
              child: CupertinoDatePicker(
                mode: CupertinoDatePickerMode.date,
                initialDateTime: _selectedDate,
                onDateTimeChanged: (DateTime newDate) {
                  setState(() {
                    _selectedDate = newDate;
                  });
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return CupertinoButton(
      onPressed: _showDatePicker,
      child: Text('Date: ${_selectedDate.toString().split(' ')[0]}'),
    );
  }
}
```

## Dialogs and Sheets

### CupertinoAlertDialog

iOS-style alert dialog.

```dart
void _showAlertDialog(BuildContext context) {
  showCupertinoDialog(
    context: context,
    builder: (context) => CupertinoAlertDialog(
      title: Text('Alert'),
      content: Text('This is an iOS-style alert dialog.'),
      actions: [
        CupertinoDialogAction(
          child: Text('Cancel'),
          onPressed: () => Navigator.pop(context),
        ),
        CupertinoDialogAction(
          isDestructiveAction: true,
          onPressed: () {
            Navigator.pop(context);
            // Handle action
          },
          child: Text('Delete'),
        ),
      ],
    ),
  );
}
```

### CupertinoActionSheet

iOS-style action sheet that slides up from bottom.

```dart
void _showActionSheet(BuildContext context) {
  showCupertinoModalPopup(
    context: context,
    builder: (context) => CupertinoActionSheet(
      title: Text('Choose an action'),
      message: Text('Please select one of the options below'),
      actions: [
        CupertinoActionSheetAction(
          onPressed: () {
            Navigator.pop(context);
            // Handle action
          },
          child: Text('Share'),
        ),
        CupertinoActionSheetAction(
          onPressed: () {
            Navigator.pop(context);
            // Handle action
          },
          child: Text('Duplicate'),
        ),
        CupertinoActionSheetAction(
          isDestructiveAction: true,
          onPressed: () {
            Navigator.pop(context);
            // Handle action
          },
          child: Text('Delete'),
        ),
      ],
      cancelButton: CupertinoActionSheetAction(
        isDefaultAction: true,
        onPressed: () => Navigator.pop(context),
        child: Text('Cancel'),
      ),
    ),
  );
}
```

## Lists and Scrolling

### CupertinoListTile

iOS-style list item.

```dart
CupertinoListTile(
  leading: Icon(CupertinoIcons.person_circle),
  title: Text('John Doe'),
  subtitle: Text('Software Engineer'),
  trailing: CupertinoListTileChevron(),
  onTap: () {
    // Handle tap
  },
)
```

### CupertinoListSection

Grouped list section with iOS styling.

```dart
CupertinoListSection(
  header: Text('Settings'),
  children: [
    CupertinoListTile(
      leading: Icon(CupertinoIcons.profile_circled),
      title: Text('Profile'),
      trailing: CupertinoListTileChevron(),
      onTap: () {},
    ),
    CupertinoListTile(
      leading: Icon(CupertinoIcons.bell),
      title: Text('Notifications'),
      trailing: CupertinoListTileChevron(),
      onTap: () {},
    ),
    CupertinoListTile(
      leading: Icon(CupertinoIcons.lock),
      title: Text('Privacy'),
      trailing: CupertinoListTileChevron(),
      onTap: () {},
    ),
  ],
)

// Inset grouped style
CupertinoListSection.insetGrouped(
  header: Text('Account'),
  children: [
    CupertinoListTile(
      title: Text('Email'),
      additionalInfo: Text('john@example.com'),
    ),
    CupertinoListTile(
      title: Text('Phone'),
      additionalInfo: Text('+1 234 567 8900'),
    ),
  ],
)
```

### CupertinoScrollbar

iOS-style scrollbar.

```dart
CupertinoScrollbar(
  child: ListView.builder(
    itemCount: 100,
    itemBuilder: (context, index) {
      return CupertinoListTile(
        title: Text('Item $index'),
      );
    },
  ),
)
```

## Navigation

### CupertinoTabScaffold and CupertinoTabBar

iOS-style tab navigation.

```dart
class TabScaffoldExample extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return CupertinoTabScaffold(
      tabBar: CupertinoTabBar(
        items: const [
          BottomNavigationBarItem(
            icon: Icon(CupertinoIcons.home),
            label: 'Home',
          ),
          BottomNavigationBarItem(
            icon: Icon(CupertinoIcons.search),
            label: 'Search',
          ),
          BottomNavigationBarItem(
            icon: Icon(CupertinoIcons.person),
            label: 'Profile',
          ),
        ],
      ),
      tabBuilder: (context, index) {
        switch (index) {
          case 0:
            return CupertinoTabView(
              builder: (context) => HomePage(),
            );
          case 1:
            return CupertinoTabView(
              builder: (context) => SearchPage(),
            );
          case 2:
            return CupertinoTabView(
              builder: (context) => ProfilePage(),
            );
          default:
            return Container();
        }
      },
    );
  }
}
```

### CupertinoPageRoute

iOS-style page transitions.

```dart
Navigator.push(
  context,
  CupertinoPageRoute(
    builder: (context) => DetailPage(),
  ),
);

// Full screen modal
Navigator.push(
  context,
  CupertinoPageRoute(
    fullscreenDialog: true,
    builder: (context) => ModalPage(),
  ),
);
```

## Icons

Use `CupertinoIcons` for iOS-style icons.

```dart
import 'package:flutter/cupertino.dart';

Icon(CupertinoIcons.heart)
Icon(CupertinoIcons.heart_fill)
Icon(CupertinoIcons.star)
Icon(CupertinoIcons.star_fill)
Icon(CupertinoIcons.home)
Icon(CupertinoIcons.search)
Icon(CupertinoIcons.settings)
Icon(CupertinoIcons.person)
Icon(CupertinoIcons.bell)
Icon(CupertinoIcons.chat_bubble)
Icon(CupertinoIcons.mail)
Icon(CupertinoIcons.location)
Icon(CupertinoIcons.camera)
Icon(CupertinoIcons.photo)
Icon(CupertinoIcons.share)
Icon(CupertinoIcons.trash)
Icon(CupertinoIcons.add)
Icon(CupertinoIcons.check_mark)
Icon(CupertinoIcons.multiply)
```

## Activity Indicator

iOS-style loading spinner.

```dart
CupertinoActivityIndicator()

// Large size
CupertinoActivityIndicator(radius: 14)

// Custom color
CupertinoActivityIndicator(
  color: CupertinoColors.systemBlue,
)
```

## Context Menu

iOS-style long-press context menu.

```dart
CupertinoContextMenu(
  actions: [
    CupertinoContextMenuAction(
      child: Text('Copy'),
      onPressed: () {
        Navigator.pop(context);
        // Handle action
      },
    ),
    CupertinoContextMenuAction(
      child: Text('Share'),
      onPressed: () {
        Navigator.pop(context);
        // Handle action
      },
    ),
    CupertinoContextMenuAction(
      isDestructiveAction: true,
      child: Text('Delete'),
      onPressed: () {
        Navigator.pop(context);
        // Handle action
      },
    ),
  ],
  child: Container(
    width: 200,
    height: 200,
    decoration: BoxDecoration(
      color: CupertinoColors.systemGrey,
      borderRadius: BorderRadius.circular(12),
    ),
    child: Center(child: Text('Long press me')),
  ),
)
```

## Cupertino Colors

iOS system colors that adapt to light/dark mode.

```dart
// System colors
CupertinoColors.systemBlue
CupertinoColors.systemGreen
CupertinoColors.systemIndigo
CupertinoColors.systemOrange
CupertinoColors.systemPink
CupertinoColors.systemPurple
CupertinoColors.systemRed
CupertinoColors.systemTeal
CupertinoColors.systemYellow

// Gray scale
CupertinoColors.systemGrey
CupertinoColors.systemGrey2
CupertinoColors.systemGrey3
CupertinoColors.systemGrey4
CupertinoColors.systemGrey5
CupertinoColors.systemGrey6

// Backgrounds
CupertinoColors.systemBackground
CupertinoColors.secondarySystemBackground
CupertinoColors.tertiarySystemBackground

// Labels
CupertinoColors.label
CupertinoColors.secondaryLabel
CupertinoColors.tertiaryLabel
CupertinoColors.quaternaryLabel

// Resolve color for current brightness
final color = CupertinoColors.systemBlue.resolveFrom(context);
```

## Platform-Adaptive Widgets

Mix Material and Cupertino for cross-platform apps.

```dart
import 'dart:io';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class AdaptiveButton extends StatelessWidget {
  final VoidCallback onPressed;
  final Widget child;

  const AdaptiveButton({
    required this.onPressed,
    required this.child,
  });

  @override
  Widget build(BuildContext context) {
    if (Platform.isIOS || Platform.isMacOS) {
      return CupertinoButton.filled(
        onPressed: onPressed,
        child: child,
      );
    } else {
      return ElevatedButton(
        onPressed: onPressed,
        child: child,
      );
    }
  }
}

// Adaptive app
class AdaptiveApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    if (Platform.isIOS || Platform.isMacOS) {
      return CupertinoApp(
        home: HomePage(),
      );
    } else {
      return MaterialApp(
        home: HomePage(),
      );
    }
  }
}

// Adaptive progress indicator
Widget adaptiveProgressIndicator() {
  if (Platform.isIOS || Platform.isMacOS) {
    return CupertinoActivityIndicator();
  } else {
    return CircularProgressIndicator();
  }
}
```

## Complete Example App

```dart
import 'package:flutter/cupertino.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return CupertinoApp(
      title: 'Cupertino Demo',
      theme: CupertinoThemeData(
        primaryColor: CupertinoColors.systemBlue,
      ),
      home: HomeScreen(),
    );
  }
}

class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return CupertinoTabScaffold(
      tabBar: CupertinoTabBar(
        items: const [
          BottomNavigationBarItem(
            icon: Icon(CupertinoIcons.home),
            label: 'Home',
          ),
          BottomNavigationBarItem(
            icon: Icon(CupertinoIcons.settings),
            label: 'Settings',
          ),
        ],
      ),
      tabBuilder: (context, index) {
        if (index == 0) {
          return CupertinoTabView(
            builder: (context) => HomePage(),
          );
        } else {
          return CupertinoTabView(
            builder: (context) => SettingsPage(),
          );
        }
      },
    );
  }
}

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return CupertinoPageScaffold(
      navigationBar: CupertinoNavigationBar(
        middle: Text('Home'),
      ),
      child: SafeArea(
        child: ListView(
          children: [
            CupertinoListSection.insetGrouped(
              header: Text('Quick Actions'),
              children: [
                CupertinoListTile(
                  leading: Icon(CupertinoIcons.add_circled),
                  title: Text('Create New'),
                  trailing: CupertinoListTileChevron(),
                  onTap: () {
                    Navigator.push(
                      context,
                      CupertinoPageRoute(
                        builder: (context) => DetailPage(),
                      ),
                    );
                  },
                ),
                CupertinoListTile(
                  leading: Icon(CupertinoIcons.search),
                  title: Text('Search'),
                  trailing: CupertinoListTileChevron(),
                  onTap: () {},
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class SettingsPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return CupertinoPageScaffold(
      navigationBar: CupertinoNavigationBar(
        middle: Text('Settings'),
      ),
      child: SafeArea(
        child: CupertinoListSection.insetGrouped(
          children: [
            CupertinoListTile(
              leading: Icon(CupertinoIcons.person),
              title: Text('Profile'),
              trailing: CupertinoListTileChevron(),
            ),
            CupertinoListTile(
              leading: Icon(CupertinoIcons.bell),
              title: Text('Notifications'),
              trailing: CupertinoListTileChevron(),
            ),
          ],
        ),
      ),
    );
  }
}

class DetailPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return CupertinoPageScaffold(
      navigationBar: CupertinoNavigationBar(
        middle: Text('Detail'),
      ),
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Detail Page'),
            SizedBox(height: 20),
            CupertinoButton.filled(
              onPressed: () => Navigator.pop(context),
              child: Text('Go Back'),
            ),
          ],
        ),
      ),
    );
  }
}
```

## Best Practices

1. **Use SafeArea** - Ensure content doesn't overlap with system UI (notch, home indicator)
2. **Respect iOS conventions** - Use back swipe gestures, iOS navigation patterns
3. **Use CupertinoIcons** - iOS-style icons for consistency
4. **Test on iOS devices** - Cupertino widgets are optimized for iOS
5. **Use CupertinoThemeData** - Maintain consistent styling across the app
6. **Handle padding properly** - Reduce padding in navigation bars to prevent clipping
7. **Use adaptive widgets** - Mix Material and Cupertino for cross-platform apps
8. **Follow HIG** - Apple's Human Interface Guidelines for iOS design
9. **Test dark mode** - Cupertino colors adapt to brightness
10. **Use CupertinoPageRoute** - Native iOS page transitions

## Cupertino vs Material Comparison

| Feature | Cupertino | Material |
|---------|-----------|----------|
| **App** | `CupertinoApp` | `MaterialApp` |
| **Scaffold** | `CupertinoPageScaffold` | `Scaffold` |
| **Button** | `CupertinoButton` | `ElevatedButton`, `FilledButton` |
| **Switch** | `CupertinoSwitch` | `Switch` |
| **Slider** | `CupertinoSlider` | `Slider` |
| **TextField** | `CupertinoTextField` | `TextField` |
| **Dialog** | `CupertinoAlertDialog` | `AlertDialog` |
| **Navigation** | `CupertinoNavigationBar` | `AppBar` |
| **Icons** | `CupertinoIcons` | `Icons` |
| **Loading** | `CupertinoActivityIndicator` | `CircularProgressIndicator` |
| **Tab Bar** | `CupertinoTabBar` | `BottomNavigationBar`, `NavigationBar` |

## Further Reading

- [Cupertino Design Guidelines](https://docs.flutter.dev/ui/design/cupertino)
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [Widget Catalog](widget-catalog.md)
- [Material Design 3](material-design-3.md)
