---
name: secure-env-manager
description: Securely manage environment variables without exposing them in chat logs or history.
---

# Secure Env Manager

This skill serves as the **Standard Operating Procedure (SOP)** for handling all environment variable related tasks, errors, and configurations. It ensures strict privacy by preventing sensitive keys from ever being exposed in chat logs.

## 🚨 CRITICAL PRIVACY RULES

1.  **NEVER** ask the user to paste API keys, secrets, or passwords in the chat.
2.  **NEVER** print or echo environment variable values in your responses.
3.  **ALWAYS** use the scripts provided in this skill to read or write sensitive data.

## Protocol for Handling Env Variable Issues

When you encounter an error related to environment variables (e.g., authentication failures, missing configuration):

### Step 1: Verification (Test)
First, verify which variables are actually missing or empty. Do NOT ask the user to check manually. Run the verification script:

```bash
./.agent/skills/secure-env-manager/scripts/verify-env.sh REQUIRED_VAR_1 REQUIRED_VAR_2
```
*Replace `REQUIRED_VAR_1`, etc., with the specific keys relevant to the error (e.g., `PAYPAL_CLIENT_ID`).*

- If the script returns **Success (0)**: The variables exist. Validating their *correctness* (e.g., is the key valid?) may require checking the service logs or asking the user to re-enter them if auth fails.
- If the script returns **Failure (1)**: It will list exactly which variables are missing or empty.

### Step 2: Targeted Reset
If variables are missing, empty, or known to be invalid/expired, provide the **Guided Mode** command to the user. This allows them to set *only* the specific keys needed.

> "It looks like the following keys are missing/invalid: `PAYPAL_CLIENT_ID`. Please run this command to securely set them:"

```bash
./.agent/skills/secure-env-manager/scripts/set-env.sh PAYPAL_CLIENT_ID
```

### Step 3: Full Reset (The "Nuclear Option")
If the user wants to start fresh, or if "everything is broken" and a full reset is requested, instruct them to use the `--all` flag. This will walk them through **every** variable currently defined in their `.env` file.

```bash
./.agent/skills/secure-env-manager/scripts/set-env.sh --all
```

## How the Scripts Work

### `scripts/set-env.sh [ARGS...]`
- **Why**: Securely writes to `.env` (or `.env.local`) using `read -s` (silent input).
- **Modes**:
    - **Interactive**: No args. Loops until user hits Enter.
    - **Guided**: `set-env.sh VAR1 VAR2`. Prompts only for those specific vars.
    - **Reset All**: `set-env.sh --all`. Scans the file and prompts for every existing variable.

### `scripts/verify-env.sh [ARGS...]`
- **Why**: Checks if specific vars are set and non-empty.
- **Usage**: Returns exit code 0 if all good, 1 if any missing. Prints missing var names.
- **Privacy**: Does NOT print values. Only prints variable names.

## Usage Example (Agent Workflow)

**User**: "My PayPal isn't working."
**Agent**: 
1. *Thinking*: I should check if `PAYPAL_CLIENT_ID` and `PAYPAL_SECRET` are set.
2. *Action*: `run_terminal` -> `./.agent/skills/secure-env-manager/scripts/verify-env.sh PAYPAL_CLIENT_ID PAYPAL_SECRET`
3. *Result*: `Missing variables: - PAYPAL_SHORT_KEY` (Example)
4. *Response*: "It looks like `PAYPAL_SECRET` is missing. Please run this command to set it:"
   ```bash
   ./.agent/skills/secure-env-manager/scripts/set-env.sh PAYPAL_SECRET
   ```
