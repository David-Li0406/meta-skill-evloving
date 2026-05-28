# Prototyping Workflow

Build interactive prototypes to validate user flows, test interactions, and demonstrate functionality.

## When to Use

- After wireframes are approved (F07-wireframes.md exists)
- Before development begins
- For user testing and validation
- For stakeholder demos and alignment
- When interaction design needs validation

## Prerequisites

**Required artifacts**:
- F01-feature-prd.md - Feature specification
- F07-wireframes.md - Wireframe designs

**Optional context**:
- Design system or component library
- F02-user-stories.md - User stories
- D06-stakeholder-insights.md - User research

## Workflow Steps

### 1. Define Prototype Scope

Determine fidelity and scope:

**Fidelity Level**:
- **Low-Fidelity**: Clickable wireframes, basic navigation
- **Medium-Fidelity**: Some styling, realistic content, key interactions
- **High-Fidelity**: Polished design, full interactions, production-like

**Scope**:
- **Happy Path Only**: Primary user flow works
- **Key Flows**: Main flows plus important alternatives
- **Full Feature**: All states, errors, edge cases

**Choose based on**:
- Time available
- Testing goals
- Stakeholder expectations
- Technical complexity

### 2. Set Up Prototype Foundation

**Option A: HTML/CSS Prototype**
- Use frontend-design skill for interactive HTML
- Benefits: Realistic interactions, shareable URL
- Use when: High fidelity needed, technical testing required

**Option B: Descriptive Prototype**
- Document interactions and state changes
- Benefits: Fast to create, good for conceptual validation
- Use when: Testing flows and concepts, not visual design

### 3. Implement Core Screens

Build screens based on wireframes:

**For each screen**:
1. Add content and components
2. Apply basic styling (if medium/high fidelity)
3. Ensure responsive layout
4. Add placeholder data

**Component Checklist**:
- [ ] Navigation elements
- [ ] Forms and inputs
- [ ] Buttons and CTAs
- [ ] Cards or content containers
- [ ] Modals or overlays (if applicable)
- [ ] Loading indicators
- [ ] Error messages

### 4. Implement Interactions

Add interactivity for key flows:

**Navigation**:
- Screen-to-screen transitions
- Tab switching
- Modal opening/closing
- Breadcrumb navigation

**Form Interactions**:
- Input validation (inline)
- Error messaging
- Success confirmation
- Multi-step progression

**Data Interactions**:
- List filtering
- Sorting
- Search
- Pagination

**State Changes**:
- Loading states
- Empty states
- Error states
- Success states

### 5. Add Realistic Content

Replace placeholders with realistic data:

**Content Guidelines**:
- Use realistic (but fake) user data
- Show various content lengths (short, medium, long)
- Include edge cases (very long names, missing data)
- Use representative images (or placeholders with dimensions)

**Data Scenarios**:
- Typical case (normal data)
- Empty case (no data)
- Error case (failed load)
- Edge case (extreme values)

### 6. Test User Flows

Verify all flows work end-to-end:

**Primary Flow Testing**:
1. Start at entry point
2. Complete happy path
3. Verify success state
4. Test back navigation
5. Ensure state persistence

**Alternative Flow Testing**:
- Test different paths through feature
- Verify conditional logic
- Test skip/cancel options

**Error Flow Testing**:
- Trigger validation errors
- Test error recovery
- Verify helpful error messages

### 7. Document Prototype

Create F08-prototype.md:

