# Apache Flink

**Category**: apache
**Description**: Stream processing framework for distributed data processing
**Homepage**: https://flink.apache.org

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### PYPI
*PyFlink packages*

- `apache-flink` - PyFlink core
- `apache-flink-libraries` - Flink libraries

#### MAVEN
*Flink Java/Scala dependencies*

- `org.apache.flink:flink-streaming-java` - Streaming API
- `org.apache.flink:flink-clients` - Flink clients
- `org.apache.flink:flink-table-api-java` - Table API
- `org.apache.flink:flink-connector-kafka` - Kafka connector
- `org.apache.flink:flink-connector-jdbc` - JDBC connector
- `org.apache.flink:flink-connector-elasticsearch7` - Elasticsearch connector
- `org.apache.flink:flink-runtime` - Flink runtime
- `org.apache.flink:flink-sql-client` - SQL client

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Flink usage*

- `flink-conf.yaml` - Flink configuration
- `log4j.properties` - Logging configuration
- `masters` - Flink masters file
- `workers` - Flink workers file

### Import Patterns

#### Python
Extensions: `.py`

**Pattern**: `^from\s+pyflink\s+import`
- PyFlink import
- Example: `from pyflink.datastream import StreamExecutionEnvironment`

**Pattern**: `^from\s+pyflink\.table\s+import`
- PyFlink Table API import
- Example: `from pyflink.table import TableEnvironment`

#### Java
Extensions: `.java`

**Pattern**: `import\s+org\.apache\.flink\.`
- Flink Java import
- Example: `import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;`

#### Scala
Extensions: `.scala`

**Pattern**: `import\s+org\.apache\.flink\.`
- Flink Scala import
- Example: `import org.apache.flink.streaming.api.scala._`

### Code Patterns

**Pattern**: `StreamExecutionEnvironment|TableEnvironment`
- Flink environment creation
- Example: `StreamExecutionEnvironment.getExecutionEnvironment()`

**Pattern**: `FLINK_HOME|FLINK_CONF_DIR`
- Flink environment variables
- Example: `FLINK_HOME=/opt/flink`

**Pattern**: `:8081|/flink-web/`
- Flink web UI
- Example: `http://localhost:8081`

**Pattern**: `flink run|flink savepoint`
- Flink CLI commands
- Example: `flink run -c com.example.Job job.jar`

---

## Environment Variables

- `FLINK_HOME` - Flink installation directory
- `FLINK_CONF_DIR` - Configuration directory
- `FLINK_BIN_DIR` - Binary directory
- `FLINK_LIB_DIR` - Library directory
- `FLINK_PLUGINS_DIR` - Plugins directory

## Detection Notes

- Default web UI port is 8081
- Often used with Kafka for streaming
- Table API provides SQL-like interface
- PyFlink is the Python API
- Checkpointing enables fault tolerance

---

## Secrets Detection

### Credentials

#### Flink S3 Credentials
**Pattern**: `s3\.access-key\s*[=:]\s*['"]?([A-Z0-9]{20})['"]?`
**Severity**: critical
**Description**: AWS access key in Flink S3 config
**Example**: `s3.access-key: AKIAIOSFODNN7EXAMPLE`

---

## TIER 3: Configuration Extraction

### Job Manager Address Extraction

**Pattern**: `jobmanager\.rpc\.address\s*[=:]\s*['"]?([^\s'"]+)['"]?`
- Job Manager address
- Extracts: `jobmanager_address`
- Example: `jobmanager.rpc.address: localhost`
