---
name: faion-gcp-cli-skill
user-invocable: false
description: ""
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Google Cloud CLI Skill

**Layer:** 3 (Technical Skill)
**Used by:** faion-devops-agent

## Purpose

Provides Google Cloud CLI (gcloud) operations and patterns for cloud infrastructure management. Covers compute, storage, serverless, containers, databases, data warehouse, identity management, networking, and monitoring.

---

## Configuration

### gcloud CLI Installation

```bash
# Install gcloud CLI (Linux)
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Install via apt (Debian/Ubuntu)
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
sudo apt update && sudo apt install google-cloud-cli

# Verify installation
gcloud version
```

### Authentication

```bash
# Interactive login (opens browser)
gcloud auth login

# Service account authentication
gcloud auth activate-service-account --key-file=service-account.json

# Application default credentials (for local development)
gcloud auth application-default login

# List authenticated accounts
gcloud auth list

# Revoke credentials
gcloud auth revoke [ACCOUNT]
```

### Project Configuration

```bash
# Set default project
gcloud config set project my-project-id

# Get current project
gcloud config get-value project

# List projects
gcloud projects list

# Create project
gcloud projects create my-new-project --name="My Project"

# Delete project
gcloud projects delete my-project-id
```

### Configuration Management

```bash
# View all configurations
gcloud config configurations list

# Create named configuration
gcloud config configurations create production

# Activate configuration
gcloud config configurations activate production

# Set properties in current config
gcloud config set compute/zone us-central1-a
gcloud config set compute/region us-central1

# View current config
gcloud config list

# Set multiple properties
gcloud config set core/project my-project
gcloud config set compute/zone us-central1-a
gcloud config set compute/region us-central1
```

### Environment Variables

```bash
# Project
export CLOUDSDK_CORE_PROJECT="my-project-id"

# Region/Zone
export CLOUDSDK_COMPUTE_REGION="us-central1"
export CLOUDSDK_COMPUTE_ZONE="us-central1-a"

# Credentials
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"

# Disable prompts (CI/CD)
export CLOUDSDK_CORE_DISABLE_PROMPTS=1
```

---

## Compute Engine

### Instance Management

```bash
# List instances
gcloud compute instances list

# List instances in specific zone
gcloud compute instances list --zones=us-central1-a

# Create instance
gcloud compute instances create my-instance \
    --zone=us-central1-a \
    --machine-type=e2-medium \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=50GB \
    --boot-disk-type=pd-balanced \
    --tags=http-server,https-server

# Create instance with startup script
gcloud compute instances create my-instance \
    --zone=us-central1-a \
    --machine-type=e2-medium \
    --metadata-from-file=startup-script=startup.sh

# Create preemptible/spot instance
gcloud compute instances create my-spot \
    --zone=us-central1-a \
    --provisioning-model=SPOT \
    --instance-termination-action=STOP

# Start/stop/delete instances
gcloud compute instances start my-instance --zone=us-central1-a
gcloud compute instances stop my-instance --zone=us-central1-a
gcloud compute instances delete my-instance --zone=us-central1-a

# SSH into instance
gcloud compute ssh my-instance --zone=us-central1-a

# SSH with specific user
gcloud compute ssh user@my-instance --zone=us-central1-a

# Copy files to/from instance
gcloud compute scp local-file.txt my-instance:/remote/path --zone=us-central1-a
gcloud compute scp my-instance:/remote/file.txt ./local/ --zone=us-central1-a

# Describe instance
gcloud compute instances describe my-instance --zone=us-central1-a
```

### Machine Types

```bash
# List machine types
gcloud compute machine-types list --zones=us-central1-a

# Filter by CPU/memory
gcloud compute machine-types list \
    --filter="guestCpus>=4 AND memoryMb>=16384" \
    --zones=us-central1-a

# Common machine types
# e2-micro, e2-small, e2-medium (cost-effective)
# n2-standard-2, n2-standard-4, n2-standard-8 (balanced)
# n2-highmem-2, n2-highmem-4 (memory optimized)
# n2-highcpu-2, n2-highcpu-4 (compute optimized)
# c2-standard-4, c2-standard-8 (compute intensive)
```

