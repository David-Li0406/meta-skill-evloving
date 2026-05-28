# Button Component Design Guidelines

## Metadata

- **Timestamp**: 2026-01-10 11:30:00
- **Project**: design-system
- **Category**: Guidelines
- **Tags**: frontend, react, design-system, components, ui
- **Version**: 1.2.0

## Overview

Design guidelines for button components in our design system. Ensures consistent visual design, behavior, and accessibility across all applications.

**Purpose:** Standardize button implementation to maintain brand consistency and improve user experience

**Scope:** All React applications using the design system

**Audience:** Frontend developers, designers, product managers

## Principles

1. **Accessibility First**: Buttons must be keyboard navigable and screen reader friendly
2. **Clarity Over Cleverness**: Button purpose should be immediately clear
3. **Consistency**: Similar actions should look and behave similarly across apps
4. **Responsive**: Buttons should work well on all device sizes

## Guidelines

### Button Variants

#### Guideline 1.1: Primary Buttons

**Description:** Use primary buttons for the main action on a page. Limit to one primary button per view.

**Rationale:** Guides users to the most important action without overwhelming them with choices

**Example:**

```tsx
// Correct: One primary action
<Button variant="primary" onClick={handleSubmit}>
  Submit Application
</Button>

// In a dialog
<DialogActions>
  <Button variant="secondary" onClick={onCancel}>
    Cancel
  </Button>
  <Button variant="primary" onClick={onSave}>
    Save Changes
  </Button>
</DialogActions>
```

**Counter-example:**

```tsx
// Incorrect: Multiple primary buttons compete for attention
<div>
  <Button variant="primary">Save Draft</Button>
  <Button variant="primary">Publish</Button>
  <Button variant="primary">Schedule</Button>
</div>
```

#### Guideline 1.2: Secondary Buttons

**Description:** Use secondary buttons for supporting actions that are less critical than the primary action

**Rationale:** Provides visual hierarchy between actions without removing access to important secondary functions

**Example:**

```tsx
// Correct: Secondary actions clearly differentiated
<FormActions>
  <Button variant="secondary" onClick={onCancel}>
    Cancel
  </Button>
  <Button variant="secondary" onClick={onSaveAsDraft}>
    Save as Draft
  </Button>
  <Button variant="primary" onClick={onPublish}>
    Publish
  </Button>
</FormActions>
```

#### Guideline 1.3: Destructive Actions

**Description:** Use destructive variant for actions that delete data or cannot be easily undone

**Rationale:** Visual warning helps prevent accidental data loss

**Example:**

```tsx
// Correct: Destructive action clearly marked
<Button
  variant="destructive"
  onClick={handleDelete}
  icon={<TrashIcon />}
>
  Delete Account
</Button>

// With confirmation dialog
const [showConfirm, setShowConfirm] = useState(false);

<>
  <Button variant="destructive" onClick={() => setShowConfirm(true)}>
    Delete Project
  </Button>
  {showConfirm && (
    <ConfirmDialog
      message="This action cannot be undone"
      onConfirm={handleDelete}
      onCancel={() => setShowConfirm(false)}
    />
  )}
</>
```

### Button Sizing

#### Guideline 2.1: Size Selection

**Description:** Choose button size based on context and importance

**Rationale:** Size conveys hierarchy and improves touch targets on mobile

**Example:**

```tsx
// Large: Hero sections, critical actions
<Button size="large" variant="primary">
  Get Started Free
</Button>

// Medium (default): Most form actions
<Button size="medium" variant="primary">
  Submit
</Button>

// Small: Compact interfaces, table actions
<Button size="small" variant="secondary" icon={<EditIcon />}>
  Edit
</Button>
```

### Button Labels

#### Guideline 3.1: Action-Oriented Labels

**Description:** Button labels should start with a verb and clearly describe the action

**Rationale:** Users immediately understand what will happen when they click

**Example:**

```tsx
// Correct: Clear action verbs
<Button onClick={handleSave}>Save Changes</Button>
<Button onClick={handleDownload}>Download Report</Button>
<Button onClick={handleInvite}>Send Invitation</Button>
```

**Counter-example:**

```tsx
// Incorrect: Vague or generic labels
<Button onClick={handleSave}>OK</Button>
<Button onClick={handleDownload}>Click Here</Button>
<Button onClick={handleInvite}>Submit</Button>
```

#### Guideline 3.2: Label Length

**Description:** Keep button labels concise (1-3 words). For longer descriptions, use tooltips

**Rationale:** Short labels are easier to scan and fit better in responsive layouts

**Example:**

```tsx
// Correct: Concise with tooltip for details
<Tooltip content="Creates a new project and redirects to the editor">
  <Button variant="primary">New Project</Button>
</Tooltip>
```

