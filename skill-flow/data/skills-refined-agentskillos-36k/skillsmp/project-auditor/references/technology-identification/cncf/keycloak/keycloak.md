# Keycloak

**Category**: cncf
**Description**: Open source identity and access management
**Homepage**: https://keycloak.org

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### MAVEN
*Keycloak Java packages*

- `org.keycloak:keycloak-core` - Keycloak core
- `org.keycloak:keycloak-admin-client` - Admin client
- `org.keycloak:keycloak-services` - Services
- `org.keycloak:keycloak-server-spi` - Server SPI
- `org.keycloak:keycloak-authz-client` - Authorization client

#### NPM
*Keycloak Node.js packages*

- `keycloak-connect` - Node.js adapter
- `keycloak-admin-client` - Admin client
- `@keycloak/keycloak-admin-client` - Admin client (scoped)

#### PYPI
*Keycloak Python packages*

- `python-keycloak` - Python client
- `keycloak` - Keycloak SDK

#### GO
*Keycloak Go packages*

- `github.com/Nerzal/gocloak/v13` - Go client

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Keycloak usage*

- `keycloak.conf` - Keycloak configuration
- `keycloak.json` - Adapter configuration
- `realm-export.json` - Realm export
- `standalone.xml` - JBoss configuration (legacy)

### Code Patterns

**Pattern**: `keycloak\.org/|keycloak-`
- Keycloak references
- Example: `keycloak.org/operator/v2alpha1`

**Pattern**: `kind:\s*(Keycloak|KeycloakRealm|KeycloakClient|KeycloakUser)`
- Keycloak Operator CRDs
- Example: `kind: Keycloak`

**Pattern**: `auth-server-url|realm|resource|credentials`
- Keycloak adapter config
- Example: `"auth-server-url": "http://localhost:8080"`

**Pattern**: `:8080/realms/|/auth/realms/|/protocol/openid-connect`
- Keycloak endpoints
- Example: `http://localhost:8080/realms/master`

**Pattern**: `bearer-only|public-client|confidential`
- Client types
- Example: `"public-client": true`

**Pattern**: `keycloak\.init|keycloak\.login|keycloak\.token`
- Keycloak JS methods
- Example: `keycloak.init({ onLoad: 'login-required' })`

**Pattern**: `KeycloakService|KeycloakAuthGuard`
- Keycloak integration services
- Example: `KeycloakService`

**Pattern**: `sso_url|logout_url|jwks_uri`
- Keycloak OIDC endpoints
- Example: `jwks_uri`

---

## Environment Variables

- `KEYCLOAK_ADMIN` - Admin username
- `KEYCLOAK_ADMIN_PASSWORD` - Admin password
- `KC_DB` - Database type
- `KC_DB_URL` - Database URL
- `KC_HOSTNAME` - Hostname
- `KC_HTTP_ENABLED` - HTTP enabled
- `KC_PROXY` - Proxy mode

## Detection Notes

- OIDC and SAML identity provider
- Realm-based multi-tenancy
- Keycloak Operator for Kubernetes
- Quarkus-based from version 17+
- Admin console on /admin

---

## Secrets Detection

### Credentials

#### Client Secret
**Pattern**: `(client[_-]?secret|credentials\.secret)\s*[=:]\s*['"]([a-zA-Z0-9_-]{8,})['"]`
**Severity**: critical
**Description**: Keycloak client secret in configuration

#### Admin Password
**Pattern**: `KEYCLOAK_ADMIN_PASSWORD\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Keycloak admin password

#### Database Password
**Pattern**: `KC_DB_PASSWORD\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Keycloak database password

---

## TIER 3: Configuration Extraction

### Realm Extraction

**Pattern**: `realm["':\s]+['"]?([a-zA-Z0-9_-]+)['"]?`
- Keycloak realm name
- Extracts: `realm`
- Example: `"realm": "my-realm"`

### Auth Server URL Extraction

**Pattern**: `auth-server-url["':\s]+['"]?(https?://[^\s'"]+)['"]?`
- Keycloak server URL
- Extracts: `auth_server_url`
- Example: `"auth-server-url": "http://localhost:8080"`

### Client ID Extraction

**Pattern**: `resource["':\s]+['"]?([a-zA-Z0-9_-]+)['"]?`
- Client ID
- Extracts: `client_id`
- Example: `"resource": "my-client"`