### Images and Snapshots

```bash
# List images
gcloud compute images list

# List images from specific project
gcloud compute images list --project=ubuntu-os-cloud

# Create image from disk
gcloud compute images create my-image \
    --source-disk=my-disk \
    --source-disk-zone=us-central1-a

# Create image from snapshot
gcloud compute images create my-image \
    --source-snapshot=my-snapshot

# Delete image
gcloud compute images delete my-image

# Create snapshot
gcloud compute disks snapshot my-disk \
    --zone=us-central1-a \
    --snapshot-names=my-snapshot

# List snapshots
gcloud compute snapshots list

# Delete snapshot
gcloud compute snapshots delete my-snapshot
```

### Disks

```bash
# List disks
gcloud compute disks list

# Create disk
gcloud compute disks create my-disk \
    --zone=us-central1-a \
    --size=100GB \
    --type=pd-balanced

# Attach disk to instance
gcloud compute instances attach-disk my-instance \
    --disk=my-disk \
    --zone=us-central1-a

# Detach disk
gcloud compute instances detach-disk my-instance \
    --disk=my-disk \
    --zone=us-central1-a

# Resize disk
gcloud compute disks resize my-disk \
    --zone=us-central1-a \
    --size=200GB

# Delete disk
gcloud compute disks delete my-disk --zone=us-central1-a
```

### Instance Groups and Templates

```bash
# Create instance template
gcloud compute instance-templates create my-template \
    --machine-type=e2-medium \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=50GB

# Create managed instance group
gcloud compute instance-groups managed create my-group \
    --zone=us-central1-a \
    --template=my-template \
    --size=3

# Set autoscaling
gcloud compute instance-groups managed set-autoscaling my-group \
    --zone=us-central1-a \
    --min-num-replicas=2 \
    --max-num-replicas=10 \
    --target-cpu-utilization=0.6

# Update instance group (rolling update)
gcloud compute instance-groups managed rolling-action start-update my-group \
    --zone=us-central1-a \
    --version=template=my-template-v2 \
    --max-unavailable=1

# List instance groups
gcloud compute instance-groups managed list
```

---

## Cloud Storage

### Bucket Operations

```bash
# List buckets
gcloud storage buckets list

# Create bucket
gcloud storage buckets create gs://my-bucket \
    --location=us-central1 \
    --uniform-bucket-level-access

# Create bucket with specific storage class
gcloud storage buckets create gs://my-archive-bucket \
    --location=us \
    --storage-class=archive

# Describe bucket
gcloud storage buckets describe gs://my-bucket

# Update bucket (enable versioning)
gcloud storage buckets update gs://my-bucket --versioning

# Delete bucket (must be empty)
gcloud storage buckets delete gs://my-bucket

# Delete bucket with all contents
gcloud storage rm -r gs://my-bucket
```

### Object Operations

```bash
# List objects
gcloud storage ls gs://my-bucket
gcloud storage ls gs://my-bucket/** --recursive

# Copy files
gcloud storage cp local-file.txt gs://my-bucket/
gcloud storage cp gs://my-bucket/file.txt ./local/
gcloud storage cp -r ./local-dir gs://my-bucket/

# Sync directories
gcloud storage rsync -r ./local-dir gs://my-bucket/path
gcloud storage rsync -r gs://my-bucket/path ./local-dir
gcloud storage rsync -r -d ./local-dir gs://my-bucket/  # -d deletes extra files

# Move/rename objects
gcloud storage mv gs://my-bucket/old-name.txt gs://my-bucket/new-name.txt

# Delete objects
gcloud storage rm gs://my-bucket/file.txt
gcloud storage rm -r gs://my-bucket/path/

# Get object metadata
gcloud storage objects describe gs://my-bucket/file.txt

# Set object metadata
gcloud storage objects update gs://my-bucket/file.txt \
    --content-type="application/json"
```

### Access Control

