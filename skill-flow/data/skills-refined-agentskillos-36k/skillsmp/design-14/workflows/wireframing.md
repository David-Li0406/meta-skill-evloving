# Wireframing Workflow

Create low-fidelity wireframes to establish layout, information architecture, and component structure.

## When to Use

- During Feature-Refinement at Story_And_Design_Start node
- After feature PRD is approved (F01-feature-prd.md exists)
- Before high-fidelity prototyping
- When exploring multiple layout options
- For communicating structure to developers

## Prerequisites

**Required artifacts**:
- F01-feature-prd.md - Feature specification
- D06-stakeholder-insights.md (optional) - User requirements

**Optional context**:
- Existing design system documentation
- F02-user-stories.md - User stories (if available)
- Similar features for reference

## Workflow Steps

### 1. Review Requirements

Read the feature PRD to understand:
- User needs and goals
- Key features and functionality
- Acceptance criteria
- Constraints and requirements

### 2. Identify Key Screens and States

List all screens/views needed:
- Entry points (how users arrive)
- Primary interactions (core workflows)
- Success states (task completion)
- Error states (validation, failures)
- Empty states (no data)
- Loading states (async operations)

### 3. Establish Information Architecture

For each screen, define:
- **Primary content**: Main focus and information
- **Secondary content**: Supporting information
- **Navigation elements**: How users move between screens
- **Actions**: Buttons, forms, interactive elements
- **Feedback**: Confirmation messages, error handling

### 4. Define Layout Structure

Sketch layout using standard patterns:

**Common Layouts**:
- **App Shell**: Header, sidebar, main content, footer
- **Dashboard**: Cards/widgets in grid layout
- **List-Detail**: Master list with detail panel
- **Wizard/Stepper**: Multi-step process
- **Modal/Dialog**: Overlay interaction

**Responsive Considerations**:
- Mobile layout (< 768px)
- Tablet layout (768px - 1024px)
- Desktop layout (> 1024px)

### 5. Design Each Wireframe

For each screen, create wireframe showing:

**Elements to Include**:
- Content blocks (labeled placeholders)
- Navigation elements (menu, breadcrumbs, tabs)
- Form fields (with labels and types)
- Buttons and CTAs (with labels)
- Interactive elements (dropdowns, toggles, etc.)
- Annotations (notes about behavior)

**Fidelity Level**:
- Use boxes and placeholders for content
- Use Lorem ipsum or realistic placeholder text
- Show hierarchy through size and spacing
- No colors or final styling (low-fidelity)

### 6. Map User Flows

Connect wireframes to show:
- Primary user journey (happy path)
- Alternative paths (different choices)
- Error handling flows
- Navigation between screens

Use arrows and annotations to show transitions.

### 7. Annotate Interactions

Add notes explaining:
- Click/tap behavior
- Form validation rules
- Dynamic content updates
- State changes
- Edge cases

### 8. Document Accessibility Considerations

Note requirements for:
- Keyboard navigation flow
- Screen reader announcements
- Focus management
- Color contrast (even in wireframes)
- Alternative text for images/icons

### 9. Create Wireframe Documentation

Document wireframes in F07-wireframes.md:

```markdown
# Wireframes: [Feature Name]

## Overview
- Feature: [name from PRD]
- User Goals: [primary objectives]
- Key Screens: [list of screens designed]

## Screen Inventory

1. [Screen 1 Name]
2. [Screen 2 Name]
3. [Screen 3 Name]
...

---

## Screen 1: [Screen Name]

### Purpose
[What this screen enables users to do]

### Layout Structure
[Describe the layout pattern used]

### Wireframe

[Option A: ASCII wireframe]
```
+--------------------------------------------------+
|  Header                                    [User]|
+--------------------------------------------------+
|  [Logo]  Nav1  Nav2  Nav3              [Search] |
+--------------------------------------------------+
|                                                  |
|  +--------------------+  +---------------------+ |
|  | Primary Content    |  | Sidebar             | |
|  |                    |  |                     | |
|  | [Title]            |  | [Filter Options]    | |
|  | [Description]      |  | - Option 1          | |
|  | [Image Placeholder]|  | - Option 2          | |
|  |                    |  | - Option 3          | |
|  | [CTA Button]       |  |                     | |
|  +--------------------+  +---------------------+ |
|                                                  |
+--------------------------------------------------+
|  Footer: Links | Privacy | Contact              |
+--------------------------------------------------+
```

[Option B: Detailed description]
The screen uses an app shell layout with:
- **Header**: Logo (left), primary navigation (center), user menu (right)
- **Main Content**: Left column (70%) with card containing title, description, image, and CTA
- **Sidebar**: Right column (30%) with filter options as checkboxes
- **Footer**: Standard links

### Components

#### Header
- Logo: Links to home
- Navigation: [Nav1], [Nav2], [Nav3]
- User Menu: Dropdown with profile, settings, logout

#### Main Content Card
- Title: [H1, max 60 characters]
- Description: [Paragraph, max 200 words]
- Image: [16:9 aspect ratio, alt text required]
- CTA Button: "[Action Text]" (primary style)

#### Sidebar Filters
- Section Title: "Filter By"
- Options: Checkboxes for Option 1, 2, 3
- Apply Button: Updates main content

### Interactions

1. **Filter Selection**:
   - User clicks checkbox
   - "Apply Filters" button activates
   - Click "Apply" → Main content updates with filtered results

2. **CTA Button**:
   - Click → Navigate to [Screen 2]
   - Loading state: Button shows spinner

3. **Navigation**:
   - Click nav item → Navigate to respective section
   - Current page highlighted in nav

### States

- **Default**: All content loaded, no filters applied
- **Loading**: Skeleton UI while data fetches
- **Empty**: "No results found" message with reset filters option
- **Error**: Error banner with retry action

### Accessibility

- **Keyboard Navigation**: Tab order: Header → Main content → Sidebar → Footer
- **Screen Reader**: Announce "Main content updated" when filters applied
- **Focus**: Visible focus indicator on all interactive elements
- **ARIA**: Filters use proper checkbox roles and labels

### Responsive Behavior

- **Mobile (< 768px)**: Sidebar moves below main content, filters in collapsible accordion
- **Tablet (768-1024px)**: Same two-column layout, slightly narrower
- **Desktop (> 1024px)**: Full layout as shown

### Notes
- [Any additional context or decisions]

---

## Screen 2: [Next Screen Name]
[Repeat structure above]

---

## User Flows

### Primary Flow: [Flow Name]

1. **[Screen 1]** → User [action] → **[Screen 2]**
2. **[Screen 2]** → User [action] → **[Screen 3]**
3. **[Screen 3]** → [Success state]

### Alternative Flow: [Flow Name]
[Same structure]

### Error Handling Flow
[Same structure]

---

## Design Decisions

### Decision 1: [Layout Choice]
**Decision**: Chose [option A] over [option B]
**Rationale**: [Why this choice better serves user needs]
**Trade-offs**: [What we're giving up]

### Decision 2: [Another Decision]
[Same structure]

---

## Open Questions

1. [Question requiring stakeholder input]
2. [Question for technical feasibility]

---

## Next Steps

- [ ] Review wireframes with ProductManager
- [ ] Validate flows with stakeholders
- [ ] Create high-fidelity prototype
- [ ] Conduct usability testing
```

