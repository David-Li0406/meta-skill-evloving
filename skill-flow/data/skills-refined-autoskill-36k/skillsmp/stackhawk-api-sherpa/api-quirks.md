# StackHawk API Quirks

This document describes API behaviors that differ from the OpenAPI specification or require special handling.

---

## Team API - Duplicate Application Assignment

### The Issue

**Assigning the same application to multiple teams can cause unexpected errors.**

When an application is assigned to more than one team, subsequent team operations may return 500 errors—even on unrelated teams.

### Symptoms

If you see unexpected 500 errors on team operations:

```
Initial State:
  team1: [App1, App2]
  team2: [JSV, hawkling]
  team3: [JSV, hawkling]  <-- JSV and hawkling in multiple teams

Result - unrelated operations may fail:
  ❌ hawkop team add-app team1 DVWA → 500 error
  ❌ hawkop team create team4       → 500 error
```

### Key Point

The team with duplicate apps isn't necessarily the one that fails—other teams may start returning errors. This makes the issue confusing to diagnose.

### HawkOp Protection

HawkOp v0.5.0+ includes client-side checks to prevent duplicate assignments:

```bash
# This will fail with a clear error message
hawkop team add-app team2 JSV
# Error: App "JSV" is already assigned to team "team1"...

# Can override with --force (not recommended)
hawkop team add-app team2 JSV --force
```

### Best Practice

**Each application should only be assigned to one team at a time.**

To move an app between teams:
```bash
hawkop team remove-app "Old Team" "App Name"
hawkop team add-app "New Team" "App Name"
```

### Recovery

If you've accidentally created duplicate assignments:
1. Identify which apps are in multiple teams
2. Remove the app from one of the teams (or delete the duplicate team)
3. Operations should start working normally again

---

## PUT /api/v1/org/{orgId}/team/{teamId} - Team Update

### The Issue

**This is a REPLACE-ALL API, not a partial update (PATCH).**

Despite the OpenAPI spec marking `teamId` and `organizationId` as `readOnly`, the API requires ALL fields in every PUT request:

| Field | OpenAPI Says | Reality | Default if Missing |
|-------|--------------|---------|-------------------|
| `teamId` | readOnly | **Required** | `""` (causes errors) |
| `organizationId` | readOnly | **Required** | `""` (causes errors) |
| `name` | required | Required | `""` (erases name) |
| `userIds` | optional | **Required** | `[]` (removes all users) |
| `applicationIds` | optional | **Required** | `[]` (removes all apps) |

### What Can Go Wrong

If you only send the fields you want to change:

```json
// Trying to just rename a team - DON'T DO THIS
{ "name": "New Name" }
```

The API interprets missing fields as empty, potentially removing all users and apps.

### Safe Pattern

**Always fetch current state, modify locally, then PUT the complete state:**

```rust
// 1. Fetch current state
let current_team = client.get_team_fresh(&org_id, &team_id).await?;

// 2. Extract current data
let current_user_ids: Vec<String> = current_team.users.iter()
    .map(|u| u.user_id.clone()).collect();
let current_app_ids: Vec<String> = current_team.applications.iter()
    .map(|a| a.application_id.clone()).collect();

// 3. Build complete desired state
let request = UpdateTeamRequest {
    team_id: team_id.clone(),
    organization_id: org_id.clone(),
    name: Some(new_name),             // Change what you want
    user_ids: Some(current_user_ids), // Preserve what you don't
    application_ids: Some(current_app_ids),
};

// 4. PUT the complete state
client.update_team(&org_id, &team_id, request).await?;
```

### Important Notes

- **Pagination**: Large teams may require paginating users/apps before updates
- **Caching**: Use fresh reads (`get_team_fresh()`) before mutations to avoid stale data

### Code Reference

See `src/client/models/user.rs` - `UpdateTeamRequest` struct for implementation details.

---

## General Guidelines for StackHawk APIs

1. **Don't trust "readOnly" in OpenAPI** - Test actual behavior
2. **Assume PUT means REPLACE-ALL** - Always send complete state
3. **Fetch before mutate** - Get current state, modify locally, PUT back
4. **Use fresh reads** - Bypass cache before mutations
5. **Handle pagination** - Large datasets may have paginated results
