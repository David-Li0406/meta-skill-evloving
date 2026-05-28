# Deployment Strategies

## Contents
- [Canary Deployment](#canary-deployment)
- [Blue-Green Deployment](#blue-green-deployment)
- [Feature Flags for Gradual Rollout](#feature-flags-for-gradual-rollout)

---

## Canary Deployment

Deploy to a canary folder first, monitor for errors, then promote to production.

```groovy
stage('Canary Deployment') {
    when { branch 'main' }
    steps {
        script {
            container('gcloud') {
                withCredentials([file(credentialsId: 'gcp-sa-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    sh '''
                        gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS

                        # Deploy to canary folder first
                        DAGS_BUCKET=$(gcloud composer environments describe $COMPOSER_ENV \
                            --location $COMPOSER_REGION \
                            --format='value(config.dagGcsPrefix)')

                        gsutil -m rsync -r src/dags/ ${DAGS_BUCKET}/canary/

                        echo "Canary deployed. Monitoring for 30 minutes..."
                        sleep 1800

                        # Check error rate in canary
                        ERROR_COUNT=$(gcloud logging read "
                            resource.type=cloud_composer_environment
                            AND severity>=ERROR
                            AND labels.dag_folder=canary
                            AND timestamp>=\"$(date -u -d '30 minutes ago' '+%Y-%m-%dT%H:%M:%SZ')\"
                        " --limit=1000 --format=json | jq '. | length')

                        if [ $ERROR_COUNT -gt 5 ]; then
                            echo "Canary deployment failed with $ERROR_COUNT errors"
                            exit 1
                        fi

                        # Promote to production
                        echo "Canary successful. Promoting to production..."
                        gsutil -m rsync -r -d ${DAGS_BUCKET}/canary/ ${DAGS_BUCKET}/dags/
                    '''
                }
            }
        }
    }
}
```

---

## Blue-Green Deployment

Maintain two identical environments and switch traffic between them.

```groovy
stage('Blue-Green Deploy') {
    steps {
        script {
            def targetEnv = env.ACTIVE_ENV == 'blue' ? 'green' : 'blue'

            echo "Deploying to ${targetEnv} environment"

            container('gcloud') {
                sh """
                    # Deploy to inactive environment
                    DAGS_BUCKET=\$(gcloud composer environments describe recommendation-${targetEnv} \
                        --location ${COMPOSER_REGION} \
                        --format='value(config.dagGcsPrefix)')

                    gsutil -m rsync -r -d src/dags/ \${DAGS_BUCKET}/

                    # Run smoke tests
                    python scripts/smoke_test.py --environment ${targetEnv}
                """
            }

            // Manual verification
            input message: "Switch traffic to ${targetEnv}?", ok: 'Switch'

            // Update DNS or load balancer to point to new environment
            sh "gcloud dns record-sets update airflow.example.com --rrdatas=\${NEW_ENV_IP}"
        }
    }
}
```

---

## Feature Flags for Gradual Rollout

Use deterministic hash-based rollout for gradual feature enablement.

```python
# scripts/feature_flags.py
from typing import Dict
import hashlib

class FeatureFlags:
    """Manage feature flags for gradual rollout."""

    def __init__(self, config: Dict[str, float]):
        self.config = config  # feature_name -> rollout_percentage

    def is_enabled(self, feature: str, dag_id: str) -> bool:
        """Check if feature is enabled for this DAG."""
        if feature not in self.config:
            return False

        rollout_pct = self.config[feature]
        if rollout_pct >= 100:
            return True
        if rollout_pct <= 0:
            return False

        # Deterministic hash-based rollout
        hash_val = int(hashlib.md5(f"{feature}:{dag_id}".encode()).hexdigest(), 16)
        return (hash_val % 100) < rollout_pct

# Usage in DAG
# feature_flags = FeatureFlags({'new_algorithm': 25})  # 25% rollout
# if feature_flags.is_enabled('new_algorithm', dag_id):
#     use_new_algorithm()
```

---

## DAG Versioning for Rollback

### Version Manifest Creation

```python
# scripts/version_dags.py
import hashlib
import json
import os
from pathlib import Path
from datetime import datetime

def calculate_dag_hash(dag_file: Path) -> str:
    """Calculate hash for DAG file."""
    return hashlib.sha256(dag_file.read_bytes()).hexdigest()[:12]

def create_version_manifest(dags_dir: Path, output_file: Path):
    """Create version manifest for rollback."""
    manifest = {
        "version": datetime.now().isoformat(),
        "commit": os.getenv("GIT_COMMIT", "unknown"),
        "dags": {}
    }

    for dag_file in dags_dir.rglob("*.py"):
        if dag_file.name.startswith("test_"):
            continue

        relative_path = str(dag_file.relative_to(dags_dir))
        manifest["dags"][relative_path] = {
            "hash": calculate_dag_hash(dag_file),
            "size": dag_file.stat().st_size,
            "modified": datetime.fromtimestamp(dag_file.stat().st_mtime).isoformat()
        }

    output_file.write_text(json.dumps(manifest, indent=2))
    return manifest
```

### Archive Stage

```groovy
stage('Version and Archive') {
    steps {
        container('python') {
            sh '''
                # Create version manifest
                python scripts/version_dags.py \
                    --dags-dir src/dags \
                    --output version-manifest.json

                # Archive to GCS
                gsutil cp version-manifest.json \
                    gs://dag-versions/${GIT_COMMIT}/manifest.json

                # Archive DAGs
                tar -czf dags-${GIT_COMMIT}.tar.gz src/dags/
                gsutil cp dags-${GIT_COMMIT}.tar.gz \
                    gs://dag-versions/${GIT_COMMIT}/
            '''
        }
    }
}
```

### Quick Rollback Script

```bash
#!/bin/bash
# scripts/rollback.sh

PREVIOUS_VERSION=$1
COMPOSER_ENV="recommendation-prod"
REGION="asia-southeast1"

echo "Rolling back to version: $PREVIOUS_VERSION"

# Download previous version
gsutil cp gs://dag-versions/${PREVIOUS_VERSION}/dags-${PREVIOUS_VERSION}.tar.gz /tmp/
tar -xzf /tmp/dags-${PREVIOUS_VERSION}.tar.gz -C /tmp/

# Deploy to Composer
DAGS_BUCKET=$(gcloud composer environments describe $COMPOSER_ENV \
    --location $REGION \
    --format='value(config.dagGcsPrefix)')

gsutil -m rsync -r -d /tmp/src/dags/ ${DAGS_BUCKET}/

echo "Rollback completed"
```
