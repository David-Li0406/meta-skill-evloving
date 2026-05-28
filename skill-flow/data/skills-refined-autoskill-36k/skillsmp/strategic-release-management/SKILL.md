---
name: Strategic Release Management
description: A unified "Releaser" skill that orchestrates all other skills (Code Quality, DB, Tests, UI) into a single gated commit workflow.
---

# 🚢 Strategic Release Management Skill

This skill is the "Captain" of the repository. It operationalizes the **Git Coordinator** persona but upgrades it for the **Gemini 3** era.

## 🎯 When to Use
- **ALWAYS**: Use this instead of `git commit`.
- **Merging branches**: Verifies integration.

## 🛠️ Toolbelt

### 1. The Gated Commit (Standard)
One command to run ALL audits (Code Quality, DB, UI, Tests) and commit only if they pass.

```bash
node .agent/skills/release-manager/scripts/gated-commit.js "feat(scope): message"
```

### 2. The Emergency Bypass
**Use with Caution.** Logs the violation for future audit.

```bash
node .agent/skills/release-manager/scripts/gated-commit.js "wip(scope): fire fix" --bypass
```

## 🛡️ The Gates of Quality

| Gate | Guarding | Tool Run |
|:---:|:---:|:---:|
| **1. Lint/Types** | Code Quality | `scan-quality-metrics.js` |
| **2. DB Health** | Data Integrity | `audit-prisma-schema.js` |
| **3. Visuals** | UI/UX Standard | `scan-token-violations.js` |
| **4. Function** | User Journey | `run-smoke-tests.js` |

## 🚨 Recovery Protocol
What to do if the Gate slams shut?

1.  **Read the Log**: The script outputs EXACTLY why it failed.
2.  **Fix Forward**:
    *   *Lint Error?* Fix the specific line.
    *   *Test Fail?* Revert the recent logic change.
3.  **Do NOT Bypass** unless:
    *   The site is down.
    *   It is a pure documentation change (use `--bypass` with context).
4.  **Re-run**: `gated-commit` is idempotent. Run it until it passes.

## 🧠 Philosophy
> **"Slow is Smooth, Smooth is Fast."**
> It feels slower to run tests locally, but it is infinitely faster than fixing a production bug.