```bash
# Make bucket public
gcloud storage buckets add-iam-policy-binding gs://my-bucket \
    --member=allUsers \
    --role=roles/storage.objectViewer

# Grant user access
gcloud storage buckets add-iam-policy-binding gs://my-bucket \
    --member=user:user@example.com \
    --role=roles/storage.objectAdmin

# Remove access
gcloud storage buckets remove-iam-policy-binding gs://my-bucket \
    --member=user:user@example.com \
    --role=roles/storage.objectAdmin

# View IAM policy
gcloud storage buckets get-iam-policy gs://my-bucket

# Generate signed URL (requires service account)
gcloud storage sign-url gs://my-bucket/file.txt \
    --duration=1h \
    --private-key-file=service-account.json
```

### Lifecycle Management

```bash
# Set lifecycle policy
cat > lifecycle.json << 'EOF'
{
  "rule": [
    {
      "action": {"type": "Delete"},
      "condition": {"age": 365}
    },
    {
      "action": {"type": "SetStorageClass", "storageClass": "NEARLINE"},
      "condition": {"age": 30}
    }
  ]
}
EOF
gcloud storage buckets update gs://my-bucket --lifecycle-file=lifecycle.json

# View lifecycle policy
gcloud storage buckets describe gs://my-bucket --format="json(lifecycle)"

# Remove lifecycle policy
gcloud storage buckets update gs://my-bucket --clear-lifecycle
```

---

## Cloud Functions

### Function Deployment

```bash
# Deploy HTTP function (Python)
gcloud functions deploy my-function \
    --gen2 \
    --runtime=python312 \
    --region=us-central1 \
    --source=. \
    --entry-point=main \
    --trigger-http \
    --allow-unauthenticated

# Deploy with environment variables
gcloud functions deploy my-function \
    --gen2 \
    --runtime=nodejs20 \
    --region=us-central1 \
    --source=. \
    --entry-point=handler \
    --trigger-http \
    --set-env-vars=API_KEY=xxx,DEBUG=true

# Deploy with secrets
gcloud functions deploy my-function \
    --gen2 \
    --runtime=python312 \
    --region=us-central1 \
    --source=. \
    --entry-point=main \
    --trigger-http \
    --set-secrets=API_KEY=my-secret:latest

# Deploy event-triggered function (Pub/Sub)
gcloud functions deploy my-function \
    --gen2 \
    --runtime=python312 \
    --region=us-central1 \
    --source=. \
    --entry-point=process_message \
    --trigger-topic=my-topic

# Deploy with Cloud Storage trigger
gcloud functions deploy my-function \
    --gen2 \
    --runtime=python312 \
    --region=us-central1 \
    --source=. \
    --entry-point=process_file \
    --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
    --trigger-event-filters="bucket=my-bucket"
```

### Function Management

```bash
# List functions
gcloud functions list

# Describe function
gcloud functions describe my-function --region=us-central1

# Call function (HTTP)
gcloud functions call my-function \
    --region=us-central1 \
    --data='{"name": "World"}'

# View logs
gcloud functions logs read my-function --region=us-central1

# Delete function
gcloud functions delete my-function --region=us-central1
```

---

## Cloud Run

### Service Deployment

```bash
# Deploy from source (builds container automatically)
gcloud run deploy my-service \
    --source=. \
    --region=us-central1 \
    --allow-unauthenticated

# Deploy from container image
gcloud run deploy my-service \
    --image=gcr.io/my-project/my-image:latest \
    --region=us-central1 \
    --platform=managed \
    --allow-unauthenticated

# Deploy with environment variables
gcloud run deploy my-service \
    --image=gcr.io/my-project/my-image:latest \
    --region=us-central1 \
    --set-env-vars=DATABASE_URL=xxx,API_KEY=yyy

# Deploy with secrets
gcloud run deploy my-service \
    --image=gcr.io/my-project/my-image:latest \
    --region=us-central1 \
    --set-secrets=API_KEY=my-secret:latest

# Deploy with resource limits
gcloud run deploy my-service \
    --image=gcr.io/my-project/my-image:latest \
    --region=us-central1 \
    --memory=2Gi \
    --cpu=2 \
    --concurrency=100 \
    --max-instances=10 \
    --min-instances=1
```

### Service Management

```bash
# List services
gcloud run services list

# Describe service
gcloud run services describe my-service --region=us-central1

# Get service URL
gcloud run services describe my-service \
    --region=us-central1 \
    --format='value(status.url)'

# Update service
gcloud run services update my-service \
    --region=us-central1 \
    --memory=4Gi

# Delete service
gcloud run services delete my-service --region=us-central1
```