```markdown
# Prototype: [Feature Name]

## Overview

- **Feature**: [name from PRD]
- **Fidelity**: [Low/Medium/High]
- **Scope**: [Happy path / Key flows / Full feature]
- **Purpose**: [User testing / Stakeholder demo / Developer handoff]

## Access

[Option A: If HTML prototype]
- **URL**: [link to hosted prototype or local path]
- **Credentials**: [if authentication required]

[Option B: If descriptive prototype]
- **Documentation**: See screens and interactions below

## Screens Included

1. [Screen 1]: [Brief description]
2. [Screen 2]: [Brief description]
3. [Screen 3]: [Brief description]

## User Flows Implemented

### Primary Flow: [Flow Name]

**Steps**:
1. User lands on [Screen 1]
2. User clicks [Element] → Navigates to [Screen 2]
3. User fills out [Form fields]
4. User clicks [Submit] → Shows [Loading state]
5. On success → Navigates to [Screen 3] with [Success message]

**Interaction Details**:
- **[Screen 1] → [Screen 2]**: Click "[CTA text]" button
- **[Screen 2] → [Screen 3]**: Submit form, validate required fields
- **Validation**: Email format, required fields, character limits

### Alternative Flow: [Flow Name]
[Same structure]

### Error Flow: [Flow Name]
[Same structure]

## Interactions Documented

### Screen 1: [Screen Name]

#### Implemented Interactions
1. **[Element Name]** (Button)
   - Event: Click
   - Behavior: Navigate to [Screen 2]
   - State Change: None

2. **[Search Input]** (Text input)
   - Event: Type
   - Behavior: Filter results in real-time
   - State Change: Results list updates
   - Debounce: 300ms

3. **[Dropdown]** (Select)
   - Event: Change
   - Behavior: Update [dependent field]
   - Validation: Required field

#### States
- **Default**: All content loaded
- **Loading**: Skeleton UI, disabled inputs
- **Empty**: "No results" message with illustration
- **Error**: Error banner with retry button

### Screen 2: [Screen Name]
[Repeat structure]

## Interactive Elements

| Element | Type | Interaction | Outcome |
|---------|------|-------------|---------|
| [Name] | Button | Click | [What happens] |
| [Name] | Input | Type/Change | [What happens] |
| [Name] | Link | Click | [Navigation] |

## Validation Rules

### [Form Name]

| Field | Type | Required | Validation | Error Message |
|-------|------|----------|------------|---------------|
| Email | text | Yes | Email format | "Please enter a valid email" |
| Password | password | Yes | Min 8 chars | "Password must be at least 8 characters" |
| Age | number | No | 18-120 | "Please enter a valid age" |

## Prototype Limitations

[What's NOT included in this prototype]:
- [ ] Backend integration (all data is mocked)
- [ ] Complete error handling
- [ ] Accessibility features (keyboard nav, screen readers)
- [ ] Performance optimization
- [ ] [Other limitations]

## Testing Scenarios

### Scenario 1: [Happy Path]
**Goal**: [What user is trying to accomplish]

**Steps**:
1. [Action 1]
2. [Action 2]
3. [Expected outcome]

**Success Criteria**: [What indicates success]

### Scenario 2: [Alternative Path]
[Same structure]

### Scenario 3: [Error Case]
[Same structure]

## Feedback Questions

Use this prototype to validate:
1. Is the flow intuitive and easy to follow?
2. Are the interactions clear and responsive?
3. Does the layout effectively prioritize information?
4. Are error messages helpful and actionable?
5. [Other specific questions]

## Design Decisions

### Decision 1: [Interaction Pattern]
**Decision**: [What we chose]
**Rationale**: [Why]
**Alternative Considered**: [What we didn't choose and why]

### Decision 2: [Another Decision]
[Same structure]

## Next Steps

- [ ] Conduct user testing with [N] users
- [ ] Gather stakeholder feedback
- [ ] Refine based on feedback
- [ ] Hand off to development with final specs
- [ ] Document interaction patterns for design system

## Changelog

### Version 1.0 - [Date]
- Initial prototype with primary flow
- [Key screens/features included]

### Version 1.1 - [Date]
- Added [feature] based on feedback
- Fixed [issue]
```

### 8. Prepare for Testing

If conducting user testing:

**Test Plan**:
- Identify test participants (3-5 users)
- Prepare testing scenarios
- Create observation guide
- Plan for feedback collection

