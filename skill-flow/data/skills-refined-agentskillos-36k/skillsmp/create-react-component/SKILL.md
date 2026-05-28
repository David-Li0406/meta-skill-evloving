---
name: Create React Component
description: Create a new React component following project best practices
---

# Creating a React Component

This skill guides the creation of new React components to ensure consistency, maintainability, and quality across the project.

## 1. Analysis & Preparation
*   **Identify Responsibility**: Clearly define what the component does. Is it a UI primitive (atom) or a complex feature (organism)?
*   **Determine Location**:
    *   Shared UI components: `src/components/ui/` or `src/components/common/`
    *   Feature-specific components: `src/features/<FeatureName>/components/`
*   **Check Existing**: Verify if a similar component already exists to avoid duplication.

## 2. File Structure
Create a directory with the **PascalCase** name of the component.
Example: `src/components/ui/MyComponent`

The directory should contain:
*   `MyComponent.tsx`: The main component implementation.
*   `index.ts`: Re-export the component (e.g., `export * from './MyComponent';`).
*   `(Optional) MyComponent.css` or `styles.ts`: For styling, depending on the project's styling strategy (e.g., CSS Modules, Styled Components, Tailwind).

## 3. Implementation Guidelines (The "Gold Standard")

### Setup
*   **Imports**: Group imports: React/Project dependencies -> Local components -> Styles/Utils.
*   **Types**: Always define a `Props` interface. Export it if it's likely to be used elsewhere.

### Coding
*   **Function Component**: Use `const ComponentName = ...` or `function ComponentName(...)`.
*   **Props Destructuring**: Destructure props in the function signature for readability.
*   **Clean Code**: Keep the render logic clean. Extract complex logic into custom hooks if proper.
*   **Accessibility (a11y)**: Ensure interactive elements have accessible names (aria-label) and keyboard navigation support.

### Example Template (`MyComponent.tsx`)

```tsx
import React from 'react';

// Define Props interface
export interface MyComponentProps {
  title: string;
  isActive?: boolean;
  onClick: () => void;
}

/**
 * MyComponent
 * Description of what this component does.
 */
export const MyComponent: React.FC<MyComponentProps> = ({
  title,
  isActive = false,
  onClick,
}) => {
  return (
    <div
      role="button"
      tabIndex={0}
      onClick={onClick}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          onClick();
        }
      }}
      className={`my-component ${isActive ? 'active' : ''}`}
    >
      <h3>{title}</h3>
    </div>
  );
};
```