### Traffic Management

```bash
# Deploy new revision
gcloud run deploy my-service \
    --image=gcr.io/my-project/my-image:v2 \
    --region=us-central1 \
    --tag=v2 \
    --no-traffic

# Split traffic (blue-green)
gcloud run services update-traffic my-service \
    --region=us-central1 \
    --to-revisions=my-service-00001=50,my-service-00002=50

# Route all traffic to latest
gcloud run services update-traffic my-service \
    --region=us-central1 \
    --to-latest
```

---

## Google Kubernetes Engine (GKE)

### Cluster Management

```bash
# Create cluster
gcloud container clusters create my-cluster \
    --zone=us-central1-a \
    --num-nodes=3 \
    --machine-type=e2-standard-4 \
    --enable-autoscaling \
    --min-nodes=1 \
    --max-nodes=10

# Create Autopilot cluster (managed)
gcloud container clusters create-auto my-autopilot-cluster \
    --region=us-central1

# List clusters
gcloud container clusters list

# Get cluster credentials (configure kubectl)
gcloud container clusters get-credentials my-cluster \
    --zone=us-central1-a

# Describe cluster
gcloud container clusters describe my-cluster --zone=us-central1-a

# Resize cluster
gcloud container clusters resize my-cluster \
    --zone=us-central1-a \
    --num-nodes=5

# Delete cluster
gcloud container clusters delete my-cluster --zone=us-central1-a
```

### Node Pools

```bash
# List node pools
gcloud container node-pools list --cluster=my-cluster --zone=us-central1-a

# Create node pool
gcloud container node-pools create my-pool \
    --cluster=my-cluster \
    --zone=us-central1-a \
    --num-nodes=3 \
    --machine-type=n2-standard-8

# Create preemptible node pool
gcloud container node-pools create spot-pool \
    --cluster=my-cluster \
    --zone=us-central1-a \
    --spot \
    --num-nodes=5

# Enable autoscaling on node pool
gcloud container node-pools update my-pool \
    --cluster=my-cluster \
    --zone=us-central1-a \
    --enable-autoscaling \
    --min-nodes=1 \
    --max-nodes=20

# Delete node pool
gcloud container node-pools delete my-pool \
    --cluster=my-cluster \
    --zone=us-central1-a
```

### Cluster Upgrades

```bash
# Get available versions
gcloud container get-server-config --zone=us-central1-a

# Upgrade control plane
gcloud container clusters upgrade my-cluster \
    --zone=us-central1-a \
    --master \
    --cluster-version=1.28

# Upgrade node pool
gcloud container clusters upgrade my-cluster \
    --zone=us-central1-a \
    --node-pool=default-pool
```

---

## Cloud SQL

### Instance Management

```bash
# Create PostgreSQL instance
gcloud sql instances create my-postgres \
    --database-version=POSTGRES_15 \
    --tier=db-custom-2-7680 \
    --region=us-central1 \
    --root-password=secretpassword \
    --storage-size=100GB \
    --storage-auto-increase

# Create MySQL instance
gcloud sql instances create my-mysql \
    --database-version=MYSQL_8_0 \
    --tier=db-n1-standard-2 \
    --region=us-central1 \
    --root-password=secretpassword

# List instances
gcloud sql instances list

# Describe instance
gcloud sql instances describe my-postgres

# Start/stop instance
gcloud sql instances patch my-postgres --activation-policy=NEVER  # Stop
gcloud sql instances patch my-postgres --activation-policy=ALWAYS # Start

# Delete instance
gcloud sql instances delete my-postgres
```

### Database Operations

```bash
# Create database
gcloud sql databases create mydb --instance=my-postgres

# List databases
gcloud sql databases list --instance=my-postgres

# Delete database
gcloud sql databases delete mydb --instance=my-postgres

# Create user
gcloud sql users create myuser \
    --instance=my-postgres \
    --password=userpassword

# List users
gcloud sql users list --instance=my-postgres

# Change password
gcloud sql users set-password myuser \
    --instance=my-postgres \
    --password=newpassword

# Delete user
gcloud sql users delete myuser --instance=my-postgres
```

