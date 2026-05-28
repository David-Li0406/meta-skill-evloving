# SOX Compliance

## Patterns

### **Golden Rules**
  
---
    ##### **Rule**
Tone at the top
    ##### **Reason**
Control environment starts with leadership
  
---
    ##### **Rule**
Segregation of duties
    ##### **Reason**
No single person controls entire process
  
---
    ##### **Rule**
Evidence everything
    ##### **Reason**
If it's not documented, it didn't happen
  
---
    ##### **Rule**
Continuous monitoring
    ##### **Reason**
Point-in-time testing misses issues
  
---
    ##### **Rule**
Risk-based approach
    ##### **Reason**
Focus controls on material risks
### **Coso Framework**
  #### **Control Environment**
    - Integrity and ethical values
    - Board independence and oversight
    - Organizational structure
    - Commitment to competence
    - Accountability
  #### **Risk Assessment**
    - Specify objectives
    - Identify and analyze risks
    - Assess fraud risk
    - Identify significant changes
  #### **Control Activities**
    - Select and develop controls
    - Select and develop technology controls
    - Deploy through policies and procedures
  #### **Information Communication**
    - Use relevant quality information
    - Communicate internally
    - Communicate externally
  #### **Monitoring**
    - Conduct ongoing evaluations
    - Evaluate and communicate deficiencies
### **Itgc Controls**
  #### **Access Controls**
    - User provisioning and deprovisioning
    - Privileged access management
    - Password policies
    - Access reviews (quarterly)
  #### **Change Management**
    - Change request documentation
    - Testing and approval
    - Segregation of duties
    - Emergency change procedures
  #### **Backup Recovery**
    - Backup procedures and schedules
    - Restoration testing
    - Offsite storage
    - Business continuity plans
  #### **Operations**
    - Job scheduling
    - Incident management
    - Problem resolution
    - Batch processing controls
### **Deficiency Levels**
  #### **Deficiency**
    ##### **Definition**
Control doesn't operate as designed
    ##### **Impact**
Document and remediate
  #### **Significant Deficiency**
    ##### **Definition**
More than remote likelihood of material misstatement
    ##### **Impact**
Report to audit committee
  #### **Material Weakness**
    ##### **Definition**
Reasonable possibility of material misstatement
    ##### **Impact**
Public disclosure required

## Anti-Patterns


---
  #### **Pattern**
Shared credentials
  #### **Problem**
No individual accountability
  #### **Solution**
Unique user IDs, no shared accounts

---
  #### **Pattern**
Admin access for developers
  #### **Problem**
No segregation of duties
  #### **Solution**
Separate dev, test, prod access

---
  #### **Pattern**
Manual spreadsheet controls
  #### **Problem**
Error prone, no audit trail
  #### **Solution**
Automate controls with logging

---
  #### **Pattern**
Point-in-time testing
  #### **Problem**
Misses control failures between tests
  #### **Solution**
Continuous monitoring

---
  #### **Pattern**
Undocumented exceptions
  #### **Problem**
No audit trail for deviations
  #### **Solution**
Formal exception process with approval