---
name: jenkins-cicd
description: Jenkins CI/CD pipelines for data platforms with Kubernetes pod agents. Use when creating Jenkinsfiles, implementing parallel linting stages (Ruff, Black, Mypy), DAG validation with DagBag, security scanning (Bandit, Safety, detect-secrets), deployment strategies (canary with error monitoring, blue-green), or setting up artifact management and DORA metrics tracking.
---

# Jenkins CI/CD Pipeline Skill

Create Jenkins pipelines for data engineering projects following best practices.

## Jenkinsfile Template

```groovy
// Jenkinsfile
pipeline {
    agent {
        kubernetes {
            yaml '''
                apiVersion: v1
                kind: Pod
                spec:
                  containers:
                  - name: python
                    image: python:3.10-slim
                    command: ['sleep', '99d']
                  - name: gcloud
                    image: google/cloud-sdk:latest
                    command: ['sleep', '99d']
            '''
        }
    }

    environment {
        GCP_PROJECT = credentials('gcp-project-id')
        COMPOSER_ENV = 'recommendation-prod'
        COMPOSER_REGION = 'asia-southeast1'
        SLACK_WEBHOOK = credentials('slack-webhook')
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                container('python') {
                    sh '''
                        pip install -r requirements.txt
                        pip install -r requirements-dev.txt
                    '''
                }
            }
        }

        stage('Lint') {
            parallel {
                stage('Ruff') {
                    steps {
                        container('python') {
                            sh 'ruff check src/'
                        }
                    }
                }
                stage('Black') {
                    steps {
                        container('python') {
                            sh 'black --check src/'
                        }
                    }
                }
                stage('Mypy') {
                    steps {
                        container('python') {
                            sh 'mypy src/'
                        }
                    }
                }
            }
        }

        stage('DAG Validation') {
            steps {
                container('python') {
                    sh '''
                        python -c "
import sys
from airflow.models import DagBag
dag_bag = DagBag(dag_folder='src/dags', include_examples=False)
if dag_bag.import_errors:
    for dag_id, error in dag_bag.import_errors.items():
        print(f'DAG {dag_id}: {error}')
    sys.exit(1)
print(f'Validated {len(dag_bag.dags)} DAGs successfully')
"
                    '''
                }
            }
        }

        stage('Unit Tests') {
            steps {
                container('python') {
                    sh '''
                        pytest tests/unit \
                            --cov=src \
                            --cov-report=xml \
                            --cov-report=html \
                            --junitxml=test-results.xml \
                            -v
                    '''
                }
            }
            post {
                always {
                    junit 'test-results.xml'
                    publishHTML(target: [
                        reportName: 'Coverage Report',
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html'
                    ])
                }
            }
        }

        stage('Integration Tests') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                }
            }
            steps {
                container('python') {
                    withCredentials([file(credentialsId: 'gcp-sa-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                        sh '''
                            pytest tests/integration \
                                --junitxml=integration-test-results.xml \
                                -v
                        '''
                    }
                }
            }
        }

        stage('Deploy to Staging') {
            when {
                branch 'develop'
            }
            steps {
                container('gcloud') {
                    withCredentials([file(credentialsId: 'gcp-sa-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                        sh '''
                            gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                            gcloud config set project $GCP_PROJECT

                            DAGS_BUCKET=$(gcloud composer environments describe recommendation-staging \
                                --location $COMPOSER_REGION \
                                --format='value(config.dagGcsPrefix)')

                            gsutil -m rsync -r -d src/dags/ $DAGS_BUCKET/
                            gsutil -m rsync -r src/sql/ $DAGS_BUCKET/../data/sql/
                        '''
                    }
                }
            }
        }

        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                input message: 'Deploy to production?', ok: 'Deploy'
                container('gcloud') {
                    withCredentials([file(credentialsId: 'gcp-sa-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                        sh '''
                            gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                            gcloud config set project $GCP_PROJECT

                            DAGS_BUCKET=$(gcloud composer environments describe $COMPOSER_ENV \
                                --location $COMPOSER_REGION \
                                --format='value(config.dagGcsPrefix)')

                            gsutil -m rsync -r -d src/dags/ $DAGS_BUCKET/
                            gsutil -m rsync -r src/sql/ $DAGS_BUCKET/../data/sql/

                            echo "Deployed to $DAGS_BUCKET"
                        '''
                    }
                }
            }
        }
    }

    post {
        success {
            slackSend(
                channel: '#data-pipeline-ci',
                color: 'good',
                message: "✅ Pipeline succeeded: ${env.JOB_NAME} #${env.BUILD_NUMBER}\n${env.BUILD_URL}"
            )
        }
        failure {
            slackSend(
                channel: '#data-pipeline-ci',
                color: 'danger',
                message: "❌ Pipeline failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}\n${env.BUILD_URL}"
            )
        }
        always {
            cleanWs()
        }
    }
}
```

## DAG Validation Script

```python
# scripts/validate_dags.py
#!/usr/bin/env python3
"""Validate Airflow DAGs before deployment."""

import sys
from pathlib import Path
from airflow.models import DagBag

def validate_dags(dag_folder: str) -> bool:
    """Validate all DAGs in the specified folder."""
    dag_bag = DagBag(dag_folder=dag_folder, include_examples=False)

    errors = []

    # Check for import errors
    if dag_bag.import_errors:
        for dag_id, error in dag_bag.import_errors.items():
            errors.append(f"Import error in {dag_id}: {error}")

    # Validate DAG configurations
    for dag_id, dag in dag_bag.dags.items():
        # Check for required tags
        if not dag.tags:
            errors.append(f"{dag_id}: Missing tags")

        # Check for owner
        if dag.default_args.get("owner") == "airflow":
            errors.append(f"{dag_id}: Default owner 'airflow' should be changed")

        # Check for catchup disabled
        if dag.catchup:
            errors.append(f"{dag_id}: catchup should be False")

    if errors:
        print("Validation errors found:")
        for error in errors:
            print(f"  ❌ {error}")
        return False

    print(f"✅ Validated {len(dag_bag.dags)} DAGs successfully")
    return True

if __name__ == "__main__":
    dag_folder = sys.argv[1] if len(sys.argv) > 1 else "src/dags"
    success = validate_dags(dag_folder)
    sys.exit(0 if success else 1)
```

## Best Practices

- Run DAG validation before deployment
- Use parallel stages for faster execution
- Require manual approval for production deploys
- Send notifications to Slack/Teams on completion
- Clean workspace after each build
- Use Kubernetes agents for scalability
- Implement security scanning in every pipeline
- Version and archive DAGs for quick rollback

## Advanced Topics

For detailed guidance on specialized patterns:

- **Canary Deployment**: See [reference/deployment-strategies.md](reference/deployment-strategies.md) for error-rate monitoring
- **Blue-Green Deployment**: See [reference/deployment-strategies.md](reference/deployment-strategies.md) for traffic switching
- **Feature Flags**: See [reference/deployment-strategies.md](reference/deployment-strategies.md) for gradual rollout
- **Security Scanning**: See [reference/security-scanning.md](reference/security-scanning.md) for SAST, dependency, and secret scanning
- **Performance Testing**: See [reference/security-scanning.md](reference/security-scanning.md) for benchmarking and regression detection
- **DORA Metrics**: See [reference/security-scanning.md](reference/security-scanning.md) for deployment tracking
