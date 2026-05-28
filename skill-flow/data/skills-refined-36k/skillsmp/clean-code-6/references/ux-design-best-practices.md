# UX Design Best Practices

## Core Principles

- **Consistency**: Same component for same function
- **User Expectations**: Follow established patterns
- **Accessibility**: Never disable built-in a11y features
- **Immediate Feedback**: Instant response to user actions
- **Purposeful Design**: Micro-interactions must solve a UX problem
- **Enhance Usability**: Guide, confirm, and inform user actions

---

## Micro-interactions

### Guidelines

- **Consistency over novelty**: Reuse patterns to reinforce brand identity
- **Lightweight & fast**: Keep interactions short (100–500ms)
- **Accessible & inclusive**: Must work for all users, even with animations disabled
- **Clear triggers**: Should be intentional and user-driven

### Feedback Types

| Type     | Examples                       |
| -------- | ------------------------------ |
| Visual   | Color shift, scale, opacity    |
| Auditory | Click sound, notification tone |
| Haptic   | Vibration on mobile            |

### Timing Guidelines

| Duration  | Use Case                      |
| --------- | ----------------------------- |
| 100-200ms | Micro-feedback (button press) |
| 200-300ms | State changes (hover, focus)  |
| 300-500ms | Transitions (page, modal)     |

---

## Component Selection

### Quick Decision Tree

1. **Action type:**
   - Immediate → Switch, Toggle
   - Validation → Checkbox, Radio, Button

2. **Options count:**
   - 1 → Button, Switch
   - 2-5 → Radio Group, Toggle Group
   - 5-15 → Select
   - 15+ → Combobox

3. **Information priority:**
   - Critical → Alert, Alert Dialog
   - Important → Badge, Alert
   - Informative → Toast, Tooltip

4. **Space constraints:**
   - Yes → Accordion, Tabs, Popover
   - No → Standard layout, Cards

5. **Destructive action:**
   - Yes → Alert Dialog with confirmation
   - No → Direct action or Dialog

---

## Buttons & Controls

### Button Variants

| Variant       | Use Case                   |
| ------------- | -------------------------- |
| `default`     | Primary actions            |
| `outline`     | Secondary actions          |
| `destructive` | Dangerous actions (delete) |
| `ghost`       | Tertiary actions           |

**Rules:**

- Avoid >3 buttons side by side
- Use clear, action-oriented text

### Toggle vs Switch

- **Toggle**: Mutually exclusive options
- **Switch**: Binary settings with immediate effect
- **Never**: Use for choices requiring validation

---

## Form Components

### Input

- Placeholder = example format
- Label = description
- Use Input Group for prefixes/suffixes
- Long text → Use Textarea

### Select / Combobox

| Options Count | Component   |
| ------------- | ----------- |
| < 5           | Radio Group |
| 5-15          | Select      |
| 15+           | Combobox    |

### Date Picker

- Localized format
- Disable unavailable dates
- Presets for common values ("Today", "Tomorrow")

### Slider

- Display current value
- Use logical steps (5, 10, 25...)
- Precise values → Use number Input

---

## Navigation

### Navigation Menu

- Max 7±2 items
- Highlight active state
- Responsive hamburger on mobile

### Tabs

- 2-7 sections max
- Short descriptive labels
- Icons + text when helpful
- Don't hide critical content

### Breadcrumb

- Use for hierarchy >3 levels
- Start with "Home"
- Current page non-clickable
- Truncate if too long

### Pagination

- Display "1-10 of 234"
- Items per page options (10, 25, 50)
- Use for >20 items

---

## Feedback & Dialogs

### Alert Types

| Variant       | Use Case               |
| ------------- | ---------------------- |
| `default`     | Informational messages |
| `destructive` | Errors                 |
| `warning`     | Caution messages       |
| `success`     | Confirmations          |

### Toast

- 3-5s duration
- Bottom-right position
- Max 3 simultaneous

### Alert Dialog

- Use for destructive confirmations
- Always include Cancel button
- Focus on safe action

### Dialog

- Modal with backdrop
- Close on Escape and outside click

### Tooltip

- Short explanations (<10 words)
- 500ms delay
- Avoid on mobile

### Popover

- Rich temporary content
- Mini-forms
- Arrow pointing to trigger

---

## Presentation

### Card

- Clear hierarchy (header, body, footer)
- Consistent spacing
- Hover state if clickable

### Table

- Sticky headers
- Pagination for >20 rows
- Avoid on mobile (use Cards)

### Loading States

| Duration  | Component          |
| --------- | ------------------ |
| <2s       | Spinner            |
| >2s       | Progress indicator |
| Structure | Skeleton           |

---

## Mobile Adaptations

| Desktop          | Mobile                   |
| ---------------- | ------------------------ |
| Navigation Menu  | Hamburger menu           |
| Hover            | Touch / Long press       |
| Table            | Cards or list            |
| Sidebar          | Sheet from bottom        |
| Tooltip          | Direct labels            |
| Context Menu     | Long press / action menu |
| Multiple columns | Vertical stack           |

---

## Interaction States

### Button States

1. Default
2. Hover
3. Focused
4. Pressed/Active
5. Disabled

### Form Validation

1. Untouched
2. Focused
3. Valid
4. Invalid
5. Submitting
6. Submitted

---

## Testing Checklist

- [ ] Clarity: Is the purpose clear?
- [ ] Accessibility: Works without animations?
- [ ] Timing: Appropriate duration?
- [ ] Cross-platform: Works on all devices?
- [ ] User tested: Validated with real users?

---

## Anti-Patterns

| Pattern                 | Problem            | Solution                         |
| ----------------------- | ------------------ | -------------------------------- |
| Too many buttons        | Choice paralysis   | Max 3 buttons                    |
| Hidden critical content | Missed information | Show important data upfront      |
| Slow animations         | Feels sluggish     | Keep 100-500ms                   |
| Toast for errors        | Easy to miss       | Use Alert or Alert Dialog        |
| Mobile tooltip          | Not accessible     | Use visible labels               |
| Table on mobile         | Poor UX            | Use Cards                        |
| Long dropdown lists     | Hard to navigate   | Use Combobox with search         |
| Disabled submit         | A11y issues        | Keep enabled, validate on submit |
