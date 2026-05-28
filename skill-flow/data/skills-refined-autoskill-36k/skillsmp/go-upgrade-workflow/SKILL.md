---
name: go-upgrade-workflow
description: Step-by-step workflow for safely upgrading Go dependencies using the standard Go toolchain.
---

# Workflow: `go-upgrade-workflow`

This skill guides you through the process of safely upgrading Go dependencies. Follow these steps exactly to ensure project stability and maintain a clean `go.mod` file.

## Prerequisites

Before starting, ensure:

- [ ] Go toolchain (1.11+) is installed and available in the PATH.
- [ ] A `go.mod` file exists in the project root.
- [ ] The current codebase compiles and the test suite is passing.

## Steps

### 1. Preparation & Baseline

1.  **Integrity Check**:
    - Run `go mod verify` to ensure the local cache has not been tampered with.
2.  **Health Check**:
    - Run the test suite: `go test ./...`
    - _Verification_: If tests fail, do not proceed until the baseline is fixed.
3.  **Back up Module Files**:
    - `cp go.mod go.mod.bak`
    - `cp go.sum go.sum.bak`
    - _Verification_: Check that backup files exist.

### 2. Execution

Choose one of the following upgrade paths:

- **Option A: Full Upgrade** (All dependencies to latest minor/patch):
  - Run `go get -u ./...`
- **Option B: Patch-only Upgrade** (All dependencies to latest patch):
  - Run `go get -u=patch ./...`
- **Option C: Targeted Upgrade** (Specific package):
  - Run `go get -u <package_path>` (e.g., `go get -u github.com/gin-gonic/gin`)

### 3. Validation & Tidying

1.  **Tidy Modules**:
    - Run `go mod tidy` to remove unused dependencies and update `go.sum`.
    - _Verification_: Ensure no errors are reported by `go mod tidy`.
2.  **Verify Integrity**:
    - Run `go mod verify` again.
3.  **Run Tests**:
    - Run `go test ./...`
    - _Verification_: Ensure all tests pass with the upgraded dependencies.
4.  **Linting (Optional but Recommended)**:
    - If `trunk` is available, run `trunk check`.
    - Otherwise, run your project's standard linter (e.g., `golangci-lint run`).

### 4. Finalization

1.  **Cleanup**:
    - If all validations pass, remove the backups: `rm go.mod.bak go.sum.bak`.
2.  **Commit Changes**:
    - Commit `go.mod` and `go.sum`.

## Rollback / Failure Handling

If any step fails, especially the validation or test steps:

1.  **Restore Module Files**:
    - `mv go.mod.bak go.mod`
    - `mv go.sum.bak go.sum`
2.  **Verify Restore**:
    - Run `go mod download` to ensure the original state is restored.
3.  **Report Failure**:
    - Provide the failure logs and list the packages that were being upgraded.
