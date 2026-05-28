---
id: consistency-standards
name: "Consistency and Standards"
domain: UX
skill: faion-ux-ui-designer
category: "ux-design"
---

# Consistency and Standards

## Metadata
- **Category:** UX / Usability Heuristic #4
- **Difficulty:** Beginner
- **Tags:** #methodology #ux #heuristics #nielsen-norman #consistency
- **Agent:** faion-usability-agent

---

## Problem

The same action works differently in different parts of the application. Buttons look different but do the same thing. Icons mean different things on different screens. Users must relearn the interface for each section. What works in one place fails in another.

Without consistency:
- Increased learning curve
- User confusion
- Errors from wrong expectations
- Reduced efficiency

---

## The Heuristic

**Usability Heuristic #4:** Users should not have to wonder whether different words, situations, or actions mean the same thing. Follow platform and industry conventions.

---

## Framework

### Types of Consistency

| Type | Description | Example |
|------|-------------|---------|
| **Internal** | Within your product | Same button style everywhere |
| **External** | With platform/industry | Standard icons, patterns |
| **Visual** | Appearance | Colors, typography, spacing |
| **Functional** | Behavior | Same gesture = same result |
| **Verbal** | Language | Consistent terminology |

### Consistency Hierarchy

```
1. Industry conventions (highest priority)
2. Platform conventions
3. Product family conventions
4. Internal application conventions
```

When in doubt, follow conventions at a higher level.

---

## Implementation Patterns

### Visual Consistency

**Colors:**
```
Primary action: Always blue (#0066CC)
Destructive action: Always red (#CC0000)
Success: Always green (#00CC66)
Warning: Always yellow (#FFCC00)
```

**Typography:**
```
Headings: Font family, sizes, weights defined
Body: Consistent size and line height
Links: Underlined or color differentiated
```

**Spacing:**
```
Base unit: 8px
Margins: Multiples of base (8, 16, 24, 32)
Consistent padding in components
```

### Functional Consistency

**Navigation:**
```
Logo click: Always goes to home
Back button: Always goes to previous page
Search: Always in top area
Menu: Consistent position and behavior
```

**Interactions:**
```
Single click: Select
Double click: Open/edit
Long press: Context menu
Swipe: Delete or archive
```

### Verbal Consistency

**Action terms:**
```
Create → Create (not Add, New, Insert)
Delete → Delete (not Remove, Trash, Erase)
Edit → Edit (not Modify, Change, Update)
Save → Save (not Store, Apply, Confirm)
```

**Status terms:**
```
Success → Success (not Done, Complete, OK)
Error → Error (not Failed, Problem, Issue)
Loading → Loading (not Processing, Please wait)
```

---

## Templates

### Consistency Audit

```markdown
# Consistency Audit: [Product]

**Date:** [Date]
**Reviewer:** [Name]

## Visual Consistency

| Element | Consistent? | Variations Found | Recommendation |
|---------|-------------|------------------|----------------|
| Primary buttons | Y/N | [Variations] | [Standard] |
| Typography | Y/N | [Variations] | [Standard] |
| Spacing | Y/N | [Variations] | [Standard] |
| Colors | Y/N | [Variations] | [Standard] |
| Icons | Y/N | [Variations] | [Standard] |

## Functional Consistency

| Action | Consistent? | Variations | Recommendation |
|--------|-------------|------------|----------------|
| [Action] | Y/N | [Where different] | [Standard] |

## Terminology Consistency

| Concept | Terms Used | Recommended Term |
|---------|------------|------------------|
| [Concept] | [Term1, Term2] | [Chosen term] |

## Platform Convention Compliance

| Convention | Followed? | Notes |
|------------|-----------|-------|
| Standard icons | Y/N | [Notes] |
| Platform navigation | Y/N | [Notes] |
| Gesture behavior | Y/N | [Notes] |

## Summary
- Total inconsistencies found: [X]
- Critical: [X]
- Minor: [X]
```

### Design System Component

```markdown
# Component: Button

## Variants

| Variant | Use Case | Appearance |
|---------|----------|------------|
| Primary | Main action | Blue, filled |
| Secondary | Alternative action | Blue, outlined |
| Destructive | Delete/remove | Red, filled |
| Ghost | Tertiary action | Text only |

## Sizes

| Size | Padding | Font Size | Use Case |
|------|---------|-----------|----------|
| Small | 8px 12px | 14px | Dense UIs |
| Medium | 12px 16px | 16px | Default |
| Large | 16px 24px | 18px | Primary CTAs |

## States

| State | Visual Change |
|-------|---------------|
| Default | Standard appearance |
| Hover | Slightly darker |
| Active | Even darker, pressed |
| Disabled | Grayed out, 50% opacity |
| Loading | Spinner replaces text |

## Usage Rules
- One primary button per view
- Use consistent placement (right side for forms)
- Loading state for async actions
```

---

## Examples

### Good Examples

**iOS Platform:**
- Back button always in top-left
- Swipe from edge to go back
- Pull to refresh
- Tab bar at bottom

**Google Products:**
- Consistent Material Design
- Same search pattern
- Same account menu
- Shared iconography

### Bad Examples

**Inconsistent terminology:**
```
Page 1: [Save]
Page 2: [Submit]
Page 3: [Done]
Same action, different labels
```

**Inconsistent layout:**
```
Page 1: [Cancel] [Save]
Page 2: [Save] [Cancel]
Button order reversed
```

---

## Building a Design System

### Components to Standardize

1. **Typography** - Font families, sizes, weights
2. **Colors** - Palette with usage rules
3. **Spacing** - Grid and spacing system
4. **Buttons** - All variants and states
5. **Form elements** - Inputs, selects, checkboxes
6. **Navigation** - Menus, tabs, breadcrumbs
7. **Cards** - Content containers
8. **Modals** - Dialogs and overlays
9. **Feedback** - Alerts, toasts, errors
10. **Icons** - Consistent icon set

### Documentation Requirements

For each component:
- Visual examples
- Usage guidelines
- Do's and don'ts
- Code examples
- Accessibility notes

---

## Common Mistakes

1. **Reinventing patterns** - Custom when standard exists
2. **Inconsistent naming** - Multiple terms for same thing
3. **Design drift** - Changes without updating system
4. **No design system** - Each page designed independently
5. **Platform violations** - Breaking expected behavior

---

## Measuring Consistency

| Metric | How to Measure |
|--------|----------------|
| Component variations | Count distinct styles for same component |
| Terminology variations | Count different terms for same concept |
| Task completion | Compare across different areas |
| User errors | Errors from inconsistent UI |

---

## Checklist

- [ ] Design system documented
- [ ] Components used consistently
- [ ] Terminology glossary exists
- [ ] Platform conventions followed
- [ ] Visual hierarchy consistent
- [ ] Interaction patterns consistent
- [ ] Error handling consistent
- [ ] Regular consistency audits conducted

---

## References

- UX research community: 10 Usability Heuristics
- Atomic Design by Brad Frost
- Design System Best Practices