---
name: cloud-collector
description: Automated compliance evidence collection for AWS, GCP, and Azure with SOC 2, ISO 27001, NIST 800-53, and CIS benchmark mappings.
---

# Evidence Collector Skill

Automated compliance evidence collection for AWS, GCP, and Azure cloud environments.

## When to Activate

Activate this skill when the user:
- Asks to collect compliance evidence
- Mentions SOC 2, ISO 27001, NIST 800-53, or CIS benchmarks
- Requests audit documentation or evidence packages
- Wants to verify security configurations across cloud providers
- Asks about IAM policies, logging, encryption, or network security evidence

## Prerequisites

Before running evidence collection, ensure:

1. **AWS**: Valid AWS credentials configured via:
   - Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
   - AWS credentials file (`~/.aws/credentials`)
   - IAM role (if running on EC2/Lambda)
   - Required permissions: `iam:Get*`, `iam:List*`, `cloudtrail:Describe*`, `cloudtrail:Get*`, `s3:GetBucket*`, `s3:ListBucket`, `securityhub:Get*`, `kms:Describe*`, `kms:List*`, `ec2:Describe*`

2. **GCP**: Valid GCP credentials configured via:
   - Application Default Credentials (`gcloud auth application-default login`)
   - Service account key file (`GOOGLE_APPLICATION_CREDENTIALS`)
   - Required roles: `roles/iam.securityReviewer`, `roles/logging.viewer`, `roles/storage.objectViewer`, `roles/securitycenter.findingsViewer`, `roles/cloudkms.viewer`, `roles/compute.viewer`

3. **Azure**: Valid Azure credentials configured via:
   - Azure CLI (`az login`)
   - Service principal environment variables
   - Required roles: `Reader`, `Security Reader`, `Key Vault Reader`

## Usage Patterns

### Collect All Evidence for a Cloud Provider

```python
from scripts.aws_evidence import AWSEvidenceCollector
from scripts.output_formatter import EvidenceFormatter

# Collect AWS evidence
collector = AWSEvidenceCollector()
package = collector.collect_all()

# Output as JSON
print(EvidenceFormatter.to_json(package))

# Output as Markdown report
print(EvidenceFormatter.to_markdown(package))

# Save to files
EvidenceFormatter.save(package, "./evidence_output")
```

### Collect Specific Evidence Categories

```python
from scripts.aws_evidence import AWSEvidenceCollector

collector = AWSEvidenceCollector()

# Collect only IAM evidence
iam_evidence = collector.collect_iam()

# Collect only logging evidence
logging_evidence = collector.collect_cloudtrail()

# Collect encryption evidence
encryption_evidence = collector.collect_kms()
```

### Multi-Cloud Collection

```python
from scripts.aws_evidence import AWSEvidenceCollector
from scripts.gcp_evidence import GCPEvidenceCollector
from scripts.azure_evidence import AzureEvidenceCollector
from scripts.output_formatter import EvidenceFormatter

# Collect from all providers
aws_package = AWSEvidenceCollector().collect_all()
gcp_package = GCPEvidenceCollector(project_id="my-project").collect_all()
azure_package = AzureEvidenceCollector(subscription_id="sub-id").collect_all()

# Save all packages
for package in [aws_package, gcp_package, azure_package]:
    EvidenceFormatter.save(package, "./evidence_output")
```

## Evidence Categories

Each cloud provider collector gathers evidence in these categories:

| Category | Description | Controls Supported |
|----------|-------------|-------------------|
| **IAM** | Identity policies, roles, users, groups | CC6.1, CC6.2, CC6.3, A.9.2, AC-2, AC-3 |
| **Logging** | Audit trails, log configurations | CC7.2, A.12.4, AU-2, AU-3, AU-12 |
| **Storage** | Bucket/blob policies, access controls | CC6.1, A.8.2, AC-3, SC-28 |
| **Security** | Security findings, vulnerabilities | CC7.1, A.12.6, SI-4, RA-5 |
| **Encryption** | Key management, encryption configs | CC6.1, A.10.1, SC-12, SC-13 |
| **Network** | Firewall rules, security groups, NSGs | CC6.6, A.13.1, SC-7, AC-4 |

## Output Formats

### JSON Output

Structured JSON following the schema in `references/evidence_schema.json`. Suitable for:
- Automated processing
- Integration with GRC tools
- Long-term evidence storage

### Markdown Output

Human-readable report with:
- Metadata summary
- Evidence grouped by category
- Control mapping tables with status indicators
- Suitable for auditor review and documentation

## Control Framework Mappings

Evidence is automatically mapped to controls from:

- **SOC 2 Type II**: CC (Common Criteria) series
- **ISO 27001**: Annex A controls
- **NIST 800-53**: Security and privacy controls
- **CIS Benchmarks**: Cloud-specific benchmarks

See `references/control_mappings.md` for complete mapping details.

## Error Handling

The collectors handle common errors gracefully:

- **Missing Permissions**: Logs warning, continues with available data
- **API Rate Limits**: Implements exponential backoff
- **Region Unavailable**: Skips region, notes in output
- **Resource Not Found**: Records as "not configured" evidence

## Best Practices

1. **Run with least privilege**: Use read-only credentials
2. **Scope appropriately**: Collect only what you need for the audit
3. **Timestamp everything**: Evidence is timestamped automatically
4. **Version control outputs**: Store evidence packages in version control
5. **Review before submission**: Always review collected evidence before sharing with auditors
