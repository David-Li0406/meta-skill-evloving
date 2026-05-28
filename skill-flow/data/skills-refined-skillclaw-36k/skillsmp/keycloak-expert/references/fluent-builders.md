# Fluent Builder API Reference

## Table of Contents
1. [FluentRealmBuilder](#fluentrealmbuilder)
2. [FluentClientBuilder](#fluentclientbuilder)
3. [FluentRoleBuilder](#fluentrolebuilder)
4. [FluentAzureIdpBuilder](#fluentazureidpbuilder)
5. [FluentAbacBuilder](#fluentabacbuilder)
6. [AbacConfiguration](#abacconfiguration)

## FluentRealmBuilder

Creates and configures Keycloak realms with security settings.

### Usage Pattern
```java
FluentRealmBuilder.create()
    .with(keycloakClient)
    .createRealm("my-realm")
        // Configuration methods
        .and()
    .apply();
```

### Realm Configuration Methods
| Method | Description | Default |
|--------|-------------|---------|
| `.accessTokenLifespan(int seconds)` | Access token TTL | 300 |
| `.accessTokenLifespanForImplicitFlow(int seconds)` | Implicit flow token TTL | 900 |
| `.ssoSessionIdleTimeout(int seconds)` | Session idle timeout | 1800 |
| `.ssoSessionMaxLifespan(int seconds)` | Max session duration | 36000 |
| `.offlineSessionIdleTimeout(int seconds)` | Offline session idle | 2592000 |
| `.accessCodeLifespan(int seconds)` | Auth code validity | 60 |
| `.accessCodeLifespanUserAction(int seconds)` | User action timeout | 300 |
| `.enabled(boolean)` | Realm enabled | true |
| `.sslRequired(String mode)` | SSL mode (all/external/none) | external |
| `.registrationAllowed(boolean)` | Allow self-registration | false |
| `.rememberMe(boolean)` | Remember me feature | false |
| `.verifyEmail(boolean)` | Email verification | false |
| `.loginWithEmailAllowed(boolean)` | Login with email | true |
| `.resetPasswordAllowed(boolean)` | Password reset | false |
| `.bruteForceProtected(boolean)` | Brute force protection | true |

### Complete Example
```java
FluentRealmBuilder.create()
    .with(keycloakClient)
    .createRealm("toolbox")
        .accessTokenLifespan(1200)           // 20 minutes
        .accessTokenLifespanForImplicitFlow(900)
        .ssoSessionIdleTimeout(1800)         // 30 min idle
        .ssoSessionMaxLifespan(36000)        // 10 hours max
        .offlineSessionIdleTimeout(2592000)  // 30 days
        .accessCodeLifespan(60)
        .accessCodeLifespanUserAction(300)
        .enabled(true)
        .sslRequired("external")
        .registrationAllowed(false)
        .rememberMe(false)
        .verifyEmail(false)
        .loginWithEmailAllowed(true)
        .resetPasswordAllowed(false)
        .bruteForceProtected(true)
        .and()
    .apply();
```

## FluentClientBuilder

Creates and configures OAuth/OIDC clients.

### Client Types
| Type | Description | Use Case |
|------|-------------|----------|
| Public | No client secret | SPAs, mobile apps |
| Confidential | Has client secret | Server-side apps |
| Bearer-only | Only validates tokens | APIs/resource servers |

### Usage Pattern
```java
FluentClientBuilder.forRealm("my-realm")
    .with(keycloakClient)
    .createClient("my-client")
        // Configuration methods
        .and()
    .apply();
```

### Client Configuration Methods
| Method | Description |
|--------|-------------|
| `.withDisplayName(String)` | Human-readable name |
| `.withRootUrl(String)` | Base URL |
| `.withAdminUrl(String)` | Admin URL |
| `.addRedirectUri(String)` | Add redirect URI |
| `.addWebOrigin(String)` | Add CORS origin |
| `.publicClient()` | Make public client |
| `.confidentialClient()` | Make confidential client |
| `.enableStandardFlow()` | Enable auth code flow |
| `.enableDirectAccessGrants()` | Enable password grant |
| `.disableDirectAccessGrants()` | Disable password grant |
| `.enableImplicitFlow()` | Enable implicit flow |
| `.enableServiceAccounts()` | Enable service account |
| `.enableAuthorizationServices()` | Enable ABAC |
| `.enablePKCE()` | Enable PKCE (S256) |
| `.withAccessTokenLifespan(int)` | Override token TTL |
| `.withAttribute(String key, String value)` | Custom attribute |

### Complete Example
```java
FluentClientBuilder.forRealm("toolbox")
    .with(keycloakClient)
    
    // Web application client
    .createClient("toolbox-webui")
        .withDisplayName("Toolbox UI")
        .withRootUrl("https://toolbox.example.com")
        .addRedirectUri("https://toolbox.example.com/auth/callback/keycloak")
        .addRedirectUri("http://localhost:3000/auth/callback/keycloak")
        .addWebOrigin("*")
        .confidentialClient()
        .enableStandardFlow()
        .disableDirectAccessGrants()
        .enableServiceAccounts()
        .enableAuthorizationServices()
        .and()
    
    // API client (bearer-only)
    .createClient("toolbox-api")
        .withDisplayName("Toolbox API")
        .publicClient()  // or bearer-only config
        .and()
    
    .apply();
```

## FluentRoleBuilder

Creates realm roles and composite role hierarchies.

### Usage Pattern
```java
FluentRoleBuilder.forRealm("my-realm")
    .with(keycloakClient)
    .createRole("role-name")
        .withDescription("Description")
        .and()
    .createCompositeRole("composite-name")
        .addRealmRole("role1")
        .addClientRole("client", "clientRole")
        .and()
    .setDefaultRole("default-role-name")
    .apply();
```

### Role Methods
| Method | Description |
|--------|-------------|
| `.createRole(String)` | Start simple role |
| `.createCompositeRole(String)` | Start composite role |
| `.withDescription(String)` | Set description |
| `.addRealmRole(String)` | Add realm role to composite |
| `.addRealmRoles(List<String>)` | Add multiple realm roles |
| `.addClientRole(String client, String role)` | Add client role |
| `.addClientRoles(String client, List<String>)` | Add multiple client roles |
| `.setDefaultRole(String)` | Set default role for new users |

### Complete Example
```java
FluentRoleBuilder.forRealm("toolbox")
    .with(keycloakClient)
    
    // Built-in roles
    .createRole("offline_access")
        .withDescription("${role_offline-access}")
        .and()
    .createRole("uma_authorization")
        .withDescription("${role_uma_authorization}")
        .and()
    
    // Application roles
    .createRole("admin")
        .withDescription("Administrator with full access")
        .and()
    .createRole("2ndline")
        .withDescription("2nd line support")
        .and()
    .createRole("1stline")
        .withDescription("1st line support")
        .and()
    
    // Composite role combining defaults
    .createCompositeRole("default-roles-toolbox")
        .withDescription("${role_default-roles}")
        .addRealmRole("offline_access")
        .addRealmRole("uma_authorization")
        .addClientRole("account", "view-profile")
        .addClientRole("account", "manage-account")
        .and()
    
    .setDefaultRole("default-roles-toolbox")
    .apply();
```

## FluentAzureIdpBuilder

Configures Azure AD identity provider with group-to-role mapping.

### Usage Pattern
```java
FluentAzureIdpBuilder.forRealm("my-realm")
    .with(keycloakClient)
    .configureAzureAD(clientId, clientSecret, tenantId)
        // Configuration methods
        .and()
    .createMapper("mapper-name")
        // Mapper configuration
        .and()
    .apply();
```

### Azure AD Configuration Methods
| Method | Description |
|--------|-------------|
| `.withAlias(String)` | IdP alias (default: "azuread") |
| `.withDisplayName(String)` | Display name in UI |
| `.withDefaultScopes(String...)` | OAuth scopes |
| `.trustEmails()` | Trust email from Azure |
| `.storeTokens()` | Store tokens in user session |
| `.enableReadTokenRole()` | Enable broker token |
| `.useJwtAuthentication()` | Use JWT client auth |
| `.withPrompt(String)` | OAuth prompt param |
| `.forceLogin()` | Force re-authentication |
| `.withDomainHint(String)` | Azure domain hint |

### Mapper Types
| Type | Method | Description |
|------|--------|-------------|
| Claim to Role | `.claimToRole()` | Map claim value to role |
| Attribute Importer | `.attributeImporter()` | Import claim as attribute |
| Username Template | `.usernameTemplate()` | Custom username format |
| Hardcoded Role | `.hardcodedRole()` | Assign fixed role |

### Complete Example
```java
FluentAzureIdpBuilder.forRealm("toolbox")
    .with(keycloakClient)
    .configureAzureAD(azureClientId, azureClientSecret, azureTenantId)
        .withAlias("azuread")
        .withDisplayName("Azure AD")
        .withDefaultScopes("openid", "profile", "email")
        .trustEmails()
        .storeTokens()
        .and()
    
    // Map Azure AD group to admin role
    .createMapper("azure-admin-group-mapper")
        .claimToRole()
        .withSyncMode("INHERIT")
        .mapClaim("groups")
        .withClaimValue("75e220b7-2387-409f-b093-803a655ed64d")
        .toRole("admin")
        .and()
    
    // Map Azure AD group to 2ndline role
    .createMapper("azure-2ndline-group-mapper")
        .claimToRole()
        .withSyncMode("INHERIT")
        .mapClaim("groups")
        .withClaimValue("9686e96f-0518-46b4-8b1f-56028ca41549")
        .toRole("2ndline")
        .and()
    
    .apply();
```

## FluentAbacBuilder

Creates complete ABAC configuration with resources, policies, and permissions.

### Usage Pattern
```java
FluentAbacBuilder.forClient("realm", "client")
    .with(abacConfiguration)
    .enableAuthorization(PolicyEnforcementMode.ENFORCING)
    .createResource("resource-name")
        // Resource config
        .and()
    .createPolicy("policy-name")
        // Policy config
        .and()
    .createPermission("permission-name")
        // Permission config
        .and()
    .apply();
```

### Resource Methods
| Method | Description |
|--------|-------------|
| `.withDisplayName(String)` | Human-readable name |
| `.withType(String)` | Resource type URN |
| `.withUris(String...)` | Associated URIs |
| `.withScopes(String...)` | Available scopes |
| `.ownerManagedAccess(boolean)` | User-managed permissions |

### Policy Methods
| Method | Description |
|--------|-------------|
| `.requireRoles(String...)` | Role-based policy |
| `.requireGroups(String...)` | Group-based policy |
| `.requireUsers(String...)` | User-based policy |
| `.withJavaScript(String)` | JavaScript policy |
| `.duringBusinessHours()` | 9-17 time policy |
| `.combining(String...)` | Aggregate policy |
| `.withStrategy(DecisionStrategy)` | Aggregate strategy |

### Permission Methods
| Method | Description |
|--------|-------------|
| `.onResource(String)` | Target resource |
| `.onScopes(String...)` | Target scopes only |
| `.withPolicies(String...)` | Applied policies |
| `.withDescription(String)` | Description |

### Complete Example
```java
FluentAbacBuilder.forClient("toolbox", "toolbox-webui")
    .with(abacConfiguration)
    .enableAuthorization(PolicyEnforcementMode.ENFORCING)
    
    // Resources
    .createResource("Default Resource")
        .withDisplayName("Default Resource")
        .withType("urn:toolbox-webui:resources:default")
        .withUris("/*")
        .and()
    
    .createResource("mailtemplate")
        .withDisplayName("mailtemplate")
        .withType("urn:toolbox:resources:mailtemplate")
        .withScopes("view")
        .and()
    
    // Policies
    .createPolicy("admin-policy")
        .withDescription("Admin access policy")
        .requireRoles("admin")
        .and()
    
    .createPolicy("Default Policy")
        .withDescription("A policy that grants access for users in realm")
        .withJavaScript("$evaluation.grant();")
        .and()
    
    // Permissions
    .createPermission("view-mailtemplate")
        .onScopes("view")
        .withPolicies("admin-policy")
        .and()
    
    .createPermission("Default Permission")
        .onResource("Default Resource")
        .withDescription("Default resource permission")
        .withPolicies("Default Policy")
        .and()
    
    .apply();
```

## AbacConfiguration

Low-level ABAC configuration class (used by FluentAbacBuilder).

### Direct Usage
```java
AbacConfiguration abac = new AbacConfiguration(keycloakClient);

// Enable authorization
abac.configureClientAuthorizationSettings(
    "realm", "client",
    PolicyEnforcementMode.ENFORCING,
    DecisionStrategy.UNANIMOUS
);

// Create resource
String resourceId = abac.createResource(
    "realm", "client", "resource-name",
    "Display Name", "urn:type", List.of("/api/*"),
    false, List.of("view", "edit")
);

// Create role policy
String policyId = abac.createRolePolicy(
    "realm", "client", "admin-policy",
    "Admin access", List.of("admin")
);

// Create permission
abac.createResourcePermission(
    "realm", "client", "admin-access",
    "Admin permission", resourceId,
    List.of(scopeId), List.of(policyId)
);
```

### Policy Types
| Method | Parameters |
|--------|------------|
| `createRolePolicy()` | realmName, clientId, name, description, roles |
| `createUserPolicy()` | realmName, clientId, name, description, userIds |
| `createGroupPolicy()` | realmName, clientId, name, description, groupPaths |
| `createJavaScriptPolicy()` | realmName, clientId, name, description, code |
| `createAggregatePolicy()` | realmName, clientId, name, description, policyIds, strategy |
