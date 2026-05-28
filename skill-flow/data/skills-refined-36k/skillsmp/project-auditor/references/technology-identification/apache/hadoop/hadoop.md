# Apache Hadoop

**Category**: apache
**Description**: Framework for distributed storage and processing of big data
**Homepage**: https://hadoop.apache.org

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### PYPI
*Hadoop Python packages*

- `pydoop` - Python interface to Hadoop
- `hdfs` - HDFS client
- `snakebite` - Pure Python HDFS client
- `mrjob` - MapReduce jobs from Python

#### MAVEN
*Hadoop Java dependencies*

- `org.apache.hadoop:hadoop-common` - Common utilities
- `org.apache.hadoop:hadoop-hdfs` - HDFS
- `org.apache.hadoop:hadoop-hdfs-client` - HDFS client
- `org.apache.hadoop:hadoop-mapreduce-client-core` - MapReduce
- `org.apache.hadoop:hadoop-yarn-client` - YARN client
- `org.apache.hadoop:hadoop-aws` - AWS integration

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Hadoop usage*

- `core-site.xml` - Core Hadoop configuration
- `hdfs-site.xml` - HDFS configuration
- `mapred-site.xml` - MapReduce configuration
- `yarn-site.xml` - YARN configuration
- `hadoop-env.sh` - Environment variables
- `slaves` - Worker nodes file

### Import Patterns

#### Java
Extensions: `.java`

**Pattern**: `import\s+org\.apache\.hadoop\.`
- Hadoop Java import
- Example: `import org.apache.hadoop.fs.FileSystem;`

**Pattern**: `import\s+org\.apache\.hadoop\.hdfs\.`
- HDFS import
- Example: `import org.apache.hadoop.hdfs.DistributedFileSystem;`

### Code Patterns

**Pattern**: `hdfs://|HADOOP_HOME|HADOOP_CONF_DIR`
- Hadoop URLs and environment
- Example: `hdfs://namenode:9000/path`

**Pattern**: `fs\.defaultFS|dfs\.namenode`
- HDFS configuration properties
- Example: `fs.defaultFS=hdfs://localhost:9000`

**Pattern**: `:9000|:9870|:8088`
- Hadoop default ports
- Example: `hdfs://namenode:9000`

**Pattern**: `FileSystem\.get\(|Path\(`
- Hadoop FileSystem API
- Example: `FileSystem.get(conf)`

---

## Environment Variables

- `HADOOP_HOME` - Hadoop installation directory
- `HADOOP_CONF_DIR` - Configuration directory
- `HADOOP_CLASSPATH` - Additional classpath
- `HADOOP_USER_NAME` - Hadoop user name
- `HDFS_NAMENODE_USER` - NameNode user
- `HDFS_DATANODE_USER` - DataNode user
- `YARN_RESOURCEMANAGER_USER` - ResourceManager user
- `YARN_NODEMANAGER_USER` - NodeManager user

## Detection Notes

- HDFS is the distributed file system
- YARN is the resource manager
- MapReduce is the processing framework
- Often paired with Hive, Pig, or Spark
- Cloud variants: EMR (AWS), Dataproc (GCP), HDInsight (Azure)

---

## Secrets Detection

### Credentials

#### HDFS Delegation Token
**Pattern**: `(?:hdfs|HDFS).*(?:token|TOKEN)\s*[=:]\s*['"]?([A-Za-z0-9+/=]{50,})['"]?`
**Severity**: high
**Description**: HDFS delegation token

#### Hadoop S3A Credentials
**Pattern**: `fs\.s3a\.access\.key\s*[=:]\s*['"]?([A-Z0-9]{20})['"]?`
**Severity**: critical
**Description**: S3A access key in Hadoop config
**Example**: `fs.s3a.access.key=AKIAIOSFODNN7EXAMPLE`

---

## TIER 3: Configuration Extraction

### NameNode Address Extraction

**Pattern**: `(?:fs\.defaultFS|fs\.default\.name)\s*[=:]\s*['"]?(hdfs://[^\s'"]+)['"]?`
- HDFS NameNode address
- Extracts: `namenode_address`
- Example: `fs.defaultFS=hdfs://namenode:9000`
