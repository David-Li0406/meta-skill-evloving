# UX Design Patterns and Standards

## Common UI Patterns

### Navigation Patterns

#### App Shell
Fixed header and sidebar with scrollable main content.
**Use when**: Multi-section applications, dashboards
**Structure**:
- Header: Logo, primary nav, user menu
- Sidebar: Secondary navigation, contextual actions
- Main: Content area
- Footer: Utility links, legal

#### Tabs
Organize related content into separate views.
**Use when**: Grouping related information, settings panels
**Best practices**:
- 3-7 tabs maximum
- Label tabs clearly (1-2 words)
- Indicate active tab visually
- Lazy-load content if heavy

#### Breadcrumbs
Show hierarchical location and enable backward navigation.
**Use when**: Deep hierarchies, multi-level navigation
**Format**: Home > Category > Subcategory > Current
**Best practices**:
- Show full path
- Last item is current page (not clickable)
- Use > or / as separator

### Form Patterns

#### Single Column Form
Vertical stack of form fields.
**Use when**: Most forms (optimal for completion)
**Best practices**:
- One column layout
- Label above field
- Group related fields
- Required field indicators (*)
- Inline validation
- Clear error messages

#### Multi-Step Form (Wizard)
Break long forms into steps.
**Use when**: Forms with 8+ fields or logical sections
**Best practices**:
- Show progress (Step 1 of 3)
- Visual indicator (●―――○―――○)
- Back and Next buttons
- Save progress if possible
- Review step before final submit

#### Inline Editing
Edit content in place without separate form.
**Use when**: Quick edits, table cells, text fields
**Interaction**:
- Click to edit
- Show save/cancel buttons
- Escape key to cancel
- Tab to next field

### List and Table Patterns

#### List-Detail View (Master-Detail)
List on left, details on right.
**Use when**: Email clients, file managers, content browsers
**Responsive**: Stack on mobile (list → detail transition)

#### Infinite Scroll
Load more content as user scrolls.
**Use when**: Continuous feeds, social media, image galleries
**Caution**: Provide "load more" button as alternative
**Footer**: Move footer outside scroll container

#### Pagination
Divide content into pages.
**Use when**: Known content count, need direct access to pages
**Controls**: Previous, 1, 2, 3 ... 10, Next
**Show**: "Showing 1-20 of 100 results"

#### Data Table
Structured tabular data with sorting and filtering.
**Features**:
- Sortable columns (click header)
- Filterable columns
- Row selection (checkboxes)
- Bulk actions
- Responsive: Stack or horizontal scroll

### Modal and Dialog Patterns

#### Modal Dialog
Overlay that requires user action.
**Use when**: Critical decisions, focused tasks, forms
**Best practices**:
- Darken background (scrim)
- Close on backdrop click or Escape
- Focus trap (tab stays in modal)
- Clear "Cancel" option
- Primary action highlighted

#### Drawer/Slideout
Panel that slides from edge of screen.
**Use when**: Settings, filters, secondary actions
**Placement**: Right (most common), Left, Bottom
**Behavior**: Overlay (mobile) or pushes content (desktop)

#### Toast/Snackbar
Temporary notification at bottom/top.
**Use when**: Success confirmations, low-priority alerts
**Duration**: 3-5 seconds
**Action**: Optional "Undo" or "Dismiss"

### Search Patterns

#### Autocomplete Search
Show suggestions as user types.
**Use when**: Large datasets, known queries
**Features**:
- Debounce (300ms)
- Keyboard navigation (arrows, enter)
- Highlight matching text
- Show recent searches
- Category grouping

#### Faceted Search/Filters
Multiple filter dimensions.
**Use when**: E-commerce, content libraries
**Layout**: Sidebar filters + result list
**Features**:
- Applied filters visible
- Clear all filters
- Filter counts (23 results)
- Instant or apply button

### Loading and Feedback Patterns

#### Skeleton Screen
Show content structure while loading.
**Use when**: Known layout, fast perceived performance
**Design**: Gray placeholders matching final content shape

#### Spinner/Progress Indicator
Show loading state.
**Use when**: Unknown duration
**Types**:
- Inline spinner (button/field level)
- Full-screen spinner (page load)
- Progress bar (known duration)

#### Empty State
Show when no data exists.
**Use when**: Lists, search results, new accounts
**Include**:
- Illustration or icon
- Helpful message
- Call-to-action (create first item, learn more)

## Interaction Patterns

### Hover States
Visual feedback on mouse over.
**Elements**: Buttons, links, cards, interactive elements
**Effects**: Color change, underline, shadow, scale

### Focus States
Keyboard navigation indicator.
**Requirement**: WCAG accessibility
**Design**: Visible outline or background color
**Never**: Remove focus indicator without alternative

### Active States
Pressed/clicked feedback.
**Design**: Darker shade, inset shadow
**Duration**: While pressed

