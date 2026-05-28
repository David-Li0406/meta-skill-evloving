# Apache Spark

**Category**: apache
**Description**: Unified analytics engine for large-scale data processing
**Homepage**: https://spark.apache.org

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### PYPI
*PySpark and related packages*

- `pyspark` - Apache Spark Python API
- `spark-nlp` - NLP library for Spark
- `sparksql-magic` - Jupyter magic for SparkSQL
- `delta-spark` - Delta Lake for Spark
- `koalas` - Pandas API on Spark (legacy)

#### MAVEN
*Spark Java/Scala dependencies*

- `org.apache.spark:spark-core_2.12` - Spark Core
- `org.apache.spark:spark-sql_2.12` - Spark SQL
- `org.apache.spark:spark-mllib_2.12` - Spark MLlib
- `org.apache.spark:spark-streaming_2.12` - Spark Streaming
- `org.apache.spark:spark-graphx_2.12` - Spark GraphX
- `org.apache.spark:spark-hive_2.12` - Spark Hive
- `io.delta:delta-core_2.12` - Delta Lake

#### SBT (Scala)
*Spark Scala dependencies*

- `org.apache.spark %% spark-core` - Spark Core
- `org.apache.spark %% spark-sql` - Spark SQL

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Spark usage*

- `spark-defaults.conf` - Spark default configuration
- `spark-env.sh` - Spark environment variables
- `log4j.properties` - Spark logging configuration
- `hive-site.xml` - Hive configuration for Spark SQL
- `core-site.xml` - Hadoop core configuration

### Import Patterns

#### Python
Extensions: `.py`

**Pattern**: `^from\s+pyspark\s+import`
- PySpark import
- Example: `from pyspark.sql import SparkSession`

**Pattern**: `^from\s+pyspark\.sql\s+import`
- PySpark SQL import
- Example: `from pyspark.sql.functions import col, lit`

**Pattern**: `^from\s+pyspark\.ml\s+import`
- PySpark ML import
- Example: `from pyspark.ml.classification import LogisticRegression`

#### Scala
Extensions: `.scala`

**Pattern**: `import\s+org\.apache\.spark\.`
- Spark Scala import
- Example: `import org.apache.spark.sql.SparkSession`

#### Java
Extensions: `.java`

**Pattern**: `import\s+org\.apache\.spark\.`
- Spark Java import
- Example: `import org.apache.spark.api.java.JavaSparkContext;`

### Code Patterns

**Pattern**: `SparkSession\.builder|SparkContext\(|JavaSparkContext\(`
- Spark session/context creation
- Example: `SparkSession.builder.appName("app").getOrCreate()`

**Pattern**: `spark\.read\.|spark\.sql\(|DataFrame`
- Spark DataFrame operations
- Example: `spark.read.csv("data.csv")`

**Pattern**: `SPARK_HOME|SPARK_MASTER|PYSPARK_PYTHON`
- Spark environment variables
- Example: `SPARK_HOME=/opt/spark`

**Pattern**: `spark://|local\[\*\]|yarn|k8s://|mesos://`
- Spark master URLs
- Example: `spark://master:7077`

**Pattern**: `:4040|:8080|:7077|:18080`
- Spark web UI and master ports
- Example: `http://localhost:4040`

**Pattern**: `\.parquet\(|\.orc\(|\.json\(|\.csv\(`
- Spark data source operations
- Example: `df.write.parquet("output/")`

---

## Environment Variables

- `SPARK_HOME` - Spark installation directory
- `SPARK_MASTER` - Spark master URL
- `SPARK_MASTER_HOST` - Spark master host
- `SPARK_MASTER_PORT` - Spark master port
- `PYSPARK_PYTHON` - Python executable for PySpark
- `PYSPARK_DRIVER_PYTHON` - Driver Python executable
- `SPARK_EXECUTOR_MEMORY` - Executor memory
- `SPARK_DRIVER_MEMORY` - Driver memory
- `SPARK_WORKER_MEMORY` - Worker memory
- `HADOOP_CONF_DIR` - Hadoop configuration directory
- `YARN_CONF_DIR` - YARN configuration directory

## Detection Notes

- PySpark is the Python API, most common entry point
- Spark SQL for structured data processing
- MLlib for machine learning
- Spark Streaming for real-time processing
- Often deployed on YARN, Kubernetes, or standalone
- Delta Lake commonly used for data lakehouse

---

## Secrets Detection

### Credentials

#### Spark S3 Credentials
**Pattern**: `spark\.hadoop\.fs\.s3a\.access\.key\s*[=:]\s*['"]?([A-Z0-9]{20})['"]?`
**Severity**: critical
**Description**: AWS access key in Spark config
**Example**: `spark.hadoop.fs.s3a.access.key=AKIAIOSFODNN7EXAMPLE`

#### Spark S3 Secret Key
**Pattern**: `spark\.hadoop\.fs\.s3a\.secret\.key\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: AWS secret key in Spark config
**Example**: `spark.hadoop.fs.s3a.secret.key=wJalrXUtnFEMI/...`

#### Databricks Token
**Pattern**: `(?:databricks|DATABRICKS).*(?:token|TOKEN)\s*[=:]\s*['"]?(dapi[a-f0-9]{32})['"]?`
**Severity**: critical
**Description**: Databricks personal access token
**Example**: `DATABRICKS_TOKEN=dapiabc123...`

### Validation

#### API Documentation
- **Spark Documentation**: https://spark.apache.org/docs/latest/
- **PySpark API**: https://spark.apache.org/docs/latest/api/python/

---

## TIER 3: Configuration Extraction

### Master URL Extraction

**Pattern**: `(?:spark\.master|SPARK_MASTER)\s*[=:]\s*['"]?([^\s'"]+)['"]?`
- Spark master URL
- Extracts: `master_url`
- Example: `spark.master=spark://master:7077`

### App Name Extraction

**Pattern**: `(?:spark\.app\.name|appName)\s*[=:'"]\s*['"]?([^\s'"()]+)['"]?`
- Spark application name
- Extracts: `app_name`
- Example: `spark.app.name=MySparkApp`

### Executor Memory Extraction

**Pattern**: `(?:spark\.executor\.memory)\s*[=:]\s*['"]?([0-9]+[gmkGMK])['"]?`
- Executor memory allocation
- Extracts: `executor_memory`
- Example: `spark.executor.memory=4g`
