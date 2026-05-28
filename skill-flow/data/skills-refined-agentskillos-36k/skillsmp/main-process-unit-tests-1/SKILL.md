---
name: main-process-unit-tests
description: Unit testing skill for Electron main process. guidelines, examples, and Vitest patterns to create and fix unit tests for services, IPC handlers, and DI-based code.
---

# Main Process Unit Tests

## When to use this skill

Use this skill when you want to:

- Create or fix unit tests for Electron main process services and IPC handlers using Vitest
- Mock Electron APIs, network calls, and file system interactions for reliable unit tests
- Validate IPC handlers, provider factories, and DI-injected services in isolation
- Diagnose and fix failing main-process unit tests and restore test suite health
- Enforce project testing conventions (co-located tests, naming, and mocking patterns)

## Directory Structure

Tests should be co-located with the files they test.

- Source: `src/main/feature/service.ts`
- Test: `src/main/feature/service.test.ts`

## Guidelines

1.  **Mock Electron APIs**: The main process runs in a Node.js environment during tests, but it imports `electron`. You must mock `electron` modules to prevent runtime errors.
2.  **Mock External Services**: Mock network requests, file system operations, and other side effects.
3.  **Test Pure Logic**: Focus on testing business logic and data transformations.
4.  **Skip E2E**: There is no requirement to create or execute Playwright or other end-to-end suites; focus solely on unit-level coverage.
5.  **Test IPC Handlers**: Verify that IPC handlers call the correct services with the correct arguments.
6.  **Positive and Negative Scenarios**: For every important behavior, add at least one positive test (happy path, valid input, successful response) and at least one negative test (error paths, invalid input, rejected promises, missing data, edge cases).
7.  **Run and Fix New Tests**: After creating a new unit test, run that test immediately (for example with `npm run test:unit:main`) and inspect the results; if the test fails, fix the test or the implementation until it passes.

## Setup

Ensure you have the necessary dependencies (already in `package.json`):

```
npm install -D vitest
```

## Writing Tests

### 1. Mocking Electron

Use `vi.mock("electron", ...)` at the top of your test file.

```
import { vi } from "vitest";

vi.mock("electron", () => ({
  app: {
    getPath: vi.fn().mockReturnValue("/tmp"),
  },
  ipcMain: {
    handle: vi.fn(),
    on: vi.fn(),
  },
  BrowserWindow: vi.fn().mockImplementation(() => ({
    loadURL: vi.fn(),
    show: vi.fn(),
  })),
}));
```

### 2. Testing Services (Example)

Suppose you have a service `src/main/user/service.ts` that fetches a user.

```
// src/main/user/service.test.ts
import { describe, it, expect, vi, beforeEach } from "vitest";
import { getUserById } from "./service.js";
import * as RestApi from "../@shared/services/rest-api/service.js";
import * as ErrorMessages from "../@shared/services/error-messages.js";

// Mock dependencies
vi.mock("../@shared/services/rest-api/service.js");
vi.mock("../@shared/services/error-messages.js");

describe("User Service", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("should return user data when API call is successful", async () => {
    const mockUser = { id: "1", name: "Test User" };

    // Mock the 'get' function from rest-api service
    vi.mocked(RestApi.get).mockResolvedValue({
      data: mockUser,
      error: undefined,
    });

    const result = await getUserById("1");

    expect(result).toEqual(mockUser);
    expect(RestApi.get).toHaveBeenCalled();
  });

  it("should show error message when API call fails", async () => {
    const mockError = { message: "Network Error" };

    vi.mocked(RestApi.get).mockResolvedValue({
      data: undefined,
      error: mockError,
    });

    await getUserById("1");

    expect(ErrorMessages.showErrorMessages).toHaveBeenCalledWith(
      expect.objectContaining({
        body: "Network Error",
      })
    );
  });
});
```

### 3. Testing IPC Handlers

To test IPC handlers, you often need to mock the registration function or the `ipcMain` calls.

If your IPC setup looks like this:

```
// src/main/user/ipc.ts
import { ipcMainOn } from "../@shared/utils.js";
import { getUserById } from "./service.js";

export function registerIpc() {
  ipcMainOn("user:get", async (event, id) => {
    return getUserById(id);
  });
}
```

You can test it like this:

```
// src/main/user/ipc.test.ts
import { describe, it, expect, vi } from "vitest";
import { registerIpc } from "./ipc.js";
import * as SharedUtils from "../@shared/utils.js";
import * as UserService from "./service.js";

vi.mock("../@shared/utils.js");
vi.mock("./service.js");

describe("User IPC", () => {
  it("should register 'user:get' handler", () => {
    registerIpc();
    expect(SharedUtils.ipcMainOn).toHaveBeenCalledWith(
      "user:get",
      expect.any(Function)
    );
  });

  it("should call getUserById when handler is invoked", async () => {
    // Capture the handler
    let handler: Function | undefined;
    vi.mocked(SharedUtils.ipcMainOn).mockImplementation((channel, cb) => {
      if (channel === "user:get") handler = cb;
    });

    registerIpc();

    expect(handler).toBeDefined();

    // Simulate IPC call
    const mockEvent = {};
    const userId = "123";
    await handler!(mockEvent, userId);

    expect(UserService.getUserById).toHaveBeenCalledWith(userId);
  });
});
```

## Running Tests

Run all unit tests:

```
npm run test:unit:main
```

Run specific test file:

```
npx vitest src/main/user/service.test.ts
```
