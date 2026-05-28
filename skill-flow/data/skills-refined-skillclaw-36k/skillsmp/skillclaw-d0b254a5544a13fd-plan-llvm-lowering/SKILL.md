---
name: plan-llvm-lowering
description: Use this skill when planning how to lower a MIR construct to LLVM IR, particularly when adding new lowering or fixing existing lowering.
---

# Plan LLVM Lowering

Guide for planning MIR -> LLVM IR lowering for a specific construct.

## Prerequisites

Read before starting:

- `docs/llvm-backend.md` - lowering principles and decision framework
- `docs/mir-design.md` - MIR semantics (what you're translating)
- `docs/pipeline-contract.md` - layer boundaries

## Mental Model

> MIR is the semantic endpoint. LLVM is only an execution substrate. Lowering is not interpretation--it is faithful translation.

Key distinction: semantics are already fixed in MIR. This skill is about mechanical translation, not semantic design. If lowering needs to "decide" behavior, the MIR is underspecified--fix MIR first.

## Process

### Step 1: Identify the MIR Construct

What are you lowering?

| MIR Category | Examples                    |
| ------------ | --------------------------- |
| Rvalue       | Binary, Unary, Cast, Call   |
| Instruction  | Assign, Compute, Effect     |
| Terminator   | Jump, Branch, Delay, Return |

**Actions:**

1. Find the definition in `include/lyra/mir/`
2. Understand what semantic information it carries
3. Check if similar constructs already have lowering (use as reference)

### Step 2: Apply the Decision Framework

Answer four questions:

| Question                      | If No                                          |
| ----------------------------- | ---------------------------------------------- |
| Is behavior fully defined?    | Fix MIR first--do not decide semantics here    |
| Does it produce a value?      | Lower as call/store/branch (not SSA value)     |
| Is it pure?                   | Likely needs runtime call or memory operations |
| Which lowering class applies? | See three-way classification below             |

**Three-way lowering classification:**

| Class            | When                                          | Example                   |
| ---------------- | --------------------------------------------- | ------------------------- |
| Native LLVM op   | One instruction or near-1:1 mapping           | `add`, `icmp`, `br`       |
| Pattern lowering | Fixed recipe of LLVM ops (shifts, masks, RMW) | bit-range extraction      |
| Runtime ABI call | Needs runtime state or complex data           | `$display`, delay/suspend |

**Decision tree example:**

```
MIR Rvalue::Binary(Add, lhs, rhs)
  Q1: Fully defined? -> Yes (operation is clear)
  ...
```