### Connections

```bash
# Connect via Cloud SQL Proxy
cloud-sql-proxy --port 5432 my-project:us-central1:my-postgres

# Direct connection (public IP)
gcloud sql connect my-postgres --user=postgres

# Export database
gcloud sql export sql my-postgres gs://my-bucket/backup.sql \
    --database=mydb

# Import database
gcloud sql import sql my-postgres gs://my-bucket/backup.sql \
    --database=mydb
```

---

## BigQuery

### Dataset Operations

```bash
# Create dataset
bq mk --dataset my_project:my_dataset

# With location
bq mk --dataset --location=US my_project:my_dataset

# List datasets
bq ls

# Describe dataset
bq show my_dataset

# Delete dataset
bq rm -r -f my_dataset  # -r removes tables, -f force
```

### Table Operations

```bash
# Create table with schema
bq mk --table my_dataset.my_table name:STRING,age:INTEGER,email:STRING

# Create table from schema file
bq mk --table my_dataset.my_table schema.json

# List tables
bq ls my_dataset

# Describe table
bq show my_dataset.my_table

# Delete table
bq rm -f my_dataset.my_table
```

### Query Operations

```bash
# Run query
bq query --use_legacy_sql=false 'SELECT * FROM my_dataset.my_table LIMIT 10'

# Save query results to table
bq query --use_legacy_sql=false \
    --destination_table=my_dataset.results \
    'SELECT * FROM my_dataset.my_table WHERE age > 30'

# Export to Cloud Storage
bq extract --destination_format=CSV \
    my_dataset.my_table \
    gs://my-bucket/export/*.csv
```

### Data Loading

```bash
# Load from CSV
bq load --source_format=CSV \
    my_dataset.my_table \
    gs://my-bucket/data.csv \
    name:STRING,age:INTEGER,email:STRING

# Load from JSON
bq load --source_format=NEWLINE_DELIMITED_JSON \
    my_dataset.my_table \
    gs://my-bucket/data.json \
    schema.json

# Load with autodetect schema
bq load --autodetect \
    --source_format=CSV \
    my_dataset.my_table \
    gs://my-bucket/data.csv
```

---

## IAM (Identity and Access Management)

### Service Accounts

```bash
# Create service account
gcloud iam service-accounts create my-service-account \
    --display-name="My Service Account"

# List service accounts
gcloud iam service-accounts list

# Create key for service account
gcloud iam service-accounts keys create key.json \
    --iam-account=my-service-account@my-project.iam.gserviceaccount.com

# List keys
gcloud iam service-accounts keys list \
    --iam-account=my-service-account@my-project.iam.gserviceaccount.com

# Delete key
gcloud iam service-accounts keys delete KEY_ID \
    --iam-account=my-service-account@my-project.iam.gserviceaccount.com

# Delete service account
gcloud iam service-accounts delete my-service-account@my-project.iam.gserviceaccount.com
```

### IAM Bindings

```bash
# View project IAM policy
gcloud projects get-iam-policy my-project

# Add IAM binding
gcloud projects add-iam-policy-binding my-project \
    --member=user:user@example.com \
    --role=roles/viewer

# Add service account binding
gcloud projects add-iam-policy-binding my-project \
    --member=serviceAccount:my-sa@my-project.iam.gserviceaccount.com \
    --role=roles/storage.admin

# Remove IAM binding
gcloud projects remove-iam-policy-binding my-project \
    --member=user:user@example.com \
    --role=roles/viewer

# Grant Cloud Run invoker
gcloud run services add-iam-policy-binding my-service \
    --region=us-central1 \
    --member=allUsers \
    --role=roles/run.invoker
```

### Custom Roles

```bash
# Create custom role
gcloud iam roles create myCustomRole \
    --project=my-project \
    --title="My Custom Role" \
    --description="Custom role for specific access" \
    --permissions=storage.buckets.list,storage.objects.get

# List custom roles
gcloud iam roles list --project=my-project

# Update custom role
gcloud iam roles update myCustomRole \
    --project=my-project \
    --add-permissions=storage.objects.create

# Delete custom role
gcloud iam roles delete myCustomRole --project=my-project
```

