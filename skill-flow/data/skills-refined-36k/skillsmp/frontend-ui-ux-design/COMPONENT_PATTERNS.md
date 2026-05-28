# React Component Patterns for Budget Buddy

React component templates and patterns used throughout Budget Buddy.

## Functional Component Template

```javascript
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import './ComponentName.css';

/**
 * ComponentName - Brief description
 */
const ComponentName = ({ title, onAction, children }) => {
  const [state, setState] = useState(initialValue);

  useEffect(() => {
    // Side effects
  }, [dependencies]);

  const handleAction = () => {
    onAction?.();
  };

  return (
    <div className="component-name">
      <div className="component-header">
        <h3>{title}</h3>
      </div>
      <div className="component-content">
        {children}
      </div>
    </div>
  );
};

ComponentName.propTypes = {
  title: PropTypes.string.isRequired,
  onAction: PropTypes.func,
  children: PropTypes.node,
};

export default ComponentName;
```

## CSS File Template

```css
/* ComponentName Styles */

.component-name {
  border-radius: 16px;
  padding: 1rem;
  background: linear-gradient(145deg, #ffffff 0%, #f8f9ff 100%);
  box-shadow: 0 4px 20px rgba(99, 102, 241, 0.1);
  transition: box-shadow 0.3s ease;
}

.component-name:hover {
  box-shadow: 0 6px 28px rgba(99, 102, 241, 0.15);
}

.component-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}
```

## React Bootstrap Patterns

### Card Component
```javascript
import { Card, Button } from 'react-bootstrap';

const MyCard = () => (
  <Card className="custom-card">
    <Card.Header>
      <Card.Title>Title</Card.Title>
    </Card.Header>
    <Card.Body>
      <Card.Text>Content</Card.Text>
      <Button variant="primary">Action</Button>
    </Card.Body>
  </Card>
);
```

### Modal Component
```javascript
import { Modal, Button } from 'react-bootstrap';

const MyModal = ({ show, onHide, title, children }) => (
  <Modal show={show} onHide={onHide} size="lg" centered>
    <Modal.Header closeButton>
      <Modal.Title>{title}</Modal.Title>
    </Modal.Header>
    <Modal.Body>{children}</Modal.Body>
    <Modal.Footer>
      <Button variant="secondary" onClick={onHide}>Cancel</Button>
      <Button variant="primary" onClick={handleSave}>Save</Button>
    </Modal.Footer>
  </Modal>
);
```

### Table Component
```javascript
import { Table } from 'react-bootstrap';

const DataTable = ({ data }) => (
  <Table responsive hover>
    <thead>
      <tr><th>Column 1</th><th>Column 2</th></tr>
    </thead>
    <tbody>
      {data.map((row, idx) => (
        <tr key={idx} className={row.isActive ? 'table-active' : ''}>
          <td>{row.col1}</td>
          <td>{row.col2}</td>
        </tr>
      ))}
    </tbody>
  </Table>
);
```

### Form Component
```javascript
import { Form, Button } from 'react-bootstrap';

const MyForm = () => {
  const [formData, setFormData] = useState({ field1: '' });

  return (
    <Form onSubmit={handleSubmit}>
      <Form.Group className="mb-3">
        <Form.Label>Field 1</Form.Label>
        <Form.Control
          type="text"
          value={formData.field1}
          onChange={(e) => setFormData({...formData, field1: e.target.value})}
        />
      </Form.Group>
      <Button variant="primary" type="submit">Submit</Button>
    </Form>
  );
};
```

## Budget Buddy Examples

### Buddy Section
```javascript
import React from 'react';
import './BuddySection.css';

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

### Accessibility Patterns

```javascript
// ARIA labels
<button aria-label="Close dialog" aria-expanded={isOpen}>
  {icon}
</button>

// Keyboard navigation
const handleKeyDown = (e) => {
  if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault();
    handleAction();
  }
};

<div tabIndex={0} onKeyDown={handleKeyDown} role="button">
  Clickable content
</div>

// Focus management
const firstFocusRef = useRef(null);
useEffect(() => {
  if (isOpen) firstFocusRef.current?.focus();
}, [isOpen]);
```

## Responsive Patterns

```css
/* Mobile-first */
.component {
  padding: 0.5rem;
  font-size: 0.875rem;
}

@media (min-width: 768px) {
  .component {
    padding: 1rem;
    font-size: 0.95rem;
  }
}

/* Flexbox */
.container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

@media (min-width: 768px) {
  .container {
    flex-direction: row;
  }
}

/* Grid */
.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
```
