---
name: pii-guard
description: Mandatory security scan for PII/PHI. Optimized for both interactive and headless (Git Hook) environments with support for templated placeholders.
---

# PII & PHI Guard Protocol (Full Version)

## 1. Objective
Identify and block the commitment of sensitive user data (Cycle Coach health domain) while allowing development templates wrapped in `{}`.

## 2. Scan Patterns (Template-Aware)
Patterns below use Lookaround assertions to ignore matches wrapped in curly braces `{}`.

| Category | Regex / Pattern | Action |
| :--- | :--- | :--- |
| **Identity** | `(?<!\{)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?!\})` | **BLOCK** |
| **Health Dates** | `(?<!\{)(ovulation\|period\|cycle_start)_date["']?\s*:\s*["']?\d{4}-\d{2}-\d{2}["']?(?!\})` | **BLOCK** |
| **Credentials** | `(?<!\{)(api_key\|secret\|bearer\|password)["']?\s*:\s*["']?[a-zA-Z0-9]{12,}(?!\})` | **HARD BLOCK** |
| **Hardware** | `(?<!\{)(device_id\|watch_sn\|serial)["']?\s*:\s*["']?[A-Z0-9-]{8,}(?!\})` | **WARN** |

## 3. Execution Instructions
1. **Fetch Diff**: Execute `git diff --cached`.
2. **Environment Detection**: 
   - If running with `--non-interactive`, within a git hook, or prompt contains **"HEADLESS"**: **DISABLE CONSENT QUESTIONS**.
   - If a non-template pattern is matched in a non-interactive session, **EXIT 1 IMMEDIATELY** and print the violation table to the console.
3. **Semantic Analysis**: Check for unmasked variables like `user_weight` or `heart_rate` in logs.
4. **Anonymization**: If PII is found, print a suggested fix (e.g., "Use hashing for this field" or "Wrap in {} for mock data") before exiting.

## 4. Exit Codes
- **0**: Clean or False Positive confirmed (Interactive only).
- **1**: PII detected or Tooling Error.
