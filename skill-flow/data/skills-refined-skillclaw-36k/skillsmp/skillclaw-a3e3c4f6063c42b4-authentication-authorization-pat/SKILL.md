---
name: authentication-authorization-patterns
description: Use this skill when implementing authentication and authorization in .NET applications, particularly with OpenIddict and the ABP Framework.
---

# Skill body

Master authentication and authorization patterns including OAuth 2.0, OpenID Connect, JWT tokens, refresh tokens, role-based access control (RBAC), claims-based authorization, and secure token storage.

## When to Use

- Implementing permission-based authorization
- Configuring role-based access control (RBAC)
- Adding custom claims to tokens
- Securing API endpoints
- Implementing multi-tenant authorization
- Configuring OAuth 2.0 flows

## ABP Permission System

### Define Permissions

```csharp
// Domain.Shared/Permissions/{ProjectName}Permissions.cs
public static class {ProjectName}Permissions
{
    public const string GroupName = "{ProjectName}";

    public static class {Feature1}
    {
        public const string Default = GroupName + ".{Feature1}";
        public const string Create = Default + ".Create";
        public const string Edit = Default + ".Edit";
        public const string Delete = Default + ".Delete";
        public const string Export = Default + ".Export";
    }

    public static class {Feature2}
    {
        public const string Default = GroupName + ".{Feature2}";
        public const string Create = Default + ".Create";
        public const string Edit = Default + ".Edit";
        public const string Delete = Default + ".Delete";
        public const string ViewAll = Default + ".ViewAll"; // Admin only
        public const string Cancel = Default + ".Cancel";
    }

    public static class {Feature3}
    {
        public const string Default = GroupName + ".{Feature3}";
        public const string Create = Default + ".Create";
        public const string Edit = Default + ".Edit";
        public const string Delete = Default + ".Delete";
        public const string Manage = Default + ".Manage";
    }
}
```

### Register Permission Definitions

```csharp
// Application.Contracts/Permissions/{ProjectName}PermissionDefinitionProvider.cs
public class {ProjectName}PermissionDefinitionProvider : PermissionDefinitionProvider
{
    // Implementation details...
}
```