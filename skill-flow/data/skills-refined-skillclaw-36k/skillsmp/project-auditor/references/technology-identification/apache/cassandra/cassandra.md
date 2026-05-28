# Apache Cassandra

**Category**: apache
**Description**: Distributed NoSQL database for high availability and scalability
**Homepage**: https://cassandra.apache.org

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Cassandra Node.js drivers*

- `cassandra-driver` - DataStax Node.js driver
- `express-cassandra` - Cassandra ORM for Express
- `cassandra-store` - Session store for Cassandra

#### PYPI
*Cassandra Python drivers*

- `cassandra-driver` - DataStax Python driver
- `acsylla` - Async Cassandra driver
- `cassandra-migrate` - Migration tool

#### GO
*Cassandra Go drivers*

- `github.com/gocql/gocql` - GoCQL driver
- `github.com/scylladb/gocqlx` - GoCQL extensions

#### MAVEN
*Cassandra Java drivers*

- `com.datastax.oss:java-driver-core` - DataStax Java driver
- `com.datastax.cassandra:cassandra-driver-core` - Legacy driver
- `org.apache.cassandra:cassandra-all` - Cassandra server

#### RUBYGEMS
*Cassandra Ruby drivers*

- `cassandra-driver` - DataStax Ruby driver
- `cequel` - Cassandra ORM

#### NUGET
*Cassandra .NET drivers*

- `CassandraCSharpDriver` - DataStax C# driver

#### CARGO
*Cassandra Rust drivers*

- `scylla` - ScyllaDB/Cassandra driver
- `cdrs-tokio` - Cassandra driver for Rust

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Cassandra usage*

- `cassandra.yaml` - Main Cassandra configuration
- `cassandra-env.sh` - Environment configuration
- `cassandra-rackdc.properties` - Rack/DC configuration
- `cassandra-topology.properties` - Topology configuration
- `cqlshrc` - CQLSH configuration

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`

**Pattern**: `from\s+['"]cassandra-driver['"]`
- Cassandra driver import
- Example: `import { Client } from 'cassandra-driver';`

**Pattern**: `require\(['"]cassandra-driver['"]\)`
- Cassandra driver require
- Example: `const cassandra = require('cassandra-driver');`

#### Python
Extensions: `.py`

**Pattern**: `^from\s+cassandra\.cluster\s+import`
- Cassandra cluster import
- Example: `from cassandra.cluster import Cluster`

**Pattern**: `^from\s+cassandra\.auth\s+import`
- Cassandra auth import
- Example: `from cassandra.auth import PlainTextAuthProvider`

#### Go
Extensions: `.go`

**Pattern**: `"github\.com/gocql/gocql"`
- GoCQL import
- Example: `import "github.com/gocql/gocql"`

#### Java
Extensions: `.java`

**Pattern**: `import\s+com\.datastax\.`
- DataStax driver import
- Example: `import com.datastax.oss.driver.api.core.CqlSession;`

### Code Patterns

**Pattern**: `Cluster\.connect\(|CqlSession\.builder\(`
- Cassandra connection
- Example: `Cluster.builder().addContactPoint('localhost').build()`

**Pattern**: `cql://|contact[_-]?points|CASSANDRA_HOST`
- Cassandra connection patterns
- Example: `CASSANDRA_HOST=cassandra.example.com`

**Pattern**: `:9042|:9160`
- Cassandra default ports
- Example: `localhost:9042`

**Pattern**: `CREATE\s+KEYSPACE|USE\s+\w+;|CREATE\s+TABLE.*PRIMARY\s+KEY`
- CQL statements
- Example: `CREATE KEYSPACE mykeyspace WITH replication = {...}`

**Pattern**: `datastax\.(cloud|com)|astra\.datastax\.com`
- DataStax Astra (cloud Cassandra)
- Example: `https://abc-xyz.apps.astra.datastax.com`

---

## Environment Variables

- `CASSANDRA_HOST` - Cassandra host
- `CASSANDRA_HOSTS` - Comma-separated hosts
- `CASSANDRA_PORT` - Cassandra port
- `CASSANDRA_KEYSPACE` - Default keyspace
- `CASSANDRA_USERNAME` - Authentication username
- `CASSANDRA_PASSWORD` - Authentication password
- `CASSANDRA_DATACENTER` - Local datacenter
- `ASTRA_DB_ID` - DataStax Astra database ID
- `ASTRA_DB_REGION` - Astra region
- `ASTRA_DB_APPLICATION_TOKEN` - Astra application token

## Detection Notes

- Default CQL port is 9042
- DataStax drivers are the standard clients
- ScyllaDB is API-compatible with Cassandra
- DataStax Astra is the cloud-managed offering
- CQL is similar to SQL but not identical

---

## Secrets Detection

### Credentials

#### Cassandra Password
**Pattern**: `(?:cassandra|CASSANDRA).*(?:password|PASSWORD)\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Cassandra authentication password
**Example**: `CASSANDRA_PASSWORD=secretpass`

#### DataStax Astra Token
**Pattern**: `AstraCS:[A-Za-z0-9_-]{32,}:[A-Za-z0-9_-]{32,}`
**Severity**: critical
**Description**: DataStax Astra application token
**Example**: `AstraCS:abc123:xyz456...`

#### Astra Secure Connect Bundle
**Pattern**: `secure[_-]?connect[_-]?bundle.*\.zip`
**Severity**: high
**Description**: Astra secure connect bundle (contains credentials)
**Example**: `secure-connect-database.zip`

### Validation

#### API Documentation
- **Cassandra Documentation**: https://cassandra.apache.org/doc/latest/
- **DataStax Drivers**: https://docs.datastax.com/en/driver-matrix/

---

## TIER 3: Configuration Extraction

### Contact Points Extraction

**Pattern**: `(?:contact[_-]?points?|hosts?|CASSANDRA_HOST)\s*[=:]\s*['"]?([^\s'"]+)['"]?`
- Cassandra contact points
- Extracts: `contact_points`
- Example: `CASSANDRA_HOST=node1.example.com,node2.example.com`

### Keyspace Extraction

**Pattern**: `(?:keyspace|CASSANDRA_KEYSPACE)\s*[=:]\s*['"]?([a-zA-Z_][a-zA-Z0-9_]*)['"]?`
- Cassandra keyspace name
- Extracts: `keyspace`
- Example: `keyspace=my_keyspace`

### Datacenter Extraction

**Pattern**: `(?:local[_-]?datacenter|datacenter|CASSANDRA_DATACENTER)\s*[=:]\s*['"]?([a-zA-Z0-9_-]+)['"]?`
- Local datacenter name
- Extracts: `datacenter`
- Example: `local_datacenter=datacenter1`
