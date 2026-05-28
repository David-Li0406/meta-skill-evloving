# Code Cleanup Agent

## Patterns


---
  #### **Name**
Dead Code Archaeology
  #### **Description**
Systematically find and remove unused code through dependency analysis
  #### **When**
After feature removal or major refactoring
  #### **Example**
    1. Use ESLint unused-vars to find candidates
    2. Check git history: when was it last modified?
    3. Search codebase for imports/references
    4. Remove in isolated commit for easy revert
    5. Run full test suite to catch missed usage
    

---
  #### **Name**
Import Organization Layers
  #### **Description**
Group imports by source and purpose for scanability
  #### **When**
Organizing any file with multiple imports
  #### **Example**
    // External dependencies
    import React from 'react';
    import { z } from 'zod';
    
    // Internal libraries/utils
    import { api } from '@/lib/api';
    import { formatDate } from '@/lib/dates';
    
    // Components
    import { Button } from '@/components/ui/button';
    
    // Types
    import type { User } from '@/types';
    

---
  #### **Name**
Progressive Type Strengthening
  #### **Description**
Replace any types incrementally by improving one module at a time
  #### **When**
Improving type safety in existing codebase
  #### **Example**
    // Start with most-used utilities first
    // Define specific types for common patterns
    type ApiResponse<T> = {
      data: T;
      error?: string;
    };
    
    // Replace any incrementally
    - function process(data: any)
    + function process(data: User | Product)
    

---
  #### **Name**
Extract Constants Pattern
  #### **Description**
Pull magic numbers and strings into named constants
  #### **When**
Multiple hardcoded values that represent business logic
  #### **Example**
    // Before
    if (user.age >= 18 && user.credits > 100)
    
    // After
    const LEGAL_AGE = 18;
    const PREMIUM_THRESHOLD = 100;
    if (user.age >= LEGAL_AGE && user.credits > PREMIUM_THRESHOLD)
    

---
  #### **Name**
Split by Domain Not Lines
  #### **Description**
Break large files by business domain, not arbitrary line counts
  #### **When**
Files become hard to navigate
  #### **Example**
    // Before: user-service.ts (2000 lines)
    // After:
    // user-service/authentication.ts
    // user-service/profile.ts
    // user-service/permissions.ts
    // user-service/index.ts (exports)
    

---
  #### **Name**
Remove Backwards Compatibility
  #### **Description**
Delete compatibility shims once migration is complete
  #### **When**
After successful feature migration
  #### **Example**
    // Check git history and tracking issues
    // Verify no references to old API
    // Remove with clear commit message
    // Update changelog with breaking change if public API
    

## Anti-Patterns


---
  #### **Name**
Cleanup Without Tests
  #### **Description**
Refactoring code without test coverage to verify behavior
  #### **Why**
Cannot verify the cleanup didn't break functionality
  #### **Instead**
    1. Add tests for current behavior first
    2. Refactor
    3. Verify tests still pass
    4. If no tests possible, refactor in tiny increments
    

---
  #### **Name**
Style Cleanup in Feature Commits
  #### **Description**
Mixing cleanup changes with functional changes in same commit
  #### **Why**
Makes code review hard and rollbacks dangerous
  #### **Instead**
    Separate commits:
    - feat: Add user authentication
    - refactor: Clean up auth imports and types
    - style: Format auth files
    

---
  #### **Name**
Mass Renaming
  #### **Description**
Renaming variables/functions across entire codebase at once
  #### **Why**
High risk, hard to review, blocks other work
  #### **Instead**
    1. Add new name alongside old (deprecate old)
    2. Migrate incrementally over multiple PRs
    3. Remove old name when no references remain
    4. Or: use IDE refactor with comprehensive test suite
    

---
  #### **Name**
Premature Abstraction
  #### **Description**
Creating abstractions before patterns are clear
  #### **Why**
Wrong abstractions are worse than duplication
  #### **Instead**
    Wait for 3 uses before abstracting (Rule of Three).
    Duplication is cheaper than wrong abstraction.
    Extract when pattern is clear, not when it might be useful.
    

---
  #### **Name**
Delete Everything Unused
  #### **Description**
Removing code without understanding why it exists
  #### **Why**
Code might be unused because of timing, not because it's truly dead
  #### **Instead**
    Check: git blame, git log, linked issues
    Ask: Why was this added? Is the need still valid?
    Try: Deprecate first, delete after observation period
    

---
  #### **Name**
Cleanup Without Communication
  #### **Description**
Large refactoring PRs with no context or explanation
  #### **Why**
Reviewers cannot verify correctness without understanding intent
  #### **Instead**
    PR description should answer:
    - What was wrong?
    - What is cleaned up?
    - How to verify nothing broke?
    - Any risks or follow-ups?
    