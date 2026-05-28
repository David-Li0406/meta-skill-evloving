# Refactor Issue Page State Management

Move behavior-specific Jotai atoms from the page-level state.ts to behavior-local state files for better organization.

# Functional Specification

## Behavior: View Code

Directory: `app/client/issues/[id]/behaviors/view-code/`

### Changes

#### State Location
- Before: Atoms defined in `app/client/issues/[id]/state.ts`
- After: Atoms defined in `behaviors/view-code/state.ts`

#### Affected Modules
- hooks/use-code-tree.ts - Update import path
- hooks/use-code-file.ts - Update import path

#### Moved Atoms
- `codeTreeState`
- `selectedFileState`
- `fileContentCacheState`
- `codeTabLoadingState`
- `CodeTabFile` (type)

### Rules

#### No Behavior Change
- When:
  - Atoms are moved to behavior-local state
- Then:
  - All existing functionality remains identical
  - Components using these atoms work without changes

---

## Behavior: View Plan

Directory: `app/client/issues/[id]/behaviors/plan/`

### Changes

#### State Location
- Before: Atoms defined in `app/client/issues/[id]/state.ts`
- After: Atoms defined in `behaviors/plan/state.ts`

#### Affected Modules
- view-plan/hooks/use-view-plan.ts - Update import path
- edit-plan/use-editor.ts - Update import path

#### Moved Atoms
- `viewPlanLoadingState`
- `viewPlanErrorState`
- `DocumentType` (interface)

### Rules

#### No Behavior Change
- When:
  - Atoms are moved to behavior-local state
- Then:
  - All existing functionality remains identical
  - Components using these atoms work without changes

---

# Technical Specification

## behaviors/view-code/state.ts

```typescript
'use client';

import { atom } from 'jotai';

export type CodeTabFile = {
  id: string;
  name: string;
  path: string;
  type: 'file' | 'directory';
  children?: CodeTabFile[];
  expanded?: boolean;
};

export const codeTreeState = atom<CodeTabFile[]>([]);
export const selectedFileState = atom<string | null>(null);
export const fileContentCacheState = atom<Map<string, string>>(new Map());
export const codeTabLoadingState = atom<boolean>(false);
```

## behaviors/plan/state.ts

```typescript
'use client';

import { atom } from 'jotai';

export interface DocumentType {
  title: string;
  content: string;
}

export const viewPlanLoadingState = atom<boolean>(false);
export const viewPlanErrorState = atom<string | null>(null);
```

## Import Changes

### use-code-tree.ts
```typescript
// Before
import { codeTreeState, selectedFileState } from '../../../../state';

// After
import { codeTreeState, selectedFileState } from '../state';
```

### use-view-plan.ts
```typescript
// Before
import { viewPlanLoadingState, viewPlanErrorState } from '../../../../state';

// After
import { viewPlanLoadingState, viewPlanErrorState } from '../../state';
```

---

# Tasks

- [ ] Create behavior-local state files
  - [ ] Create `behaviors/view-code/state.ts`
  - [ ] Create `behaviors/plan/state.ts`
- [ ] Update view-code behavior imports
  - [ ] Update `use-code-tree.ts`
  - [ ] Update `use-code-file.ts`
- [ ] Update plan behavior imports
  - [ ] Update `use-view-plan.ts`
  - [ ] Update `use-editor.ts`
- [ ] Remove from page state.ts
  - [ ] Remove CODE TAB STATE section
  - [ ] Remove PLAN STATE section
- [ ] Verify
  - [ ] Run `npm run typecheck`
