---
name: web-accessibility-implementation
description: Use this skill when implementing web accessibility best practices, including WCAG compliance, ARIA attributes, and keyboard navigation for interactive UI components.
---

# Skill body

## Overview

This skill provides guidelines for implementing web accessibility in accordance with WCAG 2.1 standards, focusing on semantic HTML, ARIA attributes, keyboard navigation, and color contrast to ensure that web applications are usable by everyone.

## When to Use This Skill

- When creating new interactive UI components such as forms, buttons, and error messages.
- When modifying existing components to improve accessibility (ARIA, keyboard navigation, contrast).
- When ensuring compliance with accessibility standards in web applications.

## Key Guidelines

1. **WCAG 2.1 Compliance**: Follow the four principles of WCAG (Perceivable, Operable, Understandable, Robust) and ensure that all content meets Level A, AA, and AAA criteria.
2. **Semantic HTML**: Use appropriate HTML elements to convey meaning and structure, enhancing accessibility for screen readers.
3. **ARIA Attributes**: Implement ARIA roles and properties to improve accessibility for dynamic content and complex UI components.
4. **Keyboard Navigation**: Ensure all interactive elements are accessible via keyboard (e.g., `<button>`, `<a>`, `<input>`).
5. **Color Contrast**: Maintain a minimum contrast ratio of 4.5:1 for body text and 3:1 for larger text to ensure readability.
6. **Error Handling**: Structure error messages clearly, using `role="alert"` for summaries and linking to specific fields with `aria-describedby`.
7. **Responsive Design**: Use fluid typography and spacing with CSS `clamp()` to ensure accessibility across different screen sizes.
8. **Testing Tools**: Utilize accessibility testing tools (e.g., axe, Lighthouse) to evaluate compliance and identify issues.

## Implementation Steps

1. **Define Design Tokens**: Use CSS Custom Properties for colors, spacing, and typography to ensure consistency and maintainability.
2. **Implement ARIA Roles**: Add ARIA roles to elements that require additional context for assistive technologies.
3. **Ensure Keyboard Focus**: Use `:focus-visible` to indicate focus states and ensure that all interactive elements are reachable via the keyboard.
4. **Test Accessibility**: Regularly test your application with screen readers and keyboard navigation to ensure all components are accessible.
5. **Document Accessibility Practices**: Maintain documentation of accessibility guidelines and best practices for your team.

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Accessibility Testing Tools](https://webaim.org/resources/eval/)