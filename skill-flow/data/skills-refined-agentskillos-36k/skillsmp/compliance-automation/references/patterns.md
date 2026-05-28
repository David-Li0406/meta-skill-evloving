# Compliance Automation

## Patterns

### **Golden Rules**
  
---
    ##### **Rule**
Policies in version control
    ##### **Reason**
Audit trail, peer review, rollback
  
---
    ##### **Rule**
Evidence immutable once collected
    ##### **Reason**
Prevents tampering, maintains integrity
  
---
    ##### **Rule**
Continuous > periodic assessment
    ##### **Reason**
Drift detected in minutes, not months
  
---
    ##### **Rule**
Controls map to frameworks
    ##### **Reason**
One control satisfies multiple frameworks
  
---
    ##### **Rule**
Automate evidence collection
    ##### **Reason**
Manual collection doesn't scale
### **Control Status**
  - pass
  - fail
  - not_applicable
  - error
### **Severity Levels**
  #### **Critical**
Immediate action required
  #### **High**
Action within 24 hours
  #### **Medium**
Action within 1 week
  #### **Low**
Informational
### **Evidence Types**
  - screenshot
  - log_export
  - config_snapshot
  - api_response
  - report
  - attestation
### **Common Frameworks**
  #### **Soc2**
    ##### **Full Name**
SOC 2 Type II
    ##### **Focus**
Trust Service Criteria
    ##### **Controls**
CC series
  #### **Iso27001**
    ##### **Full Name**
ISO 27001
    ##### **Focus**
Information Security Management
    ##### **Controls**
Annex A
  #### **Pci Dss**
    ##### **Full Name**
PCI DSS
    ##### **Focus**
Payment Card Security
    ##### **Controls**
12 requirements
  #### **Hipaa**
    ##### **Full Name**
HIPAA
    ##### **Focus**
Healthcare Data Protection
    ##### **Controls**
Administrative, Physical, Technical
### **Ccm Components**
  #### **Policy Engine**
OPA Rego rules
  #### **Evidence Collector**
Automated artifact gathering
  #### **Continuous Monitoring**
Real-time assessment
  #### **Drift Detection**
Baseline comparison
  #### **Alerting**
Violation notifications

## Anti-Patterns


---
  #### **Pattern**
Manual evidence collection
  #### **Problem**
Doesn't scale, error-prone
  #### **Solution**
Automated collectors with scheduling

---
  #### **Pattern**
Point-in-time audits
  #### **Problem**
Drift undetected between audits
  #### **Solution**
Continuous monitoring

---
  #### **Pattern**
Policies in documentation
  #### **Problem**
Can't be enforced automatically
  #### **Solution**
Policy-as-code with OPA

---
  #### **Pattern**
Siloed compliance
  #### **Problem**
Duplicated effort per framework
  #### **Solution**
Unified control framework

---
  #### **Pattern**
Evidence in email/tickets
  #### **Problem**
Not immutable, hard to find
  #### **Solution**
Centralized evidence store with integrity