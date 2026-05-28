# Phase 1: Interface

Define the structural contracts of the system.

## Browser-Based Questions

When a collab session is active, use `render_ui` for all user interactions.

**Component selection:**
| Question Type | Component |
|--------------|-----------|
| Yes/No | Card with action buttons |
| Choose 1 of 2-5 | RadioGroup |
| Choose 1 of 6+ | MultipleChoice |
| Free text | TextInput or TextArea |

**Example - Yes/No:**
```
Tool: mcp__mermaid__render_ui
Args: {
  "project": "<cwd>",
  "session": "<session>",
  "ui": {
    "type": "Card",
    "props": { "title": "<question context>" },
    "children": [{ "type": "Markdown", "props": { "content": "<question>" } }],
    "actions": [
      { "id": "yes", "label": "Yes", "primary": true },
      { "id": "no", "label": "No" }
    ]
  },
  "blocking": true
}
```

**Terminal prompts only when:** No collab session exists (pre-session selection).

## What to Produce

1. **File paths** - List all files that will be created or modified
2. **Class and function signatures** - Names, parameters, return types
3. **Public API contracts** - How components interact with each other
4. **Type definitions** - Custom types, interfaces, enums

## Process

```bash
# Read design doc
cat .collab/<name>/documents/design.md
```

**For each component identified in design:**
1. Define the file path where it will live
2. List all public functions/methods with signatures
3. Define input/output types
4. Document how it connects to other components

## Output Format

**Create per-item interface documents** instead of adding to design.md:

For each work item N, create `interface-item-N.md`:

```
Tool: mcp__mermaid__create_document
Args: {
  "project": "<cwd>",
  "session": "<session>",
  "name": "interface-item-N",
  "content": "<interface content for item N>"
}
```

**Document structure:**

```markdown
## Interface Definition

### File Structure
- `src/auth/types.ts` - Core type definitions
- `src/auth/service.ts` - Authentication service
- `src/auth/middleware.ts` - Express middleware

### Type Definitions

```typescript
// src/auth/types.ts
interface User {
  id: string;
  email: string;
  role: 'admin' | 'user';
}

interface AuthResult {
  success: boolean;
  user?: User;
  error?: string;
}
```

### Function Signatures

```typescript
// src/auth/service.ts
class AuthService {
  authenticate(email: string, password: string): Promise<AuthResult>
  validateToken(token: string): Promise<User | null>
  revokeToken(token: string): Promise<void>
}

// src/auth/middleware.ts
function requireAuth(req: Request, res: Response, next: NextFunction): void
function requireRole(role: string): Middleware
```

### Component Interactions
- `middleware.requireAuth` calls `service.validateToken`
- `service.authenticate` returns tokens stored in Redis
```

## Verification Gate

Before moving to Phase 2, run verification:

```bash
# Trigger verify-phase hook
./hooks/verify-phase.sh interface <collab-name>
```

**Checklist:**
- [ ] All files from design are listed
- [ ] All public interfaces have signatures
- [ ] Parameter types are explicit (no `any`)
- [ ] Return types are explicit
- [ ] Component interactions are documented

**GATE: Do NOT proceed until this checklist passes.**

**If Interface phase doesn't apply** (e.g., pure config changes, docker setup):
1. Document explicitly: "N/A - [reason why interface phase doesn't apply]"
2. Add this to the design doc Interface Definition section
3. You still MUST proceed through pseudocode, skeleton, and executing-plans
4. Skipping to implementation is NEVER allowed

**Update state on success:**

```
Tool: mcp__mermaid__update_session_state
Args: { "project": "<cwd>", "session": "<name>", "phase": "rough-draft/pseudocode" }
```
Note: `lastActivity` is automatically updated by the MCP tool.

## Diagram Opportunities

**Diagrams are cheap. When in doubt, make one.**

### When to Create a Diagram

CHECK these triggers as you work:

| Trigger | Diagram Type |
|---------|--------------|
| Discussing 3+ interacting components | Architecture diagram |
| Explaining data flow | Sequence or flowchart |
| Describing state transitions | State diagram |
| Showing dependencies | Dependency graph |
| Tracing execution path | Sequence diagram |
| Debugging complex flow | Flowchart with decision points |

### How to Create

```
cwd = getCurrentWorkingDirectory()
session = getCurrentSession()

mcp__mermaid__create_diagram({
  project: cwd,
  session: session,
  name: "<descriptive-name>",
  content: "<mermaid-syntax>"
})
```

### Example Triggers for This Skill

**WHEN defining interfaces for 3+ files:**
- CREATE class diagram showing relationships

**WHEN documenting component interactions:**
- CREATE sequence diagram showing calls

**WHEN defining complex types:**
- CREATE entity-relationship diagram
