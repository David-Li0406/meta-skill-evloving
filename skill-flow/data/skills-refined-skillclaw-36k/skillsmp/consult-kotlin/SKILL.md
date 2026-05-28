---
name: consult_kotlin
description: Instructions for checking and consulting parallel Kotlin implementations (AndroidX and KotlinX Coroutines) when identifying solutions.
---

# Consult Kotlin Implementation

This skill guides the agent to consult the reference Kotlin implementations for `go-compose` components, specifically `androidx.compose` and `kotlinx.coroutines`, to ensure parity and avoid reinventing the wheel.

## Step 1: Verify Environment

Before proceeding with any troubleshooting or design work that triggers this skill, you MUST verify that the reference repositories are available in the user's workspace.

**Required Resources:**
Inspect the `user_information` provided in your system prompt. Look for active workspace mappings that correspond to these projects (ignoring specific user or organization names if necessary):
1.  **AndroidX** (e.g., mapped to `zodimo/androidx` or `androidx`)
2.  **KotlinX Coroutines** (e.g., mapped to `Kotlin/kotlinx.coroutines` or `kotlinx.coroutines`)

**Action:**
1.  Read the `user_information` section.
2.  Identify the absolute paths associated with the above CorpusNames.
3.  Use these dynamically discovered paths for all subsequent checks (`list_dir`, `grep_search`, etc.).

## Step 2: Enforce Availability

**IF** either of the above repositories is not listed in the workspace mappings:
1.  **STOP** your current task immediately.
2.  **NOTIFY** the user using `notify_user`.
    -   Inform them that the required reference repositories are not found.
    -   Ask them to ensure these repositories are cloned and mapped in the workspace as expected.
3.  **DO NOT PROCEED** until the user confirms they are available.

## Step 3: Consult Sources

**WHEN** the repositories are available:
1.  Identify the Kotlin equivalent of the component you are working on.
    -   *Example*: `go-compose/pkg/flow` <-> `kotlinx.coroutines/kotlinx-coroutines-core/common/src/flow`
    -   *Example*: `go-compose/compose/material3` <-> `androidx/compose/material3`
2.  Use `grep_search` or `find_by_name` within those specific directories to find the relevant Kotlin files.
3.  Read the Kotlin implementation to understand:
    -   Algorithm logic.
    -   Thread safety and synchronization patterns.
    -   Edge case handling.
4.  Compare with the Go implementation and propose solutions that align with the reference behavior where appropriate, while adapting to Go idioms.
