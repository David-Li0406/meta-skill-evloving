# Design Systems Reference Guide

Comprehensive specifications for the four supported design systems: WeChat Work, iOS Native (HIG), Material Design 3, and Ant Design Mobile.

---

## Table of Contents

1. [WeChat Work Design System](#wechat-work-design-system)
2. [iOS Native (HIG)](#ios-native-hig)
3. [Material Design 3](#material-design-3)
4. [Ant Design Mobile](#ant-design-mobile)
5. [Component Mapping](#component-mapping)
6. [Cross-Platform Considerations](#cross-platform-considerations)

---

## WeChat Work Design System

### Overview

**Platform**: Enterprise messaging, hybrid apps (WeChat Mini Programs, H5)
**Design Philosophy**: Lightweight, efficient, enterprise-focused
**Visual Style**: Flat design, minimal shadows, functional over decorative

### Core Principles

1. **Efficiency First** - Minimize steps to complete tasks
2. **Consistency** - Align with WeChat ecosystem
3. **Clarity** - Clear visual hierarchy and information architecture
4. **Accessibility** - Support for diverse enterprise users

### Design Tokens

```css
/* Colors */
--weui-primary: #07C160;        /* Green - primary actions */
--weui-link: #576B95;           /* Blue - links */
--weui-text-primary: #000000;   /* Primary text */
--weui-text-secondary: #888888; /* Secondary text */
--weui-border: #E5E5E5;         /* Hairline borders */
--weui-bg: #FFFFFF;             /* Background */
--weui-bg-secondary: #F7F7F7;   /* Secondary background */
--weui-warn: #FA5151;           /* Warning/error red */

/* Typography */
--weui-font-family: -apple-system-font, "Helvetica Neue", sans-serif;
--weui-font-size-large: 18px;
--weui-font-size-medium: 17px;
--weui-font-size-base: 16px;
--weui-font-size-small: 14px;
--weui-font-size-mini: 13px;

/* Spacing */
--weui-spacing-small: 8px;
--weui-spacing-medium: 15px;
--weui-spacing-large: 20px;
--weui-spacing-xlarge: 30px;

/* Border Radius */
--weui-border-radius: 8px;
--weui-border-radius-large: 12px;
```

### Component Library

#### Navigation

**TabBar (weui-tabbar)**
```html
<!-- Bottom navigation for primary sections -->
<div class="weui-tabbar">
  <a class="weui-tabbar__item weui-bar__item_on">
    <div class="weui-tabbar__icon">
      <img src="icon-home.png" />
    </div>
    <p class="weui-tabbar__label">首页</p>
  </a>
  <!-- More items... -->
</div>
```
- Position: Fixed bottom
- Height: 50px
- Icons: 28x28px
- Max items: 5

**NavigationBar (weui-navigation-bar)**
```html
<!-- Top navigation with title and actions -->
<div class="weui-navigation-bar">
  <div class="weui-navigation-bar__left">
    <a class="weui-navigation-bar__btn">返回</a>
  </div>
  <h1 class="weui-navigation-bar__title">页面标题</h1>
  <div class="weui-navigation-bar__right">
    <a class="weui-navigation-bar__btn">更多</a>
  </div>
</div>
```
- Height: 44px (iOS), 48px (Android)
- Background: Solid color or translucent

#### Buttons

**Primary Button (weui-btn_primary)**
```css
.weui-btn_primary {
  background-color: #07C160;
  color: #FFFFFF;
  height: 48px;
  border-radius: 8px;
  font-size: 17px;
}
```

**Default Button (weui-btn_default)**
```css
.weui-btn_default {
  background-color: #FFFFFF;
  color: #000000;
  border: 1px solid #E5E5E5;
}
```

**Plain Button (weui-btn_plain)**
```css
.weui-btn_plain {
  background-color: transparent;
  color: #07C160;
  border: 1px solid #07C160;
}
```

#### Lists

**Cell (weui-cell)**
```html
<!-- Standard list item -->
<div class="weui-cell">
  <div class="weui-cell__hd">
    <img src="icon.png" style="width: 20px; margin-right: 5px;" />
  </div>
  <div class="weui-cell__bd">
    <p>标题</p>
  </div>
  <div class="weui-cell__ft">详细信息</div>
</div>
```

**Media Box (weui-media-box)**
```html
<!-- Rich content list item -->
<div class="weui-media-box weui-media-box_text">
  <h4 class="weui-media-box__title">标题</h4>
  <p class="weui-media-box__desc">描述文字...</p>
  <ul class="weui-media-box__info">
    <li class="weui-media-box__info__meta">作者</li>
    <li class="weui-media-box__info__meta">时间</li>
  </ul>
</div>
```

#### Forms

**Input (weui-input)**
```html
<div class="weui-cell">
  <div class="weui-cell__hd">
    <label class="weui-label">用户名</label>
  </div>
  <div class="weui-cell__bd">
    <input class="weui-input" type="text" placeholder="请输入" />
  </div>
</div>
```

**Textarea (weui-textarea)**
```html
<div class="weui-cell">
  <div class="weui-cell__bd">
    <textarea class="weui-textarea" placeholder="请输入" rows="3"></textarea>
  </div>
</div>
```

**Switch (weui-switch)**
```html
<div class="weui-cell weui-cell_switch">
  <div class="weui-cell__bd">开关</div>
  <div class="weui-cell__ft">
    <input class="weui-switch" type="checkbox" />
  </div>
</div>
```

#### Feedback

**Dialog (weui-dialog)**
```html
<div class="weui-dialog">
  <div class="weui-dialog__hd">
    <strong class="weui-dialog__title">标题</strong>
  </div>
  <div class="weui-dialog__bd">内容文本</div>
  <div class="weui-dialog__ft">
    <a class="weui-dialog__btn weui-dialog__btn_default">取消</a>
    <a class="weui-dialog__btn weui-dialog__btn_primary">确定</a>
  </div>
</div>
```

**Toast (weui-toast)**
```html
<div class="weui-toast">
  <i class="weui-icon-success-no-circle weui-icon_toast"></i>
  <p class="weui-toast__content">操作成功</p>
</div>
```
- Duration: 2000ms (default)
- Position: Center of screen

### Interaction Patterns

- **Tap**: Primary action (no hover states)
- **Long press**: Contextual menu (hold 500ms)
- **Swipe left**: Delete action in lists
- **Pull-to-refresh**: Standard WeChat pattern

### Accessibility

- Minimum tap target: 44x44px
- Color contrast: WCAG AA minimum (4.5:1)
- Font scaling: Support system font size settings
- Screen reader: Support ARIA labels (for H5)

---

## iOS Native (HIG)

### Overview

**Platform**: iPhone, iPad, Apple Watch, macOS
**Design Philosophy**: Clarity, deference, depth
**Visual Style**: Translucency, vibrancy, rounded corners, shadows

### Core Principles

1. **Clarity** - Text is legible, icons are precise, functionality is obvious
2. **Deference** - UI helps users understand content, not compete with it
3. **Depth** - Layering and motion convey hierarchy and vitality

### Design Tokens

```swift
// Colors (iOS 13+ Dynamic Colors)
UIColor.systemBackground        // Adaptive white/black
UIColor.secondarySystemBackground
UIColor.label                   // Primary text
UIColor.secondaryLabel          // Secondary text
UIColor.systemBlue              // Accent color
UIColor.systemGreen
UIColor.systemRed

// Typography (SF Pro)
UIFont.preferredFont(forTextStyle: .largeTitle)  // 34pt
UIFont.preferredFont(forTextStyle: .title1)      // 28pt
UIFont.preferredFont(forTextStyle: .title2)      // 22pt
UIFont.preferredFont(forTextStyle: .title3)      // 20pt
UIFont.preferredFont(forTextStyle: .headline)    // 17pt bold
UIFont.preferredFont(forTextStyle: .body)        // 17pt regular
UIFont.preferredFont(forTextStyle: .callout)     // 16pt
UIFont.preferredFont(forTextStyle: .subheadline) // 15pt
UIFont.preferredFont(forTextStyle: .footnote)    // 13pt
UIFont.preferredFont(forTextStyle: .caption1)    // 12pt

// Spacing (using multiples of 8)
let spacing8: CGFloat = 8
let spacing16: CGFloat = 16
let spacing24: CGFloat = 24
let spacing32: CGFloat = 32

// Corner Radius
let cornerRadiusSmall: CGFloat = 8
let cornerRadiusMedium: CGFloat = 10
let cornerRadiusLarge: CGFloat = 12
```

### Component Library

#### Navigation

**UINavigationBar**
```swift
// Large title style (iOS 11+)
navigationController?.navigationBar.prefersLargeTitles = true
navigationItem.title = "Title"
navigationItem.largeTitleDisplayMode = .always

// Right bar button
navigationItem.rightBarButtonItem = UIBarButtonItem(
  systemItem: .add,
  target: self,
  action: #selector(addTapped)
)
```
- Height: 44pt (compact), 96pt (large title)
- Background: Translucent blur
- Large title: 34pt bold, collapses on scroll

**UITabBar**
```swift
// Tab bar with SF Symbols
let tabBarItem = UITabBarItem(
  title: "Home",
  image: UIImage(systemName: "house"),
  selectedImage: UIImage(systemName: "house.fill")
)
```
- Height: 49pt (standard), 83pt (with safe area)
- Max tabs: 5 (more items go to "More" tab)
- Icons: 25x25pt target size

**UISearchBar**
```swift
let searchBar = UISearchBar()
searchBar.placeholder = "Search"
searchBar.searchBarStyle = .minimal
```
- Height: 44pt
- Corner radius: 10pt
- Integrated cancel button

#### Buttons

**UIButton (Filled)**
```swift
var configuration = UIButton.Configuration.filled()
configuration.title = "Continue"
configuration.cornerStyle = .large  // 12pt radius
let button = UIButton(configuration: configuration)
```
- Height: 44pt minimum
- Padding: 16pt horizontal, 12pt vertical

**UIButton (Borderless)**
```swift
var configuration = UIButton.Configuration.borderless()
configuration.title = "Learn More"
```

#### Lists

**UITableView**
```swift
// Standard cell
let cell = UITableViewCell(style: .default, reuseIdentifier: "cell")
cell.textLabel?.text = "Title"
cell.accessoryType = .disclosureIndicator

// Subtitle cell
let cell = UITableViewCell(style: .subtitle, reuseIdentifier: "cell")
cell.textLabel?.text = "Title"
cell.detailTextLabel?.text = "Subtitle"

// Custom cell with SF Symbols
let cell = UITableViewCell(style: .value1, reuseIdentifier: "cell")
cell.imageView?.image = UIImage(systemName: "person.fill")
cell.textLabel?.text = "Profile"
```
- Row height: 44pt minimum
- Swipe actions: Leading and trailing
- Separators: Inset 16pt from leading edge

**UICollectionView**
```swift
let layout = UICollectionViewFlowLayoutCompositional.list(
  using: .init(appearance: .grouped)
)
let collectionView = UICollectionView(frame: .zero, collectionViewLayout: layout)
```
- Modern list layouts (iOS 14+)
- Diffable data sources

#### Forms

**UITextField**
```swift
let textField = UITextField()
textField.placeholder = "Enter text"
textField.borderStyle = .roundedRect
textField.clearButtonMode = .whileEditing
```
- Height: 44pt
- Corner radius: 8pt
- Padding: 8pt

**UITextView**
```swift
let textView = UITextView()
textView.font = UIFont.preferredFont(forTextStyle: .body)
textView.textContainerInset = UIEdgeInsets(top: 8, left: 8, bottom: 8, right: 8)
```

**UISwitch**
```swift
let toggle = UISwitch()
toggle.onTintColor = .systemGreen
```
- Size: 51x31pt
- Thumb: 27x27pt circle

**UISegmentedControl**
```swift
let segmentedControl = UISegmentedControl(items: ["First", "Second", "Third"])
segmentedControl.selectedSegmentIndex = 0
```
- Height: 32pt
- Adapts to dark mode

#### Feedback

**UIAlertController**
```swift
let alert = UIAlertController(
  title: "Title",
  message: "Message text",
  preferredStyle: .alert
)
alert.addAction(UIAlertAction(title: "Cancel", style: .cancel))
alert.addAction(UIAlertAction(title: "OK", style: .default))
present(alert, animated: true)
```

**UIAlertController (Action Sheet)**
```swift
let actionSheet = UIAlertController(
  title: "Choose an option",
  message: nil,
  preferredStyle: .actionSheet
)
actionSheet.addAction(UIAlertAction(title: "Option 1", style: .default))
actionSheet.addAction(UIAlertAction(title: "Delete", style: .destructive))
actionSheet.addAction(UIAlertAction(title: "Cancel", style: .cancel))
```

**Toast (Custom)**
```swift
// iOS doesn't have native toast, use custom view
let toastView = UIView()
toastView.backgroundColor = .label.withAlphaComponent(0.8)
toastView.layer.cornerRadius = 10
// Add label, position, animate...
```

### SF Symbols

**Common Icons:**
- `house` / `house.fill` - Home
- `magnifyingglass` - Search
- `person` / `person.fill` - Profile
- `plus` - Add
- `ellipsis` - More
- `trash` / `trash.fill` - Delete
- `checkmark.circle` - Success
- `xmark.circle` - Error

**Sizing:**
```swift
let config = UIImage.SymbolConfiguration(pointSize: 24, weight: .medium)
let image = UIImage(systemName: "heart.fill", withConfiguration: config)
```

### Interaction Patterns

- **Tap**: Primary action
- **Swipe left/right**: Navigate back, reveal actions
- **Long press**: Context menu (iOS 13+)
- **3D Touch** (legacy): Peek and pop
- **Pull-to-refresh**: Refresh content

### Accessibility

- **Dynamic Type**: Support all text styles
- **VoiceOver**: Provide accessibility labels
- **Color contrast**: WCAG AA minimum
- **Haptic feedback**: Use UIImpactFeedbackGenerator
- **Minimum tap target**: 44x44pt

---

## Material Design 3

### Overview

**Platform**: Android, Web, Flutter
**Design Philosophy**: Material is the metaphor, bold and intentional, motion provides meaning
**Visual Style**: Elevation shadows, ripple effects, bold colors, FAB

### Core Principles

1. **Material as Metaphor** - Inspired by physical materials (paper, ink)
2. **Bold, Graphic, Intentional** - Strong visual hierarchy
3. **Motion Provides Meaning** - Motion respects and reinforces the user as the prime mover

### Design Tokens (Material You)

```css
/* Dynamic Color System (Material 3) */
--md-sys-color-primary: #6750A4;
--md-sys-color-on-primary: #FFFFFF;
--md-sys-color-primary-container: #EADDFF;
--md-sys-color-on-primary-container: #21005E;

--md-sys-color-secondary: #625B71;
--md-sys-color-on-secondary: #FFFFFF;
--md-sys-color-secondary-container: #E8DEF8;
--md-sys-color-on-secondary-container: #1E192B;

--md-sys-color-surface: #FFFBFE;
--md-sys-color-on-surface: #1C1B1F;
--md-sys-color-surface-variant: #E7E0EC;
--md-sys-color-on-surface-variant: #49454E;

--md-sys-color-error: #B3261E;
--md-sys-color-on-error: #FFFFFF;

/* Typography (Roboto) */
--md-sys-typescale-display-large: 57px / 64px Roboto;
--md-sys-typescale-display-medium: 45px / 52px Roboto;
--md-sys-typescale-display-small: 36px / 44px Roboto;

--md-sys-typescale-headline-large: 32px / 40px Roboto;
--md-sys-typescale-headline-medium: 28px / 36px Roboto;
--md-sys-typescale-headline-small: 24px / 32px Roboto;

--md-sys-typescale-body-large: 16px / 24px Roboto;
--md-sys-typescale-body-medium: 14px / 20px Roboto;
--md-sys-typescale-body-small: 12px / 16px Roboto;

--md-sys-typescale-label-large: 14px / 20px Roboto Medium (500);
--md-sys-typescale-label-medium: 12px / 16px Roboto Medium;
--md-sys-typescale-label-small: 11px / 16px Roboto Medium;

/* Elevation (Shadows) */
--md-sys-elevation-level0: none;
--md-sys-elevation-level1: 0 1px 2px rgba(0,0,0,0.3), 0 1px 3px 1px rgba(0,0,0,0.15);
--md-sys-elevation-level2: 0 1px 2px rgba(0,0,0,0.3), 0 2px 6px 2px rgba(0,0,0,0.15);
--md-sys-elevation-level3: 0 1px 3px rgba(0,0,0,0.3), 0 4px 8px 3px rgba(0,0,0,0.15);
--md-sys-elevation-level4: 0 2px 3px rgba(0,0,0,0.3), 0 6px 10px 4px rgba(0,0,0,0.15);
--md-sys-elevation-level5: 0 4px 4px rgba(0,0,0,0.3), 0 8px 12px 6px rgba(0,0,0,0.15);

/* Shape (Corner Radius) */
--md-sys-shape-corner-none: 0px;
--md-sys-shape-corner-extra-small: 4px;
--md-sys-shape-corner-small: 8px;
--md-sys-shape-corner-medium: 12px;
--md-sys-shape-corner-large: 16px;
--md-sys-shape-corner-extra-large: 28px;
--md-sys-shape-corner-full: 9999px;

/* Spacing */
--md-sys-spacing-unit: 8px;
```

### Component Library

#### Navigation

**Top App Bar**
```xml
<com.google.android.material.appbar.MaterialToolbar
    android:layout_width="match_parent"
    android:layout_height="?attr/actionBarSize"
    app:title="Title"
    app:navigationIcon="@drawable/ic_arrow_back" />
```
- Height: 56dp (phone), 64dp (tablet)
- Elevation: 0-4dp
- Large variant: Collapsing with large title (96dp when expanded)

**Bottom Navigation Bar**
```xml
<com.google.android.material.bottomnavigation.BottomNavigationView
    android:layout_width="match_parent"
    android:layout_height="56dp"
    app:menu="@menu/bottom_nav_menu" />
```
- Height: 56dp
- Max items: 5 (3-5 recommended)
- Icons: 24x24dp

**Navigation Rail (Tablet/Desktop)**
```xml
<com.google.android.material.navigationrail.NavigationRailView
    android:layout_width="80dp"
    android:layout_height="match_parent" />
```

**Navigation Drawer**
```xml
<com.google.android.material.navigation.NavigationView
    android:layout_width="wrap_content"
    android:layout_height="match_parent"
    android:layout_gravity="start"
    app:menu="@menu/drawer_menu" />
```
- Width: 256dp (standard), 320dp (wide)
- Overlay: 60% opacity black scrim

#### Buttons

**Filled Button (Primary)**
```xml
<com.google.android.material.button.MaterialButton
    style="@style/Widget.Material3.Button"
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:text="Continue" />
```
- Height: 40dp
- Padding: 24dp horizontal, 10dp vertical
- Corner radius: 20dp (full pill)

**Outlined Button**
```xml
<com.google.android.material.button.MaterialButton
    style="@style/Widget.Material3.Button.OutlinedButton"
    android:text="Cancel" />
```

**Text Button**
```xml
<com.google.android.material.button.MaterialButton
    style="@style/Widget.Material3.Button.TextButton"
    android:text="Learn More" />
```

**FAB (Floating Action Button)**
```xml
<com.google.android.material.floatingactionbutton.FloatingActionButton
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:src="@drawable/ic_add"
    app:fabSize="normal" />
```
- Size: 56x56dp (normal), 40x40dp (mini)
- Elevation: 6dp (resting), 12dp (pressed)
- Position: 16dp from edges

**Extended FAB**
```xml
<com.google.android.material.floatingactionbutton.ExtendedFloatingActionButton
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:text="Create"
    app:icon="@drawable/ic_add" />
```

#### Cards

**Filled Card**
```xml
<com.google.android.material.card.MaterialCardView
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    app:cardElevation="1dp"
    app:cardCornerRadius="12dp">

  <LinearLayout
      android:layout_width="match_parent"
      android:layout_height="wrap_content"
      android:orientation="vertical"
      android:padding="16dp">

    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Card Title"
        android:textAppearance="?attr/textAppearanceTitleMedium" />

    <TextView
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Card content..."
        android:textAppearance="?attr/textAppearanceBodyMedium" />

  </LinearLayout>
</com.google.android.material.card.MaterialCardView>
```

**Outlined Card**
```xml
<com.google.android.material.card.MaterialCardView
    style="@style/Widget.Material3.CardView.Outlined"
    android:layout_width="match_parent"
    android:layout_height="wrap_content" />
```

#### Lists

**List Item (3-line)**
```xml
<com.google.android.material.lists.ThreeLineListItem
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    app:primaryText="Primary text"
    app:secondaryText="Secondary text"
    app:tertiaryText="Tertiary text"
    app:leadingIcon="@drawable/ic_person" />
```
- Height: 56dp (1-line), 72dp (2-line), 88dp (3-line)
- Padding: 16dp horizontal
- Icon size: 24x24dp (leading), 18x18dp (trailing)

#### Forms

**Text Field (Outlined)**
```xml
<com.google.android.material.textfield.TextInputLayout
    style="@style/Widget.Material3.TextInputLayout.OutlinedBox"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:hint="Label">

  <com.google.android.material.textfield.TextInputEditText
      android:layout_width="match_parent"
      android:layout_height="wrap_content" />

</com.google.android.material.textfield.TextInputLayout>
```

**Text Field (Filled)**
```xml
<com.google.android.material.textfield.TextInputLayout
    style="@style/Widget.Material3.TextInputLayout.FilledBox"
    android:layout_width="match_parent"
    android:layout_height="wrap_content" />
```

**Checkbox**
```xml
<com.google.android.material.checkbox.MaterialCheckBox
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:text="Checkbox label" />
```
- Size: 18x18dp (box), 40x40dp (touch target)

**Switch**
```xml
<com.google.android.material.switchmaterial.SwitchMaterial
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:text="Switch label" />
```
- Size: 52x32dp (track), 20x20dp (thumb)

**Slider**
```xml
<com.google.android.material.slider.Slider
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:valueFrom="0.0"
    android:valueTo="100.0"
    android:value="50.0" />
```

#### Feedback

**Snackbar**
```kotlin
Snackbar.make(view, "Message text", Snackbar.LENGTH_SHORT)
    .setAction("Action") { /* Handle action */ }
    .show()
```
- Duration: 4000ms (SHORT), 10000ms (LONG), indefinite (INDEFINITE)
- Position: Bottom (phone), bottom-left (tablet)
- Width: Full width (phone), 344dp max (tablet)

**Dialog**
```xml
<com.google.android.material.dialog.MaterialAlertDialogBuilder
    android:layout_width="280dp"
    android:layout_height="wrap_content"
    app:title="Dialog Title"
    app:message="Dialog message..."
    app:positiveButton="OK"
    app:negativeButton="Cancel" />
```
- Max width: 560dp
- Padding: 24dp
- Corner radius: 28dp

**Bottom Sheet**
```xml
<com.google.android.material.bottomsheet.BottomSheetDialogFragment
    android:layout_width="match_parent"
    android:layout_height="wrap_content" />
```
- Corner radius: 28dp (top corners)
- Drag handle: 32x4dp centered

**Progress Indicator**
```xml
<!-- Circular -->
<com.google.android.material.progressindicator.CircularProgressIndicator
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:indeterminate="true" />

<!-- Linear -->
<com.google.android.material.progressindicator.LinearProgressIndicator
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:indeterminate="true" />
```

### Material Icons

**Icon Library**: https://fonts.google.com/icons

**Common Icons:**
- `home` - Home
- `search` - Search
- `person` - Profile
- `add` - Add
- `more_vert` - More (vertical dots)
- `delete` - Delete
- `check_circle` - Success
- `error` - Error
- `arrow_back` - Back navigation

**Icon Sizes:**
- 18dp - Small inline
- 24dp - Standard
- 36dp - Large
- 48dp - App icon

### Interaction Patterns

- **Tap**: Primary action with ripple effect
- **Long press**: Context menu
- **Swipe**: Dismiss, navigate between tabs
- **Drag**: Reorder lists, adjust sliders
- **Pinch**: Zoom (maps, images)

### Motion

**Duration:**
- Simple: 100ms
- Complex: 200-300ms
- Entering: 150ms
- Exiting: 75ms

**Easing:**
- Standard: cubic-bezier(0.4, 0.0, 0.2, 1)
- Decelerate: cubic-bezier(0.0, 0.0, 0.2, 1)
- Accelerate: cubic-bezier(0.4, 0.0, 1, 1)

### Accessibility

- **Touch target**: 48x48dp minimum
- **Color contrast**: WCAG AA minimum (4.5:1 text, 3:1 UI)
- **TalkBack**: Support content descriptions
- **Text scaling**: Support system font size
- **Color blind mode**: Don't rely on color alone

---

## Ant Design Mobile

### Overview

**Platform**: Mobile web (React), Hybrid apps
**Design Philosophy**: Natural, certain, meaningful, growing
**Visual Style**: Clean lines, minimal shadows, blue accent

### Core Principles

1. **Natural** - UI design rooted in nature
2. **Certain** - Interface should reduce cognitive load
3. **Meaningful** - Consistency and feedback are meaningful
4. **Growing** - Design system evolves with product

### Design Tokens

```css
/* Colors */
--adm-color-primary: #1677FF;
--adm-color-success: #00B578;
--adm-color-warning: #FF8F1F;
--adm-color-danger: #FF3141;

--adm-color-text: #333333;
--adm-color-text-secondary: #666666;
--adm-color-weak: #999999;
--adm-color-light: #CCCCCC;

--adm-color-background: #FFFFFF;
--adm-color-border: #EEEEEE;
--adm-color-box: #F5F5F5;

/* Typography (PingFang SC / Roboto) */
--adm-font-size-main: 15px;
--adm-font-size-heading: 17px;
--adm-font-size-small: 13px;
--adm-font-size-xsmall: 12px;

--adm-font-weight-regular: 400;
--adm-font-weight-medium: 500;
--adm-font-weight-bold: 600;

/* Spacing */
--adm-space-xs: 4px;
--adm-space-sm: 8px;
--adm-space-md: 12px;
--adm-space-lg: 16px;
--adm-space-xl: 24px;

/* Border Radius */
--adm-radius-s: 4px;
--adm-radius-m: 8px;
--adm-radius-l: 12px;

/* Hairline Border */
--adm-border-width: 0.5px;  /* Retina 1px */
```

### Component Library

#### Navigation

**NavBar**
```jsx
import { NavBar } from 'antd-mobile'

<NavBar onBack={() => history.back()}>
  Title
</NavBar>
```
- Height: 45px
- Background: #FFFFFF
- Border bottom: 0.5px #E5E5E5

**TabBar**
```jsx
import { TabBar } from 'antd-mobile'

<TabBar activeKey={activeKey} onChange={setActiveKey}>
  <TabBar.Item key="home" icon={<HomeOutline />} title="Home" />
  <TabBar.Item key="user" icon={<UserOutline />} title="Profile" />
</TabBar>
```
- Height: 50px
- Max tabs: 5
- Icon size: 22px

**Tabs**
```jsx
import { Tabs } from 'antd-mobile'

<Tabs activeKey={activeKey} onChange={setActiveKey}>
  <Tabs.Tab title="Tab 1" key="1">Content 1</Tabs.Tab>
  <Tabs.Tab title="Tab 2" key="2">Content 2</Tabs.Tab>
</Tabs>
```

#### Buttons

**Button (Primary)**
```jsx
import { Button } from 'antd-mobile'

<Button color="primary" size="large">
  Continue
</Button>
```
- Height: 45px (large), 35px (medium), 28px (small)
- Padding: 12px horizontal
- Border radius: 8px

**Button (Default)**
```jsx
<Button color="default">
  Cancel
</Button>
```

**Button (Text)**
```jsx
<Button fill="none">
  Learn More
</Button>
```

#### Lists

**List.Item**
```jsx
import { List } from 'antd-mobile'

<List>
  <List.Item
    prefix={<UserOutline />}
    extra="Detail"
    onClick={() => {}}
  >
    Title
  </List.Item>
</List>
```
- Height: 44px minimum
- Padding: 12px horizontal
- Separator: 0.5px hairline

**SwipeAction**
```jsx
import { SwipeAction } from 'antd-mobile'

<SwipeAction
  rightActions={[
    { key: 'delete', text: 'Delete', color: 'danger' }
  ]}
>
  <List.Item>Swipeable Item</List.Item>
</SwipeAction>
```

#### Cards

**Card**
```jsx
import { Card } from 'antd-mobile'

<Card
  title="Card Title"
  extra={<a>More</a>}
>
  Card content...
</Card>
```
- Border radius: 8px
- Padding: 12px
- Shadow: 0 2px 8px rgba(0,0,0,0.08)

#### Forms

**Input**
```jsx
import { Input } from 'antd-mobile'

<Input
  placeholder="Enter text"
  clearable
/>
```
- Height: 44px
- Font size: 15px
- Padding: 0 12px

**TextArea**
```jsx
import { TextArea } from 'antd-mobile'

<TextArea
  placeholder="Enter text"
  rows={3}
  maxLength={200}
  showCount
/>
```

**Picker**
```jsx
import { Picker } from 'antd-mobile'

<Picker
  columns={[
    [
      { label: 'Option 1', value: '1' },
      { label: 'Option 2', value: '2' },
    ]
  ]}
>
  {(items, { open }) => (
    <List.Item onClick={open}>
      {items.every(item => item === null) ? 'Select' : items.map(item => item?.label ?? '').join(' - ')}
    </List.Item>
  )}
</Picker>
```

**Switch**
```jsx
import { Switch } from 'antd-mobile'

<Switch defaultChecked />
```
- Size: 51x31px
- Thumb: 27x27px

**Stepper**
```jsx
import { Stepper } from 'antd-mobile'

<Stepper
  defaultValue={1}
  min={1}
  max={10}
/>
```

#### Feedback

**Toast**
```jsx
import { Toast } from 'antd-mobile'

Toast.show({
  icon: 'success',
  content: 'Operation successful',
  duration: 2000
})
```
- Duration: 2000ms default
- Position: Center
- Max width: 70% of screen

**Dialog**
```jsx
import { Dialog } from 'antd-mobile'

Dialog.confirm({
  title: 'Dialog Title',
  content: 'Dialog content...',
  onConfirm: () => {},
})
```
- Width: 280px
- Border radius: 12px
- Overlay: rgba(0,0,0,0.45)

**ActionSheet**
```jsx
import { ActionSheet } from 'antd-mobile'

ActionSheet.show({
  actions: [
    { text: 'Option 1', key: '1' },
    { text: 'Option 2', key: '2' },
    { text: 'Delete', key: 'delete', danger: true },
  ],
  onAction: (action) => {},
})
```

**Popover**
```jsx
import { Popover } from 'antd-mobile'

<Popover
  content="Popover content"
  trigger="click"
>
  <span>Click me</span>
</Popover>
```

**PullToRefresh**
```jsx
import { PullToRefresh } from 'antd-mobile'

<PullToRefresh onRefresh={async () => {
  await fetchData()
}}>
  <div>{list}</div>
</PullToRefresh>
```

#### Data Display

**Grid**
```jsx
import { Grid } from 'antd-mobile'

<Grid columns={3} gap={8}>
  <Grid.Item>Item 1</Grid.Item>
  <Grid.Item>Item 2</Grid.Item>
  <Grid.Item>Item 3</Grid.Item>
</Grid>
```

**Image**
```jsx
import { Image } from 'antd-mobile'

<Image
  src="https://example.com/image.jpg"
  fit="cover"
  width={200}
  height={200}
  lazy
/>
```

**Badge**
```jsx
import { Badge } from 'antd-mobile'

<Badge content="5">
  <span>Messages</span>
</Badge>
```

**Tag**
```jsx
import { Tag } from 'antd-mobile'

<Tag color="primary">Tag</Tag>
```

### Ant Design Icons

**Icon Library**: `@ant-design/icons`

**Common Icons:**
- `HomeOutline` - Home
- `SearchOutline` - Search
- `UserOutline` - Profile
- `AddOutline` - Add
- `MoreOutline` - More
- `DeleteOutline` - Delete
- `CheckCircleOutline` - Success
- `CloseCircleOutline` - Error

**Usage:**
```jsx
import { HomeOutline } from 'antd-mobile-icons'

<HomeOutline fontSize={24} color="#1677FF" />
```

### Interaction Patterns

- **Tap**: Primary action (300ms delay removed in modern browsers)
- **Long press**: Context menu (hold 500ms)
- **Swipe**: Reveal actions, navigate
- **Pull-to-refresh**: Standard pattern with rubber-band effect

### Accessibility

- **Touch target**: 44x44px minimum
- **Color contrast**: WCAG AA (4.5:1 text)
- **ARIA labels**: Support screen readers
- **Keyboard navigation**: Focus management (for desktop fallback)

---

## Component Mapping

Cross-platform component equivalence table:

| Component Type | WeChat Work | iOS Native | Material Design 3 | Ant Design Mobile |
|----------------|-------------|------------|-------------------|-------------------|
| **Primary Button** | `weui-btn_primary` | `UIButton` (filled) | `MaterialButton` (filled) | `<Button color="primary">` |
| **Secondary Button** | `weui-btn_default` | `UIButton` (tinted) | `MaterialButton` (outlined) | `<Button color="default">` |
| **Text Button** | `weui-btn_plain` | `UIButton` (plain) | `MaterialButton` (text) | `<Button fill="none">` |
| **List Item** | `weui-cell` | `UITableViewCell` | `ListItem` | `<List.Item>` |
| **List Section** | `weui-cells` | `UITableViewSection` | `ListItem` (divider) | `<List>` (grouped) |
| **Input Field** | `weui-input` | `UITextField` | `TextInputLayout` | `<Input>` |
| **Textarea** | `weui-textarea` | `UITextView` | `TextInputLayout` (multiline) | `<TextArea>` |
| **Switch** | `weui-switch` | `UISwitch` | `SwitchMaterial` | `<Switch>` |
| **Checkbox** | `weui-check` | `UIButton` (checkbox) | `MaterialCheckBox` | `<Checkbox>` |
| **Radio** | `weui-radio` | `UIButton` (radio) | `MaterialRadioButton` | `<Radio>` |
| **Picker** | `weui-picker` | `UIPickerView` | `DropdownMenu` | `<Picker>` |
| **Date Picker** | `weui-datetime-picker` | `UIDatePicker` | `DatePicker` | `<DatePicker>` |
| **Action Sheet** | `weui-actionsheet` | `UIAlertController` (actionSheet) | `BottomSheet` | `<ActionSheet>` |
| **Dialog** | `weui-dialog` | `UIAlertController` (alert) | `MaterialAlertDialog` | `<Dialog>` |
| **Toast** | `weui-toast` | Custom `UIView` | `Snackbar` | `<Toast>` |
| **Loading** | `weui-loading` | `UIActivityIndicatorView` | `CircularProgressIndicator` | `<SpinLoading>` |
| **Progress Bar** | `weui-progress` | `UIProgressView` | `LinearProgressIndicator` | `<ProgressBar>` |
| **Search Bar** | `weui-search-bar` | `UISearchBar` | `SearchView` | `<SearchBar>` |
| **Navigation Bar** | `weui-navigation-bar` | `UINavigationBar` | `MaterialToolbar` | `<NavBar>` |
| **Tab Bar** | `weui-tabbar` | `UITabBar` | `BottomNavigationView` | `<TabBar>` |
| **Segmented Control** | `weui-navbar` | `UISegmentedControl` | `TabLayout` | `<Tabs>` |
| **Card** | `weui-panel` | Custom `UIView` | `MaterialCardView` | `<Card>` |
| **Badge** | `weui-badge` | `UITabBarItem` (badge) | `BadgeDrawable` | `<Badge>` |
| **Tag** | `weui-badge` (inline) | Custom `UIView` | `Chip` | `<Tag>` |
| **Avatar** | Custom | Custom `UIImageView` | Custom | `<Avatar>` |
| **Divider** | Custom (border) | `UITableView` separator | `Divider` | `<Divider>` |
| **Floating Button** | Custom | Custom | `FloatingActionButton` | `<FloatingBubble>` |
| **Swipe Actions** | Custom | `UITableView` swipe | `SwipeRefreshLayout` | `<SwipeAction>` |
| **Pull-to-Refresh** | Custom | `UIRefreshControl` | `SwipeRefreshLayout` | `<PullToRefresh>` |
| **Empty State** | Custom | Custom | Custom | `<Empty>` |
| **Skeleton** | Custom | Custom | Custom | `<Skeleton>` |
| **Stepper** | Custom | `UIStepper` | Custom | `<Stepper>` |
| **Slider** | `weui-slider` | `UISlider` | `Slider` | `<Slider>` |
| **Rating** | Custom | Custom | Custom | `<Rate>` |
| **Collapse** | `weui-panel` | `UITableView` (expandable) | `ExpandableListView` | `<Collapse>` |
| **Popover** | `weui-dialog` (half-screen) | `UIPopoverPresentationController` | `Menu` (dropdown) | `<Popover>` |
| **Bottom Sheet** | `weui-half-screen-dialog` | `UIModalPresentationPageSheet` | `BottomSheetDialogFragment` | `<Popup>` (bottom) |

---

## Cross-Platform Considerations

### Platform-Specific Patterns

**iOS:**
- Back button: Top-left with "<" symbol
- Navigation: Hierarchical (drill-down)
- Modals: Bottom-up sheets, centered alerts
- Gestures: Swipe from left edge to go back

**Android:**
- Back button: System button (hardware/software)
- Navigation: Flexible (drawer, tabs, bottom nav)
- Modals: Bottom sheets, dialogs
- Gestures: Swipe from left edge for drawer

**WeChat Work:**
- Back button: Top-left arrow
- Navigation: Tab bar at bottom
- Modals: Centered dialogs, action sheets
- Gestures: Limited (tap, long press, swipe in lists)

**Ant Design Mobile (Web):**
- Back button: Top-left arrow (custom)
- Navigation: Flexible (depends on implementation)
- Modals: Various (dialog, drawer, popup)
- Gestures: Touch events (limited compared to native)

### Responsive Design

**Breakpoints:**

```css
/* Material Design */
@media (min-width: 600px) { /* Tablet */ }
@media (min-width: 905px) { /* Desktop */ }
@media (min-width: 1240px) { /* Large desktop */ }

/* iOS (using size classes) */
/* Compact width: iPhone portrait */
/* Regular width: iPhone landscape, iPad */

/* WeChat Work (fixed viewport) */
/* Single breakpoint at 768px for tablet view */

/* Ant Design Mobile (custom) */
@media (min-width: 768px) { /* Tablet/Desktop fallback */ }
```

### Accessibility Across Platforms

| Feature | iOS | Android | WeChat Work | Ant Design Mobile |
|---------|-----|---------|-------------|-------------------|
| **Screen Reader** | VoiceOver | TalkBack | WeChat built-in | Browser SR |
| **Min Touch Target** | 44x44pt | 48x48dp | 44x44px | 44x44px |
| **Color Contrast** | WCAG AA | WCAG AA | WCAG AA | WCAG AA |
| **Dynamic Type** | ✅ Native | ✅ Native | ⚠️ Limited | ⚠️ Manual |
| **Focus Indicators** | ✅ Auto | ✅ Auto | ❌ Manual | ⚠️ CSS-based |
| **Haptic Feedback** | ✅ UIImpactFeedbackGenerator | ✅ Vibrator | ❌ N/A | ⚠️ Vibration API |

### Performance Considerations

**WeChat Work:**
- Lightweight components (mini program constraints)
- Avoid heavy animations
- Optimize images (<500KB per image)

**iOS Native:**
- Use Auto Layout for flexibility
- Implement lazy loading for lists
- Optimize asset catalogs (1x, 2x, 3x images)

**Material Design:**
- Use RecyclerView for lists (efficient recycling)
- Implement view binding (reduce findViewById calls)
- Optimize overdraw (reduce layout layers)

**Ant Design Mobile:**
- Code splitting (reduce initial bundle)
- Virtual lists for long lists (react-virtualized)
- Optimize images (WebP, lazy loading)

---

## Design System Selection Guide

| Criteria | WeChat Work | iOS Native | Material Design | Ant Design Mobile |
|----------|-------------|------------|-----------------|-------------------|
| **Target Platform** | WeChat ecosystem | Apple devices | Android, Web, cross-platform | Mobile web, Hybrid |
| **Best For** | Enterprise apps, internal tools | Consumer iOS apps | Google-aligned apps, Android-first | Admin panels, data-heavy apps |
| **Development Complexity** | Medium (mini program) | High (native Swift/ObjC) | Medium-High (Kotlin/Java) | Low-Medium (React) |
| **Customization** | Limited | High | High | High |
| **Component Library** | WeUI | UIKit / SwiftUI | Material Components | Ant Design Mobile |
| **Learning Curve** | Low | High | Medium | Low-Medium |
| **Ecosystem** | WeChat only | Apple only | Cross-platform | Cross-platform (web-focused) |

**Decision Tree:**

```
Is the app for WeChat ecosystem?
├─ Yes → WeChat Work
└─ No
    ├─ Is it iOS-exclusive?
    │   └─ Yes → iOS Native (HIG)
    └─ No
        ├─ Is it Android-first or Google-aligned?
        │   └─ Yes → Material Design 3
        └─ No
            ├─ Is it web-based or hybrid?
            │   └─ Yes → Ant Design Mobile
            └─ No → Multi-platform strategy (choose primary)
```

---

For complete prompt template examples, see [examples/prompt-templates.md](../examples/prompt-templates.md).
