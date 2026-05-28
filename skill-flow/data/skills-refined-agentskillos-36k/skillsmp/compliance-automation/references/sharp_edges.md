# Compliance Automation - Sharp Edges

## Evidence Can Be Modified After Collection

### **Id**
evidence-tampering
### **Severity**
critical
### **Summary**
Audit evidence stored in mutable storage undermines integrity
### **Symptoms**
  - Evidence files can be edited
  - No hash verification
  - Auditor questions evidence authenticity
### **Why**
  Compliance evidence must be immutable to prove it wasn't altered after
  collection. If evidence can be modified, its value is zero - auditors
  can't trust it, and you can't prove your controls were working.
  
### **Gotcha**
  "Here's our evidence from last month"
  "How do I know this wasn't modified?"
  "It's in our S3 bucket..."
  "Can anyone edit that bucket?"
  "..."
  
  # Evidence is worthless if it can be tampered with
  
### **Solution**
  1. Immutable storage:
     - S3 Object Lock (GOVERNANCE or COMPLIANCE mode)
     - Azure Immutable Blob Storage
     - Write-once storage
  
  2. Integrity verification:
     - SHA-256 hash at collection
     - Hash stored separately
     - Verify before audit
  
  3. Chain of custody:
     - Log all access
     - Timestamp with trusted time source
     - Digital signatures
  

## Policies Don't Match Current Infrastructure

### **Id**
stale-policies
### **Severity**
high
### **Summary**
Policy-as-code hasn't been updated as infrastructure evolved
### **Symptoms**
  - New resources not covered by policies
  - Policies reference deprecated configurations
  - False negatives in compliance checks
### **Why**
  Infrastructure changes constantly - new services, renamed resources,
  changed configurations. If policies aren't updated, they silently
  stop checking what matters. You think you're compliant, but you're not.
  
### **Gotcha**
  "We passed all compliance checks"
  "What about the new Kubernetes cluster?"
  "It's not in our policies yet"
  "So it's completely unchecked?"
  
  # New infrastructure deployed without compliance coverage
  
### **Solution**
  1. Policy CI/CD:
     - Policies version-controlled
     - Review policies on infrastructure changes
     - Automated policy testing
  
  2. Coverage monitoring:
     - Track resource types vs policy coverage
     - Alert on new uncovered resources
     - Require policies before production
  
  3. Regular audits:
     - Quarterly policy review
     - Compare against infrastructure inventory
     - Update policies proactively
  

## Checking Compliance But Not Enforcing

### **Id**
compliance-theater
### **Severity**
high
### **Summary**
Violations are detected but nothing happens
### **Symptoms**
  - Dashboard shows failures
  - No remediation workflow
  - Same violations for months
### **Why**
  Compliance monitoring is useless if violations aren't addressed.
  If you detect problems but don't fix them, you're just documenting
  your non-compliance - which is worse than not knowing.
  
### **Gotcha**
  "Our compliance dashboard shows 47 critical violations"
  "How long have they been there?"
  "Some for 6 months"
  "Why weren't they fixed?"
  "Nobody assigned to remediation"
  
  # Detecting problems without fixing them is compliance theater
  
### **Solution**
  1. Automated remediation:
     - Auto-fix low-risk violations
     - Auto-create tickets for others
     - SLA for remediation
  
  2. Enforcement:
     - Block non-compliant deployments
     - Require exception approval
     - Time-bound exceptions only
  
  3. Accountability:
     - Violations assigned to owners
     - Escalation for overdue items
     - Executive visibility
  

## Scrambling Before Annual Audit

### **Id**
annual-audit-panic
### **Severity**
medium
### **Summary**
Evidence collection is a last-minute fire drill
### **Symptoms**
  - Weeks of audit prep
  - Missing evidence scramble
  - Evidence created retroactively
### **Why**
  If you're only collecting evidence before audits, you're proving you
  can scramble under pressure - not that your controls work year-round.
  Continuous compliance means the audit is just a review of existing data.
  
### **Gotcha**
  "Audit is next month!"
  "Time to collect evidence"
  "But the logs from January were purged"
  "And we changed our access process in March"
  "And nobody documented the old one"
  
  # Annual panic reveals continuous compliance failure
  
### **Solution**
  1. Continuous evidence collection:
     - Automated daily/weekly collection
     - Stored with retention policies
     - Never delete before audit
  
  2. Always audit-ready:
     - Evidence available instantly
     - Dashboards show current state
     - No special prep needed
  
  3. Process discipline:
     - Document process changes immediately
     - Evidence generated as side effect
     - Real-time compliance visibility
  