### Loading and Disabled States

#### Guideline 4.1: Loading State

**Description:** Show loading indicator for async actions, disable button during loading

**Rationale:** Provides feedback and prevents duplicate submissions

**Example:**

```tsx
// Correct: Loading state with spinner
<Button
  variant="primary"
  onClick={handleSubmit}
  loading={isSubmitting}
  disabled={isSubmitting}
>
  {isSubmitting ? 'Saving...' : 'Save Changes'}
</Button>
```

#### Guideline 4.2: Disabled State

**Description:** Use disabled state only when an action is temporarily unavailable. Provide explanation via tooltip

**Rationale:** Users understand why they can't interact rather than being frustrated

**Example:**

```tsx
// Correct: Disabled with explanation
<Tooltip content="Fill in all required fields to continue">
  <Button
    variant="primary"
    disabled={!isFormValid}
  >
    Submit
  </Button>
</Tooltip>
```

**Counter-example:**

```tsx
// Incorrect: Disabled without explanation
<Button variant="primary" disabled={!isFormValid}>
  Submit
</Button>
```

## Visual Examples

### Component: Button

**Usage:**
- Use for actions that change application state
- Use for navigation to different pages or sections
- Use for submitting forms or triggering operations

**Don't use for:**
- Navigation that should be links (`<a>` tag for SEO)
- Displaying information (use labels or badges)
- Passive content (use text or cards)

**Variants:**

- **primary**: Main action (blue, high contrast)
- **secondary**: Supporting actions (gray, medium contrast)
- **destructive**: Delete or dangerous actions (red, high contrast)
- **ghost**: Subtle actions (transparent, low contrast)

**Properties:**

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| variant | 'primary' \| 'secondary' \| 'destructive' \| 'ghost' | 'primary' | Visual style |
| size | 'small' \| 'medium' \| 'large' | 'medium' | Button size |
| loading | boolean | false | Shows loading spinner |
| disabled | boolean | false | Disables interaction |
| fullWidth | boolean | false | Expands to container width |
| icon | ReactNode | undefined | Optional icon (before text) |
| iconPosition | 'left' \| 'right' | 'left' | Icon placement |

**Code Example:**

```tsx
import { Button } from '@company/design-system';
import { SaveIcon, TrashIcon } from '@company/icons';

function ExampleForm() {
  const [loading, setLoading] = useState(false);

  return (
    <form onSubmit={handleSubmit}>
      {/* Primary action */}
      <Button
        variant="primary"
        type="submit"
        loading={loading}
        icon={<SaveIcon />}
      >
        Save Changes
      </Button>

      {/* Secondary action */}
      <Button
        variant="secondary"
        onClick={handleCancel}
      >
        Cancel
      </Button>

      {/* Destructive action */}
      <Button
        variant="destructive"
        onClick={handleDelete}
        icon={<TrashIcon />}
      >
        Delete
      </Button>
    </form>
  );
}
```

## Exceptions

**Marketing landing pages:**
- May use multiple primary buttons if A/B testing shows improved conversion
- Must maintain visual hierarchy through size/placement

**Complex workflows:**
- May use different color schemes if brand guidelines require it
- Must maintain accessibility contrast ratios (WCAG AA minimum)

**Mobile apps:**
- Minimum touch target size 44x44px overrides small button size
- May use icon-only buttons if space constrained (with aria-label)

## Enforcement

**Automated tools:**
- ESLint rule: `require-button-variant` ensures variant prop specified
- Storybook: Visual regression testing for all button variants
- a11y testing: Automated contrast and keyboard navigation checks

**Code review checklist:**
- [ ] Button variant appropriate for action importance?
- [ ] Label is action-oriented and concise?
- [ ] Loading/disabled states handled correctly?
- [ ] Tooltips provided for disabled states?
- [ ] Only one primary button per view?

**CI/CD gates:**
- Storybook build must pass
- a11y tests must pass (0 violations)
- Visual diff approval required for button changes

## Evolution

**Process for proposing changes:**

1. Create RFC document with rationale and examples
2. Present to design system working group
3. Prototype in Storybook with real examples
4. Gather feedback from 3+ teams
5. Update guidelines and version number
6. Announce in #design-system Slack channel

**Recent changes:**

- v1.2.0 (2026-01-10): Added `iconPosition` prop
- v1.1.0 (2025-12-15): Added `ghost` variant for subtle actions
- v1.0.0 (2025-11-01): Initial design system release

## References

- [WCAG 2.1 Button Guidelines](https://www.w3.org/WAI/WCAG21/Understanding/name-role-value.html)
- [Material Design: Buttons](https://m3.material.io/components/buttons/overview)
- Internal: Brand Guidelines v3.0 (Figma)
- Internal: Accessibility Checklist (Confluence)
