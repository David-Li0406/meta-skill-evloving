# Kobalte Primitives Catalog

Complete reference of all 30 Kobalte primitives for matching user descriptions to the right component.

## How to Use This Guide

When a user describes a component, scan this catalog to find matching keywords and descriptions. Suggest the top 3 matches with confidence scores:
- **Exact name match:** 100% confidence
- **Keyword match:** 70% confidence
- **Description similarity:** 40% confidence

---

## Form Controls

### Button
**Import:** `@kobalte/core/button`
**Component:** `Button`
**Element:** `button`
**Complexity:** Simple (single component)
**Keywords:** click, action, cta, submit, press

Interactive button element with built-in accessibility (keyboard navigation, ARIA attributes).

**Usage:** Any clickable action - submit buttons, CTAs, toolbar actions

---

### Checkbox
**Import:** `@kobalte/core/checkbox`
**Component:** `Checkbox`
**Element:** `div`
**Complexity:** Composite
**Keywords:** check, toggle, select, form, input

Checkbox input with label and validation support.

**Sub-components:** Root, Input, Control, Indicator, Label, Description, ErrorMessage

**Usage:** Multi-select options, boolean settings, form fields

---

### Radio Group
**Import:** `@kobalte/core/radio-group`
**Component:** `RadioGroup`
**Element:** `div`
**Complexity:** Composite
**Keywords:** radio, choice, select, option, form

Group of radio buttons for single selection from multiple options.

**Sub-components:** Root, Item, ItemInput, ItemControl, ItemIndicator, ItemLabel, ItemDescription, Label, Description, ErrorMessage

**Usage:** Single selection from 2-7 options (use Select for more)

---

### Switch
**Import:** `@kobalte/core/switch`
**Component:** `Switch`
**Element:** `div`
**Complexity:** Composite
**Keywords:** toggle, on, off, boolean, checkbox

Toggle switch for binary on/off state.

**Sub-components:** Root, Input, Control, Thumb, Label, Description, ErrorMessage

**Usage:** Settings toggles, enable/disable features, binary choices

---

### Text Field
**Import:** `@kobalte/core/text-field`
**Component:** `TextField`
**Element:** `div`
**Complexity:** Composite
**Keywords:** input, form, text, email, password, number

Text input field with label, description, and error handling.

**Sub-components:** Root, Input, TextArea, Label, Description, ErrorMessage

**Usage:** Text inputs, email fields, passwords, text areas

---

### Select
**Import:** `@kobalte/core/select`
**Component:** `Select`
**Element:** `div`
**Complexity:** Composite
**Keywords:** dropdown, picker, choose, option, menu

Dropdown select with accessible keyboard navigation.

**Sub-components:** Root, Trigger, Value, Icon, Portal, Content, Listbox, Item, ItemLabel, ItemIndicator

**Usage:** Single selection from many options (7+ items)

---

### Combobox
**Import:** `@kobalte/core/combobox`
**Component:** `Combobox`
**Element:** `div`
**Complexity:** Composite
**Keywords:** autocomplete, search, select, filter, typeahead

Searchable select with autocomplete functionality.

**Sub-components:** Root, Control, Input, Trigger, Icon, Portal, Content, Listbox, Item, ItemLabel, ItemIndicator, ItemDescription

**Usage:** Searchable dropdowns, autocomplete inputs, filterable lists

---

### Slider
**Import:** `@kobalte/core/slider`
**Component:** `Slider`
**Element:** `div`
**Complexity:** Composite
**Keywords:** range, number, track, value, input

Range slider for numeric value selection.

**Sub-components:** Root, Track, Fill, Thumb, Input, Label, ValueLabel, Description

**Usage:** Volume controls, price ranges, numeric settings

---

## Overlays & Dialogs

### Dialog
**Import:** `@kobalte/core/dialog`
**Component:** `Dialog`
**Element:** `div`
**Complexity:** Composite
**Keywords:** modal, popup, overlay, window, lightbox

Modal dialog with overlay and focus management.

**Sub-components:** Root, Trigger, Portal, Overlay, Content, Title, Description, CloseButton

**Usage:** Forms, detailed views, confirmations, any content requiring focus

---

### Alert Dialog
**Import:** `@kobalte/core/alert-dialog`
**Component:** `AlertDialog`
**Element:** `div`
**Complexity:** Composite
**Keywords:** confirm, alert, warning, modal, message

