---
name: bugs
description: Known bugs and quirks in dependencies and tools
---

# Bugs

Known issues, quirks, and workarounds for dependencies and tooling used in the ikigai project.

## lcov Version Reporting Bug

**Issue:** The `lcov --version` command reports an incorrect version string that doesn't match the installed package version.

**Evidence:**

**Host system (Debian 13.2):**
- Package version: `lcov 2.3.1-1`
- Binary reports: `lcov: LCOV version 2.0-1`

**Debian 13.2 container:**
- Package version: `lcov 2.3.1-1`
- Binary reports: `lcov: LCOV version 2.0-1`

**Ubuntu 24.04 (GitHub runners):**
- Package version: `lcov 2.0-4ubuntu2`
- Binary reports: `lcov: LCOV version 2.0-1`

**Root cause:** The version string is hardcoded in `/usr/lib/lcov/lcovutil.pm`:
```perl
our $VERSION = "2.0-1";
```

This hardcoded value is not updated when the package version changes.

**Impact:**
- Cannot rely on `lcov --version` to determine actual lcov version
- Must use `dpkg -l lcov` (Debian/Ubuntu) to get true package version
- Scripts that check lcov version via `--version` may make incorrect decisions

**Workaround:**
Use package manager to check version instead of binary:
```bash
dpkg -l lcov | grep lcov  # Shows actual package version
```

**Status:** This appears to be an upstream packaging issue in Debian lcov 2.3.1-1.
