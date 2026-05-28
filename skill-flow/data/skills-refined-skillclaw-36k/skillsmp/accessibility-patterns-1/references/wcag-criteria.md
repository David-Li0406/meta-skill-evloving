# WCAG 2.2 Level AA Complete Reference

## 1. Perceivable

### 1.1 Text Alternatives

| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| 1.1.1 Non-text Content | Alt text for images | `alt="descriptive text"` or `alt=""` for decorative |

### 1.2 Time-based Media

| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| 1.2.1 Audio-only/Video-only | Alternatives for prerecorded media | Transcript or audio description |
| 1.2.2 Captions | Captions for prerecorded audio | Synchronized captions |
| 1.2.3 Audio Description | Audio description for prerecorded video | Audio description track |
| 1.2.5 Audio Description (Prerecorded) | Audio description for all prerecorded video | Extended audio description |

### 1.3 Adaptable

| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| 1.3.1 Info and Relationships | Semantic HTML | Use proper heading hierarchy, lists, tables |
| 1.3.2 Meaningful Sequence | Reading order matches visual order | DOM order = visual order |
| 1.3.3 Sensory Characteristics | Don't rely solely on shape, color, size, location | Add text labels |
| 1.3.4 Orientation | Content works in both orientations | Support portrait and landscape |
| 1.3.5 Identify Input Purpose | Autocomplete for personal data | `autocomplete="email"`, etc. |

### 1.4 Distinguishable

| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| 1.4.1 Use of Color | Color not sole means of conveying info | Add icons, text, patterns |
| 1.4.2 Audio Control | Control for auto-playing audio | Pause/stop/mute controls |
| 1.4.3 Contrast (Minimum) | 4.5:1 for text, 3:1 for large text | Verify with contrast checker |
| 1.4.4 Resize Text | 200% zoom support | Use relative units (rem, em) |
| 1.4.5 Images of Text | Use real text, not images | CSS for styling |
| 1.4.10 Reflow | No horizontal scroll at 320px width | Responsive design |
| 1.4.11 Non-text Contrast | 3:1 for UI components | Focus rings, borders, icons |
| 1.4.12 Text Spacing | Supports custom text spacing | Don't clip content |
| 1.4.13 Content on Hover/Focus | Dismissible, hoverable, persistent | Proper tooltips/popovers |

---

## 2. Operable

### 2.1 Keyboard Accessible

| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| 2.1.1 Keyboard | All functionality via keyboard | Tab, Enter, Space, Arrow keys |
| 2.1.2 No Keyboard Trap | Users can navigate away | Proper focus management |
| 2.1.4 Character Key Shortcuts | Single-key shortcuts can be turned off | Settings or modifier keys |

### 2.2 Enough Time

| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| 2.2.1 Timing Adjustable | User can extend time limits | Warning before timeout |
| 2.2.2 Pause, Stop, Hide | Control moving/blinking content | Pause/stop buttons |

### 2.3 Seizures and Physical Reactions

| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| 2.3.1 Three Flashes | No content flashes >3 times/second | Limit animation speed |

### 2.4 Navigable

| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| 2.4.1 Bypass Blocks | Skip navigation links | Skip to main content link |
| 2.4.2 Page Titled | Descriptive page titles | Unique `<title>` per page |
| 2.4.3 Focus Order | Logical tab sequence | DOM order matches visual |
| 2.4.4 Link Purpose | Link text describes destination | Avoid "click here" |
| 2.4.5 Multiple Ways | Multiple ways to find pages | Nav + search + sitemap |
| 2.4.6 Headings and Labels | Descriptive headings | Clear, descriptive text |
| 2.4.7 Focus Visible | Clear focus indicator | Tailwind focus rings |
| 2.4.11 Focus Not Obscured | Focused element not hidden | Check sticky headers |

### 2.5 Input Modalities

| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| 2.5.1 Pointer Gestures | Single-pointer alternative | No multitouch required |
| 2.5.2 Pointer Cancellation | Abort/undo on up-event | Actions on click, not mousedown |
| 2.5.3 Label in Name | Visible label in accessible name | Text matches aria-label |
| 2.5.4 Motion Actuation | Alternative to motion | Button alternative to shake |
| 2.5.7 Dragging Movements | Non-dragging alternative | Click to move option |
| 2.5.8 Target Size | Minimum 24x24px | Touch targets 44x44px recommended |

---

## 3. Understandable

### 3.1 Readable

| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| 3.1.1 Language of Page | Declare page language | `<html lang="en">` |
| 3.1.2 Language of Parts | Declare language changes | `<span lang="fr">` |

### 3.2 Predictable

| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| 3.2.1 On Focus | No unexpected changes | Avoid auto-submit on focus |
| 3.2.2 On Input | No unexpected changes | Warn before auto-submit |
| 3.2.3 Consistent Navigation | Same order across pages | Consistent nav placement |
| 3.2.4 Consistent Identification | Same function = same name | Consistent button labels |
| 3.2.6 Consistent Help | Help in same location | Consistent help placement |

### 3.3 Input Assistance

| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| 3.3.1 Error Identification | Identify errors clearly | aria-invalid, role="alert" |
| 3.3.2 Labels or Instructions | Label all inputs | `<label>` or aria-label |
| 3.3.3 Error Suggestion | Suggest corrections | "Did you mean...?" |
| 3.3.4 Error Prevention | Confirm before submit | Review page for forms |
| 3.3.7 Redundant Entry | Don't require re-entering data | Pre-fill known values |
| 3.3.8 Accessible Authentication | Alternative to cognitive tests | Support password managers |

---

## 4. Robust

### 4.1 Compatible

| Criterion | Requirement | Implementation |
|-----------|-------------|----------------|
| 4.1.2 Name, Role, Value | Expose to assistive tech | ARIA roles, states, properties |
| 4.1.3 Status Messages | Announce without focus | aria-live regions |

---

## TailAdmin Color Contrast Analysis

### Passing Combinations (WCAG AA)

**Text on Light Backgrounds:**
```erb
<p class="text-black bg-white">           <%# 21:1 - Excellent %>
<p class="text-bodydark bg-white">        <%# ~7:1 - Pass %>
<p class="text-primary bg-white">         <%# ~4.7:1 - Pass %>
<p class="text-bodydark2 bg-white">       <%# ~5.5:1 - Pass %>
```

**Text on Dark Backgrounds:**
```erb
<p class="text-white bg-boxdark">         <%# ~12:1 - Excellent %>
<p class="text-bodydark1 bg-boxdark">     <%# ~5:1 - Pass %>
<p class="text-white bg-primary">         <%# ~4.5:1 - Pass %>
```

**Error States:**
```erb
<p class="text-danger bg-white">          <%# ~4.5:1 - Pass %>
<p class="text-meta-1 bg-white">          <%# ~4.5:1 - Pass (danger alias) %>
```

### Verify Custom Colors

Use online tools:
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
- Colour Contrast Analyser (desktop app)
- axe DevTools browser extension
