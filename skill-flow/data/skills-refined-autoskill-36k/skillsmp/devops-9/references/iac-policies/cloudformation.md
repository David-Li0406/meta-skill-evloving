# CloudFormation Security Patterns

**Category**: devops/iac-policies/cloudformation
**Description**: AWS CloudFormation security and organizational policy patterns
**CWE**: CWE-732, CWE-311

---

## S3 Bucket Patterns

### Public S3 Bucket ACL
**Pattern**: `(?i)AccessControl:\s*(?:PublicRead|PublicReadWrite)`
**Type**: regex
**Severity**: critical
**Languages**: [yaml, cloudformation]
- S3 buckets should not have public ACLs
- Remediation: Use `AccessControl: Private` and bucket policies
- CWE-732: Incorrect Permission Assignment

### S3 Bucket Without Encryption
**Pattern**: `(?i)Type:\s*AWS::S3::Bucket(?:(?!BucketEncryption).)*$`
**Type**: regex
**Severity**: high
**Languages**: [yaml, cloudformation]
- S3 buckets should have encryption enabled
- Remediation: Add BucketEncryption with AES256 or aws:kms
- CWE-311: Missing Encryption of Sensitive Data

### S3 Public Access Not Blocked
**Pattern**: `(?i)BlockPublicAcls:\s*false`
**Type**: regex
**Severity**: high
**Languages**: [yaml, cloudformation]
- S3 buckets should block public access
- Remediation: Set all PublicAccessBlockConfiguration options to true

---

## Security Group Patterns

### Security Group Open to Internet
**Pattern**: `(?i)CidrIp:\s*0\.0\.0\.0/0`
**Type**: regex
**Severity**: critical
**Languages**: [yaml, cloudformation]
- Security groups should not allow unrestricted access
- Remediation: Restrict to specific CIDR ranges

### SSH Open to Internet
**Pattern**: `(?i)FromPort:\s*22[\s\S]*?CidrIp:\s*0\.0\.0\.0/0`
**Type**: regex
**Severity**: critical
**Languages**: [yaml, cloudformation]
- SSH should not be open to the internet
- Remediation: Use bastion hosts or VPN

### RDP Open to Internet
**Pattern**: `(?i)FromPort:\s*3389[\s\S]*?CidrIp:\s*0\.0\.0\.0/0`
**Type**: regex
**Severity**: critical
**Languages**: [yaml, cloudformation]
- RDP should not be open to the internet
- Remediation: Use bastion hosts or VPN

---

## RDS Patterns

### RDS Publicly Accessible
**Pattern**: `(?i)PubliclyAccessible:\s*(?:true|'true'|"true")`
**Type**: regex
**Severity**: critical
**Languages**: [yaml, cloudformation]
- RDS instances should not be publicly accessible
- Remediation: Set `PubliclyAccessible: false`

### RDS Without Encryption
**Pattern**: `(?i)Type:\s*AWS::RDS::DBInstance(?:(?!StorageEncrypted).)*$`
**Type**: regex
**Severity**: high
**Languages**: [yaml, cloudformation]
- RDS instances should have storage encryption
- Remediation: Add `StorageEncrypted: true`

### RDS Without Multi-AZ
**Pattern**: `(?i)MultiAZ:\s*(?:false|'false'|"false")`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, cloudformation]
- Production RDS instances should use Multi-AZ
- Remediation: Set `MultiAZ: true` for high availability

---

## IAM Patterns

### Wildcard IAM Action
**Pattern**: `(?i)Action:\s*\*`
**Type**: regex
**Severity**: high
**Languages**: [yaml, cloudformation]
- IAM policies should not use wildcard actions
- Remediation: Specify explicit actions

### Wildcard IAM Resource
**Pattern**: `(?i)Resource:\s*\*`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, cloudformation]
- IAM policies should not grant access to all resources
- Remediation: Specify resource ARNs

### IAM User With Console Access
**Pattern**: `(?i)Type:\s*AWS::IAM::User[\s\S]*?LoginProfile:`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, cloudformation]
- IAM users with console access should use SSO instead
- Remediation: Use AWS SSO or federated access

---

## EC2 Patterns

### EC2 Without IMDSv2
**Pattern**: `(?i)HttpTokens:\s*optional`
**Type**: regex
**Severity**: high
**Languages**: [yaml, cloudformation]
- EC2 instances should require IMDSv2
- Remediation: Set `HttpTokens: required`

### Unencrypted EBS Volume
**Pattern**: `(?i)Encrypted:\s*(?:false|'false'|"false")`
**Type**: regex
**Severity**: high
**Languages**: [yaml, cloudformation]
- EBS volumes should be encrypted
- Remediation: Set `Encrypted: true`

---

## Lambda Patterns

### Lambda Without VPC
**Pattern**: `(?i)Type:\s*AWS::Lambda::Function(?:(?!VpcConfig).)*$`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, cloudformation]
- Lambda functions accessing private resources should be in VPC
- Remediation: Add VpcConfig with appropriate subnets

### Lambda Timeout Too High
**Pattern**: `(?i)Timeout:\s*(?:[6-9][0-9]{2}|[1-9][0-9]{3,})`
**Type**: regex
**Severity**: low
**Languages**: [yaml, cloudformation]
- Lambda timeout should be appropriate for the function
- Remediation: Set reasonable timeout based on function needs

---

## Logging and Monitoring

### CloudTrail Not Enabled
**Pattern**: `(?i)IsLogging:\s*(?:false|'false'|"false")`
**Type**: regex
**Severity**: high
**Languages**: [yaml, cloudformation]
- CloudTrail should be enabled
- Remediation: Set `IsLogging: true`

### CloudWatch Logs Not Encrypted
**Pattern**: `(?i)Type:\s*AWS::Logs::LogGroup(?:(?!KmsKeyId).)*$`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, cloudformation]
- CloudWatch Logs should be encrypted with KMS
- Remediation: Add KmsKeyId property

---

## Organizational Policies

### Missing DeletionPolicy
**Pattern**: `(?i)Type:\s*AWS::(?:RDS::DBInstance|S3::Bucket)(?:(?!DeletionPolicy).)*$`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, cloudformation]
- Critical resources should have DeletionPolicy
- Remediation: Add `DeletionPolicy: Retain` or `Snapshot`

### Missing Tags
**Pattern**: `(?i)Type:\s*AWS::(?:(?!Tags).)*$`
**Type**: regex
**Severity**: low
**Languages**: [yaml, cloudformation]
- Resources should be tagged for management
- Remediation: Add Tags including Environment, Owner, Project

### Using Default KMS Key
**Pattern**: `(?i)KmsKeyId:\s*(?:alias/aws/|aws/)`
**Type**: regex
**Severity**: medium
**Languages**: [yaml, cloudformation]
- Use customer-managed KMS keys for better control
- Remediation: Create and use customer-managed KMS key

---

## References

- [CWE-732: Incorrect Permission Assignment](https://cwe.mitre.org/data/definitions/732.html)
- [CWE-311: Missing Encryption of Sensitive Data](https://cwe.mitre.org/data/definitions/311.html)
- [CIS AWS Foundations Benchmark](https://www.cisecurity.org/benchmark/amazon_web_services)