**Testing Script**:
```markdown
## User Testing Script

### Introduction (2 min)
"Thank you for helping us test this prototype. We're evaluating the design, not you.
There are no wrong answers. Please think aloud as you use the prototype."

### Scenario 1 (5 min)
"Imagine you want to [goal]. Show me how you would do that."

**Observe**:
- Where do they click first?
- Do they hesitate?
- Do they find the right path?
- Any confusion or errors?

### Scenario 2 (5 min)
[Repeat structure]

### Debrief (3 min)
- "What was easiest?"
- "What was most confusing?"
- "What would you change?"
- "Any other feedback?"
```

### 9. Gather and Document Feedback

After testing/review:

**Feedback Template**:
```markdown
## Prototype Feedback

### Testing Date: [Date]
### Participants: [Count and description]

### Key Findings

#### Positive Feedback
1. [What worked well]
2. [Another success]

#### Issues Identified
1. [Issue]: [Description]
   - Severity: High/Medium/Low
   - Frequency: [N of N users]
   - Recommendation: [How to fix]

2. [Another issue]
   [Same structure]

#### Suggestions
1. [User suggestion]
2. [Another suggestion]

### Prioritized Changes

**Must Fix**:
- [Issue that blocks users]

**Should Fix**:
- [Issue that causes friction]

**Nice to Have**:
- [Polish or enhancement]

### Updated Prototype
[Reference to updated version if changes made]
```

### 10. Store Artifacts

Save prototype documentation:
```bash
/home/jwwelbor/projects/ai-dev-team/docs/workflow/artifacts/F08-prototype.md
```

If HTML prototype created:
```bash
/home/jwwelbor/projects/ai-dev-team/docs/workflow/artifacts/F08-prototype/
  index.html
  styles.css
  script.js
  assets/
```

## Prototype Patterns

### Interactive Form Pattern

```javascript
// Example validation pattern
function validateForm(formData) {
  const errors = {};

  if (!formData.email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
    errors.email = "Please enter a valid email";
  }

  if (formData.password.length < 8) {
    errors.password = "Password must be at least 8 characters";
  }

  return errors;
}

// Show inline validation
function showFieldError(fieldName, errorMessage) {
  const field = document.querySelector(`[name="${fieldName}"]`);
  const errorDiv = field.nextElementSibling;
  errorDiv.textContent = errorMessage;
  errorDiv.style.display = "block";
  field.classList.add("error");
}
```

### Loading State Pattern

```javascript
// Show loading state
function showLoadingState(buttonElement) {
  buttonElement.disabled = true;
  buttonElement.innerHTML = '<span class="spinner"></span> Loading...';
}

// Hide loading state
function hideLoadingState(buttonElement, originalText) {
  buttonElement.disabled = false;
  buttonElement.innerHTML = originalText;
}
```

### State Management Pattern

```javascript
// Simple state management for prototype
const state = {
  currentScreen: 'home',
  formData: {},
  filters: {},
  isLoading: false
};

function updateState(updates) {
  Object.assign(state, updates);
  render();
}

function render() {
  // Update UI based on current state
  showScreen(state.currentScreen);
  if (state.isLoading) showLoadingState();
}
```

## Success Criteria

Prototype is complete when:
- All key screens are implemented
- Primary user flow works end-to-end
- Key interactions are functional
- States (loading, error, empty) are shown
- Realistic content is used
- Testing scenarios are documented
- Feedback collection plan is ready

## Next Steps

After prototyping:
- Conduct user testing sessions
- Review with ProductManager and stakeholders
- Refine design based on feedback
- Validate alignment with user stories (Story_Design_Review)
- Hand off to developers with interaction specs
- Document patterns for design system

## Related Workflows

- `wireframing.md` - Create wireframes before prototyping
- `journey-mapping.md` - Map customer journey
- `frontend-design skill` - Build production-quality HTML prototypes
- `architecture/workflows/design-frontend.md` - Frontend architecture