Alert dialog for important confirmations (destructive actions).

**Sub-components:** Root, Trigger, Portal, Overlay, Content, Title, Description, CloseButton

**Usage:** Delete confirmations, destructive action warnings, critical decisions

---

### Popover
**Import:** `@kobalte/core/popover`
**Component:** `Popover`
**Element:** `div`
**Complexity:** Composite
**Keywords:** popup, tooltip, overlay, dropdown, menu

Contextual popover with smart positioning.

**Sub-components:** Root, Anchor, Trigger, Portal, Content, Arrow, Title, Description, CloseButton

**Usage:** Contextual menus, form helpers, additional info panels

---

### Tooltip
**Import:** `@kobalte/core/tooltip`
**Component:** `Tooltip`
**Element:** `div`
**Complexity:** Composite
**Keywords:** hint, help, info, popup, description

Tooltip with hover and focus triggers.

**Sub-components:** Root, Trigger, Portal, Content, Arrow

**Usage:** Icon explanations, hints, supplementary information

---

### Hover Card
**Import:** `@kobalte/core/hover-card`
**Component:** `HoverCard`
**Element:** `div`
**Complexity:** Composite
**Keywords:** preview, popup, hover, card, info

Rich content card that appears on hover.

**Sub-components:** Root, Trigger, Portal, Content, Arrow

**Usage:** User previews, link previews, rich hover content

---

## Menus

### Dropdown Menu
**Import:** `@kobalte/core/dropdown-menu`
**Component:** `DropdownMenu`
**Element:** `div`
**Complexity:** Composite
**Keywords:** menu, actions, list, options, dropdown

Dropdown menu with nested items and keyboard navigation.

**Sub-components:** Root, Trigger, Portal, Content, Arrow, Item, ItemLabel, ItemDescription, ItemIndicator, Group, GroupLabel, Separator, Sub, SubTrigger, SubContent

**Usage:** Action menus, user menus, option lists

---

### Context Menu
**Import:** `@kobalte/core/context-menu`
**Component:** `ContextMenu`
**Element:** `div`
**Complexity:** Composite
**Keywords:** right-click, menu, actions, options

Right-click context menu.

**Sub-components:** Root, Trigger, Portal, Content, Arrow, Item, ItemLabel, ItemDescription, ItemIndicator, Group, GroupLabel, Separator, Sub, SubTrigger, SubContent

**Usage:** Right-click actions, contextual options

---

### Menubar
**Import:** `@kobalte/core/menubar`
**Component:** `Menubar`
**Element:** `div`
**Complexity:** Composite
**Keywords:** menu, navigation, toolbar, app-menu

Application menubar with dropdowns (like desktop app menus).

**Sub-components:** Root, Menu, Trigger, Portal, Content, Arrow, Item, ItemLabel, ItemDescription, ItemIndicator, Group, GroupLabel, Separator, Sub, SubTrigger, SubContent

**Usage:** App-level navigation, desktop-style menu bars

---

## Navigation

### Tabs
**Import:** `@kobalte/core/tabs`
**Component:** `Tabs`
**Element:** `div`
**Complexity:** Composite
**Keywords:** tab, panel, navigation, switch, view

Tab navigation with associated panels.

**Sub-components:** Root, List, Trigger, Indicator, Content

**Usage:** Switching between views, settings panels, multi-step forms

---

### Breadcrumbs
**Import:** `@kobalte/core/breadcrumbs`
**Component:** `Breadcrumbs`
**Element:** `nav`
**Complexity:** Composite
**Keywords:** navigation, path, trail, hierarchy

Breadcrumb navigation trail showing current location.

**Sub-components:** Root, Link, Separator

**Usage:** Hierarchical navigation, page location indicators

---

### Navigation Menu
**Import:** `@kobalte/core/navigation-menu`
**Component:** `NavigationMenu`
**Element:** `nav`
**Complexity:** Composite
**Keywords:** nav, menu, navigation, site-nav, header

Site navigation menu with mega menu support.

**Sub-components:** Root, Menu, Trigger, Icon, Portal, Viewport, Content, Item, Link, Label, Description

**Usage:** Main site navigation, header menus, mega menus

---

### Pagination
**Import:** `@kobalte/core/pagination`
**Component:** `Pagination`
**Element:** `nav`
**Complexity:** Composite
**Keywords:** pager, pages, navigation, list

