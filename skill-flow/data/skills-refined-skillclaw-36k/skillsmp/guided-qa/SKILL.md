---
name: guided-qa
description: A guided manual testing workflow where the agent pre-verifies features using browser tools, fixes found bugs, and then walks the user through the process.
---

# Guided QA Skill

This skill guides the user through a structured manual testing session. It minimizes user frustration by ensuring the "happy path" works via automated tools before asking the user to perform the steps.

## Workflow Overview

1.  **Scope Definition**: Clarify the specific area or feature to be tested if not already stated.
2.  **Automated Pre-flight**: The Agent autonomously walks through the test steps using browser tools (`navigate_page`, `click`, `fill`, etc.) to ensure basic functionality.
3.  **Pre-flight Fixes**: Any bugs encountered during the automated phase are fixed immediately.
4.  **User Walkthrough**: The Agent guides the user step-by-step through the same flow.
5.  **Interactive Triage**: Bugs found by the user are categorized (Blocker vs. Non-Blocker) and handled accordingly.
6.  **Resolution**: Final fixes for non-blocking bugs are applied.

## Phase 0: Scope Definition

**Goal**: Establish exactly what needs to be tested.

1.  **Check Scope**: If the user did not explicitly state *what* feature or flow to QA in their initial request (e.g., "QA the login flow" vs just "Run QA"), you **MUST** ask: "What specific area or feature would you like to QA today?"
2.  **Confirm**: Briefly repeat the scope back to the user to ensure alignment before starting Phase 1.

## Phase 1: Automated Pre-flight

**Goal**: Verify the feature works for the Agent before involving the user.

1.  **Analyze**: Review the requested feature set and determine the critical user path.
2.  **Launch**: Ensure the application is running (e.g., `just web` or `just dev-api`).
    *   *Tip*: Use `run_shell_command` to check for running processes/ports.
3.  **Execute**: Use available browser tools to perform the steps.
    *   `navigate_page`: Go to the starting URL (e.g., `http://localhost:8081` for Expo Web).
    *   `take_snapshot`: Read the page structure.
    *   `click` / `fill`: Interact with elements.
    *   `wait_for`: Ensure async operations complete.
4.  **Fix**: If a step fails (e.g., button doesn't work, error message appears):
    *   **Pause** the walkthrough.
    *   **Investigate** the code causing the issue.
    *   **Fix** the bug immediately.
    *   **Verify** the fix by retrying the step.
    *   **Continue** only after the fix works.

## Phase 2: User Walkthrough

**Goal**: Guide the user through the verified path to catch UX issues or edge cases.

1.  **Instruct**: Present one clear action at a time.
    *   *Bad*: "Go to the login page, sign in, and check your profile."
    *   *Good*: "Please navigate to `http://localhost:8081`." (Wait for confirmation). "Now, enter your email and click Login."
2.  **Confirm**: After each step, ask: "Did that work as expected?" or "What do you see?"
3.  **Listen**: Pay attention to details the user mentions (styling issues, confusion, lag).

## Phase 3: Interactive Triage

**Goal**: Handle issues discovered by the user without derailing the session.

When the user reports a bug, ask: **"Is this preventing you from continuing to the next step?"**

### Scenario A: Blocker (User cannot proceed)
1.  **Acknowledge**: "Understood. This is a blocker."
2.  **Fix**: Switch to coding mode. Locate the issue, fix it, and verify.
3.  **Resume**: Ask the user to retry the step.

### Scenario B: Non-Blocker (Visual glitch, minor annoyance)
1.  **Log**: "I've noted that: [Brief description of bug]."
2.  **Defer**: Add it to a `QA_FIX_LIST` in your memory or a scratchpad.
3.  **Continue**: "Let's proceed to the next step."

## Phase 4: Resolution

**Goal**: Polish the feature by addressing the deferred list.

1.  **Review**: Present the `QA_FIX_LIST` to the user.
2.  **Fix**: Systematically go through the list and apply fixes.
3.  **Final Check**: Ask the user if they want to verify any of the specific fixes or conclude the session.

## Tools Strategy

-   **Browser Tools**: Use `navigate_page`, `take_snapshot`, and `click` heavily during Phase 1.
-   **Verification**: Always use `take_snapshot` after an action to confirm the UI state changed as expected.
-   **Debugging**: If a selector isn't found, use `take_snapshot` with `verbose=true` to debug the accessibility tree.
