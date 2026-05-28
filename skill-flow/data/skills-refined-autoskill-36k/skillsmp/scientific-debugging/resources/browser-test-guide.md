# Browser Test Guide

> How to use `browser_subagent` effectively.

## 1. Task Description
Write clear, step-by-step instructions for the subagent.

**Good:**
"Go to localhost:8080. Click the 'Login' button. Type 'user' in username. Take a screenshot."

**Bad:**
"Test the login page."

## 2. Interaction Tips
- **Wait for Elements**: Always assume async loading.
- **Specific Selectors**: Use ID or specific text content where possible.
- **Check Console**: Always ask the subagent to report console errors.

## 3. Visual Verification
- Use `screenshot` to confirm UI states (e.g., "Is the modal visible?").
- Use `recording` for animations or transitions.
