---
name: standardizing-feature-workflow
description: Standardize how to build new features from planning to documentation. Use when starting a new user story, feature request, or epic.
---

# Feature Development Workflow

## When to use this skill
- When starting work on a new Jira ticket/User Story.
- When planning a new major feature.
- When you need a checklist to ensure nothing is missed during development.

## Step 1: Planning
Before writing code:
1.  **Requirements**: Clearly define what "done" looks like.
2.  **User Stories**: Break down the feature into small, testable stories.
3.  **Mockups**: Review Figma/Sketch designs. Identify reusable components vs. new ones.
4.  **API Check**: List all endpoints needed. Are they ready? If not, define the interface contract (JSON structure) to mock.

## Step 2: Setup
1.  **Branching**: Create a fresh `feature/` branch from `develop`/`main`.
2.  **Structure**: Create necessary folders (e.g., `/screens/NewFeature`, `/components/NewFeature`).
3.  **Typing**: Define TypeScript interfaces/types for your data models and component props *first*.

## Step 3: Development
1.  **UI First**: Build "dumb" presentational components with mocked data. Ensure they look right (Storybook is helpful here).
2.  **Logic**: Implement the business logic (hooks, services).
3.  **Integration**: Replace mocks with real API calls.
4.  **State**: Wire up global state (Redux/Context) if needed.

## Step 4: Testing
1.  **Unit**: Write tests for utilities and complex logic.
2.  **Integration**: Test the main flows (happy path & error states).
3.  **Manual**: Run on actual devices (iOS & Android). Test offline mode, loading states, and weird inputs.

## Step 5: Review
1.  **Self-Review**: Diff your own code. Remove `console.log`s, commented-out code, and fix types.
2.  **Standards**: Does it meet the `mobile-coding-standards`?
3.  **A11y**: Is it accessible (screen readers, contrast)?
4.  **Performance**: No obvious lag or excessive re-renders?

## Step 6: Documentation & Merge
1.  **Docs**: Update `README.md` or internal wiki if new architecture/env vars were added.
2.  **Comments**: Add JSDoc for any complex public functions.
3.  **PR**: Open Pull Request with screenshots/video of the feature in action.
