---
name: Onboard New Role
description: Systematic workflow for introducing a new User Role (e.g., 'Auditor', 'Supervisor') into the ATLAS ecosystem.
version: 1.0.0
---

# Skill: Onboard New Role

Adding a role in ATLAS is high-impact. It touches Database Enums, RLS Policies, Frontend Types, and Sidebar Logic.
Miss one, and the system breaks or becomes insecure.

## Execution Steps

### 1. Database Layer (Enum)
*Action*: Instruct user to run SQL or create migration.
```sql
-- Example for adding 'auditor'
ALTER TYPE public.app_role ADD VALUE 'auditor';
```
*Note*: This cannot be undone easily in Postgres without dropping the type. Verify spelling first.

### 2. Type Layer (`database.types.ts`)
Update the `status` or `role` enum definition in TypeScript to match the DB.

### 3. Application Constraints (`lib/auth-context.tsx`)
Check if there is any hardcoded list of roles.
- `const ALLOWED_ROLES = [...]` -> Add new role.
- Update `hasPermission(role, action)` logic if it exists.

### 4. Sidebar Visibility (`components/layout/dashboard-sidebar.tsx`)
The new role needs to see menus.
- Find the `navItems` configuration.
- Add the new role to the `roles` array of relevant items.
```typescript
{
  title: "Auditoría",
  href: "/audit",
  icon: FileSpreadsheet,
  roles: ["admin", "auditor"] // <--- Added here
}
```

### 5. RLS Policies (Security)
**CRITICAL**: The role exists but has no data access yet.
- **Tables to check**: `documents`, `sales`, `profiles`.
- **Action**: Create policies for the new role.
```sql
CREATE POLICY "Auditors can view all sales"
ON sales FOR SELECT
USING (auth.jwt() ->> 'role' = 'auditor');
```

### 6. Verification
- Can the new user log in?
- Can they see the sidebar items?
- Can they fetch the data (RLS check)?

## Agent Checklist
- [ ] DB Enum updated.
- [ ] TS Types updated.
- [ ] Sidebar Config updated.
- [ ] RLS Policies created.
