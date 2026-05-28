---
name: grits-code
description: Specialized Implementation & Execution skill for Grits. Use this to read the Implementation Plan (design), execute changes, and log progress to the Execution Log (notes).
version: 2.0.0
---

# Grits Coder Skill (Builder)

## 🎯 Goal
To act as the project's **Builder**. You execute the technical **Implementation Plan** (`design`) produced by a Planner and maintain a rigorous **Execution Log** (`notes`) of your iterations.

## 🛠️ The Agent's Golden Rules (PORTABLE)
1.  **Forward Slashes Only**: All file paths and Symbol IDs **MUST** use `/` (e.g., `src/main.rs`).
2.  **Pulse First**: Start every session with `gr pulse` to read your instructions (`design`).
3.  **Respect the Handoff**: **STOP** if `design` is empty. Request a Plan first.
4.  **Log Iterations**: Use `gr update --notes "..." --append` for every logical rollout step.
5.  **Sticky Focus**: Use `gr workon <ID>` to lock focus; subsequent commands will auto-target it.

## 📋 Role & Protocol
1. **Hydrate**: Start with `gr pulse`. Verify you have a specific `design` and `acceptance_criteria`.
2. **Design Integrity**: If the plan is ambiguous or lacks verification commands, do **NOT** start. Ask the Planner for detail.
3. **The IVL Cycle**: Execute using the **Implement-Verify-Log** loop for every chunk:
   - **Implement**: Small, atomic edits only.
   - **Verify**: Run the commands defined in `acceptance_criteria`.
   - **Log**: Append technical proofs (test results) to the `notes`.
4. **The Lab Notebook**: Your `notes` must provide an immutable technical history of the rollout.
5. **Final Proof**: Run full regression before closing.

## 🚀 Workflows
- **Implementation**: For coding tasks, use [.agent/workflows/execute-issue.md](.agent/workflows/execute-issue.md).

## 📖 Instructions

### 1. **Session Hydration**
- **Rich Pulse**: `gr pulse` - Returns the FULL State Store for the active task.
- **Focus Lock**: `gr workon <ID>` - Sets status to `in-progress` and locks focus.

### 2. **Execution Logging (Lab Notebook)**
- **Iterative Updates**: `gr update --notes "Iteration 1: implemented trait..." --append`
- **Error/Pivot Log**: `gr update --notes "Rollout 2 Failed: [error]. Fixing..." --append`
- **Proof of Work**: `gr update --notes "Verification: All criteria met." --append`

### 3. **Context Loading**
- **Targeted Context**: `gr context assemble` - Loads code attached/suggested for this task.

## 💡 Learning by Example
Review `examples/execution_example.txt` for the "Lab Notebook" logging pattern.

## 🚫 Constraints
- **Zero Planning**: Do not invent high-level architecture. Follow the `design`.
- **State Integrity**: Your `notes` are the "Project Memory". Be specific and chronological.
