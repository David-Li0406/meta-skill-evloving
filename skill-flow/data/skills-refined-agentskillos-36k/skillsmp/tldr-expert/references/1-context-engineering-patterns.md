# Reference: Context Engineering Patterns (2026)

## Overview
Context Engineering is the art of selecting, ordering, and formatting information to maximize an LLM's reasoning capability. It is the "Data Engineering" of the Prompt Era.

## 🛠️ The "Squaads Packing" Strategy

### 1. Hierarchy of Importance
When packing context, follow the **Top-Down Priority**:
1.  **Project Index (`index.md`):** High-level purpose.
2.  **Module Signatures:** Exported functions and types (No body).
3.  **Core Logic:** The specific file being modified (Full body).
4.  **Adjacent Context:** Related files or documentation.

### 2. The "XML Tagging" Pattern
Use distinct XML tags to help the model distinguish between different parts of the context. This is the format used by Repomix by default.

```xml
<file path="src/auth.ts">
  // Code here...
</file>
<instruction_context>
  // Instructions or ADRs here...
</instruction_context>
```

---

## 📈 Pattern: Signal-to-Noise Ratio (SNR) Optimization
The goal is to increase the "Signal" (knowledge) and decrease the "Noise" (boilerplate).

### Techniques:
- **Pruning Imports:** Most imports are boilerplate. The TLDR Expert removes them from the context bundle.
- **Stubbing Constants:** If a file has a 500-line object of constants, replace it with `// ... constants ...` unless they are relevant.
- **Type Aggregation:** Move all relevant TypeScript interfaces into a single block at the top.

---

## 🚀 Pattern: The "Warm-Up" Prompt
Before asking for a complex change, "warm up" the model's context by asking it to summarize the Repomix bundle. This ensures the model has "attended" to the key parts of the code.

```bash
# Workflow:
# 1. Provide Repomix bundle.
# 2. Prompt: "Read this bundle and list the 3 most critical modules for feature X."
# 3. Prompt: "Now, based on that, implement feature X."
```

---

## 🏁 Summary for the Expert
- **More data is NOT always better.** Irrelevant context leads to "Lost in the Middle" errors.
- **Structure matters more than length.** Use clear boundaries.
- **Signatures are the map; Implementation is the terrain.** Provide the map first.