---

## VPC Networking

### Networks

```bash
# Create VPC network
gcloud compute networks create my-vpc \
    --subnet-mode=custom

# Create subnet
gcloud compute networks subnets create my-subnet \
    --network=my-vpc \
    --region=us-central1 \
    --range=10.0.0.0/24

# List networks
gcloud compute networks list

# List subnets
gcloud compute networks subnets list

# Delete subnet
gcloud compute networks subnets delete my-subnet --region=us-central1

# Delete network
gcloud compute networks delete my-vpc
```

### Firewall Rules

```bash
# Create firewall rule (allow SSH)
gcloud compute firewall-rules create allow-ssh \
    --network=my-vpc \
    --allow=tcp:22 \
    --source-ranges=0.0.0.0/0 \
    --target-tags=ssh-enabled

# Create firewall rule (allow HTTP/HTTPS)
gcloud compute firewall-rules create allow-http \
    --network=my-vpc \
    --allow=tcp:80,tcp:443 \
    --source-ranges=0.0.0.0/0 \
    --target-tags=http-server

# Create firewall rule (internal)
gcloud compute firewall-rules create allow-internal \
    --network=my-vpc \
    --allow=tcp,udp,icmp \
    --source-ranges=10.0.0.0/8

# List firewall rules
gcloud compute firewall-rules list

# Delete firewall rule
gcloud compute firewall-rules delete allow-ssh
```

### Static IPs and NAT

```bash
# Reserve static IP
gcloud compute addresses create my-static-ip \
    --region=us-central1

# List addresses
gcloud compute addresses list

# Create Cloud NAT
gcloud compute routers create my-router \
    --network=my-vpc \
    --region=us-central1

gcloud compute routers nats create my-nat \
    --router=my-router \
    --region=us-central1 \
    --nat-all-subnet-ip-ranges \
    --auto-allocate-nat-external-ips
```

### Load Balancing

```bash
# Create health check
gcloud compute health-checks create http my-health-check \
    --port=80

# Create backend service
gcloud compute backend-services create my-backend \
    --protocol=HTTP \
    --health-checks=my-health-check \
    --global

# Add instance group to backend
gcloud compute backend-services add-backend my-backend \
    --instance-group=my-instance-group \
    --instance-group-zone=us-central1-a \
    --global

# Create URL map
gcloud compute url-maps create my-url-map \
    --default-service=my-backend

# Create target proxy
gcloud compute target-http-proxies create my-proxy \
    --url-map=my-url-map

# Create forwarding rule
gcloud compute forwarding-rules create my-lb \
    --global \
    --target-http-proxy=my-proxy \
    --ports=80
```

---

## Secret Manager

### Secret Operations

```bash
# Create secret
gcloud secrets create my-secret

# Add secret version
echo -n "my-secret-value" | gcloud secrets versions add my-secret --data-file=-

# Add secret from file
gcloud secrets versions add my-secret --data-file=secret.txt

# List secrets
gcloud secrets list

# Access secret (get value)
gcloud secrets versions access latest --secret=my-secret

# Access specific version
gcloud secrets versions access 1 --secret=my-secret

# List versions
gcloud secrets versions list my-secret

# Disable version
gcloud secrets versions disable 1 --secret=my-secret

# Delete secret
gcloud secrets delete my-secret
```

### IAM for Secrets

```bash
# Grant access to secret
gcloud secrets add-iam-policy-binding my-secret \
    --member=serviceAccount:my-sa@my-project.iam.gserviceaccount.com \
    --role=roles/secretmanager.secretAccessor

# View IAM policy
gcloud secrets get-iam-policy my-secret
```

---

## Cloud Logging and Monitoring

### Logging

```bash
# Read logs
gcloud logging read "resource.type=gce_instance" --limit=50

# Read logs with filter
gcloud logging read 'severity>=ERROR AND resource.type="cloud_run_revision"' \
    --limit=100

# Read logs for specific resource
gcloud logging read 'resource.labels.function_name="my-function"' \
    --limit=50

# Stream logs (tail)
gcloud logging tail "resource.type=cloud_run_revision"

# Write log entry
gcloud logging write my-log "Test log message" --severity=INFO
```

