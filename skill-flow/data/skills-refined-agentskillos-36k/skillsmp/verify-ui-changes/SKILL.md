---
name: Verify UI Changes
description: Standard procedure for verifying UI updates and bug fixes using the browser subagent.
---

# Verify UI Changes

Use this skill whenever you modify UI components, CSS, or layout logic to ensure visual correctness and stability.

## 1. Define the Test Case
Before launching the browser, clearly define:
- **Target URL**: Where the change is visible.
- **Key Elements**: Which components need inspection.
- **Interactions**: What clicks/inputs trigger the state changes.
- **Success Criteria**: What *exactly* should happen (e.g., "Colon remains fixed at x=500", "No console errors").

## 2. Launch Browser Subagent
Call `browser_subagent` with a detailed task prompt:

```markdown
Navigate to [URL].
1. [Interaction Step 1]
2. [Interaction Step 2]
...
Critically observe [Specific Element] for [Specific Behavior (e.g., layout shift, bounce, flash)].
Capture browser console logs to check for errors.
Return a report confirming [Success Criteria] or detailing any regressions.
```

## 3. Critical Observation Checks
- **Layout Stability**: Do elements jump, shift, or resize unexpectedly?
- **Alignment**: Are items properly centered/aligned as requested?
- **Console Errors**: Are there any red errors in the console? (Use `capture_browser_console_logs`)
- **Responsive Behavior**: Does it look right at the current viewport size?

## 4. Documentation
- Verify the change with a screenshot or recording.
- If issues persist, **DO NOT** mark the task as done. Iterate on the fix.
