# Control Mappings Reference

This document maps evidence categories to compliance framework controls.

## Evidence Categories to Controls Matrix

### Identity and Access Management (IAM)

| Framework | Control ID | Control Name | Evidence Collected |
|-----------|------------|--------------|-------------------|
| **SOC 2** | CC6.1 | Logical Access Security | IAM policies, users, roles, MFA status |
| **SOC 2** | CC6.2 | Access Provisioning | User creation dates, role assignments |
| **SOC 2** | CC6.3 | Access Removal | User status, access key status |
| **ISO 27001** | A.9.2.1 | User Registration | User inventory, creation dates |
| **ISO 27001** | A.9.2.2 | User Access Provisioning | Role assignments, permission sets |
| **ISO 27001** | A.9.2.3 | Privileged Access Management | Admin roles, elevated permissions |
| **NIST 800-53** | AC-2 | Account Management | User accounts, service accounts |
| **NIST 800-53** | AC-3 | Access Enforcement | IAM policies, permission boundaries |
| **NIST 800-53** | AC-6 | Least Privilege | Role definitions, custom roles |
| **CIS** | 1.1-1.4 | Identity & Access | Password policy, MFA, access keys |

### Logging and Monitoring

| Framework | Control ID | Control Name | Evidence Collected |
|-----------|------------|--------------|-------------------|
| **SOC 2** | CC7.2 | System Monitoring | CloudTrail/Audit Logs/Activity Logs config |
| **SOC 2** | CC7.3 | Security Event Analysis | Log sinks, metrics, alerts |
| **ISO 27001** | A.12.4.1 | Event Logging | Trail/sink configurations |
| **ISO 27001** | A.12.4.2 | Protection of Log Info | Log encryption, retention |
| **ISO 27001** | A.12.4.3 | Admin/Operator Logs | Admin activity logging |
| **NIST 800-53** | AU-2 | Audit Events | Logged event types |
| **NIST 800-53** | AU-3 | Content of Audit Records | Log detail level |
| **NIST 800-53** | AU-6 | Audit Review/Analysis | Log analysis configuration |
| **NIST 800-53** | AU-12 | Audit Generation | Log generation status |
| **CIS** | 2.x/3.x/5.x | Logging | Cloud-specific logging benchmarks |

### Storage Security

| Framework | Control ID | Control Name | Evidence Collected |
|-----------|------------|--------------|-------------------|
| **SOC 2** | CC6.1 | Logical Access | Bucket/blob policies |
| **SOC 2** | CC6.7 | Data Protection | Encryption, versioning |
| **ISO 27001** | A.8.2.3 | Handling of Assets | Storage classification, access |
| **ISO 27001** | A.13.2.1 | Info Transfer Policies | Public access blocks |
| **NIST 800-53** | AC-3 | Access Enforcement | Bucket policies, ACLs |
| **NIST 800-53** | SC-28 | Protection at Rest | Encryption configuration |
| **CIS** | 2.x/3.x/5.x | Storage | Cloud-specific storage benchmarks |

### Security Monitoring & Vulnerability Management

| Framework | Control ID | Control Name | Evidence Collected |
|-----------|------------|--------------|-------------------|
| **SOC 2** | CC7.1 | Detection of Changes | Security Hub/SCC/Defender findings |
| **SOC 2** | CC7.2 | Monitoring | Security alerts, monitoring config |
| **ISO 27001** | A.12.6.1 | Technical Vulnerability Mgmt | Vulnerability findings |
| **ISO 27001** | A.18.2.3 | Technical Compliance Review | Security standards compliance |
| **NIST 800-53** | SI-4 | System Monitoring | Security monitoring status |
| **NIST 800-53** | RA-5 | Vulnerability Scanning | Scan results, findings |
| **CIS** | 4.x/7.x | Security | Cloud-specific security benchmarks |

### Encryption & Key Management

| Framework | Control ID | Control Name | Evidence Collected |
|-----------|------------|--------------|-------------------|
| **SOC 2** | CC6.1 | Logical Access | Key access policies |
| **SOC 2** | CC6.7 | Encryption | Key configurations |
| **ISO 27001** | A.10.1.1 | Cryptographic Policy | KMS policies |
| **ISO 27001** | A.10.1.2 | Key Management | Key rotation, lifecycle |
| **NIST 800-53** | SC-12 | Cryptographic Key Mgmt | Key management config |
| **NIST 800-53** | SC-13 | Cryptographic Protection | Encryption usage |
| **CIS** | 1.x/2.x/8.x | Encryption | Cloud-specific encryption benchmarks |

### Network Security

| Framework | Control ID | Control Name | Evidence Collected |
|-----------|------------|--------------|-------------------|
| **SOC 2** | CC6.6 | Security Over Networks | Security groups, firewall rules |
| **SOC 2** | CC6.7 | External Threats | Network ACLs, perimeter controls |
| **ISO 27001** | A.13.1.1 | Network Controls | VPC/VNet configurations |
| **ISO 27001** | A.13.1.3 | Network Segregation | Subnet configuration |
| **NIST 800-53** | SC-7 | Boundary Protection | Firewall rules, NSGs |
| **NIST 800-53** | AC-4 | Information Flow | Network flow rules |
| **CIS** | 3.x/5.x/6.x | Networking | Cloud-specific network benchmarks |