### Metrics

```bash
# List metric descriptors
gcloud monitoring metrics list

# Get time series data
gcloud monitoring metrics read \
    'compute.googleapis.com/instance/cpu/utilization' \
    --start-time="2024-01-01T00:00:00Z" \
    --end-time="2024-01-02T00:00:00Z"
```

### Alerting

```bash
# Create notification channel
gcloud alpha monitoring channels create \
    --display-name="Email Channel" \
    --type=email \
    --channel-labels=email_address=alerts@example.com

# List notification channels
gcloud alpha monitoring channels list

# Create alert policy (via JSON)
gcloud alpha monitoring policies create --policy-from-file=alert-policy.json
```

---

## Pub/Sub

### Topics

```bash
# Create topic
gcloud pubsub topics create my-topic

# List topics
gcloud pubsub topics list

# Delete topic
gcloud pubsub topics delete my-topic

# Publish message
gcloud pubsub topics publish my-topic --message="Hello World"

# Publish with attributes
gcloud pubsub topics publish my-topic \
    --message="Hello" \
    --attribute=key1=value1,key2=value2
```

### Subscriptions

```bash
# Create pull subscription
gcloud pubsub subscriptions create my-sub --topic=my-topic

# Create push subscription
gcloud pubsub subscriptions create my-push-sub \
    --topic=my-topic \
    --push-endpoint=https://example.com/webhook

# List subscriptions
gcloud pubsub subscriptions list

# Pull messages
gcloud pubsub subscriptions pull my-sub --limit=10 --auto-ack

# Delete subscription
gcloud pubsub subscriptions delete my-sub
```

---

## Artifact Registry

### Repository Management

```bash
# Create Docker repository
gcloud artifacts repositories create my-repo \
    --repository-format=docker \
    --location=us-central1

# List repositories
gcloud artifacts repositories list

# Configure Docker authentication
gcloud auth configure-docker us-central1-docker.pkg.dev

# Push image
docker tag my-image us-central1-docker.pkg.dev/my-project/my-repo/my-image:v1
docker push us-central1-docker.pkg.dev/my-project/my-repo/my-image:v1

# List images
gcloud artifacts docker images list us-central1-docker.pkg.dev/my-project/my-repo

# Delete image
gcloud artifacts docker images delete \
    us-central1-docker.pkg.dev/my-project/my-repo/my-image:v1
```

---

## Security Best Practices

### Credential Management

```bash
# Never hardcode credentials - use IAM roles and service accounts
# Use Workload Identity for GKE
# Use Secret Manager for application secrets

# Rotate service account keys
gcloud iam service-accounts keys create new-key.json \
    --iam-account=my-sa@my-project.iam.gserviceaccount.com
# Delete old key after updating applications

# Use short-lived credentials
gcloud auth print-access-token  # 1 hour token
```

### Least Privilege

```bash
# Use predefined roles when possible
# Create custom roles for specific needs
# Regularly audit IAM policies

# Check who has access
gcloud asset search-all-iam-policies \
    --scope=projects/my-project \
    --query="policy:roles/owner"

# IAM Recommender
gcloud recommender recommendations list \
    --project=my-project \
    --location=global \
    --recommender=google.iam.policy.Recommender
```

### Encryption

```bash
# Enable CMEK for Cloud Storage
gcloud storage buckets update gs://my-bucket \
    --default-encryption-key=projects/my-project/locations/us/keyRings/my-ring/cryptoKeys/my-key

# Enable CMEK for Cloud SQL
gcloud sql instances patch my-instance \
    --disk-encryption-key=projects/my-project/locations/us/keyRings/my-ring/cryptoKeys/my-key

# Create KMS key ring
gcloud kms keyrings create my-ring --location=us

# Create KMS key
gcloud kms keys create my-key \
    --keyring=my-ring \
    --location=us \
    --purpose=encryption
```

### Audit Logging

```bash
# Enable data access audit logs
gcloud projects get-iam-policy my-project --format=yaml > policy.yaml
# Edit policy.yaml to add auditConfigs
gcloud projects set-iam-policy my-project policy.yaml

# View audit logs
gcloud logging read 'logName:"cloudaudit.googleapis.com"' --limit=50
```

