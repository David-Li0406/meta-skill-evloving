# TiKV

**Category**: cncf
**Description**: Distributed transactional key-value database
**Homepage**: https://tikv.org

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### CARGO
*TiKV Rust packages*

- `tikv` - TiKV core
- `tikv-client` - TiKV Rust client
- `raft` - Raft implementation

#### GO
*TiKV Go packages*

- `github.com/tikv/client-go` - TiKV Go client
- `github.com/tikv/pd` - Placement Driver

#### PYPI
*TiKV Python packages*

- `tikv-client` - TiKV Python client

#### MAVEN
*TiKV Java packages*

- `org.tikv:tikv-client-java` - TiKV Java client

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate TiKV usage*

- `tikv.toml` - TiKV configuration
- `pd.toml` - Placement Driver configuration
- `tikv.yaml` - TiKV YAML config

### Code Patterns

**Pattern**: `tikv\.org|tikv-server|pd-server`
- TiKV references
- Example: `tikv-server --config tikv.toml`

**Pattern**: `TiKV|PD|Placement\s*Driver`
- TiKV component names
- Example: `Placement Driver cluster`

**Pattern**: `:2379|:2380|:20160|:20180`
- TiKV default ports
- Example: `pd-addr: "127.0.0.1:2379"`

**Pattern**: `\[server\]|\[storage\]|\[raftstore\]|\[rocksdb\]`
- TiKV config sections
- Example: `[server]\naddr = "0.0.0.0:20160"`

**Pattern**: `region|raft|coprocessor|scheduler`
- TiKV concepts
- Example: `region-split-size`

**Pattern**: `tikv-ctl|pd-ctl|tiup`
- TiKV/TiDB tools
- Example: `tikv-ctl --db /path/to/tikv`

**Pattern**: `RawKV|TxnKV`
- TiKV API modes
- Example: `RawKVClient`

---

## Environment Variables

- `TIKV_ADDR` - TiKV address
- `PD_ENDPOINTS` - Placement Driver endpoints
- `TIKV_CONFIG` - Configuration file path

## Detection Notes

- Part of TiDB ecosystem
- Uses Raft for consensus
- PD manages cluster metadata
- RocksDB as storage engine
- Supports transactions (TxnKV)

---

## Secrets Detection

### Credentials

#### TiKV Security Certificate
**Pattern**: `cert-path\s*=\s*['"]?([^\s'"]+)['"]?`
**Severity**: high
**Description**: TLS certificate path

#### TiKV Private Key
**Pattern**: `key-path\s*=\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: TLS private key path

---

## TIER 3: Configuration Extraction

### Listen Address Extraction

**Pattern**: `addr\s*=\s*['"]?([0-9.:]+)['"]?`
- TiKV listen address
- Extracts: `listen_addr`
- Example: `addr = "0.0.0.0:20160"`

### PD Endpoints Extraction

**Pattern**: `pd-endpoints\s*=\s*\[['"]?([^\]]+)['"]?\]`
- Placement Driver endpoints
- Extracts: `pd_endpoints`
- Example: `pd-endpoints = ["127.0.0.1:2379"]`

### Data Directory Extraction

**Pattern**: `data-dir\s*=\s*['"]?([^\s'"]+)['"]?`
- Data storage directory
- Extracts: `data_dir`
- Example: `data-dir = "/var/lib/tikv"`
