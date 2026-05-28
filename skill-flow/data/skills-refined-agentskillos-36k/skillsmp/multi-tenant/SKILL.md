---
name: multi-tenant
description: Multi-tenant architecture patterns. Preload for agents working with org/team/user scoping.
user-invocable: false
---

# Multi-Tenant Architecture

## Hierarchy

```
Organization (tenant boundary)
├── OrganizationMember (user ↔ org, role: OWNER|ADMIN|MEMBER)
├── Team
│   └── TeamMember (org_member ↔ team, role: ADMIN|MEMBER|VIEWER)
└── Resources scoped by: organization_id + team_id + user_id
```

## Critical FK Pattern

```python
# TeamMember links to OrganizationMember, NOT User
class TeamMember(SQLModel, table=True):
    org_member_id: UUID = Field(foreign_key="organization_member.id")
```

## Query Scoping (REQUIRED)

```python
# ALWAYS filter by organization
statement = select(Resource).where(
    Resource.organization_id == org_context.organization.id,
    Resource.deleted_at == None,  # noqa: E711
)

# Add team scope for team resources
statement = statement.where(Resource.team_id == team_context.team.id)
```

## Settings Hierarchy

```
Organization (defaults)
    ↓ overrides
Team (if allow_team_customization)
    ↓ overrides
User (if allow_user_customization)
```

## RBAC Roles

| Org Role | Permissions |
|----------|-------------|
| OWNER | All + delete org + transfer ownership |
| ADMIN | Manage members, teams, settings |
| MEMBER | Minimal access |

| Team Role | Permissions |
|-----------|-------------|
| ADMIN | All team management |
| MEMBER | Standard access |
| VIEWER | Read-only |
