# Search Patterns Cookbook

## Finding Static Values

### Constants and Tokens
```bash
# Named constants
grep -r "const [A-Z_]*\s*=" --include="*.ts" --include="*.tsx"

# String literals assigned to constants
grep -r "const.*=.*['\"]" --include="*.ts" apps/

# Export constants
grep -r "export const [A-Z]" --include="*.ts"
```

### Environment Variables
```bash
# Vite env vars (client-side)
grep -r "import\.meta\.env\." --include="*.ts" --include="*.tsx"

# Deno env vars (Edge Functions)
grep -r "Deno\.env\.get" supabase/functions/

# All env usage
grep -rE "(import\.meta\.env|Deno\.env|process\.env)" .
```

### Configuration Values
```bash
# Config file values
grep -r "config\." apps/raamattu-nyt/src/lib/config.ts

# Default values in code
grep -r "DEFAULT_\|default:" --include="*.ts"
```

## Finding Functions

### React Hooks
```bash
# Custom hook definitions
grep -r "^export.*function use\|^export const use" --include="*.ts" --include="*.tsx"

# Hook usage
grep -r "const.*= use[A-Z]" --include="*.tsx"

# Specific hook
grep -r "useAIQuota\|usePlanInfo" --include="*.ts" --include="*.tsx"
```

### Service Functions
```bash
# Async function exports
grep -r "export async function\|export const.*= async" apps/*/src/lib/

# Named function in file
grep "^export.*function\|^export const" <file_path>
```

### Edge Function Handlers
```bash
# Deno.serve handlers
grep -r "Deno\.serve" supabase/functions/

# Function entry points
ls supabase/functions/*/index.ts
```

## Finding Database Usage

### Supabase Tables
```bash
# All table queries
grep -roh "\.from(['\"][^'\"]*['\"])" apps/ | sort -u

# Specific table
grep -r "\.from(['\"]profiles['\"])" --include="*.ts"

# Schema-specific queries
grep -r "schema(['\"]bible_schema['\"])" --include="*.ts"
```

### RPC Functions
```bash
# All RPC calls
grep -roh "\.rpc(['\"][^'\"]*['\"])" apps/ | sort -u

# Specific RPC
grep -r "\.rpc(['\"]check_ai_quota['\"])" --include="*.ts"
```

### Mutations
```bash
# Insert operations
grep -r "\.insert\(" --include="*.ts"

# Update operations
grep -r "\.update\(" --include="*.ts"

# Delete operations
grep -r "\.delete\(" --include="*.ts"
```

## Finding React Query Usage

### Query Keys
```bash
# All query keys
grep -roh "queryKey: \[.*\]" apps/ | sort -u

# Specific key pattern
grep -r "queryKey.*admin" --include="*.ts" --include="*.tsx"
```

### Query Definitions
```bash
# useQuery calls
grep -r "useQuery\({" --include="*.ts" --include="*.tsx"

# useMutation calls
grep -r "useMutation\({" --include="*.ts" --include="*.tsx"
```

## Finding Routes

### App Routes
```bash
# Route definitions
grep -r "<Route.*path=" apps/raamattu-nyt/src/App.tsx

# Navigation links
grep -r "navigate\(['\"]/" --include="*.tsx"

# Link components
grep -r "<Link to=" --include="*.tsx"
```

## Finding Components

### Component Definitions
```bash
# Function components
grep -r "^const.*=.*\(\).*=>" --include="*.tsx" | grep -v "test\|spec"

# Component exports
grep -r "^export.*const.*=" --include="*.tsx" apps/*/src/components/
```

### Component Usage
```bash
# Specific component
grep -r "<BibleReader" --include="*.tsx"

# Components from package
grep -r "from ['\"]@ui/" --include="*.tsx"
```

## Finding Types

### Type Definitions
```bash
# Interface definitions
grep -r "^interface\|^export interface" --include="*.ts"

# Type definitions
grep -r "^type\|^export type" --include="*.ts"

# Enum definitions
grep -r "^enum\|^export enum" --include="*.ts"
```

### Generated Types
```bash
# Supabase types
grep -r "Database\[" apps/*/src/integrations/supabase/types.ts
```

## Finding Imports/Exports

### Module Exports
```bash
# All exports from file
grep "^export" <file_path>

# Default exports
grep "^export default" --include="*.ts" --include="*.tsx"
```

### Import Patterns
```bash
# Imports from specific package
grep -r "from ['\"]@shared-auth" --include="*.ts" --include="*.tsx"

# Supabase imports
grep -r "from.*supabase" --include="*.ts"
```

## Finding Test Files

```bash
# Test files
find . -name "*.test.ts" -o -name "*.test.tsx" -o -name "*.spec.ts"

# Tests for specific file
ls apps/*/src/**/*.test.ts 2>/dev/null
```

## Multi-Pattern Searches

### Find All Feature Touchpoints
```bash
# Everything related to "quota"
grep -ri "quota" --include="*.ts" --include="*.tsx" --include="*.sql"

# Everything related to "topic"
grep -ri "topic" --include="*.ts" --include="*.tsx" apps/*/src/ | grep -v node_modules
```

### Find Dead Code Candidates
```bash
# Exported but possibly unused
grep -r "^export const\|^export function" --include="*.ts" | cut -d: -f2 | sort -u
```
