---
name: frontend-ui-ux-design
description: Guide React component design for Budget Buddy using established design system (indigo/purple theme, rem spacing, React Bootstrap). Use when designing UI, creating components, styling, or writing frontend code.
allowed-tools: [Read, Grep, Glob]
---

# Frontend UI/UX Design

Quick reference for creating React components following Budget Buddy's design patterns.

## Quick Start

### Component Creation Checklist

```
Component Creation:
- [ ] Use functional component template
- [ ] Add PropTypes validation
- [ ] Apply design system colors (#6366f1 indigo, #8b5cf6 purple)
- [ ] Use rem spacing (0.25, 0.5, 0.75, 1, 1.25 rem)
- [ ] Add 16px border-radius for cards
- [ ] Include hover states with box-shadow
- [ ] Test keyboard navigation
- [ ] Verify color contrast (WCAG AA)
```

## Essential Patterns

### Create a New Component

```javascript
import React from 'react';
import PropTypes from 'prop-types';
import './ComponentName.css';

const ComponentName = ({ title, children }) => (
  <div className="component-name">
    <h3>{title}</h3>
    {children}
  </div>
);

ComponentName.propTypes = {
  title: PropTypes.string.isRequired,
  children: PropTypes.node,
};

export default ComponentName;
```

### Style with Design System

```css
.component-name {
  /* Use design system values */
  padding: 1rem;                /* Standard spacing */
  border-radius: 16px;          /* Card radius */
  background: linear-gradient(145deg, #ffffff 0%, #f8f9ff 100%);
  box-shadow: 0 4px 20px rgba(99, 102, 241, 0.1);
  transition: box-shadow 0.3s ease;
}

.component-name:hover {
  box-shadow: 0 6px 28px rgba(99, 102, 241, 0.15);
}
```

## Design System

**Complete specifications**: See [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md)

**Key values**:
- **Colors**: #6366f1 (primary), #8b5cf6 (accent), #334155 (text)
- **Spacing**: 0.25rem → 1.25rem increments
- **Radius**: 8px (buttons), 16px (cards)
- **Transitions**: 0.2-0.3s ease

## Component Patterns

**React templates and examples**: See [COMPONENT_PATTERNS.md](COMPONENT_PATTERNS.md)

**Common patterns**:
- React Bootstrap integration (Card, Modal, Table, Form)
- Accessibility (ARIA, keyboard nav, focus management)
- Responsive design (mobile-first, flexbox, grid)

## Naming Conventions

**CSS Classes** (BEM-like):
```css
.buddy-insights-panel { }      /* Block */
.buddy-header { }              /* Element */
.buddy-title--highlighted { }  /* Modifier */
```

Or simplified (common in Budget Buddy):
```css
.buddy-insights-panel { }
.buddy-header { }
.buddy-title { }
```

## React Bootstrap Integration

```javascript
import { Card, Button, Modal, Table, Form } from 'react-bootstrap';

// Card with custom styling
<Card className="custom-card">
  <Card.Header>Title</Card.Header>
  <Card.Body>Content</Card.Body>
</Card>

// Apply design system via custom CSS classes
```

## Accessibility Checklist

```
Accessibility:
- [ ] Add ARIA labels to icon buttons
- [ ] Support keyboard navigation (Tab, Enter, Escape)
- [ ] Manage focus for modals/dialogs
- [ ] Use semantic HTML (<button>, <nav>, etc.)
- [ ] Ensure 4.5:1 contrast ratio (text)
- [ ] Test with screen reader
```

## Common Examples

### Budget Buddy Section Component

From `/frontend/src/components/Buddy/BuddySection.js`:

```javascript
const BuddySection = ({ icon, title, children }) => (
  <div className="buddy-section">
    <div className="buddy-section-header">
      <span className="buddy-section-icon">{icon}</span>
      <h6 className="buddy-section-title">{title}</h6>
    </div>
    <div className="buddy-section-content">{children}</div>
  </div>
);
```

**CSS** (uses design system):
```css
.buddy-section {
  margin-bottom: 1.25rem;  /* xl spacing */
}

.buddy-section-title {
  color: #6366f1;          /* Primary indigo */
  font-size: 0.75rem;      /* xs text */
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
```

### Responsive Layout

```css
/* Mobile first */
.container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

@media (min-width: 768px) {
  .container {
    flex-direction: row;  /* Horizontal on tablet+ */
  }
}
```

## References

- [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md) - Complete color, spacing, typography specs
- [COMPONENT_PATTERNS.md](COMPONENT_PATTERNS.md) - React templates and examples
- `/frontend/src/components/Buddy/` - Real component examples
- React Bootstrap: https://react-bootstrap.github.io/

## Last Updated

January 1, 2026
