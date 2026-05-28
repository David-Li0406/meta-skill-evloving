# AWS Encryption Patterns

Encrypt data at rest and in transit using AWS KMS.

## KMS Key Types

| Type | Use Case | Management | Cost |
|------|----------|------------|------|
| AWS Managed | Default encryption | AWS manages | Free |
| Customer Managed (CMK) | Custom policies | You manage | $1/month + usage |
| Customer Provided (BYOK) | Regulatory compliance | You provide | $1/month + usage |

## S3 Encryption

```yaml
# CloudFormation - Server-side encryption with CMK
SecureBucket:
  Type: AWS::S3::Bucket
  Properties:
    BucketEncryption:
      ServerSideEncryptionConfiguration:
        - ServerSideEncryptionByDefault:
            SSEAlgorithm: aws:kms
            KMSMasterKeyID: !GetAtt KMSKey.Arn
          BucketKeyEnabled: true  # Reduces KMS costs
```

```hcl
# Terraform
resource "aws_s3_bucket_server_side_encryption_configuration" "secure" {
  bucket = aws_s3_bucket.main.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.main.arn
      sse_algorithm     = "aws:kms"
    }
    bucket_key_enabled = true
  }
}
```

## RDS Encryption

```yaml
# Encryption at rest
SecureDatabase:
  Type: AWS::RDS::DBInstance
  Properties:
    StorageEncrypted: true
    KmsKeyId: !GetAtt KMSKey.Arn
```

```hcl
resource "aws_db_instance" "secure" {
  storage_encrypted = true
  kms_key_id        = aws_kms_key.main.arn

  # Encryption in transit
  parameter_group_name = aws_db_parameter_group.ssl_required.name
}

resource "aws_db_parameter_group" "ssl_required" {
  family = "postgres14"
  parameter {
    name  = "rds.force_ssl"
    value = "1"
  }
}
```

## EBS Volume Encryption

```yaml
# Default encryption for all new volumes
aws ec2 enable-ebs-encryption-by-default

# Encrypted volume
SecureVolume:
  Type: AWS::EC2::Volume
  Properties:
    Encrypted: true
    KmsKeyId: !GetAtt KMSKey.Arn
```

## Secrets Manager

```hcl
# Store secret
resource "aws_secretsmanager_secret" "db_password" {
  name       = "prod/database/password"
  kms_key_id = aws_kms_key.main.arn
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = random_password.db.result
}

# Access from Lambda/ECS
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = aws_secretsmanager_secret.db_password.id
}

# IAM policy for access
resource "aws_iam_policy" "read_secrets" {
  policy = jsonencode({
    Statement = [{
      Effect = "Allow"
      Action = [
        "secretsmanager:GetSecretValue"
      ]
      Resource = aws_secretsmanager_secret.db_password.arn
    }, {
      Effect = "Allow"
      Action = ["kms:Decrypt"]
      Resource = aws_kms_key.main.arn
    }]
  })
}
```

## KMS Key Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Enable IAM policies",
      "Effect": "Allow",
      "Principal": {"AWS": "arn:aws:iam::ACCOUNT:root"},
      "Action": "kms:*",
      "Resource": "*"
    },
    {
      "Sid": "Allow use by specific role",
      "Effect": "Allow",
      "Principal": {"AWS": "arn:aws:iam::ACCOUNT:role/AppRole"},
      "Action": [
        "kms:Encrypt",
        "kms:Decrypt",
        "kms:GenerateDataKey*"
      ],
      "Resource": "*"
    }
  ]
}
```

## In-Transit Encryption

### ALB to Targets

```yaml
HTTPSListener:
  Type: AWS::ElasticLoadBalancingV2::Listener
  Properties:
    Protocol: HTTPS
    Certificates:
      - CertificateArn: !Ref Certificate
    DefaultActions:
      - Type: forward
        TargetGroupArn: !Ref TargetGroup

# Backend encryption (HTTPS to targets)
TargetGroup:
  Type: AWS::ElasticLoadBalancingV2::TargetGroup
  Properties:
    Protocol: HTTPS  # Not HTTP
    HealthCheckProtocol: HTTPS
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| SSE-S3 for sensitive data | AWS manages key | Use CMK |
| No key rotation | Compliance risk | Enable auto-rotation |
| Wide KMS permissions | Over-privileged | Scope to specific keys |
| Unencrypted snapshots | Data exposure | Encrypt before sharing |
| HTTP endpoints | Data in transit exposed | Force HTTPS |
