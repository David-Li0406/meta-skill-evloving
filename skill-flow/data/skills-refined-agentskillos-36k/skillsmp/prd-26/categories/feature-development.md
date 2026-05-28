# Feature Development

Building new features, enhancements, and integrations.

## Mental Model

Feature development is translation: idea → spec → code → verification.

```
Idea: "Users should be able to export data"
         ↓
Spec: What formats? What data? Where does button go? What happens during export?
         ↓
Dependencies: What needs to exist first? What patterns to follow?
         ↓
Implementation: Build piece by piece, verifying each piece
         ↓
Verification: Does it match the spec? Does it work in the browser?
```

## Key Principles

### Specification First
Before implementation, understand exactly what should exist.
- What screens, routes, or pages?
- What components and their behavior?
- What data flows and state changes?
- Current state vs. desired state?

### Map Dependencies
Features rarely exist in isolation.
- What needs to exist before this feature?
- What existing patterns should this follow?
- What might this break or affect?
- What order should things be built?

### Implement Incrementally
Build piece by piece, not all at once.
- Each piece should be verifiable independently
- Catch problems early, not at the end
- Maintain a working state throughout

### Verify Against Spec
The final check is always: does this match what we said we'd build?
- Use Agent Browser CLI for any UI work
- Test all specified behaviors
- Check edge cases that were identified

## Agent Browser CLI Usage

Browser verification is essential for feature development.

**During implementation:**
```bash
# After building a component, verify it works
agent-browser open http://localhost:3000/feature-page
agent-browser snapshot -i
agent-browser click @element
agent-browser screenshot progress.png
```

**Final validation:**
```bash
# Verify complete feature against original spec
agent-browser open http://localhost:3000
# Navigate through all specified flows
# Verify all UI elements appear and behave correctly
# Screenshot final states
agent-browser close
```

## What to Extract from Users

- Complete specification (screens, components, behaviors)
- Current state vs. desired state
- UI/UX expectations (mockups, references, descriptions)
- Data requirements and sources
- Integration points with existing systems
- Performance expectations
- Edge cases and error scenarios
- Success criteria

## Red Flags

You're doing it wrong if:
- Starting implementation without clear specification
- Building multiple things before testing any
- Skipping browser verification for UI work
- Assuming you know what the user wants without confirming
- Not following existing patterns in the codebase
- Batching all verification at the end

## Story Structure for Features

Typical feature PRD structure:
1. Context gathering - understand current state
2. Foundation - setup, dependencies, scaffolding
3. Core implementation - main functionality
4. Edge cases and error handling
5. Browser verification - visual/interactive testing
6. Final validation - full test suite, build