Pagination navigation for multi-page content.

**Sub-components:** Root, Item, Previous, Next, Ellipsis

**Usage:** Table pagination, search results, multi-page lists

---

### Link
**Import:** `@kobalte/core/link`
**Component:** `Link`
**Element:** `a`
**Complexity:** Simple
**Keywords:** anchor, href, url, navigation, hyperlink

Accessible link component with router integration support.

**Usage:** Navigation links, external links, anchor links

---

## Disclosure & Layout

### Accordion
**Import:** `@kobalte/core/accordion`
**Component:** `Accordion`
**Element:** `div`
**Complexity:** Composite
**Keywords:** collapse, expand, toggle, disclosure, faq

Collapsible accordion panels (multiple items).

**Sub-components:** Root, Item, ItemTrigger, ItemContent, Header

**Usage:** FAQs, collapsible sections, grouped content

---

### Collapsible
**Import:** `@kobalte/core/collapsible`
**Component:** `Collapsible`
**Element:** `div`
**Complexity:** Composite
**Keywords:** collapse, expand, toggle, show, hide

Single collapsible content section.

**Sub-components:** Root, Trigger, Content

**Usage:** "Show more" sections, expandable details, reveal content

---

### Separator
**Import:** `@kobalte/core/separator`
**Component:** `Separator`
**Element:** `hr`
**Complexity:** Simple
**Keywords:** divider, line, hr, border, split

Visual and semantic separator/divider.

**Usage:** Section dividers, menu separators, content breaks

---

## Feedback & Status

### Alert
**Import:** `@kobalte/core/alert`
**Component:** `Alert`
**Element:** `div`
**Complexity:** Simple
**Keywords:** message, notification, warning, error, info

Alert message with ARIA live region for screen readers.

**Usage:** Status messages, notifications, inline alerts

---

### Progress
**Import:** `@kobalte/core/progress`
**Component:** `Progress`
**Element:** `div`
**Complexity:** Composite
**Keywords:** loading, bar, indicator, status, percentage

Progress indicator with determinate/indeterminate states.

**Sub-components:** Root, Track, Fill, Label, ValueLabel

**Usage:** Loading states, upload progress, task completion

---

## Other Components

### Toggle Button
**Import:** `@kobalte/core/toggle-button`
**Component:** `ToggleButton`
**Element:** `button`
**Complexity:** Simple
**Keywords:** toggle, press, button, state, on-off

Button that toggles between pressed/unpressed states.

**Usage:** Formatting toolbars (bold/italic), view toggles, state buttons

---

### Toggle Group
**Import:** `@kobalte/core/toggle-group`
**Component:** `ToggleGroup`
**Element:** `div`
**Complexity:** Composite
**Keywords:** toggle, group, button-group, segmented-control

Group of toggle buttons (single or multiple selection).

**Sub-components:** Root, Item, ItemLabel

**Usage:** View switchers, segmented controls, filter groups

---

### Toolbar
**Import:** `@kobalte/core/toolbar`
**Component:** `Toolbar`
**Element:** `div`
**Complexity:** Composite
**Keywords:** actions, buttons, controls, editor

Toolbar with button controls and keyboard navigation.

**Sub-components:** Root, Button, ToggleButton, Separator

**Usage:** Editor toolbars, action bars, control panels

---

### Image
**Import:** `@kobalte/core/image`
**Component:** `Image`
**Element:** `div`
**Complexity:** Composite
**Keywords:** img, picture, photo, graphic

Image component with fallback support.

**Sub-components:** Root, Img, Fallback

**Usage:** User avatars, product images, any image with fallback

---

## Quick Reference by Use Case

**Need a button?** → Button, Toggle Button
**Need a form control?** → TextField, Select, Checkbox, Radio Group, Switch, Slider, Combobox
**Need a modal/overlay?** → Dialog, Alert Dialog, Popover
**Need a menu?** → Dropdown Menu, Context Menu, Menubar
**Need navigation?** → Tabs, Breadcrumbs, Navigation Menu, Pagination, Link
**Need collapsible content?** → Accordion, Collapsible
**Need feedback?** → Alert, Progress, Tooltip
**Need a toolbar?** → Toolbar, Toggle Group

## Complexity Legend

- **Simple:** Single component, use `simple-component.tsx.template`
- **Composite:** Multiple sub-components, requires namespace exports, may need custom template
