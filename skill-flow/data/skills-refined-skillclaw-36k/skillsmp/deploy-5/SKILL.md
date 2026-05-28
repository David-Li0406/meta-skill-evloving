---
name: deploy
description: Deploy applications to AWS (SageMaker, Amplify, EC2). Use this skill to deploy models, frontends, or manage infrastructure. Invoke with /deploy.
---

# AWS Deployment

This skill manages deployments to AWS services for the wc_simd project.

## SageMaker Endpoints

### Deploy Embedding Model

```bash
cd demos/timetrvlr/cdk
npm install
cdk deploy
```

Or manually:
```python
import sagemaker
from sagemaker.huggingface import HuggingFaceModel

model = HuggingFaceModel(
    model_data="s3://bucket/model.tar.gz",
    role="arn:aws:iam::xxx:role/SageMakerRole",
    transformers_version="4.37",
    pytorch_version="2.1",
    py_version="py310"
)

predictor = model.deploy(
    instance_type="ml.g5.xlarge",
    endpoint_name="embedding-endpoint"
)
```

### Async Inference

For long-running inference (VLM embeddings):
```python
from sagemaker.async_inference import AsyncInferenceConfig

async_config = AsyncInferenceConfig(
    output_path="s3://bucket/async-output/",
    max_concurrent_invocations_per_instance=4
)

predictor = model.deploy(
    instance_type="ml.g5.2xlarge",
    async_inference_config=async_config
)
```

### SageMaker Auto-Scaling & 504 Errors

**Common Issue**: Endpoint returns 504 "Service Unavailable" after periods of inactivity.

**Cause**: Auto-scaling with `MinCapacity=0` scales down to zero instances. When a request comes in, the endpoint enters "Updating" state while scaling up (~5-10 min).

**Check current scaling config**:
```bash
aws application-autoscaling describe-scalable-targets \
  --service-namespace sagemaker \
  --resource-ids "endpoint/<ENDPOINT_NAME>/variant/AllTraffic" \
  --region eu-west-2
```

**Fix: Keep at least 1 instance running** (prevents scale-to-zero):
```bash
aws application-autoscaling register-scalable-target \
  --service-namespace sagemaker \
  --resource-id "endpoint/<ENDPOINT_NAME>/variant/AllTraffic" \
  --scalable-dimension "sagemaker:variant:DesiredInstanceCount" \
  --min-capacity 1 \
  --max-capacity 1 \
  --region eu-west-2
```

**Revert to scale-to-zero** (saves costs when not in use):
```bash
aws application-autoscaling register-scalable-target \
  --service-namespace sagemaker \
  --resource-id "endpoint/<ENDPOINT_NAME>/variant/AllTraffic" \
  --scalable-dimension "sagemaker:variant:DesiredInstanceCount" \
  --min-capacity 0 \
  --max-capacity 1 \
  --region eu-west-2
```

**Cost note**: ml.g4dn.xlarge costs ~$0.526/hour (~$380/month) when always running.

### Update SageMaker Endpoint with New Docker Image

After pushing a new image to ECR:

```bash
TIMESTAMP=$(date +%s)
NEW_MODEL_NAME="EmbeddingModel-$TIMESTAMP"
NEW_CONFIG_NAME="EmbeddingEndpointConfig-$TIMESTAMP"
ENDPOINT_NAME="EmbeddingEndpoint-u6w61sZPU1fj"
ECR_IMAGE="760097843905.dkr.ecr.eu-west-2.amazonaws.com/embed-inference:latest"

# 1. Create new model
aws sagemaker create-model \
  --model-name "$NEW_MODEL_NAME" \
  --primary-container Image=$ECR_IMAGE,Mode=SingleModel \
  --execution-role-arn "arn:aws:iam::760097843905:role/EmbeddingEndpointStack-EmbeddingModelExecutionRole3-AXtNk8S08NEo" \
  --region eu-west-2

# 2. Create new endpoint config
aws sagemaker create-endpoint-config \
  --endpoint-config-name "$NEW_CONFIG_NAME" \
  --production-variants VariantName=AllTraffic,ModelName=$NEW_MODEL_NAME,InitialInstanceCount=1,InstanceType=ml.g4dn.xlarge,InitialVariantWeight=1,ContainerStartupHealthCheckTimeoutInSeconds=600 \
  --async-inference-config "ClientConfig={MaxConcurrentInvocationsPerInstance=1},OutputConfig={S3OutputPath=s3://embeddingendpointstack-asyncoutputbucketea73fa4d-gsaebf9dvszc/results/,S3FailurePath=s3://embeddingendpointstack-asyncoutputbucketea73fa4d-gsaebf9dvszc/failures/}" \
  --region eu-west-2

# 3. Update endpoint (takes 5-10 min)
aws sagemaker update-endpoint \
  --endpoint-name "$ENDPOINT_NAME" \
  --endpoint-config-name "$NEW_CONFIG_NAME" \
  --region eu-west-2

# 4. Wait for update
watch -n 30 "aws sagemaker describe-endpoint --endpoint-name $ENDPOINT_NAME --region eu-west-2 --query 'EndpointStatus' --output text"
```

## AWS Amplify (Frontend)

### TimeTraveler Demo

```bash
cd demos/timetrvlr/amplify-cdk
npm install
cdk deploy
```

The CDK stack:
- Connects to GitHub repository
- Sets up build pipeline
- Configures custom domain (optional)
- Deploys Next.js/React frontend

### Manual Amplify Setup

```bash
amplify init
amplify add hosting
amplify publish
```

## EC2 Instances

### Start/Stop via Script
```bash
python aws/ec2_control.py start --name simd_gpu
python aws/ec2_control.py stop --name simd_gpu
```

### Launch New Instance
Use AWS Console or CLI:
```bash
aws ec2 run-instances \
  --image-id ami-xxx \
  --instance-type g5.xlarge \
  --key-name your-key \
  --security-group-ids sg-xxx \
  --iam-instance-profile Name=spark-docker-s3-profile
```

## S3 Data Management

### Upload Data
```bash
aws s3 sync data/ s3://bucket/data/
```

### Download Data
```bash
aws s3 sync s3://bucket/data/ data/
```

## RDS (Hive Metastore)

The production Spark stack uses RDS MySQL for the Hive metastore.

### Connect Manually
```bash
mysql -h <rds-endpoint> -u hive -p hive
```

### Initialize Schema
Set `INIT_HIVE_SCHEMA=true` in `spark_docker_s3/.env` on first run.

## CDK Stacks

| Stack | Location | Purpose |
|-------|----------|---------|
| `SparkDockerS3Stack` | `spark_docker_s3/infra/` | S3 bucket, RDS, IAM roles |
| `TimetrvlrStack` | `demos/timetrvlr/cdk/` | SageMaker endpoint |
| `AmplifyStack` | `demos/timetrvlr/amplify-cdk/` | Frontend hosting |

### Deploy CDK Stack
```bash
cd <stack-directory>
npm install
cdk bootstrap  # First time only
cdk synth      # Preview
cdk deploy     # Deploy
```

### Destroy Stack
```bash
cdk destroy
```

## Environment Variables

Required in `.env`:
```bash
AWS_REGION=eu-west-2
S3_BUCKET=your-bucket
HIVE_METASTORE_HOST=rds-endpoint
HIVE_METASTORE_USER=hive
HIVE_METASTORE_PASSWORD=xxx
```

Load with:
```python
from dotenv import load_dotenv
load_dotenv()
```
