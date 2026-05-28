---
name: testing-standards
description: Standards for writing and running tests. Use this whenever writing code to verify functionality.
---

# Testing Strategy

## Philosophy
- **Test-Driven-ish**: When writing a new feature, write the test *before* or *simultaneously* with the code.
- **Keep it Simple**: Prioritize Unit Tests (testing one function) over complex End-to-End tests.

## Preferred Tools (Stack Dependent)
- **If Next.js/React**: Use **Vitest** + **React Testing Library**.
- **If React Native (Expo)**: Use **Jest** + **React Native Testing Library** (`@testing-library/react-native`).
- **If Python**: Use **Pytest**.
- **If Node/Backend**: Use **Vitest** or **Jest**.

## Manual Verification (UAT)
- **Validation Balance**: Automated tests are for logic; manual verification is for **Experience**.
- **Artifacts**: Every feature must have a corresponding test plan in `specs/test_plans/[feature_name].md`.
- **UAT Checklist**: A test plan should cover:
  - **Visuals**: Layout check on small/large screens.
  - **Interactions**: Touch/Gesture responsiveness.
  - **Logic**: Positive/Negative path functional flows.
- **Record Keeping**: Before finishing a task, the agent MUST verify the checkboxes in the test plan have been addressed.

## Mocking Strategy
- **Mock Custom Hooks**: When testing a component that uses custom hooks (e.g., `usePantry`, `useAuth`), ALWAYS mock the hook module, not just the network call inside it.
  - *Why*: It isolates the component test from the hook's implementation details and persistence layer.
  - *Example*: `jest.mock('../../hooks/usePantry', () => ({ useAddPantryItem: jest.fn(() => ({ mutate: jest.fn() })) }));`
- **Mock External Libraries**: If a library uses native modules (e.g., `expo-haptics`, `expo-camera`, `@react-native-community/datetimepicker`), you **MUST** mock it immediately in the test file or setup file.
  - **Critical**: Native modules will cause Jest to **HANG** or crash silently if unmocked. Do not assume they work in a Node.js test environment.
  - *Action*: When adding a new dependency, check if it has native code. If yes, write the mock *before* running the first test.
- **Transform Ignore Patterns**: If using modern ESM-only libraries (like `lucide-react-native`) in Expo/Jest, ensure they are added to `transformIgnorePatterns` in `jest.config.js`.

## Rules for the Agent
1. **Self-Correction**: If a test fails, analyze the error message. Do not ask the user for help unless you fail 3 times.
2. **Mocking**: Never make real API calls in tests. Always mock network requests (e.g., using `msw` or simple function mocks).
3. **Clean Output**: When running tests, use the verbose flag only if debugging. Otherwise, keep output minimal.
4. **Logic Extraction**: If a UI component contains data transformation logic (e.g., sorting, filtering, grouping) longer than 5 lines, **EXTRACT IT** to a pure function in `utils/` and write a Unit Test for it immediately. Do not test complex logic implicitly via UI snapshots.
5. **Refactor Safety**: When modifying any file in `utils/`, you MUST first check for the existence of `utils/__tests__/[file].test.ts`. If it exists, you MUST run it immediately after your changes to verify no regression. Do not wait for the final "Verify" step to run known unit tests.
6. **Naming Conventions**: React Hooks MUST follow the `useCamelCase` standard (e.g., `useFrequentlyStats`). Custom utility functions should be descriptive and use `camelCase`.
