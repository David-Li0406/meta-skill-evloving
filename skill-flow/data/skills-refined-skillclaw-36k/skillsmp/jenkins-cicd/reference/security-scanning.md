# Security Scanning

## Contents
- [SAST with Bandit](#sast-with-bandit)
- [Dependency Scanning with Safety](#dependency-scanning-with-safety)
- [Secret Detection](#secret-detection)
- [SQL Injection Detection](#sql-injection-detection)
- [Performance Testing](#performance-testing)

---

## SAST with Bandit

Static Application Security Testing using Bandit.

```groovy
stage('Security Scan') {
    parallel {
        stage('SAST - Bandit') {
            steps {
                container('python') {
                    sh '''
                        pip install bandit
                        bandit -r src/ -f json -o bandit-report.json || true
                    '''
                    recordIssues(
                        tools: [bandit(pattern: 'bandit-report.json')],
                        qualityGates: [[threshold: 1, type: 'TOTAL_HIGH', unstable: false]]
                    )
                }
            }
        }
    }
}
```

---

## Dependency Scanning with Safety

Check installed packages for known security vulnerabilities.

```groovy
stage('Dependency Scan - Safety') {
    steps {
        container('python') {
            sh '''
                pip install safety
                safety check --json --output safety-report.json || true
            '''
        }
    }
}
```

---

## Secret Detection

Detect hardcoded secrets in source code.

```groovy
stage('Secret Detection') {
    steps {
        container('python') {
            sh '''
                pip install detect-secrets
                detect-secrets scan --all-files > secrets-baseline.json

                SECRETS_COUNT=$(jq '.results | length' secrets-baseline.json)
                if [ $SECRETS_COUNT -gt 0 ]; then
                    echo "ERROR: Secrets detected in code!"
                    jq '.results' secrets-baseline.json
                    exit 1
                fi
            '''
        }
    }
}
```

---

## SQL Injection Detection

Check SQL files for potential injection vulnerabilities.

```groovy
stage('SQL Security Check') {
    steps {
        container('python') {
            sh '''
                python scripts/check_sql_security.py src/sql/
            '''
        }
    }
}
```

```python
# scripts/check_sql_security.py
import re
import sys
from pathlib import Path

def check_sql_file(filepath: Path) -> list:
    """Check SQL file for security issues."""
    issues = []
    content = filepath.read_text()

    # Check for string concatenation (potential SQL injection)
    if re.search(r'\+\s*["\'].*["\']', content):
        issues.append(f"{filepath}: Potential SQL injection via string concatenation")

    # Check for format strings without parameterization
    if re.search(r'\.format\(', content) or re.search(r'%\s*\(', content):
        issues.append(f"{filepath}: Use parameterized queries instead of format()")

    return issues

if __name__ == "__main__":
    sql_dir = Path(sys.argv[1])
    all_issues = []

    for sql_file in sql_dir.rglob("*.sql"):
        all_issues.extend(check_sql_file(sql_file))

    if all_issues:
        for issue in all_issues:
            print(f"❌ {issue}")
        sys.exit(1)

    print("✅ No SQL security issues found")
```

---

## Performance Testing

### Query Performance Benchmarking

```python
# scripts/performance_test.py
import json
import time
from google.cloud import bigquery
from typing import Dict

def benchmark_queries(baseline_file: str, max_regression_pct: float = 10.0) -> bool:
    """Benchmark query performance against baseline."""

    client = bigquery.Client()

    queries = {
        "user_features": "SELECT * FROM `project.recommendation.user_features` LIMIT 1000",
        "product_stats": "SELECT * FROM `project.recommendation.product_stats` LIMIT 1000",
    }

    results = {}
    for query_name, query_sql in queries.items():
        # Dry run for cost
        job_config = bigquery.QueryJobConfig(dry_run=True)
        dry_run = client.query(query_sql, job_config=job_config)

        # Actual run for performance
        start = time.time()
        query_job = client.query(query_sql)
        query_job.result()
        duration_ms = (time.time() - start) * 1000

        results[query_name] = {
            "duration_ms": duration_ms,
            "bytes_processed": dry_run.total_bytes_processed,
        }

    # Compare with baseline
    try:
        with open(baseline_file, 'r') as f:
            baseline = json.load(f)

        regressions = []
        for name, current in results.items():
            if name in baseline:
                baseline_duration = baseline[name]["duration_ms"]
                regression_pct = ((current["duration_ms"] - baseline_duration) / baseline_duration) * 100

                if regression_pct > max_regression_pct:
                    regressions.append(f"{name}: {regression_pct:.1f}% slower")

        if regressions:
            print("Performance regressions:")
            for r in regressions:
                print(f"  ❌ {r}")
            return False
    except FileNotFoundError:
        print("No baseline found. Creating new baseline...")

    # Update baseline
    with open(baseline_file, 'w') as f:
        json.dump(results, f, indent=2)

    return True
```

### Performance Stage

```groovy
stage('Performance Tests') {
    steps {
        container('python') {
            withCredentials([file(credentialsId: 'gcp-sa-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                sh '''
                    python scripts/performance_test.py \
                        --baseline performance-baseline.json \
                        --max-regression-percent 10
                '''
            }
        }
    }
}
```

---

## Pipeline Observability

### Build Metrics Collection

```groovy
post {
    always {
        script {
            def buildDuration = currentBuild.duration
            def buildResult = currentBuild.result ?: 'SUCCESS'

            // Send metrics to monitoring system
            sh """
                curl -X POST https://monitoring.example.com/api/metrics \
                    -H 'Content-Type: application/json' \
                    -d '{
                        "pipeline": "${env.JOB_NAME}",
                        "build_number": ${env.BUILD_NUMBER},
                        "duration_ms": ${buildDuration},
                        "result": "${buildResult}",
                        "branch": "${env.BRANCH_NAME}",
                        "commit": "${env.GIT_COMMIT}"
                    }'
            """
        }
    }
}
```

### DORA Metrics Tracking

```python
# scripts/track_dora_metrics.py
from datetime import datetime
import requests

class DORAMetrics:
    """Track DORA (DevOps Research and Assessment) metrics."""

    def __init__(self, api_url: str):
        self.api_url = api_url

    def track_deployment(self, success: bool):
        """Track deployment frequency and success rate."""
        requests.post(f"{self.api_url}/deployments", json={
            "timestamp": datetime.now().isoformat(),
            "success": success,
            "environment": "production"
        })

    def track_lead_time(self, commit_time: datetime, deploy_time: datetime):
        """Track lead time for changes."""
        lead_time_minutes = (deploy_time - commit_time).total_seconds() / 60
        requests.post(f"{self.api_url}/lead_time", json={
            "lead_time_minutes": lead_time_minutes,
            "timestamp": deploy_time.isoformat()
        })

    def track_mttr(self, incident_start: datetime, resolution_time: datetime):
        """Track Mean Time To Recovery."""
        mttr_minutes = (resolution_time - incident_start).total_seconds() / 60
        requests.post(f"{self.api_url}/mttr", json={
            "mttr_minutes": mttr_minutes,
            "timestamp": resolution_time.isoformat()
        })
```