---

## SOC 2 Type II Controls Reference

### Common Criteria (CC) Series

| Control | Name | Description |
|---------|------|-------------|
| CC6.1 | Logical Access Security | Logical access security software, infrastructure, and architectures |
| CC6.2 | Access Provisioning | Prior to issuing system credentials and granting system access, registers authorized users |
| CC6.3 | Access Removal | Removes access to system components timely when access is no longer authorized |
| CC6.6 | Security Over Networks | Prevents unauthorized access from outside system boundaries |
| CC6.7 | External Threats | Restricts transmission and removal of information to authorized addresses |
| CC7.1 | Detection of Changes | Detects and monitors configuration changes that could introduce vulnerabilities |
| CC7.2 | System Monitoring | Monitors system components for anomalies and indicators of compromise |
| CC7.3 | Security Event Analysis | Analyzes anomalies and indicators of compromise to determine responses |

---

## ISO 27001:2022 Annex A Controls Reference

### A.9 - Access Control

| Control | Name |
|---------|------|
| A.9.2.1 | User Registration and De-registration |
| A.9.2.2 | User Access Provisioning |
| A.9.2.3 | Management of Privileged Access Rights |
| A.9.4.3 | Password Management System |

### A.10 - Cryptography

| Control | Name |
|---------|------|
| A.10.1.1 | Policy on Use of Cryptographic Controls |
| A.10.1.2 | Key Management |

### A.12 - Operations Security

| Control | Name |
|---------|------|
| A.12.4.1 | Event Logging |
| A.12.4.2 | Protection of Log Information |
| A.12.4.3 | Administrator and Operator Logs |
| A.12.6.1 | Management of Technical Vulnerabilities |

### A.13 - Communications Security

| Control | Name |
|---------|------|
| A.13.1.1 | Network Controls |
| A.13.1.3 | Segregation in Networks |
| A.13.2.1 | Information Transfer Policies |

### A.18 - Compliance

| Control | Name |
|---------|------|
| A.18.2.3 | Technical Compliance Review |

---

## NIST 800-53 Rev. 5 Controls Reference

### Access Control (AC)

| Control | Name |
|---------|------|
| AC-2 | Account Management |
| AC-3 | Access Enforcement |
| AC-4 | Information Flow Enforcement |
| AC-6 | Least Privilege |

### Audit and Accountability (AU)

| Control | Name |
|---------|------|
| AU-2 | Audit Events |
| AU-3 | Content of Audit Records |
| AU-6 | Audit Review, Analysis, and Reporting |
| AU-12 | Audit Generation |

### Risk Assessment (RA)

| Control | Name |
|---------|------|
| RA-5 | Vulnerability Scanning |

### System and Communications Protection (SC)

| Control | Name |
|---------|------|
| SC-7 | Boundary Protection |
| SC-12 | Cryptographic Key Establishment and Management |
| SC-13 | Cryptographic Protection |
| SC-28 | Protection of Information at Rest |

### System and Information Integrity (SI)

| Control | Name |
|---------|------|
| SI-4 | System Monitoring |

---

## CIS Benchmark Mappings

### AWS CIS Benchmark v2.0

| Section | Focus Area |
|---------|------------|
| 1.x | Identity and Access Management |
| 2.x | Storage |
| 3.x | Logging |
| 4.x | Monitoring |
| 5.x | Networking |

### GCP CIS Benchmark v2.0

| Section | Focus Area |
|---------|------------|
| 1.x | Identity and Access Management |
| 2.x | Logging and Monitoring |
| 3.x | Virtual Machines |
| 4.x | Cloud SQL |
| 5.x | Storage |
| 6.x | Cloud DNS |
| 7.x | BigQuery |

### Azure CIS Benchmark v2.0

| Section | Focus Area |
|---------|------------|
| 1.x | Identity and Access Management |
| 2.x | Microsoft Defender |
| 3.x | Storage Accounts |
| 4.x | Database Services |
| 5.x | Logging and Monitoring |
| 6.x | Networking |
| 7.x | Virtual Machines |
| 8.x | Key Vault |
| 9.x | App Service |

---

## Using Control Mappings

When generating evidence packages, the collector automatically maps collected evidence to relevant controls. The mapping is based on:

1. **Evidence Category**: Each evidence item is categorized (iam, logging, storage, etc.)
2. **Framework Selection**: Mappings are provided for all supported frameworks
3. **Control Status**: Each control is marked as:
   - `collected`: Evidence available
   - `partial`: Some evidence available
   - `missing`: No evidence collected

### Example Evidence Package Control Mapping

```json
{
  "control_mappings": [
    {
      "framework": "soc2",
      "control_id": "CC6.1",
      "control_name": "Logical Access Security",
      "evidence_ids": ["aws-iam-password-policy", "aws-iam-users", "aws-iam-roles"],
      "status": "collected"
    }
  ]
}
```
