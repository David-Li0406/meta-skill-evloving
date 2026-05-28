# Apache Airflow

**Category**: apache
**Description**: Platform for programmatically authoring, scheduling, and monitoring workflows
**Homepage**: https://airflow.apache.org

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### PYPI
*Airflow and provider packages*

- `apache-airflow` - Core Airflow package
- `apache-airflow-providers-amazon` - AWS providers
- `apache-airflow-providers-google` - GCP providers
- `apache-airflow-providers-microsoft-azure` - Azure providers
- `apache-airflow-providers-postgres` - PostgreSQL provider
- `apache-airflow-providers-mysql` - MySQL provider
- `apache-airflow-providers-snowflake` - Snowflake provider
- `apache-airflow-providers-databricks` - Databricks provider
- `apache-airflow-providers-slack` - Slack provider
- `apache-airflow-providers-http` - HTTP provider
- `apache-airflow-providers-ssh` - SSH provider
- `apache-airflow-providers-docker` - Docker provider
- `apache-airflow-providers-kubernetes` - Kubernetes provider
- `apache-airflow-providers-celery` - Celery provider
- `astronomer-cosmos` - dbt integration

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Airflow usage*

- `airflow.cfg` - Airflow configuration
- `airflow.db` - Airflow SQLite database
- `webserver_config.py` - Web server configuration
- `dags/` - DAG directory
- `plugins/` - Plugins directory
- `logs/` - Airflow logs directory

### Configuration Directories
*Known directories that indicate Airflow usage*

- `dags/` - DAG definitions
- `plugins/` - Custom plugins
- `config/` - Configuration files

### Import Patterns

#### Python
Extensions: `.py`

**Pattern**: `^from\s+airflow\s+import`
- Airflow core import
- Example: `from airflow import DAG`

**Pattern**: `^from\s+airflow\.operators\s+import`
- Airflow operators import
- Example: `from airflow.operators.python import PythonOperator`

**Pattern**: `^from\s+airflow\.providers\s+import`
- Airflow providers import
- Example: `from airflow.providers.amazon.aws.operators.s3 import S3Hook`

**Pattern**: `^from\s+airflow\.decorators\s+import`
- Airflow TaskFlow API import
- Example: `from airflow.decorators import dag, task`

### Code Patterns

**Pattern**: `@dag\(|@task\(|DAG\(`
- DAG/task decorators and class
- Example: `@dag(schedule="@daily")`

**Pattern**: `PythonOperator|BashOperator|EmailOperator`
- Airflow operators
- Example: `PythonOperator(task_id='my_task', python_callable=func)`

**Pattern**: `>>|<<`
- Airflow task dependencies
- Example: `task1 >> task2 >> task3`

**Pattern**: `AIRFLOW__|AIRFLOW_HOME|AIRFLOW_CONFIG`
- Airflow environment variables
- Example: `AIRFLOW__CORE__EXECUTOR=CeleryExecutor`

**Pattern**: `:8080/admin|/airflow/|/home/airflow`
- Airflow web UI and paths
- Example: `http://localhost:8080/admin`

**Pattern**: `Variable\.get\(|Connection\.get_connection_from_secrets`
- Airflow Variables and Connections
- Example: `Variable.get("my_variable")`

---

## Environment Variables

- `AIRFLOW_HOME` - Airflow home directory
- `AIRFLOW_CONFIG` - Path to airflow.cfg
- `AIRFLOW__CORE__EXECUTOR` - Executor type
- `AIRFLOW__CORE__SQL_ALCHEMY_CONN` - Database connection
- `AIRFLOW__CORE__FERNET_KEY` - Encryption key
- `AIRFLOW__WEBSERVER__SECRET_KEY` - Web server secret
- `AIRFLOW__CELERY__BROKER_URL` - Celery broker URL
- `AIRFLOW__CELERY__RESULT_BACKEND` - Celery result backend
- `AIRFLOW_CONN_*` - Connection definitions
- `AIRFLOW_VAR_*` - Variable definitions

## Detection Notes

- DAGs are Python files defining workflows
- dags/ folder is the standard location
- Providers are separate packages for integrations
- TaskFlow API is the modern decorator-based approach
- Connections store credentials for external systems
- Variables store configuration values

---

## Secrets Detection

### Credentials

#### Airflow Fernet Key
**Pattern**: `(?:AIRFLOW__CORE__FERNET_KEY|fernet_key)\s*[=:]\s*['"]?([A-Za-z0-9_=-]{44})['"]?`
**Severity**: critical
**Description**: Airflow Fernet encryption key for connections
**Example**: `AIRFLOW__CORE__FERNET_KEY=abc123def456...=`

#### Airflow Secret Key
**Pattern**: `(?:AIRFLOW__WEBSERVER__SECRET_KEY|secret_key)\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Airflow web server secret key
**Example**: `AIRFLOW__WEBSERVER__SECRET_KEY=supersecret`

#### Airflow Database Connection
**Pattern**: `(?:AIRFLOW__CORE__SQL_ALCHEMY_CONN|sql_alchemy_conn)\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Airflow database connection string
**Example**: `AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql://user:pass@host/db`

#### Airflow Connection URI
**Pattern**: `AIRFLOW_CONN_([A-Z_]+)\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: high
**Description**: Airflow connection definition (may contain credentials)
**Example**: `AIRFLOW_CONN_AWS_DEFAULT=aws://key:secret@`

### Validation

#### API Documentation
- **Airflow Documentation**: https://airflow.apache.org/docs/
- **REST API**: https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html

---

## TIER 3: Configuration Extraction

### Executor Extraction

**Pattern**: `(?:executor|AIRFLOW__CORE__EXECUTOR)\s*[=:]\s*['"]?([A-Za-z]+Executor)['"]?`
- Airflow executor type
- Extracts: `executor`
- Example: `executor = CeleryExecutor`

### DAG Directory Extraction

**Pattern**: `(?:dags_folder|AIRFLOW__CORE__DAGS_FOLDER)\s*[=:]\s*['"]?([^\s'"]+)['"]?`
- DAGs folder path
- Extracts: `dags_folder`
- Example: `dags_folder = /opt/airflow/dags`

### Schedule Extraction

**Pattern**: `schedule(?:_interval)?\s*[=:]\s*['"]([^'"]+)['"]`
- DAG schedule
- Extracts: `schedule`
- Example: `schedule='@daily'`
