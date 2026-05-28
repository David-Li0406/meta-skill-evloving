# Error Root Analyzer Skill

## Overview

The **Error Root Analyzer** skill provides a comprehensive, systematic approach to debugging and resolving programming errors. Unlike surface-level debugging that only addresses immediate symptoms, this skill guides deep error analysis to identify and fix root causes while conducting thorough module reviews to uncover related issues.

## Key Features

### 🎯 Root Cause Analysis
- Traces errors back to their fundamental causes
- Distinguishes between symptoms and actual problems
- Prevents recurring issues by addressing core problems

### 🔍 Comprehensive Module Review
- Reviews entire modules when errors are found
- Identifies related bugs, exceptions, and edge cases
- Ensures holistic fixes across the codebase

### 📚 Extensive Knowledge Base
- **Error Patterns Reference**: Catalog of 10+ common error categories with root causes
- **Debugging Checklists**: Language-specific checklists for Python, JavaScript, Java, C/C++, and more
- **Framework-Specific Guidance**: Debugging tips for databases, web frameworks, and APIs

### 🛠️ Automated Tools
- Python error analysis script (`analyze_error.py`) for quick stack trace categorization
- Structured investigation workflow
- Systematic verification and testing approach

## When to Use This Skill

Use this skill when:
- ✅ Programs fail, crash, or produce errors during execution
- ✅ You need to debug complex or recurring issues
- ✅ Surface-level fixes haven't resolved the problem
- ✅ You want to ensure no related bugs exist in the module
- ✅ Conducting post-mortem analysis of production issues
- ✅ Reviewing code that has a history of bugs

## Workflow

The skill follows a 5-phase systematic approach:

### Phase 1: Error Capture and Initial Analysis
- Gather complete error information (stack traces, inputs, environment)
- Identify error surface and category

### Phase 2: Root Cause Investigation
- Trace error execution backwards
- Identify where incorrect state originated
- Analyze error patterns and common root causes

### Phase 3: Comprehensive Module Review
- Static code analysis of entire module
- Dependency and logic flow analysis
- Exception landscape mapping
- Language and framework-specific checks

### Phase 4: Fix Design and Implementation
- Design comprehensive fix addressing root cause
- Fix all related issues discovered
- Add prevention mechanisms
- Implement with proper prioritization

### Phase 5: Verification and Testing
- Verify root cause is fixed
- Test all related fixes
- Perform regression and integration testing

## Contents

```
error-root-analyzer/
├── SKILL.md                              # Main skill instructions
├── references/
│   ├── error-patterns.md                 # 10+ error categories with root causes
│   └── debugging-checklist.md            # Language-specific debugging checklists
└── scripts/
    └── analyze_error.py                  # Automated error analysis tool
```

## Usage Example

When you encounter an error:

1. **Trigger the skill** with a message like:
   - "I'm getting an error when running my program"
   - "This module keeps failing, help me debug it"
   - "Fix this error and review the entire module"

2. **Provide error information**:
   - Paste the complete stack trace
   - Describe what operation triggered the error
   - Share relevant code context

3. **The skill will guide you through**:
   - Identifying the root cause
   - Reviewing the entire module for related issues
   - Implementing comprehensive fixes
   - Verifying all issues are resolved

## Error Categories Covered

- **Import/Dependency Errors**: ModuleNotFoundError, ImportError
- **Type Errors**: TypeError, type mismatches
- **Attribute/Name Errors**: AttributeError, NameError
- **Index/Key Errors**: IndexError, KeyError
- **File/IO Errors**: FileNotFoundError, PermissionError
- **Network Errors**: ConnectionError, TimeoutError
- **Database Errors**: OperationalError, IntegrityError
- **Memory Errors**: MemoryError, resource exhaustion
- **Concurrency Errors**: Race conditions, deadlocks
- **Configuration Errors**: Missing or invalid config

## Benefits

✅ **Eliminates recurring bugs** by fixing root causes
✅ **Improves code quality** through comprehensive module reviews
✅ **Saves time** with systematic debugging approach
✅ **Prevents future issues** with defensive programming additions
✅ **Knowledge transfer** through extensive error pattern documentation
✅ **Cross-language support** with multiple debugging checklists

## Installation

The skill is packaged as `error-root-analyzer.skill` and ready to use with your AI coding assistant.

---

Created: 2026-01-23
Version: 1.0
