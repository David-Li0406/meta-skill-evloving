---
name: Cloud Providers
description: This skill should be used when the user asks to "deploy to AWS", "configure GCP", "Azure setup", "cloud infrastructure", "EC2 instance", "S3 bucket", "Lambda function", "Cloud Run", "Azure Functions", "terraform", "cloud networking", "VPC configuration", or needs help with AWS, GCP, or Azure resource management.
version: 1.0.0
---

# Cloud Providers

Comprehensive guidance for AWS, GCP, and Azure resource management and infrastructure.

## AWS (Amazon Web Services)

### EC2 (Compute)

```bash
# Launch instance
aws ec2 run-instances \
  --image-id ami-0abcdef1234567890 \
  --instance-type t3.medium \
  --key-name my-key \
  --security-group-ids sg-12345678 \
  --subnet-id subnet-12345678 \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=MyServer}]'

# List instances
aws ec2 describe-instances --filters "Name=tag:Name,Values=MyServer"

# Stop/Start
aws ec2 stop-instances --instance-ids i-1234567890abcdef0
aws ec2 start-instances --instance-ids i-1234567890abcdef0
```

### S3 (Storage)

```bash
# Create bucket
aws s3 mb s3://my-unique-bucket-name

# Sync files
aws s3 sync ./dist s3://my-bucket/static --delete

# Set lifecycle policy
aws s3api put-bucket-lifecycle-configuration \
  --bucket my-bucket \
  --lifecycle-configuration file://lifecycle.json
```

### Lambda

```bash
# Create function
aws lambda create-function \
  --function-name my-function \
  --runtime nodejs20.x \
  --handler index.handler \
  --zip-file fileb://function.zip \
  --role arn:aws:iam::123456789:role/lambda-role

# Invoke
aws lambda invoke \
  --function-name my-function \
  --payload '{"key": "value"}' \
  response.json
```

### ECS/Fargate

```json
// task-definition.json
{
  "family": "myapp",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "myapp",
      "image": "123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:latest",
      "portMappings": [
        {
          "containerPort": 8080,
          "protocol": "tcp"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/myapp",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### VPC Networking

```bash
# Create VPC
aws ec2 create-vpc --cidr-block 10.0.0.0/16

# Create subnets
aws ec2 create-subnet --vpc-id vpc-123 --cidr-block 10.0.1.0/24 --availability-zone us-east-1a
aws ec2 create-subnet --vpc-id vpc-123 --cidr-block 10.0.2.0/24 --availability-zone us-east-1b

# Create Internet Gateway
aws ec2 create-internet-gateway
aws ec2 attach-internet-gateway --vpc-id vpc-123 --internet-gateway-id igw-123
```

## GCP (Google Cloud Platform)

### Compute Engine

```bash
# Create instance
gcloud compute instances create my-instance \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --image-family=debian-12 \
  --image-project=debian-cloud \
  --boot-disk-size=20GB

# List instances
gcloud compute instances list

# SSH to instance
gcloud compute ssh my-instance --zone=us-central1-a
```

### Cloud Storage

```bash
# Create bucket
gsutil mb gs://my-unique-bucket

# Copy files
gsutil -m cp -r ./dist gs://my-bucket/static

# Set CORS
gsutil cors set cors.json gs://my-bucket
```

### Cloud Run

```bash
# Deploy service
gcloud run deploy my-service \
  --image gcr.io/my-project/my-image:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 10

# Update traffic
gcloud run services update-traffic my-service \
  --to-revisions=my-service-00002=50,my-service-00001=50
```

### Cloud Functions

```bash
# Deploy function
gcloud functions deploy my-function \
  --runtime nodejs20 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point handler \
  --source ./function
```

### VPC Networking

```bash
# Create VPC
gcloud compute networks create my-vpc --subnet-mode=custom

# Create subnet
gcloud compute networks subnets create my-subnet \
  --network=my-vpc \
  --range=10.0.0.0/24 \
  --region=us-central1
```

## Azure

### Virtual Machines

```bash
# Create VM
az vm create \
  --resource-group myResourceGroup \
  --name myVM \
  --image Ubuntu2204 \
  --admin-username azureuser \
  --generate-ssh-keys \
  --size Standard_B2s

# List VMs
az vm list --output table

# Start/Stop
az vm start --resource-group myResourceGroup --name myVM
az vm stop --resource-group myResourceGroup --name myVM
```

### Blob Storage

```bash
# Create storage account
az storage account create \
  --name mystorageaccount \
  --resource-group myResourceGroup \
  --location eastus \
  --sku Standard_LRS

# Create container
az storage container create \
  --name mycontainer \
  --account-name mystorageaccount

# Upload blob
az storage blob upload \
  --account-name mystorageaccount \
  --container-name mycontainer \
  --name myfile.txt \
  --file ./myfile.txt
```

### Azure Functions

```bash
# Create function app
az functionapp create \
  --resource-group myResourceGroup \
  --consumption-plan-location eastus \
  --runtime node \
  --runtime-version 20 \
  --functions-version 4 \
  --name myfunctionapp \
  --storage-account mystorageaccount

# Deploy
func azure functionapp publish myfunctionapp
```

### App Service

```bash
# Create app service plan
az appservice plan create \
  --name myAppServicePlan \
  --resource-group myResourceGroup \
  --sku B1 \
  --is-linux

# Create web app
az webapp create \
  --resource-group myResourceGroup \
  --plan myAppServicePlan \
  --name mywebapp \
  --runtime "NODE:20-lts"
```

## Terraform (Multi-Cloud)

### AWS Example

```hcl
# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = var.instance_type

  vpc_security_group_ids = [aws_security_group.web.id]
  subnet_id              = aws_subnet.public.id

  tags = {
    Name        = "web-server"
    Environment = var.environment
  }
}

resource "aws_security_group" "web" {
  name        = "web-sg"
  description = "Security group for web server"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

### Terraform Commands

```bash
# Initialize
terraform init

# Plan
terraform plan -out=tfplan

# Apply
terraform apply tfplan

# Destroy
terraform destroy

# State management
terraform state list
terraform state show aws_instance.web
```

## Cost Optimization

### AWS Cost Tools

```bash
# Get cost and usage
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-01-31 \
  --granularity MONTHLY \
  --metrics "BlendedCost" \
  --group-by Type=DIMENSION,Key=SERVICE
```

### Best Practices

| Strategy | AWS | GCP | Azure |
|----------|-----|-----|-------|
| Reserved capacity | Reserved Instances | Committed Use | Reserved VMs |
| Spot/Preemptible | Spot Instances | Preemptible VMs | Spot VMs |
| Right-sizing | Compute Optimizer | Recommender | Advisor |
| Auto-scaling | Auto Scaling | Autoscaler | VMSS |

## Additional Resources

### Reference Files

- **`references/aws-services.md`** - AWS service reference
- **`references/gcp-services.md`** - GCP service reference
- **`references/azure-services.md`** - Azure service reference

### Example Files

- **`examples/terraform-aws-vpc/`** - Complete AWS VPC setup
- **`examples/multi-cloud-deploy.tf`** - Multi-cloud Terraform
