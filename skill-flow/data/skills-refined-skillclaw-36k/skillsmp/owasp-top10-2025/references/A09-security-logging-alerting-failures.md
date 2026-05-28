# A09 Security Logging and Alerting Failures

## Background

This vulnerability category maintains **9th position** in OWASP Top 10:2025, holding its position from the previous list. The name has been updated to emphasize the role of alerts in triggering responses to security events.

### Statistics
| Item | Value |
|------|-------|
| Mapped CWEs | 5 |
| Max Incidence Rate | 11.33% |
| Avg Incidence Rate | 3.91% |
| Avg Weighted Impact | 2.65 |
| Total CVEs | 723 |

### Characteristics
Despite minimal CVE representation, this category has significant impact on incident detection and forensic capabilities.

## Description

The core issue is **inadequate logging, monitoring, and alerting mechanisms** that prevent organizations from detecting breaches and responding effectively.

### Logging Flaws

1. **Inconsistent Logging of Auditable Events**: Logins, failed authentication attempts, transactions
2. **Inadequate or Unclear Log Messages for Warnings and Errors**
3. **Unprotected Log Integrity Vulnerable to Tampering**
4. **Local-Only Storage Without Proper Backups**

### Monitoring and Detection Failures

5. **No Real-Time or Near Real-Time Attack Detection Capabilities**
6. **Unmonitored Application and API Logs**
7. **Missing or Ineffective Alerting Thresholds**
8. **Penetration Testing Tools Not Triggering Alerts**

### Sensitive Data Risks

9. **Logging Sensitive Information (PII or PHI) That Should Not Be Logged**
10. **Log Visibility to Unauthorized Users or Attackers**

### Operational Issues

11. **Incomplete Error and Exception Handling**
12. **Outdated or Missing Alerting Use Cases**
13. **Excessive False Positives Overwhelming SOC Teams**
14. **Incomplete Incident Playbooks**

## How to Prevent

### Implementation Controls

#### Logging Foundation
1. **Log All Login Attempts, Access Control Failures, and Validation Failures with Sufficient User Context**
2. **Document Security Control Outcomes (Both Successes and Failures)**
3. **Ensure Log Data is Properly Encoded to Prevent Injection or Attacks on Logging or Monitoring Systems**
4. **Generate Logs in Formats Compatible with Management Solutions**

#### Data Integrity
5. **Ensure Audit Trails with Integrity Controls to Prevent Tampering or Deletion**: Append-only database tables or similar approaches
6. **Implement Rollback Mechanisms for Failed Transactions**

#### Alerting Strategy
7. **Establish Behavioral Monitoring for Suspicious Activity**
8. **Develop Developer Guidelines for Alert Implementation**
9. **Create Honeytokens to Catch Attackers Without False Positives**

#### Organizational Approach
10. **Have DevSecOps Teams Establish Effective Monitoring Use Cases with Documented Playbooks**
11. **Implement or Adopt Incident Response Frameworks (NIST 800-61r2 or higher)**
12. **Train Developers in Application Attack Awareness**
13. **Consider AI/Behavioral Analysis Tools to Reduce False Positives**

### Technical Solutions

Available tools:
- OWASP ModSecurity Core Rule Set
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Commercial observability platforms supporting real-time attack response

## Example Attack Scenarios

### Scenario #1 - Children's Health Plan Breach
```
A health plan operator experienced a massive breach affecting 3.5 million children's records.
Absence of monitoring and logging allowed the breach to persist
"since 2013, a period of more than 7 years" before detection.
Post-mortem review revealed developers had not addressed critical vulnerabilities.
```

### Scenario #2 - Airline Data Exposure
```
A major Indian airline suffered a breach of 10 years of passenger data
(passports, credit cards) from a third-party cloud provider.
The breach was discovered only after external notification.
```

### Scenario #3 - GDPR Violation
```
A European airline experienced a GDPR-reportable breach through
payment application exploitation that compromised over 400,000 customer payment records,
resulting in a £20 million regulatory fine.
```

## References

- [OWASP Proactive Controls: C9: Implement Logging and Monitoring](https://owasp.org/www-project-proactive-controls/)
- [OWASP ASVS: V16 Security Logging and Error Handling](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP Cheat Sheet: Application Logging Vocabulary](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Vocabulary_Cheat_Sheet.html)
- [OWASP Cheat Sheet: Logging](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- [NIST SP 1800-11: Data Integrity—Recovering from Ransomware](https://www.nccoe.nist.gov/projects/building-blocks/data-integrity/recover)
- [NIST SP 1800-25: Data Integrity—Identifying and Protecting Assets](https://www.nccoe.nist.gov/projects/building-blocks/data-integrity/identify-protect)
- [NIST SP 1800-26: Data Integrity—Detecting and Responding to Ransomware](https://www.nccoe.nist.gov/projects/building-blocks/data-integrity/detect-respond)
- [Huntress Threat Library: Real-World Snowflake Breach Cases](https://www.huntress.com/threat-library)

## List of Mapped CWEs

| CWE ID | Description |
|--------|-------------|
| [CWE-117](https://cwe.mitre.org/data/definitions/117.html) | Improper Output Neutralization for Logs |
| [CWE-221](https://cwe.mitre.org/data/definitions/221.html) | Information Loss or Omission |
| [CWE-223](https://cwe.mitre.org/data/definitions/223.html) | Omission of Security-relevant Information |
| [CWE-532](https://cwe.mitre.org/data/definitions/532.html) | Insertion of Sensitive Information into Log File |
| [CWE-778](https://cwe.mitre.org/data/definitions/778.html) | Insufficient Logging |
