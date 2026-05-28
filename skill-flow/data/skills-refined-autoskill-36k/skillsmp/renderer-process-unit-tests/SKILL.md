---
name: renderer-process-unit-tests
description: This document describes how to write unit tests for the React renderer process (src/renderer). Use this when asked to create or update and fix unit tests.
---

# Renderer Process Unit Tests

## When to use this skill

Use this skill when I say some like this:

- Create unit tests for renderer process
- Fix unit tests for renderer process
- Create unit tests for [name of component or hook and so on]
- I see failed unit tests. Fix that!

## Technologies

- **Test Runner**: [Vitest](https://vitest.dev/)
- **Testing Library**: [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- **Environment**: `jsdom` (simulates a browser environment in Node.js)

## Configuration

Create or update `vitest.config.ts` (or add to `vite.config.ts`) to set the environment to `jsdom`.

```
// vitest.config.ts
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: "./src/renderer/test/setup.ts", // Optional: for global setups like jest-dom
    alias: {
      "@windows": path.resolve(__dirname, "src/renderer/windows"),
      "@utils": path.resolve(__dirname, "src/renderer/utils"),
      "@hooks": path.resolve(__dirname, "src/renderer/hooks"),
      "@layouts": path.resolve(__dirname, "src/renderer/layouts"),
      "@conceptions": path.resolve(__dirname, "src/renderer/conceptions"),
      "@components": path.resolve(__dirname, "src/renderer/components"),
      "@composites": path.resolve(__dirname, "src/renderer/composites"),
      "@shared": path.resolve(__dirname, "src/renderer/shared"),
    },
  },
});
```

If you use `setupFiles`, create `src/renderer/test/setup.ts`:

```
import "@testing-library/jest-dom";
```

## Guidelines

1.  **Mock `window.electron`**: The renderer communicates with the main process via `window.electron`. This object is not available in the test environment and must be mocked.
2.  **Test Components**: Use `@testing-library/react` to render components and assert on their output.
3.  **Test Hooks**: Use `renderHook` from `@testing-library/react` to test custom hooks.
4.  **Skip E2E**: You do not need to write or execute Playwright or other end-to-end suites for renderer changes; focus solely on unit coverage.
5.  **Positive and Negative Scenarios**: For key UI flows and hooks, write at least one positive test (expected user behavior, valid state, successful IPC) and at least one negative test (error UI states, validation failures, failed IPC, empty/edge data).
6.  **Avoid Implementation Details**: Test how the user interacts with the component, not the internal state.
7.  **The `data-testid` Rule**: Always use the **`data-testid`** word to find elements. This is for elements where you want to check the value or text. if the component does not have this prop `data-testid` then find this component and add this prop, then just use for example `screen.getByTestId('test-id')` in the unit test

- Example:

```
  // In the component: <div data-testid="user-greeting">Hello, ${userName}</div>
  // In the test: expect(screen.getByTestId('user-greeting')).toHaveTextContent('Hello, John');
```

8. **Run and Fix New Tests**: After creating a new unit test, run that test immediately (for example with `npm run test:unit:renderer`) and inspect the results; if the test fails, fix the test or the implementation until it passes.

## Writing Tests

### 1. Mocking `window.electron`

You can mock it globally in your setup file or per test.

```
// In a test file
import { vi } from "vitest";

global.window.electron = {
  ipcRenderer: {
    invoke: vi.fn(),
    on: vi.fn(),
    send: vi.fn(),
    removeListener: vi.fn(),
  },
  // ... other properties
} as any;
```

### 2. Testing a Component (Example)

Suppose you have a component `src/renderer/components/UserInfo.tsx`.

```
// src/renderer/components/UserInfo.test.tsx
import { render, screen, waitFor } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { UserInfo } from "./UserInfo";
import userEvent from "@testing-library/user-event";

// Mock a custom hook that fetches data
vi.mock("../../hooks/useUser", () => ({
  useUser: () => ({
    user: { name: "John Doe" },
    loading: false,
  }),
}));

describe("UserInfo", () => {
  it("renders user name", () => {
    render(<UserInfo />);
    expect(screen.getByText("John Doe")).toBeInTheDocument();
  });
});
```

### 3. Testing Hooks (Example)

Suppose you have a hook `src/renderer/hooks/useLogin.ts`.

```
import { renderHook, act } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { useLogin } from "./useLogin";

describe("useLogin", () => {
  it("should call login IPC on submit", async () => {
    const mockInvoke = vi.fn().mockResolvedValue({ success: true });
    global.window.electron.ipcRenderer.invoke = mockInvoke;

    const { result } = renderHook(() => useLogin());

    await act(async () => {
      await result.current.login("user", "pass");
    });

    expect(mockInvoke).toHaveBeenCalledWith("auth:login", {
      username: "user",
      password: "pass",
    });
  });
});
```

## Running Tests

Run all unit tests:

```
npm run test:unit:renderer
```