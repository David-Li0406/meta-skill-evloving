# Terraform Security Patterns

**Category**: devops/iac-policies/terraform
**Description**: Terraform security and organizational policy patterns
**CWE**: CWE-732, CWE-311

---

## Access Control Patterns

### Public S3 Bucket ACL
**Pattern**: `(?i)acl\s*=\s*["'](?:public-read|public-read-write)["']`
**Type**: regex
**Severity**: critical
**Languages**: [terraform]
- S3 buckets should not have public ACLs
- Remediation: Use `acl = "private"` and configure bucket policies
- CWE-732: Incorrect Permission Assignment

### S3 Bucket Without Encryption
**Pattern**: `(?i)resource\s*"aws_s3_bucket"\s*"[^"]+"\s*\{(?:(?!server_side_encryption_configuration).)*\}`
**Type**: regex
**Severity**: high
**Languages**: [terraform]
- S3 buckets should have server-side encryption enabled
- Remediation: Add encryption configuration with AES-256 or AWS KMS
- CWE-311: Missing Encryption of Sensitive Data

### Public Security Group Ingress
**Pattern**: `(?i)cidr_blocks\s*=\s*\[\s*["']0\.0\.0\.0/0["']`
**Type**: regex
**Severity**: critical
**Languages**: [terraform]
- Security groups should not allow unrestricted ingress
- Remediation: Restrict CIDR blocks to specific IP ranges

### Open SSH Port to World
**Pattern**: `(?i)from_port\s*=\s*22[^0-9].*?cidr_blocks\s*=\s*\[\s*["']0\.0\.0\.0/0["']`
**Type**: regex
**Severity**: critical
**Languages**: [terraform]
- SSH access should not be open to the entire internet
- Remediation: Restrict SSH access or use bastion hosts

### Open RDP Port to World
**Pattern**: `(?i)from_port\s*=\s*3389[^0-9].*?cidr_blocks\s*=\s*\[\s*["']0\.0\.0\.0/0["']`
**Type**: regex
**Severity**: critical
**Languages**: [terraform]
- RDP access should not be open to the entire internet
- Remediation: Restrict RDP access or use VPN

---

## Encryption Patterns

### Unencrypted EBS Volume
**Pattern**: `(?i)resource\s*"aws_ebs_volume".*?encrypted\s*=\s*false`
**Type**: regex
**Severity**: high
**Languages**: [terraform]
- EBS volumes should be encrypted at rest
- Remediation: Set `encrypted = true` and configure KMS key

### RDS Without Encryption
**Pattern**: `(?i)resource\s*"aws_db_instance".*?storage_encrypted\s*=\s*false`
**Type**: regex
**Severity**: high
**Languages**: [terraform]
- RDS instances should have storage encryption enabled
- Remediation: Set `storage_encrypted = true`

### RDS Public Access
**Pattern**: `(?i)publicly_accessible\s*=\s*true`
**Type**: regex
**Severity**: critical
**Languages**: [terraform]
- Database instances should not be publicly accessible
- Remediation: Set `publicly_accessible = false`

### ELB Without SSL
**Pattern**: `(?i)resource\s*"aws_elb".*?listener\s*\{[^}]*lb_protocol\s*=\s*["']HTTP["']`
**Type**: regex
**Severity**: high
**Languages**: [terraform]
- Load balancers should use HTTPS
- Remediation: Configure `lb_protocol = "HTTPS"` with SSL certificate

---

## Logging and Monitoring Patterns

### CloudTrail Not Enabled
**Pattern**: `(?i)enable_logging\s*=\s*false`
**Type**: regex
**Severity**: high
**Languages**: [terraform]
- CloudTrail logging should be enabled for audit purposes
- Remediation: Set `enable_logging = true`

### VPC Flow Logs Disabled
**Pattern**: `(?i)resource\s*"aws_vpc"(?:(?!aws_flow_log).)*$`
**Type**: regex
**Severity**: medium
**Languages**: [terraform]
- VPCs should have flow logs enabled for network monitoring
- Remediation: Create `aws_flow_log` resource for the VPC

### S3 Access Logging Disabled
**Pattern**: `(?i)resource\s*"aws_s3_bucket"\s*"[^"]+"\s*\{(?:(?!logging).)*\}`
**Type**: regex
**Severity**: medium
**Languages**: [terraform]
- S3 buckets should have access logging enabled
- Remediation: Add `logging` block with target bucket

---

## IAM Patterns

### Wildcard IAM Action
**Pattern**: `(?i)"Action"\s*:\s*\[\s*["']\*["']`
**Type**: regex
**Severity**: high
**Languages**: [terraform]
- IAM policies should not grant wildcard actions
- Remediation: Specify required actions explicitly

### Wildcard IAM Resource
**Pattern**: `(?i)"Resource"\s*:\s*\[\s*["']\*["']`
**Type**: regex
**Severity**: medium
**Languages**: [terraform]
- IAM policies should not grant access to all resources
- Remediation: Specify specific resource ARNs

### Assume Role Without Condition
**Pattern**: `(?i)"Effect"\s*:\s*["']Allow["'].*?"Action"\s*:\s*\[\s*["']sts:AssumeRole["'](?:(?!"Condition").)*$`
**Type**: regex
**Severity**: medium
**Languages**: [terraform]
- AssumeRole policies should have conditions
- Remediation: Add external ID or MFA requirement

---

## Network Patterns

### Missing VPC Security Groups
**Pattern**: `(?i)resource\s*"aws_instance"(?:(?!vpc_security_group_ids).)*\}`
**Type**: regex
**Severity**: medium
**Languages**: [terraform]
- EC2 instances should be deployed in VPC with security groups
- Remediation: Deploy in VPC with appropriate security groups

### Default Security Group Used
**Pattern**: `(?i)security_groups\s*=\s*\[\s*["']default["']`
**Type**: regex
**Severity**: medium
**Languages**: [terraform]
- Default security groups should not be used
- Remediation: Create and use custom security groups

---

## Organizational Policies

### Missing Tags
**Pattern**: `(?i)resource\s*"aws_[^"]+"\s*"[^"]+"\s*\{(?:(?!tags).)*\}`
**Type**: regex
**Severity**: low
**Languages**: [terraform]
- Resources should be tagged for cost allocation
- Remediation: Add tags including Owner, Environment, Project

### Missing Provider Region
**Pattern**: `(?i)provider\s*"aws"\s*\{(?:(?!region).)*\}`
**Type**: regex
**Severity**: low
**Languages**: [terraform]
- AWS provider should have explicit region configuration
- Remediation: Specify `region` in provider block

---

## References

- [CWE-732: Incorrect Permission Assignment](https://cwe.mitre.org/data/definitions/732.html)
- [CWE-311: Missing Encryption of Sensitive Data](https://cwe.mitre.org/data/definitions/311.html)
- [CIS AWS Foundations Benchmark](https://www.cisecurity.org/benchmark/amazon_web_services)
