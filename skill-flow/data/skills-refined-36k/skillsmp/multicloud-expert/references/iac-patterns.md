# Infrastructure as Code Patterns

## Table of Contents
- [Terraform](#terraform)
- [Pulumi](#pulumi)
- [CloudFormation](#cloudformation)
- [Tool Comparison](#tool-comparison)

## Terraform

### Module Structure
```
module/
├── main.tf          # Primary resources
├── variables.tf     # Input variables
├── outputs.tf       # Output values
├── versions.tf      # Provider constraints
└── locals.tf        # Local values (optional)
```

### Version Pinning
```hcl
terraform {
  required_version = ">= 1.5.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"  # >= 5.0, < 6.0
    }
  }
}
```

### State Management
```hcl
# Remote backend (AWS example)
terraform {
  backend "s3" {
    bucket         = "terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "eu-west-2"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

### Common Patterns

**Conditional creation:**
```hcl
resource "aws_eip" "this" {
  count = var.create_public_ip ? 1 : 0
}
```

**For_each (stable addressing):**
```hcl
resource "aws_instance" "this" {
  for_each      = var.instances  # map
  instance_type = each.value.type
  tags          = { Name = each.key }
}
```

**Dynamic blocks:**
```hcl
dynamic "ingress" {
  for_each = var.ingress_rules
  content {
    from_port   = ingress.value.from_port
    to_port     = ingress.value.to_port
    protocol    = ingress.value.protocol
    cidr_blocks = ingress.value.cidr_blocks
  }
}
```

**Moved blocks (refactoring):**
```hcl
moved {
  from = aws_instance.old_name
  to   = aws_instance.new_name
}
```

### Import Workflow
```bash
# Import existing resource
terraform import aws_instance.web i-1234567890abcdef0

# Generate config (TF 1.5+)
terraform plan -generate-config-out=generated.tf
```

## Pulumi

### Project Structure
```
project/
├── Pulumi.yaml       # Project definition
├── Pulumi.dev.yaml   # Stack config (dev)
├── Pulumi.prod.yaml  # Stack config (prod)
├── __main__.py       # Program entry (Python)
└── requirements.txt  # Dependencies
```

### Python Example
```python
import pulumi
import pulumi_aws as aws

# Create resource
bucket = aws.s3.Bucket("my-bucket",
    versioning=aws.s3.BucketVersioningArgs(enabled=True),
    tags={"Environment": pulumi.get_stack()}
)

# Export output
pulumi.export("bucket_name", bucket.id)

# Conditional creation
if pulumi.get_stack() == "prod":
    alarm = aws.cloudwatch.MetricAlarm("alarm", ...)

# Transformations (bulk tag application)
def add_tags(args):
    if hasattr(args.props, "tags"):
        args.props["tags"] = {**args.props.get("tags", {}), "ManagedBy": "pulumi"}
    return pulumi.ResourceTransformationResult(args.props, args.opts)

pulumi.runtime.register_stack_transformation(add_tags)
```

### State Management
```bash
# Login to backend
pulumi login s3://pulumi-state-bucket

# Stack operations
pulumi stack init dev
pulumi stack select prod
```

### Import Workflow
```bash
# Import existing resource
pulumi import aws:s3/bucket:Bucket my-bucket my-bucket-name
```

## CloudFormation

### Template Structure
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: My stack

Parameters:
  Environment:
    Type: String
    AllowedValues: [dev, staging, prod]

Conditions:
  IsProd: !Equals [!Ref Environment, prod]

Resources:
  MyBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub 'my-bucket-${Environment}'
      Tags:
        - Key: Environment
          Value: !Ref Environment

Outputs:
  BucketArn:
    Value: !GetAtt MyBucket.Arn
    Export:
      Name: !Sub '${AWS::StackName}-BucketArn'
```

### Intrinsic Functions
| Function | Purpose | Example |
|----------|---------|---------|
| `!Ref` | Reference parameter/resource | `!Ref MyBucket` |
| `!GetAtt` | Get resource attribute | `!GetAtt MyBucket.Arn` |
| `!Sub` | String substitution | `!Sub 'arn:aws:s3:::${BucketName}'` |
| `!Join` | Join strings | `!Join ['-', [!Ref Env, bucket]]` |
| `!If` | Conditional value | `!If [IsProd, 3, 1]` |
| `!ImportValue` | Cross-stack reference | `!ImportValue OtherStack-VpcId` |

### StackSets (Multi-Account/Region)
```yaml
# Deploy to multiple accounts/regions
aws cloudformation create-stack-set \
  --stack-set-name my-stackset \
  --template-body file://template.yaml \
  --permission-model SERVICE_MANAGED \
  --auto-deployment Enabled=true
```

### Import Workflow
```bash
# Create change set for import
aws cloudformation create-change-set \
  --stack-name my-stack \
  --change-set-name import-bucket \
  --change-set-type IMPORT \
  --resources-to-import "[{\"ResourceType\":\"AWS::S3::Bucket\",\"LogicalResourceId\":\"MyBucket\",\"ResourceIdentifier\":{\"BucketName\":\"existing-bucket\"}}]" \
  --template-body file://template.yaml
```

## Tool Comparison

| Aspect | Terraform | Pulumi | CloudFormation |
|--------|-----------|--------|----------------|
| **Language** | HCL | Python/TS/Go/C# | YAML/JSON |
| **State** | Self-managed or Terraform Cloud | Pulumi Cloud or self-hosted | AWS-managed |
| **Multi-cloud** | Native | Native | AWS only |
| **Learning curve** | Medium | Low (if you know the language) | Medium |
| **Drift detection** | `terraform plan` | `pulumi preview` | Drift detection feature |
| **Secret handling** | External (Vault, etc.) | Built-in encryption | Parameter Store/Secrets Manager |
| **Testing** | Terratest, built-in tests | Native unit tests | TaskCat, cfn-lint |

### When to Use What

**Terraform:**
- Multi-cloud standardisation
- Large ecosystem of providers
- Team with mixed programming backgrounds

**Pulumi:**
- Team strong in one language
- Complex logic in infrastructure
- Need real programming constructs (loops, functions, tests)

**CloudFormation:**
- AWS-only, want native integration
- StackSets for multi-account
- Organisation mandates it
