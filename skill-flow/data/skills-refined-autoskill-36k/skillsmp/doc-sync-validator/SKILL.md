---
name: doc-sync-validator
description: Ensures code changes in src/ are reflected in the product documentation within docs/en/product/.
---

# Documentation Sync Protocol

## 1. Context Mapping
The project uses a `docs_manifest.yaml` to map source code modules to their corresponding documentation files. 

## 2. Validation Logic
Whenever changes are detected in the `src/` directory:
1. **Analyze Diff**: Identify which modules or functions were modified.
2. **Manifest Check**: Cross-reference the modified paths against `docs_manifest.yaml`.
3. **Parity Audit**: 
   - Check if the corresponding `.md` files in `docs/en/product/` have been modified in the current staged changes.
   - If code was added/changed but documentation was not, flag a **Sync Warning**.

## 3. Agent Instructions
- If a drift is detected, do not block the commit immediately. Instead, present a summary:
  > "⚠️ Source change detected in `src/auth/` but `docs/en/product/auth-flow.md` was not updated. Would you like me to draft the documentation update now?"
- If the user says "No," proceed but log the drift in `PROJECT_STATE.md` under a "Technical Debt" section.

## 4. Exit Criteria
- **Pass (0)**: Code and Docs are both updated, or no source changes were detected.
- **Review (1)**: Source changed without documentation update (requires user bypass).