### Disabled States
Indicate non-interactive elements.
**Design**: Reduced opacity (0.5), no pointer cursor
**Alternative**: Hide if not contextually relevant

## Responsive Patterns

### Mobile-First Breakpoints
```css
/* Mobile: < 768px (base) */
/* Tablet: 768px - 1024px */
/* Desktop: > 1024px */
```

### Responsive Navigation
- **Mobile**: Hamburger menu
- **Tablet**: Collapsed sidebar or tabs
- **Desktop**: Full horizontal nav or sidebar

### Responsive Tables
- **Mobile**: Stack rows as cards or horizontal scroll
- **Tablet**: Show essential columns only
- **Desktop**: Full table

### Touch Targets
- **Minimum size**: 44x44px (iOS), 48x48px (Material)
- **Spacing**: 8px minimum between targets

## Accessibility Patterns

### Keyboard Navigation
- **Tab**: Move forward through interactive elements
- **Shift+Tab**: Move backward
- **Enter/Space**: Activate buttons
- **Escape**: Close modals/dialogs
- **Arrows**: Navigate lists, menus, tabs

### Screen Reader Support
- **Alt text**: All images and icons
- **ARIA labels**: Interactive elements without visible text
- **ARIA live regions**: Dynamic content updates
- **Heading hierarchy**: Proper H1-H6 structure
- **Landmarks**: header, nav, main, footer, aside

### Color Contrast
- **Normal text**: 4.5:1 minimum (WCAG AA)
- **Large text** (18pt+): 3:1 minimum
- **UI components**: 3:1 for borders/icons
- **Don't**: Rely on color alone to convey information

## Component Library References

### Material Design (Google)
- Comprehensive component library
- Detailed interaction specs
- URL: material.io

### Human Interface Guidelines (Apple)
- iOS and macOS patterns
- Native-feeling designs
- URL: developer.apple.com/design

### Fluent Design (Microsoft)
- Windows and web patterns
- Enterprise-friendly
- URL: microsoft.com/design/fluent

### Bootstrap
- Popular CSS framework
- Pre-built components
- URL: getbootstrap.com

### Tailwind UI
- Utility-first framework
- Modern patterns
- URL: tailwindui.com

## Design Systems

### Building a Design System

**Core Elements**:
1. **Color Palette**: Primary, secondary, neutral, semantic (error, warning, success)
2. **Typography**: Font families, sizes, weights, line heights
3. **Spacing Scale**: 4px, 8px, 16px, 24px, 32px, 48px, 64px
4. **Components**: Buttons, inputs, cards, etc.
5. **Patterns**: Common layouts and interactions
6. **Icons**: Consistent icon set and usage
7. **Documentation**: Usage guidelines

### Design Tokens

```css
/* Color Tokens */
--color-primary: #0066cc;
--color-secondary: #6c757d;
--color-success: #28a745;
--color-danger: #dc3545;
--color-warning: #ffc107;

/* Spacing Tokens */
--space-xs: 4px;
--space-sm: 8px;
--space-md: 16px;
--space-lg: 24px;
--space-xl: 32px;

/* Typography Tokens */
--font-size-sm: 14px;
--font-size-base: 16px;
--font-size-lg: 18px;
--font-weight-normal: 400;
--font-weight-semibold: 600;
--font-weight-bold: 700;
```

## Best Practices

### General UX Principles

1. **Consistency**: Use same patterns throughout
2. **Feedback**: Always respond to user actions
3. **Visibility**: Make status and options clear
4. **Error Prevention**: Validate and warn before destructive actions
5. **Recognition over Recall**: Show options, don't make users remember
6. **Flexibility**: Support different skill levels and shortcuts
7. **Aesthetic and Minimalism**: Remove unnecessary elements

### Form Best Practices

- Label every field clearly
- Mark required fields (*)
- Provide helpful placeholder text
- Validate inline after field loses focus
- Group related fields
- Use appropriate input types (email, tel, date)
- Show password strength meter
- Auto-tab for formatted inputs (credit card, phone)
- Preserve data on errors

### Error Message Best Practices

- **Be specific**: "Email format is invalid" not "Error"
- **Be helpful**: Suggest fix or next step
- **Be polite**: No blame or technical jargon
- **Be visible**: Show near the error, use color + icon
- **Be timely**: Validate early, show errors immediately

### Loading State Best Practices

- Show loading indicator immediately (within 100ms)
- Use skeleton screens for known layouts
- Show progress percentage if known duration
- Provide cancel option for long operations
- Disable submit buttons while loading

### Mobile UX Best Practices

- Larger touch targets (48x48px minimum)
- Thumb-friendly zones (bottom of screen)
- Minimize typing (use pickers, dropdowns)
- Support gestures (swipe, pinch, long-press)
- Test on real devices
- Consider offline states
- Optimize for one-handed use