---

## Common Patterns

### CI/CD Deployment

```bash
# Build and push to Artifact Registry
gcloud builds submit --tag us-central1-docker.pkg.dev/my-project/my-repo/my-app:$TAG

# Deploy to Cloud Run
gcloud run deploy my-app \
    --image=us-central1-docker.pkg.dev/my-project/my-repo/my-app:$TAG \
    --region=us-central1

# Deploy to GKE
kubectl set image deployment/my-app my-app=us-central1-docker.pkg.dev/my-project/my-repo/my-app:$TAG
```

### Blue-Green Deployment

```bash
# Deploy to green (no traffic)
gcloud run deploy my-app \
    --image=us-central1-docker.pkg.dev/my-project/my-repo/my-app:v2 \
    --region=us-central1 \
    --no-traffic \
    --tag=green

# Test green deployment
curl https://green---my-app-xxxx.run.app

# Shift traffic
gcloud run services update-traffic my-app \
    --region=us-central1 \
    --to-tags=green=100
```

### Disaster Recovery

```bash
# Create cross-region replica (Cloud SQL)
gcloud sql instances create my-replica \
    --master-instance-name=my-primary \
    --region=europe-west1

# Copy snapshot to another region (Compute Engine)
gcloud compute snapshots create my-snapshot-dr \
    --source-disk=my-disk \
    --source-disk-zone=us-central1-a \
    --storage-location=europe-west1

# Multi-region Cloud Storage bucket
gcloud storage buckets create gs://my-dr-bucket --location=eu
```

### Cost Optimization

```bash
# Find idle resources
gcloud recommender recommendations list \
    --project=my-project \
    --location=us-central1-a \
    --recommender=google.compute.instance.IdleResourceRecommender

# List committed use discounts
gcloud compute commitments list

# View billing export
bq query --use_legacy_sql=false '
SELECT
  service.description,
  SUM(cost) as total_cost
FROM `my-project.billing_export.gcp_billing_export_v1_*`
WHERE DATE(_PARTITIONTIME) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10'
```

---

## Output Formatting

### Format Options

```bash
# JSON output
gcloud compute instances list --format=json

# YAML output
gcloud compute instances list --format=yaml

# Table output
gcloud compute instances list --format=table

# Custom format
gcloud compute instances list \
    --format="table(name,zone,machineType,status)"

# Value only
gcloud compute instances describe my-instance \
    --format="value(networkInterfaces[0].accessConfigs[0].natIP)"

# CSV output
gcloud compute instances list \
    --format="csv(name,zone,machineType)"
```

### Filtering

```bash
# Filter by field
gcloud compute instances list --filter="status=RUNNING"

# Multiple filters
gcloud compute instances list \
    --filter="status=RUNNING AND machineType:n2-*"

# Filter by label
gcloud compute instances list --filter="labels.env=production"

# Filter by creation time
gcloud compute instances list \
    --filter="creationTimestamp>'2024-01-01'"
```

---

## Troubleshooting

### Debug Mode

```bash
# Enable verbose output
gcloud compute instances list --verbosity=debug

# Log HTTP requests
gcloud compute instances list --log-http

# Check current configuration
gcloud info

# Check authentication
gcloud auth list
gcloud config list account
```

### Common Errors

```bash
# Permission denied - check IAM roles
gcloud projects get-iam-policy my-project

# API not enabled
gcloud services enable compute.googleapis.com
gcloud services enable run.googleapis.com

# Quota exceeded
gcloud compute project-info describe --format="yaml(quotas)"
gcloud compute regions describe us-central1 --format="yaml(quotas)"

# Network errors
gcloud compute firewall-rules list
gcloud compute routes list
```

### Health Checks

```bash
# Check service health
gcloud run services describe my-service --region=us-central1

# Check GKE cluster
gcloud container clusters describe my-cluster --zone=us-central1-a

# Check Cloud SQL
gcloud sql instances describe my-instance
```

---

*Google Cloud CLI Skill v1.0*
*Layer 3 Technical Skill*
*Used by: faion-devops-agent*
