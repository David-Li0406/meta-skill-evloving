---
name: implement
description: Implement features following spec-driven workflow. Read specs first, extract design principles, plan file strategy, then write production-ready code with type hints and docstrings. Use when user asks to implement a feature, write code, or build a module. Depends on spec-sync for specification access.
metadata:
  category: implementation
  triggers: "implement, write code, build module, 实现, 写代码"
allowed-tools: Read Write Bash(python:*) Bash(pytest:*)
---

# Standard Operating Procedure: Implement from Spec

You are the Lead Architect for the Modular RAG MCP Server. When the user asks to implement a feature, you MUST follow this strictly defined workflow.

> **Prerequisite**: This skill depends on `spec-sync` for accessing specification documents.
> Spec files are located at: `.github/skills/spec-sync/specs/`

---

## Step 1: Spec Retrieval & Analysis
**Goal**: Ground your work in the authoritative spec documentation using progressive disclosure.

### 1.1 Navigate Intelligently
Instead of reading the entire `DEV_SPEC.md` , use the modular approach:
- **First**, read `.github/skills/spec-sync/SPEC_INDEX.md` to locate the relevant chapter.
- **Then**, read only the specific chapter file from `.github/skills/spec-sync/specs/`.

### 1.2 Extract Task-Specific Requirements
Identify key requirements from the targeted chapter:
*   **Inputs/Outputs**: What data types are expected?
*   **Dependencies**: Are there specific libraries required?
*   **Modified Files**: What files should be created or modified for this task?
*   **Verification Criteria**: What are the acceptance criteria for this task?

### 1.3 Extract Design Principles

**CRITICAL**: Identify and extract relevant design principles from the spec for the current task.

**Actions**:
1. Locate task in `specs/06-schedule.md`
2. Cross-reference `specs/03-tech-stack.md` or `specs/05-architecture.md`
3. Extract applicable principles (Pluggable, Config-Driven, Fallback, Idempotent, Observable)
4. Document principles before coding

**Output Template**:
```
────────────────────────────────────
DESIGN PRINCIPLES FOR THIS TASK
────────────────────────────────────
Task: [Task ID] [Task Name]

Applicable Principles:
1. [Principle] - [Implementation requirement]
2. [Principle] - [Implementation requirement]

Source: specs/XX-xxx.md Section X.X
────────────────────────────────────
```

### 1.4 Acknowledge
Explicitly state to the user which chapter you consulted and which principles apply. Example:
> *"I have reviewed `specs/03-tech-stack.md` Section 3.3.2. For task B1 (LLM Factory), the applicable design principles are: Pluggable Architecture (abstract base + factory), Configuration-Driven (provider from settings.yaml), and Graceful Error Handling."*

**Chapter Reference Quick Guide** (files in `.github/skills/spec-sync/specs/`):
- **Architecture questions** → `05-architecture.md`
- **Tech implementation details** → `03-tech-stack.md`
- **Testing requirements** → `04-testing.md`
- **Schedule/Progress tracking** → `06-schedule.md`

---

## Step 2: Technical Planning
**Goal**: Ensure modularity and design principle compliance before writing a single line of code.

1.  **File Strategy**: List the files to create or modify (cross-check with task's "Modified Files" field in schedule).
2.  **Interface Design**: Based on the design principles extracted in Step 1.3:
    - If **Pluggable** principle applies → Define abstract base classes first
    - If **Factory Pattern** applies → Plan the factory function signature
    - If **Config-Driven** applies → Identify settings.yaml fields needed
3.  **Dependency Check**: If new libraries are needed, plan to update `pyproject.toml` or `requirements.txt`.
4.  **Design Principle Checklist**: Before proceeding, verify your plan addresses each principle from Step 1.3.

---

## Step 3: Implementation
**Goal**: Write production-ready, compliant code.

1.  **Coding Standards**:
    *   **Type Hinting**: Mandatory for all function signatures.
    *   **Docstrings**: Google-style docstrings for all classes and methods.
    *   **No Hardcoding**: Use configuration or dependency injection.
    *   **Clean Code Principles** :
        - **Single Responsibility**: Each function/class does ONE thing and does it well
        - **Short & Focused**: Functions should be small (< 20 lines ideal), classes should be cohesive
        - **Meaningful Names**: Variables/functions reveal intent (`getUserById` not `getData`)
        - **No Side Effects**: Functions do what their name says, nothing hidden
        - **DRY**: Abstract common patterns, avoid duplication
        - **Fail Fast**: Validate inputs early, raise clear exceptions
2.  **Error Handling**: Implement robust try/except blocks for external integrations (LLMs, Databases).

---

## Step 4: Self-Verification (Before Testing)
**Goal**: Self-correction and design principle compliance before handing off to testing-stage.

> **Scope**: This is STATIC verification (code review, not execution). Actual test execution happens in Stage 4 (testing-stage).

1.  **Spec Compliance Check**: Does the generated code violate any constraint found in Step 1?
2.  **Design Principle Compliance Check**: Verify each principle from Step 1.3 is implemented:
    - [ ] If **Pluggable** → Is there an abstract base class? Can implementations be swapped?
    - [ ] If **Factory Pattern** → Does the factory correctly route based on config?
    - [ ] If **Config-Driven** → Are all magic values moved to settings.yaml?
    - [ ] If **Fallback** → Is there graceful degradation on failure?
    - [ ] If **Idempotent** → Are operations safely repeatable?
3.  **Test File Verification**: Ensure test files are created with proper structure (imports, test cases)
4.  **Refinement**: If you used placeholders like `pass`, replace them with working logic or a clear `NotImplementedError` with a TODO comment explaining why.
5.  **Final Output**: Summarize which design principles were applied:
    ```
    ────────────────────────────────────
     DESIGN PRINCIPLES APPLIED
    ────────────────────────────────────
    [x] Pluggable: BaseLLM abstract class defined
    [x] Factory: LLMFactory.create() routes by provider
    [x] Config-Driven: Provider read from settings.llm.provider
    [x] Error Handling: Unknown provider raises ValueError
    ────────────────────────────────────
    ```

---
