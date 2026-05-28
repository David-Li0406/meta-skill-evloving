---
name: manual-testing
description: Manually verify code changes work as expected. Use after implementing a feature or bug fix, after making visual/UI changes, after modifying API endpoints, or before considering work "done". All functional changes must be manually verified, even small changes. This is in addition to automated tests.
---

# Manual Testing

## Testing Approaches

### Visual/UI Changes

For front-end changes, use the Chrome browser to verify the UI:

1. **Navigate to the relevant page** using the browser automation tools
2. **Take a screenshot** to see the current state
3. **Evaluate the result** - does it look correct? Is the layout right? Are styles applied?
4. **Iterate 2-3 times** if needed until the UI looks good
5. **Test interactions** - click buttons, fill forms, verify behavior

### API Endpoint Changes

Use curl to verify endpoints work. Key things to verify:
- Correct HTTP status codes
- Expected response structure
- Error handling for invalid inputs
- Authentication/authorization works correctly

### Backend Changes

- Execute method with various inputs directly in a REPL or test script (e.g. `rails console`, `rails runner`, etc.)
- Verify database state changes when applicable

### Configuration Changes

- Verify the configuration loads without errors
- Test that the configuration has the intended effect
- Check for syntax errors or typos

### CLI/Script Changes

- Run commands with different argument combinations
- Test with valid and invalid inputs
- Verify output format and content
- Check exit codes

## Verification Checklist

Before marking work as complete:
- Happy path works as expected
- Edge cases handled appropriately
- Error states display correctly
- No console errors in browser
- No unexpected server errors in logs
