# Vitess

**Category**: cncf
**Description**: Database clustering system for horizontal scaling of MySQL
**Homepage**: https://vitess.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### GO
*Vitess Go packages*

- `vitess.io/vitess` - Vitess core
- `vitess.io/vitess/go/vt/vtgate` - VTGate proxy
- `vitess.io/vitess/go/vt/vttablet` - VTTablet
- `vitess.io/vitess/go/vt/vtctl` - Control client

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Vitess usage*

- `vschema.json` - Vitess schema
- `vschema.yaml` - Vitess schema (YAML)
- `vtgate.yaml` - VTGate configuration
- `vttablet.yaml` - VTTablet configuration

### Code Patterns

**Pattern**: `vitess\.io|planetscale`
- Vitess references
- Example: `vitess.io/vitess`

**Pattern**: `vtgate|vttablet|vtctld|vtctl|vtadmin`
- Vitess components
- Example: `vtgate --mysql_server_port=3306`

**Pattern**: `keyspace|shard|tablet|vschema`
- Vitess concepts
- Example: `keyspace: commerce`

**Pattern**: `:15000|:15001|:15991|:15999|:3306`
- Vitess default ports
- Example: `vtgate:15991`

**Pattern**: `vindexes:|tables:|sharded:|unsharded:`
- VSchema structure
- Example: `vindexes:\n  hash:`

**Pattern**: `vtctlclient|vtctldclient`
- Vitess control clients
- Example: `vtctlclient CreateKeyspace commerce`

**Pattern**: `ApplyVSchema|ApplySchema|Reshard|MoveTables`
- Vitess operations
- Example: `vtctlclient ApplyVSchema`

**Pattern**: `mysql_server_port|cell|shard_count`
- Vitess configuration flags
- Example: `--cell=zone1`

---

## Environment Variables

- `VTGATE_HOST` - VTGate host
- `VTGATE_PORT` - VTGate port
- `VTGATE_GRPC_PORT` - VTGate gRPC port
- `VT_MYSQL_ROOT_PASSWORD` - MySQL root password
- `TOPOLOGY_FLAGS` - Topology service flags

## Detection Notes

- Horizontally scales MySQL
- VTGate is the query router
- VTTablet manages MySQL instances
- Supports sharding via vindexes
- Compatible with MySQL protocol

---

## Secrets Detection

### Credentials

#### MySQL Password
**Pattern**: `mysql.*password\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: MySQL password for Vitess

#### Topology Credentials
**Pattern**: `topology.*auth\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: high
**Description**: Topology service authentication

---

## TIER 3: Configuration Extraction

### Keyspace Extraction

**Pattern**: `keyspace['":\s]+['"]?([a-zA-Z0-9_]+)['"]?`
- Vitess keyspace name
- Extracts: `keyspace`
- Example: `keyspace: commerce`

### Cell Extraction

**Pattern**: `--cell[=\s]+['"]?([a-zA-Z0-9_-]+)['"]?`
- Vitess cell/datacenter
- Extracts: `cell`
- Example: `--cell=zone1`

### Shard Count Extraction

**Pattern**: `shard[-_]?count[=:\s]+['"]?([0-9]+)['"]?`
- Number of shards
- Extracts: `shard_count`
- Example: `shard_count: 4`
