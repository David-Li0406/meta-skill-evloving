# Workflow Integration

How context verification integrates with the implementation workflow.

## Step 2.6: Context Verification in Implementation Executor

Before delegating to any specialist, the implementation-executor MUST verify context:

### 1. Identify Namespace

```bash
# What namespace am I working in?
- Admin namespace (app/controllers/admins/, app/views/admins/)
- Client namespace (app/controllers/clients/, app/views/clients/)
- API namespace (app/controllers/api/)
- Public namespace (app/controllers/)
```

### 2. Search for Existing Patterns

```bash
# Authentication helpers
rg "def current_" app/controllers/

# signed_in? helpers
rg "signed_in\?" app/views/[namespace]/

# Route patterns
rails routes | grep [namespace]

# before_actions
rg "before_action" app/controllers/[namespace]/base_controller.rb
```

### 3. Extract Verified Names

- Authentication helper: [verified from search]
- Routes prefix: [verified from search]
- Authorization method: [verified from search]

### 4. Pass to Specialist with Verified Context

---

## Delegation Message Format

Include Context Verification section in every delegation:

```markdown
**Context Verification:**
Namespace: [admin/clients/api/public]
Authentication helper: `current_administrator` (verified: app/controllers/application_controller.rb:42)
Signed-in helper: `administrator_signed_in?` (verified: app/views/admins/dashboard/_header.html.erb:12)
Route prefix: `admins_` (verified: rails routes | grep admins)
Authorization: `require_super_admin` (verified: app/controllers/admins/base_controller.rb:8)
Available instance variables: `@current_administrator` (set in before_action)

**CRITICAL:**
- DO NOT assume helper names - use ONLY the verified helpers above
- DO NOT copy patterns from other namespaces without verification
- DO NOT use helpers that aren't listed above (they don't exist)
- If you need a helper not listed, ask for it to be added first
```

---

## Per-Feature Context Tracking (Beads Integration)

Context verification results are persisted per-feature in beads comments:

```yaml
verified_context:
  namespace: admin
  auth_helper: current_administrator
  signed_in_helper: administrator_signed_in?
  route_prefix: admins_
  authorization_methods:
    - require_super_admin
    - authenticate_administrator!
  instance_variables:
    - @current_administrator
  verified_at: 2025-01-15T10:30:00Z
```

### Benefits

1. **Single verification** for entire feature (not per-phase)
2. **All specialists** reference same verified context
3. **Audit trail** of what was verified and when
4. **Quality assurance** - reviewers can verify correct usage

### Usage

When implementing any phase, check the feature beads comment for verified context and use only those exact helper/route names.

---

## Enforcement Mechanisms

### PreToolUse Hook

The `verify-assumptions.sh` hook runs **before any code generation**:

**Checks:**
1. Context verification exists in beads feature comment
2. Generated code uses only verified helpers
3. No cross-namespace assumptions
4. All route helpers match verified prefix

**Blocks if:**
- Context not verified (Step 2.6 not complete)
- Code uses unverified helpers
- Cross-namespace copying detected

**Logs:**
Violations logged to `.claude/assumption-violations.log`

### Quality Gate Validation

The Chief Reviewer validates:
- All helpers used match verified context
- No assumption patterns in generated code
- Beads comment has verified context section
- Context verification timestamp exists