### 10. Store Artifact

Save wireframes:
```bash
/home/jwwelbor/projects/ai-dev-team/docs/workflow/artifacts/F07-wireframes.md
```

Optional: Create interactive HTML wireframe using frontend-design skill.

## Wireframe Templates

### Dashboard Screen Template

```
+--------------------------------------------------+
| [App Name]    Dashboard    Reports    Settings  |
+--------------------------------------------------+
| Summary Metrics                                  |
| +----------+ +----------+ +----------+ +--------+|
| | Metric 1 | | Metric 2 | | Metric 3 | | M4   | |
| | [Value]  | | [Value]  | | [Value]  | | [Val]| |
| | [Change] | | [Change] | | [Change] | | [Chg]| |
| +----------+ +----------+ +----------+ +--------+|
|                                                  |
| Recent Activity                  Quick Actions  |
| +-------------------------+  +----------------+ |
| | [Item 1]     [Time]     |  | [Action 1]     | |
| | [Item 2]     [Time]     |  | [Action 2]     | |
| | [Item 3]     [Time]     |  | [Action 3]     | |
| | [View All →]            |  +----------------+ |
| +-------------------------+                      |
+--------------------------------------------------+
```

### Form Screen Template

```
+--------------------------------------------------+
| [Back]         [Form Title]                      |
+--------------------------------------------------+
|                                                  |
|  Step 1 of 3: [Step Name]                       |
|  ●―――○―――○                                      |
|                                                  |
|  Field Label *                                   |
|  [Input field____________________________]       |
|  Helper text explaining the field                |
|                                                  |
|  Another Field                                   |
|  [Input field____________________________]       |
|                                                  |
|  Dropdown Field *                                |
|  [Select an option ▼          ]                  |
|                                                  |
|  Checkbox Options                                |
|  □ Option 1                                      |
|  □ Option 2                                      |
|  ☑ Option 3                                      |
|                                                  |
|                        [Cancel]  [Next Step →]   |
|                                                  |
+--------------------------------------------------+
```

### List-Detail Template

```
+--------------------------------------------------+
| [App Name]              [Search______] [+ New]  |
+--------------------------------------------------+
| Filter/Sort ▼      |  Detail View                |
|                    |                             |
| ● Item 1           |  [Title]                    |
|   [Preview text]   |  [Metadata]                 |
|   [Timestamp]      |                             |
|                    |  [Content block]            |
| ○ Item 2           |  [Content block]            |
|   [Preview text]   |                             |
|   [Timestamp]      |  [Actions: Edit | Delete]   |
|                    |                             |
| ○ Item 3           |                             |
|   [Preview text]   |                             |
|   [Timestamp]      |                             |
|                    |                             |
| [Load More]        |                             |
+--------------------------------------------------+
```

## Success Criteria

Wireframes are complete when:
- All key screens and states are documented
- Information architecture is clear and logical
- User flows are mapped end-to-end
- Interactions and states are annotated
- Accessibility considerations are noted
- Responsive behavior is defined
- Design decisions are documented with rationale

## Next Steps

After wireframing:
- Review with ProductManager at Story_Design_Review
- Validate with stakeholders for feedback
- Use wireframes to inform user story creation (F02-user-stories.md)
- Progress to high-fidelity prototyping if needed
- Hand off to developers with clear specifications

## Related Workflows

- `prototyping.md` - Create interactive prototype from wireframes
- `journey-mapping.md` - Map customer journey across touchpoints
- `specification-writing/workflows/write-stories.md` - User story creation
- `architecture/workflows/design-frontend.md` - Frontend architecture
