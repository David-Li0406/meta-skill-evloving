# Data Governance

## Patterns

### **Golden Rules**
  
---
    ##### **Rule**
Data is a business asset
    ##### **Reason**
Treat it with same rigor as financial assets
  
---
    ##### **Rule**
Accountability must be clear
    ##### **Reason**
Every data element needs an owner
  
---
    ##### **Rule**
Quality is everyone's job
    ##### **Reason**
Not just a technical problem
  
---
    ##### **Rule**
Automate where possible
    ##### **Reason**
Manual governance doesn't scale
  
---
    ##### **Rule**
Measure outcomes
    ##### **Reason**
Track data quality, usage, value
### **Governance Roles**
  #### **Cdo**
    ##### **Description**
Executive sponsor for data governance
    ##### **Accountability**
Overall program success
  #### **Data Owner**
    ##### **Description**
Business leader accountable for data domain
    ##### **Accountability**
Data quality and compliance in domain
  #### **Data Steward**
    ##### **Description**
Day-to-day data quality and metadata
    ##### **Accountability**
Operational data quality
  #### **Data Custodian**
    ##### **Description**
Technical management of data storage
    ##### **Accountability**
Technical data security and availability
### **Quality Dimensions**
  #### **Completeness**
Are all required values present?
  #### **Accuracy**
Are values correct?
  #### **Consistency**
Are values consistent across systems?
  #### **Timeliness**
Is data current and updated timely?
  #### **Validity**
Do values conform to rules?
  #### **Uniqueness**
Are duplicates managed?
### **Data Classification**
  #### **Public**
Freely available
  #### **Internal**
Internal use only
  #### **Confidential**
Restricted access
  #### **Restricted**
Highly sensitive
  #### **Pii**
Personally identifiable information
  #### **Phi**
Protected health information

## Anti-Patterns


---
  #### **Pattern**
No ownership
  #### **Problem**
Nobody accountable for data issues
  #### **Solution**
Assign clear data owners

---
  #### **Pattern**
Documentation only
  #### **Problem**
Policies exist but not enforced
  #### **Solution**
Automate enforcement

---
  #### **Pattern**
IT-only governance
  #### **Problem**
Business not engaged
  #### **Solution**
Embed in business processes

---
  #### **Pattern**
Big bang rollout
  #### **Problem**
Try to govern everything at once
  #### **Solution**
Start with critical data domains

---
  #### **Pattern**
Quality as afterthought
  #### **Problem**
Check quality at consumption
  #### **Solution**
Shift left, check at source

---
  #### **Pattern**
Manual lineage
  #### **Problem**
Lineage outdated immediately
  #### **Solution**
Auto-capture from pipelines