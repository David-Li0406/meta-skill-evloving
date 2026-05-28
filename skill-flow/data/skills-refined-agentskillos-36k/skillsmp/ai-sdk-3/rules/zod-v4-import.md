# Rule: zod-v4-import (ARCHIVED)

**Status:** ARCHIVED - No longer applicable

## Context

This rule was created when the repo used Zod 3.25.x, which shipped both Zod v3 and v4. The `/v4` subpath was required to get Zod 4's optimized types that work with AI SDK v6's recursive generics.

## Current State

The repo now uses **Zod 4.x** (4.3.5+) directly. Standard imports work:

```typescript
import { z } from 'zod'
```

No special import path needed. Zod 4's types are designed to work with AI SDK v6.
